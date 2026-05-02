""" Module for ghettorecorder Python package to container deployment.

All container need different folders to store 'settings.ini'.
Some areas are write protected, restored to default after app exit, or the user can not access them.

Methods
    container_setup decide to set up a container env
    container_config_dir get path for new folder creation
    create_config_env overwrite base dir for ghetto, copy config file to that dir
"""
import os
import shutil
import getpass
from ghettorecorder import ghetto_ini
from ghettorecorder.ghetto_api import ghettoApi


def container_setup() -> str:
    """ return False, empty string if no package specific env variable is set

    Copy settings.ini to the container writable user folder.

    Android Studio 'can not' copy settings.ini from /assets to user folder. Need root access.

    *DOCKER* Variable must be set in package config file Dockerfile or snapcraft.yaml

     Android problem with mp queue. Same as SNAP, but there it was appArmor related.
              stdlib/multiprocessing/queues.py", line 43, in __init__
    W    File "stdlib/multiprocessing/context.py", line 68, in Lock
    W    File "stdlib/multiprocessing/synchronize.py", line 162, in __init__
    W    File "stdlib/multiprocessing/synchronize.py", line 57, in __init__
    W    File "./java/android/__init__.py", line 140, in __init__
    W  OSError: This platform lacks a functioning sem_open implementation, therefore,
       the required synchronization primitives needed will not function, see issue 3770.


    :returns: string of folder where settings.ini and blacklist.json resides
    """
    folder = ''
    is_snap = 'SNAP' in os.environ
    is_docker = 'DOCKER' in os.environ  # must be set in Docker file
    is_android = 'ANDROID_STORAGE' in os.environ

    if is_snap:
        get_env_snap()  # track snap ver, release beta, edge ...
        username = getpass.getuser()
        print('Hello, ' + username)
        folder = os.path.join('/home', username, 'GhettoRecorder')
        create_config_env(folder)

    if is_docker:
        print('\n\tGhettoRecorder App in Docker Container\n')
        folder = os.path.join('/tmp', 'GhettoRecorder')
        create_config_env(folder)

    if is_android:
        print('\n\tGhettoRecorder Android App\n')
        # we are not allowed to write files (.ini) from setup apk to user folders; redirect rec via ini
        is_path = parent_record_path_get()
        if not is_path:
            parent_record_path_change("/storage/emulated/0/Music/")  # same as menu 'Change parent record path'

    return folder


def get_env_snap():
    print('GhettoRecorder App in Snap Container, check environment:\n')
    print('SNAP_USER_COMMON: ' + os.environ["SNAP_USER_COMMON"])
    print('SNAP_LIBRARY_PATH: ' + os.environ["SNAP_LIBRARY_PATH"])
    print('SNAP_COMMON: ' + os.environ["SNAP_COMMON"])
    print('SNAP_USER_DATA: ' + os.environ["SNAP_USER_DATA"])
    print('SNAP_DATA: ' + os.environ["SNAP_DATA"])
    print('SNAP_REVISION: ' + os.environ["SNAP_REVISION"])
    print('SNAP_NAME: ' + os.environ["SNAP_NAME"])
    print('SNAP_ARCH: ' + os.environ["SNAP_ARCH"])
    print('SNAP_VERSION: ' + os.environ["SNAP_VERSION"])
    print('SNAP: ' + os.environ["SNAP"])


def create_config_env(ghetto_folder):
    """ copy config files outside the default package folder /site-settings/ghettorecorder

    statements
       create new parent record folder
       overwrite radio_base_dir default path where config is searched
       copy settings.ini to that folder, blacklist is created automatically if choice
    """
    make_config_folder(ghetto_folder)
    ghettoApi.config_dir = ghetto_folder
    conf_dct = {
        'source_ini': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'settings.ini'),
        'dst_ini': os.path.join(ghetto_folder, 'settings.ini'),
        'source_json': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'blacklist.json'),
        'dst_json': os.path.join(ghetto_folder, 'blacklist.json')
    }
    container_copy_settings(**conf_dct)


def make_config_folder(ghetto_folder):
    try:
        os.makedirs(ghetto_folder, exist_ok=True)
        print(f"\tOK: {ghetto_folder}")
    except OSError as error_os:
        print(f"\tDirectory {ghetto_folder} can not be created {error_os}")
        return False


def container_copy_settings(**kwargs):
    """ Copy settings.ini and never overwrite a user customized settings.ini. """
    try:
        if not os.path.exists(kwargs['dst_ini']):
            shutil.copyfile(kwargs['source_ini'], kwargs['dst_ini'])
            shutil.copyfile(kwargs['source_ini'], kwargs['dst_ini'])
    except FileExistsError:
        pass
    except Exception as e:
        print(e)


def parent_record_path_get():
    """ Return the custom path used as parent dir from ini. save_to_dir = \\storage\\emulated\\0\\Music """
    ghettoApi.path.config_dir = os.path.dirname(__file__)
    ghettoApi.path.config_name = "settings.ini"
    print(f'\n\tWrite a new path to store files\n.. config file settings.ini in  {ghettoApi.path.config_dir}')

    ghetto_ini.global_config_to_api()  # dump [GLOBAL] section to api dicts
    parent_dir = ghettoApi.path.save_to_dir
    ghetto_ini.global_config_get()
    ghetto_ini.global_config_show()
    return parent_dir


def parent_record_path_change(folder):
    """ populate variables in GIni
     """
    try:
        ghetto_ini.global_record_path_write(folder)
    except FileNotFoundError:
        print("--> error, config file is not there or writeable (check path) - proceed")
    ghetto_ini.global_config_get()
    ghetto_ini.global_config_show()
