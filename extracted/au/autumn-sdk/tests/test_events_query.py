import json
import unittest

import httpx
import zstandard
from autumn_sdk import Autumn, models


class EventsQueryTests(unittest.IsolatedAsyncioTestCase):
    async def test_sync_and_async_streams_preserve_precise_values(self):
        lines = [
            {"type": "columns", "columns": [{"name": "count", "type": "UInt64"}]},
            {"type": "row", "values": ["18446744073709551615"]},
            {"type": "end", "rows": 1, "truncated": False, "stopped_by": None},
        ]
        compressed = zstandard.compress(
            ("\n".join(json.dumps(line) for line in lines) + "\n").encode()
        )

        def respond(request):
            self.assertEqual(request.url.path, "/v1/events.query")
            self.assertEqual(json.loads(request.content), {"sql": "SELECT count() FROM events"})
            self.assertIn("zstd", request.headers["accept-encoding"])
            return httpx.Response(
                200,
                headers={"content-type": "application/x-ndjson", "content-encoding": "zstd"},
                content=compressed,
            )

        transport = httpx.MockTransport(respond)
        with httpx.Client(transport=transport) as client:
            async with httpx.AsyncClient(transport=transport) as async_client:
                autumn = Autumn(
                    secret_key="test-key",
                    server_url="https://autumn.test",
                    client=client,
                    async_client=async_client,
                )
                result = autumn.events.query(sql="SELECT count() FROM events")
                self.assertIsInstance(result, models.QueryEventsResponse)
                try:
                    self.assertEqual([json.loads(line) for line in result.result.iter_lines()], lines)
                finally:
                    result.result.close()
                result = await autumn.events.query_async(sql="SELECT count() FROM events")
                try:
                    self.assertEqual([json.loads(line) async for line in result.result.aiter_lines()], lines)
                finally:
                    await result.result.aclose()
