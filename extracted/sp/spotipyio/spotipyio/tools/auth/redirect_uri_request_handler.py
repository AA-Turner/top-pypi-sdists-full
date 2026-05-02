from http.server import SimpleHTTPRequestHandler
from typing import Optional


class RedirectURIRequestHandler(SimpleHTTPRequestHandler):
    access_code: Optional[str] = None

    def do_GET(self):
        if self.path.startswith("/?code"):
            RedirectURIRequestHandler.access_code = self.path.split("?code=")[-1]
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(
                b"<html><body><h1>Successfully fetched access code! You may close this window</h1></body></html>"
            )

        else:
            self.send_response(404)
            self.end_headers()
