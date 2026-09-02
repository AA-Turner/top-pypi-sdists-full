import argparse
import json
import multiprocessing
import os
import signal
import time
import uuid
from datetime import datetime, timedelta
from multiprocessing import Pipe, Process
from types import SimpleNamespace

import pytest
from sh import eumdac

from eumdac.cli import subscription
from eumdac.cli_subscriptions import (
    OrderEventHandler,
    SubscriptionOrder,
    collectionid_to_topic,
)
from eumdac.subscription import (
    CorruptedJsonError,
    InsufficientInfoError,
    TimeWindow,
    subscription_json_to_args_dict,
)


@pytest.fixture
def collection_ids():
    return [
        "EO:EUM:DAT:METOP:SOMO12",
        "EO:EUM:DAT:MSG:CLM",
        "EO:EUM:DAT:MSG:RSS-CLM",
        "EO:EUM:DAT:METOP:IASSND02",
        "EO:EUM:DAT:METOP:ASCSZF1B",
        "EO:EUM:DAT:METOP:IASIL1C-ALL",
        "EO:EUM:DAT:METOP:IASSND02",
    ]


def test_collection_to_topic_no_satellite(collection_ids):
    for collection_id in collection_ids:
        output = collectionid_to_topic(collection_id)
        expected = f"org/eumetsat/ds/notification/+/{collection_id.lower()}"
        assert output == expected


def test_collection_to_topic_with_satellite(collection_ids):
    for collection_id in collection_ids:
        output = collectionid_to_topic(collection_id, satellite="MSG4")
        expected = f"org/eumetsat/ds/notification/MSG4/{collection_id.lower()}"
        assert output == expected


def test_subscription_json_to_args_dict_corrupted_json():
    with pytest.raises(CorruptedJsonError):
        subscription_json_to_args_dict(None)


def test_subscription_json_to_args_dict_json_with_insufficient_info():
    with pytest.raises(InsufficientInfoError):
        subscription_json_to_args_dict({})


# test order creation
def mqtt_data(
    id=None,
    version="v04",
    type="Feature",
    geometry=None,
    pubtime_minutes=None,
    data_id=None,
    start_datetime_minutes=None,
    end_datetime_minutes=None,
    links=None,
    parentIdentifier="EO:EUM:DAT:MSG:MSG15-RSS",
    platform="MSG4",
    productType="MSG15",
    base_date=None,
):
    # Set a base date to January 1, 2025, if not provided
    if base_date is None:
        base_date = datetime(2025, 1, 1)

    # Generate a unique ID if not provided
    if id is None:
        id = str(uuid.uuid4())

    # Calculate timestamps based on provided minutes
    pubtime = (
        (base_date + timedelta(minutes=pubtime_minutes))
        if pubtime_minutes is not None
        else base_date
    )
    start_datetime = (
        (base_date + timedelta(minutes=start_datetime_minutes))
        if start_datetime_minutes is not None
        else (base_date - timedelta(minutes=3))
    )
    end_datetime = (
        (base_date + timedelta(minutes=end_datetime_minutes))
        if end_datetime_minutes is not None
        else base_date
    )

    # Format the data_id to match the required format
    if data_id is None:
        timestamp_str = (
            pubtime.strftime("%Y%m%d%H%M%S.%f") + "000Z"
        )  # Format to YYYYMMDDHHMMSS.sssZ
        data_id = f"{platform}-SEVI-{productType}-0100-NA-{timestamp_str}-NA"

    # Set default links if not provided
    if links is None:
        links = [
            {
                "href": "https://user.eumetsat.int/api-definitions/data-store-download-api",
                "rel": "canonical",
                "type": "text/html",
            },
            {
                "href": "https://api.eumetsat.int/data/download/1.0.0/collections/EO%3AEUM%3ADAT%3AMSG%3AMSG15-RSS/products/MSG4-SEVI-MSG15-0100-NA-20240807081915.421000000Z-NA",
                "rel": "service",
                "type": "application/zip",
                "length": 57528,
            },
            {
                "href": "https://api.eumetsat.int/data/browse/1.0.0/collections/EO%3AEUM%3ADAT%3AMSG%3AMSG15-RSS/products/MSG4-SEVI-MSG15-0100-NA-20240807081915.421000000Z-NA?format=json",
                "rel": "related",
                "type": "application/json",
            },
        ]

    # Construct the test data dictionary
    fake_d = {
        "id": id,
        "version": version,
        "type": type,
        "geometry": geometry,
        "properties": {
            "pubtime": pubtime.isoformat() + "Z",
            "data_id": data_id,
            "start_datetime": start_datetime.isoformat() + "Z",
            "end_datetime": end_datetime.isoformat() + "Z",
        },
        "links": links,
        "_eumetsat_product_information": {
            "parentIdentifier": parentIdentifier,
            "platform": platform,
            "productType": productType,
        },
    }
    return json.dumps(fake_d)


def test_subscription_json_to_args_dict_normal():
    output = subscription_json_to_args_dict(json.loads(mqtt_data()))
    expected = {
        "collection": "EO:EUM:DAT:MSG:MSG15-RSS",
        "product": "MSG4-SEVI-MSG15-0100-NA-20250101000000.000000000Z-NA",
    }
    assert output == expected


class FakeMQTTClientCore:
    def __init__(self, parent):
        self.parent = parent

    def loop_forever(self):
        self.parent.loop_forever()


class FakeMQTTClient:
    def __init__(self, messages):
        self.messages = messages
        self.client = FakeMQTTClientCore(self)
        self.on_msg_callbacks = []

    def add_subscription(self, topic, num):
        pass

    def connect(self):
        pass

    def add_on_msg_callback(self, func):
        self.on_msg_callbacks.append(func)

    def loop_forever(self):
        for msg in self.messages:
            for cb in self.on_msg_callbacks:
                msg_resp = SimpleNamespace()
                msg_resp.payload = msg.encode()
                cb(None, None, msg_resp)


class TestNamespace:
    __test__ = False

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __getattr__(self, name):
        # Return None for non-existent attributes
        return None


def test_orders_will_be_created_in_subscription_orders_dir(tmp_path):
    tag = "foo"
    subscription(
        TestNamespace(
            subscription_command="add",
            test=True,
            collection=["FooCollection"],
            sat=None,
            query=None,
            bbox=None,
            geo=None,
            printnotifications=False,
            createorders=True,
            mqtttest=False,
            tag=tag,
        ),
        mqtt_client=FakeMQTTClient([mqtt_data()]),
        config_dir=tmp_path / "config",
    )
    orders = list((tmp_path / f"config/subscriptions/orders/{tag}").glob("*.yml"))
    assert len(orders) == 1


class FakeOrderEventHandler(OrderEventHandler):
    def __init__(self, conn):
        self.conn = conn

    def handle(self, object):
        print(f"handled {object}")
        self.conn.send(f"Handled {object}")


def test_orders_will_be_picked_up_by_download_subscriptions(tmp_path):
    tag = "test"
    config_dir = tmp_path / "config"
    order_dir = config_dir / f"subscriptions/orders/{tag}"
    c_receiving, c_sending = Pipe()

    ctx = multiprocessing.get_context("fork")

    def download():
        event_handler = FakeOrderEventHandler(c_sending)
        subscription(
            argparse.Namespace(
                subscription_command="download",
                only_incoming=True,
                tag=tag,
                output_dir=tmp_path,
                product=None,
                integrity=None,
                keep_order=None,
                dirs=None,
                onedir=None,
                entry=None,
                download_coverage=None,
                test=True,
                chain=None,
            ),
            event_handler=event_handler,
            config_dir=config_dir,
        )

    p = ctx.Process(target=download)
    p.start()
    time.sleep(0.1)  # Thread needs some setup time for being ready and listening

    order = SubscriptionOrder(order_dir=order_dir)
    order.initialize(None, [], None, None, None, tag=tag)
    time.sleep(0.1)  # Thread needs some time for notifying about the new file

    p.kill()
    events = []
    while c_receiving.poll(0.5):
        events.append(c_receiving.recv())
    assert len(list(order_dir.glob("*.yml"))) == 1
    assert any(["Handled" in str(x) for x in events])


def t(num):
    return datetime(year=2025, month=1, day=1, second=num)


def test_filter_window_left_overlapping():
    """
    requested:    |--------|
    product:   |-----|
    """
    assert TimeWindow(t(5), t(10)).overlaps_with(TimeWindow(t(1), t(7)))


def test_filter_window_full_overlapping():
    """
    requested:    |--------|
    product:       |----|
    """
    assert TimeWindow(t(5), t(10)).overlaps_with(TimeWindow(t(5), t(10)))


def test_filter_window_full_overlapping_product():
    """
    requested:    |--------|
    product:     |----------|
    """
    assert TimeWindow(t(5), t(10)).overlaps_with(TimeWindow(t(3), t(11)))


def test_filter_window_right_overlapping():
    """
    requested:    |--------|
    product:            |-----|
    """
    assert TimeWindow(t(5), t(10)).overlaps_with(TimeWindow(t(8), t(12)))


def test_filter_window_outside_left():
    """
    requested:    |--------|
    product: |---|
    """
    assert not TimeWindow(t(5), t(10)).overlaps_with(TimeWindow(t(1), t(4)))


def test_filter_window_outside_right():
    """
    requested:    |--------|
    product:                 |-----|
    """
    assert not TimeWindow(t(5), t(10)).overlaps_with(TimeWindow(t(11), t(15)))


def test_time_within_window():
    """
    requested:    |
    product:   |-----|
    """
    assert TimeWindow(t(5), t(10)).contains(t(7))  # 7 is within the window


def test_time_at_start():
    """
    requested: |
    product:   |-----|
    """
    assert TimeWindow(t(5), t(10)).contains(t(5))  # 5 is at the start of the window


def test_time_at_end():
    """
    requested:       |
    product:   |-----|
    """
    assert TimeWindow(t(5), t(10)).contains(t(10))  # 10 is at the end of the window


def test_time_outside_window_left():
    """
    requested: |
    product:    |-----|
    """
    assert not TimeWindow(t(5), t(10)).contains(t(4))  # 4 is outside the window


def test_time_outside_window_right():
    """
    requested:        |
    product:   |-----|
    """
    assert not TimeWindow(t(5), t(10)).contains(t(11))  # 11 is outside the window


import eumdac.cli_subscriptions as cs


def test_extract_payload_just_datetime():
    # No start_datetime or end_datetime
    data = '{"id":"07d6872a-4f56-408e-8683-db75f2eb9f05","conformsTo":["http://wis.wmo.int/spec/wnm/1/conf/core"],"type":"Feature","geometry":null,"properties":{"pubtime":"2025-11-11T11:18:16.149Z","data_id":"MSG4-SEVI-MSGCLMK-0100-0100-20251111110500.000000000Z-NA","datetime":"2025-11-11T11:05:00Z"},"links":[{"href":"https://user.eumetsat.int/api-definitions/data-store-download-api","rel":"service-doc","type":"text/html"},{"href":"https://api.eumetsat.int/data/download/1.0.0/collections/EO%3AEUM%3ADAT%3AMSG%3ARSS-CLM/products/MSG4-SEVI-MSGCLMK-0100-0100-20251111110500.000000000Z-NA","rel":"canonical","type":"application/zip","length":111},{"href":"https://api.eumetsat.int/data/browse/1.0.0/collections/EO%3AEUM%3ADAT%3AMSG%3ARSS-CLM/products/MSG4-SEVI-MSGCLMK-0100-0100-20251111110500.000000000Z-NA?format=json","rel":"service-meta","type":"application/json"}],"_eumetsat_product_information":{"parentIdentifier":"EO:EUM:DAT:MSG:RSS-CLM","platform":"MSG4","productType":"MSGCLMK"}}'

    message = SimpleNamespace()
    message.topic = "XX"
    message.payload = data.encode()
    payload = cs.extract_payload(message, parse_times=True)

    assert "datetime" in payload["properties"]

    # Handle notifications without start_datetime or end_datetime, only datetime
    sensing_start = payload["properties"].get("start_datetime")
    sensing_end = payload["properties"].get("end_datetime")
    if not sensing_start:
        sensing_start = payload["properties"].get("datetime")
    if not sensing_end:
        sensing_end = payload["properties"].get("datetime")


def test_extract_payload_start_datetime():
    # No start_datetime or end_datetime
    data = '{"id":"729a485e-bd22-4937-9bdd-0cf2ac2f6bf9","conformsTo":["http://wis.wmo.int/spec/wnm/1/conf/core"],"type":"Feature","geometry":null,"properties":{"pubtime":"2025-11-11T11:34:49.858Z","data_id":"MSG4-SEVI-MSG15-0100-NA-20251111113419.878000000Z-NA","start_datetime":"2025-11-11T11:30:12.61Z","end_datetime":"2025-11-11T11:34:19.878Z"},"links":[{"href":"https://user.eumetsat.int/api-definitions/data-store-download-api","rel":"service-doc","type":"text/html"},{"href":"https://api.eumetsat.int/data/download/1.0.0/collections/EO%3AEUM%3ADAT%3AMSG%3AMSG15-RSS/products/MSG4-SEVI-MSG15-0100-NA-20251111113419.878000000Z-NA","rel":"canonical","type":"application/zip","length":57425},{"href":"https://api.eumetsat.int/data/browse/1.0.0/collections/EO%3AEUM%3ADAT%3AMSG%3AMSG15-RSS/products/MSG4-SEVI-MSG15-0100-NA-20251111113419.878000000Z-NA?format=json","rel":"service-meta","type":"application/json"}],"_eumetsat_product_information":{"parentIdentifier":"EO:EUM:DAT:MSG:MSG15-RSS","platform":"MSG4","productType":"MSG15"}}'

    message = SimpleNamespace()
    message.topic = "XX"
    message.payload = data.encode()
    payload = cs.extract_payload(message, parse_times=True)

    assert "start_datetime" in payload["properties"]
    assert "end_datetime" in payload["properties"]

    # Handle notifications without start_datetime or end_datetime, only datetime
    sensing_start = payload["properties"].get("start_datetime")
    sensing_end = payload["properties"].get("end_datetime")
    if not sensing_start:
        sensing_start = payload["properties"].get("datetime")
    if not sensing_end:
        sensing_end = payload["properties"].get("datetime")
