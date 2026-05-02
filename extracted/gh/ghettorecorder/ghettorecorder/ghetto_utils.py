import os
import base64
import shutil
import threading
from time import sleep


dir_name = os.path.join(os.path.dirname(os.path.abspath(__file__)))
db_name = 'ghetto_recorder_control.db'


def thread_is_up(thread):
    """Test if thread name is active.

    :params: thread: name
    :returns: True if found
    """
    names_list = [thread.name for thread in threading.enumerate()]
    return True if thread in names_list else False


def thread_shutdown_wait(*threads):
    """We return if none of the thread names are listed anymore.
    Blocks.

    :params: threads: arbitrary list of thread names
    """
    busy = True
    while busy:
        names_list = [thread.name for thread in threading.enumerate()]
        busy = True if any([True for thread in threads if thread in names_list]) else False
        sleep(.1)


def is_callable(radio_name, mod, func):
    """Raise error early, no crash if module method is unavailable.
    """
    rv = True
    try:
        if not callable(getattr(mod, func)):
            raise Exception
    except Exception as e:
        print(f'\n Exception {radio_name}: {e}\n')
        rv = False
    return True if rv else False


def make_dirs(path):
    """Create folders for recorder file and user files.

    :exception: error_writer dict can be parsed by Main thread, which can cancel the instance
    :params: path: absolute path that can contain subdirectories
    """
    rv = True
    try:
        os.makedirs(path, exist_ok=True)
        print(f"\t{path} created")
    except OSError:
        rv = False
    return True if rv else False


def delete_dirs(path):
    """"""
    rv = True
    try:
        shutil.rmtree(path)
        print(f"\t{path} deleted")
    except OSError:
        rv = False
    return True if rv else False


def shutdown_msg(radio_name, msg):
    """Shutdown sends a formatted message.

    :params: msg: to print
    """
    print(f'Shutdown {radio_name} {msg}')


def remove_special_chars(str_name):
    """ remove special characters for writing to file system

    :params: str_name: string with special chars
    :rtype: str
    """
    ret_value = str_name.translate({ord(string): "" for string in '"!@#$%^*()[]{};:,./<>?\\|`~=+"""'})
    return ret_value


def convert_ascii(file_name):
    with open(file_name, "rb") as reader:
        img_bytes = reader.read()
        img_ascii = render_data(img_bytes, 'encode')
    return img_ascii


def render_data(byte_data, de_enc):
    data = ''
    if de_enc == 'encode':
        data = base64.b64encode(byte_data).decode('ascii')
    if de_enc == 'decode':
        data = base64.b64decode(byte_data).decode('ascii')
    return data
