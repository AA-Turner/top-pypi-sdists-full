import argparse
import errno
import fnmatch
import json
import logging
import os
import random
import re
import shutil
import signal
import socket
import stat
import string
import subprocess
import sys
import threading
import time
import uuid
from collections import defaultdict
from datetime import datetime, timedelta
from multiprocessing import Process
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

import yaml
from paho.mqtt.client import Client, MQTTMessage, Properties

import eumdac
from eumdac import cli
from eumdac.cli_helpers import (
    _search,
    check_daily_window,
    get_datastore,
    get_datatailor,
    parse_arguments_resources,
    safe_run,
    validate_daily_window_args,
)
from eumdac.cli_mtg_helpers import (
    build_entries_from_coverage,
    is_collection_valid_for_coverage,
)
from eumdac.config import get_config_dir
from eumdac.download_app import DownloadApp
from eumdac.errors import EumdacError
from eumdac.fake import FakeMQTTClient  # type: ignore
from eumdac.logging import gen_table_printer, logger
from eumdac.order import Order, generate_random_string
from eumdac.product import Product
from eumdac.signals import signal_registry
from eumdac.subscription import (
    EumdacMQTTClient,
    ProcessFile,
    extract_payload,
    subscription_json_to_args_dict,
)
from eumdac.tailor_app import TailorApp
from eumdac.tailor_models import Chain
from eumdac.token import URLs


class OrderEventHandler:
    def __init__(
        self,
        datastore: Any,
        datatailor: Any,
        tags: List[str],
        download_params: Dict[str, Any],
        process_file: ProcessFile,
    ):
        self.datastore = datastore
        self.datatailor = datatailor
        self.tags = tags
        self.download_params = download_params
        self.process_file = process_file
        self.errors_logger = RollingBuffer(Path(download_params["output_dir"]) / "errors.log")

    def handle(self, filename: Path) -> None:
        # Ignore non-initialized orders
        if filename.name.startswith("_"):
            return
        order = SubscriptionOrder.from_file(Path(filename))
        (tag,) = order.get_dict_entries("tag")
        if tag in self.tags:
            set_latest_activity(self.process_file)
            order.update_download_params(self.download_params, self.datatailor)
            download_order(Path(filename), self.datastore, self.datatailor, self.errors_logger)


def subscription(
    args: argparse.Namespace,
    mqtt_client: Optional[Any] = None,  # used in tests
    config_dir: Path = get_config_dir(),  # used in tests
    event_handler: Optional[OrderEventHandler] = None,  # used in tests
) -> None:
    """eumdac subscription entrypoint"""

    eumdac.common.headers["referer"] += " DSN"

    if args.subscription_command == "list":
        subscription_list(args)
    elif args.subscription_command == "add":
        subscription_add(args, mqtt_client, config_dir)
    elif args.subscription_command == "download":
        subscription_download(args, config_dir, event_handler)
    elif args.subscription_command == "set-credentials":
        set_subs_credentials(args, config_dir)
    else:
        logger.error(f"Unknown subcommand: {args.subscription_command}")


def set_subs_credentials(args: argparse.Namespace, config_dir: Path) -> None:
    config_dir.mkdir(exist_ok=True)
    credentials_path = config_dir / "subscriptions/credentials"
    credentials_path.touch(mode=(stat.S_IRUSR | stat.S_IWUSR))

    try:
        with credentials_path.open(mode="w") as file:
            file.write(f"{args.username}\n{args.password}")  # type: ignore[arg-type]
        logger.info(f"Subscription credentials are written to file {credentials_path}")
    except OSError:
        logger.error(
            f"Credentials could not be written to {credentials_path}. Please review your configuration."
        )


def get_mqtt_client_auth(config_dir: Path) -> Tuple[str, str]:
    config_dir.mkdir(exist_ok=True)
    credentials_path = config_dir / "subscriptions/credentials"
    try:
        lines = credentials_path.read_text().split("\n")
        if len(lines) != 2 or len("".join(lines).strip()) == 0:
            logger.warning("Using no authentication.")
        else:
            return (lines[0], lines[1])
    except Exception as e:
        logger.warning(
            f"Unable to read subscription credentials from {credentials_path}, using no authentication."
        )
    return ("", "")


def cleanup_processes(config_dir: Path) -> None:
    if sys.platform.startswith("win"):
        cleanup_processes_win(config_dir)
    else:
        cleanup_processes_unix(config_dir)


def cleanup_processes_unix(config_dir: Path) -> None:
    # Cleanup leftover processes which pids are no longer valid
    process_dir = config_dir / "subscriptions/processes"
    hostname = socket.gethostname()
    for process_file in process_dir.glob("*.process"):
        p = load_json(process_file)
        if p["host"] != hostname:
            # Avoid removing processes started in another host
            logger.warning(
                f"Note: process {p['pid']} with tag {p['tag']} was started in a different host: {p['host']}."
            )
            continue

        # Try killing the process with signal 0, this will do nothing
        # but will raise an exception if the process doesn't exist
        try:
            os.kill(int(p["pid"]), 0)
        except OSError as error:
            if error.errno == errno.ESRCH:  # No such process
                logger.warning(
                    f"Cleaning leftover process file {p['pid']} as the process could not be found."
                )
                process_file.unlink()


def cleanup_processes_win(config_dir: Path) -> None:
    # Build the list of win processes running TASKLIST as a subprocess
    output_str = subprocess.check_output(("TASKLIST", "/FO", "CSV")).decode()
    # get rid of extra " and split into lines
    output = output_str.replace('"', "").split("\r\n")
    proc_list = [i.split(",") for i in output[1:] if i]
    existing_pids = [str(i[1]) for i in proc_list]

    process_dir = config_dir / "subscriptions/processes"
    hostname = socket.gethostname()
    for process_file in process_dir.glob("*.process"):
        p = load_json(process_file)
        if p["host"] != hostname:
            # Avoid removing processes started in another host
            logger.warning(
                f"Note: process {p['pid']} with tag {p['tag']} was started in a different host: {p['host']}."
            )
            continue

        if str(p["pid"]) not in existing_pids:
            logger.debug(
                f"Cleaning leftover process file {p['pid']} as the process could not be found"
            )
            process_file.unlink()


def subscription_list(
    args: argparse.Namespace,
    config_dir: Path = get_config_dir(),
) -> None:
    cleanup_processes(config_dir)

    logger.info("Subscriptions")
    logger.info("=" * len("Subscriptions"))

    process_dir = config_dir / "subscriptions/processes"
    subscription_processes = [load_json(fn) for fn in process_dir.glob("subscription_*.process")]
    download_processes = [load_json(fn) for fn in process_dir.glob("download_*.process")]

    host_length: int = 4
    for d in subscription_processes:
        if len(d["host"]) > host_length:
            host_length = len(d["host"])

    table_printer = gen_table_printer(
        logger.info,
        [
            ("Host", host_length),
            ("PID", 10),
            ("Tag", 38),
            ("Created on", 20),
            ("Latest Activity", 20),
            ("Collection", 30),
            ("Query", 50 if args.verbose else 5),
        ],
        column_sep="  ",
    )
    for d in subscription_processes:
        info = []
        if args.verbose:
            search_query = d["search_query"]
        else:
            search_query = "Yes" if d.get("search_query", None) else "No"
        info.extend(
            [
                d["host"],
                d["pid"],
                d["tag"],
                d["created_at"][:-7],
                d.get("latest_activity", "Never1234567")[:-7],
                topic_to_collectionid(d["topic"]),
                search_query,
            ]
        )
        table_printer(info)

    logger.info("")
    if not args.verbose:
        logger.info("(Note: use -v to get more details)\n")

    host_length = 4
    for d in download_processes:
        if len(d["host"]) > host_length:
            host_length = len(d["host"])

    logger.info("Downloaders")
    logger.info("=" * len("Downloaders"))
    table_printer = gen_table_printer(
        logger.info,
        [
            ("Host", host_length),
            ("PID", 10),
            ("Tag", 38),
            ("Created on", 20),
            ("Output dir", 50),
        ],
        column_sep="  ",
    )

    for p in download_processes:
        info = []
        info.extend(
            [
                p["host"],
                p["pid"],
                p["tag"],
                p["created_at"][:-7],
                p["output_dir"],
            ]
        )
        table_printer(info)

    logger.info("")

    subscription_tags = set([x["tag"] for x in subscription_processes])
    download_tags = set([x["tag"] for x in download_processes])
    downloaders_without_subscriptions = download_tags - subscription_tags
    if downloaders_without_subscriptions:
        logger.warning(
            f"There are downloaders for tags without subscriptions for the tags: {downloaders_without_subscriptions}"
        )

    subscription_without_downloaders = subscription_tags - download_tags
    if subscription_without_downloaders:
        logger.warning(
            f"There are subscriptions without downloaders for the tags: {subscription_without_downloaders}"
        )


def load_json(fn: Path) -> Dict[str, str]:
    with fn.open("r") as f:
        return json.load(f)


def search_is_needed(requested: Dict[str, Any]) -> bool:
    for attr in [
        "query",
        "dtstart",
        "dtend",
        "publication_before",
        "publication_after",
        "bbox",
        "geo",
    ]:
        if requested.get(attr) is not None:
            return True
    return False


def check_filters_via_mqtt_metadata(payload: Dict[str, Any], requested: Dict[str, Any]) -> bool:
    """
    Check if the given payload meets the specified filters in the requested dictionary.
    Returns:
        Optional[bool]:
            - Returns None if any of the requested filters for bounding box, geo, or query are present.
            - Returns True if all checks pass, False otherwise.
    """
    checks_passed = []
    requested = defaultdict(lambda: None, requested)
    payload["properties"] = defaultdict(lambda: None, payload["properties"])
    payload["_eumetsat_product_information"] = defaultdict(
        lambda: None, payload["_eumetsat_product_information"]
    )

    if requested["filename"]:
        checks_passed.append(
            fnmatch.fnmatch(payload["properties"]["data_id"], requested["filename"])
        )

    if requested["cycle"]:
        checks_passed.append(
            payload["_eumetsat_product_information"]["cycleNumber"] == str(requested["cycle"])
        )

    if requested["orbit"]:
        checks_passed.append(
            payload["_eumetsat_product_information"]["orbitNumber"] == str(requested["orbit"])
        )

    if requested["relorbit"]:
        checks_passed.append(
            payload["_eumetsat_product_information"]["relativeOrbitNumber"]
            == str(requested["relorbit"])
        )

    if requested["timeliness"]:
        checks_passed.append(
            payload["_eumetsat_product_information"]["timeliness"] == str(requested["timeliness"])
        )

    if requested["product_type"]:
        checks_passed.append(
            payload["_eumetsat_product_information"]["productType"]
            == str(requested["product_type"])
        )

    return all(checks_passed)


def check_filters_via_search(product_name: str, requested: Dict[str, Any]) -> bool:
    # The product filename will be used for faster searches, so "--filename" and "&title="
    # will be replaced, this forces us to check the filename through fnmatch before
    if requested["filename"]:
        if not fnmatch.fnmatch(product_name, requested["filename"]):
            return False
    # Now replace the filename filter with the product name for the rest of the search
    if not requested["query"]:
        requested["filename"] = product_name
    else:
        requested["query"] = [requested["query"][0] + f"&title={product_name}"]

    # Pending to confirm under which cirumstances we get the collection id as a list
    if type(requested["collection"]) is list:
        requested["collection"] = requested["collection"][0]

    _products, products_count = _search(argparse.Namespace(**requested))
    return products_count != 0


_urls = URLs()


def collectionid_to_topic(collection_id: str, satellite: Optional[str] = None) -> str:
    base_topic = _urls.get("datastore", "subscription_topic")
    if satellite is None:
        satellite = "+"
    return f"{base_topic}/{satellite}/{collection_id.lower()}"


def topic_to_collectionid(topic: str) -> str:
    """Convert a valid subscription topic to a Collection id"""
    return topic.split("/")[-1].upper()


def subscription_add(
    args: argparse.Namespace,
    mqtt_client: Optional[Any] = None,  # used in tests
    config_dir: Path = get_config_dir(),  # used in tests
) -> None:
    if args.tag is None:
        raise ValueError("--tag is required")

    (client_username, client_password) = get_mqtt_client_auth(config_dir)

    datastore = get_datastore(args, anonymous_allowed=True)

    if args.query:
        query_dict = {k: v for k, v in (pair.split("=") for pair in args.query[0].split("&"))}
        collection_id = query_dict["pi"]
        # The filename filter will be executed locally
        if query_dict.get("title"):
            logger.debug("Found title in query, check will be processed locally")
            args.filename = query_dict["title"]
            query_dict.pop("title")
        args.query = ["&".join([f"{k}={v}" for (k, v) in query_dict.items()])]
    else:
        collection_id = args.collection[0]
    if not getattr(args, "test", None):
        datastore.check_collection_id(collection_id)
    collection = datastore.get_collection(collection_id)

    def print_payload(
        message: MQTTMessage,
        level: int = logging.INFO,
    ) -> None:
        payload = extract_payload(message)
        logger.log(level, json.dumps(payload))

    def create_order(
        client: Client,
        userdata: Optional[Any],
        message: MQTTMessage,
        properties: Optional[Properties] = None,
    ) -> None:
        payload = extract_payload(message, parse_times=True)
        args_dict = subscription_json_to_args_dict(payload)
        product_str = args_dict["product"]
        product = datastore.get_product(collection._id, product_str)
        # args.tag is already safe for use as a directory name
        order_dir = config_dir / f"subscriptions/orders/{args.tag}"
        order_dir.mkdir(exist_ok=True, parents=True)
        order = SubscriptionOrder(order_dir=order_dir)
        order.initialize(
            products=[product],
            file_pattern=None,
            query=None,
            tag=args.tag,
            chain=None,
            output_dir=None,
        )

    if args.sat:
        valid_satellites = collection.search_options["sat"]["options"]
        if args.sat not in valid_satellites:
            logger.error(
                f"The satellite '{args.sat}' is not in the list of the valid choices for the collection '{collection}'. Valid choices are {valid_satellites}"
            )
            sys.exit(1)
    topic = collectionid_to_topic(str(collection), args.sat)
    t = datetime.now().strftime("%Y%m%d%H%M%S")
    random_suffix = "".join(random.choices(string.ascii_letters + string.digits, k=3))
    subscription_name = f"subscription_{t}_{random_suffix}"

    process_dir = config_dir / "subscriptions/processes"
    process_dir.mkdir(exist_ok=True, parents=True)

    def datetime_serializer(obj):  # type: ignore
        if isinstance(obj, datetime):
            return obj.isoformat()  # Convert datetime to ISO 8601 string
        raise TypeError(f"Type {type(obj)} not serializable")

    if not args.notifications_only:
        subscription_processes = [
            load_json(fn) for fn in process_dir.glob("subscription_*.process")
        ]
        existing_subscriptions = [
            (d["topic"], d["search_query"], d["tag"]) for d in subscription_processes
        ]
        query = query_dict_from_args(args)
        logger.debug(f"Query for listener: {query}")
        if (topic, query, args.tag) in existing_subscriptions:  # type: ignore
            logger.error("Subscription already exists!")
            sys.exit(1)
        process_file = ProcessFile(
            process_dir / f"{subscription_name}.process",
            json.dumps(
                {
                    "topic": topic,
                    "created_at": datetime.now().isoformat(),
                    "tag": args.tag,
                    "search_query": query,
                    "pid": os.getpid(),
                    "host": socket.gethostname(),
                },
                default=datetime_serializer,
            ),
        )

    def callback(
        client: Client,
        userdata: Optional[Any],
        message: MQTTMessage,
        properties: Optional[Properties] = None,
    ) -> None:
        payload = extract_payload(message, parse_times=True)

        # Ignore deletion notifications
        if str(payload["links"]).find("deletion") >= 0:
            logger.debug(f"Not processing deletion event for {payload['properties']['data_id']}")
            return

        vargs = vars(args)
        filters_passed = False
        if search_is_needed(vargs):
            payload = extract_payload(message, parse_times=True)
            args_dict = subscription_json_to_args_dict(payload)
            filters_passed = check_filters_via_search(args_dict["product"], vargs.copy())
        else:
            filters_passed = check_filters_via_mqtt_metadata(payload, vargs)

        # Check daily window if requested
        if filters_passed and getattr(args, "daily_window", None):
            (dw_start, dw_end) = validate_daily_window_args(args.daily_window)
            # Handle notifications without start_datetime or end_datetime, only datetime
            sensing_start = payload["properties"].get("start_datetime")
            sensing_end = payload["properties"].get("end_datetime")
            if not sensing_start:
                sensing_start = payload["properties"].get("datetime")
            if not sensing_end:
                sensing_end = payload["properties"].get("datetime")

            filters_passed &= check_daily_window(
                sensing_start,
                sensing_end,
                dw_start,
                dw_end,
            )

        if not filters_passed:
            logger.debug(f"Notification received but didn't pass the query filters:")
            print_payload(message, logging.DEBUG)
            return

        set_latest_activity(process_file)

        if args.print_notifications or args.notifications_only:
            print_payload(message)
        if not args.notifications_only:
            create_order(client, userdata, message, properties=None)

    if not mqtt_client:
        mqtturl = datastore.token.urls.get("datastore", "subscription_endpoint")
        logger.debug(f"Subscribing to {topic} on {mqtturl}")
        mqtt_client = EumdacMQTTClient(mqtturl, client_username, client_password)
    if args.mqtttest:
        mqtt_client = FakeMQTTClient()

    mqtt_client.add_subscription(topic, 1)
    mqtt_client.connect()
    mqtt_client.add_on_msg_callback(callback)
    logger.warning(f"Starting subscription to {topic}...")
    if not args.notifications_only and not args.quiet:
        logger.warning(
            f"You can now use 'eumdac subscribe download --tag={args.tag}' or 'eumdac subscribe download --only-incoming --tag={args.tag}' in another shell to download products published on this subscription"
        )
    mqtt_client.client.loop_forever()


def query_dict_from_args(args: argparse.Namespace) -> Dict[str, str]:
    # See https://docs.opengeospatial.org/is/13-026r9/13-026r9.html#20 for the mathematical notation expected by the publication filter
    if getattr(args, "publication_after", None) and getattr(args, "publication_before", None):
        publication = f"[{args.publication_after.isoformat(timespec='milliseconds')}Z,{args.publication_before.isoformat(timespec='milliseconds')}Z]"
    elif getattr(args, "publication_after", None):
        publication = f"[{args.publication_after.isoformat(timespec='milliseconds')}Z"
    elif getattr(args, "publication_before", None):
        publication = f"{args.publication_before.isoformat(timespec='milliseconds')}Z]"
    else:
        publication = None

    sort_query = None
    if getattr(args, "sort", None) or getattr(args, "asc", False) or getattr(args, "desc", False):
        if args.sort == "ingestion":
            sort_prefix = "publicationDate,,"
        elif args.sort == "sensing":
            sort_prefix = "start,time,"
        else:  # default to sensing time sorting
            if not args.sort:
                logger.warning(
                    "Sorting by sensing time by default, use --sort {sensing, ingestion} to remove this warning."
                )

        direction = 1
        if args.desc:
            direction = 0
        if args.asc:
            direction = 1
        sort_query = f"{sort_prefix}{direction}"
    _query = {
        "dtstart": getattr(args, "dtstart", None),
        "dtend": getattr(args, "dtend", None),
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

    return {key: value for key, value in _query.items() if value is not None}


def set_latest_activity(process_file: ProcessFile) -> None:
    try:
        with process_file.path.open("r") as f:
            d = json.load(f)
        d["latest_activity"] = datetime.now().isoformat()
        with process_file.path.open("w") as f:
            f.write(json.dumps(d))
    except Exception as e:
        logger.debug(f"Failed to set latest activity: {e}")


class RollingBuffer:
    def __init__(self, filename: Path):
        self.filename = filename
        self.filename.parent.mkdir(parents=True, exist_ok=True)

    def get_filename(self, datetime: datetime) -> Path:
        return self.filename.parent / str(
            f"{self.filename.stem}.{datetime.date().isoformat()}{self.filename.suffix}"
        )

    def add_message(self, message: str) -> None:
        current_time = datetime.now()
        filename = self.get_filename(current_time)
        try:
            with open(filename, "a") as file:
                file.write(f"{current_time.isoformat()} {message}\n")
        except Exception as e:
            # Writing to the rolling buffer is a best effort action that can fail
            logger.debug(f"Could not write to {filename} due to {e}")
            pass


def download_order(
    order_path: Path, datastore: Any, datatailor: Any, errors_logger: RollingBuffer
) -> None:
    if not re.match(r"\d{4}-\d{2}-\d{2}_\d{2}-\d{2}_[A-Za-z0-9]+\.yml", order_path.name):
        return
    try:
        order = Order(order_path)
        order.status()
    except (EumdacError, FileNotFoundError):
        return
    if order.status() != "NOT COMPLETED":
        return

    with order.dict_from_file() as d:
        try:
            output_dir = d["output_dir"]
            file_patterns = d["file_patterns"]
        except KeyError:
            output_dir = None
            logger.error("Could not get output_dir for errors.log")

    product = ",".join(p.p_id for p in order.iter_product_info())
    chain_str = ""
    collection = order.collections()[0]
    logger.info(f"Processing product {product}")
    app: Any = None
    if datatailor:
        app = TailorApp(order, datastore, datatailor)
        chain_str = str(order.get_dict_entries("chain")[0])[1:-1]
    else:
        app = DownloadApp(order, datastore, integrity=(not file_patterns))
    success = False
    try:
        success = safe_run(app, keep_order=False, avoid_order_management=True)
    except Exception as e:
        logger.error(f"Got exception: {e}")
        success = False

    if not success:
        # Report the failure
        logger.error(f"FAILED processing order for {product}")
        # Including how to retry the download
        logger.error("In order to try again for this product, do it manually by running:")
        download_command = f"eumdac download -c {collection} -p {product}"
        if chain_str:
            download_command += f' --chain "{chain_str}"'
        logger.error(f"\t $ {download_command}")
        # And add the info to the error log
        if output_dir is not None:
            errors_logger.add_message(f"Failed to execute $ {download_command}")
    else:
        logger.info(f"SUCCESS processing order for {product}")

    # Cleanup the order (won't be deleted in case of FAILURES or --entry causing no download)
    cleanup_order(order_path)


def subscription_download(
    args: argparse.Namespace,
    config_dir: Path = get_config_dir(),  # used in tests
    event_handler: Optional[OrderEventHandler] = None,  # used in tests
) -> None:
    t = datetime.now().strftime("%Y%m%d%H%M%S")
    random_suffix = "".join(random.choices(string.ascii_letters + string.digits, k=3))
    subscription_name = f"download_{t}_{random_suffix}"

    datastore = get_datastore(args, anonymous_allowed=True)
    datatailor = None
    if getattr(args, "chain", None):
        datatailor = get_datatailor(args, datastore.token)

    tag = args.tag
    delay = getattr(args, "delay", 0)
    if not delay:
        delay = 0
    delay_delta = timedelta(minutes=delay)

    process_dir = config_dir / "subscriptions/processes"
    process_dir.mkdir(exist_ok=True, parents=True)

    # Check if there's already a downloader for the tag (they'd compete for the order files)
    download_processes = [load_json(fn) for fn in process_dir.glob("download_*.process")]
    for p in download_processes:
        if p["tag"] == tag:
            logger.error(f'A downloader for tag "{tag}" already exists.')
            logger.error(
                "If you really need to download the same products multiple times, start a new listener with a different tag."
            )
            logger.error("Run the following command to get info on existing processes:")
            logger.error("\t$ eumdac subs list")
            return

    order_dir = config_dir / f"subscriptions/orders/{tag}"
    order_dir.mkdir(exist_ok=True, parents=True)
    logger.warning(f"Start listening for orders in {order_dir}...")

    process_file = ProcessFile(
        process_dir / f"{subscription_name}.process",
        json.dumps(
            {
                "created_at": datetime.now().isoformat(),
                "tag": tag,
                "output_dir": str(args.output_dir.resolve()),
                "pid": os.getpid(),
                "host": socket.gethostname(),
            }
        ),
    )
    download_params = {
        "dirs": args.dirs,
        "onedir": args.onedir,
        "file_patterns": args.entry,
        "output_dir": args.output_dir,
        "chain": getattr(args, "chain", None),
    }

    # Manage MTG coverage (--download-coverage)
    if args.download_coverage:
        # Extract collection from topic based on tag
        subscription_processes = [
            load_json(fn) for fn in process_dir.glob("subscription_*.process")
        ]
        for p in subscription_processes:
            if p["tag"] == tag:
                collection = topic_to_collectionid(p["topic"])
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
        download_params["file_patterns"], expected = build_entries_from_coverage(
            args.download_coverage
        )
        logger.info(
            f"As per the requested {args.download_coverage} coverage, {expected} entries will be downloaded for each product."
        )
    # Manage --entry param
    elif download_params["file_patterns"]:
        logger.warning("Disabling integrity check as --entry was provided.")
        if download_params["onedir"]:
            logger.warning(
                "Warning: the --onedir flag together with --entry can result in files with the same filename not being downloaded."
            )

    if event_handler is None:
        event_handler = OrderEventHandler(datastore, datatailor, tag, download_params, process_file)

    if not args.only_incoming:
        for f in sorted(
            list(order_dir.glob("*.yml")), key=lambda x: x.stat().st_mtime, reverse=True
        ):
            # Ignore non-initialized orders
            if f.name.startswith("_"):
                continue
            # Consider requested delay
            if datetime.fromtimestamp(f.stat().st_ctime) + delay_delta > datetime.now():
                continue
            order = SubscriptionOrder.from_file(Path(f))
            order.update_download_params(download_params, datatailor)
            logger.info(f"START processing order {f}")
            download_order(f, datastore, datatailor, event_handler.errors_logger)

    observer = Observer(delay_delta)
    observer.schedule(event_handler, str(order_dir))
    observer.start()

    def handle_shutdown() -> None:
        observer.stop()
        observer.join(1)

    signal_registry.register(signal.SIGINT, handle_shutdown)

    while True:
        observer.join(1)


class Observer(threading.Thread):
    _delay_delta: timedelta

    def __init__(self, delay_delta: timedelta = timedelta(minutes=0)) -> None:
        self.observed_dirs: List[Dict[str, Any]] = []
        self.stopped = False
        self._delay_delta = delay_delta
        super().__init__()

    def schedule(self, event_handler: OrderEventHandler, dir: str) -> None:
        self.observed_dirs.append(
            {
                "handler": event_handler,
                "dir": Path(dir),
                "last_state": set(Path(dir).glob("*")),
            }
        )

    def run(self) -> None:
        while not self.stopped:
            for entry in self.observed_dirs:
                # Remove not-yet-attended orders due to delay from last state
                to_remove = set()
                for t in entry["last_state"]:
                    try:
                        if (
                            datetime.fromtimestamp(t.stat().st_ctime) + self._delay_delta
                            > datetime.now()
                        ):
                            to_remove.add(t)
                    except Exception:
                        pass
                for t in to_remove:
                    entry["last_state"].remove(t)
                # Assess current state
                current_state = set(Path(entry["dir"]).glob("*"))
                new_things = current_state - entry["last_state"]
                for t in new_things:
                    if self.stopped:
                        break
                    if not t.is_file():
                        continue
                    # Consider requested delay
                    if (
                        datetime.fromtimestamp(t.stat().st_ctime) + self._delay_delta
                        > datetime.now()
                    ):
                        current_state.remove(t)
                        continue
                    try:
                        entry["handler"].handle(t)
                    except EumdacError as e:
                        # TODO: Clearly identify what couldn't be downloaded
                        logger.error(f"Could not handle {t} due to {e}")
                        cleanup_order(t)
                    except Exception as e:
                        # TODO: Clearly identify what couldn't be downloaded
                        logger.exception(f"Unhandled Error! {e}")
                        cleanup_order(t)
                entry["last_state"] = current_state
            time.sleep(0.1)

    def stop(self) -> None:
        self.stopped = True


def cleanup_order(order_file: Path) -> None:
    try:
        order_file.unlink()
    except Exception:
        # Don't care if we can't delete the file
        pass


class SubscriptionOrder(Order):
    def __init__(
        self,
        order_dir: Path,
    ):
        self._order_dir = order_dir
        self._order_file = self.new_order_filename()
        super().__init__(self._order_file, order_dir)

    @classmethod
    def from_file(cls, order_file: Path) -> "SubscriptionOrder":
        self = cls(Path(order_file).parent)
        self._order_file = order_file
        return self

    def initialize(
        self,
        chain: Optional[Chain],
        products: Iterable[Product],
        output_dir: Optional[Path],
        file_pattern: Optional[Iterable[str]],
        query: Optional[Dict[str, str]],
        dirs: bool = False,
        onedir: bool = False,
        no_warning_logs: bool = True,
        tag: Optional[str] = None,
    ) -> None:
        self._order_file.touch(exist_ok=False)
        self._file_patterns = file_pattern
        self._no_warning_logs = no_warning_logs
        order_info: Dict[str, Any] = {
            "file_patterns": file_pattern,
            "query": query,
            "tag": tag,
            "dirs": dirs,
            "onedir": onedir,
            "type": "download",
            "products_to_process": {
                p._id: {
                    "col_id": p.collection._id,
                    "server_state": "UNSUBMITTED",
                }
                for p in products
            },
        }

        with self._lock:
            with self._order_file.open("w") as orf:
                yaml.dump(
                    order_info,
                    orf,
                )
        final_order_name = self._order_file.name.lstrip("_")
        self._order_file.rename(self._order_file.with_name(final_order_name))

    def update_download_params(self, download_params: Dict[str, Any], datatailor: Any) -> None:
        with self.dict_from_file() as d:
            d["output_dir"] = str(download_params["output_dir"].resolve())  # type: ignore
            d["dirs"] = download_params["dirs"]
            d["onedir"] = download_params["onedir"]
            d["file_patterns"] = download_params["file_patterns"]
            if download_params["chain"]:
                d["type"] = "tailor"
                d["chain"] = parse_arguments_resources(
                    download_params["chain"], datatailor, resource="chains"
                ).asdict()
                for p_id in d["products_to_process"].keys():
                    d["products_to_process"][p_id]["customisation"] = None
            # Update instance members
            self._output_dir = d["output_dir"]
            self._file_patterns = d["file_patterns"]
        self._locked_serialize(d)

    def new_order_filename(self) -> Path:
        order_dir = self._order_dir
        salt = generate_random_string()
        # Prepend with underscore as long as it is not initialized
        order_fn = order_dir / Path(f"_{datetime.now().strftime('%Y-%m-%d_%H-%M')}_{salt}.yml")
        return order_fn


def handle_livefeed(args: argparse.Namespace) -> Any:
    tag = str(uuid.uuid4())

    def wire_arg(
        args: argparse.Namespace,
        arg_list: List[str],
        arg_name: str,
        arg_cli_name: Optional[str] = None,
    ) -> None:
        if getattr(args, arg_name, None):
            name = arg_cli_name if arg_cli_name else arg_name
            value = getattr(args, arg_name)
            if type(value) is datetime:
                value = value.isoformat()
            else:
                value = str(value)
            arg_list += [f"--{name}", value]

    # Split arguments for listener and downloader processes
    listener_args = ["subs", "add", "--tag", tag, "--quiet"]
    if args.print_notifications:
        listener_args.append("--print-notifications")

    if getattr(args, "query", None):
        listener_args += ["-q", args.query[0]]
    else:
        listener_args += ["-c", args.collection[0]]
    wire_arg(args, listener_args, "dtstart", "start")
    wire_arg(args, listener_args, "dtend", "end")
    wire_arg(args, listener_args, "publication_before", "publication-before")
    wire_arg(args, listener_args, "publication_after", "publication-after")
    if getattr(args, "daily_window"):
        listener_args += ["--daily-window"]
        listener_args += [d for d in args.daily_window]
    wire_arg(args, listener_args, "sat")
    if getattr(args, "bbox"):
        listener_args += ["--bbox"]
        listener_args += [str(b) for b in args.bbox]
    wire_arg(args, listener_args, "geo", "geometry")
    wire_arg(args, listener_args, "cycle")
    wire_arg(args, listener_args, "orbit")
    wire_arg(args, listener_args, "relorbit")
    wire_arg(args, listener_args, "filename")
    wire_arg(args, listener_args, "timeliness")
    wire_arg(args, listener_args, "product_type", "product-type")

    downloader_args = [
        "subs",
        "download",
        "--tag",
        tag,
        "-o",
        str(args.output_dir),
        "--quiet",
    ]
    if getattr(args, "entry"):
        downloader_args += ["--entry"]
        downloader_args += [str(e) for e in args.entry]
    wire_arg(args, downloader_args, "download_coverage", "download-coverage")
    if getattr(args, "onedir"):
        downloader_args += ["--onedir"]
    if getattr(args, "dirs"):
        downloader_args += ["--dirs"]
    wire_arg(args, downloader_args, "download_threads", "threads")
    if getattr(args, "no_progress_bars"):
        downloader_args += ["--no-progress-bars"]
    wire_arg(args, downloader_args, "chain")
    wire_arg(args, downloader_args, "delay")

    if args.verbose:
        listener_args += ["-v" for _ in range(0, args.verbose)]
        downloader_args += ["-v" for _ in range(0, args.verbose)]

    if args.debug:
        listener_args.append("--debug")
        downloader_args.append("--debug")

    if args.trace:
        listener_args.append("--trace")
        downloader_args.append("--trace")

    logger.debug("Spawning subprocesses")
    p_listener = Process(target=cli.cli, args=(listener_args,))
    p_listener.start()
    # Wait two seconds for the listener to start and check before starting the downloader
    time.sleep(2)
    if not p_listener.is_alive():
        logger.debug(f"Listener process terminated with code {p_listener.exitcode}")
        logger.error("Failed to start listener process, please review your input.")
        p_listener.join()
        sys.exit(1)

    p_downloader = Process(target=cli.cli, args=(downloader_args,))
    p_downloader.start()
    time.sleep(0.5)
    if not p_downloader.is_alive():
        logger.debug(f"Downloader process terminated with code {p_listener.exitcode}")
        logger.error("Failed to start downloader process, please review your input.")
        p_listener.terminate()
        p_listener.join()
        p_downloader.join()
        sys.exit(1)

    done = False
    try:
        while not done:
            logger.trace("Checking status of subprocesses...")
            if not p_listener.is_alive():
                logger.debug(f"Listener process terminated with code {p_listener.exitcode}")
                logger.warning(
                    f"Listener process with PID {p_listener.pid} is no longer running, restarting..."
                )
                p_listener.join()
                delete_process_file(p_listener.pid)  # type: ignore
                p_listener = Process(target=cli.cli, args=(listener_args,))
                p_listener.start()
            if not p_downloader.is_alive():
                logger.debug(f"Downloader process terminated with code {p_downloader.exitcode}")
                logger.warning(
                    f"Downloader process with PID {p_downloader.pid} is no longer running, restarting..."
                )
                p_downloader.join()
                delete_process_file(p_downloader.pid)  # type: ignore
                p_downloader = Process(target=cli.cli, args=(downloader_args,))
                p_downloader.start()
            # Wait before trying to revive the processes again
            time.sleep(5)
    except KeyboardInterrupt:
        logger.info("Shutting down")
    finally:
        # Wait for the processes to finish one last time
        p_listener.join()
        p_downloader.join()


def delete_process_file(pid: int) -> None:
    try:
        hostname = socket.gethostname()
        process_dir = get_config_dir() / "subscriptions/processes"
        processes = [(fn, load_json(fn)) for fn in process_dir.glob("*.process")]
        for process in processes:
            if int(process[1]["pid"]) == pid and process[1]["host"] == hostname:
                logger.warning(
                    f"Manually deleting leftover process file {(process_dir / process[0])}"
                )
                # Remnant process, delete file
                (process_dir / process[0]).unlink(missing_ok=True)
                return
    except Exception as e:
        logger.debug(f"Failed to delete process file for {pid}", e)
        pass
