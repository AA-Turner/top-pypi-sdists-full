import html
import json
import logging
import mimetypes
import socket
import string
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from ._helpers import TunaError, get_version_text
from ._import_profile import read_import_profile
from ._runtime_profile import read_runtime_profile

logger = logging.getLogger(__name__)


def read(filename):
    try:
        return read_import_profile(filename)
    except (TunaError, StopIteration):
        pass

    return read_runtime_profile(filename)


def render(data, prof_filename):
    this_dir = Path(__file__).resolve().parent
    with (this_dir / "web" / "index.html").open(encoding="utf-8") as _file:
        template = string.Template(_file.read())

    return template.substitute(
        data=html.escape(json.dumps(data).replace("</", "<\\/")),
        version=html.escape(get_version_text()),
        filename=html.escape(prof_filename.replace("</", "<\\/")),
    )


def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("localhost", port)) == 0


def start_server(prof_filename, start_browser, port):
    data = read(prof_filename)

    class StaticServer(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)

            if self.path == "/":
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(render(data, prof_filename).encode())
            else:
                this_dir = Path(__file__).resolve().parent
                filepath = this_dir / "web" / self.path[1:]

                mimetype, _ = mimetypes.guess_type(str(filepath))
                assert mimetype is not None
                self.send_header("Content-type", mimetype)
                self.end_headers()

                with filepath.open("rb") as fh:
                    content = fh.read()
                self.wfile.write(content)

    if port is None:
        port = 8000
        while is_port_in_use(port):
            port += 1

    httpd = ThreadingHTTPServer(("", port), StaticServer)

    if start_browser:
        address = f"http://localhost:{port}"
        threading.Thread(target=lambda: webbrowser.open_new_tab(address)).start()

    logger.info("Starting httpd on port %s", port)
    httpd.serve_forever()
