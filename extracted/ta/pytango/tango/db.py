# SPDX-FileCopyrightText: All Contributors to the PyTango project
# SPDX-License-Identifier: LGPL-3.0-or-later

"""
This is an internal PyTango module.
"""

__all__ = ("db_init",)

__docformat__ = "restructuredtext"

import collections.abc

from tango import (
    StdStringVector,
    Database,
    DbDatum,
    DbData,
    DbDevInfo,
    DbDevInfos,
    DbDevExportInfo,
    DbDevExportInfos,
)

from tango.utils import (
    _trace_client,
    is_non_str_seq,
    seq_2_DbDevInfos,
    seq_2_DbDevExportInfos,
    seq_2_DbData,
    DbData_2_dict,
    parameter_2_dbdata,
)

# -~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-
# DbDatum extension
# -~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-


def __DbDatum___setitem(self, k, v):
    self.value_string[k] = v


def __DbDatum___delitem(self, k):
    self.value_string.__delitem__(k)


def __DbDatum_append(self, v):
    self.value_string.append(v)


def __DbDatum_extend(self, v):
    self.value_string.extend(v)


def __DbDatum___imul(self, n):
    self.value_string *= n


def __init_DbDatum():
    DbDatum.__len__ = lambda self: len(self.value_string)
    DbDatum.__getitem__ = lambda self, k: self.value_string[k]
    DbDatum.__setitem__ = __DbDatum___setitem
    DbDatum.__delitem__ = __DbDatum___delitem
    DbDatum.__iter__ = lambda self: self.value_string.__iter__()
    DbDatum.__contains__ = lambda self, v: self.value_string.__contains__(v)
    DbDatum.__add__ = lambda self, seq: self.value_string + seq
    DbDatum.__mul__ = lambda self, n: self.value_string * n
    DbDatum.__imul__ = __DbDatum___imul
    DbDatum.append = __DbDatum_append
    DbDatum.extend = __DbDatum_extend


#    DbDatum.__str__      = __DbDatum___str__
#    DbDatum.__repr__      = __DbDatum___repr__

# -~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-
# Database extension
# -~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-


def __Database__add_server(self, servname, dev_info, with_dserver=False):
    """
    add_server( self, servname, dev_info, with_dserver=False) -> None

            Add a (group of) devices to the database. This is considered as a
            low level call because it may render the database inconsistent
            if it is not used properly.

            If *with_dserver* parameter is set to False (default), this
            call will only register the given dev_info(s). You should include
            in the list of dev_info an entry to the usually hidden **DServer**
            device.

            If *with_dserver* parameter is set to True, the call will add an
            additional **DServer** device if it is not included in the
            *dev_info* parameter.

        Example using *with_dserver=True*::

            dev_info1 = DbDevInfo()
            dev_info1.name = 'my/own/device'
            dev_info1._class = 'MyDevice'
            dev_info1.server = 'MyServer/test'
            db.add_server(dev_info1.server, dev_info1, with_dserver=True)

        Same example using *with_dserver=False*::

            dev_info1 = DbDevInfo()
            dev_info1.name = 'my/own/device'
            dev_info1._class = 'MyDevice'
            dev_info1.server = 'MyServer/test'

            dev_info2 = DbDevInfo()
            dev_info2.name = 'dserver/' + dev_info1.server
            dev_info2._class = 'DServer
            dev_info2.server = dev_info1.server

            dev_info = dev_info1, dev_info2
            db.add_server(dev_info1.server, dev_info)

        .. versionadded:: 8.1.7
            added *with_dserver* parameter

        Parameters :
            - servname : (str) server name
            - dev_info : (sequence<DbDevInfo> | DbDevInfos | DbDevInfo) containing the server device(s) information
            - with_dserver: (bool) whether or not to auto create **DServer** device in server
        Return     : None

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)
    """

    if not isinstance(dev_info, collections.abc.Sequence) and not isinstance(
        dev_info, DbDevInfo
    ):
        raise TypeError("Value must be a DbDevInfos, a seq<DbDevInfo> or a DbDevInfo")

    if isinstance(dev_info, DbDevInfos):
        pass
    elif isinstance(dev_info, DbDevInfo):
        dev_info = seq_2_DbDevInfos((dev_info,))
    else:
        dev_info = seq_2_DbDevInfos(dev_info)
    if with_dserver:
        has_dserver = False
        for i in dev_info:
            if i._class == "DServer":
                has_dserver = True
                break
        if not has_dserver:
            dserver_info = DbDevInfo()
            dserver_info.name = "dserver/" + dev_info[0].server
            dserver_info._class = "DServer"
            dserver_info.server = dev_info[0].server
            dev_info.append(dserver_info)
    self._add_server(servname, dev_info)


def __Database__export_server(self, dev_info):
    """
    export_server(self, dev_info) -> None

            Export a group of devices to the database.

        Parameters :
            - devinfo : (sequence<DbDevExportInfo> | DbDevExportInfos | DbDevExportInfo)
                        containing the device(s) to export information
        Return     : None

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)
    """

    if not isinstance(dev_info, collections.abc.Sequence) and not isinstance(
        dev_info, DbDevExportInfo
    ):
        raise TypeError(
            "Value must be a DbDevExportInfos, a seq<DbDevExportInfo> or "
            "a DbDevExportInfo"
        )

    if isinstance(dev_info, DbDevExportInfos):
        pass
    elif isinstance(dev_info, DbDevExportInfo):
        dev_info = seq_2_DbDevExportInfos(
            (dev_info),
        )
    else:
        dev_info = seq_2_DbDevExportInfos(dev_info)
    self._export_server(dev_info)


def __generic_get_property(obj_name, value, f):
    new_value = parameter_2_dbdata(value, "value")
    f(obj_name, new_value)
    return new_value, value if isinstance(value, collections.abc.Mapping) else {}


def __Database__generic_get_property(self, obj_name, value, f):
    """internal usage"""

    new_value, ret = __generic_get_property(obj_name, value, f)
    return DbData_2_dict(new_value, ret)


def __Database__generic_put_property(self, obj_name, value, f):
    """internal usage"""
    value = parameter_2_dbdata(value, "value")
    return f(obj_name, value)


def __Database__generic_delete_property(self, obj_name, value, f):
    """internal usage"""
    value = parameter_2_dbdata(value, "value")
    return f(obj_name, value)


def __Database__generic_get_attr_pipe_property(self, obj_name, value, f):
    """internal usage for class or device attribute and pipe properties."""

    new_value, ret = __generic_get_property(obj_name, value, f)
    nb_items = len(new_value)
    i = 0
    while i < nb_items:
        db_datum = new_value[i]
        curr_dict = {}
        ret[db_datum.name] = curr_dict
        nb_props = int(db_datum[0])
        i += 1
        for k in range(nb_props):
            db_datum = new_value[i]
            curr_dict[db_datum.name] = db_datum.value_string
            i += 1

    return ret


def __Database__generic_put_attr_pipe_property(self, obj_name, value, f):
    """internal usage for class or device attribute and pipe properties."""
    new_value = parameter_2_dbdata(value, "value")
    return f(obj_name, new_value)


def __Database__generic_delete_attr_pipe_property(self, obj_name, value, f):
    """internal usage for class or device attribute and pipe properties."""
    if isinstance(value, DbData):
        f(obj_name, value)
    elif is_non_str_seq(value):
        f(obj_name, seq_2_DbData(value))
    elif isinstance(value, collections.abc.Mapping):
        for attr_pipe_name, properties in value.items():
            new_value = DbData()
            new_value.append(DbDatum(attr_pipe_name))
            for prop in properties:
                new_value.append(DbDatum(prop))
            f(obj_name, new_value)
    else:
        raise TypeError(
            "Value must be a string, tango.DbDatum, "
            "tango.DbData, a sequence or a dictionary"
        )


def __Database__put_property(self, obj_name, value):
    """
    put_property(self, obj_name, value) -> None

        Insert or update a list of properties for the specified object.

    Parameters :
        - obj_name : (str) object name
        - value : can be one of the following:

            1. DbDatum - single property data to be inserted
            2. DbData - several property data to be inserted
            3. sequence<DbDatum> - several property data to be inserted
            4. dict<str, DbDatum> - keys are property names and value has data to be inserted
            5. dict<str, obj> - keys are property names and str(obj) is property value
            6. dict<str, seq<str>> - keys are property names and value has data to be inserted
    Return     : None

    Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)
    """

    return __Database__generic_put_property(self, obj_name, value, self._put_property)


def __Database__get_property(self, obj_name, value):
    """
    get_property(self, obj_name, value) -> dict<str, seq<str>>

            Query the database for a list of object (i.e non-device) properties.

        Parameters :
            - obj_name : (str) object name
            - value : can be one of the following:

                1. str [in] - single property data to be fetched
                2. DbDatum [in] - single property data to be fetched
                3. DbData [in,out] - several property data to be fetched
                   In this case (direct C++ API) the DbData will be filled with
                   the property values
                4. sequence<str> [in] - several property data to be fetched
                5. sequence<DbDatum> [in] - several property data to be fetched
                6. dict<str, obj> [in,out] - keys are property names
                   In this case the given dict values will be changed to contain
                   the several property values

        Return     : a dictionary which keys are the property names the value
                     associated with each key being a a sequence of strings being
                     the property value.

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)
    """
    return __Database__generic_get_property(self, obj_name, value, self._get_property)


def __Database__get_property_forced(self, obj_name, value):
    return __Database__generic_get_property(
        self, obj_name, value, self._get_property_forced
    )


__Database__get_property_forced.__doc__ = __Database__get_property.__doc__


def __Database__delete_property(self, obj_name, value):
    """
    delete_property(self, obj_name, value) -> None

            Delete a the given of properties for the specified object.

        Parameters :
            - obj_name : (str) object name
            - value : can be one of the following:

                1. str [in] - single property data to be deleted
                2. DbDatum [in] - single property data to be deleted
                3. DbData [in] - several property data to be deleted
                4. sequence<string> [in]- several property data to be deleted
                5. sequence<DbDatum> [in] - several property data to be deleted
                6. dict<str, obj> [in] - keys are property names to be deleted
                   (values are ignored)
                7. dict<str, DbDatum> [in] - several DbDatum.name are property names
                   to be deleted (keys are ignored)
        Return     : None

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)
    """
    return __Database__generic_delete_property(
        self, obj_name, value, self._delete_property
    )


def __Database__get_device_property(self, dev_name, value):
    """
    get_device_property(self, dev_name, value) -> dict<str, seq<str>>

        Query the database for a list of device properties.

        Parameters :
            - dev_name : (str) object name
            - value : can be one of the following:

                1. str [in] - single property data to be fetched
                2. DbDatum [in] - single property data to be fetched
                3. DbData [in,out] - several property data to be fetched
                   In this case (direct C++ API) the DbData will be filled with
                   the property values
                4. sequence<str> [in] - several property data to be fetched
                5. sequence<DbDatum> [in] - several property data to be fetched
                6. dict<str, obj> [in,out] - keys are property names
                   In this case the given dict values will be changed to contain
                   the several property values

        Return     : a dictionary which keys are the property names the value
                    associated with each key being a a sequence of strings being the
                    property value.

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)
    """
    return __Database__generic_get_property(
        self, dev_name, value, self._get_device_property
    )


def __Database__put_device_property(self, dev_name, value):
    """
    put_device_property(self, dev_name, value) -> None

        Insert or update a list of properties for the specified device.

        Parameters :
            - dev_name : (str) object name
            - value : can be one of the following:

                1. DbDatum - single property data to be inserted
                2. DbData - several property data to be inserted
                3. sequence<DbDatum> - several property data to be inserted
                4. dict<str, DbDatum> - keys are property names and value has data to be inserted
                5. dict<str, obj> - keys are property names and str(obj) is property value
                6. dict<str, seq<str>> - keys are property names and value has data to be inserted
        Return     : None

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)
    """
    return __Database__generic_put_property(
        self, dev_name, value, self._put_device_property
    )


def __Database__delete_device_property(self, dev_name, value):
    """
    delete_device_property(self, dev_name, value) -> None

        Delete a the given of properties for the specified device.

        Parameters :
            - dev_name : (str) object name
            - value : can be one of the following:

                1. str [in] - single property data to be deleted
                2. DbDatum [in] - single property data to be deleted
                3. DbData [in] - several property data to be deleted
                4. sequence<str> [in]- several property data to be deleted
                5. sequence<DbDatum> [in] - several property data to be deleted
                6. dict<str, obj> [in] - keys are property names to be deleted (values are ignored)
                7. dict<str, DbDatum> [in] - several DbDatum.name are property names to be deleted (keys are ignored)

        Return     : None

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)
    """
    return __Database__generic_delete_property(
        self, dev_name, value, self._delete_device_property
    )


def __Database__get_device_property_list(self, dev_name, wildcard, array=None):
    """
    get_device_property_list(self, dev_name, wildcard, array=None) -> DbData

            Query the database for a list of properties defined for the
            specified device and which match the specified wildcard.
            If array parameter is given, it must be an object implementing de 'append'
            method. If given, it is filled with the matching property names. If not given
            the method returns a new DbDatum containing the matching property names.

        New in PyTango 7.0.0

        Parameters :
            - dev_name : (str) device name
            - wildcard : (str) property name wildcard
            - array : [out] (sequence) (optional) array that
                          will contain the matching property names.
        Return     : if container is None, return is a new DbDatum containing the
                     matching property names. Otherwise returns the given array
                     filled with the property names

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device"""
    if array is None:
        return self._get_device_property_list(dev_name, wildcard)
    elif isinstance(array, StdStringVector):
        return self._get_device_property_list(dev_name, wildcard, array)
    elif is_non_str_seq(array):
        res = self._get_device_property_list(dev_name, wildcard)
        for e in res:
            array.append(e)
        return array


def __Database__get_device_attribute_property(self, dev_name, value):
    """
    get_device_attribute_property(self, dev_name, value) -> dict<str, dict<str, seq<str>>>

            Query the database for a list of device attribute properties for the
            specified device. The method returns all the properties for the specified
            attributes.

        Parameters :
            - dev_name : (string) device name
            - value : can be one of the following:

                1. str [in] - single attribute properties to be fetched
                2. DbDatum [in] - single attribute properties to be fetched
                3. DbData [in,out] - several attribute properties to be fetched
                   In this case (direct C++ API) the DbData will be filled with
                   the property values
                4. sequence<str> [in] - several attribute properties to be fetched
                5. sequence<DbDatum> [in] - several attribute properties to be fetched
                6. dict<str, obj> [in,out] - keys are attribute names
                   In this case the given dict values will be changed to contain the
                   several attribute property values

        Return     :  a dictionary which keys are the attribute names the
                             value associated with each key being a another
                             dictionary where keys are property names and value is
                             a DbDatum containing the property value.

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)
    """
    return __Database__generic_get_attr_pipe_property(
        self, dev_name, value, self._get_device_attribute_property
    )


def __Database__get_device_pipe_property(self, dev_name, value):
    """
    get_device_pipe_property(self, dev_name, value) -> dict<str, dict<str, seq<str>>>

            Query the database for a list of device pipe properties for the
            specified device. The method returns all the properties for the specified
            pipes.

        Parameters :
            - dev_name : (string) device name
            - value : can be one of the following:

                1. str [in] - single pipe properties to be fetched
                2. DbDatum [in] - single pipe properties to be fetched
                3. DbData [in,out] - several pipe properties to be fetched
                   In this case (direct C++ API) the DbData will be filled with
                   the property values
                4. sequence<str> [in] - several pipe properties to be fetched
                5. sequence<DbDatum> [in] - several pipe properties to be fetched
                6. dict<str, obj> [in,out] - keys are pipe names
                   In this case the given dict values will be changed to contain the
                   several pipe property values

        Return     :  a dictionary which keys are the pipe names the
                             value associated with each key being a another
                             dictionary where keys are property names and value is
                             a DbDatum containing the property value.

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)
    """
    return __Database__generic_get_attr_pipe_property(
        self, dev_name, value, self._get_device_pipe_property
    )


def __Database__put_device_attribute_property(self, dev_name, value):
    """
    put_device_attribute_property( self, dev_name, value) -> None

            Insert or update a list of properties for the specified device.

        Parameters :
            - dev_name : (str) device name
            - value : can be one of the following:

                1. DbData - several property data to be inserted
                2. sequence<DbDatum> - several property data to be inserted
                3. dict<str, dict<str, obj>> keys are attribute names and value being another
                   dictionary which keys are the attribute property names and the value
                   associated with each key being seq<str> or tango.DbDatum.

        Return     : None

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)
    """
    return __Database__generic_put_attr_pipe_property(
        self, dev_name, value, self._put_device_attribute_property
    )


def __Database__put_device_pipe_property(self, dev_name, value):
    """
    put_device_pipe_property( self, dev_name, value) -> None

            Insert or update a list of properties for the specified device.

        Parameters :
            - dev_name : (str) device name
            - value : can be one of the following:

                1. DbData - several property data to be inserted
                2. sequence<DbDatum> - several property data to be inserted
                3. dict<str, dict<str, obj>> keys are pipe names and value being another
                   dictionary which keys are the pipe property names and the value
                   associated with each key being seq<str> or tango.DbDatum.

        Return     : None

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)
    """
    return __Database__generic_put_attr_pipe_property(
        self, dev_name, value, self._put_device_pipe_property
    )


def __Database__delete_device_attribute_property(self, dev_name, value):
    """
    delete_device_attribute_property(self, dev_name, value) -> None

            Delete a list of attribute properties for the specified device.

        Parameters :
            - devname : (str) device name
            - propnames : can be one of the following:

                1. DbData [in] - several property data to be deleted
                2. sequence<str> [in]- several property data to be deleted
                3. sequence<DbDatum> [in] - several property data to be deleted
                4. dict<str, seq<str>> with each key an attribute name and the value a list of attribute property names to delete from that attribute

        Return     : None

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)
    """
    return __Database__generic_delete_attr_pipe_property(
        self, dev_name, value, self._delete_device_attribute_property
    )


def __Database__delete_device_pipe_property(self, dev_name, value):
    """
    delete_device_pipe_property(self, dev_name, value) -> None

            Delete a list of pipe properties for the specified device.

        Parameters :
            - devname : (string) device name
            - propnames : can be one of the following:

                1. DbData [in] - several property data to be deleted
                2. sequence<str> [in]- several property data to be deleted
                3. sequence<DbDatum> [in] - several property data to be deleted
                3. dict<str, seq<str>> with each key a pipe name and the value a list of pipe property names to delete from that pipe

        Return     : None

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)
    """
    return __Database__generic_delete_attr_pipe_property(
        self, dev_name, value, self._delete_device_pipe_property
    )


def __Database__get_class_property(self, class_name, value):
    """
    get_class_property(self, class_name, value) -> dict<str, seq<str>>

            Query the database for a list of class properties.

        Parameters :
            - class_name : (str) class name
            - value : can be one of the following:

                1. str [in] - single property data to be fetched
                2. tango.DbDatum [in] - single property data to be fetched
                3. tango.DbData [in,out] - several property data to be fetched
                   In this case (direct C++ API) the DbData will be filled with
                   the property values
                4. sequence<str> [in] - several property data to be fetched
                5. sequence<DbDatum> [in] - several property data to be fetched
                6. dict<str, obj> [in,out] - keys are property names
                   In this case the given dict values will be changed to contain
                   the several property values

        Return     : a dictionary which keys are the property names the value
                     associated with each key being a a sequence of strings being the
                     property value.

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)
    """
    return __Database__generic_get_property(
        self, class_name, value, self._get_class_property
    )


def __Database__put_class_property(self, class_name, value):
    """
    put_class_property(self, class_name, value) -> None

            Insert or update a list of properties for the specified class.

        Parameters :
            - class_name : (str) class name
            - value : can be one of the following:

                1. DbDatum - single property data to be inserted
                2. DbData - several property data to be inserted
                3. sequence<DbDatum> - several property data to be inserted
                4. dict<str, DbDatum> - keys are property names and value has data to be inserted
                5. dict<str, obj> - keys are property names and str(obj) is property value
                6. dict<str, seq<str>> - keys are property names and value has data to be inserted
        Return     : None

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)
    """
    return __Database__generic_put_property(
        self, class_name, value, self._put_class_property
    )


def __Database__delete_class_property(self, class_name, value):
    """
    delete_class_property(self, class_name, value) -> None

            Delete a the given of properties for the specified class.

        Parameters :
            - class_name : (str) class name
            - value : can be one of the following:

                1. str [in] - single property data to be deleted
                2. DbDatum [in] - single property data to be deleted
                3. DbData [in] - several property data to be deleted
                4. sequence<str> [in]- several property data to be deleted
                5. sequence<DbDatum> [in] - several property data to be deleted
                6. dict<str, obj> [in] - keys are property names to be deleted
                   (values are ignored)
                7. dict<str, DbDatum> [in] - several DbDatum.name are property names
                   to be deleted (keys are ignored)

        Return     : None

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)
    """
    return __Database__generic_delete_property(
        self, class_name, value, self._delete_class_property
    )


def __Database__get_class_attribute_property(self, class_name, value):
    """
    get_class_attribute_property( self, class_name, value) -> dict<str, dict<str, seq<str>>

            Query the database for a list of class attribute properties for the
            specified class. The method returns all the properties for the specified
            attributes.

        Parameters :
            - class_name : (str) class name
            - propnames : can be one of the following:

                1. str [in] - single attribute properties to be fetched
                2. DbDatum [in] - single attribute properties to be fetched
                3. DbData [in,out] - several attribute properties to be fetched
                   In this case (direct C++ API) the DbData will be filled with the property
                   values
                4. sequence<str> [in] - several attribute properties to be fetched
                5. sequence<DbDatum> [in] - several attribute properties to be fetched
                6. dict<str, obj> [in,out] - keys are attribute names
                   In this case the given dict values will be changed to contain the several
                   attribute property values

        Return     : a dictionary which keys are the attribute names the
                     value associated with each key being a another
                     dictionary where keys are property names and value is
                     a sequence of strings being the property value.

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)
    """
    return __Database__generic_get_attr_pipe_property(
        self, class_name, value, self._get_class_attribute_property
    )


def __Database__put_class_attribute_property(self, class_name, value):
    """
    put_class_attribute_property(self, class_name, value) -> None

            Insert or update a list of properties for the specified class.

        Parameters :
            - class_name : (str) class name
            - propdata : can be one of the following:

                1. tango.DbData - several property data to be inserted
                2. sequence<DbDatum> - several property data to be inserted
                3. dict<str, dict<str, obj>> keys are attribute names and value
                   being another dictionary which keys are the attribute property
                   names and the value associated with each key being seq<str> or
                   tango.DbDatum

        Return     : None

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)
    """
    return __Database__generic_put_attr_pipe_property(
        self, class_name, value, self._put_class_attribute_property
    )


def __Database__delete_class_attribute_property(self, class_name, value):
    """
    delete_class_attribute_property(self, class_name, value) -> None

            Delete a list of attribute properties for the specified class.

        Parameters :
            - class_name : (str) class name
            - propnames : can be one of the following:

                1. DbData [in] - several property data to be deleted
                2. sequence<str> [in]- several property data to be deleted
                3. sequence<DbDatum> [in] - several property data to be deleted
                4. dict<str, seq<str>> keys are attribute names and value being a
                   list of attribute property names

        Return     : None

        Throws     : ConnectionFailed, CommunicationFailed
                     DevFailed from device (DB_SQLError)"""
    return __Database__generic_delete_attr_pipe_property(
        self, class_name, value, self._delete_class_attribute_property
    )


def __Database__get_service_list(self, filter=".*"):
    import re

    data = self.get_property("CtrlSystem", "Services")
    res = {}
    filter_re = re.compile(filter)
    for service in data["Services"]:
        service_name, service_value = service.split(":")
        if filter_re.match(service_name) is not None:
            res[service_name] = service_value
    return res


def __Database__str(self):
    return f"Database({self.get_db_host()}, {self.get_db_port()})"


def __init_Database():
    Database.add_server = _trace_client(__Database__add_server)
    Database.export_server = _trace_client(__Database__export_server)
    Database.put_property = _trace_client(__Database__put_property)
    Database.get_property = _trace_client(__Database__get_property)
    Database.get_property_forced = _trace_client(__Database__get_property_forced)
    Database.delete_property = _trace_client(__Database__delete_property)
    Database.get_device_property = _trace_client(__Database__get_device_property)
    Database.put_device_property = _trace_client(__Database__put_device_property)
    Database.delete_device_property = _trace_client(__Database__delete_device_property)
    Database.get_device_property_list = _trace_client(
        __Database__get_device_property_list
    )
    Database.get_device_attribute_property = _trace_client(
        __Database__get_device_attribute_property
    )
    Database.put_device_attribute_property = _trace_client(
        __Database__put_device_attribute_property
    )
    Database.delete_device_attribute_property = _trace_client(
        __Database__delete_device_attribute_property
    )
    Database.get_class_property = _trace_client(__Database__get_class_property)
    Database.put_class_property = _trace_client(__Database__put_class_property)
    Database.delete_class_property = _trace_client(__Database__delete_class_property)
    Database.get_class_attribute_property = _trace_client(
        __Database__get_class_attribute_property
    )
    Database.put_class_attribute_property = _trace_client(
        __Database__put_class_attribute_property
    )
    Database.delete_class_attribute_property = _trace_client(
        __Database__delete_class_attribute_property
    )
    Database.get_service_list = _trace_client(__Database__get_service_list)
    Database.__str__ = __Database__str
    Database.__repr__ = __Database__str


def db_init():
    __init_DbDatum()
    __init_Database()
