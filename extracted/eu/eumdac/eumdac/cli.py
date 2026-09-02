"""EUMETSAT Data Access Client"""

from __future__ import annotations

import argparse
import fnmatch
import itertools
import os
import re
import shlex
import shutil
import signal
import stat
import sys
import tempfile
from datetime import datetime, timedelta
from pathlib import Path
import time
from typing import TYPE_CHECKING, Any

import requests
import yaml
from requests.exceptions import HTTPError

import eumdac
from eumdac.cli_helpers import (
    CredentialsFileNotFoundError,
    _search,
    get_datastore,
    get_datatailor,
    load_credentials,
    parse_arguments_resources,
    parse_time_str,
    safe_run,
)
from eumdac.cli_subscriptions import subscription, handle_livefeed
import eumdac.common
from eumdac import DataTailor
from eumdac.arguments import (
    build_eumdac_parser,
    parse_isoformat_beginning_of_day_default,
    parse_isoformat_end_of_day_default,
)
from eumdac.cli_mtg_helpers import (
    build_entries_from_coverage,
    is_collection_valid_for_coverage,
    pretty_print_entry,
)
from eumdac.collection import SearchResults
from eumdac.config import get_config_dir, get_credentials_path
from eumdac.download_app import DownloadApp
from eumdac.errors import EumdacError
from eumdac.fake import FakeDataStore, FakeDataTailor  # type: ignore
from eumdac.local_tailor import (
    all_url_filenames,
    get_api_url,
    get_local_tailor,
    get_tailor_id,
    get_tailor_path,
    is_online,
    new_local_tailor,
    remove_local_tailor,
)
from eumdac.logging import gen_table_printer, init_logger, logger
from eumdac.order import (
    Order,
    all_order_filenames,
    get_default_order_archive_dir,
    get_default_order_dir,
    resolve_order,
    get_default_order_failed_dir,
    generate_order_name,
)
from eumdac.product import Product, ProductError
from eumdac.tailor_app import TailorApp
from eumdac.tailor_models import Chain, Filter, RegionOfInterest, Quicklook
from eumdac.token import AccessToken, AnonymousAccessToken, URLs

if TYPE_CHECKING:  # pragma: no cover
    from typing import Any, Callable, Collection, Dict, Iterator, Optional, Tuple, Union

    if sys.version_info < (3, 9):
        from typing import Iterable, Sequence
    else:
        from collections.abc import Iterable, Sequence


if not sys.platform.startswith("win"):
    # stop program on SIGPIPE to avoid e.g. eumdac describe | head to fail
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)

key_mgmt_url = URLs().get("token", "key_management")


def json_clean_unwrap(json_dic: dict[str, Any]) -> dict[str, Any]:
    if isinstance(json_dic, dict):
        return {
            key: json_clean_unwrap(value) for key, value in json_dic.items() if value is not None
        }
    elif isinstance(
        json_dic,
        (
            eumdac.tailor_models.Filter,
            eumdac.tailor_models.Quicklook,
            eumdac.tailor_models.RegionOfInterest,
        ),
    ):
        return {
            key: json_clean_unwrap(value)
            for key, value in vars(json_dic).items()
            if value is not None
        }
    else:
        return json_dic


def json_to_yaml(json_dic: dict[str, Any]) -> str:
    return yaml.dump(json_dic, default_flow_style=True, sort_keys=False, width=999)[1:-2]


def parse_size(size_str: str) -> int:
    size_str = size_str.upper()
    units = {"B": 1, "KB": 1024, "MB": 1024**2, "GB": 1024**3, "TB": 1024**4}
    match = re.match(r"^(\d+(?:\.\d+)?)\s*([KMGT]?B)$", size_str)
    if match:
        number, unit = match.groups()
        return int(float(number) * units[unit])
    else:
        raise ValueError("Invalid size format")


def set_credentials(values: Union[str, Sequence[Any], None]) -> None:
    token = eumdac.AccessToken(values)  # type: ignore[arg-type]

    try:
        logger.info(f"Credentials are correct. Token was generated: {token}")
    except HTTPError as e:
        if e.response.status_code == 401:
            logger.error(
                "The provided credentials are not valid. "
                f"Get your consumer key and secret at {key_mgmt_url}",
            )
        else:
            report_request_error(e.response)
        return

    try:
        config_dir = get_config_dir()
        config_dir.mkdir(exist_ok=True)
        credentials_path = get_credentials_path()
        credentials_path.touch(mode=(stat.S_IRUSR | stat.S_IWUSR))
        with credentials_path.open(mode="w") as file:
            file.write(",".join(values))  # type: ignore[arg-type]
        logger.info(f"Credentials are written to file {credentials_path}")
    except Exception as e:
        logger.error(
            f"Credentials could not be written to {credentials_path}. Please review your configuration."
        )


def token(args: argparse.Namespace) -> None:
    """eumdac token entrypoint"""

    try:
        creds = load_credentials()
    except CredentialsFileNotFoundError as exc:
        raise EumdacError("No credentials found! Please set credentials!") from exc

    try:
        old_token = ""
        validity = 86400 if not args.validity else args.validity
        token = AccessToken(creds, validity=validity)
        # Request the token value to fetch an actual token
        str(token)
        # Manage previously generated tokens: validity and expiration
        expires_in = token._expiration - time.time()
        logger.debug(f"Got token {token}, which expires in {expires_in:.2f} seconds")
        got_new_token = not (
            old_token == token._access_token
            or abs(expires_in - token.validity_period) > token.request_margin
        )

        if args.force:
            while not got_new_token:
                logger.debug(
                    f"Failed to get new token, got: {token._access_token}, which expires in: {expires_in} seconds"
                )
                old_token = token._access_token
                token._revoke()
                token._update_token_data()
                expires_in = token._expiration - time.time()
                logger.debug(f"Got token {token}, which expires in {expires_in} seconds.")
                got_new_token = not (
                    old_token == token._access_token
                    or abs(expires_in - token.validity_period) > token.request_margin
                )
            logger.warning("Existing tokens have been revoked as per the  --force parameter")
            logger.warning(
                "Note: this has invalidated any other token already in use, effecting other processes using the same credentials"
            )
        if not args.force and args.validity:
            logger.warning(
                f"The requested validity of {args.validity} seconds may not be applied if a valid token was already available"
            )
            logger.warning(
                "Use --force to revoke any current token and get a token with the desired validity, but this will effect other processes using the same credentials"
            )
        # Report the validity
        logger.warning(f"The following token is valid until {token.expiration}")
        # Show the token to the user
        print(token)
    except HTTPError as e:
        if e.response.status_code == 401:
            logger.error(
                "A token could not be generated with your current credentials. "
                f"Get your consumer key and secret from {key_mgmt_url}",
            )
        report_request_error(e.response)


def describe(args: argparse.Namespace) -> None:
    """eumdac describe entrypoint"""
    datastore = get_datastore(args, anonymous_allowed=True)
    if args.filter and (args.collection or args.product):
        raise ValueError("The -f/--filter flag and can't be used together with -c or -p")
    if args.collection is None and args.product is None:
        filter = str(args.filter).lower() if args.filter else ""
        for collection in datastore.collections:
            collection_str = f"{collection} - {collection.title}"
            if args.filter:
                collection_str_lowercase = collection_str.lower()
                if (filter in collection_str_lowercase) or (
                    fnmatch.fnmatch(collection_str_lowercase, filter)
                ):
                    logger.info(collection_str)
            else:
                logger.info(collection_str)
    elif args.collection is not None and args.product is None:
        collection = datastore.get_collection(args.collection)
        date = collection.metadata["properties"].get("date", "/")
        match = re.match(r"([^/]*)/([^/]*)", date)
        start_date, end_date = match.groups()  # type: ignore[union-attr]
        start_date = start_date or "-"
        end_date = end_date or "now"
        logger.info(f"{collection} - {collection.title}")
        logger.info(f"Date: {start_date} - {end_date}")
        logger.info(collection.abstract)
        logger.info(f'Licence: {"; ".join(collection.metadata["properties"].get("rights", "-"))}')
        logger.info("Search options:")
        for option in collection.search_options.items():
            extra_pad = "\t" if len(option[0]) < 8 else ""
            option_str = f"{option[0]}\t{extra_pad} - {option[1]['title']}"
            if option[1]["options"] and option[1]["options"][0]:
                option_str += f", accepts: {option[1]['options']}"
            cli_param = get_cli_parameter(option[0])
            if cli_param:
                option_str += f", in CLI {cli_param}"
            logger.info(option_str)
    elif args.collection is None and args.product is not None:
        raise ValueError("Please provide a collection id and a product id")
    else:
        noneLabel: str = "(Not available for product)"
        product = datastore.get_product(args.collection, args.product)
        attributes = {
            "Platform": product.satellite,
            "Instrument": product.instrument,
            "Acronym": noneLabel if (not product.acronym) else f"{product.acronym}",
            "Orbit": "GEO" if (not product.orbit_is_LEO) else "LEO",
            "Sensing Start": (
                noneLabel
                if (not product.sensing_start)
                else f"{product.sensing_start.isoformat(timespec='milliseconds')}Z"
            ),
            "Sensing End": (
                noneLabel
                if (not product.sensing_end)
                else f"{product.sensing_end.isoformat(timespec='milliseconds')}Z"
            ),
            "Size": f"{product.size} KB",
            "Published": (
                noneLabel
                if (not product.ingested)
                else f"{product.ingested.isoformat(timespec='milliseconds')}Z"
            ),
            "MD5": noneLabel if (not product.md5) else product.md5,
        }
        lines = [f"{product.collection} - {product}"] + [
            f"{key}: {value}" for key, value in attributes.items()
        ]
        logger.info("\n".join(lines))

        ## Add additional attributes for LEO products
        if product.orbit_is_LEO:
            LEO_attributes = {
                "Timeliness": product.timeliness,
                "Orbit Number": product.orbit_number,
                "Orbit Direction": product.orbit_direction,
                "Relative Orbit": product.relative_orbit,
                "Cycle Number": product.cycle_number,
            }
            lines = [f"{key}: {value}" for key, value in LEO_attributes.items() if value]
            logger.info("\n".join(lines))

        ## Add additional attributes for MTG products
        if product.is_mtg:
            MTG_attributes = {
                "Coverage": (
                    noneLabel if (not product.region_coverage) else f"{product.region_coverage}"
                ),
                "Sub-Region": (
                    noneLabel
                    if (not product.subregion_identifier)
                    else f"{product.subregion_identifier}"
                ),
                "Repeat Cycle": (
                    noneLabel if (not product.repeat_cycle) else f"{product.repeat_cycle}"
                ),
            }
            lines = [f"{key}: {value}" for key, value in MTG_attributes.items() if value]
            logger.info("\n".join(lines))

        if args.verbose:
            verbose_attributes = {
                "Processing Time": (
                    noneLabel if (not product.processingTime) else f"{product.processingTime}"
                ),
                "Processor Version": (
                    noneLabel if (not product.processorVersion) else f"{product.processorVersion}"
                ),
                "Format": noneLabel if (not product.format) else f"{product.format}",
                "Quality Status": (
                    noneLabel if (not product.qualityStatus) else f"{product.qualityStatus}"
                ),
            }
            lines = [f"{key}: {value}" for key, value in verbose_attributes.items() if value]
            logger.info("\n".join(lines))

        if product.entries:
            entries: list[str] = []
            if args.flat:
                entries = sorted(product.entries)
            else:
                entries = get_product_entries_tree(product.entries)
            lines = ["SIP Entries:"] + [f"  {filenames}" for filenames in entries]
            logger.info("\n".join(lines))


def get_product_entries_tree(entries: Iterable[str]) -> list[str]:
    output: list[str] = []
    groups: dict[str, list[str]] = {}
    for entry in sorted(entries):
        if entry.find("/") < 0:
            groups[entry] = []
        else:
            members = entry.split("/", 1)
            if members[0] not in groups:
                groups[members[0]] = [members[1]]
            else:
                groups[members[0]].append(members[1])

    for group in groups:
        is_group: bool = bool(groups[group])
        output.append(f"{'+' if is_group else '-'} {group}{('/' if is_group else '')}")
        if is_group:
            for child in sorted(groups[group]):
                output.append(f"  - {child}")

    return output


def get_cli_parameter(option: str) -> str:
    params = {
        "bbox": "--bbox",
        "geo": "--geometry",
        "title": "--filename",
        "sat": "--satellite",
        "dtstart": "-s, --start",
        "dtend": "-e, --end",
        "publication": "--publication-after, --publication-before",
        "sort": "--sort, --asc, --desc",
        "type": "--product-type, --acronym",
        "timeliness": "--timeliness",
        "orbit": "--orbit",
        "relorbit": "--relorbit",
        "cycle": "--cycle",
    }
    if option in params:
        return params[option]
    else:
        return ""


def _parse_timerange(args: argparse.Namespace) -> Tuple[datetime, datetime]:
    """
    Parses the time range provided as arguments.

    This function receives the parsed command-line arguments as an argparse.Namespace object.
    The function checks if the `--time-range` argument is used, and if so, it parses the start
    and end times from the provided time range. The start time defaults to the beginning of the day
    and the end time defaults to the end of the day if specific times are not provided.

    If the `--time-range` argument is not used, the function uses the `--start` (`dtstart`) and
    `--end` (`dtend`) arguments instead. If `--time-range` is used in combination with
    `--start` or `--end`, a ValueError is raised.

    Parameters:
        args (argparse.Namespace): The parsed command-line arguments.

    Returns:
        tuple: A tuple of two datetime objects representing the start and end of the time range.

    Raises:
        ValueError: If both --time-range and --start/--end are used.
    """
    if args.time_range and (args.dtstart or args.dtend):
        raise ValueError("You can't combine --time-range and --start/--end.")

    if args.time_range:
        start, end = args.time_range
        start = parse_isoformat_beginning_of_day_default(start)
        end = parse_isoformat_end_of_day_default(end)
    else:
        start = args.dtstart
        end = args.dtend
    return start, end


def search(args: argparse.Namespace) -> None:
    """eumdac search entrypoint"""
    products_query, products_count = _search(args)

    limit = args.limit
    products = itertools.islice(products_query, limit)

    if args.daily_window:
        daily_window_start: datetime = parse_time_str(args.daily_window[0])
        daily_window_end: datetime = parse_time_str(args.daily_window[1])
        if daily_window_start > daily_window_end:
            raise ValueError(
                f"The daily window start time must be earlier than the end time. Please review the provided window: {datetime.strftime(daily_window_start, '%H:%M:%S')} - {datetime.strftime(daily_window_end, '%H:%M:%S')}"
            )
        logger.warning(
            f"The search found {products_count} products, but only those within the daily time window are returned: {datetime.strftime(daily_window_start, '%H:%M:%S')} - {datetime.strftime(daily_window_end, '%H:%M:%S')}"
        )

    def is_product_within_daily_window(
        product: Product, daily_window_start: datetime, daily_window_end: datetime
    ) -> bool:
        return (
            product.sensing_end.time() >= daily_window_start.time()
            and product.sensing_start.time() <= daily_window_end.time()
        )

    num_filtered_products = 0
    for product in products:
        if not args.daily_window or is_product_within_daily_window(
            product, daily_window_start, daily_window_end
        ):
            num_filtered_products += 1
            logger.info(str(product).replace("\r\n", "-"))

    if num_filtered_products == 0:
        logger.error("No products were found for the given search parameters")


def download(args: argparse.Namespace) -> None:
    """eumdac download entrypoint"""
    datastore = get_datastore(args)
    products: Union[SearchResults, Collection[Product]]
    collection: str
    products_count: int

    if args.query:
        # Search using a query
        products, products_count = _search(args)
        collection = str([products.collection])
    else:
        # Search using CLI parameters or product
        if not args.collection:
            raise ValueError("Please provide a (single) collection.")

        if args.product:
            if args.dtstart or args.dtend:
                logger.warning(
                    "Parameter(s) for filtering using sensing time ignored as specific product ID was given."
                )
            if args.publication_after or args.publication_before:
                logger.warning(
                    "Parameter(s) for filtering using sensing time ignored as specific product ID was given."
                )
            if args.bbox or args.geo:
                logger.warning(
                    "Parameter(s) for filtering using spatial geometry ignored as specific product ID was given."
                )
            if args.sat:
                logger.warning(
                    "Parameter for filtering using satellite/platform ignored as specific product ID was given."
                )
            if args.product_type:
                logger.warning(
                    "Parameter for filtering using product type/acronym ignored as specific product ID was given."
                )
            if args.cycle or args.orbit or args.relorbit:
                logger.warning(
                    "Parameter(s) for filtering using acquisition parameters ignored as specific product ID was given."
                )
            if args.filename:
                logger.warning(
                    "Parameter for filtering using filename/title ignored as specific product ID was given."
                )
            if args.timeliness:
                logger.warning(
                    "Parameter for filtering using timeliness ignored as specific product ID was given."
                )

        collection = args.collection

        if args.product:
            products = []
            for pid in args.product:
                pid = pid.strip()
                if pid:
                    products.append(datastore.get_product(collection, pid))
            products_count = len(products)
        else:
            products, products_count = _search(args)

    if args.integrity:
        if args.download_coverage:
            logger.warning("Ignoring --integrity flag as --download-coverage was provided.")
            args.integrity = False
        elif args.entry:
            logger.warning("Ignoring --integrity flag as --entry was provided.")
            args.integrity = False

    # Apply --limit argument if provided
    if args.limit and not args.product and products_count > args.limit:
        products = itertools.islice(products, args.limit)  # type: ignore
        products_count = args.limit

    plural = "" if products_count == 1 else "s"
    logger.info(f"Processing {products_count} product{plural}.")

    if args.daily_window:
        daily_window_start: datetime = parse_time_str(args.daily_window[0])
        daily_window_end: datetime = parse_time_str(args.daily_window[1])
        if daily_window_start > daily_window_end:
            raise ValueError(
                f"The daily window start time must be earlier than the end time. Please review the provided window: {datetime.strftime(daily_window_start, '%H:%M:%S')} - {datetime.strftime(daily_window_end, '%H:%M:%S')}"
            )
        logger.info(
            f"Filtering products by daily search window: {datetime.strftime(daily_window_start, '%H:%M:%S')} - {datetime.strftime(daily_window_end, '%H:%M:%S')}"
        )

        filtered_products = []
        for product in products:
            if (
                product.sensing_end.time() >= daily_window_start.time()
                and product.sensing_start.time() <= daily_window_end.time()
            ):
                filtered_products.append(product)
        products = filtered_products
        total_count = products_count
        products_count = len(products)
        logger.info(
            f"From the {total_count} products found, only {products_count} sensed within the daily time window will be downloaded."
        )

    if products_count >= 10 and not args.yes:
        user_in = input("Do you want to continue (Y/n)? ")
        if user_in.lower() == "n":
            return

    order = Order()

    try:
        query = products.search_query  # type: ignore
    except AttributeError:
        query = None

    if args.download_coverage:
        # Check that a valid, pdu-based collection has been provided (MTG FCI 1C)
        if not is_collection_valid_for_coverage(collection):
            logger.error(f"Collection {collection} does not support coverage area downloads.")
            logger.error(
                f"Remove coverage: {args.download_coverage} parameter or provide a different collection."
            )
            return
        # Complain about entry being provided with coverage
        if args.entry:
            logger.warning(
                f"The provided --entry values {args.entry} will be discarded in favour of the coverage parameter."
            )
        # Prepare multi-entry considering coverage
        args.entry, expected = build_entries_from_coverage(args.download_coverage)
        # Check first if all the chunks are in the product
        if args.entry:
            for product in products:
                matches = []
                for pattern in args.entry:
                    matches.extend(fnmatch.filter(product.entries, pattern))
                logger.info(f"{len(matches)} entries will be downloaded for {product}")
                if args.verbose:
                    logger.info(
                        "\n".join([f"  - {pretty_print_entry(match)}" for match in sorted(matches)])
                    )
                if len(matches) < expected:
                    logger.warning(
                        f"Warning: not all the expected chunks could be found: found {len(matches)} out of {expected}"
                    )

    if args.chain:
        datatailor = get_datatailor(args, datastore.token)
        chain = parse_arguments_resources(args.chain, datatailor, resource="chains")
        order.initialize(
            chain,
            products,
            Path(args.output_dir),
            args.entry,
            query,
            args.dirs,
            args.onedir,
            args.no_warning_logs,
        )
        app: Any = TailorApp(order, datastore, datatailor)
    else:
        order.initialize(
            None,
            products,
            Path(args.output_dir),
            args.entry,
            query,
            args.dirs,
            args.onedir,
            args.no_warning_logs,
        )
        app = DownloadApp(
            order,
            datastore,
            integrity=args.integrity,
            download_threads=args.download_threads,
            chunk_size=parse_size(args.chunk_size) if args.chunk_size else None,
        )

    if args.dirs:
        logger.warning("A subdirectory per product will be created, as per the --dirs option")
    if args.onedir:
        logger.warning("Subdirectories per product will not be created, as per the --onedir option")

    success = safe_run(
        app,
        collection=collection,
        num_products=products_count,
        keep_order=args.keep_order,
    )
    if not success:
        raise EumdacError("Downloads didn't finish successfully")


def download_cart(args: argparse.Namespace) -> None:
    cart_filename = args.file
    datastore = get_datastore(args)
    products = []
    try:
        from xml.dom.minidom import parse

        cart_dom = parse(cart_filename)
        urls = cart_dom.getElementsByTagName("url")
        for u in urls:
            product: Product = datastore.get_product_from_url(u.firstChild.data)  # type: ignore
            products.append(product)
    except eumdac.datastore.DataStoreError:
        raise
    except Exception as e:
        logger.error(f"Cart XML file could not be read due to {e}")
        sys.exit(1)

    products_count = len(products)
    plural = "" if products_count == 1 else "s"
    logger.info(f"Processing {products_count} product{plural}.")

    if products_count >= 10 and not args.yes:
        user_in = input("Do you want to continue (Y/n)? ")
        if user_in.lower() == "n":
            return

    order = Order()

    order.initialize(
        None,
        products,
        Path(args.output_dir),
        None,
        None,
        args.dirs,
        False,
        False,
    )
    app = DownloadApp(order, datastore, integrity=args.integrity)

    if args.dirs:
        logger.warning("A subdirectory per product will be created, as per the --dirs option")

    success = safe_run(
        app, collection=None, num_products=products_count, keep_order=args.keep_order
    )
    if not success:
        raise EumdacError("Downloads didn't finish successfully")


def order(args: argparse.Namespace) -> None:
    """eumdac order entrypoint"""
    orders_dir = get_default_order_dir()
    if args.order_command != "housekeep":
        if args.failed and args.archived:
            logger.error("Please provide only one of the following flags: --failed, --archived")
            return
        if args.failed:
            orders_dir = get_default_order_failed_dir()
        elif args.archived:
            orders_dir = get_default_order_archive_dir()

    if args.order_command == "list":
        filenames = list(all_order_filenames(orders_dir))
        orders_label = " archived " if args.archived else (" failed " if args.failed else " ")
        logger.info(f"Found {len(filenames)}{orders_label}order(s):")
        # Reverse the list if needed
        # Note: all_order_filenames returns the list in asc order
        #       but the user expects newer orders first
        #       so the list is reversed when user wants reverse order
        if not args.reverse:
            filenames.reverse()
        full_filenames_length = -1
        # Show only the first 10 orders unless verbose mode is on
        if len(filenames) > 10 and not args.verbose:
            full_filenames_length = len(filenames)
            filenames = filenames[:10]
        table_printer = gen_table_printer(
            logger.info,
            [
                ("Order ID", len(generate_order_name()) - 4),  # remove .yml extension
                ("Created on", 10),
                ("Products", 8),
                ("Tailor", 6),
                ("Status", 15),
                ("Collection", 28),
            ],
            column_sep="  ",
        )
        for filename in filenames:
            try:
                order = Order(filename)
                with order.dict_from_file() as order_d:
                    table_printer(
                        [
                            filename.stem,  # order_id
                            filename.stem.split("#")[0],  # created
                            str(len(order_d["products_to_process"])),  # products
                            "Yes" if order_d["type"] == "tailor" else "No",  # tailor
                            order.status(),  # status
                            ", ".join(order.collections()),  # collection
                        ]
                    )
            except (EumdacError, KeyError, yaml.scanner.ScannerError):
                logger.error(f"{filename.stem}  is corrupted.")
        # Notify about the reduced list being shown
        if full_filenames_length > 0:
            logger.info(
                f"Showing only the {'last' if args.reverse else 'first'} 10 out of {full_filenames_length} orders, use -v to show all of them"
            )
        return
    elif args.order_command == "housekeep":
        filenames = list(all_order_filenames(orders_dir))
        archive_dir = get_default_order_archive_dir()
        logger.info(f"Housekeeping {len(filenames)} orders.")
        logger.info(f"Moving orders older than 1 week to the archive in {archive_dir}")
        moved_files = 0
        for filename in filenames:
            if datetime.strptime(filename.stem.split("#")[0], "%Y-%m-%d") < (
                datetime.now() - timedelta(weeks=1)
            ):
                shutil.move(str(filename), archive_dir / filename.name)
                moved_files += 1
        logger.info(f"Moved {moved_files} order files to {archive_dir}")
        failed_dir = get_default_order_failed_dir()
        failed_orders = len(all_order_filenames(failed_dir))
        if failed_orders > 10:
            logger.warning(
                f"There are {failed_orders} in {failed_dir}. Consider deleting them running:\n\teumdac order delete --failed."
            )
        archived_orders = len(all_order_filenames(archive_dir))
        if archived_orders > 100:
            logger.warning(
                f"There are {archived_orders} in {archive_dir}. Consider deleting them running:\n\teumdac order delete --archived."
            )
        return

    order_name = args.order_id
    # Pretty print the order name
    printable_order_name = ""
    if not order_name == "latest":
        printable_order_name = f" {order_name}"
    if args.failed:
        printable_order_name = f"failed order{printable_order_name}"
    elif args.archived:
        printable_order_name = f"archived order{printable_order_name}"
    else:
        printable_order_name = f"order{printable_order_name}"

    if order_name == "latest":
        printable_order_name = f"latest {printable_order_name}"

    order = resolve_order(orders_dir, order_name)

    if not order._order_file.is_file():
        logger.info(f"Order {order_name} doesn't exist.")
        sys.exit(1)

    if args.order_command == "status":
        logger.info(order.pretty_string(print_products=args.verbose))
        if not args.verbose:
            logger.info("")
            logger.info("Use the -v flag to see more details")
        return

    if args.order_command == "restart":
        order.reset_states()

    if args.order_command == "delete":
        if args.all:
            filenames = list(all_order_filenames(orders_dir))
            logger.info(f"Deleting {len(filenames)} order(s):")
            for filename in filenames:
                try:
                    order = Order(filename)
                    order.delete()
                    logger.info(f"Order {order} successfully deleted.")
                except Exception as err:
                    logger.error(f"Unable to delete order {order} due to: {err}")
        elif order._order_file.is_file():
            delete = True
            if not args.yes:
                user_in = input(f"Are you sure you want to delete {printable_order_name}? (Y/n): ")
                delete = not (user_in.lower() == "n")
            if delete:
                try:
                    order.delete()
                    logger.info(f"Successfully deleted {printable_order_name}.")
                except:
                    logger.warning(f"Could not delete {printable_order_name}.")
            else:
                logger.info(f"{printable_order_name.capitalize()} wasn't deleted.")
        else:
            logger.info(f"{printable_order_name.capitalize()} doesn't exist.")
        sys.exit(1)

    (typ,) = order.get_dict_entries("type")
    if typ == "download":
        if args.integrity and order.get_dict_entries("file_patterns")[0]:
            logger.warning("Ignoring --integrity flag as Order is configured to download entries.")
            args.integrity = False
        app: Any = DownloadApp(
            order,
            get_datastore(args),
            integrity=args.integrity,
            download_threads=args.download_threads,
            chunk_size=parse_size(args.chunk_size) if args.chunk_size else None,
        )

    elif typ == "tailor":
        if order.all_done():
            logger.info("Order already completed")
            return
        datastore = get_datastore(args)
        app = TailorApp(order, datastore, get_datatailor(args, datastore.token))

    else:
        raise Exception(f"Unknown Order Type: {typ}")

    success = safe_run(app, keep_order=args.keep_order)
    if not success:
        raise EumdacError("Process didn't finish successfully")


def local_tailor(args: argparse.Namespace) -> None:
    """eumdac config entrypoint"""
    if args.local_tailor_command == "set":
        old_url = ""
        try:
            try:
                old_url = get_api_url(get_tailor_path(args.localtailor_id[0]))
            except:
                pass

            local_tailor_config_path = new_local_tailor(
                args.localtailor_id[0], args.localtailor_url[0]
            )

            logger.info(
                f"Local tailor instance {get_tailor_id(local_tailor_config_path)} is configured with the following address: {get_api_url(local_tailor_config_path)}"
            )
            if old_url:
                logger.warning(
                    f"This replaces the previous address for {get_tailor_id(local_tailor_config_path)}: {old_url}"
                )
            if not is_online(local_tailor_config_path):
                logger.warning(
                    "Note that the provided local-tailor instance address is unavailable at the moment"
                )

        except EumdacError as e:
            logger.error(
                f"The provided address {args.localtailor_url[0]} appears to be invalid: {e}"
            )
            # Don't remove existing instances
            if not old_url:
                remove_local_tailor(args.localtailor_id[0])

    elif args.local_tailor_command == "remove":
        try:
            local_tailor_config_path = get_tailor_path(args.localtailor_id[0])
            logger.info(
                f"Local tailor instance {get_tailor_id(local_tailor_config_path)} is removed"
            )
            remove_local_tailor(args.localtailor_id[0])
        except EumdacError as e:
            logger.error(f"Could not remove local tailor instance: {e}")

    elif args.local_tailor_command == "show":
        table_printer = gen_table_printer(logger.info, [("Name", 10), ("URL", 40), ("Status", 8)])
        local_tailor_config_path = get_tailor_path(args.localtailor_id[0])
        table_printer(
            [
                get_tailor_id(local_tailor_config_path),
                get_api_url(local_tailor_config_path),
                "ONLINE" if is_online(local_tailor_config_path) else "OFFLINE",
            ]
        )

    elif args.local_tailor_command == "instances":
        table_printer = gen_table_printer(logger.info, [("Name", 10), ("URL", 40), ("Status", 8)])
        for filepath in all_url_filenames():
            if filepath.exists():
                line = [
                    get_tailor_id(filepath),
                    get_api_url(filepath),
                    "ONLINE" if is_online(filepath) else "OFFLINE",
                ]
                table_printer(line)

    else:
        raise EumdacError(f"Unsupported clear command: {args.local_tailor_command}")


def tailor_post_job(args: argparse.Namespace) -> None:
    """eumdac tailor post entrypoint"""
    from eumdac.tailor_models import Chain

    datastore = get_datastore(args)
    datatailor = get_datatailor(args, datastore.token)
    collection_id = args.collection
    product_ids = args.product

    if not args.collection or not args.product or not args.chain:
        raise ValueError("Please provide collection ID, product ID and a chain file!")

    chain = parse_arguments_resources(args.chain, datatailor, resource="chains")
    products = [datastore.get_product(collection_id, product_id) for product_id in product_ids]
    try:
        customisation = datatailor.new_customisations(products, chain=chain)
        jobidsToStr = "\n".join([str(jobid) for jobid in customisation])
        logger.info("Customisation(s) has been started.")
        logger.info(jobidsToStr)
    except requests.exceptions.HTTPError as exception:
        messages = {
            400: "Collection ID and/or Product ID does not seem to be a valid. See below:",
            500: "There was an issue on server side. See below:",
            0: "An error occurred. See below:",
            -1: "An unexpected error has occurred.",
        }
        report_request_error(exception.response, None, messages=messages)


def tailor_list_customisations(args: argparse.Namespace) -> None:
    """eumdac tailor list entrypoint"""
    datatailor = get_datatailor(args)
    try:
        customisations = datatailor.customisations
        if not customisations:
            logger.error("No customisations available")
        else:
            table_printer = gen_table_printer(
                logger.info,
                [("Job ID", 10), ("Status", 8), ("Product", 10), ("Creation Time", 20)],
            )
            for customisation in datatailor.customisations:
                line = [
                    str(customisation),
                    customisation.status,
                    customisation.product_type,
                    str(customisation.creation_time),
                ]
                table_printer(line)
    except requests.exceptions.HTTPError as exception:
        report_request_error(exception.response)


def tailor_show_status(args: argparse.Namespace) -> None:
    """eumdac tailor status entrypoint"""
    datatailor = get_datatailor(args)
    if args.verbose:
        table_printer = gen_table_printer(
            logger.info,
            [("Job ID", 10), ("Status", 8), ("Product", 10), ("Creation Time", 20)],
        )
        for customisation_id in args.job_ids:
            try:
                customisation = datatailor.get_customisation(customisation_id)
                line = [
                    str(customisation),
                    customisation.status,
                    customisation.product_type,
                    str(customisation.creation_time),
                ]
                table_printer(line)
            except requests.exceptions.HTTPError as exception:
                report_request_error(exception.response, customisation_id)
    else:
        for customisation_id in args.job_ids:
            try:
                customisation = datatailor.get_customisation(customisation_id)
                logger.info(customisation.status)
            except requests.exceptions.HTTPError as exception:
                report_request_error(exception.response, customisation_id)


def tailor_get_log(args: argparse.Namespace) -> None:
    """eumdac tailor log entrypoint"""
    datatailor = get_datatailor(args)
    try:
        customisation = datatailor.get_customisation(args.job_id)
        logger.info(customisation.logfile)
    except requests.exceptions.HTTPError as exception:
        report_request_error(exception.response, args.job_id)


def tailor_quota(args: argparse.Namespace) -> None:
    """eumdac tailor quota entrypoint"""
    datatailor = get_datatailor(args)
    user_name = datatailor.user_info["username"]
    quota_info = datatailor.quota["data"][user_name]
    is_quota_active = quota_info["disk_quota_active"]

    logger.info(f"Usage: {round(quota_info['space_usage'] / 1024, 1)} Gb")
    if is_quota_active:
        logger.info(f"Percentage: {round(quota_info['space_usage_percentage'], 1)}%")
        if args.verbose:
            logger.info(f"Available: {round(quota_info['user_quota'] / 1024, 1)} Gb")
    else:
        logger.info("No quota limit set in the system")

    if args.verbose:
        logger.info(f"Workspace usage: {round(quota_info['workspace_dir_size'] / 1024, 1)} Gb")
        logger.info(f"Logs space usage: {round(quota_info['log_dir_size'], 3)} Mb")
        logger.info(f"Output usage: {round(quota_info['output_dir_size'], 1)} Mb")
        logger.info(f"Jobs: {quota_info['nr_customisations']}")


def tailor_resources(args: argparse.Namespace) -> None:
    """eumdac tailor resources entrypoint"""
    resource = args.resources_command
    datatailor = get_datatailor(args)

    # Get the appropriate resource manager based on resource type
    resource_managers = {
        "filters": datatailor.filters,
        "rois": datatailor.rois,
        "quicklooks": datatailor.quicklooks,
        "chains": datatailor.chains,
    }

    resource_manager = resource_managers[resource]
    resource_singular = resource[:-1]  # Remove 's' to get singular form

    # Save
    if args.save:
        logger.info(f"Saving {resource_singular}")
        try:
            resource_to_save = parse_arguments_resources(args.save, datatailor, resource=resource)
            resource_manager.create(model=resource_to_save)
            logger.info(f"Resource {resource_singular} successfully saved")
        except Exception as e:
            if "already exists" in str(e):
                logger.error(
                    f"A {resource_singular} with ID '{resource_to_save.id}' already exists. Use '--update' to save anyway"
                )
            else:
                logger.error(e)
    # Update
    elif args.update:
        logger.info(f"Updating {resource_singular}")
        try:
            resource_to_update = parse_arguments_resources(
                args.update, datatailor, resource=resource
            )
            resource_manager.update(model=resource_to_update)
            logger.info(f"Resource {resource_singular} successfully updated")
        except Exception as e:
            logger.error(e)
    # Delete
    elif args.delete:
        logger.info(f"Deleting {resource_singular}")
        try:
            resource_id_to_delete = args.delete
            resource_manager.delete(model=resource_id_to_delete)
            logger.info(f"Resource {resource_singular} successfully deleted")
        except Exception as e:
            logger.error(e)
    # Show specific
    elif args.id:
        try:
            resource_info = resource_manager.read(model_id=args.id)
            if not args.raw:
                breakline = "\n"
                logger.info(f"{breakline}{resource_info.id}")
            else:
                breakline = ""
            resource_json = json_clean_unwrap(vars(resource_info))
            resource_yaml = json_to_yaml(resource_json)
            logger.info(f"{resource_yaml}")
        except Exception as e:
            logger.error(e)
    # Show all if no args are passed
    else:
        resource_info = resource_manager.search()
        if not args.raw:
            logger.info(f"Available {resource}:")
        for resource_i in resource_info:
            if args.verbose:
                if not args.raw:
                    breakline = "\n"
                    logger.info(f"{breakline}{resource_i.id}")
                else:
                    breakline = ""
                resource_json = json_clean_unwrap(vars(resource_i))
                resource_yaml = json_to_yaml(resource_json)
                logger.info(f"{resource_yaml}")
            else:
                logger.info(f"{resource_i.id}")


def tailor_delete_jobs(args: argparse.Namespace) -> None:
    """eumdac tailor delete entrypoint"""
    datatailor = get_datatailor(args)
    for customisation_id in args.job_ids:
        customisation = datatailor.get_customisation(customisation_id)
        try:
            customisation.delete()
            logger.info(f"Customisation {customisation_id} has been deleted.")
        except requests.exceptions.HTTPError as exception:
            if exception.response.status_code >= 400:
                report_request_error(exception.response, customisation_id)


def tailor_cancel_jobs(args: argparse.Namespace) -> None:
    """eumdac tailor cancel entrypoint"""
    datatailor = get_datatailor(args)

    for customisation_id in args.job_ids:
        customisation = datatailor.get_customisation(customisation_id)
        try:
            customisation.kill()
            logger.info(f"Customisation {customisation_id} has been cancelled.")
        except requests.exceptions.HTTPError as exception:
            messages = {
                400: f"{customisation_id} is already cancelled or job id is invalid. See below:",
                500: "There was an issue on server side. See below:",
                0: "An error occurred. See below:",
                -1: "An unexpected error has occurred.",
            }
            report_request_error(exception.response, None, messages=messages)


def tailor_clear_jobs(args: argparse.Namespace) -> None:
    """eumdac tailor clear entrypoint"""
    datatailor = get_datatailor(args)

    jobs_to_clean = args.job_ids

    if args.all and len(args.job_ids) > 0:
        logger.info(
            "All flag provided. Ignoring the provided customization IDs and clearing all jobs"
        )

    if args.all:
        # Fetch all job ids
        jobs_to_clean = datatailor.customisations

    for customisation in jobs_to_clean:
        # If we are provided a job id, get the customisation
        if isinstance(customisation, str):
            customisation_id = customisation
            customisation = datatailor.get_customisation(customisation)
        else:
            customisation_id = customisation._id

        try:
            if (
                customisation.status == "QUEUED"
                or customisation.status == "RUNNING"
                or customisation.status == "INACTIVE"
            ):
                customisation.kill()
                logger.info(f"Customisation {customisation_id} has been cancelled.")
        except requests.exceptions.HTTPError as exception:
            messages = {
                400: f"{customisation_id} is already cancelled or job id is invalid. See below:",
                500: "There was an issue on server side. See below:",
                0: "An error occurred. See below:",
                -1: "An unexpected error has occurred.",
            }
            report_request_error(exception.response, None, messages=messages)

        try:
            customisation.delete()
            logger.info(f"Customisation {customisation_id} has been deleted.")
        except requests.exceptions.HTTPError as exception:
            report_request_error(exception.response, customisation_id)


def tailor_download(args: argparse.Namespace) -> None:
    """eumdac tailor download entrypoint"""
    creds = load_credentials()
    token = AccessToken(creds)
    customisation = eumdac.datatailor.Customisation(args.job_id, datatailor=DataTailor(token))
    results: Iterable[str] = customisation.outputs
    logger.info(f"Output directory: {os.path.abspath(args.output_dir)}")
    if not os.path.exists(args.output_dir):
        logger.info(f"Output directory {args.output_dir} does not exist. It will be created.")
        os.makedirs(args.output_dir)
    # Download all the output files into the output path
    logger.info(f"Downloading {len(results)} output products")  # type: ignore
    for result in results:
        product_name = os.path.basename(result)
        logger.info("Downloading " + product_name)

        with tempfile.TemporaryDirectory(dir=args.output_dir, suffix=".tmp") as tempdir:
            tmp_prod_p = Path(tempdir) / str(product_name)
            with tmp_prod_p.open("wb") as tmp_prod:
                with customisation.stream_output_iter_content(result) as chunks:
                    for chunk in chunks:
                        tmp_prod.write(chunk)
            shutil.move(str(tmp_prod_p), str(args.output_dir) + "/" + product_name)
            logger.info(f"{product_name} has been downloaded.")


def report_request_error(
    response: requests.Response,
    cust_id: Optional[str] = None,
    messages: Optional[Dict[int, str]] = None,
) -> None:
    """helper function report requests errors to the user"""
    if messages is not None:
        _messages = messages
    else:
        _messages = {
            400: "There was an issue on client side. See below:",
            500: "There was an issue on server side. See below:",
            0: "An error occurred. See below:",
            -1: "An unexpected error has occurred.",
        }
        if cust_id is not None:
            _messages[400] = f"{cust_id} does not seem to be a valid job id. See below:"

    def _message_func(status_code: Optional[int] = None) -> str:
        try:
            if not status_code:
                return _messages[-1]

            if 400 <= status_code < 500:
                return _messages[400]

            elif status_code >= 500:
                return _messages[500]
            return _messages[0]
        except KeyError:
            return "Error description not found"
        return "Unexpected error"

    message = _message_func(response.status_code)

    logger.error(message)
    logger.error(f"{response.status_code} - {response.text}")


def get_piped_args() -> str:
    """
    Attempt to read from standard input (stdin) and return the contents as a string.

    This function is designed to handle being executed in a variety of environments,
    including being called with 'nohup', in which case stdin may not be accessible.
    In such a scenario, it will log a warning and return an empty string.

    :return: A string containing the data read from stdin, or an empty string if stdin
             is not accessible (for example, when the script is executed with 'nohup').
    """
    try:
        return sys.stdin.read()
    except OSError:
        logger.warning(
            "Received OSError when trying to read stdin. "
            "This is expected when executed with nohup."
        )
        return ""


def cli(command_line: Optional[Sequence[str]] = None) -> None:
    """eumdac CLI entrypoint"""
    init_logger("INFO")

    # Change referer to mark CLI usage
    eumdac.common.headers["referer"] = "EUMDAC.CLI"

    # append piped args
    if not sys.stdin.isatty():
        pipe_args = get_piped_args()
        if pipe_args:
            sys.argv.extend(shlex.split(pipe_args))

    if command_line is not None:
        # when we are called directly (e.g. by tests) then mimic a call from
        # commandline by setting sys.argv accordingly
        sys.argv = ["eumdac"] + list(command_line)

    parser = build_eumdac_parser(
        set_credentials,
        token,
        describe,
        search,
        download,
        download_cart,
        tailor_post_job,
        tailor_cancel_jobs,
        tailor_clear_jobs,
        tailor_delete_jobs,
        tailor_download,
        tailor_get_log,
        tailor_list_customisations,
        tailor_quota,
        tailor_resources,
        tailor_show_status,
        local_tailor,
        order,
        subscription,
        handle_livefeed,
    )

    args = parser.parse_args(command_line)
    if hasattr(args, "time_range"):
        args.dtstart, args.dtend = _parse_timerange(args)
        del args.time_range

    # initialize logging
    progress_bars = not getattr(args, "no_progress_bars", False)

    if args.trace:
        init_logger("TRACE", progress_bars)
    elif args.debug:
        init_logger("DEBUG", progress_bars)
    elif args.verbose > 1:
        init_logger("VERBOSE", progress_bars)
    else:
        init_logger("INFO", progress_bars)

    if args.command:
        if getattr(args, "test", None):
            return args.func(args)

        try:
            args.func(args)
        except KeyboardInterrupt:
            # Ignoring KeyboardInterrupts to allow for clean CTRL+C-ing
            pass
        except Exception as error:
            log_error(error)
            if args.debug:
                raise
            sys.exit(1)
    else:
        parser.print_help()


def log_error(error: Exception) -> None:
    logger.error(str(error))
    if isinstance(error, EumdacError) and error.extra_info:  # type:ignore
        extra_info: Dict[str, Any] = error.extra_info  # type: ignore

        extra_msg: str = ""
        if "text" in extra_info:
            extra_msg += f"{extra_info['text']}, "
        if "title" in extra_info:
            extra_msg += f"{extra_info['title']} "
        if "description" in extra_info:
            extra_msg += f"{extra_info['description']} "
        if extra_msg:
            # Add the status code only if there's more info
            if "status" in extra_info:
                extra_msg = f"{extra_info['status']} - {extra_msg}"
            logger.error(extra_msg)

        if "exceptions" in extra_info:
            for problem in extra_info["exceptions"]:
                detail_msg: str = f"{extra_info['status']} - {problem['exceptionText']}"
                if not ("NoApplicableCode" in problem["exceptionCode"]):
                    detail_msg += f" - Type: {problem['exceptionCode']}"
                logger.error(detail_msg)
