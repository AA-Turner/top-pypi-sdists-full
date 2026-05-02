""" GhettoRecorder command line menu display,

settings.ini
   [GLOBAL]
   SAVE_TO_DIR = f:\2
   BLACKLIST_ENABLE = true
   [STATIONS]
   classic = http://37.251.146.169:8000/streamHD

Methods
   menu_main()      - main menu
   menu_path()      - store custom path in config, default is recorder parent dir in config file folder
   menu_blacklist() - enable blacklist feature, store in config and create json dict file if not exists
   record()         - init all dicts in ghetto_ini.GIni, show the list of radios to choose from
   record_read_radios() - input prompt, get radio name or the choice (index) number of a radio list, create folder
   record_validate_input(radio_name) - True if choice in list, True if index of list is valid, False if not valid
   record_validate_radio_name(radio_name) - change the index number back to radio name, if index was the choice
   record_create_radio_url_dict(radio_name) - need radio name as thread and folder name, url to connect to network
   terminal_record_parent_dir_get()  - return GIni.radio_base_dir, parent folder
   terminal_record_custom_path_get() - called by ghetto_recorder module, config is called at radio choice in main menu
   terminal_record_blacklist_enabled_get() - called by ghetto_recorder module, enable api variable
   terminal_record_all_radios_get() - called by ghetto_recorder module to write blacklist beside settings.ini
   path_change() - call menu_path(), Change record parent path
   parent_record_path_change() - store path in [GLOBAL], test if path is writeable
   path_validate_input(custom_path) - return True if path is valid
   blacklist()                      - Enable/disable blacklists
   blacklist_is_enabled()           - Write a new blacklist option to settings.ini file
   blacklist_on()                   - write enabled to config file
   blacklist_off()                  - write disabled to config file
   remove_special_chars(str_name)   - clean radio name to create a folder
"""
import os
from aacrepair import AacRepair
from ghettorecorder.ghetto_api import ghettoApi
import ghettorecorder.ghetto_ini as ghetto_ini


def menu_main():
    print('\tmenu \'Main\'')
    menu_options = {
        1: 'Record (local listen option)',
        2: 'Change parent record path',
        3: 'Enable/disable blacklists',
        4: 'Set path to config, settings.ini',
        5: 'aac file repair',
        6: 'Exit',
    }

    while 1:
        option = ""
        for key in menu_options.keys():
            print(key, '--', menu_options[key])

        try:
            option = int(input('Enter your choice: '))
        except ValueError:
            print('Invalid option. Please enter a number between 1 and 4.')
        if option == 1:
            record()
            break
        elif option == 2:
            path_change()
            break
        elif option == 3:
            blacklist()
        elif option == 4:
            config_path_change()
        elif option == 5:
            aac_file_repair()
            break
        elif option == 6:
            print('Thank you for using GhettoRecorder.')
            exit()
        else:
            print('Invalid option. Please enter a number between 1 and 6.')
    return


def menu_path():
    menu_options = {
        1: 'Write to config. Parent path for recorded radios.',
        2: 'Back to Main Menu',
    }

    while 1:
        option = ""
        for key in menu_options.keys():
            print(key, '--', menu_options[key])

        try:
            option = int(input('Enter your choice: '))
        except ValueError:
            print('Invalid option. Please enter a number between 1 and 2.')
        if option == 1:
            parent_record_path_change()
            menu_main()
            break
        elif option == 2:
            menu_main()
            break
        else:
            print('Invalid option. Please enter a number between 1 and 2.')


def menu_blacklist():
    ghetto_ini.global_config_get()
    ghetto_ini.global_config_show()
    menu_options = {
        1: "blacklist on (don't write title if already downloaded)",
        2: 'blacklist off',
        3: 'Back to Main Menu',
    }

    while 1:
        option = ""
        for key in menu_options.keys():
            print(key, '--', menu_options[key])

        try:
            option = int(input('Enter your choice: '))
        except ValueError:
            print('Invalid option. Please enter a number between 1 and 3.')
        if option == 1:
            blacklist_on()
            break
        elif option == 2:
            blacklist_off()
            break
        elif option == 3:
            menu_main()
            break
        else:
            print('Invalid option. Please enter a number between 1 and 3.')


def menu_find_config():
    ghetto_ini.global_config_show()
    menu_options = {
        1: 'Path to "setting.ini" and "blacklist.json"',
        2: 'Back to Main Menu',
    }

    while 1:
        option = ""
        for key in menu_options.keys():
            print(key, '--', menu_options[key])

        try:
            option = int(input('Enter your choice: '))
        except ValueError:
            print('Invalid option. Please enter a number between 1 and 2.')
        if option == 1:
            config_path_change()
            break
        elif option == 2:
            menu_main()
            break
        else:
            print('Invalid option. Please enter a number between 1 and 2.')


def record():
    """ show all options if True, else fail brutal to retrieve the error message
    init all dicts in ghetto_ini.GIni, show the list of radios to choose from

    Functions
       GIni.config_path_test()    - test if configparser can read config file
       ghetto_ini.global_config_show()  - [GLOBAL] settings.ini vars
       ghetto_ini.global_config_to_api  - read in [GLOBAL] settings.ini vars
       ghetto_ini.stations_config_show() - show the main menu headline and description
    """
    print('\toption \'record\'')
    if ghetto_ini.stations_config_get():
        ghetto_ini.stations_config_show()

        print(f'\n..  config file settings.ini in {ghettoApi.path.config_dir}')
        ghetto_ini.global_config_get()
        ghetto_ini.global_config_to_api()
        ghetto_ini.global_config_show()  # if something is configured


def record_read_radios():
    """ return validated 'radio_url_dict' to ghetto_recorder module

    input on main menu
       the list index number of a radio (prefix, [6 >> time_machine <<])
       name on the list in main menu

    target
       write radio_url_dict[radioName] = URL
       recognize list index numbers to transform number into radio name

    Methods
       record_validate_radio_name() - validate radio name or transform choice (index) number of a radio to name,
       record_create_radio_url_dict(valid_name) - return (name, url) tuple

    return
       'radio_url_dict'
    """
    radio_list = []  # fill a list, just to see if we get valid input
    radio_url_dict = {}  # return value of the function
    while True:
        line_input = input('Enter to record -->:')
        radio_name = line_input.strip()

        if line_input == str(12345):  # all
            for name in ghetto_ini.gini.radio_names_list:
                name, url = record_create_radio_url_dict(name)
                radio_url_dict[name] = url
                print(f"12345...{name}")
            break

        elif (not len(radio_list)) and (not len(radio_name)):
            print("nothing to do, next try ...")
            menu_main()
        elif (len(radio_list) > 0) and (not len(radio_name)):
            # list is filled with valid inputs, record starts with empty input
            print(f".. got the radio list: {list(set(radio_list))}")
            break
        else:
            # True, if valid index was used, turn it in the radio name from list, else check name in choice list
            is_valid = record_validate_input(radio_name)
            if is_valid:
                # turn list index in element name, choice '0' to Blues_UK,
                valid_name = record_validate_radio_name(radio_name)
                name, url = record_create_radio_url_dict(valid_name)
                radio_url_dict[name] = url
                radio_dir_name = remove_special_chars(valid_name)
                radio_list.append(radio_dir_name)
                print(' Hit Enter <---| to RECORD, or paste next radio, write 12345 for all radios ')
    return radio_url_dict


def radio_url_dict_create():
    radio_url_dict = {}
    for name in ghetto_ini.gini.radio_names_list:
        name, url = record_create_radio_url_dict(name)
        radio_url_dict[name] = url
    return radio_url_dict


def settings_ini_to_dict():
    """"""
    radio_url_dict = {}
    for name in ghetto_ini.gini.radio_names_list:
        name, url = record_create_radio_url_dict(name)
        radio_url_dict[name] = url
    return radio_url_dict


def settings_ini_global():
    """"""
    rv_empty = {}
    config_global_dct = ghetto_ini.global_config_get()
    return config_global_dct if config_global_dct else rv_empty


def record_validate_input(radio_name) -> bool:
    """ return True if choice is name in list, return True for choice if index of list is a valid integer
    return False if not valid
     """
    if radio_name in ghetto_ini.gini.radio_names_list:
        return True
    try:
        radio_index = abs(int(radio_name))  # 0000 and -1
    except ValueError:
        return False
    if len(ghetto_ini.gini.radio_names_list) < radio_index:
        # input 100 if radio list has only 12 members
        return False
    if ghetto_ini.gini.radio_names_list[radio_index]:
        return True


def record_validate_radio_name(radio_name):
    """ return radio name from 'radio_names_list', else return name by absolute number of index of 'radio_names_list'
    clean false input like 0000 to 0, -12 to 12
    GIni.radio_names_list[abs(int(12))] = 'nachtflug'
    """
    if radio_name in ghetto_ini.gini.radio_names_list:
        return radio_name
    else:
        radio_id = radio_name
        return ghetto_ini.gini.radio_names_list[abs(int(radio_id))]


def record_create_radio_url_dict(radio_name):
    """ return tuple radio name, url
    need radio name as thread name and folder name, url to connect to network
    clean the radio name from special chars to make folders
    """
    url = ghetto_ini.gini.config_stations_dct[radio_name]
    radio_spec = remove_special_chars(radio_name)
    radio_url_tuple = (radio_spec, url)
    return radio_url_tuple


def terminal_record_blacklist_enabled_get():
    """ return True/False, called by ghetto_recorder module """
    ghetto_ini.global_config_show()
    return ghettoApi.blacklist.blacklist_enable


def terminal_record_all_radios_get():
    """ called by ghetto_recorder module to write blacklist beside settings.ini """
    return ghetto_ini.gini.radio_names_list


def path_change():
    """ call menu_path(), Change record parent path """
    print('\toption \'Change record parent path\'')
    menu_path()


def parent_record_path_change():
    """ populate variables in GIni

     show old path
        if any, write new one to GLOBAL section, create GLOBAL, if not exists
        test if path is writeable
        show new path, GIni.global_config_show

     Exception
        we crash, if config file is not in path, writing will fail
     """
    print(f'\n\tWrite a new path to store files\n.. config file settings.ini in  {ghettoApi.path.config_dir}')
    ghetto_ini.global_config_get()
    ghetto_ini.global_config_show()
    while True:
        line_input = input('Enter a new path, OS syntax (f:\\10 or /home ) -->:')
        custom_path = line_input.strip()  # to validate the name

        if not len(custom_path):
            print("nothing to do ...")
            menu_main()
            break
        else:
            is_valid = path_validate_input(custom_path)
            if is_valid:
                try:
                    ghetto_ini.global_record_path_write(custom_path)
                except FileNotFoundError:
                    print("--> error, config file is not there or writeable (check path) - proceed")
                ghetto_ini.global_config_get()
                ghetto_ini.global_config_show()
                input('Hit Enter to leave -->:')
                break
            else:
                input_exit = input('Hit Enter to try again, or "E" to leave -->:')
                if (input_exit == "E") or (input_exit == "E".lower()):
                    break


def config_path_change():
    """ change the path to settings.ini and blacklist.json

     show old path
        write new path to [GLOBAL] section, create [GLOBAL], if not exists
        test if path is writeable
        show new path, ghetto_ini.global_config_show()
     """
    print(f'\n\tType path to folder with settings.ini and blacklist.json (used for radio sub directories)'
          f'\n.. config file settings.ini in  {ghettoApi.path.config_dir}')
    ghetto_ini.global_config_show()
    while True:
        line_input = input('Enter a new path, OS syntax (f:\\10 or /home ) -->:')
        config_files_dir = line_input.strip()  # to validate the name

        if not len(config_files_dir):
            print("nothing to do ...")
            menu_main()
            break
        else:
            old_config_dir = ghettoApi.path.config_dir
            ghettoApi.path.config_dir = config_files_dir
            has_config = ghetto_ini.config_file_read()
            is_valid = path_validate_input(config_files_dir)
            if is_valid and has_config:
                ghetto_ini.config_path_api_set(config_files_dir)
                ghetto_ini.global_config_show()
                input('Hit Enter to leave -->:')
                break
            else:
                ghettoApi.path.config_dir = old_config_dir
                print(f'Not valid. Directory writeable: {is_valid}, has config: {has_config}')
                input_exit = input('Hit Enter to try again, or "E" to leave -->:')
                if (input_exit == "E") or (input_exit == "E".lower()):
                    break


def path_validate_input(custom_path):
    """ return True if path is valid """
    try:
        os.makedirs(custom_path, exist_ok=True)
        print(f".. path: {custom_path}")
    except OSError:
        print(f"\tDirectory {custom_path} can not be created")
        return False
    return True


def blacklist():
    """ Enable/disable blacklists """
    print('\toption \'Enable/disable blacklists\'')
    blacklist_is_enabled()


def blacklist_is_enabled():
    """ Write a new blacklist option to settings.ini file """
    print('\n\tWrite a new blacklist option to settings.ini file'
          f'\n.. config file settings.ini in  {ghettoApi.path.config_dir}')
    menu_blacklist()


def blacklist_on():
    """ write enabled to config file """
    print('\n\tblacklist is ON: settings.ini file'
          '\n\tExisting titles are not recorded again and again.'
          '\nfile name is "blacklist.json" in the same folder as "settings.ini"')
    ghetto_ini.global_blacklist_enable_write("True")
    ghetto_ini.global_config_get()
    ghetto_ini.global_config_show()
    input('Hit Enter to leave -->:')


def blacklist_off():
    """ write disabled to config file """
    print('\n\tblacklist is OFF: settings.ini file')
    ghetto_ini.global_blacklist_enable_write("False")
    ghetto_ini.global_config_get()
    ghetto_ini.global_config_show()
    input('Hit Enter to leave -->:')


def aac_file_repair():
    """
    """
    print('\n\tWrite a path to aac files. Only aac files will be touched.')
    ghetto_ini.global_config_show()
    while True:
        line_input = input('Enter a path, OS syntax (f:\\10 or /home ) -->:')
        aac_path = line_input.strip()  # to validate the name

        if not len(aac_path):
            print("nothing to do ...")
            menu_main()
            break
        else:
            is_valid = path_validate_input(aac_path)
            if is_valid:
                aacRepair = AacRepair(aac_path)
                aacRepair.repair()
                # input('Hit Enter to leave -->:')
                break
            else:
                input_exit = input('Hit Enter to try again, or "E" to leave -->:')
                if (input_exit == "E") or (input_exit == "E".lower()):
                    break


def remove_special_chars(str_name):
    ret_value = str_name.translate({ord(string): "" for string in '"!@#$%^*()[]{};:,./<>?\\|`~=+"""'})
    return ret_value


def main():
    config_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    ghettoApi.path.config_dir = config_dir
    ghettoApi.path.config_name = "settings.ini"
    menu_main()


if __name__ == "__main__":
    main()
