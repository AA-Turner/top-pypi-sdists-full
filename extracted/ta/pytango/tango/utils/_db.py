# SPDX-FileCopyrightText: All Contributors to the PyTango project
# SPDX-License-Identifier: LGPL-3.0-or-later

"""Helpers for the database structures: DbDatum, DbData and friends."""

import collections.abc

from tango import DbData, DbDatum, DbDevExportInfos, DbDevInfos, StdStringVector

from ._convert import __seq_2_vector, ensure_binary, seq_2_StdStringVector
from ._types import is_non_str_seq, is_pure_str


def seq_2_DbDevInfos(seq, vec=None):
    """Converts a python sequence<DbDevInfo> object to a :class:`tango.DbDevInfos`

    :param seq: the sequence of DbDevInfo
    :type seq: sequence<DbDevInfo>
    :param vec: (optional, default is None) an :class:`tango.DbDevInfos`
                to be filled. If None is given, a new :class:`tango.DbDevInfos`
                is created
    :return: a :class:`tango.DbDevInfos` filled with the same contents as seq
    :rtype: :class:`tango.DbDevInfos`
    """
    return __seq_2_vector(seq, vec, DbDevInfos, lambda e: e)


def seq_2_DbDevExportInfos(seq, vec=None):
    """Converts a python sequence<DbDevExportInfo> object to a :class:`tango.DbDevExportInfos`

    :param seq: the sequence of DbDevExportInfo
    :type seq: sequence<DbDevExportInfo>
    :param vec: (optional, default is None) an :class:`tango.DbDevExportInfos`
                to be filled. If None is given, a new :class:`tango.DbDevExportInfos`
                is created
    :return: a :class:`tango.DbDevExportInfos` filled with the same contents as seq
    :rtype: :class:`tango.DbDevExportInfos`
    """
    return __seq_2_vector(seq, vec, DbDevExportInfos, lambda e: e)


def seq_2_DbData(seq, vec=None):
    """Converts a python sequence<DbDatum> object to a :class:`tango.DbData`

    :param seq: the sequence of DbDatum
    :type seq: sequence<DbDatum>
    :param vec: (optional, default is None) an :class:`tango.DbData`
                to be filled. If None is given, a new :class:`tango.DbData`
                is created
    :return: a :class:`tango.DbData` filled with the same contents as seq
    :rtype: :class:`tango.DbData`
    """
    if vec is None:
        if isinstance(seq, DbData):
            return seq
        vec = DbData()
    if not isinstance(vec, DbData):
        raise TypeError("vec must be a tango.DbData")
    else:
        for e in seq:
            if isinstance(e, DbDatum):
                vec.append(e)
            else:
                e = ensure_binary(e, "latin-1")
                vec.append(DbDatum(e))
    return vec


def DbData_2_dict(db_data, d=None):
    if d is None:
        d = {}
    if not isinstance(db_data, DbData):
        raise TypeError(f"db_data must be a tango.DbData. A {type(db_data)} found instead")
    for db_datum in db_data:
        d[db_datum.name] = db_datum.value_string
    return d


def _append_dict_to_db_data(db_data, value):
    for k, v in value.items():
        if isinstance(v, DbDatum):
            db_data.append(v)
            continue
        db_datum = DbDatum(k)
        if is_non_str_seq(v):
            seq_2_StdStringVector(v, db_datum.value_string)
        else:
            if not is_pure_str(v):
                v = str(v)
            v = ensure_binary(v, encoding="latin-1")
            db_datum.value_string.append(v)
        db_data.append(db_datum)


def parameter_2_dbdata(param, param_name):
    if isinstance(param, DbData):
        return param
    elif isinstance(param, DbDatum):
        new_param = DbData()
        new_param.append(param)
        return new_param
    elif is_pure_str(param):
        new_param = DbData()
        new_param.append(DbDatum(param))
        return new_param
    elif is_non_str_seq(param):
        return seq_2_DbData(param)
    elif isinstance(param, collections.abc.Mapping):
        new_param = DbData()
        if len(param) > 0:
            # for attributes we have nested dict
            first_dict_value = next(iter(param.values()))
            if isinstance(first_dict_value, collections.abc.Mapping):
                for k1, v1 in param.items():
                    attr = DbDatum(k1)
                    attr.append(str(len(v1)))
                    new_param.append(attr)
                    _append_dict_to_db_data(new_param, v1)
            else:
                _append_dict_to_db_data(new_param, param)
        return new_param

    raise TypeError(
        f"{param_name} must be a str, tango.DbDatum, tango.DbData, a sequence<DbDatum>, a sequence<str> or a dictionary"
    )


def get_property_from_db(self, propname, user_dbdata):
    if user_dbdata is None:
        user_dbdata = DbData()
    if is_pure_str(propname):
        self._get_property(propname, user_dbdata)
        return DbData_2_dict(user_dbdata)
    elif isinstance(propname, (collections.abc.Sequence, StdStringVector)):
        if len(propname) == 0:
            return {}
        all_str = True
        for p in propname:
            if not is_pure_str(p):
                all_str = False
                break
        if all_str:
            self._get_property(propname, user_dbdata)
            return DbData_2_dict(user_dbdata)

    dbdata = parameter_2_dbdata(propname, "propname")
    if len(dbdata) == 0:
        return {}
    self._get_property(dbdata)
    return DbData_2_dict(dbdata)
