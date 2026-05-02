"""
"""
import os
import sys
import time
import signal
import multiprocessing as mp
from pathlib import Path

import ghettorecorder.ghetto_menu as menu
import ghettorecorder.ghetto_procenv as procenv
import ghettorecorder.ghetto_blacklist as ghetto_blacklist
import ghettorecorder.ghetto_container as container
from ghettorecorder.ghetto_api import ghettoApi

if 'ANDROID_STORAGE' not in os.environ:
    mp.set_start_method('spawn', force=True)  # http server process


class Entry:
    def __init__(self):
        # file system config
        self.dir_name = os.path.dirname(__file__)  # absolute dir path
        self.config_dir = ''  # where settings ini is located
        self.config_name = "settings.ini"
        self.blacklist_name = "blacklist.json"
        self.radios_parent_dir = ''  # changed if settings GLOBAL 'save_to_dir' changes, blacklist_dir is also that dir
        # radio dicts, lists
        self.runs_meta = True
        self.runs_record = True
        self.runs_listen = True
        self.radio_name_list = []
        self.config_file_radio_url_dict = {}  # all {name: url}
        self.config_file_settings_dict = {}  # blacklist, folders
        self.radio_selection_dict = {}  # selection to rec

        # can be useful if on command line, and want start a http server to stream one of the radio instances local
        self.no_err_radios = []  # started radios without errors in err dict


entry = Entry()


def init_path():
    """File system basic info to find the configuration file.
    | Container creates folders in places where writing is allowed.
    """
    config_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)))

    container_dir = container.container_setup()
    if container_dir:
        config_dir = container_dir
        print('container config_dir ', config_dir)

    entry.config_dir = config_dir
    ghettoApi.path.config_dir = config_dir
    ghettoApi.path.config_name = entry.config_name
    pass


def run_radios(radio_dict):
    """
    Each instance can have its own configuration. Use a Database or json file.

    - instantiate radios in a dict, start instances
    - failed radios are canceled
    - first radio of the ini list starts a http server to listen local buffered sound

    :params: radio_base_dir: parent dir
    :params: radio_dict: radios with url from menu
    """
    for radio, url in radio_dict.items():
        procenv.radio_instance_create(radio, url, **entry.__dict__)

    url_timeout = 15
    start = time.perf_counter()
    while 1:  # minimize wait time
        done = all([True if instance.init_done else False for instance in ghettoApi.radio_inst_dict.values()])
        if done or (round((time.perf_counter() - start)) >= url_timeout):
            break


def radios_error_get():
    """Useful for terminal, where we must start
    all instances at the same time.

    """
    instance_err_dict = {}
    for radio, inst in ghettoApi.radio_inst_dict.items():
        if ghettoApi.radio_inst_dict[radio].error_dict:
            instance_err_dict[radio] = ghettoApi.radio_inst_dict[radio].error_dict
            ghettoApi.radio_inst_dict[radio].cancel()
            print(f' ### cancel radio {radio} ###')

    if len(instance_err_dict):
        print('\n\n --- errors ---\n\n')
        [print(k, v) for k, v in instance_err_dict.items()]
        print('\n\n --- end ---\n\n')

    entry.no_err_radios = [radio for radio in ghettoApi.radio_inst_dict.keys() if radio not in instance_err_dict.keys()]
    return entry.no_err_radios


def show_radios_urls_formatted():
    """Print formatted urls to be able to click listen.
    """
    for radio, url in entry.config_file_radio_url_dict.items():
        print(f'* {radio:<20} {url}')
    print('\n\t---')


def signal_handler(sig, frame):
    """ Terminal: catch Keyboard Interrupt ctrl + c, "signal.signal()" instances listen.

    :params: sig:  SIGTERM
    :params: frame: SIGINT
    """
    ghettoApi.blacklist.stop_blacklist_writer = True
    shutdown()

    print('\nThank you for using the GhettoRecorder module.')
    sys.exit(0)


if 'ANDROID_STORAGE' not in os.environ:
    # crashes the module under Android
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)


def shutdown():
    """Trigger shutdown of radio instances.
    """
    radio_lst = procenv.radio_instances_get()
    for radio in radio_lst:
        procenv.del_radio_instance(radio)


def run_ghetto(frontend=None):
    """
    | [STATIONS] *config_file_radio_url_dict* {radio: url} from ini; radio = url
    | [GLOBAL] *config_file_settings_dict* {'blacklist_enable': 'True', 'save_to_dir': 'f:\\012345'}
    | *radio_selection_dict* user selection command line, bulk start radio instances later
    | *radios_parent_dir* is the folder for all the radio dirs

    | HTTP server can use Ajax, radio buttons and a dict to switch radio instances on/off

    :methods: init_path: collect path variables in an instance and API
    :params: frontend: switch options to avoid input() loops and forced parallel start of instances, unlike cmd
    """
    init_path()
    # show main menu and collect radios or update config file
    menu.record() if frontend else menu.menu_main()  # ini file to internal dict or show terminal selection

    entry.config_file_radio_url_dict = menu.settings_ini_to_dict()
    for radio in entry.config_file_radio_url_dict.keys():
        entry.radio_name_list.append(radio)
    entry.config_file_settings_dict = menu.settings_ini_global()
    # dict for html radio buttons or terminal menu input() loop
    entry.radio_selection_dict = menu.radio_url_dict_create() if frontend else menu.record_read_radios()

    remote_dir = ghettoApi.path.save_to_dir  # settings.ini [GLOBAL] section path option for custom folder
    if remote_dir:
        entry.radios_parent_dir = Path(ghettoApi.path.save_to_dir)
    else:
        entry.radios_parent_dir = Path(ghettoApi.path.config_dir)

    ghetto_blacklist.init(**entry.__dict__)  # checks start option on/off itself


def main():
    """"""
    run_ghetto()

    entry.runs_listen = False  # use frontend for listen
    run_radios(entry.radio_selection_dict)
    show_radios_urls_formatted()
    while 1:
        # names_list = [thread.name for thread in threading.enumerate()]
        # print(names_list)
        time.sleep(10)  # interval to show list; exit via signal_handler and keyboard


if __name__ == "__main__":
    main()
