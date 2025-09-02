"""
Utilities for working with networking devices defined based upon the platform
being run upon
"""

import sys


class BaseManager:
    """
    A base network manager class.

    Defines the methods a consumer application might require.  Each
    raises NotImplementedError except in subclasses.
    """

    @staticmethod
    def hardware_address_to_string(addr):
        """
        Convert a hardware address to a string.
        """
        return ':'.join('%02x' % ord(byte) for byte in addr)

    @staticmethod
    def ip_address_to_string(addr):
        """
        Convert an IPv4 address into a string.
        """
        assert len(addr) == 4, "Only IPv4 addresses are supported at this time"
        return '.'.join('%d' % ord(byte) for byte in addr)

    def get_host_mac_address_strings(self):
        """
        Iterate over the MAC address strings for the host. These are
        strings of six pairs of hex digits separated by colons.
        """
        return map(self.hardware_address_to_string, self.get_host_mac_addresses())

    def get_host_mac_addresses(self):
        """
        Get the MAC addresses for the host.
        """
        raise NotImplementedError("Not implemented on platform %s" % sys.platform)

    def get_host_ip_address_strings(self):
        """
        Iterate over the IP address strings for the host.  These are
        strings of four integers in the range [0, 255] separated by
        periods.
        """
        return map(self.ip_address_to_string, self.get_host_ip_addresses())

    def get_host_ip_addresses(self):
        """
        Get the IP addresses of the host.
        """
        raise NotImplementedError("Not implemented on platform %s" % sys.platform)
