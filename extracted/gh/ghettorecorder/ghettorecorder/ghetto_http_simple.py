"""
"""
from http.server import BaseHTTPRequestHandler, HTTPServer


def run_http(**kwargs):
    """Blocked, no loop here

    :params: kwargs:
    """
    MiniHandler.port = kwargs['port']
    MiniHandler.srv_name = kwargs['srv_name']
    MiniHandler.com_queue = kwargs['com_queue']
    MiniHandler.radio_name = kwargs['radio_name']
    MiniHandler.radio_url = kwargs['radio_url']
    MiniHandler.content_type = kwargs['content_type']

    while 1:
        try:
            webServer = HTTPServer(('localhost', kwargs['port']), MiniHandler)
            print(f"Record buffer . {kwargs['radio_name']} . http://localhost:{kwargs['port']}")
            break
        except OSError:
            print(f'port in use {kwargs["port"]}')
            print('\n\tadd one to port number')
            kwargs['port'] += 1  # port already in use

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass
    webServer.server_close()
    print("SimpleHTTPServer stopped.")


class MiniHandler(BaseHTTPRequestHandler):

    port = ""
    com_queue = None
    radio_url = ""
    radio_name = ""
    content_type = ''

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', self.content_type)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-cache,no-store')  # up to browser
        self.end_headers()
        # this will be shown if a browser connects to us
        # msg = f'\tHttp connection for local buffer - {self.radio_name} - established. {self.content_type}' \
        #       f'\n\tAddress: me("http://localhost:{self.port}") you{self.client_address}'
        # print(msg)

        while 1:
            try:
                qq = self.com_queue.get(block=True)
                # print(qq)
                self.wfile.write(qq)
            except ConnectionAbortedError as e:
                print(f' \t--GhettoHttpHandler--> local host connection aborted: {e} {self.radio_name}')
                self.close_connection = True  # else chrome refuses reconnect endless
                break
            except Exception as e:
                print(f'--GhettoHttpHandler--> {e} {self.radio_name}')
                self.close_connection = True
                return
