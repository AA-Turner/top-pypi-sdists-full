import argparse
import json
import logging as pylogging
import os
import sys
import traceback
from pathlib import Path
from typing import TYPE_CHECKING, List, Optional, cast

from dataclasses_json import DataClassJsonMixin

from chalk._gen.chalk.artifacts.v1 import export_pb2 as export_pb
from chalk._lsp.error_builder import LSPErrorBuilder
from chalk.parsed._proto.export import import_files_then_export_from_registry
from chalk.parsed._proto.lsp import convert_lsp_gql_to_proto

if TYPE_CHECKING:
    from pydantic import ValidationError
else:
    try:
        from pydantic.v1 import ValidationError
    except ImportError:
        from pydantic import ValidationError

from chalk.config.project_config import load_project_config
from chalk.importer import import_all_files
from chalk.parsed.user_types_to_json import get_lsp_gql, get_registered_types_as_json
from chalk.utils.stubgen import configure_stubgen_argparse, run_stubgen


def get_list_results(directory: Optional[str], file_allowlist: Optional[List[str]]):
    if directory is not None:
        os.chdir(directory)
    scope_to = Path(directory or os.getcwd())
    try:
        failed = import_all_files(
            file_allowlist=file_allowlist,
            project_root=None if directory is None else Path(directory),
        )
        return get_registered_types_as_json(scope_to, failed)
    except Exception:
        ex_type, ex_value, ex_traceback = sys.exc_info()
        assert ex_type is not None
        relevant_traceback = f"""{os.linesep.join(traceback.format_tb(ex_traceback))}
\n{ex_type.__name__}: {str(ex_value)}
"""
        return json.dumps(
            dict(
                failed=[dict(traceback=relevant_traceback)],
                lsp=cast(DataClassJsonMixin, get_lsp_gql()).to_dict(),
            ),
            indent=2,
        )


def get_artifacts_export_safe(directory: Optional[str], file_allowlist: Optional[List[str]]) -> bytes:
    try:
        return import_files_then_export_from_registry(directory, file_allowlist).SerializeToString()
    except Exception:
        ex_type, ex_value, ex_traceback = sys.exc_info()
        assert ex_type is not None
        relevant_traceback = f"""{os.linesep.join(traceback.format_tb(ex_traceback))}
\n{ex_type.__name__}: {str(ex_value)}
"""
        return export_pb.Export(
            failed=[
                export_pb.FailedImport(
                    traceback=relevant_traceback,
                )
            ],
            lsp=convert_lsp_gql_to_proto(get_lsp_gql()),
        ).SerializeToString()


def dump_cmd(filename: str, directory: Optional[str], filter_file: Optional[str], use_proto: bool = False):
    file_allowlist = None
    if filter_file is not None and os.path.exists(filter_file):
        with open(filter_file) as f:
            file_allowlist = [f.strip() for f in f.readlines()]

    if use_proto:
        with open(filename, "wb") as f:
            f.write(
                get_artifacts_export_safe(
                    directory=directory,
                    file_allowlist=file_allowlist,
                )
            )
    else:
        with open(filename, "w") as f:
            f.write(
                get_list_results(
                    directory=directory,
                    file_allowlist=file_allowlist,
                )
            )


def config_cmd():
    json_response: str
    try:
        model = load_project_config()
    except ValidationError as e:
        json_response = json.dumps({"error": str(e)})
    else:
        if model is None:
            print("No `chalk.yaml` configuration file found")
            return
        json_response = model.json()

    print(json_response)


def cli(args_override: Optional[List[str]] = None):
    parser = argparse.ArgumentParser(
        prog="Chalk Python CLI",
        description=(
            "You typically do not need to invoke this utility directly. "
            "Prefer https://github.com/chalk-ai/cli instead."
        ),
    )
    parser.add_argument("--log-level", help="Print debug info", nargs="?")
    subparsers = parser.add_subparsers(dest="command")

    # CONFIG
    subparsers.add_parser("config", help="Print the config for the current project")

    # EXPORT
    export_parser = subparsers.add_parser(
        "export", help="Write the resolvers for the current project to the given file"
    )
    export_parser.add_argument("filename", help="Write to this file")
    export_parser.add_argument("--directory", help="Scope to this directory", nargs="?")
    export_parser.add_argument("--file_filter", help="Path containing only files to consider", nargs="?")
    # >= 3.9 version
    # export_parser.add_argument(
    #     "--lsp",
    #     help="If set, will output the diagnostics in the format expected by the LSP instead of eagerly raising",
    #     action=argparse.BooleanOptionalAction,
    # )
    # < 3.9 version
    export_parser.add_argument("--lsp", action="store_true")
    export_parser.add_argument("--no-lsp", dest="lsp", action="store_false")
    export_parser.set_defaults(lsp=False)

    export_parser.add_argument("--proto", action="store_true")
    export_parser.set_defaults(proto=False)

    # STUBGEN
    stubgen_parser = subparsers.add_parser("stubgen", help="Generate type stubs for feature set classes")
    configure_stubgen_argparse(stubgen_parser)

    # Parsing only known args for forwards compatibility.
    # Changing this to `.parse_args` means once the args are
    # set for a command, you can never add to them.
    # Please do not change to `.parse_args`.
    args, _ = parser.parse_known_args(args_override)
    if args.log_level:
        level = getattr(pylogging, args.log_level.upper())
        pylogging.basicConfig(
            format="%(asctime)s %(levelname)s: %(message)s",
            datefmt="%m/%d/%Y %I:%M:%S %p",
            level=level,
        )

    if args.command == "export":
        LSPErrorBuilder.lsp = args.lsp
        dump_cmd(filename=args.filename, directory=args.directory, filter_file=args.file_filter, use_proto=args.proto)

    elif args.command == "config":
        config_cmd()

    elif args.command == "stubgen":
        run_stubgen(args=args, file_filter=args.file_filter)

    else:
        parser.print_help(sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(cli())
