"""
A few helpful scripts used in the MultiPyVu module
"""

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
