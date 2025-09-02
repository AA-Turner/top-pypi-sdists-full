# Copyright 2025 Q-CTRL. All rights reserved.
#
# Licensed under the Q-CTRL Terms of service (the "License"). Unauthorized
# copying or use of this file, via any medium, is strictly prohibited.
# Proprietary and confidential. You may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
#    https://q-ctrl.com/terms
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS. See the
# License for the specific language.

import os
import socket
import webbrowser
from http.server import (
    BaseHTTPRequestHandler,
    HTTPServer,
)
from typing import Any, Callable

BASE_REDIRECT_URL = "https://accounts.q-ctrl.com/auth"
REDIRECT_SUCCESS_URL = f"{BASE_REDIRECT_URL}/success?messageid=pythonpackage"
REDIRECT_ERROR_URL = f"{BASE_REDIRECT_URL}/error?messageId=pythonPackage"


def check_if_network_port_is_available(port: int) -> bool:
    """Check if a network port is available."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        return sock.connect_ex(("", port)) != 0


def get_free_network_port(range_from: int = 8000, range_to: int = 9000) -> int:
    """Get a free network port."""
    for port in range(range_from, range_to):
        if check_if_network_port_is_available(port):
            return port
    raise RuntimeError("No free network port found")


def complete_login(port: int, url: str, callback: Callable[[str], None]) -> None:
    """
    Creates a simple web server that will open a browser to the login page and
    listen for the redirect callback.
    """

    class RequestHandler(BaseHTTPRequestHandler):
        """
        Basic HTTP server that listen to a single request and redirects the path
        to the context callback function.
        """

        def log_request(self, *args: Any, **kwargs: Any) -> None:
            """Only log the request if `DEBUG_OIDC` is set."""
            if os.environ.get("DEBUG_OIDC"):
                super().log_request(*args, **kwargs)

        def do_GET(self) -> None:  # noqa: N802
            """Handle GET requests."""
            try:
                callback(self.path)

            except Exception:  # noqa: BLE001
                self.send_response(307)
                self.send_header("Location", REDIRECT_ERROR_URL)
                self.end_headers()

            else:
                self.send_response(307)
                self.send_header("Location", REDIRECT_SUCCESS_URL)
                self.end_headers()

    server_address = ("", port)
    try:
        httpd = HTTPServer(server_address, RequestHandler)
    except OSError as exc:
        raise RuntimeError(
            "Could not start HTTP server, port is already in use"
        ) from exc

    print("The URL above should be automatically opened in your default web browser.")
    print("(Please copy and paste in case it doesn't open automatically)")
    print()
    print("Authenticate your credentials in your browser...")
    print()
    webbrowser.open(url)
    httpd.handle_request()
