""" GhettoRecorder config
settings.ini file
"""
import os
import configparser
from pathlib import Path as Pathlib_path
from ghettorecorder.ghetto_api import ghettoApi


class Gini:
    """Configparser stores most found setting in itself.
    | config.read_file() returns nothing
    """
    def __init__(self):
        self.config_name = "settings.ini"
        self.radio_names_list = []  # search radio name via character, from ghetto_menu
        self.dir_name = os.path.dirname(os.path.abspath(__file__))  # print ghettorecorder logo to screen
        self.config_stations_dct = {}  # config section [STATIONS] radio, url pairs
        self.config_global_dct = {}    # config section [GLOBAL]  info SAVE_TO_DIR = f:\2, BLACKLIST_ENABLE = True


gini = Gini()


def global_config_get():
    """Fills the 'config_global_dct', if [GLOBAL] section has members.
    """
    config = config_file_read()
    try:
        gini.config_global_dct = dict(config.items('GLOBAL'))
    except Exception as error:
        print(f'Config found, minor error [GLOBAL]: {error} - proceed')
    return gini.config_global_dct


def global_config_show():
    """ extract [GLOBAL] section from settings.ini, if available
    GLOBAL can be - not there, empty, or with values (test case)

    Method
       config_parse_get() - exit if no path

    Raise
       show that there is no config, but can proceed without (config_parse_get(), ok)
    """
    if not len(gini.config_global_dct):
        print("--> section [GLOBAL] is empty. No blacklist, or record path set.")
        return False
    else:
        print(f'.. settings.ini [GLOBAL] section: {gini.config_global_dct}')
        return True


def stations_config_get():
    """Fills the 'config_stations_dct', if [STATIONS] section has members.
    """
    config = config_file_read()
    try:
        gini.config_stations_dct = dict(config.items('STATIONS'))
    except AttributeError:
        print("--> gini.setting_config_show(), can not find configuration section [STATIONS] - proceed")
        return False

    for name in dict(config.items('STATIONS')):
        gini.radio_names_list.append(name)

    return True


def stations_config_show():
    """ show the content of the ini file to choose from
    fill radio_names_list and radio_names_dict to later validate the choice
     """
    with open(os.path.join(gini.dir_name, "ghetto_recorder.ascii"), "r") as reader:
        print(reader.read())

    for index, name in enumerate(gini.radio_names_list):
        print(f'\t{index} \t>> %-20s <<' % name)

    with open(os.path.join(gini.dir_name, "ghetto_recorder.menu_info"), "r") as reader:
        print(reader.read())
    # print(' \n Radio stations in your list. --> CHANGED: 42 to 12345')
    # print(' Please use "Ctrl + C" to stop the app.\n')
    # print('\tCopy/Paste a Radio from >> settings.ini <<, \n\tor type the leading number and press Enter\n')
    # print("\tType: 'ghetto_url' in a terminal to start the User Interface at " + "http://localhost:1242/")
    # print("\t If blacklist is ON, file: blacklist.json in the same folder as settings.ini")


def config_file_read():
    """Error if configparser fails.
    Path can be local module path or remote.
    """
    config = configparser.ConfigParser()
    try:
        config_file_path = os.path.join(ghettoApi.path.config_dir, ghettoApi.path.config_name)
        with open(config_file_path, 'r') as configfile:
            config.read_file(configfile)
        return config
    except OSError:
        try:
            config_file_path = os.path.join(gini.dir_name, gini.config_name)
            with open(config_file_path, 'r') as configfile:
                config.read_file(configfile)
            return config
        except OSError:
            print('OSError in config_parse_get not avail.')
            return False


def global_config_to_api():
    """ return True if [GLOBAL] section exists and has settings
    push setting of [GLOBAL] section from settings.ini in variables,

    Raise
       show that there is no config, but can proceed without (config_parse_get(), ok)
    """
    config = config_file_read()
    if config:
        try:
            gini.config_global_dct = dict(config.items('GLOBAL'))
        except Exception as error:
            print(f'Config found, minor error: {error} - proceed')
            return False

        if not len(gini.config_global_dct):
            print("--> section [GLOBAL] is empty. No blacklist, or record path set.")
            return False
        else:
            for key, val in gini.config_global_dct.items():
                if key == "SAVE_TO_DIR".lower():
                    # push path from [GLOBAL]
                    ghettoApi.path.save_to_dir = val
                if key == "BLACKLIST_ENABLE".lower():
                    ghettoApi.blacklist.blacklist_enable = val
            return True


def global_record_path_write(custom_path):
    """ ini config write SAVE_TO_DIR 'remote' from modules path.
    We have already tried to read the global section.
    ["GLOBAL"]
    SAVE_TO_DIR = f:/2

    :params: custom_path: can be a remote path of an .ini in Alaska, not the dir where module is located
    """
    # the magic happens here
    config_file_path = os.path.join(ghettoApi.path.config_dir, ghettoApi.path.config_name)

    config = configparser.ConfigParser()
    with open(config_file_path, 'r') as configfile:
        config.read_file(configfile)
    config.sections()
    if "GLOBAL" not in config:
        config.add_section('GLOBAL')
    config.set('GLOBAL', 'SAVE_TO_DIR', str(Pathlib_path(custom_path)))  # help to write path for OS
    with open(config_file_path, 'w') as configfile:
        config.write(configfile)


def global_blacklist_enable_write(option):
    """ ini config write
    ["GLOBAL"]
    BLACKLIST_ENABLE = True
    """
    # the magic happens here
    config_file_path = os.path.join(ghettoApi.path.config_dir, ghettoApi.path.config_name)

    config = configparser.ConfigParser()
    with open(config_file_path, 'r') as configfile:
        config.read_file(configfile)
    config.sections()
    if "GLOBAL" not in config:
        config.add_section('GLOBAL')
    config.set('GLOBAL', 'BLACKLIST_ENABLE', option)
    with open(config_file_path, 'w') as configfile:
        config.write(configfile)


def config_path_api_set(config_files_dir):
    """ Menu 'Set path to config, settings.ini'
    set path blacklist,
    set path to a 'remote' config file (local fs, writable network location)

    Hint
       can have config somewhere and write to save_to_dir path elsewhere, if this option is used
    """
    ghettoApi.blacklist.blacklist_dir = ghettoApi.path.config_dir = str(Pathlib_path(config_files_dir))


def main():
    """Show what we are doing here and
    function test module.
    """

    global_config_get()  # read [GLOBAL] section to dict
    global_config_show()
    stations_config_get()  # read [STATIONS] section to dict
    stations_config_show()
    # write new record path to either local ini or remote ini (custom_path)
    import ghetto_utils
    custom_path = os.path.join(gini.dir_name, "home_of_the_grinch")
    ghetto_utils.make_dirs(custom_path)
    import shutil
    src_ini, dst_ini = os.path.join(gini.dir_name, gini.config_name), os.path.join(custom_path, gini.config_name)
    shutil.copy(src_ini, dst_ini)
    ghettoApi.path.config_dir, ghettoApi.path.config_name = custom_path, gini.config_name
    global_record_path_write(custom_path)  # save_to_dir custom path
    global_blacklist_enable_write('False')  # write False to blacklist
    global_config_get()  # read [GLOBAL] section to dict
    global_config_show()
    ghetto_utils.delete_dirs(custom_path)

    global_config_to_api()  # blacklist_enable should be True
    print('to_api: save_to_dir, blacklist_enable', ghettoApi.path.save_to_dir, ghettoApi.blacklist.blacklist_enable)
    config_path_api_set(custom_path)
    print('to_api: config_dir, blacklist_dir', ghettoApi.path.config_dir, ghettoApi.blacklist.blacklist_dir)


if __name__ == "__main__":
    main()
