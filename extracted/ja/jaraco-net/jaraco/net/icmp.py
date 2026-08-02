import sys
import socket
import time
import datetime

import icmplib


def ping(dest_addr, timeout=2):
    """
    Send an ICMP Echo request to a host and return how long it takes.

    Raise socket.timeout if no response is received within timeout.

    >>> ping('127.0.0.1')
    datetime.timedelta(...)

    >>> ping('10.10.10.254', timeout=.01)
    Traceback (most recent call last):
    ...
    TimeoutError: timed out
    """
    host = icmplib.ping(dest_addr, count=1, timeout=timeout, privileged=False)
    if not host.is_alive:
        raise socket.timeout('timed out')
    return datetime.timedelta(host.rtts[0])


def wait_for_host(host):
    """
    Continuously wait for a host until it becomes available. When it does,
    return the datetime when it occurred.
    """
    while True:
        try:
            ping(host)
            break
        except OSError:
            pass
    return datetime.datetime.now(datetime.timezone.utc)


def monitor_cmd():
    try:
        monitor_hosts(sys.argv[1:])
    except KeyboardInterrupt:
        pass


def monitor_hosts(hosts):
    while True:
        for host in hosts:
            try:
                delay = ping(host)
            except socket.timeout:
                delay = None
            except OSError as exc:
                delay = str(exc)
            save_result(host, delay)
        time.sleep(3)


def save_result(host, delay):
    with open('ping-results.txt', 'a') as res:
        ts = datetime.datetime.now()
        msg = 'time: {ts}, host: {host}, res: {delay}'.format(
            ts=ts, host=host, delay=delay
        )
        print(msg, file=res)


if __name__ == '__main__':
    monitor_cmd()
