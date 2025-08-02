import socket
import threading
import uvicorn
from fastapi import FastAPI, Request
from starlette.responses import HTMLResponse
import asyncio
import os
import time

# Default port for OAuth callback server
PORT = int(os.getenv("ORBY_PORT", 2626))
# Default host (localhost) for OAuth callback server
HOST = "localhost"


class OAuthCallbackServer:
    def __init__(self, port: int = PORT, host: str = HOST):
        self.port = port
        self.host = host
        self.code = None
        self.app = FastAPI()
        self._setup_routes()
        self._server = None
        self._thread = None
        self._code_received = False

    def _setup_routes(self):
        @self.app.get("/oauth/callback", response_class=HTMLResponse)
        async def handle_callback(request: Request):
            self.code = request.query_params.get("code")
            self._code_received = True

            # TODO: Redirect to an auth success page
            return """
                <html>
                    <head>
                        <title>Authorization Complete</title>
                        <style>
                            body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
                            .success { color: green; }
                        </style>
                    </head>
                    <body>
                        <h1 class="success">✅ Authentication successful!</h1>
                        <p>You may now close this window and return to the terminal.</p>
                    </body>
                </html>
            """

    def _is_port_available(self) -> bool:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind((self.host, self.port))
                return True
            except Exception:
                return False

    def start(self):
        if not self._is_port_available():
            raise RuntimeError(f"Port {self.port} is already in use")

        config = uvicorn.Config(
            self.app,
            host=self.host,
            port=self.port,
            log_level="error",  # Minimal logging
            access_log=False,
        )
        self._server = uvicorn.Server(config)

        def run_server():
            asyncio.run(self._server.serve())

        self._thread = threading.Thread(target=run_server, daemon=True)
        self._thread.start()

    def wait_for_callback(self, timeout: int = 120) -> str:
        """Wait for OAuth callback with timeout"""
        start_time = time.time()

        while not self._code_received:
            if time.time() - start_time > timeout:
                raise TimeoutError(
                    f"OAuth callback not received within {timeout} seconds"
                )
            time.sleep(0.1)  # Check every 100ms

        return self.code

    def stop(self):
        if self._server:
            self._server.should_exit = True

        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=2)
