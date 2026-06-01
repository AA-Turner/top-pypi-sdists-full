import asyncio
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn


class _HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        if self.path == "/health":
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"OK")
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format: str, *args: object) -> None:
        pass  # Suppress health check request logging


class HealthServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True

    def __init__(self, host: str, port: int):
        super().__init__((host, port), _HealthCheckHandler)

    async def run(self) -> None:
        await asyncio.get_event_loop().run_in_executor(None, self.serve_forever)
