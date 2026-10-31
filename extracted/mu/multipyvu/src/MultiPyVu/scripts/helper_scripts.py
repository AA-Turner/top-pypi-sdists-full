"""
A few helpful scripts used in the MultiPyVu module
"""

import os
import shutil
import socket


def get_ip() -> str:
    """
    The IP address for the computer, i.e. the address other machines
    on the network would use to reach this one.

    Returns:
    --------
    String with the IP address
    """
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        try:
            # A UDP connect() doesn't send anything on the wire - it just
            # asks the OS which local interface/address it would use to
            # route to the given destination. This works the same way on
            # Windows, macOS, and Linux, so there's no need to shell out
            # to netsh/ifconfig or guess at interface names.
            sock.connect(('8.8.8.8', 80))
            ip_address = sock.getsockname()[0]
        except OSError:
            ip_address = '127.0.0.1'
    return ip_address


def copy_examples(destination: str) -> str:
    """
    Copies the example scripts installed with MultiPyVu into a folder,
    where they can be edited without being overwritten the next time
    MultiPyVu is upgraded.  The folder is created if it does not exist,
    and files in it with the same names as the examples are replaced.

    Parameters:
    -----------
    destination : str
        The folder to copy the examples into.

    Returns:
    --------
    String with the full path to the copied examples
    """
    source = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                          'examples')
    destination = os.path.abspath(destination)
    # the __init__.py files are only there for packaging, and the logs
    # and .dat files are left behind by running the examples in place
    shutil.copytree(source,
                    destination,
                    ignore=shutil.ignore_patterns('__init__.py',
                                                  '__pycache__',
                                                  '*.log',
                                                  '*.dat'),
                    dirs_exist_ok=True)
    return destination
