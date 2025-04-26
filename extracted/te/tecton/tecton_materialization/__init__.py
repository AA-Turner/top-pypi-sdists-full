import importlib
import os


def __init():
    # Workaround for https://github.com/sdispater/pendulum/issues/429
    # to allows loading this module from a .zip with transitive dependencies included. It works by tricking an
    # additional check that pendulum does using os.path.exists() before it imports the pendulum.locales.en.locale module
    real_os_path_exists = os.path.exists
    try:

        def fake_os_path_exists(path, *args, **kwargs):
            return path.endswith(".zip/pendulum/locales/en") or real_os_path_exists(path, *args, **kwargs)

        os.path.exists = fake_os_path_exists
        importlib.import_module("pendulum")
    finally:
        os.path.exists = real_os_path_exists


__init()
