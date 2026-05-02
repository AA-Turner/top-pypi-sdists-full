#g4fp.py
import asyncio
import random
import requests
import aiohttp
from g4f.client import Client, AsyncClient
import asyncio

def fetch_proxy_list(debug=False, proxy_fetch_url=None):
    try:
        response = requests.get(proxy_fetch_url)
        if response.status_code == 200:
            proxies = response.text.strip().splitlines()
            proxies = [p.strip() for p in proxies if p.strip()]
            if debug:
                print(f"[DEBUG] Fetched proxies")
            return proxies
        else:
            if debug:
                print(f"[ERROR] Failed to fetch proxy list, status code: {response.status_code}")
    except Exception as e:
        if debug:
            print(f"[ERROR] Exception fetching proxy list: {e}")
    return []

def get_random_proxy(debug=False, proxy_fetch_url=None):
    proxies = fetch_proxy_list(debug, proxy_fetch_url)
    if not proxies:
        raise Exception("No proxies available")
    return random.choice(proxies)

async def fetch_proxy_list_async(debug=False, proxy_fetch_url=None):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(proxy_fetch_url) as response:
                if response.status == 200:
                    text = await response.text()
                    proxies = text.strip().splitlines()
                    proxies = [p.strip() for p in proxies if p.strip()]
                    if debug:
                        print(f"[DEBUG] Fetched proxies")
                    return proxies
                else:
                    if debug:
                        print(f"[ERROR] Failed to fetch proxy list, status code: {response.status}")
    except Exception as e:
        if debug:
            print(f"[ERROR] Exception fetching proxy list: {e}")
    return []

async def get_random_proxy_async(debug=False, proxy_fetch_url=None):
    proxies = await fetch_proxy_list_async(debug, proxy_fetch_url)
    if not proxies:
        raise Exception("No proxies available")
    return random.choice(proxies)

class _ProxyWrapper:
    def __init__(self, wrapped_obj, debug=False, proxy_fetch_url=None):
        self._wrapped = wrapped_obj
        self.debug = debug
        self.proxy_fetch_url = proxy_fetch_url

    def __getattr__(self, name):
        attr = getattr(self._wrapped, name)
        if callable(attr):
            def method_wrapper(*args, **kwargs):
                t = 0
                while t < 5:
                    try:
                        proxy = get_random_proxy(self.debug, self.proxy_fetch_url)
                        if self.debug:
                            print(f"[DEBUG] Using proxy: {proxy}")
                        kwargs["proxies"] = "http://" + proxy
                        result = attr(*args, **kwargs)
                        if self.debug:
                            print("[SUCCESS]")
                        return result
                    except Exception as e:
                        if self.debug:
                            print(f"[ERROR] {e}")
                        continue
            return method_wrapper
        elif hasattr(attr, '__dict__'):
            return _ProxyWrapper(attr, self.debug, self.proxy_fetch_url)
        else:
            return attr

class _AsyncProxyWrapper:
    def __init__(self, wrapped_obj, debug=False, proxy_fetch_url=None):
        self._wrapped = wrapped_obj
        self.debug = debug
        self.proxy_fetch_url = proxy_fetch_url

    def __getattr__(self, name):
        attr = getattr(self._wrapped, name)
        if callable(attr):
            async def method_wrapper(*args, **kwargs):
                t = 0
                while t < 5:
                    try:
                        proxy = await get_random_proxy_async(self.debug, self.proxy_fetch_url)
                        if self.debug:
                            print(f"[DEBUG] Using proxy: {proxy}")
                        kwargs["proxies"] = "http://" + proxy
                        result = attr(*args, **kwargs)
                        if asyncio.iscoroutine(result):
                            result = await result
                        if self.debug:
                            print("[SUCCESS]")
                        return result
                    except Exception as e:
                        if self.debug:
                            print(f"[ERROR] {e}")
                        continue
            return method_wrapper
        elif hasattr(attr, '__dict__'):
            return _AsyncProxyWrapper(attr, self.debug, self.proxy_fetch_url)
        else:
            return attr

def ClientProxy(debug=False, proxy_fetch_url=None):
    original_client = Client()
    return _ProxyWrapper(original_client, debug, proxy_fetch_url)

async def AsyncClientProxy(debug=False, proxy_fetch_url=None):
    original_async_client = AsyncClient()
    return _AsyncProxyWrapper(original_async_client, debug, proxy_fetch_url)
