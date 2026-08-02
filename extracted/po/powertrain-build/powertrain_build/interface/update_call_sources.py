# Copyright 2024 Volvo Car Corporation
# Licensed under Apache 2.0.

"""Module that handles the update of call sources."""


import argparse
import re
import sys
from typing import List, Optional
from ruamel.yaml import YAML
from pathlib import Path


PARSER_HELP = "Update call sources for method calls in source files."


def configure_parser(parser: argparse.ArgumentParser):
    """Configure the parser for the update call sources command."""
    parser.add_argument("interface", help="Interface specification dict", type=Path)
    parser.add_argument("src_dir", help="Path to source file directory", type=Path)
    parser.add_argument(
        "-p",
        "--project-config",
        type=Path,
        default=None,
        help="Path to project config json file",
    )
    parser.set_defaults(func=update_call_sources_cli)


def update_call_sources_cli(args: argparse.Namespace):
    """CLI function for updating call sources."""
    method_config = read_project_config(args.project_config)
    with open(args.interface, encoding="utf-8") as interface_file:
        yaml = YAML(typ='safe', pure=True)
        adapter_spec = yaml.load(interface_file)
    update_call_sources(args.src_dir, adapter_spec, method_config)


def main(argv: Optional[List[str]] = None):
    """ Main function for stand alone execution."""
    parser = argparse.ArgumentParser(description=PARSER_HELP)
    configure_parser(parser)
    args = parser.parse_args(argv)
    args.func(args)


def read_project_config(project_config_path):
    """ Reads project config file and extract method specific settings if they are present.

    Args:
        project_config_path (Path): path to the ProjectCfg.json file
    Returns:
        method_config (dict): dictionary of method related configs.
    """
    project_info = {}
    if project_config_path is not None:
        with project_config_path.open() as config_file:
            yaml = YAML(typ='safe', pure=True)
            config = yaml.load(config_file)
            project_info = config["ProjectInfo"]
    method_config = {
        "adapter_declarations_change": project_info.get("adapterDeclarations", None)
    }
    method_config["method_call_wrapper"] = {
        "pre": project_info.get("methodPreCallWrapper", ""),
        "post": project_info.get("methodPostCallWrapper", "")
    }
    for key, value in method_config["method_call_wrapper"].items():
        if value != "":
            method_config["method_call_wrapper"][key] = value + "\n"

    return method_config


def is_method_adapter(adapter):
    """ Check if adapter has methods in it

    Args:
        adapter (dict): adapter specification
    Returns:
        methods_in_adapter (bool): true if adapter contains methods,
        false otherwise
    """
    methods_in_adapter = "methods" in adapter and len(adapter["methods"]) > 0
    return methods_in_adapter


def update_call_sources(src_dir, adapter_spec, method_config):
    """ Update the source files for specified method calls with
    adapter function calls that trigger the methods.

    Args:
        src_dir (Path): path to folder for method call sources
        adapter_spec (list): adapter specifications with methods
        method_config (dict): project specific method configs
    """

    method_adapters = [a for a in adapter_spec if is_method_adapter(a)]
    for adapter in method_adapters:
        for method in adapter["methods"]:
            method_src = src_dir / (method["name"] + ".c")
            with method_src.open("r+") as src_file:
                old_src = src_file.read()
            new_src = generate_src_code(adapter, method, old_src, method_config)
            method_src.unlink()
            with open(method_src.with_suffix(".cpp"), "w", encoding="utf-8") as dst_file:
                dst_file.write(new_src)
            method_header = src_dir / (method["name"] + ".h")
            with method_header.open("r+") as header_file:
                old_header = header_file.read()
                new_header = generate_header_code(method_config, old_header)
                header_file.seek(0)
                header_file.write(new_header)
                header_file.truncate()


def generate_header_code(method_config, old_header):
    """ Change header code to include project specific adapter wrapper.

    Args:
        method_config (dict): project specific method settings
        old_header (string): header source code
    Returns:
        new_header (string): modified header source code

    """
    adapter_pattern = r'(?<=#include ")adapter_wrapper.hh'
    if method_config["adapter_declarations_change"]:
        new_header = re.sub(
            adapter_pattern, method_config["adapter_declarations_change"], old_header
        )
        return new_header
    return old_header


def generate_src_code(adapter, method, old_src, method_config):
    """ Generate the method call source code to trigger the method call

    Args:
        adapter (dict): adapter specification
        method (dict): method specification
        old_src (string): method call source code with mock call
        method_config (dict): project specific method settings
    Returns:
        new_src (string): method call source code with adapter function call
        that triggers method

    """
    call_pattern = (
        r"    \/\* CSP method call\n"
        r"(.*)ADAPTER->METHOD(.*)"
        r"    CSP method call end\*\/\n"
    )
    dummy_pattern = (
        r"    \/\* C dummy call\*\/" r".*" r"    \/\* C dummy call end\*\/\n"
    )
    comment = (
        r"\/\* Used for running spm without csp, such as silver\n"
        r"   This code should be replaced when using csp. \*\/\n"
    )
    name = method["name"]
    adapter_name = [adapter["name"].title()]
    namespace = []
    if method["namespace"] != "":
        namespace = [method["namespace"]]
    adapter = "::".join(namespace + adapter_name) + "->" + name
    pre_call = method_config["method_call_wrapper"]["pre"]
    post_call = method_config["method_call_wrapper"]["post"]
    sans_comment = re.sub(comment, "", old_src)
    sans_dummy_call = re.sub(dummy_pattern, "", sans_comment, flags=re.DOTALL)
    new_src = re.sub(
        call_pattern, pre_call + r"\1" + adapter + r"\2" + post_call, sans_dummy_call, flags=re.DOTALL
    )
    return new_src


if __name__ == "__main__":
    main(sys.argv[1:])
