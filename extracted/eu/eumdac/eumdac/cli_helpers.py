import argparse
import json
import re
import signal
import sys
from datetime import datetime
from typing import Any, Iterable, List, Optional, Tuple

import yaml

from eumdac.collection import SearchResults
from eumdac.config import get_credentials_path
from eumdac.datastore import DataStore
from eumdac.datatailor import DataTailor
from eumdac.errors import EumdacError
from eumdac.fake import FakeDataStore, FakeDataTailor  # type: ignore
from eumdac.futures import FutureAbortedError
from eumdac.local_tailor import get_local_tailor
from eumdac.logging import logger
from eumdac.product import ProductError
from eumdac.signals import signal_registry
from eumdac.tailor_models import Chain, Filter, Quicklook, RegionOfInterest
from eumdac.token import AccessToken, AnonymousAccessToken


def validate_daily_window_args(
    daily_window_arg: List[str],
) -> Tuple[datetime, datetime]:
    daily_window_start: datetime = parse_time_str(daily_window_arg[0])
    daily_window_end: datetime = parse_time_str(daily_window_arg[1])
    if daily_window_start > daily_window_end:
        raise ValueError(
            f"The daily window start time must be earlier than the end time. Please review the provided window: {datetime.strftime(daily_window_start, '%H:%M:%S')} - {datetime.strftime(daily_window_end, '%H:%M:%S')}"
        )
    return (daily_window_start, daily_window_end)


def check_daily_window(
    sensing_start: datetime,
    sensing_end: datetime,
    daily_window_start: datetime,
    daily_window_end: datetime,
) -> bool:
    return (
        sensing_end.time() >= daily_window_start.time()
        and sensing_start.time() <= daily_window_end.time()
    )


def parse_time_str(input_string: str) -> datetime:
    """helper function to parse time with optional minutes and seconds: HH[:MM[:SS]]"""
    if len(input_string) == 2:
        input_string += ":00:00"
    elif len(input_string) == 5:
        input_string += ":00"
    return datetime.strptime(input_string, "%H:%M:%S")


def get_datastore(args: argparse.Namespace, anonymous_allowed: bool = False) -> Any:
    """get an instance of DataStore"""
    if getattr(args, "test", None):
        return FakeDataStore()
    try:
        creds = load_credentials()
    except CredentialsFileNotFoundError as exc:
        if anonymous_allowed:
            creds = None
        else:
            raise EumdacError("No credentials found! Please set credentials!") from exc

    if creds is None:
        token: Any = AnonymousAccessToken()
    else:
        token = AccessToken(creds)
    return DataStore(token)


def get_datatailor(args: argparse.Namespace, token: Optional[AccessToken] = None) -> Any:
    """get an instance of DataTailor"""
    if args.test:
        logger.info("Using Fake DataTailor instance")
        return FakeDataTailor()
    if args.local_tailor:
        logger.info(f"Using Data Tailor Standalone instance: {args.local_tailor}")
        return get_local_tailor(args.local_tailor)
    if not token:
        try:
            creds = load_credentials()
        except CredentialsFileNotFoundError as exc:
            raise EumdacError("No credentials found! Please set credentials!") from exc
        token = AccessToken(creds)
    logger.info("Using Data Tailor Web Service")
    return DataTailor(token)


def safe_run(
    app: Any,
    collection: Optional[str] = None,
    num_products: int = -1,
    keep_order: bool = False,
    avoid_order_management: bool = False,
) -> bool:
    """wrapper around app.run() for exception handling and logging"""
    if num_products < 0:
        num_products = len(list(app.order.iter_product_info()))
        plural = "" if num_products == 1 else "s"
        logger.info(f"Processing {num_products} product{plural}.")
    (chain,) = app.order.get_dict_entries("chain")
    if chain:
        plural = "" if num_products == 1 else "s"
        logger.info(f"Product{plural} will be customized with the following parameters:")
        for line in yaml.dump(chain).splitlines():
            logger.info(f"   {line}")

    logger.info(f"Using order: {app.order}")
    failed_order = True

    def shutdown() -> None:
        logger.info("\nReceived request to shut down.")
        logger.info("Finishing threads... (this may take a while)")
        app.shutdown()
        if not avoid_order_management:
            logger.info("Resume this order with the following command:")
            logger.info(f"$ eumdac order resume {app.order}")
        nonlocal failed_order
        failed_order = False

    signal_registry.register(signal.SIGINT, shutdown)

    try:
        success = app.run()
        failed_order = not success
        if not keep_order and success:
            logger.info(f"Removing successfully finished order {app.order}")
            app.order.delete()
        return success
    except ProductError:
        if collection:
            app.datastore.check_collection_id(collection)
        raise
    except FutureAbortedError:
        logger.debug("Program aborted by user")
        return False
    except Exception as e:
        import logging

        if logger.isEnabledFor(logging.DEBUG):
            import traceback

            traceback.print_exc()
        logger.critical(f"Unexpected exception ({type(e)}): {str(e)}")
        raise
    finally:
        signal_registry.unregister(signal.SIGINT, shutdown)
        # Failed orders get moved to the failed orders directory
        if failed_order and not avoid_order_management:
            app.order.move_to_failed()
            logger.warning(
                "The order file for the failed order has been moved to the failed orders directory."
            )
            logger.warning("Run the following command to try again:")
            logger.warning(f"\t$ eumdac order restart --failed {app.order}")


def load_credentials() -> Iterable[str]:
    """load the credentials and do error handling"""
    credentials_path = get_credentials_path()
    try:
        content = credentials_path.read_text()
    except FileNotFoundError as exc:
        raise CredentialsFileNotFoundError(str(credentials_path)) from exc
    match = re.match(r"(\w+),(\w+)$", content)
    if match is None:
        raise EumdacError(f'Corrupted file "{credentials_path}"! Please reset credentials!')
    return match.groups()


class CredentialsFileNotFoundError(EumdacError):
    """Error that will be raised when no credentials file is found"""


def _search(args: argparse.Namespace) -> Tuple[SearchResults, int]:
    """given search query arguments will return the list of matching products"""
    datastore = get_datastore(args, anonymous_allowed=True)
    products: SearchResults
    num_products: int

    if args.query:
        extra_search_params = _get_args_search_params(args)
        if extra_search_params:
            logger.warning(
                f"The following search parameters have been ignored in favour of the opensearch query: {', '.join(extra_search_params)}"
            )
        paging_params = _get_query_paging_params(args.query[0])
        if paging_params:
            logger.warning(
                f"The following opensearch terms have been ignored: {', '.join(paging_params)}"
            )
        search_results = datastore.opensearch(args.query[0])
        products = search_results
        # Check the number of products
        num_products = len(products)
    else:
        # See https://docs.opengeospatial.org/is/13-026r9/13-026r9.html#20 for the mathematical notation expected by the publication filter
        if args.publication_after and args.publication_before:
            publication = f"[{args.publication_after.isoformat(timespec='milliseconds')}Z,{args.publication_before.isoformat(timespec='milliseconds')}Z]"
        elif args.publication_after:
            publication = f"[{args.publication_after.isoformat(timespec='milliseconds')}Z"
        elif args.publication_before:
            publication = f"{args.publication_before.isoformat(timespec='milliseconds')}Z]"
        else:
            publication = None

        sort_query = None
        if (
            getattr(args, "sort", None)
            or getattr(args, "asc", False)
            or getattr(args, "desc", False)
        ):
            if getattr(args, "sort", None) == "ingestion":
                sort_prefix = "publicationDate,,"
            else:  # default to sensing time sorting
                sort_prefix = "start,time,"
                if not getattr(args, "sort", None):
                    logger.warning(
                        "Sorting by sensing time by default, use --sort {sensing, ingestion} to remove this warning."
                    )

            direction = 0
            if getattr(args, "desc", False):
                direction = 0
            if getattr(args, "asc", None):
                direction = 1
            sort_query = f"{sort_prefix}{direction}"

        _query = {
            "dtstart": args.dtstart,
            "dtend": args.dtend,
            "publication": publication,
            "bbox": args.bbox,
            "geo": args.geo,
            "sat": args.sat,
            "sort": sort_query,
            "cycle": args.cycle,
            "orbit": args.orbit,
            "relorbit": args.relorbit,
            "title": args.filename,
            "timeliness": args.timeliness,
            "type": args.product_type,
        }

        query = {key: value for key, value in _query.items() if value is not None}
        bbox = query.pop("bbox", None)
        if bbox is not None:
            query["bbox"] = ",".join(map(str, bbox))

        # Use the set=brief parameter to get results faster
        query["set"] = "brief"

        collection = datastore.get_collection(args.collection)
        search_results = collection.search(**query)
        products = search_results
        # Check the number of products
        num_products = len(products)

    return products, num_products


def _get_args_search_params(args: argparse.Namespace) -> List[str]:
    search_params_in_args = []
    vargs = vars(args)
    for param in [
        "dtstart",
        "dtend",
        "time_range",
        "publication_after",
        "publication_before",
        "sort",
        "bbox",
        "geo",
        "sat",
        "sort",
        "cycle",
        "orbit",
        "relorbit",
        "title",
        "timeliness",
    ]:
        if param in vargs and vargs[param]:
            search_params_in_args.append(param)
    return search_params_in_args


def _get_query_paging_params(query: str) -> List[str]:
    return [
        member
        for member in query.split("&")
        if member.split("=")[0] in ["format", "si", "c", "id", "pw"]
    ]


def parse_arguments_resources(args_res: str, datatailor: Any, resource: str) -> Any:
    res_config = args_res
    if res_config.endswith(".yml") or res_config.endswith(".yaml"):
        with open(res_config, "r") as file:
            try:
                if resource == "filters":
                    return Filter(**yaml.safe_load(file))
                elif resource == "rois":
                    return RegionOfInterest(**yaml.safe_load(file))
                elif resource == "quicklooks":
                    return Quicklook(**yaml.safe_load(file))
                else:  # chains
                    return Chain(**yaml.safe_load(file))
            except:
                logger.error("YAML file is corrupted. Please, check the YAML syntax.")
                sys.exit()
    elif res_config.endswith(".json"):
        with open(res_config, "r") as file:
            try:
                if resource == "filters":
                    return Filter(**json.load(file))
                elif resource == "rois":
                    return RegionOfInterest(**json.load(file))
                elif resource == "quicklooks":
                    return Quicklook(**json.load(file))
                else:  # chains
                    return Chain(**json.load(file))
            except:
                logger.error("JSON file is corrupted. Please, check the JSON syntax.")
                sys.exit()
    else:
        res_config = res_config.strip()
        if res_config.find(" ") < 0:
            # Assume resource name is being provided
            res_name = res_config
            logger.info(f"Using resource name: {res_name}")
            if resource == "filters":
                return datatailor.filters.read(res_name)
            elif resource == "rois":
                return datatailor.rois.read(res_name)
            elif resource == "quicklooks":
                return datatailor.quicklooks.read(res_name)
            else:  # chains
                return datatailor.chains.read(res_name)
        else:
            if not res_config.startswith("{"):
                res_config = "{" + res_config + "}"
            try:
                if resource == "filters":
                    return Filter(**yaml.safe_load(res_config))
                elif resource == "rois":
                    return RegionOfInterest(**yaml.safe_load(res_config))
                elif resource == "quicklooks":
                    return Quicklook(**yaml.safe_load(res_config))
                else:  # chains
                    return Chain(**yaml.safe_load(res_config))
            except:
                logger.error("YAML string is corrupted. Please, check the YAML syntax.")
                sys.exit()
