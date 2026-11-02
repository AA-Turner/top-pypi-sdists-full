"""Shared small classes."""
from __future__ import annotations


class RequestView:
    """The two things fitevict's KeyAuth reads from a request (client address and
    headers), for an aiohttp request."""

    def __init__(self, request):
        self.client_address = (request.remote or "", 0)
        self.headers = request.headers
