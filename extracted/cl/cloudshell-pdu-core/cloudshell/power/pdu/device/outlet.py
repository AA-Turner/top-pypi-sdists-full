from abc import ABCMeta
from abc import abstractmethod


class Outlet:
    """ Interface for outlet, an outgoing power socket on PDU which is connected to a remote device """

    __metaclass__ = ABCMeta

    @abstractmethod
    def power_on(self):
        pass

    @abstractmethod
    def power_off(self):
        pass
