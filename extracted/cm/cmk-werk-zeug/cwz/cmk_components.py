#!/usr/bin/env python3

"""Checkmk-code-owners CLI
* [Brainstorming document](https://docs.google.com/document/d/1Yul9GjAIkJBowWhvIzwRFFtK-GIZfdTKMSllEzF4Juw)
* [Component Matrix Owners File Implementation](https://jira.lan.tribe29.com/browse/CMK-24954)
* [Component Ownership at Checkmk](https://docs.google.com/document/d/11pbv5J6VjdbuwDTUqBLTP2SqWsd5C1AXjgdpfjZupCM)
* [code-owners / REST API](https://android-review.googlesource.com/plugins/code-owners/Documentation/rest-api.html)
"""

# Insights we want to get:
# - [x] what components do exist?
# - [x] who's in charge of a component
# - [x] what components am I owner for?
# - [x] what files am I responsible for?
# - [x] check OWNERS files with per-file only for `set noparent`
# - [-] what files/directories belong to a component
# - [-] how do the provided ownership infos reflect the 'reality' reported by 'git blame'?
# - [-] consistency checks
# - [ ] check for redundant (nested) information
# - [ ] consequent naming (owners, leads, members)

import asyncio
import datetime
import json
import logging
import sys
import time
from argparse import ArgumentParser
from argparse import Namespace as Args
from collections.abc import AsyncIterator, Iterable, Sequence
from contextlib import ExitStack, asynccontextmanager, suppress
from itertools import count
from pathlib import Path
from typing import ClassVar, ParamSpec

import vcr  # type: ignore[import-untyped]
import yaml
from aiohttp import ClientResponseError
from rich import traceback
from rich.console import Console
from rich.status import Status
from textual import on, work
from textual.app import ComposeResult
from textual.binding import Binding
from textual.events import Click, Key
from textual.suggester import SuggestFromList
from textual.widgets import Header, Input, Label, Tree
from trickkiste.base_tui_app import TuiBaseApp
from trickkiste.logging_helper import apply_common_logging_cli_args, setup_logging
from trickkiste.misc import awatch_duration

from . import __version__
from .gerrit_utils.client import (
    CodeOwnersClient,
    Component,
    GerritClient,
    apply_code_owner_cli_args,
    with_gerrit_client,
)

STYLE_COMPONENT_NAME = "italic spring_green1 bold"
STYLE_COMPONENT_ID = "deep_sky_blue2"
STYLE_COMPONENT_DESCRIPTION = "italic yellow"
STYLE_PATH = "orchid1"
STYLE_EMAIL = "orange_red1"

ArgumentsP = ParamSpec("ArgumentsP")


def parse_arguments(args: Sequence[str]) -> Args:  # noqa: PLR0915 - too many statements
    """parse command line arguments and return argument object"""

    parser = ArgumentParser(
        "cmk-components",
        description="Provides information about components and code owners",
    )

    apply_common_logging_cli_args(parser)
    # apply_common_gerrit_cli_args(parser)  # fixme(frans): either unify or consequent implementation
    apply_code_owner_cli_args(parser)

    parser.add_argument(
        "--vcr-cache-file",
        type=Path,
        help="Cache requests replies in provided file (for debugging only!)",
    )

    parser.set_defaults(func=_fn_tui)

    subparsers = parser.add_subparsers(help="available commands", metavar="CMD")

    parser_tui = subparsers.add_parser("tui", help="Start a TUI (default)")
    parser_tui.set_defaults(func=_fn_tui)

    def add_common_args(parser: ArgumentParser) -> None:
        parser.add_argument("-v", "--verbose", action="store_true")
        parser.add_argument(
            "--mode",
            type=str,
            choices=["rich", "json", "script"],
            default="rich" if sys.stdout.isatty() else "script",
            help="Output mode",
        )

    # ls / list
    parser_list = subparsers.add_parser(
        "list",
        aliases=["ls"],
        help="List components",
    )
    parser_list.set_defaults(func=_fn_list)
    add_common_args(parser_list)

    # info
    parser_info = subparsers.add_parser(
        "info",
        help="retrieve all available information about components",
    )
    parser_info.set_defaults(func=_fn_info)
    parser_info.add_argument("entities", type=str, nargs="*", metavar="COMPONENT")
    add_common_args(parser_info)

    # members
    parser_component_owners_and_members = subparsers.add_parser(
        "members",
        help="[COMPONENT ..] Show members of COMPONENT*",
    )
    parser_component_owners_and_members.set_defaults(func=_fn_component_owners_and_members)
    parser_component_owners_and_members.add_argument(
        "entities", type=str, nargs="*", metavar="COMPONENT"
    )
    add_common_args(parser_component_owners_and_members)

    # paths
    parser_component_paths = subparsers.add_parser(
        "paths",
        help="[COMPONENT ..] Show code-location paths of COMPONENT*",
    )
    parser_component_paths.set_defaults(func=_fn_component_paths)
    parser_component_paths.add_argument("entities", type=str, nargs="+", metavar="COMPONENT")
    add_common_args(parser_component_paths)

    # owners
    parser_owners_for = subparsers.add_parser(
        "owners",
        aliases=[],
        help="[PATH ..] Show code owners for PATH*",
    )
    parser_owners_for.set_defaults(func=_fn_owners_for)
    parser_owners_for.add_argument("entities", type=str, nargs="+", metavar="PATH")
    add_common_args(parser_owners_for)

    # component
    parser_component_for_path = subparsers.add_parser(
        "component",
        aliases=[],
        help="[PATH ..] Show component for PATH*",
    )
    parser_component_for_path.set_defaults(func=_fn_component_for_path)
    parser_component_for_path.add_argument("entities", type=str, nargs="+", metavar="PATH")
    add_common_args(parser_component_for_path)

    # config-files
    parser_all_code_owners_config_files = subparsers.add_parser(
        "config-files",
        aliases=[],
        help="List all owners config files",
    )
    parser_all_code_owners_config_files.set_defaults(func=_fn_all_code_owners_config_files)
    add_common_args(parser_all_code_owners_config_files)

    # my-responsibilities
    parser_my_responsibilities = subparsers.add_parser(
        "my-responsibilities",
        aliases=["me"],
        help="Tell me what I'm responsible for",
    )
    parser_my_responsibilities.set_defaults(func=_fn_my_responsibilities)
    add_common_args(parser_my_responsibilities)

    # validate-config
    parser_validate_config = subparsers.add_parser(
        "validate-config",
        help="Validate the code-owners configuration for consistency and correctness",
    )
    parser_validate_config.set_defaults(func=_fn_validate_config)

    # check-plausibility
    parser_check_plausibility = subparsers.add_parser(
        "check-plausibility",
        help="Looks for sparse, over-crowded or unrealistic components and responsibilities",
    )
    parser_check_plausibility.set_defaults(func=_fn_check_plausibility)

    # These have no help text -> don't show up in console help text (intentionally)

    parser_config = subparsers.add_parser("config")
    parser_config.set_defaults(func=_fn_config)
    add_common_args(parser_config)
    parser_config.add_argument("entities", type=str, nargs="*", metavar="PATH")

    # restricted access
    parser_check_config = subparsers.add_parser("check-config")
    parser_check_config.set_defaults(func=_fn_check_config)

    # reference and debug only (will vanish)
    parser_stuff = subparsers.add_parser("stuff")
    parser_stuff.set_defaults(func=_fn_stuff)

    return parser.parse_args(args)


class FatalError(RuntimeError):
    """Fatal error during execution"""


class GerritObjectsEncoder(json.JSONEncoder):
    def default(self, obj: object) -> object:
        if isinstance(obj, Component):
            return obj.model_dump()
        return super().default(obj)


@with_gerrit_client()
async def _fn_list(
    cli_args: Args,
    owners_client: CodeOwnersClient,
) -> None:
    """Do what a 'list' command is expected to do without further information.
    Currently: List all components known to the code-owners plugin
    """
    component_info = await owners_client.all_components_info()
    if cli_args.mode == "json":
        json.dump(list(component_info), sys.stdout, cls=GerritObjectsEncoder, indent=2)
    else:  # script / rich
        rich_print(
            "\n".join(f"[{STYLE_COMPONENT_ID}]{component_id}[/]" for component_id in component_info)
        )


@with_gerrit_client()
async def _fn_info(  # noqa: C901 - too complex
    cli_args: Args,
    status: Status,
    owners_client: CodeOwnersClient,
) -> None:
    """`info` command implementation"""
    status.start()
    status.update("gather code locations..")
    all_component_info = await owners_client.all_components_info(with_code_locations=True)
    if bad_keys := (set(cli_args.entities) - set(all_component_info)):
        raise FatalError(f"Unknown components: {', '.join(bad_keys)}")

    component_info = {
        component_id: component
        for component_id, component in all_component_info.items()
        if not cli_args.entities or component_id in cli_args.entities
    }
    status.stop()

    if cli_args.mode == "json":
        json.dump(component_info, sys.stdout, cls=GerritObjectsEncoder, indent=2)
    else:  # script / rich
        for i, (component_id, component) in enumerate(sorted(component_info.items())):
            if i:
                print()
            rich_print(
                rf"[{STYLE_COMPONENT_NAME}]{component.name}[/] \[[{STYLE_COMPONENT_ID}]{component_id}[/]]"
            )
            if component.previous_name:
                rich_print(f"  previous name: [{STYLE_COMPONENT_NAME}]{component.previous_name}[/]")
            rich_print(
                f"  type: [bold]{component.type}[/] (has support component: {component.has_support_component})"
            )
            if component.description:
                rich_print("  description:")
                rich_print(
                    f"[{STYLE_COMPONENT_DESCRIPTION}]    {'\n    '.join(component.description.splitlines())}[/]"
                )
            rich_print(f"  min. member count: {component.members_required}")
            rich_print(f"  component lead: [{STYLE_EMAIL}]{component.component_owner_email}[/]")
            rich_print("  additional members:")
            for member in component.code_owners_email:
                rich_print(f"  - [{STYLE_EMAIL}]{member}[/]")
            rich_print("  code location:")
            if component.code_location:
                for path in component.code_location:
                    rich_print(f"  - [{STYLE_PATH}]{path}[/]")
            if component.external_code_location:
                rich_print("  external code location:")
                for path in component.external_code_location:
                    rich_print(f"  - [{STYLE_PATH}]{path}[/]")


@with_gerrit_client()
async def _fn_component_owners_and_members(
    cli_args: Args,
    owners_client: CodeOwnersClient,
) -> None:
    """`members` command implementation"""

    all_component_info = await owners_client.all_components_info()
    if bad_keys := (set(cli_args.entities) - set(all_component_info)):
        raise FatalError(f"Unknown components: {', '.join(bad_keys)}")

    component_info = {
        component_id: component
        for component_id, component in all_component_info.items()
        if not cli_args.entities or component_id in cli_args.entities
    }
    if cli_args.mode == "json":
        json.dump(
            {
                component_id: [
                    component.component_owner_email,
                    *(component.code_owners_email or []),
                ]
                for component_id, component in component_info.items()
            },
            sys.stdout,
            indent=2,
        )
    else:  # script / rich
        for ci, component in enumerate(component_info.values()):
            if ci:
                rich_print()
            rich_print(
                rf"[{STYLE_COMPONENT_NAME}]{component.name}[/] \[[{STYLE_COMPONENT_ID}]{component.component_id}[/]]"
            )
            for i, member in enumerate(
                (component.component_owner_email, *(component.code_owners_email or []))
            ):
                rich_print(
                    f"  - [{STYLE_EMAIL}]{member}[/][italic]{' (Lead)' if i == 0 else ''}[/]"
                )


@with_gerrit_client()
async def _fn_component_for_path(
    cli_args: Args,
    status: Status,
    owners_client: CodeOwnersClient,
) -> None:
    """`component` command implementation"""

    status.start()
    status.update("gather path types..")

    if missing_paths := (
        {f"/{path.lstrip('/').rstrip('/')}" for path in cli_args.entities}
        - set(await owners_client.all_remote_paths())
    ):
        raise FatalError(
            f"Not a valid path in {cli_args.project_name} @ {cli_args.branch}: {' '.join(missing_paths)}"
        )

    status.update("gather component details..")
    component_for_path = {
        path: await owners_client.component_for_path(path) for path in cli_args.entities
    }
    if cli_args.mode == "json":
        json.dump(component_for_path, sys.stdout, cls=GerritObjectsEncoder, indent=2)
    else:  # script / rich
        for path, component_id in component_for_path.items():
            rich_print(f"[{STYLE_PATH}]{path}[/]: [{STYLE_COMPONENT_ID}]{component_id}[/]")


@with_gerrit_client()
async def _fn_component_paths(
    cli_args: Args,
    status: Status,
    owners_client: CodeOwnersClient,
) -> None:
    """`paths` command implementation"""

    status.start()
    status.update("gather code locations..")
    all_component_info = await owners_client.all_components_info(with_code_locations=True)
    if bad_keys := (set(cli_args.entities) - set(all_component_info)):
        raise FatalError(f"Unknown components: {', '.join(bad_keys)}")

    component_info = {
        component_id: component
        for component_id, component in all_component_info.items()
        if not cli_args.entities or component_id in cli_args.entities
    }
    status.stop()

    if cli_args.mode == "json":
        json.dump(
            {
                component_id: component.code_location
                for component_id, component in component_info.items()
            },
            sys.stdout,
            cls=GerritObjectsEncoder,
            indent=2,
        )
    else:  # script / rich
        for i, (component_id, component) in enumerate(component_info.items()):
            if i:
                rich_print()
            rich_print(
                rf"[{STYLE_COMPONENT_NAME}]{component.name}[/] \[[{STYLE_COMPONENT_ID}]{component_id}[/]]"
            )
            for path in component.code_location or []:
                rich_print(f"  - [{STYLE_PATH}]{path}[/]")


@with_gerrit_client()
async def _fn_owners_for(
    cli_args: Args,
    status: Status,
    owners_client: CodeOwnersClient,
) -> None:
    """`owners` command implementation"""
    status.start()
    status.update("gather code locations..")

    if missing_paths := (
        {f"/{path.lstrip('/').rstrip('/')}" for path in cli_args.entities}
        - set(await owners_client.all_remote_paths())
    ):
        raise FatalError(
            f"Not a valid path in {cli_args.project_name} @ {cli_args.branch}: {' '.join(missing_paths)}"
        )

    await owners_client._ensure_all_entries_loaded()  # noqa: SLF001
    owners_dict = {
        path: {
            "entry": entry,
            # fixme(frans): currently we only support one components per path
            "component": components[0] if components else None,
            "owners": owners,
        }
        for path in cli_args.entities
        for entry, components, owners in (owners_client._query(path),)  # noqa: SLF001
    }
    status.stop()

    if cli_args.mode == "json":
        json.dump(owners_dict, sys.stdout, cls=GerritObjectsEncoder, indent=2)
    else:  # script / rich
        for path in cli_args.entities:
            _entry, components, owners = owners_client._query(path)  # noqa: SLF001
            if not (component_id := components[0] if components else None):
                rich_print(f"* [{STYLE_PATH}]{path}[/]: [red]No component found[/]")
                continue
            component = (await owners_client.all_components_info())[component_id]
            component_str = rf"[{STYLE_COMPONENT_NAME}]{component.name}[/] \[[{STYLE_COMPONENT_ID}]{component_id}[/]]"
            rich_print(f"* [{STYLE_PATH}]{path}[/]: {component_str}")
            for i, owner in enumerate(owners):
                rich_print(f"  - [{STYLE_EMAIL}]{owner}[/][italic]{' (Lead)' if i == 0 else ''}[/]")


@with_gerrit_client()
async def _fn_my_responsibilities(
    status: Status,
    gerrit_client: GerritClient,
    owners_client: CodeOwnersClient,
) -> None:
    """`my-responsibilities`/`me` command implementation"""
    status.start()
    status.update("gather code locations..")
    components = (await owners_client.all_components_info(with_code_locations=True)).values()
    status.stop()

    my_mail = (await gerrit_client.current_account()).email
    for component in components:
        if my_mail in (component.component_owner_email, *component.code_owners_email):
            rich_print(
                f"* {'[bold sandy_brown]owner[/]' if component.component_owner_email == my_mail else '[sandy_brown]member[/]'}:"
                rf" [{STYLE_COMPONENT_NAME}]{component.name}[/] \[[{STYLE_COMPONENT_ID}]{component.component_id}[/]]"
            )
            for path in component.code_location or []:
                rich_print(f"  - [{STYLE_PATH}]{path}[/]")


@with_gerrit_client()
async def _fn_all_code_owners_config_files(
    cli_args: Args, gerrit_client: GerritClient, owners_client: CodeOwnersClient
) -> None:
    """`config-files` command implementation"""
    owners_files = await owners_client.all_code_owners_config_files()
    if cli_args.mode == "json":
        json.dump(owners_files, sys.stdout, cls=GerritObjectsEncoder, indent=2)
    else:  # script / rich
        for owners_file in owners_files:
            owners_file_content = await gerrit_client.repo_file_content(
                owners_file, cli_args.project_name, cli_args.branch
            )
            rich_print(
                f"[{STYLE_PATH}]{owners_file}[/] [italic]({len(owners_file_content)} bytes)[/]"
            )


@with_gerrit_client()
async def _fn_config(
    cli_args: Args,
    owners_client: CodeOwnersClient,
) -> None:
    """Display the project configuration related to code-owners"""
    if cli_args.entities:
        path_config = {path: await owners_client.config_for(path) for path in cli_args.entities}
        sys.stdout.write(yaml.dump(path_config))
    else:
        project_config = await owners_client.project_config()
        if cli_args.mode == "json":
            json.dump(project_config, sys.stdout, cls=GerritObjectsEncoder, indent=2)
        elif cli_args.mode == "script":
            sys.stdout.write(yaml.dump(project_config))
        else:  # rich
            rich_print(yaml.dump(project_config))


@with_gerrit_client()
async def _fn_validate_config(
    status: Status,
    owners_client: CodeOwnersClient,
) -> None:
    """
    Not validated yet:
    # - per-file entries must be file
    # - per-file entries must exist or match
    # - only one component / file
    # - over-matching per-file entries must be avoided
    # - missing description
    # - emails must be valid
    # - member count
    # - code_location should not be empty
    """
    status.start()
    status.update("execute built-in config-check..")
    try:
        await owners_client.check_config()
    except ClientResponseError as exc:
        if not exc.status == 403:  # noqa: PLR2004 (magic value)
            raise
        Console(stderr=True).print("Can't validate config via Gerrit API due to permission issues")

    status.update("load ownership and component data..")
    await owners_client._load_cached_state(mode="never")  # noqa: SLF001
    await owners_client._ensure_all_components_loaded()  # noqa: SLF001
    issues: list[str] = list(await owners_client._ensure_all_entries_loaded())  # noqa: SLF001

    status.update("check OWNERS files consistency..")
    for per_file_path, entries in owners_client._cached.entries.items():  # noqa: SLF001
        for pattern, entry in entries.items():
            if not entry.noparent:
                issues.append(f"Entry {per_file_path}:{pattern} should have noparent set by now")

    if issues:
        for issue in issues:
            Console(stderr=True).print(f"{issue}")
        raise SystemExit(1)

    status.update("Check whether local path query returns same results as Gerrit API..")
    paths_to_check = {
        path for path in (await owners_client.all_remote_paths()) if not path.startswith("/.werks/")
    }

    for i, composite_path in enumerate(paths_to_check):
        status.update(
            f"{100 / len(paths_to_check) * i:.1f}% validate and compare {composite_path}.."
        )
        plugin_response = await owners_client.owners_for(composite_path or "/")
        plugin_mails = sorted({a["email"] for a in plugin_response})

        _entry, components, mails = owners_client._query(composite_path)  # noqa: SLF001

        log().info(f"{composite_path} {components} {len(list(mails))}")

        if plugin_mails != sorted(mails):
            log().warning(composite_path)
            log().warning("  query:  %s", components)
            log().warning("  query:  %s", sorted(mails))
            log().warning("  plugin: %s", plugin_mails)
            log().warning("  plugin: %s", plugin_response)
            raise SystemExit(1)


@with_gerrit_client()
async def _fn_check_plausibility(
    cli_args: Args,
    status: Status,
    gerrit_client: GerritClient,
    owners_client: CodeOwnersClient,
) -> None:

    status.update("check for plausibility issues..")
    await owners_client._ensure_all_entries_loaded()  # noqa: SLF001
    all_files = await owners_client.all_remote_files()
    all_directories = {Path(p).parent for p in all_files}

    # how many files in a folder?
    # how many changes in last time?
    # compare owners / git blame
    # people with too much responsibility

    count = 0
    last_dir = None
    cutoff_date = datetime.datetime.now(tz=datetime.UTC).date() - datetime.timedelta(days=60)
    wrong_owners_style = "yellow"
    matching_owners_style = "green"
    missing_owners_style = "red"

    rich_print(
        f"{'Path':<65}"
        # f"{'Entry':<40}"
        f"{'Component':<42}"
        f"{'Commits':<10}"
        f"{'Owners':>10}"
        f"{'Matching':>10}{'Wrong':>10}{'Missing':>10}"
    )

    for i, dir_path in enumerate(sorted(all_directories)):
        status.update(f"{i} {dir_path}..")
        dir_path_str = dir_path.as_posix()
        entry, components, raw_owners_mails = owners_client._query(dir_path_str)  # noqa: SLF001
        if last_dir and dir_path.is_relative_to(last_dir[0]) and entry == last_dir[1]:
            # print(f"{dir_path_str} {entry}")
            continue

        last_dir = dir_path, entry

        if not raw_owners_mails:
            continue  # fixme(frans): suggest mails

        count += 1
        # commit_id, date, author, message, list of files affected)
        log_data = await gerrit_client.get_log(
            dir_path_str, cutoff_date, cli_args.project_name, cli_args.branch
        )

        owners_mails = {email.split("@")[0] for email in raw_owners_mails}

        committer_emails = {email.split("@")[0] for _, _, email, _, _ in log_data}
        if "lm" in committer_emails:
            committer_emails.remove("lm")
            committer_emails.add("lars.michelsen")

        path_str = (
            dir_path_str
            if len(dir_path_str) < 60  # noqa: PLR2004 'magic value'
            else f"{dir_path_str[: 60 // 2]}..{dir_path_str[-60 // 2 :]}"
        )

        wrong_owners_str = (
            f"[{wrong_owners_style}]{' '.join(wrong_owners)}[/]"
            if (wrong_owners := (committer_emails - owners_mails))
            else ""
        )
        matching_owners_str = (
            f"[{matching_owners_style}]{' '.join(matching_owners)}[/]"
            if (matching_owners := (owners_mails & committer_emails))
            else ""
        )
        missing_owners_str = (
            f"[{missing_owners_style}]{' '.join(missing_owners)}[/]"
            if (missing_owners := (owners_mails - committer_emails))
            else ""
        )

        rich_print(
            f"[{STYLE_PATH}]{path_str[1:]:<65}[/]"
            # f"{entry!r:<40}"
            f"[{STYLE_COMPONENT_ID}]{(components and components[0]) or '':42}[/]"
            f"{len(log_data):>10}"
            f"{len(owners_mails):>10}"
            f"[{matching_owners_style}]{len(matching_owners):>10}[/]"
            f"[{wrong_owners_style}]{len(wrong_owners):>10}[/]"
            f"[{missing_owners_style}]{len(missing_owners):>10}[/]"
        )

        rich_print(f"{wrong_owners_str} {matching_owners_str} {missing_owners_str}")

        # for commit_id, commit_date, author, message, paths in log_data:
        #    print(f"  {commit_id[:8]} {commit_date} {author:20} {message.splitlines()[0]}")
        # contributors_by_git_blame =
        # print(f"  git blame contributors: {', '.join(contributors_by_git_blame)}")

        if count > 10:  # noqa: PLR2004
            break


@with_gerrit_client()
async def _fn_check_config(
    cli_args: Args,  # noqa: ARG001 Unused function argument
    gerrit_client: GerritClient,  # noqa: ARG001 Unused function argument
    owners_client: CodeOwnersClient,
) -> None:
    await owners_client.check_config()


@with_gerrit_client()
async def _fn_stuff(
    cli_args: Args, gerrit_client: GerritClient, owners_client: CodeOwnersClient
) -> None:
    log().debug("check configuration..")
    # await owners_client.check_config()
    log().debug("all_code_owners_config_files..")
    for owners_file in await owners_client.all_code_owners_config_files():
        owners_file_content = await gerrit_client.repo_file_content(
            owners_file, cli_args.project_name, cli_args.branch
        )
        rich_print(f"{owners_file} {len(owners_file_content)}")

    log().debug("all_components_info..")
    rich_print(f"{await owners_client.all_components_info()}")
    rich_print(f"{await owners_client.component_for_path('mixed_component/core_part')}")
    rich_print(f"{await owners_client.code_locations('core_component')}")
    rich_print(f"{await owners_client.owners_for('mixed_component/core_part')}")


@with_gerrit_client(populate=False)
async def _fn_tui(  # noqa: C901 - too complex
    cli_args: Args, gerrit_client: GerritClient, owners_client: CodeOwnersClient
) -> None:
    class TabCompleteInput(Input):
        """Input widget that accepts suggestions on Tab instead of right arrow."""

        async def _on_key(self, event: Key) -> None:
            if event.key == "tab" and self._suggestion:
                self.value = self._suggestion
                self.cursor_position = len(self.value)
                event.prevent_default()
                event.stop()
            else:
                await super()._on_key(event)

    class CmkComponents(TuiBaseApp):
        CSS = """
          Header {text-style: bold;}
          Tree > .tree--guides {color: $success-darken-3;}
          Tree > .tree--guides-selected {
            text-style: none;
            color: $success-darken-1;
          }
          #app_log {height: 8;}
          #error-label {
            border: solid black;
            background: red;
            color: white;
            width: 100%;
          }
        """
        BINDINGS: ClassVar[list[Binding | tuple[str, str] | tuple[str, str, str]]] = [
            Binding("ctrl+x", "app.quit", "Quit", show=True),
            Binding("u", "populate_tree"),
        ]

        def __init__(
            self,
            gerrit_client: GerritClient,
            owners_client: CodeOwnersClient,
            branch: str,
        ) -> None:
            super().__init__(
                logger_show_funcname=False, logger_show_tid=True, logger_show_name=True
            )
            log_level = cli_args.log_level if cli_args.log_level != "WARNING" else "INFO"
            self.set_log_levels(log_level, ("trickkiste", log_level))
            self.title = "CMK Components"
            self.main_tree_widget: Tree[None] = Tree("CmkComponents")
            self.main_tree_widget.show_root = False
            self.result_tree_node = self.main_tree_widget.root.add(
                "search results", expand=True, allow_expand=False
            )
            self.component_tree_node = self.main_tree_widget.root.add(
                "[bold spring_green1]Components[/] [white](press 'u' to force update)[/]",
                expand=False,
                allow_expand=True,
            )
            self.my_components_tree_node = self.main_tree_widget.root.add(
                "[bold spring_green1]Components I'm lead or member of[/]",
                expand=False,
                allow_expand=True,
            )
            self.my_files_tree_node = self.main_tree_widget.root.add(
                "[bold spring_green1]Files I'm (co-)responsible for[/]",
                expand=False,
                allow_expand=True,
            )
            self.gerrit_client = gerrit_client
            self.owners_client = owners_client
            self.branch = branch
            self.ongoing_tasks: set[str] = set()
            self.own_mail = ""

        def compose(self) -> ComposeResult:
            """Set up the UI"""
            yield Header(show_clock=True, id="header")
            self.error_label = Label(id="error-label")
            self.error_label.display = False
            self.input = TabCompleteInput(placeholder="path or component", id="dictionary-search")
            yield self.error_label
            yield self.input
            yield self.main_tree_widget
            yield from super().compose()

        @asynccontextmanager
        async def task_indicator(self, description: str) -> AsyncIterator[None]:
            self.ongoing_tasks.add(description)
            await asyncio.sleep(0.1)
            try:
                yield
            finally:
                self.ongoing_tasks.discard(description)

        @awatch_duration
        async def initialize(self) -> None:
            try:
                self.own_mail = (await gerrit_client.current_account()).email or "n/a"
                self.lookup()
                self.maintain_statusbar()
                self.action_populate_tree()
                self.populate_auto_completion_dict()
            except Exception as exc:  # noqa: BLE001
                self.error_label.update(f"[black]Error during initialization: {exc}[/]")
                self.error_label.display = True

        @work(exit_on_error=True)
        @awatch_duration
        async def action_populate_tree(self) -> None:
            async with self.task_indicator("query component and ownership via Gerrit"):
                log().info("query components to populate tree with")
                self.input.placeholder = "Initialize component and ownership data.."
                await owners_client.initialize_data(cache_mode=cli_args.cache_mode)
                await owners_client._ensure_all_entries_loaded()  # noqa: SLF001
                self.populate_responsibilities()
                self.populate_auto_completion_dict()
                self.component_tree_node.remove_children()
                await asyncio.sleep(0.1)
                for component in await owners_client.all_components_info():
                    self.component_tree_node.add_leaf(f"[bold cyan]{component}[/]")
                self.input.placeholder = "path or component"

        @work(exit_on_error=True)
        async def populate_responsibilities(self) -> None:
            """Populate the 'my responsibilities' section of the tree"""
            async with self.task_indicator("populate responsibilities"):
                self.my_components_tree_node.remove_children()
                self.my_files_tree_node.remove_children()
                for component in (await owners_client.all_components_info()).values():
                    if self.own_mail in (
                        component.component_owner_email,
                        *component.code_owners_email,
                    ):
                        self.my_components_tree_node.add_leaf(
                            f"{'owner' if component.component_owner_email == self.own_mail else 'member'}: {component.dump_rich()}"
                        )
                        for path in component.code_location or []:
                            self.my_files_tree_node.add_leaf(f"[bold cyan]{path}[/]")

        @staticmethod
        def suggestion_strings_from(file_paths: Iterable[str]) -> Sequence[str]:
            return list(
                {
                    d
                    for a in file_paths
                    if "qa-test-data" not in a
                    for b in (a, a.rsplit("/", maxsplit=1)[0])  # add file and parent
                    if (c := b.lstrip("/"))
                    for d in (c, f"/{c}")  # add with and without leading slash
                }
            )

        @work(exit_on_error=True)
        async def populate_auto_completion_dict(self) -> None:
            async with self.task_indicator("init auto completion"):
                log().info("initialize auto completion with files and components")
                # raw_paths = map(str.strip, process_output("git ls-files").split("\n"))
                raw_paths = list(await owners_client.all_remote_files())
                all_paths = self.suggestion_strings_from(raw_paths)
                all_components = list(await owners_client.all_components_info())
                self.input.suggester = SuggestFromList(
                    sorted((*all_paths, *all_components)), case_sensitive=False
                )

        @on(Click, "#error-label")
        def handle_error_label_click(self, _event: Click) -> None:
            self.exit()

        @awatch_duration
        async def on_input_changed(self, message: Input.Changed) -> None:
            self.lookup(message.value)

        @work(group="search", exclusive=True)
        @awatch_duration
        async def lookup(self, phrase: str = "") -> None:
            components = await owners_client.all_components_info()
            self.result_tree_node.remove_children()
            if not phrase:
                self.result_tree_node.label = "[italic]no search phrase given[/]"
                return
            self.result_tree_node.label = "[italic]searching...[/]"
            if phrase in components:
                self.result_tree_node.label = f"component [bold cyan]{phrase}[/] found:"
                component = components[phrase]
                if component.code_location:
                    for path in component.code_location:
                        self.result_tree_node.add_leaf(f"[bold cyan]{path}[/]")
                else:
                    self.result_tree_node.add_leaf("[red]no code locations found[/]")
                return
            if not (result := sorted(await owners_client.owners_for(phrase), key=str)):
                self.result_tree_node.label = f"no results for '{phrase}'"
                return
            self.result_tree_node.label = (
                f"[bold spring_green1]Search results for [/]'{phrase}'[white][/]:"
            )
            for element in result:
                self.result_tree_node.add_leaf(f"[cyan]{element.get('email')}[/]")

        @work(exit_on_error=True)
        async def maintain_statusbar(self) -> None:
            """Status bar stub (to avoid 'nonsense' status)"""
            for i in count():
                if (i % 10 == 0) or self.ongoing_tasks:
                    always = (
                        f"{len(asyncio.all_tasks())} async tasks │ CmkComponents v{__version__}"
                        f" │ logged in as [bold blue]{self.own_mail}[/]"
                        f" │ commit: [bold blue]{(await self.owners_client.commit_id())[:6]}[/]"
                    )
                    progress = (f"{'⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏'[i % 10]} [blue]{t}[/]" for t in self.ongoing_tasks)
                    self.update_status_bar(" │ ".join((always, *progress)))
                await asyncio.sleep(0.3)

    await CmkComponents(gerrit_client, owners_client, cli_args.branch).run_async()


def main(args: None | Sequence[str] = None) -> int:
    """See main docstring"""
    traceback.install()
    cli_args = parse_arguments(args or sys.argv[1:])
    status = None

    t1 = time.time()

    with ExitStack() as context:
        if cli_args.func != _fn_tui:
            status = context.enter_context(console.status(""))
            status.stop()
            setup_logging(log(), level=cli_args.log_level, show_name=20, show_funcname=30)
            logging.getLogger("vcr.matchers").setLevel(logging.WARNING)

        if cli_args.vcr_cache_file:
            context.enter_context(
                vcr.use_cassette(cli_args.vcr_cache_file, record_mode="new_episodes")
            )

        with suppress(KeyboardInterrupt):
            log().debug("run %r", cli_args.func.__name__)
            try:
                asyncio.run(cli_args.func(cli_args, status=status))
            except FatalError as exc:
                Console(stderr=True).print(f"ERROR: {exc}")
                return 1

    if cli_args.func != _fn_tui:
        log().debug("took %.2fms", (time.time() - t1) * 1000)

    return 0


def log() -> logging.Logger:
    """Convenience function retrieves 'our' logger"""
    return logging.getLogger("trickkiste.cmk-components")


def rich_print(*args: None | str) -> None:
    """Does what you'd expect from print()"""
    console.print(*args)


console = Console()

if __name__ == "__main__":
    raise SystemExit(main())
