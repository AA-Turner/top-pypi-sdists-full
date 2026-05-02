import os
import sys
import tempfile
import unittest

from aiohttp import web

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from cpsl.msg import Attachment


class AttachmentTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        async def handle(_request):
            return web.Response(body=b"hello from attachment", content_type="text/plain")

        self.app = web.Application()
        self.app.router.add_get("/file.txt", handle)
        self.runner = web.AppRunner(self.app)
        await self.runner.setup()
        self.site = web.TCPSite(self.runner, "127.0.0.1", 0)
        await self.site.start()
        sock = self.site._server.sockets[0]
        self.base_url = f"http://127.0.0.1:{sock.getsockname()[1]}"

    async def asyncTearDown(self):
        await self.runner.cleanup()

    async def test_download_fetches_attachment_url(self):
        attachment = Attachment(
            name="file.txt",
            content_type="text/plain",
            url=f"{self.base_url}/file.txt",
            size=21,
        )
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, attachment.name)
            got = await attachment.download(path)

            self.assertEqual(got, path)
            with open(path, "rb") as f:
                self.assertEqual(f.read(), b"hello from attachment")
