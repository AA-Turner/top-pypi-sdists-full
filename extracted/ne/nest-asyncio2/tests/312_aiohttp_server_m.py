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
import warnings
warnings.filterwarnings("default")

import asyncio
import nest_asyncio2
from aiohttp import web

with warnings.catch_warnings(record=True) as w:
    nest_asyncio2.apply()
    assert len(w) == 0, w

async def f_async():
    routes = web.RouteTableDef()

    @routes.get('/')
    async def hello(request):
        return web.Response(text="Hello, world")

    app = web.Application()
    app.add_routes(routes)
    web.run_app(app)

def f():
    nest_asyncio2.apply()
    asyncio.run(f_async())

async def main():
    f()

with warnings.catch_warnings(record=True) as w:
    asyncio.run(main())
    assert len(w) == 0, w
