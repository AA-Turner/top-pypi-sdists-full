from abc import ABCMeta
from abc import abstractmethod


class PowerResourceDriverInterface:
    """ Abstract interface for the PDU resource driver. """

    __metaclass__ = ABCMeta

    @abstractmethod
    def get_inventory(self, context):
        """ Returns a device inventory, which is used by a resource management system to represent this device

        :param context: context from the command which invoked get_inventory
        :returns: The device inventory, including resources, sub-resources and attributes
        :rtype: cloudshell.shell.core.driver_context.AutoLoadDetails
        """
        pass

    @abstractmethod
    def PowerOn(self, context, ports):
        """ Powers on outlets on the managed PDU

        :param context: context from the command which invoked PowerOn
        :param ports: full addresses of outlets on PDU, example: ['192.168.30.128/4', '192.168.30.128/6']
        :type ports: str
        :returns: command result
        :rtype: str
        """
        pass

    @abstractmethod
    def PowerOff(self, context, ports):
        """ Powers off outlets on the managed PDU

        :param context: context from the command which invoked PowerOff
        :param ports: full addresses of outlets on PDU, example: ['192.168.30.128/4', '192.168.30.128/6']
        :type ports: str
        :returns: command result
        :rtype: str
        """
        pass

    @abstractmethod
    def PowerCycle(self, context, ports, delay):
        """ Powers off outlets, waits during delay, then powers outlets on

        :param context: context from the command which invoked PowerCycle
        :param ports: full addresses of outlets on PDU, example: ['192.168.30.128/4', '192.168.30.128/6']
        :type ports: str
        :param delay: seconds to wait after power off
        :type delay: int
        :returns: command result
        :rtype: str
        """
        pass
