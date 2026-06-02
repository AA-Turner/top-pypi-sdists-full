#!/usr/bin/env python3

"""cmk-check-plugins"""
# ruff: noqa: RUF100 Unused `noqa` directive

# Not yet implemented:
# - [ ] accept directories rather than discrete files for walks and agent outputs
# - [ ] performance measurements
# - [ ] HaSI

# try:
#     import debugpy  # noqa: T100 Import for `debugpy` found
# except ImportError:
#     debugpy = None

import cProfile
import inspect
import json
import logging
import pstats
import re
import sys
import tempfile
import time
from argparse import ArgumentParser
from argparse import Namespace as Args
from collections import defaultdict
from collections.abc import Iterable, Mapping, MutableMapping, Sequence
from contextlib import ExitStack, suppress
from pathlib import Path
from unittest.mock import patch

import cmk.agent_based.v2

# from cmk.agent_based.v1.value_store import set_value_store_manager
from cmk.agent_based.v2 import StringTable

# from cmk.checkengine import value_store
from rich import print as rich_print
from rich import traceback
from rich.console import Console
from rich.status import Status

try:
    import cmk.utils.paths
    from cmk.agent_based.internal import evaluate_snmp_detection
    from cmk.agent_based.v1._value_store_utils import GetRateError
    from cmk.base import config
    from cmk.ccc.hostaddress import HostAddress, HostName
    from cmk.checkengine.plugins import AgentBasedPlugins, SNMPSectionPlugin
    from cmk.fetchers.snmp_backend import StoredWalkSNMPBackend
    from cmk.snmplib import (
        BackendSNMPTree,
        SNMPBackendEnum,
        SNMPHostConfig,
        SNMPSectionName,
        SNMPVersion,
        ensure_str,
        get_snmp_table,
    )


except ModuleNotFoundError as exc:
    print(
        f"Could not load Checkmk modules ({exc}). You need to run me inside a check_mk checkout",
        file=sys.stderr,
    )
    raise SystemExit(1) from None


def parse_arguments(args: Sequence[str]) -> Args:
    """parse command line arguments and return argument object"""

    parser = ArgumentParser(
        "cmk-check-plugins",
        description="Checks check plugins",
    )
    parser.add_argument("--show-all", "-a", action="store_true")
    parser.add_argument("--suppress-duration", action="store_true")
    parser.add_argument("--filter-sections", type=str.lower)
    parser.add_argument("--raise-error", nargs="?", const="", default=None, type=str.lower)
    parser.add_argument("--ignore-error", type=str.lower, help="")
    parser.add_argument("--ignore-walks", type=str, default="")
    parser.add_argument("--error-file", nargs="?", const="errors.txt", default=None, type=Path)
    parser.add_argument("--snmp-walks", type=Path, nargs="*", default=[])
    parser.add_argument("--agent-outputs", type=Path, nargs="*", default=[])

    # apply_common_logging_cli_args(parser)

    return parser.parse_args(args)


def _snmp_host_config_from(walk_file_path: Path, encoding: None | str) -> SNMPHostConfig:
    return SNMPHostConfig(
        is_ipv6_primary=False,
        hostname=HostName(walk_file_path.name),
        ipaddress=HostAddress("127.0.0.1"),
        credentials="",
        port=0,
        bulkwalk_enabled=True,
        snmp_version=SNMPVersion.V2C,
        bulk_walk_size_of=0,
        timing={},
        oid_range_limits={},
        snmpv3_contexts=[],
        character_encoding=encoding,
        snmp_backend=SNMPBackendEnum.STORED_WALK,
        stored_walk_path=walk_file_path.parent,
    )


def _agent_based_plugins() -> Sequence[AgentBasedPlugins]:
    plugins = config.load_all_plugins()
    for error in plugins.errors:
        console.print(f"ERROR: {error}")
    if plugins.errors:
        raise SystemExit(1)
    return plugins


def _get_string_table(
    section_plugin: SNMPSectionPlugin, backend: StoredWalkSNMPBackend
) -> Sequence[StringTable]:
    return [
        get_snmp_table(
            section_name=SNMPSectionName(section_plugin.name),
            tree=BackendSNMPTree.from_frontend(base=tree.base, oids=tree.oids),
            walk_cache={},
            backend=backend,
            log=log().debug,
        )
        for tree in section_plugin.trees
    ]


def _snmp_is_detected(section_plugin: SNMPSectionPlugin, backend: StoredWalkSNMPBackend) -> bool:
    def oid_value_getter(oid: str) -> str | None:
        value = backend.get(oid, context="")
        return (
            None if value is None else ensure_str(value, encoding=backend.config.character_encoding)
        )

    return evaluate_snmp_detection(
        detect_spec=section_plugin.detect_spec,
        oid_value_getter=oid_value_getter,
    )


def _temp_file_path(path: Path, tmp_dir: Path) -> Path:
    for encoding in ("utf-8", "latin-1", "cp437"):
        try:
            content = path.read_bytes().decode(encoding)
            tmp_path = Path(tmp_dir) / path.name
            tmp_path.write_text(content, encoding="utf-8")
            return tmp_path  # noqa: TRY300 Consider moving this statement to an `else` block
        except UnicodeDecodeError:
            # rich_print(f"could not read '{path.name}' using {encoding=}: {exc}")
            pass
    raise RuntimeError(f"could not decode '{path.name}' with any encoding")


def _load_sections(lines: Iterable[str]) -> Mapping[str, Sequence[Sequence[str]]]:
    result: Mapping[str, Sequence[Sequence[str]]] = {}
    current_section_lines: None | Sequence[Sequence[str]] = None
    separator = None
    for line in lines:
        if match := re.match(
            r"^<<<(.*?)(?::sep\((.*?)\))?(?::encoding\(.*?\))?(?::persist\(.*?\))?(?::cached\(.*?\))?>>>$",
            line,
        ):
            # print(match.groups())
            section_name, separator_ord = match.groups()
            separator = separator_ord and chr(int(separator_ord))
            result[section_name] = []
            current_section_lines = result[section_name]
            continue
        if current_section_lines is None:
            continue
        current_section_lines.append(line.split(separator))
    return result


def _get_check_results(check_plugin: int, parsed_section: int, service_item: str) -> Sequence:
    # print(inspect.signature(check_plugin.check_function).parameters)
    # print(check_plugin.check_default_parameters)
    for i in reversed(range(10)):
        try:
            return list(
                check_plugin.check_function(
                    **{
                        key: {
                            "item": service_item,
                            "params": check_plugin.check_default_parameters,
                            "section": parsed_section,
                            # "value_store": {},
                        }.get(key)
                        for key in inspect.signature(check_plugin.check_function).parameters
                    }
                )
            )
        except GetRateError as exc:
            log().debug(f"{i} {exc}")
            if i == 0:
                raise
    return []


def _get_discovered_items(check_plugin: int, parsed_section: int) -> Sequence:
    # print(inspect.signature(check_plugin.discovery_function).parameters)
    # print(check_plugin.discovery_default_parameters)
    return list(
        check_plugin.discovery_function(
            **{
                key: {
                    "params": [check_plugin.discovery_default_parameters],
                    "section": parsed_section,
                }.get(key)
                for key in inspect.signature(check_plugin.discovery_function).parameters
            }
        )
    )


def check(
    cli_args: Args, status: Status, results: MutableMapping[str, object], tmp_dir: Path
) -> None:
    """Traverses SNMP and agent plugins and checks them against provided SNMP walks and agent outputs"""
    broken_walks = ",".join(  # noqa: FLY002
        (
            "switch-alcatel-6900-X20-AOS-8-4-1-233-R02,SUP-969-hr_mem-2",  # broken syntax
            # IndexError: list index out of range: return [rowinfo[0]]
            "usv-rittal-cs121,usv-piller,usv-kellser,usv-generex,usv-masterguard-4",
            # dedacted IP addresses
            "wagner-titanus-prosens,fcswitch-brocade-9,raritan-px2-dominian,pdu-raritan-2,pdu-raritan-1,firewall-checkpoint-10",
        )
    )
    # ,fcswitch-brocade-9,firewall-checkpoint-10,firewall-pfsense-1
    mocked_timestamp = time.time() // 1000 * 1000

    # quick and dirty
    value_store = dict[str, object]()

    def _get_value_store() -> dict[str, object]:
        return value_store

    cmk.agent_based.v2.get_value_store = _get_value_store

    show_all = cli_args.show_all
    filter_sections = (cli_args.filter_sections or "").split(",")
    error_file = (
        None if cli_args.error_file is None else Path(cli_args.error_file).open("w")  # noqa: SIM115 Use a context manager for opening files
    )
    ignored_errors = (
        list(filter(bool, cli_args.ignore_error.split(","))) if cli_args.ignore_error else None
    )
    raise_errors = (
        list(filter(bool, cli_args.raise_error.split(",")))
        if cli_args.raise_error is not None
        else None
    )
    ignore_walks = list(filter(bool, f"{broken_walks},{cli_args.ignore_walks}".split(",")))
    walks = [snmp_walk for snmp_walk in cli_args.snmp_walks if snmp_walk.name not in ignore_walks]
    agent_output_paths = [
        agent_output
        for agent_output in cli_args.agent_outputs
        if agent_output.name not in ignore_walks
    ]

    status.update("find plugins to check..")
    all_plugins = _agent_based_plugins()

    t0 = time.time()
    status.update("find SNMP section plugins to check..")
    snmp_section_plugins_to_check = {
        name: element
        for name, element in all_plugins.snmp_sections.items()
        if not filter_sections or any(f in name.lower() for f in filter_sections)
    }
    console.print(f"Found {len(snmp_section_plugins_to_check)} SNMP section plugins")
    for snmp_section_plugin in snmp_section_plugins_to_check.values():
        if inspect.isgeneratorfunction(snmp_section_plugin.parse_function):
            # fixme(frans): should be a warning / error
            console.print(f"[red]{snmp_section_plugin}[/]")

    status.update("find agent section plugins to check..")
    agent_section_plugins_to_check = {
        name: element
        for name, element in all_plugins.agent_sections.items()
        if not filter_sections or any(f in name.lower() for f in filter_sections)
    }
    console.print(f"Found {len(agent_section_plugins_to_check)} agent section plugins")
    for section_plugin in agent_section_plugins_to_check.values():
        if inspect.isgeneratorfunction(section_plugin.parse_function):
            console.print(f"[red]{section_plugin}[/]")

    status.update("find check plugins to check..")
    check_plugins_to_check = {  # noqa: C416 Unnecessary dict comprehension
        name: element
        for name, element in all_plugins.check_plugins.items()
        # fixme(frans): needs extra argument
        # if not filter_sections or any(f in name.lower() for f in filter_sections)
    }
    console.print(f"Found {len(check_plugins_to_check)} check plugins")

    status.update("find inventory plugins to check..")
    inventory_plugins_to_check = {
        name: element
        for name, element in all_plugins.inventory_plugins.items()
        if not filter_sections or any(f in name.lower() for f in filter_sections)
    }
    console.print(f"Found {len(inventory_plugins_to_check)} inventory plugins")

    status.update(f"pre-parse {len(agent_output_paths)} agent outputs ..")
    all_agent_sections: Mapping[str, Mapping[str, Sequence[Sequence[str]]]] = {}
    for path in agent_output_paths:
        if "LIESMICH" in path.as_posix():
            continue
        try:
            for section_name, lines in _load_sections(
                _temp_file_path(path, tmp_dir).open()
            ).items():
                files_sections = all_agent_sections.setdefault(section_name, {})
                files_sections[path] = lines
        except Exception as exc:
            raise RuntimeError(f"Could not load {path}: {exc!r}") from exc
    console.print(
        f"Found {sum(len(x) for x in all_agent_sections.values())}"
        f" sections with {len(all_agent_sections)} different section names"
        f" in {len(agent_output_paths)} agent output files"
    )

    console.print(f"Now iterate {len(agent_section_plugins_to_check)} agent section plugins ..")
    for plugin_name, agent_section_plugin in agent_section_plugins_to_check.items():
        if not (entries := all_agent_sections.get(plugin_name)):
            continue

        check_plugin = check_plugins_to_check.get(agent_section_plugin.parsed_section_name)

        if not check_plugin:  # fixme(frans): make optional
            continue

        for filename, string_table in entries.items():
            task_key = f"{plugin_name}:{Path(filename).name}"
            status_string = f"plugin=[cyan]{plugin_name}[/]:[yellow]{Path(filename).name}[/]"
            status.update(f"{status_string} ..")
            exception = None
            try:
                with patch("time.time", return_value=mocked_timestamp):
                    parsed_section = agent_section_plugin.parse_function(string_table)
                    status_string = f"{status_string} {type(parsed_section)}"
                    if not check_plugin:
                        continue

                    discovered_items = _get_discovered_items(check_plugin, parsed_section)
                    # results[task_key]["discovery"] = list(map(str, discovered_items))
                    check_results = {
                        service.item: _get_check_results(check_plugin, parsed_section, service.item)
                        for service in discovered_items
                    }

                    results[task_key]["check_results"] = {
                        # fixme(frans): sorting should be optional
                        key: sorted(map(str, value))
                        for key, value in check_results.items()
                    }
                    # out_str += f" check_result={check_result}"
            except Exception as exc:  # noqa: BLE001 broad exception (we want to catch everything here)
                exception = exc
                # raise
            finally:
                if exception:
                    console.print(f"  - ⚠️  {status_string} [red bold]{exception!r}[/]")
                    # raise  # noqa: PLE0704 Bare `raise` statement is not inside an exception handler

                console.print(f"  -    {status_string}")

    snmp_backends = {}
    console.print(
        f"Now validate {len(snmp_section_plugins_to_check)} SNMP section"
        f" plugins against {len(walks)} walks .."
    )

    for plugin_name, snmp_section_plugin in snmp_section_plugins_to_check.items():
        t0 = time.time()
        console.print(f"plugin [bold]'{plugin_name}'[/]")
        detect_count = 0
        no_detect_count = 0
        error_count = 0
        for path in walks:
            task_key = f"{plugin_name}:{path.name}"
            status.update(f"plugin=[cyan]{plugin_name}[/]:[yellow]{path.name}[/]..")
            try:
                with patch("time.time", return_value=mocked_timestamp):
                    if path not in snmp_backends:
                        snmp_backends[path] = StoredWalkSNMPBackend(
                            _snmp_host_config_from(_temp_file_path(path, tmp_dir), encoding=None),
                            log(),
                        )
                    backend = snmp_backends[path]

                    is_detected = _snmp_is_detected(snmp_section_plugin, backend)
                    out_str = f"  - {'✅' if is_detected else '❌'} walk={path.name!r:<40}"
                    # f" ({int(dur * 1_000_000)}µs)"
                    if True and is_detected:
                        string_table = _get_string_table(snmp_section_plugin, backend)
                        results[task_key]["string_table"] = string_table

                        parsed_section = snmp_section_plugin.parse_function(string_table)

                        # assert isinstance(parsed_section, dict), f"{parsed_section.__class__}"
                        match parsed_section:
                            case dict():
                                # fixme(frans): make more fine grained
                                results[task_key]["section"] = {
                                    key: str(value) for key, value in parsed_section.items()
                                }
                            case list():
                                # fixme(frans): make more fine grained
                                results[task_key]["section"] = [
                                    str(v).replace(", name=''", "") for v in parsed_section
                                ]
                            case None:
                                # fixme(frans): report error
                                raise RuntimeError(f"{plugin_name=} / {path=} {parsed_section=}")
                                continue
                            case _:
                                raise RuntimeError(f"{parsed_section.__class__}")

                        check_plugin = check_plugins_to_check.get(
                            snmp_section_plugin.parsed_section_name
                        )
                        if not check_plugin:  # fixme(frans): make optional
                            continue

                        # print(inspect.signature(check_plugin.discovery_function).parameters)
                        discovered_items = _get_discovered_items(check_plugin, parsed_section)
                        results[task_key]["discovery"] = list(map(str, discovered_items))
                        value_store = dict[str, object]()

                        check_results = {
                            service.item: _get_check_results(
                                check_plugin, parsed_section, service.item
                            )
                            for service in discovered_items
                        }
                        # out_str += f" check_result={check_result}"
                        results[task_key]["check_results"] = {
                            # fixme(frans): sorting should be optional
                            key: sorted(str(v) for v in value)
                            for key, value in check_results.items()
                        }

                        # inventory_plugin = inventory_plugins_to_check[name]

                        # print(yaml.dump(parsed_section))
                        # print(yaml.dump([i for a in parsed_section for i in a.inet6]))
                        # labels = list(host_labels_if_snmp(parsed_section))
                        # out_str += f" labels={' '.join(map(str, labels)):<50}"
                        # inventory = list(inventorize_ip_addresses_snmp(parsed_section))
                        # out_str += f" HaSI: {len(inventory)}"

                    # if True and is_detected:
                    #    parsed_section = get_parsed_snmp_section(section, backend)
                    # out_str += f" {parsed_section}"

                    if is_detected or show_all:
                        console.print(out_str)
                        # console.print(parsed_section)

                    detect_count += is_detected
                    no_detect_count += not is_detected

            except Exception as exc:
                error_count += 1
                if isinstance(exc, UnicodeDecodeError):
                    console.print(f"  - ⚠️  walk='{path.name}' [red bold]UnicodeDecodeError[/]")
                else:
                    console.print(f"  - ⚠️  walk='{path.name}' Error: [red bold]{exc!r}[/]")
                    # raise

                if not (ignored_errors and type(exc).__name__.lower() in ignored_errors):
                    if error_file:
                        error_file.write(f"{path}\n")
                    if (
                        raise_errors is not None and type(exc).__name__.lower() in raise_errors
                    ) or raise_errors == []:
                        raise

        console.print(
            f"  detected: {detect_count}, not detected: {no_detect_count}, errors: {error_count}"
            f", plugin took {int((time.time() - t0) * 1000)}ms"
        )
        # assert detect_count + no_detect_count + error_count == len(walks)


def log() -> logging.Logger:
    """Convenience function retrieves 'our' logger"""
    return logging.getLogger("trickkiste.cmk-check-plugins")


console = Console()


def main(args: None | Sequence[str] = None) -> int:
    """See main docstring"""
    traceback.install()
    cli_args = parse_arguments(args or sys.argv[1:])
    # logging.basicConfig(level=logging.DEBUG)
    # setup_logging(log(), level=cli_args.log_level, show_name=20, show_funcname=30)
    # logging.getLogger("vcr.matchers").setLevel(logging.WARNING)

    with ExitStack() as context:
        results = defaultdict(dict)
        try:
            status = context.enter_context(console.status("doing"))
            context.enter_context(suppress(KeyboardInterrupt))
            tmp_dir = Path(
                context.enter_context(tempfile.TemporaryDirectory(prefix="cwz-reencoded-"))
            )
            rich_print(
                f"Use temporary directory for re-encoded SNMP walks/agent outputs: {tmp_dir}"
            )
            profiler = cProfile.Profile()
            profiler.enable()
            try:
                check(cli_args, status, results, tmp_dir)
            finally:
                profiler.disable()
                pstats.Stats(profiler).sort_stats("cumtime").dump_stats("profile_stats.prof")
                console.print("uvx snakeviz profile_stats.prof")

        finally:
            results_path = "results.json"
            status.update(f"store {results_path}..")
            with Path("results.json").open("w") as results_file:
                json.dump(results, results_file, sort_keys=True, indent=4)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
