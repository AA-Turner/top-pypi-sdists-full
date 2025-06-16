import chargehound
import requests_mock
import unittest2


class ApiRequestorTest(unittest2.TestCase):

    def setUp(self):
        super(ApiRequestorTest, self).setUp()
        chargehound.api_key = 'API_KEY'

    @requests_mock.mock()
    def test_response_status(self, mock):
        mock.get('https://api.chargehound.com/v1/disputes/dp_123',
                 json={'id': 'dp_123'})
        dispute = chargehound.Disputes.retrieve('dp_123')
        assert dispute.response.status == 200
