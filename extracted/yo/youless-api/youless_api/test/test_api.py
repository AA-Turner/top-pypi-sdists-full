import unittest
from datetime import datetime
from unittest.mock import patch, Mock, MagicMock

from requests import Response

from youless_api import YoulessAPI

test_host = "192.1.1.1"


def mock_ls120_pvoutput(*args, **kwargs) -> Response:
    if args[0] == 'http://192.1.1.1/d':
        return Mock(
            ok=True,
            json=lambda: {'mac': '293:23fd:23'}
        )

    if args[0] == 'http://192.1.1.1/e':
        return Mock(
            ok=True,
            headers={'Content-Type': 'text/html'}
        )

    if args[0] == 'http://192.1.1.1/a?f=j':
        return Mock(
            ok=True,
            json=lambda: {
                "cnt": "141950,625",
                "pwr": 750,
                "lvl": 90,
                "dev": "(&plusmn;3%)",
                "det": "",
                "con": "OK",
                "sts": "(33)",
                "raw": 743
            })

    return Mock(ok=False)


def mock_ls120(*args, **kwargs) -> Response:
    if args[0] == 'http://192.1.1.1/d':
        return Mock(
            ok=True,
            json=lambda: {'mac': '293:23fd:23', 'fw': '1.6.0-EL'}
        )

    if args[0] == 'http://192.1.1.1/e':
        return Mock(
            ok=True,
            headers={'Content-Type': 'application/json'},
            json=lambda: [{
                "tm": 1611929119,
                "net": 9194.164,
                "pwr": 2382,
                "ts0": 1608654000,
                "cs0": 15.000,
                "ps0": 10,
                "p1": 4703.562,
                "p2": 4490.631,
                "n1": 0.029,
                "n2": 0.000,
                "gas": 1624.264,
                "gts": int(datetime.now().strftime("%y%m%d%H00")),
                "wtr": 1234.564,
                "wts": int(datetime.now().strftime("%y%m%d%H00"))
            }])

    if args[0] == 'http://192.1.1.1/f':
        return Mock(
            ok=True,
            json=lambda: {
                "tr": 1,
                "i1": 0.123,
                "v1": 240,
                "l1": 462,
                "v2": 240,
                "l2": 230,
                "i2": 0.123,
                "v3": 240,
                "l3": 230,
                "i3": 0.123,
                "pp": 1200,
                "pts": int(datetime.now().strftime("%y%m%d%H%M")),
                "pa": 400
            }
        )

    return Mock(ok=False)


def mock_ls120_reported(*args, **kwargs) -> Response:
    if args[0] == 'http://192.1.1.1/d':
        return Mock(
            ok=True,
            json=lambda: {'mac': '293:23fd:23', 'fw': '1.6.0-EL'}
        )

    if args[0] == 'http://192.1.1.1/e':
        return Mock(
            ok=True,
            headers={'Content-Type': 'application/json'},
            json=lambda: [{
                "tm": 1719966932,
                "net": 24277.256,
                "pwr": -6,
                "ts0": 1719964559,
                "cs0": 75.271,
                "ps0": 0,
                "p1": 13775.844,
                "p2": 12057.301,
                "n1": 439.157,
                "n2": 1116.732,
                "gas": 3754.789,
                "gts":int(datetime.now().strftime("%y%m%d%H00")),
                "wtr": 0.000,
                "wts": 0
            }])

    if args[0] == 'http://192.1.1.1/f':
        return Mock(
            ok=True,
            json=lambda: {
                "tr": 2,
                "pa": 0,
                "pp": 0,
                "pts": 0,
                "i1": 1.000,
                "i2": 2.000,
                "i3": 1.000,
                "v1": 233.900,
                "v2": 232.400,
                "v3": 233.600,
                "l1": 50,
                "l2": 199,
                "l3": -218}
        )

    return Mock(ok=False)


def mock_ls110_device(*args, **kwargs):
    if args[0] == 'http://192.1.1.1/d':
        return Mock(ok=False)
    if args[0] == 'http://192.1.1.1/a?f=j':
        return Mock(
            ok=True,
            json=lambda: {
                "cnt": "141950,625",
                "pwr": 750,
                "lvl": 90,
                "dev": "(&plusmn;3%)",
                "det": "",
                "con": "OK",
                "sts": "(33)",
                "raw": 743
            })

    return Mock(ok=False)


class YoulessAPITest(unittest.TestCase):

    @patch('youless_api.gateway.requests.get', side_effect=mock_ls120)
    def test_device_ls120(self, mock_get: MagicMock):
        api = YoulessAPI(test_host)
        api.initialize()
        api.update()

        self.assertEqual(api.model, 'LS120')
        self.assertEqual(api.mac_address, '293:23fd:23')
        self.assertEqual(api.firmware_version, '1.6.0-EL')
        self.assertEqual(api.current_tariff, 1)

        self.assertEqual(api.water_meter.value, 1234.564)
        self.assertEqual(api.extra_meter.total.value, 15.0)
        self.assertEqual(api.extra_meter.usage.value, 10)
        self.assertEqual(api.delivery_meter.low.value, 0.029)
        self.assertEqual(api.delivery_meter.high.value, 0.0)
        self.assertEqual(api.gas_meter.value, 1624.264)
        self.assertEqual(api.current_power_usage.value, 2382)
        self.assertEqual(api.power_meter.high.value, 4490.631)
        self.assertEqual(api.power_meter.low.value, 4703.562)
        self.assertEqual(9194.164, api.power_meter.total.value)
        self.assertEqual(400, api.average_power.value)
        self.assertEqual(1200, api.peak_power.value)
        self.assertEqual(datetime.now().replace(second=0, microsecond=0), api.peak_power_time)

        mock_get.assert_any_call('http://192.1.1.1/d', auth=None, timeout=2)
        mock_get.assert_any_call('http://192.1.1.1/e', auth=None, timeout=2)
        mock_get.assert_any_call('http://192.1.1.1/f', auth=None, timeout=2)

    @patch('youless_api.gateway.requests.get', side_effect=mock_ls120_reported)
    def test_device_ls120_reported_issues(self, mock_get: MagicMock):
        api = YoulessAPI(test_host)
        api.initialize()
        api.update()

        self.assertEqual(api.extra_meter.total.value, 75.271)
        self.assertEqual(api.extra_meter.usage.value, 0)

    @patch('youless_api.gateway.requests.get', side_effect=mock_ls120)
    def test_device_ls120_authenticated(self, mock_get: MagicMock):
        api = YoulessAPI(test_host, 'admin', 'password')
        api.initialize()

        self.assertEqual(api.model, 'LS120')
        mock_get.assert_any_call('http://192.1.1.1/d', auth=('admin', 'password'), timeout=2)
        mock_get.assert_any_call('http://192.1.1.1/e', auth=('admin', 'password'), timeout=2)

    @patch('youless_api.gateway.requests.get', side_effect=mock_ls120_pvoutput)
    def test_ls120_firmare_pvoutput(self, mock_get: MagicMock):
        api = YoulessAPI(test_host)
        api.initialize()
        api.update()

        self.assertEqual(api.model, 'LS120 - PVOutput')
        self.assertEqual(api.mac_address, '293:23fd:23')
        mock_get.assert_any_call('http://192.1.1.1/d', auth=None, timeout=2)
        mock_get.assert_any_call('http://192.1.1.1/e', auth=None, timeout=2)

    @patch('youless_api.gateway.requests.get', side_effect=mock_ls120_pvoutput)
    def test_ls120_firmare_pvoutput_authenticated(self, mock_get: MagicMock):
        api = YoulessAPI(test_host, 'admin', 'password')
        api.initialize()

        self.assertEqual(api.model, 'LS120 - PVOutput')
        self.assertEqual(api.mac_address, '293:23fd:23')
        mock_get.assert_any_call('http://192.1.1.1/d', auth=('admin', 'password'), timeout=2)
        mock_get.assert_any_call('http://192.1.1.1/e', auth=('admin', 'password'), timeout=2)

    @patch('youless_api.gateway.requests.get', side_effect=mock_ls110_device)
    def test_device_ls110(self, mock_get: MagicMock):
        api = YoulessAPI(test_host)
        api.initialize()

        mock_get.assert_called_with('http://192.1.1.1/d', auth=None, timeout=2)
        self.assertEqual(api.model, 'LS110')
        self.assertIsNone(api.mac_address)

        api.update()
        mock_get.assert_called_with('http://192.1.1.1/a?f=j', auth=None, timeout=2)

    @patch('youless_api.gateway.requests.get', side_effect=mock_ls110_device)
    def test_device_ls110_authenticated(self, mock_get: MagicMock):
        api = YoulessAPI(test_host, 'admin', 'password')
        api.initialize()
        mock_get.assert_called_with('http://192.1.1.1/d', auth=('admin', 'password'), timeout=2)

        self.assertEqual(api.model, 'LS110')
        self.assertIsNone(api.mac_address)
