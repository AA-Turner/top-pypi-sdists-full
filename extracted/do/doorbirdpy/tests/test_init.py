from aiohttp import ClientResponseError

from doorbirdpy import DoorBird
from doorbirdpy.schedule_entry import DoorBirdScheduleEntry
from aioresponses import aioresponses
import pytest

MOCK_HOST = "127.0.0.1"
MOCK_USER = "user"
MOCK_PASS = "pass"
URL_TEMPLATE = "http://{}:{}@{}:80{}"


@pytest.fixture
def mock_aioresponse():
    with aioresponses() as m:
        yield m


@pytest.mark.asyncio
async def test_ready(mock_aioresponse: aioresponses) -> None:
    with open("tests/info.json") as f:
        mock_aioresponse.get(
            URL_TEMPLATE.format(MOCK_USER, MOCK_PASS, MOCK_HOST, "/bha-api/info.cgi"),
            body=f.read(),
        )

    db = DoorBird(MOCK_HOST, MOCK_USER, MOCK_PASS)
    ready, code = await db.ready()
    assert ready is True
    assert code == 200
    await db.close()


@pytest.mark.asyncio
async def test_get_image(mock_aioresponse: aioresponses) -> None:
    db = DoorBird(MOCK_HOST, MOCK_USER, MOCK_PASS)
    url = db.live_image_url
    mock_aioresponse.get(
        url,
        body=b"jpeg",
    )

    image_bytes = await db.get_image(url)
    assert image_bytes == b"jpeg"
    await db.close()


@pytest.mark.asyncio
async def test_http_url():
    db = DoorBird(MOCK_HOST, MOCK_USER, MOCK_PASS)
    url = db._url(
        path="/test",
        args=[
            ("arg1", "value1"),
            ("arg2", "value2"),
        ],
    )
    assert (
        url
        == f"http://{MOCK_USER}:{MOCK_PASS}@{MOCK_HOST}:80/test?arg1=value1&arg2=value2"
    )


@pytest.mark.asyncio
async def test_http_url_custom_port():
    db = DoorBird(MOCK_HOST, MOCK_USER, MOCK_PASS, port=8080)
    url = db._url("/test")
    assert url == f"http://{MOCK_USER}:{MOCK_PASS}@{MOCK_HOST}:8080/test"


@pytest.mark.asyncio
async def test_https_url():
    db = DoorBird(MOCK_HOST, MOCK_USER, MOCK_PASS, secure=True)
    url = db._url("/test")
    assert url == f"https://{MOCK_USER}:{MOCK_PASS}@{MOCK_HOST}:443/test"


@pytest.mark.asyncio
async def test_https_url_custom_port():
    db = DoorBird(MOCK_HOST, MOCK_USER, MOCK_PASS, secure=True, port=8443)
    url = db._url("/test")
    assert url == f"https://{MOCK_USER}:{MOCK_PASS}@{MOCK_HOST}:8443/test"


@pytest.mark.asyncio
async def test_rtsp_url():
    db = DoorBird(MOCK_HOST, MOCK_USER, MOCK_PASS)
    assert db.rtsp_live_video_url.startswith(
        f"rtsp://{MOCK_USER}:{MOCK_PASS}@{MOCK_HOST}:554"
    )


@pytest.mark.asyncio
async def test_rtsp_http_url():
    db = DoorBird(MOCK_HOST, MOCK_USER, MOCK_PASS)
    assert db.rtsp_over_http_live_video_url.startswith(
        f"rtsp://{MOCK_USER}:{MOCK_PASS}@{MOCK_HOST}:8557"
    )


@pytest.mark.asyncio
async def test_energize_relay(mock_aioresponse: aioresponses) -> None:
    mock_aioresponse.get(
        URL_TEMPLATE.format(
            MOCK_USER, MOCK_PASS, MOCK_HOST, "/bha-api/open-door.cgi?r=1"
        ),
        body='{"BHA": {"RETURNCODE": "1"}}',
    )

    db = DoorBird(MOCK_HOST, MOCK_USER, MOCK_PASS)
    assert await db.energize_relay() is True
    await db.close()


@pytest.mark.asyncio
async def test_turn_light_on(mock_aioresponse: aioresponses) -> None:
    mock_aioresponse.get(
        URL_TEMPLATE.format(MOCK_USER, MOCK_PASS, MOCK_HOST, "/bha-api/light-on.cgi"),
        body='{"BHA": {"RETURNCODE": "1"}}',
    )

    db = DoorBird(MOCK_HOST, MOCK_USER, MOCK_PASS)
    assert await db.turn_light_on() is True
    await db.close()


@pytest.mark.asyncio
async def test_schedule(mock_aioresponse: aioresponses) -> None:
    with open("tests/schedule.json") as f:
        mock_aioresponse.get(
            URL_TEMPLATE.format(
                MOCK_USER, MOCK_PASS, MOCK_HOST, "/bha-api/schedule.cgi"
            ),
            body=f.read(),
        )

    db = DoorBird(MOCK_HOST, MOCK_USER, MOCK_PASS)
    assert len(await db.schedule()) == 3
    await db.close()


@pytest.mark.asyncio
async def test_get_schedule_entry(mock_aioresponse: aioresponses) -> None:
    with open("tests/schedule_get_entry.json") as f:
        mock_aioresponse.get(
            URL_TEMPLATE.format(
                MOCK_USER, MOCK_PASS, MOCK_HOST, "/bha-api/schedule.cgi"
            ),
            body=f.read(),
        )

    db = DoorBird(MOCK_HOST, MOCK_USER, MOCK_PASS)
    assert isinstance(
        await db.get_schedule_entry("doorbell", "1"), DoorBirdScheduleEntry
    )
    await db.close()


@pytest.mark.asyncio
async def test_change_schedule_entry(mock_aioresponse: aioresponses) -> None:
    with open("tests/schedule_get_entry.json") as f:
        mock_aioresponse.get(
            URL_TEMPLATE.format(
                MOCK_USER, MOCK_PASS, MOCK_HOST, "/bha-api/schedule.cgi"
            ),
            body=f.read(),
        )

    db = DoorBird(MOCK_HOST, MOCK_USER, MOCK_PASS)
    entry = await db.get_schedule_entry("doorbell", "1")
    assert entry.output[0].enabled is True
    entry.param = "5"
    mock_aioresponse.post(
        URL_TEMPLATE.format(MOCK_USER, MOCK_PASS, MOCK_HOST, "/bha-api/schedule.cgi"),
    )
    await db.change_schedule(entry)
    mock_aioresponse.assert_called_with(
        url=URL_TEMPLATE.format(
            MOCK_USER, MOCK_PASS, MOCK_HOST, "/bha-api/schedule.cgi"
        ),
        method="POST",
        **{
            "json": entry.export,
            "timeout": 10.0,
            "headers": {"Content-Type": "application/json"},
            "allow_redirects": True,
        },
    )
    await db.close()


@pytest.mark.asyncio
async def test_doorbell_state_false(mock_aioresponse: aioresponses) -> None:
    mock_aioresponse.get(
        URL_TEMPLATE.format(
            MOCK_USER, MOCK_PASS, MOCK_HOST, "/bha-api/monitor.cgi?check=doorbell"
        ),
        body="doorbell=0\r\n",
    )

    db = DoorBird(MOCK_HOST, MOCK_USER, MOCK_PASS)
    assert await db.doorbell_state() is False
    await db.close()


@pytest.mark.asyncio
async def test_doorbell_state_true(mock_aioresponse: aioresponses) -> None:
    mock_aioresponse.get(
        URL_TEMPLATE.format(
            MOCK_USER, MOCK_PASS, MOCK_HOST, "/bha-api/monitor.cgi?check=doorbell"
        ),
        body="doorbell=1\r\n",
    )

    db = DoorBird(MOCK_HOST, MOCK_USER, MOCK_PASS)
    assert await db.doorbell_state() is True
    await db.close()


@pytest.mark.asyncio
async def test_motion_sensor_state_false(mock_aioresponse: aioresponses) -> None:
    mock_aioresponse.get(
        URL_TEMPLATE.format(
            MOCK_USER, MOCK_PASS, MOCK_HOST, "/bha-api/monitor.cgi?check=motionsensor"
        ),
        body="motionsensor=0\r\n",
    )

    db = DoorBird(MOCK_HOST, MOCK_USER, MOCK_PASS)
    assert await db.motion_sensor_state() is False
    await db.close()


@pytest.mark.asyncio
async def test_motion_sensor_state_true(mock_aioresponse: aioresponses) -> None:
    mock_aioresponse.get(
        URL_TEMPLATE.format(
            MOCK_USER, MOCK_PASS, MOCK_HOST, "/bha-api/monitor.cgi?check=motionsensor"
        ),
        body="motionsensor=1\r\n",
    )

    db = DoorBird(MOCK_HOST, MOCK_USER, MOCK_PASS)
    assert await db.motion_sensor_state() is True
    await db.close()


@pytest.mark.asyncio
async def test_info(mock_aioresponse: aioresponses) -> None:
    with open("tests/info.json") as f:
        mock_aioresponse.get(
            URL_TEMPLATE.format(MOCK_USER, MOCK_PASS, MOCK_HOST, "/bha-api/info.cgi"),
            body=f.read(),
        )

    db = DoorBird(MOCK_HOST, MOCK_USER, MOCK_PASS)
    data = await db.info()
    assert data == {
        "BUILD_NUMBER": "15870439",
        "DEVICE-TYPE": "DoorBird D2101V",
        "FIRMWARE": "000125",
        "RELAYS": [
            "1",
            "2",
            "ghchdi@1",
            "ghchdi@2",
            "ghchdi@3",
            "ghdwkh@1",
            "ghdwkh@2",
            "ghdwkh@3",
        ],
        "WIFI_MAC_ADDR": "1234ABCD",
    }
    await db.close()


@pytest.mark.asyncio
async def test_info_auth_fails(mock_aioresponse: aioresponses) -> None:
    mock_aioresponse.get(
        URL_TEMPLATE.format(MOCK_USER, MOCK_PASS, MOCK_HOST, "/bha-api/info.cgi"),
        status=401,
    )

    db = DoorBird(MOCK_HOST, MOCK_USER, MOCK_PASS)
    with pytest.raises(ClientResponseError):
        await db.info()
    await db.close()


@pytest.mark.asyncio
async def test_reset(mock_aioresponse: aioresponses) -> None:
    mock_aioresponse.get(
        URL_TEMPLATE.format(MOCK_USER, MOCK_PASS, MOCK_HOST, "/bha-api/restart.cgi"),
    )

    db = DoorBird(MOCK_HOST, MOCK_USER, MOCK_PASS)
    assert await db.restart() is True
    await db.close()
