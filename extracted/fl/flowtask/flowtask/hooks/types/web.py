from aiohttp import web
from .http import HTTPHook


class WebHook(HTTPHook):
    """WebHook.

    Can be used to receive data from a web URL.
    """

    methods: list = ["GET", "POST"]

    async def get(self, request: web.Request):
        data = self.query_parameters(request)
        result = await self.run_actions(**dict(data))
        return self.response(
            response=result,
            status=self.default_status
        )

    async def post(self, request: web.Request):
        # TODO: deal with post data or JSON payloads:
        data = await self.json_data(request)
        result = await self.run_actions(**dict(data))
        return self.response(
            response=result,
            status=self.default_status
        )

    async def put(self, request: web.Request):
        data = await self.json_data(request)
        result = await self.run_actions(**dict(data))
        return self.response(
            response=result,
            status=self.default_status
        )
