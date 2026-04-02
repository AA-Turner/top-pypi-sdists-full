from unittest.mock import Mock, patch

from bravado.exception import HTTPInternalServerError

from eveuniverse.core import esitools
from eveuniverse.tests.testdata.esi import EsiClientStub
from eveuniverse.utils import NoSocketsTestCase


@patch("eveuniverse.core.esitools.esi")
class TestIsEsiOnline(NoSocketsTestCase):
    def test_is_online(self, mock_esi):
        mock_esi.client = EsiClientStub()

        self.assertTrue(esitools.is_esi_online())

    def test_is_offline(self, mock_esi):
        mock_esi.client.Status.get_status.side_effect = HTTPInternalServerError(
            Mock(**{"response.status_code": 500})
        )

        self.assertFalse(esitools.is_esi_online())

    def test_str_response(self, mock_esi):
        mock_esi.client.Status.get_status.return_value.results.return_value = "error"

        self.assertFalse(esitools.is_esi_online())
