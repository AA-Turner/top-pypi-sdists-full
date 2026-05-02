from abc import ABCMeta
from abc import abstractmethod


class PDUFactory:
    """ Interacts with PDU device returning its inventory, as well as objects that manage its outlets """

    __metaclass__ = ABCMeta

    @abstractmethod
    def get_outlets(self):
        """ Outlets are outgoing power sockets that provide power to remote devices that are connected to PDU.

        :returns: a collection of outlets that are capable of powering on and off
        :rtype: list(cloudshell.power.pdu.device.outlet.Outlet)
        """
        pass

    @abstractmethod
    def get_inventory(self):
        """ Returns a device inventory, which is used by a resource management system to represent this device

        :returns: The device inventory, including resources, sub-resources and attributes
        :rtype: cloudshell.shell.core.driver_context.AutoLoadDetails
        """
        pass