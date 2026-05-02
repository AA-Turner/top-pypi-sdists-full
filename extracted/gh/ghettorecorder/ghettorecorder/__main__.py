"""*Multithreading* HTTP server for frontend,
  else we stuck on one radio playing and we (the module) can not accept new requests.

| Threads started before socket connect.
| Means, connect gets a random http handler thread, already active.
| Have a timeout to disconnect from radio audio_out connector (queue), handler release.
"""
import os
import time
import json
import socket
import threading

from http.server import BaseHTTPRequestHandler, HTTPServer

import ghettorecorder.cmd as cmd
import ghettorecorder.ghetto_utils as utils
import ghettorecorder.ghetto_procenv as procenv
from ghettorecorder.cmd import entry  # instance [GLOBAL] [STATIONS] ini sections
from ghettorecorder.ghetto_api import ghettoApi

dir_name = os.path.dirname(__file__)


class Helper:
    def __init__(self):
        self.content_type = None
        self.server_shutdown = False


helper = Helper()


class Handler(BaseHTTPRequestHandler):

    def do_POST(self):
        """Ajax SENDs id or name strings.
        self.path is independent of post and get
        """
        if self.path == '/radio_btn_id':
            self.post_switch_radio()
        elif self.path == '/title_get':
            self.post_title_get()
        elif self.path == '/write_config_file':
            self.post_write_config_file()
        elif self.path == '/get_config_file':
            self.post_get_config_file()
        elif self.path == '/write_blacklist_file':
            self.post_write_blacklist_file()
        elif self.path == '/get_blacklist_file':
            self.post_get_blacklist_file()
        elif self.path == '/server_shutdown':
            self.post_server_shutdown()
        elif self.path == '/wait_shutdown':
            self.post_wait_shutdown()
        else:
            self.send_error(404, '[POST] wrong endpoint /<endpoint_name>')

    def do_GET(self):

        if self.path == '/':
            self.get_index_html()
        elif '/sound/' in self.path:
            radio = self.path[7:]  # skip 7 chars, read string to end
            self.get_sound(radio)
        elif '/shutdown/' in self.path:
            radio = self.path[10:]
            self.get_shutdown(radio)
        elif '/static/js/' in self.path:
            js = self.path[11:]
            self.get_js(js)
        elif self.path == '/static/css/style.css':
            self.get_style_css()
        elif '/static/images/' in self.path:
            img = self.path[15:]
            self.get_image(img)
        else:
            self.send_error(404, '[GET] wrong endpoint /<endpoint_name>')

    def post_wait_shutdown(self):
        """JS has ajax timeout."""
        self.data_string_get()
        dct = wait_shutdown()
        self.data_json_send(dct)

    def post_server_shutdown(self):
        """Shutdown is fast now.
        Must send answer before action.
        """
        self.data_string_get()
        self.data_json_send({'server_shutdown': ' recorder_shutdown_init'})
        server_shutdown()

    def post_get_blacklist_file(self):
        """blacklist to browser"""
        self.data_string_get()
        dct = read_blacklist_file()
        self.data_json_send(dct)

    def post_write_blacklist_file(self):
        """Write changes made by browser to blacklist."""
        file_content = self.data_string_get()
        dct = write_blacklist_file(file_content.decode('utf-8'))
        self.data_json_send(dct)

    def post_get_config_file(self):
        """settings.int to browser"""
        self.data_string_get()
        dct = read_config_file()
        self.data_json_send(dct)

    def post_write_config_file(self):
        """Write changes to settings.ini."""
        file_content = self.data_string_get()
        dct = write_config_file(file_content.decode('utf-8'))
        self.data_json_send(dct)

    def post_title_get(self):
        """data_string_get contains name of radio we want to check for new title. {'title': new_title}"""
        active_radio_name = self.data_string_get()
        dct = radio_title_get(active_radio_name.decode('utf-8'))
        self.data_json_send(dct)

    def post_switch_radio(self):
        """data_string_get contains name of radio we want to switch online.
        Contains Zero int '0' if first call. We disable cover to enable audio, browser demands this step.
        """
        radio_name = self.data_string_get()
        dct = switch_local_buffer(radio_name.decode('utf-8'))
        self.data_json_send(dct)

    def data_json_send(self, data):
        """Send a dictionary here.
        | First key can be identifier for ajax to validate correct delivery. {'foo_transfer': null, 'bar': 'fake_news'}
        | if (!data.foo_transfer) {return;}
        """
        json_string = json.dumps(data)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        try:
            self.wfile.write(bytes(json_string, "utf-8"))
        except OSError:  # browser dropped connection, supress broken pipe error
            pass

    def data_string_get(self):
        """Read the binary content of request."""
        length = int(self.headers.get_all('content-length')[0])
        data_string = self.rfile.read(length)
        self.send_response(200)
        return data_string

    def get_js(self, js):
        """Browser reads index.html line by line. We send JavaScript content (link or src) to browser."""
        self.send_response(200)
        self.send_header('Content-type', 'text/javascript')
        self.end_headers()
        with open(os.path.join(dir_name, 'static', 'js', js), 'r', encoding='utf-8') as f:
            txt = f.read()
        self.wfile.write(bytes(txt, "utf-8"))

    def get_style_css(self):
        """Browser reads index.html. Send Style Sheet to browser."""
        self.send_response(200)
        self.send_header('Content-type', 'text/css')
        self.end_headers()
        with open(os.path.join(dir_name, 'static', 'css', 'style.css'), 'r', encoding='utf-8') as f:
            txt = f.read()
        self.wfile.write(bytes(txt, "utf-8"))

    def get_image(self, img):
        """Image to browser."""
        self.send_response(200)
        self.send_header('Content-type', 'image/svg+xml')
        self.end_headers()
        with open(os.path.join(dir_name, 'static', 'images', img), 'r', encoding='utf-8') as f:
            txt = f.read()
        self.wfile.write(bytes(txt, "utf-8"))

    def get_shutdown(self, radio):
        """Radio instance shutdown and removal from dict."""
        self.send_response(200)
        self.end_headers()
        procenv.del_radio_instance(radio)

    def get_sound(self, radio=None):
        """The browser audio element (net client) auto connects /sound and is served here, no json return
        | We stuck here in a loop and THIS Handler Thread, module, is not able to respond to other requests.
        | Absorb errors from JS, minus sign in front of radio is stop radio button id

        | first char is minus if stop radio button, btn id is -radio name
        | None and empty on whatever

        :returns: Nothing, on error None;
        """
        if radio is None or radio == '' or radio[0:1] == '-':
            return
        self.get_send_header(helper.content_type)
        timeout = 20 if 'ANDROID_STORAGE' in os.environ else 5  # absorb minor network outages
        start = time.perf_counter()
        while 1:
            if radio in ghettoApi.radio_inst_dict.keys():
                audio_out_q = ghettoApi.radio_inst_dict[radio].audio_out
                if not audio_out_q:
                    break
                if not audio_out_q.empty():
                    start = time.perf_counter()  # reset
                    try:
                        self.wfile.write(audio_out_q.get())
                    except OSError:  # browser dropped connection, supress broken pipe error
                        while not audio_out_q.empty():
                            audio_out_q.get()
                        try:
                            audio_out_q.cancel_join_thread()  # py q feeder thread, q content is already removed
                        except AttributeError:
                            pass  # we run queue.Queue() on Android not mp.Queue, this has no cancel_join_thread
                        break

            idle = round((time.perf_counter() - start))
            if helper.server_shutdown or idle >= timeout:
                print(f'\tGhetto HTTP Handler - release connection {radio}')  # thread no more locked, out
                break
            time.sleep(.2)

    @staticmethod
    def generate_index_html():
        """Generate page line by line. We can change content if keyword string is found."""
        with open(os.path.join(dir_name, 'index.html'), 'r', encoding='utf-8') as f:
            while 1:
                line = f.readline()
                if line == '':
                    break
                yield line

    def get_index_html(self):
        """First call, we build the page. That's all.
        Button press on page will ajax 'do_POST' and update page.
        Ajax feed radio name, 'do_POST' calls py func and updates page.
        Java has to update the audio control element with new source URL (ghetto_simple stream srv on port 124....).

        :params: _o__radio_names____: write two radio buttons for a radio, stop (-) radio and run with to listen radio
        """
        self.get_send_header('text/html')
        generator = self.generate_index_html()
        while 1:
            try:
                next_line = next(generator)
                if '_o__gr_sky____' in next_line:
                    next_line = f"<img src='data:image/svg+xml;base64,{convert_img('gr_sky.svg')}'/>"
                if '_o__gr_basket____' in next_line:
                    next_line = f"<img src='data:image/svg+xml;base64,{convert_img('gr_sky_basket.svg')}'/>"
                if '_o__radio_names____' in next_line:
                    self.wfile.write(bytes("<div class='divRadioBtn' id='divRadioBtnHead'>stop 🌺 listen</div>",
                                           "utf-8"))
                    for radio_name in entry.config_file_radio_url_dict.keys():
                        radio_names_line = f"<div class='divRadioBtn' id='div{radio_name}'>" \
                                           "<label><input type='radio' name='da' " \
                                           f"id='-{radio_name}' onclick=ajax_switch_radio(id)></label>&nbsp; " \
                                           "<label><input type='radio' name='da' " \
                                           f"id='{radio_name}' onclick=ajax_switch_radio(id)>{radio_name}</label>" \
                                           "</div> "
                        self.wfile.write(bytes(radio_names_line, "utf-8"))
                    continue

            except StopIteration:  # last line already send, break in get_content()
                break
            self.wfile.write(bytes(next_line, "utf-8"))

    def get_send_header(self, content_type):
        """Send header with Access control tag."""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')  # absolute essential for using gain and analyzer
        self.send_header('Cache-Control', 'no-cache, no-store')  # absolute essential to not replay old saved stuff
        self.send_header('Content-type', content_type)
        self.end_headers()


def wait_shutdown():
    """Return a string for ajax to show we are still alive after shutdown command."""
    return {'wait_shutdown': 'alive'}


def server_shutdown():
    """Shutdown all radio instances command line style and tell server to shut down."""
    cmd.shutdown()
    helper.server_shutdown = True


def radio_title_get(radio):
    """Active radio interval title request."""
    title = procenv.radio_attribute_get(radio=radio, attribute='new_title')
    return {'title': title}


def switch_local_buffer(radio):
    """Radio checked if exists.
    Server checked by port number add digit (radio index in radio list) if exists already.
    """
    helper.content_type = None
    is_alive = True

    if radio == '0':  # disable cover div
        radio_instance_lst = procenv.radio_instances_get()
    elif radio[:1] == '-':  # del radio, name has a leading minus
        procenv.del_radio_instance(radio[1:])
        radio_instance_lst = procenv.radio_instances_get()
    else:  # add radio
        url = entry.config_file_radio_url_dict[radio]

        is_alive = procenv.radio_instance_create(radio, url, **entry.__dict__)
        radio_instance_lst = procenv.radio_instances_get()
    rv_dct = procenv.user_display_dict_get(radio)
    helper.content_type = rv_dct['content']
    rv_dct['recorder'] = radio_instance_lst
    rv_dct['server_port'] = server_port
    if not is_alive:
        print(f'----------- {radio} fail -------------')
        rv_dct['content'] = 'no_response'   # ajax knows an error
    return rv_dct


def start_radio_if_off(name, url):
    """feed content type to helper instance.
    create, fire and forget if error

    :returns: list of started radio instances names
    """
    is_online = procenv.radio_instance_create(name, url)
    active_radios_lst = procenv.radio_instances_get()
    if is_online:
        helper.content_type = procenv.radio_attribute_get(name, 'content_type')
    return active_radios_lst if is_online else False


def convert_img(file_name):
    """Base64 string converter.
    Remnant of first attempt to generate the page only from a python list, no file system.
    Still used.
    """
    file_path = os.path.join(dir_name, 'static', 'images', file_name)
    base_64_str = utils.convert_ascii(file_path)
    return base_64_str


def read_config_file():
    """Ajax send content of config file settings.ini.
    """
    file = entry.config_name
    folder = entry.config_dir  # changed from entry.dir_name
    conf_path = os.path.join(folder, file)
    with open(conf_path, 'r', encoding='utf-8') as reader:
        file_cont = reader.read()
    return {'get_config_file': file_cont, 'path': conf_path}


def write_config_file(file_content):
    """entry.config_dir is either our package folder or
    container folder.
    """
    file = entry.config_name
    folder = entry.config_dir
    conf_path = os.path.join(folder, file)
    with open(conf_path, 'w', encoding='utf-8') as writer:
        writer.write(file_content)
    return {'write_config_file': 'Done: ' + str(time.ctime())}


def read_blacklist_file():
    """Ajax send content of config file settings.ini"""
    file = entry.blacklist_name
    folder = entry.config_dir  # changed from radios_parent_dir to config_dir, keep conf and blist together
    file_path = os.path.join(folder, file)
    with open(file_path, 'r', encoding='utf-8') as reader:
        file_cont = reader.read()
    return {'get_blacklist_file': file_cont, 'path': file_path}


def write_blacklist_file(file_content):
    """"""
    file = entry.blacklist_name
    folder = entry.config_dir
    file_path = os.path.join(folder, file)
    with open(file_path, 'w', encoding='utf-8') as writer:
        writer.write(file_content)
    return {'write_blacklist_file': 'Done: ' + str(time.ctime())}


# Create ONE socket.
server_port = 1242
addr = ('', server_port)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(addr)
sock.listen(5)


# Launch listener threads.
class Thread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True  # self kill on prog exit
        self.start()

    def run(self):
        httpd = HTTPServer(addr, Handler, False)

        # Prevent the HTTP server from re-binding every handler.
        # https://stackoverflow.com/questions/46210672/
        httpd.socket = sock
        # Android, 3 threads, 3 msg "/ghettorecorder/__main__.py:408: ResourceWarning: unclosed <socket.socket fd=113,
        # family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('0.0.0.0', 0)>"
        # better would be to have a listener loop on socket to start a thread if needed
        httpd.server_bind = None

        httpd.serve_forever()


def main():
    """
    | Need more than one thread to not get blocked on serving one stream and answer requests.
    | 1st thread accept request and serves endless stream as listen connection.
    | 2nd thread accept request, browser drops connection -> 1st thread exit, 2nd thread start stream.
    | 3rd thread is for an unknown blocking error. Proceed with normal operation.

    :methods: run_ghetto: same function call as command line, but skip input() loops
    """
    cmd.run_ghetto(frontend=True)
    [Thread() for _ in range(3)]  # all on same port, means if range(2) one can connect 2 browser tabs = 2 connections
    print("\n\tUser Interface at " + f"http://localhost:{server_port}/\n")

    while 1:  # keep the show running until ajax sends shutdown command
        time.sleep(1)
        if helper.server_shutdown:
            ghettoApi.blacklist.stop_blacklist_writer = True
            break   # Process finished with exit code 0, if all threads are down


if __name__ == '__main__':
    main()
