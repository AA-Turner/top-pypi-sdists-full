import argparse
import json
import os
import re
from pathlib import Path

import niquests

from ipfabric import IPFClient
from ipfabric.models import Inventory, Technology, Endpoint, Device
from ipfabric.scripts.shared import base_args, load_env, parse_base_args

try:
    import pandas as pd
    import openpyxl  # noqa: F401
    from rich.console import Console
    from rich import box  # Export BOX_STYLE=MARKDOWN before running commands for docs.
    from rich.table import Table
except ImportError:
    raise ImportError(
        "pandas, openpyxl, and rich are required, please install by using: "
        "`pip3 install ipfabric[cli]` or `pip3 install pandas openpyxl rich`."
    )

CONSOLE = Console()


def collect_endpoints(data):
    endpoints = set()
    for key, value in data.items():
        if isinstance(value, dict):
            if "endpoint" in value:
                endpoints.add(value["endpoint"])
            endpoints.update(collect_endpoints(value))
    return endpoints


def verify_tables(ipf: IPFClient, args: argparse.Namespace) -> set[Endpoint]:
    valid_tables = set()
    for table in args.ipf_tables:
        if not (endpoint := ipf.oas.get(ipf._check_url(table), None)) or not endpoint.post:
            CONSOLE.print(f"[red]Error:[/red] Not a valid table: {table}")
            continue
        if (args.device_hostname or args.device_sn) and not endpoint.post.sn_columns:
            CONSOLE.print(f"[red]Error:[/red] Table '{table}' does not have 'sn' column.")
            continue
        valid_tables.add(endpoint.post)
    return valid_tables


def rich_print(results: pd.DataFrame, filters: dict, url: str, columns: list[str]):

    # Export BOX_STYLE=MARKDOWN before running commands for docs.
    box_style = getattr(box, os.getenv("BOX_STYLE", "HEAVY_HEAD").upper(), box.HEAVY_HEAD)
    caption = f"Filter: {json.dumps(filters)}" if filters else None
    table = Table(*columns, title=results.title, caption=caption, box=box_style)

    for result in results.head(3).to_dict(orient="records"):
        table.add_row(*[str(result[c]) for c in columns])
    CONSOLE.print(table)
    CONSOLE.print(url, style=f"link {url}")


def get_table(
    ipf: IPFClient, args: argparse.Namespace, table: Endpoint, table_filter: dict, title: str
) -> pd.DataFrame | None:
    try:
        data = ipf.fetch_all(table.api_endpoint, filters=table_filter, export="df")
        data.title = title
        if args.preview and data is not None:
            url = ipf.oas[table.api_endpoint].post.filter_url(table_filter, ipf._client.base_url)
            rich_print(data, table_filter, url, table.columns)
        return data
    except niquests.exceptions.HTTPError as e:
        if e.response.status_code == 422:
            CONSOLE.print(f"Cant fetch data for {table}.")
        CONSOLE.print(f"[red]Error:[/red] {e} ")


def create_filter(devices: list[Device], table: Endpoint) -> dict:
    return {"or": [{col: ["eq", dev.sn]} for dev in devices for col in table.sn_columns]} if devices else {}


def get_tables_by_device(
    ipf: IPFClient, args: argparse.Namespace, valid_tables: set[Endpoint], valid_devices: set[Device]
) -> list[pd.DataFrame]:
    dataframes_for_export = []

    for table in valid_tables:
        for device in valid_devices:
            title = f"{device.hostname}-{table.title or table.summary}"
            if (data := get_table(ipf, args, table, create_filter([device], table), title)) is not None:
                dataframes_for_export.append(data)
    return dataframes_for_export


def get_tables_joined(
    ipf: IPFClient, args: argparse.Namespace, valid_tables: set[Endpoint], valid_devices: set[Device]
) -> list[pd.DataFrame]:
    dataframes_for_export = []

    for table in valid_tables:
        table_filter = create_filter(valid_devices, table)
        title = table.title or table.summary
        if (data := get_table(ipf, args, table, table_filter, title)) is not None:
            dataframes_for_export.append(data)
    return dataframes_for_export


def get_tables(args: argparse.Namespace) -> list[pd.DataFrame]:
    ipf = IPFClient(snapshot_id=args.snapshot, base_url=args.base_url, auth=args.auth, verify=(not args.insecure))
    valid_tables = verify_tables(ipf, args)
    if not valid_tables:
        CONSOLE.print("[red]Error:[/red] No valid tables provided. Exiting...")
        exit(1)

    valid_devices = set()
    for hostname in args.device_hostname:
        if hostname not in ipf.devices.by_hostname:
            CONSOLE.print(f"[red]Error:[/red] Hostname '{hostname}' not found in inventory.")
            continue
        valid_devices.add(ipf.devices.by_hostname[hostname][0])
    for sn in args.device_sn:
        if sn not in ipf.devices.by_sn:
            CONSOLE.print(f"[red]Error:[/red] Device Serial Number '{sn}' not found in inventory.")
            continue
        valid_devices.add(ipf.devices.by_sn[sn])
    if (args.device_hostname or args.device_sn) and not valid_devices:
        CONSOLE.print("[red]Error:[/red] No valid hostnames provided. Exiting...")
        exit(1)

    return (
        get_tables_by_device(ipf, args, valid_tables, valid_devices)
        if args.device_separate
        else get_tables_joined(ipf, args, valid_tables, valid_devices)
    )


def main():
    load_env()
    parser = argparse.ArgumentParser(
        description="Fetch tables from IP Fabric and insert into a single excel file with multiple sheets."
    )
    CONSOLE.print(":rocket: IP Fabric Tables to Excel Exporter! :rocket:")

    ipf_tables = collect_endpoints(Inventory(client=None).model_dump())
    ipf_tables.update(collect_endpoints(Technology(client=None).model_dump()))
    parser.add_argument(
        "ipf_tables",
        help="API or Front end URL for IP Fabric tables to fetch. Can be used multiple times.",
        metavar="table",
        nargs="+",
    )
    parser.add_argument(
        "-d",
        "--device-hostname",
        help="Device Hostname to fetch data for. Can be used multiple times; default to return all devices.",
        metavar="hostname",
        nargs="+",
        action="extend",
        default=[],
    )
    parser.add_argument(
        "-sn",
        "--device-sn",
        help="Device Serial Number to fetch data for. Can be used multiple times; default to return all devices.",
        metavar="sn",
        nargs="+",
        action="extend",
        default=[],
    )
    parser.add_argument(
        "-P",
        "--preview",
        action="store_true",
        help="Print first 3 rows of each table fetched",
        default=False,
    )
    parser.add_argument(
        "-D",
        "--device-separate",
        action="store_true",
        help="Creates a unique Excel Worksheet separately for each device for each table requested. "
        "Default is False and will return a single Worksheet for each table requested.",
        default=False,
    )
    parser.add_argument(
        "-f",
        "--filename",
        type=str,
        help="Name or Path of the output file",
        default="output.xlsx",
    )
    parser = base_args(parser)
    args = parse_base_args(parser.parse_args())
    if not args.ipf_tables:
        CONSOLE.print("[red]Error:[/red] No tables provided. Exiting...")
        exit(1)

    dataframes_for_export = get_tables(args)

    CONSOLE.print("Exporting data to excel...")

    args.filename = Path(args.filename).resolve().with_suffix(".xlsx").absolute()
    with pd.ExcelWriter(f"{args.filename}", engine="openpyxl") as writer:
        for index, df in enumerate(dataframes_for_export):
            sheet_name = re.sub(r"[\/\\\?\*\:\[\]]", "_", df.title)
            if len(sheet_name) > 31:
                CONSOLE.print(f"[yellow]Sheet name {sheet_name} is too long.[/yellow] Truncating to 31 characters.")
            df.to_excel(writer, sheet_name=f"{sheet_name[:31]}", index=False)
    CONSOLE.print(f"Export complete. Check {args.filename}")

    CONSOLE.print(":wave: Bye!")


if __name__ == "__main__":
    main()
