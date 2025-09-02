"""
Python3 script to search for Devices in the Inventory Table.
"""

import argparse
import csv
import json
import logging
import os
import re
import sys
from collections import defaultdict
from typing import Union

from ipfabric import IPFClient
from ipfabric.scripts.shared import shared_args, load_env

try:
    from rich.console import Console
    from rich.table import Table
    from rich import box
except ImportError:
    raise ImportError("Rich is required for printing, please install by using `pip3 install rich`.")

CONSOLE = Console()

logging.basicConfig(format="%(levelname)s: %(message)s")

LOGGER = logging.getLogger("ipf_device_search")

VALID_COLUMNS = {
    "uptime": {"name": "uptime", "filter": "float", "alt_name": None},
    "model": {"name": "model", "filter": "str", "alt_name": None},
    "reload": {"name": "reload", "filter": "str", "alt_name": None},
    "image": {"name": "image", "filter": "str", "alt_name": None},
    "domain": {"name": "domain", "filter": "str", "alt_name": None},
    "platform": {"name": "platform", "filter": "str", "alt_name": None},
    "slug": {"name": "slug", "filter": "str", "alt_name": None},
    "hostname": {"name": "hostname", "filter": "str", "alt_name": None},
    "fqdn": {"name": "fqdn", "filter": "str", "alt_name": None},
    "processor": {"name": "processor", "filter": "str", "alt_name": None},
    "sn": {"name": "sn", "filter": "str", "alt_name": None},
    "version": {"name": "version", "filter": "str", "alt_name": None},
    "vendor": {"name": "vendor", "filter": "str", "alt_name": None},
    "family": {"name": "family", "filter": "str", "alt_name": None},
    "stpdomain": {"name": "stpDomain", "filter": "str", "alt_name": "stp_domain"},
    "hostnameoriginal": {"name": "hostnameOriginal", "filter": "str", "alt_name": "hostname_original"},
    "loginip": {"name": "loginIpv4", "filter": "str", "alt_name": "login_ipv4"},
    "loginipv4": {"name": "loginIpv4", "filter": "str", "alt_name": "login_ipv4"},
    "loginipv6": {"name": "loginIpv6", "filter": "str", "alt_name": "login_ipv6"},
    "snhw": {"name": "snHw", "filter": "str", "alt_name": "sn_hw"},
    "memorytotalbytes": {"name": "memoryTotalBytes", "filter": "float", "alt_name": "mem_total_bytes"},
    "hostnameprocessed": {"name": "hostnameProcessed", "filter": "str", "alt_name": "hostname_processed"},
    "sitename": {"name": "siteName", "filter": "str", "alt_name": "site"},
    "devtype": {"name": "devType", "filter": "str", "alt_name": "dev_type"},
    "tsdiscoveryend": {"name": "tsDiscoveryEnd", "filter": "float", "alt_name": "ts_discovery_end"},
    "configreg": {"name": "configReg", "filter": "str", "alt_name": "config_reg"},
    "rd": {"name": "rd", "filter": "str", "alt_name": "routing_domain"},
    "memoryusedbytes": {"name": "memoryUsedBytes", "filter": "float", "alt_name": "mem_used_bytes"},
    "memoryutilization": {"name": "memoryUtilization", "filter": "float", "alt_name": "mem_utilization"},
    "secdiscoveryduration": {"name": "secDiscoveryDuration", "filter": "float", "alt_name": "sec_discovery_duration"},
    "logintype": {"name": "loginType", "filter": "str", "alt_name": "login_type"},
    "tsdiscoverystart": {"name": "tsDiscoveryStart", "filter": "float", "alt_name": "ts_discovery_start"},
    "loginport": {"name": "loginPort", "filter": "int", "alt_name": "login_port"},
    "objectid": {"name": "objectId", "filter": "str", "alt_name": "object_id"},
    "taskkey": {"name": "taskKey", "filter": "str", "alt_name": "task_key"},
}
VALID_ALT_COLUMNS = {_["alt_name"]: _ for _ in VALID_COLUMNS.values()}
COLUMNS_HELP = [
    f"{_['name']}{'|' + _['alt_name'] if _['alt_name'] else ''} ({_['filter']})" for _ in VALID_COLUMNS.values()
]
DEFAULT_COLUMNS = [
    "hostname",
    "siteName",
    "vendor",
    "family",
    "platform",
    "model",
    "version",
    "loginIpv4",
    "loginIpv6",
    "snHw",
    "devType",
]
STR_OPERATORS = {
    "=": "eq",
    "!=": "neq",
    "i=": "ieq",
    "i!=": "nieq",
    "~": "like",
    "!": "notlike",
    "=~": "reg",
    "!=~": "nreg",
    "i=~": "ireg",
    "i!=~": "nireg",
}
INT_OPERATORS = {
    "=": "eq",
    "!=": "neq",
    ">": "gt",
    ">=": "gte",
    "<": "lt",
    "<=": "lte",
}


def main() -> dict[str, dict[str, Union[str, list]]]:
    load_env()
    arg_parser = argparse.ArgumentParser(
        description="Search the Inventory > Device table and return the results.",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=f"""
Valid Column Names:
{json.dumps(COLUMNS_HELP, indent=2)}

String Operators:
{json.dumps(STR_OPERATORS, indent=2)}

Number Operators:
{json.dumps(INT_OPERATORS, indent=2)}
""",
    )
    arg_parser.add_argument(
        "search",
        help="Search value: 'ipf_device_search rtr1'. Default uses 'hostname' for search. "
        "Example for different column: 'ipf_device_search vendor cisco'.",
        nargs="+",
    )
    arg_parser.add_argument(
        "-o",
        "--operator",
        help="Operator used in searching; default is 'like'.",
        default="like",
    )
    arg_parser.add_argument(
        "-C",
        "--csv",
        help="Export to CSV format.",
        action="store_true",
        default=False,
    )
    arg_parser.add_argument(
        "-a",
        "--add-columns",
        help="Comma separated list of column names to add to output.",
        default=None,
    )
    arg_parser.add_argument(
        "-r",
        "--remove-columns",
        help="Comma separated list of column names to remove from output.",
        default=None,
    )
    arg_parser.add_argument(
        "-A",
        "--attribute",
        help="Do a Device Attribute search (operator chosen is applied to both name and value): "
        "'ipf_device_search -A attribute_name attribute_value'.",
        action="store_true",
        default=False,
    )
    arg_parser.add_argument(
        "-B",
        "--box-style",
        help="Table box style (see https://rich.readthedocs.io/en/stable/appendix/box.html#appendix-box for options).",
        default="HEAVY_HEAD",
    )
    args = shared_args(arg_parser, "ipf_device_search")

    column, columns, search, operator = validate_args(args)
    columns = modify_columns(columns, args.add_columns, args.remove_columns)

    results, filters, url = query_ipf(args, column, search, operator, columns)
    if args.json and args.rich_disable:
        print(json.dumps(results, indent=2))
    elif args.json:
        CONSOLE.print(results)
    else:
        styles = [_ for _ in dir(box) if isinstance(getattr(box, _), box.Box)]
        # Export BOX_STYLE=MARKDOWN before running commands for docs.
        box_style = os.getenv("BOX_STYLE").upper() if os.getenv("BOX_STYLE", None) else args.box_style.upper()
        if box_style in styles:
            box_style = getattr(box, box_style)
        else:
            LOGGER.warning(
                f'Box style "{box_style}" is not valid, defaulting to `HEAVY_HEAD`. ' f"Valid styles: {styles}."
            )
            box_style = box.HEAVY_HEAD
        rich_print(results, filters, url, columns, args.count, box_style)


def query_ipf(args: argparse.Namespace, column: str, search: str, operator: str, columns: list):
    ipf = IPFClient(snapshot_id=args.snapshot, base_url=args.base_url, auth=args.auth)
    ipf._client.headers["user-agent"] += "; ipf_device_search"
    if args.attribute:
        results = attribute_search(ipf, column, search, operator, columns)
        columns.insert(0, "attributes")
        if args.csv:
            writer = csv.DictWriter(
                sys.stdout, fieldnames=columns, lineterminator="\n", quotechar='"', quoting=csv.QUOTE_ALL
            )
            writer.writeheader()
            writer.writerows(results)
            exit(0)
        return results, None, None
    else:
        filters = {column: [operator, search]}
        if args.csv:
            print(ipf.inventory.devices.all(export="csv", filters=filters, columns=columns).decode())
            exit(0)
        return (
            ipf.inventory.devices.all(filters=filters, columns=columns),
            filters,
            ipf.oas["tables/inventory/devices"].post.filter_url(filters, ipf._client.base_url),
        )


def attribute_search(ipf: IPFClient, name: str, value: str, operator: str, columns: list):
    # Search Snapshot Attributes table for matching attributes.
    snap_attr = ipf.fetch_all(
        "tables/snapshot-attributes",
        columns=["sn", "name", "value"],
        filters={"and": [{"name": [operator, name]}, {"value": [operator, value]}]},
    )
    filters, dev_attr = defaultdict(set), defaultdict(list)
    for _ in snap_attr:
        dev_attr[_["sn"]].append(_)
        filters[_["name"]].add(_["value"])
    cols = columns.copy()
    if "sn" not in cols:
        cols.append("sn")
    results = dict()
    for key, value in filters.items():
        f = {key: list(value)}
        LOGGER.info(f"Querying using Attribute Filter: {f}.")
        # Attribute filters are "and" not "or" so we must do multiple searches based on Attribute key.
        for data in ipf.inventory.devices.all(attr_filters=f, columns=cols):
            sn = data["sn"] if "sn" in columns else data.pop("sn")
            if sn in results:
                # Do not return duplicates if it matches multiple attributes.
                continue
            data.update({"attributes": ",".join([f"{_['name']}={_['value']}" for _ in dev_attr[sn]])})
            results[sn] = data
    return list(results.values())


def modify_columns(columns: list, add: str, remove: str):
    cols = set(columns)
    if add:
        for _ in add.split(","):
            col = validate_column(_.lower())
            if col and col not in cols:
                columns.append(col)
    if remove:
        for _ in remove.split(","):
            col = validate_column(_.lower())
            if col and col in cols:
                columns.remove(_)
    return columns


def validate_column(column: str) -> str:
    if not column:
        return column
    if column not in VALID_COLUMNS and column not in VALID_ALT_COLUMNS:
        LOGGER.critical(
            f"Column '{column}' is not a valid column name. "
            f"Valid names:\n{json.dumps(sorted(COLUMNS_HELP), indent=2)}"
        )
        exit(1)
    return VALID_COLUMNS[column]["name"] if column in VALID_COLUMNS else VALID_ALT_COLUMNS[column]["name"]


def validate_operator(operator: str, col_filter: str):
    if col_filter == "str":
        if operator in STR_OPERATORS:
            operator = STR_OPERATORS[operator]
        elif operator not in STR_OPERATORS.values():
            LOGGER.critical(
                f"Operator '{operator}' is not valid for text column. "
                f"Valid operators:\n{json.dumps(list(STR_OPERATORS), indent=2)}"
            )
            exit(1)
    else:
        if operator in INT_OPERATORS:
            operator = INT_OPERATORS[operator]
        elif operator not in INT_OPERATORS.values():
            LOGGER.critical(
                f"Operator '{operator}' is not a valid for number column. "
                f"Valid operators:\n{json.dumps(list(INT_OPERATORS), indent=2)}"
            )
            exit(1)
    return operator


def validate_args(args: argparse.Namespace):
    if len(args.search) != 2 and args.attribute:
        LOGGER.critical(
            "Two positional arguments required for Attribute searching: "
            "'ipf_device_search -A attribute_name attribute_value'."
        )
        exit(1)
    if len(args.search) == 1:
        column, search, col_filter = "hostname", args.search[0], "str"
    elif len(args.search) == 2:
        if args.attribute:
            return (
                args.search[0],
                DEFAULT_COLUMNS.copy(),
                args.search[1],
                validate_operator(args.operator.lower(), "str"),
            )
        column, search = args.search[0].lower(), args.search[1]
        column = validate_column(column)
        col_filter = VALID_COLUMNS[column.lower()]["filter"]
    else:
        LOGGER.critical("Too many positional arguments given.")
        exit(1)

    operator = validate_operator(args.operator.lower(), col_filter)

    columns = DEFAULT_COLUMNS.copy()
    if column in columns:
        columns.remove(column)
    columns.insert(0, column)
    if column in ["secDiscoveryDuration", "uptime"]:
        search = time_converter(search)
    return column, columns, search, operator


def time_converter(search: Union[str, int, float]) -> int:
    if isinstance(search, (int, float)):
        return int(search)
    time_duration_units = {
        "year": 31557600,
        "month": 2629800,
        "week": 604800,
        "day": 86400,
        "hour": 3600,
        "minute": 60,
        "second": 1,
    }
    time_convert = {
        **time_duration_units,
        "y": time_duration_units["year"],
        "mon": time_duration_units["month"],
        "w": time_duration_units["week"],
        "d": time_duration_units["day"],
        "h": time_duration_units["hour"],
        "min": time_duration_units["minute"],
        "m": time_duration_units["minute"],
        "sec": time_duration_units["second"],
        "s": time_duration_units["second"],
    }
    _ = re.findall(r"(\d*)\s?([a-z]*)", search.lower())

    seconds = 0
    for v, d in _:
        try:
            v = int(v)
        except ValueError:
            continue
        if d != "s" and d[-1] == "s":
            d = d[:-1]
        seconds += v * time_convert[d]

    return seconds


def rich_print(
    results: list, filters: dict, url: str, columns: list, count: bool = False, box_style: box.Box = box.HEAVY_HEAD
):
    if count or not results:
        CONSOLE.print(f"Total rows: {str(len(results))}")
    if not count and results:
        if filters:
            table = Table(*columns, title="Device Inventory", caption=f"Filter: {json.dumps(filters)}", box=box_style)
        else:
            table = Table(*columns, title="Device Inventory", box=box_style)
        for result in results:
            table.add_row(*[str(result[c]) for c in columns])
        CONSOLE.print(table)
    if url:
        CONSOLE.print(url, style=f"link {url}")


if __name__ == "__main__":
    main()
