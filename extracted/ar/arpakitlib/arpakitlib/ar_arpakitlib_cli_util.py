# arpakit

import sys

from arpakitlib.ar_arpakit_project_template_util import init_arpakit_project_template
from arpakitlib.ar_need_type_util import parse_need_type, NeedTypes
from arpakitlib.ar_parse_command import parse_command

_ARPAKIT_LIB_MODULE_VERSION = "3.0"


def execute_arpakitlib_cli(*, full_command: str | None = None):
    if full_command is None:
        full_command = " ".join(sys.argv)

    parsed_command = parse_command(text=full_command)

    command = parsed_command.get_value_by_keys(keys=["command", "c"])
    if command:
        command = command.strip()
    if not command:
        raise Exception(f"not command, command={command}")

    if command == "help":
        print("Commands:")
        print()
        print("-c init_arpakit_project_template")
        print("-version (1,) ...")
        print("-project_dirpath ./")
        print("-overwrite_if_exists ...")
        print("-ignore_paths_startswith ...")
        print("-only_paths_startswith ...")
        print("\n")

    elif command == "init_arpakit_project_template":
        version: str = parse_need_type(
            value=parsed_command.get_value_by_keys(keys=["version"]),
            need_type=NeedTypes.str_,
            allow_none=False
        )
        project_dirpath: str = parse_need_type(
            value=parsed_command.get_value_by_keys(keys=["project_dirpath"]),
            need_type=NeedTypes.str_,
            allow_none=False
        )
        overwrite_if_exists: bool = parse_need_type(
            value=parsed_command.get_value_by_keys(keys=["overwrite_if_exists"]),
            need_type=NeedTypes.bool_,
            allow_none=False
        )
        ignore_paths_startswith: list[str] | None = parse_need_type(
            value=parsed_command.get_value_by_keys(keys=["ignore_paths_startswith"]),
            need_type=NeedTypes.list_of_str,
            allow_none=True
        )
        only_paths_startswith: list[str] | None = parse_need_type(
            value=parsed_command.get_value_by_keys(keys=["only_paths_startswith"]),
            need_type=NeedTypes.list_of_str,
            allow_none=True
        )
        init_arpakit_project_template(
            version=version,
            project_dirpath=project_dirpath,
            overwrite_if_exists=overwrite_if_exists,
            ignore_paths_startswith=ignore_paths_startswith,
            only_paths_startswith=only_paths_startswith
        )

    else:
        raise Exception(f"not recognized command, command={command}")


if __name__ == '__main__':
    execute_arpakitlib_cli(full_command="/arpakitlib -c help")
