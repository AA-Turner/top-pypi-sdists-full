import ctypes
import struct
from ctypes.wintypes import DWORD, BYTE, WCHAR

from .base import BaseManager

# select constants
# error.h
NO_ERROR = 0
ERROR_INSUFFICIENT_BUFFER = 122
ERROR_INVALID_PARAMETER = 87
ERROR_NOT_SUPPORTED = 50

# mprapi.h
MAX_INTERFACE_NAME_LEN = 256

# iprtrmib.h
MAXLEN_PHYSADDR = 8
MAXLEN_IFDESCR = 256


class MIB_IFROW(ctypes.Structure):
    _fields_ = (
        ('name', WCHAR * MAX_INTERFACE_NAME_LEN),
        ('index', DWORD),
        ('type', DWORD),
        ('MTU', DWORD),
        ('speed', DWORD),
        ('physical_address_length', DWORD),
        ('physical_address_raw', BYTE * MAXLEN_PHYSADDR),
        ('admin_status', DWORD),
        ('operational_status', DWORD),
        ('last_change', DWORD),
        ('octets_received', DWORD),
        ('unicast_packets_received', DWORD),
        ('non_unicast_packets_received', DWORD),
        ('incoming_discards', DWORD),
        ('incoming_errors', DWORD),
        ('incoming_unknown_protocols', DWORD),
        ('octets_sent', DWORD),
        ('unicast_packets_sent', DWORD),
        ('non_unicast_packets_sent', DWORD),
        ('outgoing_discards', DWORD),
        ('outgoing_errors', DWORD),
        ('outgoing_queue_length', DWORD),
        ('description_length', DWORD),
        ('description_raw', ctypes.c_char * MAXLEN_IFDESCR),
    )

    def get_variable_length_property(self, name):
        val = getattr(self, name + '_raw')
        length = getattr(self, name + '_length')
        return memoryview(val).tobytes()[:length]

    @property
    def physical_address(self):
        return self.get_variable_length_property('physical_address')

    @property
    def description(self):
        return self.get_variable_length_property('description')


class MIB_IFTABLE(ctypes.Structure):
    _fields_ = (
        ('num_entries', DWORD),  # dwNumEntries
        ('entries', MIB_IFROW * 0),  # table
    )


class MIB_IPADDRROW(ctypes.Structure):
    _fields_ = (
        ('address', DWORD),
        ('index', DWORD),
        ('mask', DWORD),
        ('broadcast_address', DWORD),
        ('reassembly_size', DWORD),
        ('unused', ctypes.c_ushort),
        ('type', ctypes.c_ushort),
    )


class MIB_IPADDRTABLE(ctypes.Structure):
    _fields_ = (('num_entries', DWORD), ('entries', MIB_IPADDRROW * 0))


ip_helper = ctypes.windll.iphlpapi


class AllocatingTable:
    """
    Microsoft uses a consistent interface to retrieve arrays of structures of
    unknown length. This class abstracts that functionality so that it
    can be used to retrieve table entries using different API calls.
    """

    def __get_table_length(self):
        """
        Call the retrieval method with a null pointer and length of
        zero.  This should cause the 'insufficient buffer' error and
        return the size of the buffer needed.
        """
        length = DWORD()
        res = self.method(None, ctypes.byref(length), False)
        if res != ERROR_INSUFFICIENT_BUFFER:
            raise RuntimeError("Error getting table length (%d)" % res)
        return length.value

    def get_table(self):
        """
        Retrieve the complete table for the given method and structures.
        """
        buffer_length = self.__get_table_length()
        returned_buffer_length = DWORD(buffer_length)
        buffer = (ctypes.c_byte * buffer_length)()
        res = self.method(
            ctypes.byref(buffer), ctypes.byref(returned_buffer_length), False
        )
        if res != NO_ERROR:
            raise RuntimeError("Error retrieving table (%d)" % res)
        pointer_type = ctypes.POINTER(self.structure)
        return ctypes.cast(buffer, pointer_type).contents

    def get_entries(self):
        """
        Cast the result to an array of the size indicated by the container
        structure.
        """
        table = self.get_table()
        entries_array = self.row_structure * table.num_entries
        pointer_type = ctypes.POINTER(entries_array)
        return ctypes.cast(table.entries, pointer_type).contents

    entries = property(get_entries)


class InterfaceTable(AllocatingTable):
    method = ip_helper.GetIfTable
    structure = MIB_IFTABLE
    row_structure = MIB_IFROW


class AddressTable(AllocatingTable):
    method = ip_helper.GetIpAddrTable
    structure = MIB_IPADDRTABLE
    row_structure = MIB_IPADDRROW


class Manager(BaseManager):
    def get_host_mac_addresses(self):
        for entry in InterfaceTable().entries:
            if entry.physical_address:
                yield entry.physical_address

    def get_host_ip_addresses(self):
        for entry in AddressTable().entries:
            yield struct.pack('L', entry.address)
