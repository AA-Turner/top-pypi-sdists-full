__all__ = ['selenium', 'paramiko', 'telegram', 'dropbox', 'util', 'schedule']

__version__ = '0.7.1'

from . import selenium, paramiko, telegram, dropbox, util, schedule

from .util import *

def is_latest_version() -> bool:
    """
    It checks if the current version of the package is the latest version
    :return: A boolean value.
    """
    import feedparser
    feed = feedparser.parse('https://pypi.org/rss/project/scode/releases.xml')
    latest_version = feed.entries[0]['title']
    return __version__ == latest_version


def update_scode() -> None:
    """
    It updates the PATH environment variable to include the Python 3.4 and 3.8 directories, then runs
    the command `python -m pip install -U scode` to update the `scode` package
    """
    import os
    import subprocess
    os.environ['PATH'] = ';'.join(distinct(os.getenv('PATH').split(';') if os.getenv('PATH') else [] + ["C:\\Python38\\Scripts\\", "C:\\Python38\\", "C:\\Python34\\Scripts\\", "C:\\Python34\\"]))
    subprocess.run(['python', '-m', 'pip', 'install', '-U', 'scode'], stdout=subprocess.DEVNULL)


def refresh() -> None:
    """
    It reloads the current module
    """
    import sys
    import importlib
    importlib.reload(sys.modules[__name__])

try:
    is_outdated = not is_latest_version()
except Exception as e:
    try:
        import os, ssl
        if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
            getattr(ssl, '_create_unverified_context', None)): 
            ssl._create_default_https_context = ssl._create_unverified_context
            is_outdated = not is_latest_version()
            
    except Exception as e:
        import warnings
        warnings.warn(f"{type(e).__name__}: Skipped auto update sequence because error occurred while checking the version", Warning)
else:
    if is_outdated:

        try:
            update_scode()
        except Exception as e:
            import warnings
            warnings.warn(f"{type(e).__name__}: Skipped auto update sequence because error occurred while updating", Warning)
        else:
            refresh()
