# /// script
# requires-python = ">=3.5"
# dependencies = [
#     "aiohttp",
#     "nest-asyncio2",
# ]
#
# [tool.uv.sources]
# nest-asyncio2 = { path = "../", editable = true }
# ///
import unittest
import warnings
warnings.filterwarnings("default")

import asyncio
import nest_asyncio2
from aiohttp import web

with warnings.catch_warnings(record=True) as w:
    nest_asyncio2.apply()
    assert len(w) == 0, w

from aiohttp.test_utils import AioHTTPTestCase
from aiohttp import web

class MyAppTestCase(AioHTTPTestCase):
    async def get_application(self):
        """
        Override the get_app method to return your application.
        """
        async def hello(request):
            return web.Response(text='Hello, world')

        app = web.Application()
        app.router.add_get('/', hello)
        return app

    async def test_async(self):
        async with self.client.request("GET", "/") as resp:
            self.assertEqual(resp.status, 200)
            text = await resp.text()
        self.assertIn("Hello, world", text)

    def test(self):
        asyncio.run(self.test_async())

if __name__ == '__main__':
    with warnings.catch_warnings(record=True) as w:
        unittest.main()
        assert len(w) == 0, w
