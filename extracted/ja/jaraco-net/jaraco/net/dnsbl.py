"""
dnsbl: DNS blocklist support
"""

import socket
import argparse


class BlocklistHit:
    def __init__(self, host, blocklist, result):
        self.host = host
        self.blocklist = blocklist
        self.result = result

    def __str__(self):
        return "{host} listed with {blocklist} as {result}".format(**vars(self))


class Service(str):
    """
    Blocklist service. Represents a blocklist service suitable for referencing
    the reputation of potentially malicious or malfeasant hosts.

    Initialize with the domain of the blocklist service or use the classmethod
    Service.get_services to get Services for a commonly-used set of domains.
    """

    service_domains = [
        'dnsbl.jaraco.com',
        'zen.spamhaus.org',
        'ips.backscatterer.org',
        'bl.spamcop.net',
        'list.dsbl.org',
    ]

    @staticmethod
    def reverse_ip(ip):
        return '.'.join(reversed(ip.split('.')))

    def lookup(self, host):
        ip = socket.gethostbyname(host)
        rev_ip = self.reverse_ip(ip)
        key = '.'.join((rev_ip, self))
        try:
            res = socket.gethostbyname(key)
            print(host, 'listed with', self, 'as', res)
        except socket.gaierror:
            return
        return BlocklistHit(host, self, res)

    @classmethod
    def handle_command_line(cls):
        parser = argparse.ArgumentParser()
        parser.add_argument('host')
        args = parser.parse_args()
        cls.lookup_all(args.host)

    @classmethod
    def lookup_all(cls, host):
        services = cls.get_services()
        for service in services:
            res = service.lookup(host)
            if res:
                print(res)

    @classmethod
    def get_services(cls):
        return map(cls, cls.service_domains)


__name__ == '__main__' and Service.handle_command_line()
