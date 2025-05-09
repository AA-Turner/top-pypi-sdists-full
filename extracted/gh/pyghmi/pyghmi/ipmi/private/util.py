# Copyright 2015-2017 Lenovo
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import ctypes
import functools
import os
import socket
import struct

from pyghmi.ipmi.private import constants

try:
    range = xrange
except NameError:
    pass
try:
    buffer
except NameError:
    buffer = memoryview


wintime = None
try:
    wintime = ctypes.windll.kernel32.GetTickCount64
except AttributeError:
    pass


def decode_wireformat_uuid(rawguid, bigendian=False):
    """Decode a wire format UUID

    It handles the rather particular scheme where half is little endian
    and half is big endian.  It returns a string like dmidecode would output.
    """
    if isinstance(rawguid, list):
        rawguid = bytearray(rawguid)
    endian = '<IHH'  # little endian
    if bigendian:
        endian = '>IHH'  # big endian
    lebytes = struct.unpack_from(endian, buffer(rawguid[:8]))
    bebytes = struct.unpack_from('>HHI', buffer(rawguid[8:]))
    return '{0:08X}-{1:04X}-{2:04X}-{3:04X}-{4:04X}{5:08X}'.format(
        lebytes[0], lebytes[1], lebytes[2], bebytes[0], bebytes[1], bebytes[2])


def urlsplit(url):
    """Split an arbitrary url into protocol, host, rest

    The standard urlsplit does not want to provide 'netloc' for arbitrary
    protocols, this works around that.

    :param url: The url to split into component parts
    """
    proto, rest = url.split(':', 1)
    host = ''
    if rest[:2] == '//':
        host, rest = rest[2:].split('/', 1)
        rest = '/' + rest
    return proto, host, rest


def get_ipv4(hostname):
    """Get list of ipv4 addresses for hostname

    """
    addrinfo = socket.getaddrinfo(hostname, None, socket.AF_INET,
                                  socket.SOCK_STREAM)
    return [addrinfo[x][4][0] for x in range(len(addrinfo))]


def get_ipmi_error(response, suffix=""):
    if 'error' in response:
        return response['error'] + suffix
    code = response['code']
    if code == 0:
        return False
    command = response['command']
    netfn = response['netfn']
    if ((netfn, command) in constants.command_completion_codes
            and code in constants.command_completion_codes[(netfn, command)]):
        res = constants.command_completion_codes[(netfn, command)][code]
        res += suffix
    elif code in constants.ipmi_completion_codes:
        res = constants.ipmi_completion_codes[code] + suffix
    else:
        res = "Unknown code 0x%2x encountered" % code
    return res


def _monotonic_time():
    """Provides a monotonic timer

    This code is concerned with relative, not absolute time.
    This function facilitates that prior to python 3.3
    """
    # Python does not provide one until 3.3, so we make do
    # for most OSes, os.times()[4] works well.
    # for microsoft, GetTickCount64
    if wintime:
        return wintime() / 1000.0
    return os.times()[4]


class protect(object):

    def __init__(self, lock):
        self.lock = lock

    def __call__(self, func):
        @functools.wraps(func)
        def _wrapper(*args, **kwargs):
            self.lock.acquire()
            try:
                return func(*args, **kwargs)
            finally:
                self.lock.release()
        return _wrapper

    def __enter__(self):
        self.lock.acquire()

    def __exit__(self, exc_type, exc_value, traceback):
        self.lock.release()
