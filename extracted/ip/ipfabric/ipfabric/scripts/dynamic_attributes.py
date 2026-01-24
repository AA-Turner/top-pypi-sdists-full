import argparse
import sys
from pathlib import Path
from typing import Union, Optional

try:
    import yaml
    import pandas  # noqa: F401
    import yaml_include  # noqa: F401
except ImportError:
    raise ImportError(
        "Required packages are missing to run this script. "
        "Please install them with 'pip3 install ipfabric[dynamic-attributes]'."
    )

from ipfabric.dynamic_attributes import AttributeSync, MultiConfig
from ipfabric.dynamic_attributes.configs import IPFabric, load_config


def _check_excel(outfile: Path) -> str:
    if not outfile:
        raise SyntaxError("Output file '-o|--outfile' must be specified with Excel format.")
    if outfile.suffix != ".xlsx":
        raise SyntaxError("Output file for Excel format must have '.xlsx' extension.")
    try:
        import openpyxl  # noqa: F401

        return "openpyxl"
    except ImportError:
        pass
    try:
        import xlsxwriter  # noqa: F401

        return "xlsxwriter"
    except ImportError:
        raise ImportError(
            "Excel format requires either 'xlsxwriter' or 'openpyxl' to be installed. "
            "Please install one of them using pip, recommended to use 'xlsxwriter'."
        )


def parse_overrides(value: Optional[Union[str, int]]) -> Union[bool, None]:
    if isinstance(value, str):
        if value.lower() in ["true", "1"]:
            return True
        elif value.lower() in ["false", "0"]:
            return False
    elif isinstance(value, int):
        return bool(value)
    return value


def parse_ipfabric_config(files: set[Path], file: Optional[Path] = None) -> Union[IPFabric, None]:
    if not file:
        return None
    if file in files or file.exists():
        return load_config(file).ipfabric
    filenames = {f.name: f for f in files}
    if len(filenames) != len(files) or file.name not in filenames:
        raise ValueError(
            f"Could not determine location of config file '{file}'; please check name or provide full path."
        )
    return load_config(filenames[file.name]).ipfabric


def main():
    arg_parser = argparse.ArgumentParser(
        description="IP Fabric Dynamic Attribute.",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""
    This script will run the AttributeSync with the provided configuration file(s) which defaults to 'config.yml'.
    You can specify a different or multiple configuration files by passing the filename as an argument:
    ipf_dynamic_attributes mgmt-ip.yml region.yml
    """,
    )
    arg_parser.add_argument(
        "filenames",
        nargs="*",
        default=["config.yml"],
        type=Path,
        help="Configuration filename(s), defaults to 'config.yml'.",
    )
    arg_parser.add_argument(
        "-f",
        "--format",
        choices=["csv", "json", "excel"],
        default="csv",
        help="Output format for the report. Default is 'csv'. Use 'json' for JSON output.",
    )
    arg_parser.add_argument(
        "-o",
        "--outfile",
        type=Path,
        help="Output filename to send report instead of standard out.",
    )
    arg_parser.add_argument(
        "-m",
        "--merge-only",
        action="store_true",
        default=False,
        help="Merge the default rule settings into rules and display the resulting file; does not run any automation.\n"
        "This will also merge multiple configuration files into a single file.",
    )
    arg_parser.add_argument(
        "-d",
        "--dry-run-override",
        choices=["true", "false", "0", "1"],
        default=None,
        help="Override 'dry_run' setting in configuration(s); defaults to null to use value(s) in the config.\n"
        "If specifying multiple config files, all 'dry_run' values must be the same unless this flag is set.",
    )
    arg_parser.add_argument(
        "-u",
        "--update-snapshot-override",
        choices=["true", "false", "0", "1"],
        default=None,
        help="Override 'update_snapshot' setting in configuration(s); defaults to null to use value(s) in the config.\n"
        "If specifying multiple config files, all 'update_snapshot' values must be the same unless this flag is set.",
    )
    arg_parser.add_argument(
        "-i",
        "--ipfabric-override",
        type=Path,
        default=None,
        help="Override 'ipfabric' setting in configurations; defaults to null to use value in the config file(s).\n"
        "If specifying multiple config files, all 'ipfabric' values must be the same unless this flag is set "
        "to the name of the file to use the IP Fabric configuration settings from.",
    )
    args = arg_parser.parse_args()
    for file in args.filenames:
        if not file.exists():
            raise FileNotFoundError(f"Configuration file '{file}' does not exist.")

    ipf = parse_ipfabric_config(set(args.filenames), args.ipfabric_override)
    multiconfig = MultiConfig(
        configs=args.filenames,
        dry_run_override=parse_overrides(args.dry_run_override),
        update_snapshot_override=parse_overrides(args.update_snapshot_override),
        ipfabric_override=ipf,
    )

    sync = AttributeSync(config=multiconfig)

    if args.merge_only:
        print(yaml.dump(sync.config.model_dump_merged()))
        exit(0)

    engine = None
    if args.format == "excel":
        engine = _check_excel(args.outfile)

    report = sync.run()

    outfile = args.outfile or sys.stdout
    columns = [*sync.config.inventory.df_columns, "correct", "update", "create"]
    if args.format == "json":
        report.to_json(outfile, index=False, orient="records")
    elif args.format == "csv":
        report.to_csv(outfile, index=False, columns=columns)
    else:
        report.to_excel(outfile, index=False, columns=columns, engine=engine)


if __name__ == "__main__":
    main()
