import os

import pytest

from utf_queue_client.utils import (
    UTF_QUEUE_REGION_MAP,
    get_closest_queue_region,
    get_queue_url_list,
)

NOMAD_DC_PARAMS = [
    ("NOMAD_DC", value)
    for value in [
        None,
        "aws-us-east-1",
        "vmw-us-aus-1",
        "vmw-us-bos-1",
        "vmw-eu-bud-1",
        "vmw-ap-hyd-1",
        "vmw-ca-yul-1",
        "vmw-ap-syd-1",
    ]
]
FAKE_CREDS = "notarealusername:notarealpassword"


@pytest.mark.parametrize(
    "set_environment_variable",
    NOMAD_DC_PARAMS,
    indirect=True,
)
@pytest.mark.parametrize("domain", ["dev.silabs.net", "silabs.net"])
def test_get_queue_url_list(set_environment_variable, domain):
    nomad_dc = os.getenv("NOMAD_DC")
    url = f"amqps://{FAKE_CREDS}@utf-queue-central.{domain}:443/%2F?stack_timeout=30"
    urls = get_queue_url_list(url)
    assert len(urls) == 6

    region_list = list(UTF_QUEUE_REGION_MAP.values())
    if nomad_dc is None or nomad_dc not in UTF_QUEUE_REGION_MAP:
        assert urls[0] == url
        region_list.remove("central")
    else:
        region = UTF_QUEUE_REGION_MAP[nomad_dc]
        assert urls[0] == url.replace("utf-queue-central", f"utf-queue-{region}")
        region_list.remove(region)
    assert urls[1:] == [
        url.replace("utf-queue-central", f"utf-queue-{region}")
        for region in region_list
    ]


def test_get_queue_url_list_no_match():
    url_list = [
        f"amqps://{FAKE_CREDS}@custom-server.silabs.net:443/%2F?stack_timeout=30",
        f"amqp://{FAKE_CREDS}@utf-queue-central.silabs.net:5672/%2F",
        f"amqps://{FAKE_CREDS}@utf-queue-central.silabs.net:5672/%2F",
        f"amqps://{FAKE_CREDS}@utf-queue-central.silabs.com:443/%2F",
    ]
    for url in url_list:
        urls = get_queue_url_list(url)
        assert urls == [url]


@pytest.mark.parametrize(
    "set_environment_variable",
    NOMAD_DC_PARAMS,
    indirect=True,
)
def test_get_closest_queue_region(set_environment_variable):
    nomad_dc = os.getenv("NOMAD_DC")
    try:
        if nomad_dc is None or nomad_dc not in UTF_QUEUE_REGION_MAP:
            assert get_closest_queue_region() == "central"
        else:
            assert get_closest_queue_region() == UTF_QUEUE_REGION_MAP[nomad_dc]
    finally:
        os.environ.pop("NOMAD_DC", None)
