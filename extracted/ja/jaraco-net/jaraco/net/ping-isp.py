import itertools
import socket
import importlib
import functools

import autocommand
import icmplib


def is_router(addr):
    return addr.startswith('192.168') or 'amplifi' in socket.gethostbyaddr(addr)


def _patch_traceroute_privilege():
    """
    Force the socket objects to disable privilege.
    """
    module = importlib.import_module('icmplib.traceroute')
    module.ICMPv4Socket = functools.partial(module.ICMPv4Socket, privileged=False)
    module.ICMPv6Socket = functools.partial(module.ICMPv6Socket, privileged=False)


@autocommand.autocommand(__name__)
def main():
    """
    Detect the ISP and ping it for some stats.
    """
    _patch_traceroute_privilege()
    trace = icmplib.traceroute('1.1.1.1', max_hops=3, fast=True)
    addresses = (hop.address for hop in trace)
    ISP = next(itertools.filterfalse(is_router, addresses))
    print('pinging', ISP, f'({socket.gethostbyaddr(ISP)[0]})')
    host = icmplib.ping(ISP, count=30, privileged=False)
    print(host)
