import json
from unittest import TestCase
from unittest.mock import Mock, patch

from pycarlo.common import http


class S3UtilsTests(TestCase):
    @patch("pycarlo.common.http.requests")
    def test_upload_bytes(self, mock_requests: Mock):
        # given
        url = "http://upload.com"
        content = b"test"

        # when
        http.upload(url, content)

        # then
        mock_requests.request.assert_called_once_with(method="post", url=url, data=content)

    @patch("pycarlo.common.http.requests")
    def test_upload_dict(self, mock_requests: Mock):
        # given
        url = "http://upload.com"
        content = {"foo": "bar"}

        # when
        http.upload(url, content)

        # then
        mock_requests.request.assert_called_once_with(
            method="post", url=url, data=json.dumps(content).encode("utf-8")
        )

    @patch("pycarlo.common.http.requests")
    def test_upload_str(self, mock_requests: Mock):
        # given
        url = "http://upload.com"
        content = "test"
        method = "put"

        # when
        http.upload(url, content, method=method)

        # then
        mock_requests.request.assert_called_once_with(
            method=method, url=url, data=content.encode("utf-8")
        )
