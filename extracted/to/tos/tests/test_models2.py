# -*- coding: utf-8 -*-

import unittest

from requests.structures import CaseInsensitiveDict

from tos.exceptions import TosServerError
from tos.models2 import CopyObjectOutput, FetchObjectOutput


class FakeJsonResponse(object):
    def __init__(self, data, status=200):
        self._data = data
        self.status = status
        self.headers = CaseInsensitiveDict({'x-tos-request-id': 'request-id'})
        self.request_id = 'request-id'

    def json_read(self):
        return self._data


class Models2OutputTestCase(unittest.TestCase):
    def test_copy_object_output_requires_etag(self):
        resp = FakeJsonResponse({'Code': 'InternalError', 'Message': 'copy failed'})

        with self.assertRaises(TosServerError):
            CopyObjectOutput(resp)

    def test_fetch_object_output_requires_etag(self):
        resp = FakeJsonResponse({'Code': 'InternalError', 'Message': 'fetch failed'})

        with self.assertRaises(TosServerError):
            FetchObjectOutput(resp)

    def test_copy_object_output_accepts_etag(self):
        resp = FakeJsonResponse({'ETag': '"etag"', 'LastModified': '2021-01-01T00:00:00.000Z'})

        out = CopyObjectOutput(resp)

        self.assertEqual(out.etag, 'etag')

    def test_fetch_object_output_accepts_etag(self):
        resp = FakeJsonResponse({'ETag': '"etag"'})

        out = FetchObjectOutput(resp)

        self.assertEqual(out.etag, 'etag')


if __name__ == '__main__':
    unittest.main()
