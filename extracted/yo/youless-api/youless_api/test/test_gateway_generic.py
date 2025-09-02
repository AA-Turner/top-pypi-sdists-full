from unittest import TestCase
from unittest.mock import patch, Mock, MagicMock

from requests import Response

from youless_api.gateway import fetch_generic_api


def mock_generic_ok(*args, **kwargs) -> Response:
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


class GatewayGenericTest(TestCase):

    @patch('youless_api.gateway.requests.get', side_effect=mock_generic_ok)
    def test_generic_ok(self, mock_get: MagicMock):
        dataset = fetch_generic_api('localhost', None)

        self.assertEqual(dataset['cnt'], 141950.625)
        self.assertEqual(dataset['pwr'], 750)
        self.assertEqual(dataset['lvl'], 90)
        self.assertEqual(dataset['dev'], '(&plusmn;3%)')
        self.assertEqual(dataset['det'], "")
        self.assertEqual(dataset['con'], 'OK')
        self.assertEqual(dataset['sts'], "(33)")
        self.assertEqual(dataset['raw'], 743)

        mock_get.assert_any_call('http://localhost/a?f=j', auth=None, timeout=2)
