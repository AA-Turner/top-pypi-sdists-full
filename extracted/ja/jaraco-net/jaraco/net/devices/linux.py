"""
Network Manager for Linux
"""

import ctypes
import socket

from .base import BaseManager

# select constants
IFNAMSIZ = 16
SIOCGIFCONF = 0x8912
SIOCGIFFLAGS = 0x8913
SIOCGIFADDR = 0x8915
SIOCGIFHWADDR = 0x8927
IFF_LOOPBACK = 0x8

sa_family_t = ctypes.c_ushort


class sockaddr(ctypes.Structure):
    _fields_ = (('family', sa_family_t), ('data', ctypes.c_byte * 14))


class ifr_map(ctypes.Structure):
    _fields_ = (
        ('mem_start', ctypes.c_ulong),
        ('mem_end', ctypes.c_ulong),
        ('base_addr', ctypes.c_ushort),
        ('irq', ctypes.c_char),
        ('dma', ctypes.c_char),
        ('port', ctypes.c_char),
    )


class ifreq_union(ctypes.Union):
    _fields_ = (
        ('addr', sockaddr),
        ('dest_addr', sockaddr),
        ('broadcast_addr', sockaddr),
        ('netmask', sockaddr),
        ('hardware_addr', sockaddr),
        ('flags', ctypes.c_ushort),
        ('if_index', ctypes.c_int),
        ('metric', ctypes.c_int),
        ('mtu', ctypes.c_int),
        ('map', ifr_map),
        ('slave', ctypes.c_char * IFNAMSIZ),
        ('new_name', ctypes.c_char * IFNAMSIZ),
        ('data', ctypes.c_char_p),
    )


class ifreq(ctypes.Structure):
    _fields_ = (('name', ctypes.c_char * IFNAMSIZ), ('detail', ifreq_union))


p_ifreq = ctypes.POINTER(ifreq)


class ifconf(ctypes.Structure):
    _fields_ = (('length', ctypes.c_int), ('req', p_ifreq))


libc = ctypes.cdll.LoadLibrary('libc.so.6')
ioctl = libc.ioctl


def get_interfaces():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    buf = ctypes.create_string_buffer(1024)
    ifc = ifconf()
    ifc.length = 1024
    ifc.req = ctypes.cast(buf, p_ifreq)
    ioctl(s.fileno(), SIOCGIFCONF, ctypes.byref(ifc))
    n_records = ifc.length // ctypes.sizeof(ifreq)
    for index in range(n_records):
        rec = ifc.req[index]
        yield str(rec.name)


def get_hardware_addresses(if_names):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    for name in if_names:
        ifr = ifreq(name.encode())
        res = ioctl(s.fileno(), SIOCGIFFLAGS, ctypes.byref(ifr))
        if res != 0:
            continue
        if ifr.detail.flags & IFF_LOOPBACK:
            continue
        res = ioctl(s.fileno(), SIOCGIFHWADDR, ctypes.byref(ifr))
        if res != 0:
            continue
        yield memoryview(ifr.detail.hardware_addr.data).tobytes()[:6]


def get_ip_addresses(if_names):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    for name in if_names:
        ifr = ifreq(name.encode())
        res = ioctl(s.fileno(), SIOCGIFADDR, ctypes.byref(ifr))
        if res != 0:
            continue
        yield memoryview(ifr.detail.addr.data).tobytes()[2:6]


class Manager(BaseManager):
    def get_host_mac_addresses(self):
        return get_hardware_addresses(get_interfaces())

    def get_host_ip_addresses(self):
        return get_ip_addresses(get_interfaces())
