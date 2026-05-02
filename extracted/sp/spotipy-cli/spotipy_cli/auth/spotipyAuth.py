import webbrowser
import sys
import http.server
import time
from urllib import parse


class SpotipyAuth:
    authUri = 'https://accounts.spotify.com/authorize?client_id={}&response_type=code&' \
              'redirect_uri=http%3A%2F%2Flocalhost%3A{}%2F{}&' \
              'scope=user-modify-playback-state user-read-currently-playing user-read-playback-state ' \
              'playlist-read-private&'
    port = 9999
    path = 'callback'

    def __init__(self):
        self.server = http.server.HTTPServer(('localhost', self.port), ResponseHandler)
        self.server.hasToken = False

    def get_auth_code(self, client_id):
        sys.stdout.write("opening web browser...\n")
        webbrowser.open(self.authUri.format(client_id, self.port, self.path), new=2)
        self.server.handle_request()
        while not self.server.hasToken:
            sys.stdout.write("waiting...\n")
            time.sleep(1)
        return self.server.code


class ResponseHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'<html><head></head><body>Token Received. You can close this page now.</body></html>')
        params = parse.parse_qs(parse.urlsplit(self.path).query)
        self.server.code = params['code'][0]
        self.server.hasToken = True
