"""
KIRA interface to send UDP packets to a Keene Electronics IR-IP bridge.
"""
# pylint: disable=import-error
import socket
import sys
import time

from . import utils

from .constants import (
    DEFAULT_PORT
)

class KiraModule(object):
    """
    Construct and send IR-IP packets.
    """

    def __init__(self, host, port=DEFAULT_PORT):
        """Construct a KIRA interface object."""
        self.host = host
        self.port = port
        self.codeMap = {}

    def registerCode(self, codeName, code, codeType=None):
        rawCode = utils.code2kira(code, codeType=codeType)
        if rawCode:
            self.codeMap[codeName] = rawCode

    def sendCode(self, codeName, repeat=1, delay=0.05):
        code = self.codeMap.get(codeName)
        if code:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.connect((self.host, self.port))
            if sys.version_info[0] == 2:
                code = "%s\n" % code
            else:
                code = bytes("%s\n" % code, "ascii")
            for i in range(repeat):
                sock.send(code)
                time.sleep(delay)
            sock.close()
