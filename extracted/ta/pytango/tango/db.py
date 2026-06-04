# SPDX-FileCopyrightText: All Contributors to the PyTango project
# SPDX-License-Identifier: LGPL-3.0-or-later

"""
This is an internal PyTango module.
"""

__all__ = ("db_init",)

__docformat__ = "restructuredtext"

import collections.abc
from collections.abc import Sequence

from tango import (
    Database,
    DbData,
    DbDatum,
    DbDevExportInfo,
    DbDevExportInfos,
    DbDevInfo,
    DbDevInfos,
    StdStringVector,
)
from tango._instrumentation import _trace_client
from tango.utils import (
    DbData_2_dict,
    is_non_str_seq,
    parameter_2_dbdata,
    seq_2_DbData,
    seq_2_DbDevExportInfos,
    seq_2_DbDevInfos,
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

    :param servname: server name
    :type servname: str

    :param dev_info: the server device(s) information
    :type dev_info: list[:obj:`~tango.DbDevInfo`], :obj:`~tango.DbDevInfos`, :obj:`~tango.DbDevInfo`

    :param with_dserver: whether or not to auto create **DServer** device in server
    :type with_dserver: bool

    :throws: :obj:`~tango.ConnectionFailed`, :obj:`~tango.CommunicationFailed`, :obj:`~tango.DevFailed`

    .. versionadded:: 8.1.7
        added *with_dserver* parameter
    """

    if not isinstance(dev_info, collections.abc.Sequence) and not isinstance(dev_info, DbDevInfo):
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


def __Database__export_server(self, dev_info: Sequence[DbDevExportInfo] | DbDevExportInfos | DbDevExportInfo):
    """
    Export a group of devices to the database.

    :param dev_info: the server device(s) information

    :throws: :obj:`~tango.ConnectionFailed`, :obj:`~tango.CommunicationFailed`, :obj:`~tango.DevFailed`
    """

    if not isinstance(dev_info, collections.abc.Sequence) and not isinstance(dev_info, DbDevExportInfo):
        raise TypeError("Value must be a DbDevExportInfos, a seq<DbDevExportInfo> or a DbDevExportInfo")

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
        for _ in range(nb_props):
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
        raise TypeError("Value must be a string, tango.DbDatum, tango.DbData, a sequence or a dictionary")


def __Database__put_property(
    self,
    obj_name: str,
    value: DbDatum | DbData | Sequence[DbDatum] | dict[str, DbDatum] | dict[str, Sequence[str]] | dict[str, object],
) -> None:
    """
    Insert or update a list of properties for the specified object.

    :param obj_name: name of the object
    :type obj_name: str

    :param value: Can be one of the following: \n
        1. :obj:`~tango.DbDatum` - single property data to be inserted \n
        2. :obj:`~tango.DbData` - several property data to be inserted \n
        3. :py:obj:`list`\\[:obj:`~tango.DbDatum`]- several property data to be inserted \n
        4. :py:obj:`dict`\\[:py:obj:`str`, :obj:`~tango.DbDatum`] - keys are property names and value has data
           to be inserted \n
        5. :py:obj:`dict`\\[:py:obj:`str`, :py:obj:`list`\\[str]] - keys are property names and value has data
           to be inserted \n
        6. :py:obj:`dict`\\[:py:obj:`str`, :py:obj:`obj`] - keys are property names and str(obj) is property value \n

    :throws: :obj:`~tango.ConnectionFailed`, :obj:`~tango.CommunicationFailed`, :obj:`~tango.DevFailed`
    """

    return __Database__generic_put_property(self, obj_name, value, self._put_property)


def __Database__get_property(
    self,
    obj_name: str,
    value: str | DbDatum | DbData | Sequence[str] | Sequence[DbDatum] | dict[str, object],
) -> dict[str, list[str]]:
    """
    Query the database for a list of object (i.e non-device) properties.

    :param obj_name: name of the object
    :type obj_name: str

    :param value: the server device(s) information \n
        1. :py:obj:`str` [in] - single property data to be fetched \n
        2. :obj:`~tango.DbDatum` [in] - single property data to be fetched \n
        3. :obj:`~tango.DbData` [in,out] - several property data to be fetched.
           In this case (direct C++ API) the DbData will be filled with the property values \n
        4. :py:obj:`list`\\[:py:obj:`str`] [in] - several property data to be fetched \n
        5. :py:obj:`list`\\[:obj:`~tango.DbDatum`] [in] - several property data to be fetched
        6. :py:obj:`dict`\\[:py:obj:`str`, :py:obj:`obj`] [in,out] - keys are property names. In this case the
           given dict values will be changed to contain the several property values

    :return: a dictionary keyed by the property name, with the associated value
             a sequence of strings representing the property value.

    :throws: :obj:`~tango.ConnectionFailed`, :obj:`~tango.CommunicationFailed`, :obj:`~tango.DevFailed`
    """
    return __Database__generic_get_property(self, obj_name, value, self._get_property)


def __Database__get_property_forced(self, obj_name, value):
    return __Database__generic_get_property(self, obj_name, value, self._get_property_forced)


__Database__get_property_forced.__doc__ = __Database__get_property.__doc__


def __Database__delete_property(
    self,
    obj_name: str,
    value: str | DbDatum | DbData | list[str] | list[DbDatum] | dict[str, object] | dict[str, DbDatum],
) -> None:
    """
    Delete the given properties for the specified object.

    :param obj_name: name of the object
    :type obj_name: str

    :param value: the server device(s) information: \n
        1. :py:obj:`str` [in] - single property data to be deleted \n
        2. :obj:`~tango.DbDatum` [in] - single property data to be deleted \n
        3. :obj:`~tango.DbData` [in] - several property data to be deleted \n
        4. :py:obj:`list`\\[:py:obj:`str`] [in]- several property data to be deleted \n
        5. :py:obj:`list`\\[:obj:`~tango.DbDatum`] [in] - several property data to be deleted \n
        6. :py:obj:`dict`\\[:py:obj:`str`, :py:obj:`object`] [in] - keys are property names
           to be deleted (values are ignored) \n
        7. :py:obj:`dict`\\[:py:obj:`str`, :obj:`~tango.DbDatum`] [in] - several DbDatum.name
           are property names to be deleted (keys are ignored)

    :throws: :obj:`~tango.ConnectionFailed`, :obj:`~tango.CommunicationFailed`, :obj:`~tango.DevFailed`
    """
    return __Database__generic_delete_property(self, obj_name, value, self._delete_property)


def __Database__get_device_property(
    self,
    dev_name: str,
    value: str | DbDatum | DbData | list[str] | list[DbDatum] | dict[str, object],
) -> dict[str, list[str]]:
    """
    Query the database for a list of device properties.

    :param dev_name: object name
    :type dev_name: str

    :param value: can be one of the following: \n
        1. :py:obj:`str` [in] - single property data to be fetched \n
        2. :obj:`~tango.DbDatum` [in] - single property data to be fetched \n
        3. :obj:`~tango.DbData` [in,out] - several property data to be fetched.
           In this case (direct C++ API) the DbData will be filled with the property values \n
        4. :py:obj:`list`\\[:py:obj:`str`] [in] - several property data to be fetched \n
        5. list[:obj:`~tango.DbDatum`] [in] - several property data to be fetched \n
        6. :py:obj:`dict`\\[:py:obj:`str`, :py:obj:`object`] [in,out] - keys are property names. In this case the
           given dict values will be changed to contain the several property values

    :return: a dictionary keyed by the property name, with the associated value
             a sequence of strings representing the property value.

    :throws: :obj:`~tango.ConnectionFailed`, :obj:`~tango.CommunicationFailed`, :obj:`~tango.DevFailed`
    """
    return __Database__generic_get_property(self, dev_name, value, self._get_device_property)


def __Database__put_device_property(
    self,
    dev_name: str,
    value: DbDatum | DbData | list[DbDatum] | dict[str, DbDatum] | dict[str, object] | dict[str, list[str]],
) -> None:
    """
    Insert or update a list of properties for the specified device.

    :param dev_name: object name
    :type dev_name: str

    :param value: can be one of the following: \n
        1. :obj:`~tango.DbDatum` - single property data to be inserted \n
        2. :obj:`~tango.DbData` - several property data to be inserted \n
        3. :py:obj:`list`\\[:obj:`~tango.DbDatum`] - several property data to be inserted \n
        4. :py:obj:`dict`\\[:py:obj:`str`, :obj:`~tango.DbDatum`] - keys are property
           names and value has data to be inserted \n
        5. :py:obj:`dict`\\[:py:obj:`str`, :py:obj:`object`] - keys are property
           names and str(obj) is property value \n
        6. :py:obj:`dict`\\[:py:obj:`str`, :py:obj:`list`[:py:obj:`str`]] - keys are
           property names and value has data to be inserted

    :throws: :obj:`~tango.ConnectionFailed`, :obj:`~tango.CommunicationFailed`, :obj:`~tango.DevFailed`
    """
    return __Database__generic_put_property(self, dev_name, value, self._put_device_property)


def __Database__delete_device_property(self, dev_name: str, value) -> None:
    """
    Delete the given properties for the specified device.

    :param dev_name: object name
    :type dev_name: str

    :param value: can be one of the following: \n
        1. :py:obj:`str` [in] - single property data to be deleted \n
        2. :obj:`~tango.DbDatum` [in] - single property data to be deleted \n
        3. :obj:`~tango.DbData` [in] - several property data to be deleted \n
        4. :py:obj:`list`\\[:py:obj:`str`] [in]- several property data to be deleted \n
        5. :py:obj:`list`\\[:obj:`~tango.DbDatum`] [in] - several property data to be deleted \n
        6. :py:obj:`dict`\\[:py:obj:`str`, :py:obj:`object`] [in] - keys are property names to be deleted
           (values are ignored) \n
        7. :py:obj:`dict`\\[:py:obj:`str`, :obj:`~tango.DbDatum`] [in] - several DbDatum.name
           are property names to be deleted (keys are ignored) \n

    :throws: :obj:`~tango.ConnectionFailed`, :obj:`~tango.CommunicationFailed`, :obj:`~tango.DevFailed`
    """
    return __Database__generic_delete_property(self, dev_name, value, self._delete_device_property)


def __Database__get_device_property_list(
    self, dev_name: str, wildcard: str, array: list[object] | None = None
) -> DbDatum | None | list[object]:
    """
    Query the database for a list of properties defined for the
    specified device and which match the specified wildcard.
    If array parameter is given, it must be an object implementing de 'append'
    method. If given, it is filled with the matching property names. If not given
    the method returns a new DbDatum containing the matching property names.

    :param dev_name: device name
    :type dev_name: str

    :param wildcard: property name wildcard
    :type wildcard: str

    :param array: (optional) array that will contain the matching property names.
    :type array: list[]

    :return: if container is None, return is a new DbDatum containing the
             matching property names. Otherwise returns the given array
             filled with the property names
    :rtype: :obj:`~tango.DbDatum` | list[]

    :throws: :obj:`~tango.ConnectionFailed`, :obj:`~tango.CommunicationFailed`, :obj:`~tango.DevFailed`

    .. versionadded:: 7.0.0
    """
    if array is None:
        return self._get_device_property_list(dev_name, wildcard)
    elif isinstance(array, StdStringVector):
        return self._get_device_property_list(dev_name, wildcard, array)
    elif is_non_str_seq(array):
        res = self._get_device_property_list(dev_name, wildcard)
        for e in res:
            array.append(e)
        return array


def __Database__get_device_attribute_property(
    self,
    dev_name: str,
    value: str | DbDatum | DbData | list[str] | list[DbDatum] | dict[str, object],
) -> dict[str, dict[str, list[str]]]:
    """
    Query the database for a list of device attribute properties for the
    specified device. The method returns all the properties for the specified
    attributes.

    :param dev_name: device name
    :type dev_name: str

    :param value: can be one of the following: \n
        1. :py:obj:`str` [in] - single attribute properties to be fetched \n
        2. :obj:`~tango.DbDatum` [in] - single attribute properties to be fetched \n
        3. :obj:`~tango.DbData` [in,out] - several attribute properties to be fetched.
           In this case (direct C++ API) the DbData will be filled with the property values \n
        4. :py:obj:`list`\\[:py:obj:`str`] [in] - several attribute properties to be fetched \n
        5. :py:obj:`list`\\[:obj:`~tango.DbDatum`] [in] - several attribute properties to be fetched \n
        6. :py:obj:`dict`\\[:py:obj:`str`, :py:obj:`object`] [in,out] - keys are attribute names.
           In this case the given dict values will be changed to contain the several attribute property values

    :return: a dictionary keyed by the attribute name, with the associated value
             another dictionary. The inner dictionary is keyed by attribute property
             name, with the associated value a sequence of strings representing
             the property value.

    :throws: :obj:`~tango.ConnectionFailed`, :obj:`~tango.CommunicationFailed`, :obj:`~tango.DevFailed`
    """
    return __Database__generic_get_attr_pipe_property(self, dev_name, value, self._get_device_attribute_property)


def __Database__put_device_attribute_property(
    self,
    dev_name: str,
    value: DbData | list[DbDatum] | dict[str, dict[str, DbDatum]],
) -> None:
    """
    Insert or update a list of properties for the specified device.

    :param dev_name: device name
    :type dev_name: str

    :param value: can be one of the following: \n
        1. :obj:`~tango.DbData` [in,out] - several property data to be inserted \n
        2. :py:obj:`list`\\[:obj:`~tango.DbDatum`] [in] - several property data to be inserted \n
        3. :py:obj:`dict`\\[:py:obj:`str`, :py:obj:`dict`\\[:py:obj:`str`, :obj:`~tango.DbDatum`]] - keys
           are attribute names and value another dictionary where keys are the
           attribute property names and the values are DbDatum.

    :throws: :obj:`~tango.ConnectionFailed`, :obj:`~tango.CommunicationFailed`, :obj:`~tango.DevFailed`
    """
    return __Database__generic_put_attr_pipe_property(self, dev_name, value, self._put_device_attribute_property)


def __Database__delete_device_attribute_property(
    self,
    dev_name: str,
    value: DbDatum | list[str] | list[DbDatum] | dict[str, list[str]],
) -> None:
    """
    Delete a list of attribute properties for the specified device.

    :param dev_name: device name
    :type dev_name: str

    :param value: can be one of the following: \n
        1. :obj:`~tango.DbData` [in,out] - several property data to be deleted \n
        2. :py:obj:`list`\\[:py:obj:`str`] [in] - several property data to be deleted \n
        3. :py:obj:`list`\\[:obj:`~tango.DbDatum`] [in] - several property data to be deleted \n
        4. :py:obj:`dict`\\[:py:obj:`str`, :py:obj:`list`\\[:py:obj:`str`]] - with each key
           a attribute name and the value a list of pipe property names to delete from that pipe

    :throws: :obj:`~tango.ConnectionFailed`, :obj:`~tango.CommunicationFailed`, :obj:`~tango.DevFailed`
    """
    return __Database__generic_delete_attr_pipe_property(self, dev_name, value, self._delete_device_attribute_property)


def __Database__get_class_property(
    self,
    class_name: str,
    value: str | DbDatum | DbData | list[str] | list[DbDatum] | dict[str, object],
) -> dict[str, list[str]]:
    """
    Query the database for a list of class properties.

    :param class_name: class name
    :type class_name: str

    :param value: can be one of the following: \n
        1. :py:obj:`str` [in] - single property data to be fetched \n
        2. :obj:`~tango.DbDatum` [in] - single property data to be fetched \n
        3. :obj:`~tango.DbData` [in,out] - several property data to be fetched.
           In this case (direct C++ API) the DbData will be filled with the property values \n
        4. :py:obj:`list`\\[:py:obj:`str`] [in] - several property data to be fetched \n
        5. :py:obj:`list`\\[:obj:`~tango.DbDatum`] [in] - several property data to be fetched \n
        6. :py:obj:`dict`\\[:py:obj:`str`, :py:obj:`object`] [in,out] - keys are property names.
           In this case the given dict values will be changed to contain the several property values

    :return: a dictionary keyed by the property name, with the associated value
             a sequence of strings representing the property value.

    :throws: :obj:`~tango.ConnectionFailed`, :obj:`~tango.CommunicationFailed`, :obj:`~tango.DevFailed`
    """
    return __Database__generic_get_property(self, class_name, value, self._get_class_property)


def __Database__put_class_property(
    self,
    class_name: str,
    value: DbDatum | DbData | list[DbDatum] | dict[str, DbDatum] | dict[str, object] | dict[str, list[str]],
) -> None:
    """
    Insert or update a list of properties for the specified class.

    :param class_name: class name
    :type class_name: str

    :param value: can be one of the following: \n
        1. :obj:`~tango.DbDatum` [in] - single attribute properties to be inserted \n
        2. :obj:`~tango.DbData` [in,out] - several attribute properties to be inserted \n
        3. :py:obj:`list`[:obj:`~tango.DbDatum`] [in] - several attribute properties to be inserted \n
        4. :py:obj:`dict`\\[:py:obj:`str`, :obj:`~tango.DbDatum`] - keys are property names
           and value has data to be inserted \n
        5. :py:obj:`dict`\\[:py:obj:`str`, :py:obj:`object`] - keys are property names and str(obj) is property value
        6. :py:obj:`dict`\\[:py:obj:`str`, :py:obj:`list`\\[:py:obj:`str`]] - keys are property names
           and value has data to be inserted

    :throws: :obj:`~tango.ConnectionFailed`, :obj:`~tango.CommunicationFailed`, :obj:`~tango.DevFailed`
    """
    return __Database__generic_put_property(self, class_name, value, self._put_class_property)


def __Database__delete_class_property(
    self,
    class_name: str,
    value: str | DbDatum | DbData | list[str] | list[DbDatum] | dict[str, object] | dict[str, DbDatum],
) -> None:
    """
    Delete the given properties for the specified class.

    :param class_name: class name
    :type class_name: str

    :param value: can be one of the following: \n
        1. :py:obj:`str` [in] - single attribute properties to be deleted \n
        2. :obj:`~tango.DbDatum` [in] - single attribute properties to be deleted \n
        3. :obj:`~tango.DbData` [in,out] - several attribute properties to be deleted \n
        4. :py:obj:`list`\\[:py:obj:`str`] [in] - several attribute properties to be deleted \n
        5. :py:obj:`list`\\[:obj:`~tango.DbDatum`] [in] - several attribute properties to be deleted \n
        6. :py:obj:`dict`\\[:py:obj:`str`, :py:obj:`object`] [in,out] - keys are property names to be deleted
           (values are ignored) \n
        7. :py:obj:`dict`\\[:py:obj:`str`, :obj:`~tango.DbDatum`] [in] - several
           DbDatum.name are property names to be deleted (keys are ignored)

    :throws: :obj:`~tango.ConnectionFailed`, :obj:`~tango.CommunicationFailed`, :obj:`~tango.DevFailed`
    """
    return __Database__generic_delete_property(self, class_name, value, self._delete_class_property)


def __Database__get_class_attribute_property(
    self,
    class_name: str,
    value: str | DbDatum | DbData | list[str] | list[DbDatum] | dict[str, object],
) -> dict[str, dict[str, list[str]]]:
    """
    Query the database for a list of class attribute properties for the
    specified class. The method returns all the properties for the specified
    attributes.

    :param class_name: class name
    :type class_name: str

    :param value: can be one of the following: \n
        1. :py:obj:`str` [in] - single attribute properties to be fetched \n
        2. :obj:`~tango.DbDatum` [in] - single attribute properties to be fetched \n
        3. :obj:`~tango.DbData` [in,out] - several attribute properties to be fetched.
           In this case (direct C++ API) the :obj:`~tango.DbData` will be filled with the property values \n
        4. :py:obj:`list`\\[str] [in] - several attribute properties to be fetched \n
        5. :py:obj:`list`\\[:obj:`~tango.DbDatum`] [in] - several attribute properties to be fetched \n
        6. :py:obj:`dict`\\[:py:obj:`str`, :py:obj:`object`] [in,out] - keys are attribute names.
           In this case the given dict values will be changed to contain the several attribute property values

    :return: a dictionary keyed by the attribute name, with the associated value
             another dictionary. The inner dictionary is keyed by attribute property
             name, with the associated value a sequence of strings representing
             the property value.

    :throws: :obj:`~tango.ConnectionFailed`, :obj:`~tango.CommunicationFailed`, :obj:`~tango.DevFailed`
    """
    return __Database__generic_get_attr_pipe_property(self, class_name, value, self._get_class_attribute_property)


def __Database__put_class_attribute_property(
    self, class_name: str, value: DbData | list[DbDatum] | dict[str, DbDatum]
) -> None:
    """
    Insert or update a list of properties for the specified class.

    :param class_name: class name
    :type class_name: str

    :param value: can be one of the following: \n
        1. :obj:`~tango.DbData` - several property data to be inserted \n
        2. :py:obj:`list`\\[:obj:`~tango.DbDatum`] - several property data to be inserted \n
        3. :py:obj:`dict`\\[:py:obj:`str`, :py:obj:`dict`\\[:py:obj:`str`, :obj:`~tango.DbDatum`]]
           keys are attribute names and value being another dictionary which
           keys are the attribute property names and the value

    :throws: :obj:`~tango.ConnectionFailed`, :obj:`~tango.CommunicationFailed`, :obj:`~tango.DevFailed`
    """
    return __Database__generic_put_attr_pipe_property(self, class_name, value, self._put_class_attribute_property)


def __Database__delete_class_attribute_property(
    self,
    class_name: str,
    value: DbDatum | list[str] | list[DbDatum] | dict[str, list[str]],
) -> None:
    """
    Delete a list of attribute properties for the specified class.

    :param class_name: class name
    :type class_name: str

    :param value: can be one of the following: \n
        1. :obj:`~tango.DbData` [in] - several property data to be deleted \n
        2. :py:obj:`list`\\[:py:obj:`str`] [in]- several property data to be deleted \n
        3. :py:obj:`list`\\[:obj:`~tango.DbDatum`] [in] - several property data to be deleted \n
        4. :py:obj:`dict`\\[:py:obj:`str`, :py:obj:`list`\\[:py:obj:`str`]] keys are attribute
           names and value being a list of attribute property names

    :throws: :obj:`~tango.ConnectionFailed`, :obj:`~tango.CommunicationFailed`, :obj:`~tango.DevFailed`
    """
    return __Database__generic_delete_attr_pipe_property(self, class_name, value, self._delete_class_attribute_property)


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
    Database.get_device_property_list = _trace_client(__Database__get_device_property_list)
    Database.get_device_attribute_property = _trace_client(__Database__get_device_attribute_property)
    Database.put_device_attribute_property = _trace_client(__Database__put_device_attribute_property)
    Database.delete_device_attribute_property = _trace_client(__Database__delete_device_attribute_property)
    Database.get_class_property = _trace_client(__Database__get_class_property)
    Database.put_class_property = _trace_client(__Database__put_class_property)
    Database.delete_class_property = _trace_client(__Database__delete_class_property)
    Database.get_class_attribute_property = _trace_client(__Database__get_class_attribute_property)
    Database.put_class_attribute_property = _trace_client(__Database__put_class_attribute_property)
    Database.delete_class_attribute_property = _trace_client(__Database__delete_class_attribute_property)
    Database.get_service_list = _trace_client(__Database__get_service_list)
    Database.__str__ = __Database__str
    Database.__repr__ = __Database__str


def db_init():
    __init_DbDatum()
    __init_Database()
