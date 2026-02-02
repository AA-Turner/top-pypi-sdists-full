import httpx
import os

from ytSearch.core.constants import userAgent

class RequestCore:
    def __init__(self):
        self.url = None
        self.data = None
        self.timeout = 2
        self.proxy = {}
        http_proxy = os.environ.get("HTTP_PROXY")
        if http_proxy:
            self.proxy["http://"] = http_proxy
        https_proxy = os.environ.get("HTTPS_PROXY")
        if https_proxy:
            self.proxy["https://"] = https_proxy

    def syncPostRequest(self) -> httpx.Response:
        proxy_url = self.proxy.get("https://") or self.proxy.get("http://") if self.proxy else None
        return httpx.post(
            self.url,
            headers={"User-Agent": userAgent},
            json=self.data,
            timeout=self.timeout,
            proxy=proxy_url
        )

    async def asyncPostRequest(self) -> httpx.Response:
        proxy_url = self.proxy.get("https://") or self.proxy.get("http://") if self.proxy else None
        async with httpx.AsyncClient(proxy=proxy_url) as client:
            r = await client.post(self.url, headers={"User-Agent": userAgent}, json=self.data, timeout=self.timeout)
            return r

    def syncGetRequest(self) -> httpx.Response:
        proxy_url = self.proxy.get("https://") or self.proxy.get("http://") if self.proxy else None
        return httpx.get(self.url, headers={"User-Agent": userAgent}, timeout=self.timeout, cookies={'CONSENT': 'YES+1'}, proxy=proxy_url)

    async def asyncGetRequest(self) -> httpx.Response:
        proxy_url = self.proxy.get("https://") or self.proxy.get("http://") if self.proxy else None
        async with httpx.AsyncClient(proxy=proxy_url) as client:
            r = await client.get(self.url, headers={"User-Agent": userAgent}, timeout=self.timeout, cookies={'CONSENT': 'YES+1'})
            return r
