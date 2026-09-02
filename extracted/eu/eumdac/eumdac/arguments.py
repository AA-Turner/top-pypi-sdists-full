"""EUMETSAT Data Access Client"""

import argparse
from datetime import datetime
import pathlib
import re
import sys
from typing import Any, Optional, Tuple, Callable, List, Dict, Union, Sequence

import eumdac
from eumdac.logging import logger
from eumdac.token import URLs


def build_eumdac_parser(
    set_credentials: Callable[..., Any],
    token: Callable[..., Any],
    describe: Callable[..., Any],
    search: Callable[..., Any],
    download: Callable[..., Any],
    download_cart: Callable[..., Any],
    tailor_post_job: Callable[..., Any],
    tailor_cancel_jobs: Callable[..., Any],
    tailor_clear_jobs: Callable[..., Any],
    tailor_delete_jobs: Callable[..., Any],
    tailor_download: Callable[..., Any],
    tailor_get_log: Callable[..., Any],
    tailor_list_customisations: Callable[..., Any],
    tailor_quota: Callable[..., Any],
    tailor_resources: Callable[..., Any],
    tailor_show_status: Callable[..., Any],
    local_tailor: Callable[..., Any],
    order: Callable[..., Any],
    subscribe: Callable[..., Any],
    livefeed: Callable[..., Any],
) -> argparse.ArgumentParser:
    key_mgmt_url = URLs().get("token", "key_management")

    class SetCredentialsAction(argparse.Action):
        """eumdac set-credentials entry point"""

        def __call__(
            self,
            parser: argparse.ArgumentParser,
            namespace: argparse.Namespace,
            values: Union[str, Sequence[Any], None],
            option_string: Optional[str] = None,
        ) -> None:
            set_credentials(values)
            parser.exit()

    # main parser
    parser = argparse.ArgumentParser(description=__doc__, fromfile_prefix_chars="@")
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="increase output verbosity (can be provided multiple times)",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {eumdac.__version__}")
    parser.add_argument(
        "--set-credentials",
        nargs=2,
        action=SetCredentialsAction,
        help=argparse.SUPPRESS,
        metavar=("ConsumerKey", "ConsumerSecret"),
        dest="credentials",
    )
    parser.add_argument(
        "-y",
        "--yes",
        help="set any confirmation value to 'yes' automatically",
        action="store_true",
    )
    parser.add_argument(
        "--debug",
        help="show additional debugging info",
        action="store_true",
    )
    parser.add_argument(
        "--trace",
        help="show additional debugging info and detailed traces",
        action="store_true",
    )

    common_parser = argparse.ArgumentParser(add_help=False)
    common_parser.add_argument("--test", action="store_true", help=argparse.SUPPRESS)
    common_parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="increase output verbosity (can be provided multiple times)",
    )
    common_parser.add_argument(
        "-y",
        "--yes",
        help="set any confirmation value to 'yes' automatically",
        action="store_true",
    )
    common_parser.add_argument(
        "--debug",
        help="show additional debugging info",
        action="store_true",
    )
    common_parser.add_argument(
        "--trace",
        help="show additional debugging info and detailed traces",
        action="store_true",
    )
    # Avoid user support messages
    common_parser.add_argument(
        "--quiet",
        help=argparse.SUPPRESS,
        action="store_true",
    )
    common_parser.set_defaults(func=subscribe)

    subparsers = parser.add_subparsers(dest="command")

    # credentials parser
    def credentials(args: argparse.Namespace) -> None:
        set_credentials((args.ConsumerKey, args.ConsumerSecret))

    parser_credentials = subparsers.add_parser(
        "set-credentials",
        description=f"Set authentication parameters for the EUMETSAT APIs, see {key_mgmt_url}",
        help=(f"permanently set consumer key and secret, see {key_mgmt_url}"),
        parents=[common_parser],
    )
    parser_credentials.add_argument("ConsumerKey", help="consumer key")
    parser_credentials.add_argument("ConsumerSecret", help="consumer secret")
    parser_credentials.set_defaults(func=credentials)

    # token parser
    parser_token = subparsers.add_parser(
        "token",
        description="Generate an access token and exit",
        help="generate an access token",
        epilog="example: %(prog)s",
        parents=[common_parser],
    )
    parser_token.add_argument(
        "--val",
        "--validity",
        help="duration of the token, in seconds, default: 86400 seconds (1 day)",
        dest="validity",
        type=int,
    )
    parser_token.add_argument(
        "--force",
        help="revokes current token and forces the generation of a new one. Warning: this will effect other processes using the same credentials",
        action="store_true",
    )
    parser_token.set_defaults(func=token)

    # describe parser
    parser_describe = subparsers.add_parser(
        "describe",
        description="Describe a collection or product, provide no arguments to list all collections",
        help="describe a collection or product",
        epilog="example: %(prog)s -c EO:EUM:DAT:MSG:HRSEVIRI",
        parents=[common_parser],
    )
    parser_describe.add_argument(
        "-f",
        "--filter",
        help='wildcard filter for collection identifier and name, e.g. "*MSG*"',
        dest="filter",
        type=str,
    )
    parser_describe.add_argument(
        "-c",
        "--collection",
        help="id of the collection to describe, e.g. EO:EUM:DAT:MSG:CLM",
        metavar="COLLECTION",
    )
    parser_describe.add_argument(
        "-p",
        "--product",
        help="id of the product to describe, e.g. MSG1-SEVI-MSGCLMK-0100-0100-20040129130000.000000000Z-NA",
        metavar="PRODUCT",
    )
    parser_describe.add_argument(
        "--flat",
        help="avoid tree view when showing product package contents",
        action="store_true",
    )
    parser_describe.set_defaults(func=describe)

    # search parser
    search_argument_parser = argparse.ArgumentParser(add_help=False)
    query_group = search_argument_parser.add_mutually_exclusive_group(required=True)
    query_group.add_argument(
        "-q",
        "--query",
        nargs=1,
        help='opensearch query string, e.g. "pi=EO:EUM:DAT:MSG:HRSEVIRI&dtstart=2023-06-21T12:27:42Z&dtend=2023-06-22T12:27:42Z"',
    )
    query_group.add_argument("-c", "--collection", help="collection id")

    search_argument_parser.add_argument(
        "-s",
        "--start",
        type=parse_isoformat_beginning_of_day_default,
        help='sensing start date/time in UTC, e.g. "2002-12-21T12:30:15"',
        metavar="YYYY-MM-DD[THH[:MM[:SS]]]",
        dest="dtstart",
    )
    search_argument_parser.add_argument(
        "-e",
        "--end",
        type=parse_isoformat_end_of_day_default,
        help='sensing end date/time in UTC, e.g. "2002-12-21T12:30:15"',
        metavar="YYYY-MM-DD[THH[:MM[:SS]]]",
        dest="dtend",
    )
    search_argument_parser.add_argument(
        "--time-range",
        nargs=2,
        type=str,
        help="range of dates in UTC to search by sensing date/time",
        metavar="YYYY-MM-DD[THH[:MM[:SS]]]",
    )
    search_argument_parser.add_argument(
        "--publication-after",
        type=parse_isoformat_beginning_of_day_default,
        help='filter by publication date, products ingested after this UTC date e.g. "2002-12-21T12:30:15"',
        metavar="YYYY-MM-DD[THH[:MM[:SS]]]",
    )
    search_argument_parser.add_argument(
        "--publication-before",
        type=parse_isoformat_beginning_of_day_default,
        help='filter by publication date, products ingested before this UTC date e.g. "2002-12-21T12:30:15"',
        metavar="YYYY-MM-DD[THH[:MM[:SS]]]",
    )
    search_argument_parser.add_argument(
        "--daily-window",
        nargs=2,
        metavar=("HH[:MM[:SS]]", "HH[:MM[:SS]]"),
        dest="daily_window",
        help="filter by daily time window, e.g. 10:00:00 12:30:00",
        default=None,
    )
    search_argument_parser.add_argument(
        "--bbox",
        nargs=4,
        type=float,
        metavar=("W", "S", "E", "N"),
        help="filter by bounding box, defined in EPSG:4326 decimal degrees, e.g. 51.69 0.33 0.51 51.69",
    )
    search_argument_parser.add_argument(
        "--geometry",
        help='filter by geometry, custom geometry in a EPSG:4326 decimal degrees, e.g. "POLYGON ((10.09 56.09, 10.34 56.09, 10.34 56.19, 10.09 56.09))"',
        dest="geo",
    )
    search_argument_parser.add_argument(
        "--cycle",
        help="filter by cycle number, must be a positive integer",
        dest="cycle",
        type=positive_int,
    )
    search_argument_parser.add_argument(
        "--orbit",
        help="filter by orbit number, must be a positive integer",
        dest="orbit",
        type=positive_int,
    )
    search_argument_parser.add_argument(
        "--relorbit",
        help="filter by relative orbit number, must be a positive integer",
        dest="relorbit",
        type=positive_int,
    )
    search_argument_parser.add_argument(
        "--filename",
        help='wildcard filter by product identifier, e.g. "*MSG*"',
        dest="filename",
        type=str,
    )
    search_argument_parser.add_argument(
        "--timeliness",
        help="filter by timeliness",
        dest="timeliness",
        choices=["NT", "NR", "ST"],
    )
    search_argument_parser.add_argument(
        "--product-type",
        "--acronym",
        help="filter by product type/acronym, e.g. MSG15",
        dest="product_type",
        type=str,
    )
    search_argument_parser.add_argument(
        "--satellite", help="filter by satellite, e.g. MSG4", dest="sat"
    )
    search_argument_parser.add_argument(
        "--sort",
        choices=("ingestion", "sensing"),
        help="sort results by ingestion time or sensing time, default: sensing",
    )
    sorting_direction = search_argument_parser.add_mutually_exclusive_group(required=False)
    sorting_direction.add_argument("--asc", action="store_true", help="sort ascending")
    sorting_direction.add_argument("--desc", action="store_true", help="sort descending")
    search_argument_parser.add_argument(
        "--limit", type=positive_int, help="max number of products to return"
    )
    parser_search = subparsers.add_parser(
        "search",
        description="Search for products",
        help="search for products",
        epilog="example: %(prog)s -c EO:EUM:DAT:MSG:CLM -s 2010-03-01 -e 2010-03-15T12:15",
        parents=[common_parser, search_argument_parser],
    )
    StandardArgs.add_defaulthelp_argument(parser_search)

    parser_search.set_defaults(func=search)

    parser_download = subparsers.add_parser(
        "download",
        description="Download products, with optional customisation",
        help="download products, with optional customisation",
        parents=[
            common_parser,
            search_argument_parser,
        ],  # this inherits collection lists
    )
    parser_download.add_argument(
        "-p", "--product", nargs="*", help="id of the product(s) to download"
    )
    parser_download.add_argument(
        "-o",
        "--output-dir",
        type=pathlib.Path,
        help="path to output directory, default: current directory",
        metavar="DIR",
        default=pathlib.Path.cwd(),
    )
    parser_download.add_argument(
        "-i",
        "--integrity",
        action="store_true",
        help="verify integrity of downloaded files through their md5, if available",
    )
    parser_download.add_argument(
        "--chunk-size",
        help=argparse.SUPPRESS,
    )
    parser_download.add_argument(
        "--entry",
        nargs="+",
        help="shell-style wildcard pattern(s) to filter product files",
    )
    parser_download.add_argument(
        "--download-coverage",
        choices=["FD", "H1", "H2", "T1", "T2", "T3", "Q1", "Q2", "Q3", "Q4"],
        help="download only the area matching the provided coverage (only for specific missions)",
    )
    parser_download.add_argument(
        "--chain",
        "--tailor",
        help="chain id, file, or YAML string for customising the data",
        metavar="CHAIN",
    )
    parser_download.add_argument(
        "--local-tailor",
        help="id of the instance to use for customisating the data",
        metavar="ID",
    )
    dir_group = parser_download.add_mutually_exclusive_group()
    dir_group.add_argument(
        "--onedir",
        action="store_true",
        help="avoid creating a subdirectory for each product",
    )
    dir_group.add_argument(
        "--dirs",
        help="download each product into its own individual directory",
        action="store_true",
    )
    parser_download.add_argument(
        "-k",
        "--keep-order",
        action="store_true",
        help="keep order file after finishing successfully",
    )
    parser_download.add_argument(
        "--no-warning-logs", help="don't show logs when jobs fail", action="store_true"
    )
    parser_download.add_argument(
        "-t",
        "--threads",
        type=int,
        help="set the number of parallel connections",
        default=3,
        dest="download_threads",
    )
    parser_download.add_argument(
        "--no-progress-bars", help="don't show the download status bar", action="store_true"
    )
    StandardArgs.add_defaulthelp_argument(parser_download)

    parser_download.set_defaults(func=download)

    parser_download_cart = subparsers.add_parser(
        "download-metalink",
        description="Download Data Store cart metalink files",
        help="download Data Store cart metalink files",
        parents=[
            common_parser,
        ],
    )
    parser_download_cart.add_argument(
        "file", help="Data Store cart metalink file to download, i.e. cart-user.xml"
    )
    parser_download_cart.add_argument(
        "-o",
        "--output-dir",
        type=pathlib.Path,
        help="path to output directory, default: current directory",
        metavar="DIR",
        default=pathlib.Path.cwd(),
    )
    parser_download_cart.add_argument(
        "-i",
        "--integrity",
        action="store_true",
        help="verify integrity of downloaded files through their md5, if available",
    )
    parser_download_cart.add_argument(
        "--dirs",
        help="download each product into its own individual directory",
        action="store_true",
    )
    parser_download_cart.add_argument(
        "-k",
        "--keep-order",
        action="store_true",
        help="keep order file after finishing successfully",
    )
    parser_download_cart.add_argument(
        "--no-progress-bars",
        help="don't show download progress bars",
        action="store_true",
    )
    parser_download_cart.set_defaults(func=download_cart)

    # Subscription parser
    subs_search_parser = build_search_parser(for_subscription=True)
    subs_download_parser = build_download_parser(for_subscription=True)

    parser_subscription = subparsers.add_parser(
        "subscribe",
        aliases=["subs"],
        description="Manage subscriptions to data published in collections.",
        help="manage subscriptions",
        epilog="example: %(prog)s -c EO:EUM:DAT:MSG:CLM",
    )
    StandardArgs.add_defaulthelp_argument(parser_subscription)
    subscription_subparsers = parser_subscription.add_subparsers(dest="subscription_command")

    subscription_parser_set_credentials = subscription_subparsers.add_parser(
        "set-credentials",
        description="Set authentication parameters for the subscription API.",
        help=("set subscription authentication parameters."),
        parents=[common_parser],
    )
    subscription_parser_set_credentials.add_argument(
        "username", help='username, use "" for no value'
    )
    subscription_parser_set_credentials.add_argument(
        "password", help='password, use "" for no value'
    )
    subscription_parser_set_credentials.set_defaults(func=subscribe)

    subscription_parser_list = subscription_subparsers.add_parser(
        "list",
        description="List active subscriptions and downloaders.",
        help="list active subscriptions and downloaders",
        parents=[common_parser],
    )
    subscription_parser_list.set_defaults(func=subscribe)

    subscription_parser_add = subscription_subparsers.add_parser(
        "add",
        description="Subscribe to a collection with the given search parameters and a unique tag.",
        help="add a new subscription with the given tag",
        parents=[common_parser, subs_search_parser],
        epilog="example: %(prog)s -c EO:EUM:DAT:0409 --sat Sentinel-3A --tag OLCI_L1B_S3A",
    )
    subscription_parser_add.add_argument(
        "--mqtttest",
        help=argparse.SUPPRESS,
        action="store_true",
    )
    subscription_parser_add.add_argument(
        "--print-notifications",
        help="print received notifications",
        action="store_true",
    )
    subscription_parser_add.add_argument(
        "--notifications-only",
        "-n",
        help="print received notifications and do not create orders for downloading",
        action="store_true",
    )
    subscription_parser_add.add_argument(
        "--tag",
        type=subscription_tag,
        required=True,
        help="label to assign to the subscription",
    )
    subscription_parser_add.set_defaults(func=subscribe)

    subscription_parser_download = subscription_subparsers.add_parser(
        "download",
        description="Download products based on notifications received on a subscription.",
        help="start a new downloader for a given subscription",
        parents=[common_parser, subs_download_parser],
        epilog="example: %(prog)s --tag OLCI_L1B_S3A --integrity -o OLCI_L1B_S3A_products",
    )
    subscription_parser_download.add_argument(
        "--only-incoming",
        help="only download files from new incoming orders; skip orders already existing for the given tag",
        action="store_true",
    )
    subscription_parser_download.add_argument(
        "--tag",
        help="tag identifying the subscription to download from",
        required=True,
        type=subscription_tag,
        default=["default"],
    )
    subscription_parser_download.add_argument(
        "--delay",
        help="wait time before downloading after a notification, in minutes",
        type=positive_int,
    )
    subscription_parser_download.set_defaults(func=subscribe)

    # Livefeed parser
    parser_livefeed = subparsers.add_parser(
        "livefeed",
        description="Download products from a collection as soon as they are published",
        help="download livefeed",
        parents=[common_parser, subs_search_parser, subs_download_parser],
        epilog='example: %(prog)s -c EO:EUM:DAT:MSG:MSG15-RSS --entry "*.nat" --onedir',
    )
    parser_livefeed.add_argument(
        "--print-notifications",
        help="print received notifications",
        action="store_true",
    )
    parser_livefeed.add_argument(
        "--delay",
        help="wait time before downloading after a notification, in minutes",
        type=positive_int,
    )
    parser_livefeed.set_defaults(func=livefeed)

    # tailor parser
    # tailor parser common arguments
    tailor_common_parser = argparse.ArgumentParser(add_help=False)
    tailor_common_parser.add_argument(
        "--local-tailor",
        help="id of a local instance to use instead of the Data Tailor Web Service",
        metavar="ID",
    )
    tailor_common_parser.add_argument(
        "--raw", help="show output without formatting", action="store_true"
    )

    parser_tailor = subparsers.add_parser(
        "tailor",
        description="Manage Data Tailor customisations",
        help="manage Data Tailor resources",
        parents=[common_parser],
    )
    StandardArgs.add_defaulthelp_argument(parser_tailor)

    tailor_subparsers = parser_tailor.add_subparsers(dest="tailor-command")

    tailor_post_parser = tailor_subparsers.add_parser(
        "post",
        description="Post individual customisation jobs",
        help="post a new customisation job",
        parents=[common_parser, tailor_common_parser],
    )
    tailor_post_parser.add_argument("-c", "--collection", help="collection id")
    tailor_post_parser.add_argument(
        "-p", "--product", nargs="+", help="id of the product(s) to customise"
    )
    tailor_post_parser.add_argument(
        "--chain",
        "--tailor",
        help="chain id, file, or YAML string for customising the data",
        metavar="CHAIN",
    )
    tailor_post_parser.set_defaults(func=tailor_post_job)

    tailor_list_parser = tailor_subparsers.add_parser(
        "list",
        description="List customisation jobs",
        help="list customisation jobs",
        parents=[common_parser, tailor_common_parser],
    )
    tailor_list_parser.set_defaults(func=tailor_list_customisations)

    tailor_status_parser = tailor_subparsers.add_parser(
        "status",
        description="Check the status of one (or more) customisations",
        help="check the status of customisations",
        parents=[common_parser, tailor_common_parser],
    )
    tailor_status_parser.add_argument("job_ids", metavar="Customisation ID", type=str, nargs="+")
    tailor_status_parser.set_defaults(func=tailor_show_status)

    tailor_log_parser = tailor_subparsers.add_parser(
        "log",
        description="Get the log of a customisation",
        help="get the log of a customisation",
        parents=[common_parser, tailor_common_parser],
    )
    tailor_log_parser.add_argument(
        "job_id", metavar="Customisation ID", type=str, help="Customisation ID"
    )
    tailor_log_parser.set_defaults(func=tailor_get_log)

    tailor_quota_parser = tailor_subparsers.add_parser(
        "quota",
        description="Show user workspace usage quota. Verbose mode (-v) shows more details",
        help="show user workspace usage quota",
        parents=[common_parser, tailor_common_parser],
    )
    tailor_quota_parser.set_defaults(func=tailor_quota)

    tailor_resources_parser = tailor_subparsers.add_parser(
        "resources",
        aliases=["res"],
        description="Manage customisation resources, i.e chains, filters, rois and quicklooks",
        help="manage customisation resources",
        parents=[common_parser],
    )

    resources_subparsers = tailor_resources_parser.add_subparsers(
        dest="resources_command", required=True, metavar="{chains, filters, rois, quicklooks}"
    )

    tailor_resources_chains_parser = resources_subparsers.add_parser(
        "chains",
        description="Show and manage customisation chains. Use verbosity (-v) for more details.",
        help="show and manage chains",
        parents=[common_parser, tailor_common_parser],
    )
    tailor_resources_chains_exlusive_g = (
        tailor_resources_chains_parser.add_mutually_exclusive_group()
    )

    tailor_resources_chains_exlusive_g.add_argument(
        "--id", help="show details of specific chain", metavar="Chain ID"
    )
    tailor_resources_chains_exlusive_g.add_argument(
        "--save", help="save a new chain", metavar="<Chain>"
    )
    tailor_resources_chains_exlusive_g.add_argument(
        "--update", help="update an existing chain", metavar="<Chain>"
    )
    tailor_resources_chains_exlusive_g.add_argument(
        "--delete", help="delete a chain by ID", metavar="Chain ID"
    )
    tailor_resources_chains_exlusive_g.set_defaults(func=tailor_resources)

    tailor_resources_filters_parser = resources_subparsers.add_parser(
        "filters",
        description="Show and manage customisation filters. User verbosity (-v) for more details.",
        help="show and manage filters",
        parents=[common_parser, tailor_common_parser],
    )
    tailor_resources_filters_exlusive_g = (
        tailor_resources_filters_parser.add_mutually_exclusive_group()
    )

    tailor_resources_filters_exlusive_g.add_argument(
        "--id", help="show details of specific filter", metavar="Filter ID"
    )
    tailor_resources_filters_exlusive_g.add_argument(
        "--save", help="save a new filter", metavar="<Filter>"
    )
    tailor_resources_filters_exlusive_g.add_argument(
        "--update", help="update an existing filter", metavar="<Filter>"
    )
    tailor_resources_filters_exlusive_g.add_argument(
        "--delete", help="delete a filter by ID", metavar="Filter ID"
    )
    tailor_resources_filters_exlusive_g.set_defaults(func=tailor_resources)

    tailor_resources_rois_parser = resources_subparsers.add_parser(
        "rois",
        description="Show and manage customisation ROIs. User verbosity (-v) for more details.",
        help="show and manage ROIs",
        parents=[common_parser, tailor_common_parser],
    )
    tailor_resources_rois_exlusive_g = tailor_resources_rois_parser.add_mutually_exclusive_group()

    tailor_resources_rois_exlusive_g.add_argument(
        "--id", help="show details of specific ROI", metavar="ROI ID"
    )
    tailor_resources_rois_exlusive_g.add_argument("--save", help="save a new ROI", metavar="<ROI>")
    tailor_resources_rois_exlusive_g.add_argument(
        "--update", help="update an existing ROI", metavar="<ROI>"
    )
    tailor_resources_rois_exlusive_g.add_argument(
        "--delete", help="delete a ROI by ID", metavar="ROI ID"
    )
    tailor_resources_rois_exlusive_g.set_defaults(func=tailor_resources)

    tailor_resources_quicklooks_parser = resources_subparsers.add_parser(
        "quicklooks",
        description="Show and manage customisation quicklooks. User verbosity (-v) for more details.",
        help="show and manage quicklooks",
        parents=[common_parser, tailor_common_parser],
    )
    tailor_resources_quicklooks_exlusive_g = (
        tailor_resources_quicklooks_parser.add_mutually_exclusive_group()
    )

    tailor_resources_quicklooks_exlusive_g.add_argument(
        "--id", help="show details of specific quicklook", metavar="Quicklook ID"
    )
    tailor_resources_quicklooks_exlusive_g.add_argument(
        "--save", help="save a new quicklook", metavar="<Quicklook>"
    )
    tailor_resources_quicklooks_exlusive_g.add_argument(
        "--update", help="update an existing quicklook", metavar="<Quicklook>"
    )
    tailor_resources_quicklooks_exlusive_g.add_argument(
        "--delete", help="delete a quicklook by ID", metavar="Quicklook ID"
    )
    tailor_resources_quicklooks_exlusive_g.set_defaults(func=tailor_resources)

    tailor_delete_parser = tailor_subparsers.add_parser(
        "delete",
        description="Delete finished customisations",
        help="delete customisations",
        parents=[common_parser, tailor_common_parser],
    )
    tailor_delete_parser.add_argument("job_ids", metavar="Customisation ID", type=str, nargs="+")
    tailor_delete_parser.set_defaults(func=tailor_delete_jobs)

    tailor_cancel_parser = tailor_subparsers.add_parser(
        "cancel",
        description="Cancel QUEUED, RUNNING or INACTIVE customisations",
        help="cancel running customisations",
        parents=[common_parser, tailor_common_parser],
    )
    tailor_cancel_parser.add_argument("job_ids", metavar="Customisation ID", type=str, nargs="+")
    tailor_cancel_parser.set_defaults(func=tailor_cancel_jobs)

    tailor_clean_parser = tailor_subparsers.add_parser(
        "clean",
        description="Clean up customisations in any state (cancelling them if needed)",
        help="clean up customisations in any state",
        parents=[common_parser, tailor_common_parser],
    )
    tailor_clean_parser.add_argument("job_ids", metavar="Customisation ID", type=str, nargs="*")
    tailor_clean_parser.add_argument("--all", help="Clean all customisations", action="store_true")
    tailor_clean_parser.set_defaults(func=tailor_clear_jobs)

    tailor_download_parser = tailor_subparsers.add_parser(
        "download",
        description="Download the output of finished customisations",
        help="download the output of finished customisations",
        parents=[common_parser, tailor_common_parser],
    )
    tailor_download_parser.add_argument(
        "job_id", metavar="Customisation ID", type=str, help="Customisation ID"
    )
    tailor_download_parser.add_argument(
        "-o",
        "--output-dir",
        type=pathlib.Path,
        help="path to output directory, default: current directory",
        metavar="DIR",
        default=pathlib.Path.cwd(),
    )
    tailor_download_parser.set_defaults(func=tailor_download)

    # Local Data Tailor instances parser
    parser_local_tailor = subparsers.add_parser(
        "local-tailor",
        description="Manage local Data Tailor instances",
        help="manage local Data Tailor instances",
        parents=[common_parser],
    )
    StandardArgs.add_defaulthelp_argument(parser_local_tailor)

    local_tailor_subparsers = parser_local_tailor.add_subparsers(dest="local_tailor_command")

    local_tailor_list_parser = local_tailor_subparsers.add_parser(
        "instances",
        help="list configured instances",
        description="List configured local Data Tailor instances",
        parents=[common_parser],
    )
    local_tailor_list_parser.set_defaults(func=local_tailor)

    local_tailor_show_parser = local_tailor_subparsers.add_parser(
        "show",
        help="show details of an instance",
        description="Show details of local Data Tailor instances",
        parents=[common_parser],
    )
    local_tailor_show_parser.add_argument(
        "localtailor_id",
        help="id of the local instance, e.g. my-local-tailor",
        metavar="ID",
        nargs=1,
    )
    local_tailor_show_parser.set_defaults(func=local_tailor)

    local_tailor_set_parser = local_tailor_subparsers.add_parser(
        "set",
        help="configure a local instance",
        description="Configure a local Data Tailor instance",
        parents=[common_parser],
    )
    local_tailor_set_parser.add_argument(
        "localtailor_id",
        help="id for the local instance, e.g. my-local-tailor",
        metavar="ID",
        nargs=1,
    )
    local_tailor_set_parser.add_argument(
        "localtailor_url",
        help="base URL of the local instance, e.g. http://localhost:40000/",
        metavar="URL",
        nargs=1,
    )
    local_tailor_set_parser.set_defaults(func=local_tailor)

    local_tailor_remove_parser = local_tailor_subparsers.add_parser(
        "remove",
        help="remove a configured instance",
        description="Remove a configured local instance",
        parents=[common_parser],
    )
    local_tailor_remove_parser.add_argument(
        "localtailor_id",
        help="id of the local instance, e.g. my-local-tailor",
        metavar="ID",
        nargs=1,
    )
    local_tailor_remove_parser.set_defaults(func=local_tailor)

    #  Order parser
    parser_order = subparsers.add_parser(
        "order",
        description="Manage eumdac orders",
        help="manage orders",
        parents=[common_parser],
    )
    StandardArgs.add_defaulthelp_argument(parser_order)

    order_subparsers = parser_order.add_subparsers(dest="order_command")
    order_parsers = {}
    order_parsers["list"] = order_subparsers.add_parser(
        "list",
        description="List eumdac orders",
        help="list orders",
        parents=[common_parser],
    )
    order_parsers["list"].add_argument(
        "-f", "--failed", help="show only failed orders", action="store_true"
    )
    order_parsers["list"].add_argument(
        "-a", "--archived", help="show only archived orders", action="store_true"
    )
    order_parsers["list"].add_argument(
        "-r", "--reverse", help="show older orders first", action="store_true"
    )
    order_parsers["list"].set_defaults(func=order)
    housekeep_parser = order_subparsers.add_parser(
        "housekeep",
        description="Perform housekeeping of the order directories",
        help="cleanup past orders",
    )
    housekeep_parser.set_defaults(func=order)
    for action in ["status", "resume", "restart", "delete"]:
        subparser = order_subparsers.add_parser(
            action,
            description=f"{action.capitalize()} eumdac orders",
            help=f"{action} orders",
            parents=[common_parser],
        )
        if action in ["resume", "restart"]:
            subparser.add_argument(
                "--chunk-size",
                help=argparse.SUPPRESS,
            )
            subparser.add_argument(
                "-t",
                "--threads",
                type=int,
                help="set the number of parallel connections",
                default=3,
                dest="download_threads",
            )
            subparser.add_argument(
                "-i",
                "--integrity",
                action="store_true",
                help="verify integrity of downloaded files through their md5, if available",
            )
            subparser.add_argument(
                "--local-tailor",
                help="id of the instance to use for customisating the data",
                metavar="ID",
            )
            subparser.add_argument(
                "-k",
                "--keep-order",
                action="store_true",
                help="keep order file after finishing successfully",
            )
        subparser.add_argument(
            "order_id", help="order id", metavar="ID", nargs="?", default="latest"
        )
        subparser.add_argument(
            "-f", "--failed", help="work with failed orders", action="store_true"
        )
        subparser.add_argument(
            "-a", "--archived", help="work with archived orders", action="store_true"
        )
        if action == "delete":
            subparser.add_argument("--all", help="delete all orders", action="store_true")
        subparser.set_defaults(func=order)
        order_parsers[action] = subparser

    return parser


def build_search_parser(for_subscription: bool = False) -> argparse.ArgumentParser:
    search_parser = argparse.ArgumentParser(add_help=False)
    # search_parser.add_argument(
    #     "-c", "--collection", nargs="+", help="collection id", required=True
    # )
    query_group = search_parser.add_mutually_exclusive_group(required=True)
    query_group.add_argument(
        "-q",
        "--query",
        nargs=1,
        help="opensearch query string, e.g. pi=EO:EUM:DAT:MSG:HRSEVIRI&dtstart=2023-06-21T12:27:42Z&dtend=2023-06-22T12:27:42Z",
    )
    query_group.add_argument("-c", "--collection", nargs="+", help="collection id")
    search_parser.add_argument(
        "-s",
        "--start",
        type=parse_isoformat_beginning_of_day_default,
        help="sensing start date/time in UTC, e.g. 2002-12-21T12:30:15",
        metavar="YYYY-MM-DD[THH[:MM[:SS]]]",
        dest="dtstart",
    )
    search_parser.add_argument(
        "-e",
        "--end",
        type=parse_isoformat_end_of_day_default,
        help="sensing end date/time in UTC, e.g. 2002-12-21T12:30:15",
        metavar="YYYY-MM-DD[THH[:MM[:SS]]]",
        dest="dtend",
    )
    search_parser.add_argument(
        "--time-range",
        nargs=2,
        type=str,
        help="range of dates in UTC to search by sensing date/time",
        metavar="YYYY-MM-DD[THH[:MM[:SS]]]",
    )
    search_parser.add_argument(
        "--publication-after",
        type=parse_isoformat_beginning_of_day_default,
        help="filter by publication date, products ingested after this UTC date e.g. 2002-12-21T12:30:15",
        metavar="YYYY-MM-DD[THH[:MM[:SS]]]",
    )
    search_parser.add_argument(
        "--publication-before",
        type=parse_isoformat_beginning_of_day_default,
        help="filter by publication date, products ingested before this UTC date e.g. 2002-12-21T12:30:15",
        metavar="YYYY-MM-DD[THH[:MM[:SS]]]",
    )
    search_parser.add_argument(
        "--daily-window",
        nargs=2,
        metavar=("HH[:MM[:SS]]", "HH[:MM[:SS]]"),
        dest="daily_window",
        help="filter by daily time window, e.g. 10:00:00 12:30:00",
        default=None,
    )
    add_product_filter_arguments(search_parser)
    if not for_subscription:
        search_parser.add_argument(
            "--sort",
            choices=("ingestion", "sensing"),
            help="sort results by ingestion time or sensing time, default: sensing",
        )
        sorting_direction = search_parser.add_mutually_exclusive_group(required=False)
        sorting_direction.add_argument("--asc", action="store_true", help="sort ascending")
        sorting_direction.add_argument("--desc", action="store_true", help="sort descending")
        search_parser.add_argument(
            "--limit", type=positive_int, help="max number of products to return"
        )

    return search_parser


def add_product_filter_arguments(parser: argparse.ArgumentParser) -> None:
    StandardArgs.add_sat_argument(parser)
    parser.add_argument(
        "--bbox",
        nargs=4,
        type=float,
        metavar=("W", "S", "E", "N"),
        help="filter by bounding box, defined in EPSG:4326 decimal degrees, e.g. 51.28 51.69 0.51 0.33",
    )
    parser.add_argument(
        "--geometry",
        help="filter by geometry, custom geometry in a EPSG:4326 decimal degrees, e.g. POLYGON ((10.09 56.09, 10.34 56.09, 10.34 56.19, 10.09 56.09))",
        dest="geo",
    )
    parser.add_argument(
        "--cycle",
        help="filter by cycle number, must be a positive integer",
        dest="cycle",
        type=positive_int,
    )
    parser.add_argument(
        "--orbit",
        help="filter by orbit number, must be a positive integer",
        dest="orbit",
        type=positive_int,
    )
    parser.add_argument(
        "--relorbit",
        help="filter by relative orbit number, must be a positive integer",
        dest="relorbit",
        type=positive_int,
    )
    parser.add_argument(
        "--filename",
        help="wildcard filter by product identifier, e.g. *MSG*",
        dest="filename",
        type=str,
    )
    parser.add_argument(
        "--timeliness",
        help="filter by timeliness",
        dest="timeliness",
        choices=["NT", "NR", "ST"],
    )
    parser.add_argument(
        "--product-type",
        "--acronym",
        help="filter by product type/acronym, e.g. MSG15",
        dest="product_type",
        type=str,
    )


def build_download_parser(for_subscription: bool = False) -> argparse.ArgumentParser:
    parser_download = argparse.ArgumentParser(add_help=False)
    if not for_subscription:
        parser_download.add_argument(
            "-p", "--product", nargs="*", help="id of the product(s) to download"
        )
    StandardArgs.add_output_dir_argument(parser_download)
    if not for_subscription:
        parser_download.add_argument(
            "-i",
            "--integrity",
            action="store_true",
            help="verify integrity of downloaded files through their md5, if available",
        )
    parser_download.add_argument(
        "--chunk-size",
        help=argparse.SUPPRESS,
    )
    parser_download.add_argument(
        "--entry",
        nargs="+",
        help="shell-style wildcard pattern(s) to filter product files",
    )
    parser_download.add_argument(
        "--download-coverage",
        choices=["FD", "H1", "H2", "T1", "T2", "T3", "Q1", "Q2", "Q3", "Q4"],
        help="download only the area matching the provided coverage (only for specific missions)",
    )
    parser_download.add_argument(
        "--chain",
        "--tailor",
        help="chain id, file, or YAML string for customising the data",
        metavar="CHAIN",
    )
    parser_download.add_argument(
        "--local-tailor",
        help="id of the instance to use for customisating the data",
        metavar="ID",
    )
    dir_group = parser_download.add_mutually_exclusive_group()
    dir_group.add_argument(
        "--onedir",
        action="store_true",
        help="avoid creating a subdirectory for each product",
    )
    dir_group.add_argument(
        "--dirs",
        help="download each product into its own individual directory",
        action="store_true",
    )
    if not for_subscription:
        parser_download.add_argument(
            "-k",
            "--keep-order",
            action="store_true",
            help="keep order file after finishing successfully",
        )
        parser_download.add_argument(
            "--no-warning-logs",
            help="don't show logs when jobs fail",
            action="store_true",
        )
    parser_download.add_argument(
        "-t",
        "--threads",
        type=positive_int,
        help="set the number of parallel connections",
        default=3,
        dest="download_threads",
    )
    parser_download.add_argument(
        "--no-progress-bars",
        help="don't show download progress bars",
        action="store_true",
    )
    return parser_download


class StandardArgs:
    @staticmethod
    def add_defaulthelp_argument(parser: argparse.ArgumentParser) -> None:
        def show_help(_: Any) -> None:
            parser.print_help()
            parser.exit()

        parser.set_defaults(func=show_help)

    @staticmethod
    def add_debug_argument(parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "--debug",
            help="show additional debugging info and traces for errors",
            action="store_true",
        )

    @staticmethod
    def add_yes_argument(parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "-y",
            "--yes",
            help="set any confirmation value to 'yes' automatically",
            action="store_true",
        )

    @staticmethod
    def add_verbose_argument(parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "-v",
            "--verbose",
            action="count",
            default=0,
            help="increase output verbosity (can be provided multiple times)",
        )

    @staticmethod
    def add_collection_argument(parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "-c",
            "--collection",
            help="id of the collection to describe, e.g. EO:EUM:DAT:MSG:CLM",
            metavar="COLLECTION",
        )

    @staticmethod
    def add_sat_argument(parser: argparse.ArgumentParser) -> None:
        parser.add_argument("--satellite", help="filter by satellite, e.g. MSG4", dest="sat")

    @staticmethod
    def add_output_dir_argument(parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "-o",
            "--output-dir",
            type=pathlib.Path,
            help="path to output directory, default: current directory",
            metavar="DIR",
            default=pathlib.Path.cwd(),
        )


def parse_isoformat(input_string: str, time_default: str = "start") -> datetime:
    """helper function to provide a user readable message when argparse encounters
    a wrongly formatted date"""
    time_defaults = {
        "start": "00:00:00",
        "end": "23:59:59",
    }
    try:
        _default_time = time_defaults[time_default]
    except KeyError as exc:
        raise ValueError(f"Unexpected time_default: '{time_default}'") from exc

    if "T" not in input_string:
        input_string += f"T{_default_time}"
        if time_default == "end":
            logger.warning(f"As no time was given for end date, it was set to {input_string}.")

    try:
        return datetime.fromisoformat(input_string)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            "The format of the provided date was not recognized."
            "Expecting YYYY-MM-DD[THH[:MM[:SS]]]"
        ) from exc


def parse_isoformat_beginning_of_day_default(input_string: str) -> datetime:
    """helper function to provide to parse start dates"""
    return parse_isoformat(input_string, time_default="start")


def parse_isoformat_end_of_day_default(input_string: str) -> datetime:
    """helper function to provide to parse end dates"""
    return parse_isoformat(input_string, time_default="end")


# support type for argparse positive int
def positive_int(value: str) -> int:
    if int(value) <= 0:
        raise argparse.ArgumentTypeError(f"{value} is an invalid positive integer")
    return int(value)


# support type for argparse filename safe tags
def subscription_tag(value: str) -> str:
    invalid_chars = re.findall('[/\\\\?%*:|"<>\x7F\x00-\x1F]', value)
    if invalid_chars:
        raise argparse.ArgumentTypeError(
            f"\"{value}\" is an invalid tag: the following characters are not allowed {', '.join(invalid_chars)}"
        )
    return value
