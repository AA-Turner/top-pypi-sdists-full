import json
import logging
import re
from typing import Any, Dict, Iterable, Optional
from urllib.parse import urlparse
import threading
from uuid import UUID

from packaging.version import parse as parse_version
import requests
from tabulate import tabulate

from rich.status import Status
from datafold_sdk.version import __version__
from datafold_sdk import sdk_log


def join_iter(joiner: Any, iterable: Iterable) -> Iterable:
    it = iter(iterable)
    try:
        yield next(it)
    except StopIteration:
        return
    for i in it:
        yield joiner
        yield i


def safezip(*args):
    "zip but makes sure all sequences are the same length"
    lens = list(map(len, args))
    if len(set(lens)) != 1:
        raise ValueError(f"Mismatching lengths in arguments to safezip: {lens}")
    return zip(*args)


UUID_PATTERN = re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", re.I)


def is_uuid(u: str) -> bool:
    # E.g., hashlib.md5(b'hello') is a 32-letter hex number, but not an UUID.
    # It would fail UUID-like comparison (< & >) because of casing and dashes.
    if not UUID_PATTERN.fullmatch(u):
        return False
    try:
        UUID(u)
    except ValueError:
        return False
    return True


def remove_passwords_in_dict(d: dict, replace_with: str = "***"):
    for k, v in d.items():
        if k == "password":
            d[k] = replace_with
        elif k == "filepath":
            if "motherduck_token=" in v:
                d[k] = v.split("motherduck_token=")[0] + f"motherduck_token={replace_with}"
        elif isinstance(v, dict):
            remove_passwords_in_dict(v, replace_with)
        elif k.startswith("database"):
            d[k] = remove_password_from_url(v, replace_with)


def _join_if_any(sym, args):
    args = list(args)
    if not args:
        return ""
    return sym.join(str(a) for a in args if a)


def remove_password_from_url(url: str, replace_with: str = "***") -> str:
    if "motherduck_token=" in url:
        replace_token_url = url.split("motherduck_token=")[0] + f"motherduck_token={replace_with}"
        return replace_token_url
    parsed = urlparse(url)
    account = parsed.username or ""
    if parsed.password:
        account += ":" + replace_with
    host = _join_if_any(":", filter(None, [parsed.hostname, parsed.port]))
    netloc = _join_if_any("@", filter(None, [account, host]))
    replaced = parsed._replace(netloc=netloc)
    return replaced.geturl()


def run_as_daemon(threadfunc, *args):
    th = threading.Thread(target=threadfunc, args=args)
    th.daemon = True
    th.start()
    return th


def getLogger(name):
    return logging.getLogger(name.rsplit(".", 1)[-1])


def truncate_error(error: str):
    first_line = error.split("\n", 1)[0]
    return re.sub("'(.*?)'", "'***'", first_line)


def dbt_diff_string_template(
    total_rows_table1: int,
    total_rows_table2: int,
    total_rows_diff: int,
    rows_added: int,
    rows_removed: int,
    rows_updated: int,
    rows_unchanged: str,
    extra_info_dict: Dict,
    extra_info_str: str,
    is_cloud: Optional[bool] = False,
    deps_impacts: Optional[Dict] = None,
) -> str:
    # main table
    main_rows = [
        ["Total", str(total_rows_table1), "", f"{total_rows_table2} [{diff_int_dynamic_color_template(total_rows_diff)}]"],
        ["Added", "", str(diff_int_dynamic_color_template(rows_added)), ""],
        ["Removed", "", str(diff_int_dynamic_color_template(-rows_removed)), ""],
        ["Different", "", str(rows_updated), ""],
        ["Unchanged", "", str(rows_unchanged), ""],
    ]

    main_headers = ["rows", "PROD", "<>", "DEV"]
    main_table = tabulate(main_rows, headers=main_headers)

    # diffs table
    diffs_rows = sorted(list(extra_info_dict.items()))

    diffs_headers = ["columns", "% diff values" if is_cloud else "# diff values"]
    diffs_table = tabulate(diffs_rows, headers=diffs_headers)

    # deps impacts table
    deps_impacts_table = ""
    if deps_impacts:
        deps_impacts_rows = list(deps_impacts.items())
        deps_impacts_headers = ["deps", "# data assets"]
        deps_impacts_table = f"\n\n{tabulate(deps_impacts_rows, headers=deps_impacts_headers)}"

    # combine all tables
    string_output = f"\n{main_table}\n\n{diffs_table}{deps_impacts_table}"

    return string_output


def diff_int_dynamic_color_template(diff_value: int) -> str:
    if not isinstance(diff_value, int):
        return diff_value

    if diff_value > 0:
        return f"[green]+{diff_value}[/]"
    if diff_value < 0:
        return f"[red]{diff_value}[/]"
    return "0"


def _jsons_equiv(a: str, b: str):
    try:
        return json.loads(a) == json.loads(b)
    except (ValueError, TypeError, json.decoder.JSONDecodeError):  # not valid jsons
        return False


def columns_removed_template(columns_removed: set) -> str:
    columns_removed_str = f"[red]Columns removed [-{len(columns_removed)}]:[/] [blue]{columns_removed}[/]\n"
    return columns_removed_str


def columns_added_template(columns_added: set) -> str:
    columns_added_str = f"[green]Columns added [+{len(columns_added)}]: {columns_added}[/]\n"
    return columns_added_str


def columns_type_changed_template(columns_type_changed) -> str:
    columns_type_changed_str = f"Type changed [{len(columns_type_changed)}]: [green]{columns_type_changed}[/]\n"
    return columns_type_changed_str


def no_differences_template() -> str:
    return "[bold][green]No row differences[/][/]\n"


def print_version_info() -> None:
    base_version_string = f"Running with datafold-sdk={__version__}"
    logger = getLogger(__name__)
    logger.addHandler(sdk_log.SDKLogHandler())

    latest_version = None
    try:
        response = requests.get(url="https://pypi.org/pypi/datafold-sdk/json", timeout=3)
        response.raise_for_status()
        response_json = response.json()
        latest_version = response_json["info"]["version"]
    except (requests.exceptions.RequestException, ValueError, KeyError) as ex:
        logger.debug(f"Failed checking version: {ex}")

    if latest_version and parse_version(__version__) < parse_version(latest_version):
        print(f"{base_version_string} (Update {latest_version} is available!)")
    else:
        print(base_version_string)


class LogStatusHandler(logging.Handler):
    """
    This log handler can be used to update a rich.status every time a log is emitted.
    """

    def __init__(self) -> None:
        super().__init__()
        self.status = Status("")
        self.prefix = ""
        self.diff_status : Dict[str, str] = {}

    def emit(self, record):
        log_entry = self.format(record)
        if self.diff_status:
            self._update_diff_status(log_entry)
        else:
            self.status.update(self.prefix + log_entry)

    def set_prefix(self, prefix_string):
        self.prefix = prefix_string

    def diff_started(self, model_name):
        self.diff_status[model_name] = "[yellow]In Progress[/]"
        self._update_diff_status()

    def diff_finished(self, model_name):
        self.diff_status[model_name] = "[green]Finished   [/]"
        self._update_diff_status()

    def _update_diff_status(self, log=None):
        status_string = "\n"
        for model_name, status in self.diff_status.items():
            status_string += f"{status} {model_name}\n"
        self.status.update(f"{status_string}{log or ''}")
