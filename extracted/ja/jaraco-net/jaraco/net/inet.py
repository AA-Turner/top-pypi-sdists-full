"""
inet.py

Tools for IP communication.

Objects:
    PortScanner: scans a range of ports
    PortListener: listens on a port
    PortRangeListener: listens on a range of ports
"""

import threading
import socket
import sys
import operator
import time
import logging
import functools
from typing import List

from more_itertools.recipes import consume

from . import icmp

log = logging.getLogger(__name__)


class PortScanner:
    def __init__(self):
        self.ranges = [range(1, 1024)]
        self.n_threads = 100

    def set_range(self, *r):
        self.ranges = [range(*r)]

    def add_range(self, *r):
        self.ranges.append(range(*r))


class ScanThread(threading.Thread):
    all_testers: List[threading.Thread] = []

    def __init__(self, address):
        threading.Thread.__init__(self)
        self.address = address

    def run(self):
        ScanThread.all_testers.append(self)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect(self.address)
            s.close()
            self.result = True
        except OSError:
            self.result = False

        self.report()

    def __unicode__(self):
        msg_map = {
            True: '{address} connection established.',
            False: '{address} connection failed.',
            None: '{address} no result obtained.',
        }
        msg_fmt = msg_map[getattr(self, 'result', None)]
        return msg_fmt.format(**vars(self))

    def report(self):
        log_method_map = {True: log.info, False: log.debug, None: log.error}
        log_method = log_method_map[getattr(self, 'result', None)]
        log_method(str(self))

    @staticmethod
    def wait_for_testers_to_finish():
        map(lambda x: x.join(), ScanThread.all_testers)


def portscan_hosts(hosts, *args, **kargs):
    consume(map(lambda h: portscan(h, *args, **kargs), hosts))


def portscan(host, ports=range(1024), frequency=20):
    def make_address(port):
        return host, port

    addresses = map(make_address, ports)
    testers = map(ScanThread, addresses)
    for tester in testers:
        log.debug('starting tester')
        tester.start()
        time.sleep(1 / frequency)


class PortListener(threading.Thread):
    def __init__(self, port):
        threading.Thread.__init__(self)
        self.port = port
        self.setDaemon(1)
        self.output = sys.stdout

    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.bind(('', self.port))
            s.listen(1)
            while 1:
                conn, addr = s.accept()
                self.output.write(f'Received connection on {self.port} from {addr}.\n')
                conn.close()
        except OSError as e:
            if e[0] == 10048:
                self.output.write(
                    'Cannot listen on port %d: Address already in use.\n' % self.port
                )
            else:
                raise


class PortRangeListener:
    def __init__(self):
        self.ranges = [range(1, 1024)]

    def listen(self):
        ports = functools.reduce(operator.add, self.ranges)
        ports.sort()
        self.threads = map(PortListener, ports)
        [t.start for t in self.threads]


def ping_host(host):
    try:
        icmp.ping(host)
        msg = f"{host} is online"
    except OSError:
        msg = f"Either {host} is offline or ping request has been blocked."
    print(msg)
