import subprocess
import operator

import ifconfigparser

from .base import BaseManager


def if_config():
    cfg = subprocess.check_output(['ifconfig'], text=True, encoding='utf-8')
    return ifconfigparser.IfconfigParser(cfg)


class Manager(BaseManager):
    def get_host_mac_addresses(self):
        return self._iface_values('mac_addr')

    def get_host_ip_addresses(self):
        return self._iface_values('ipv4_addr')

    @staticmethod
    def _iface_values(key):
        ifaces = if_config().get_interfaces().values()
        return filter(None, map(operator.attrgetter(key), ifaces))
