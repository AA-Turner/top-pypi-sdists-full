#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import json

from requests import Response
from requests import request as _request

from .exception import UnSupportVersionError
from .signature import SignatureImpl


class HttpClient:
    def __init__(self, api_key: str = None, api_secret: str = None, recv_window: int = 50000) -> None:
        self.api_key = api_key
        self.api_secret = api_secret
        self.recv_window = recv_window

        if api_key and api_secret:
            self.signimpl = SignatureImpl(self.api_key, self.api_secret, self.recv_window)

    def request(self, method: str, url: str, params_or_body: dict = None, **kwargs) -> Response:
        method = method.lower()
        is_private: bool = HttpClient.is_private(url)

        if "/v3" in url:
            if method == "get":
                if is_private:
                    sign = self.signimpl.generate(method, url, params_or_body)
                    headers = self.signimpl.get_auth_headers(sign)
            else:
                sign = self.signimpl.generate(method, url, params_or_body)
                headers = self.signimpl.get_auth_headers(sign)
            return _request(method, url, data=json.dumps(params_or_body), headers=headers, **kwargs)

        elif "/v5" in url:
            if method == "get":
                sign = self.signimpl.generate(method, url, params_or_body) if is_private else None
                headers = self.signimpl.get_auth_headers(sign)
                return _request(method, url, params=params_or_body, headers=headers, **kwargs)
            else:
                sign = self.signimpl.generate(method, url, params_or_body)
                headers = self.signimpl.get_auth_headers(sign)
                return _request(method, url, data=json.dumps(params_or_body), headers=headers, **kwargs)
        else:
            raise UnSupportVersionError(f"Unrecognized request url: {url}")

    @staticmethod
    def is_private(url) -> bool:
        need_auth = False
        if "/v5/" in url:
            # exclude path like `/orderbook/`
            if "/position/" in url or "/order/" in url or "/execution/" in url:
                need_auth = True
        elif "private" in url:
            need_auth = True

        return need_auth
