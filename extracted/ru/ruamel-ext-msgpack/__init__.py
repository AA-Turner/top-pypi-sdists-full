# coding: utf-8

from typing import Dict, Any

_package_data: Dict[str, Any] = dict(
    full_package_name='ruamel.ext.msgpack',
    version_info=(0, 2, 2),
    __version__='0.2.2',
    version_timestamp='2023-08-05 11:29:23',
    author='Anthon van der Neut',
    author_email='a.van.der.neut@ruamel.eu',
    description='thin wrapper around msgpack to deal with naive datetime and ruamel'
    ' defined extension types',
    keywords='pypi statistics',
    entry_points='msgpack=ruamel.ext.msgpack.__main__:main',
    # entry_points=None,
    license='Copyright Ruamel bvba 2007-2023',
    since=2023,
    # status='α|β|stable',  # the package status on PyPI
    # data_files="",
    # universal=True,  # py2 + py3
    install_requires=['msgpack>=1.0.4'],
    tox=dict(env='3'),  # *->all p->pypy
    mypy=False,
    python_requires='>=3',
)  # NOQA


version_info = _package_data['version_info']
__version__ = _package_data['__version__']

#################

import struct  # NOQA
import datetime  # NOQA
from functools import partial  # NOQA
import msgpack  # NOQA


class MsgPackDate:
    """
    these 2 and 4 byte num encodings are created to more easily mask out information for e.g.
    Q3 of 2020 without comparing year/month/day or a day offset starting from e.g. 1970-01-01
    the values are ordered, but non-consecutive:
       date_numX(2020-10-01) != (date_numX(2020-09-30) + 1)

    num2 is a 16 bit format (bit ranges inclusive)
    16-9 -> seven bits for years 2000 up to and including 2126
            the all bits are one (pseudo year 2127) -> yearless month day info
     8-7 -> quarter of year ( Q1 = 0x0, Q2 = 0x1, Q3 = 0x2, Q4 = 0x3
     6-5 -> month within the quarter (Jan/Apr/Jul/Oct = 0x0, Feb/May/Aug/Nov = 0x1,
                Mar/Jun/Sep/Dec = 0x2
     4-0 -> day of month (ranging 1-31)

    num4 is a 32 bit format (bit ranges inclusive)
    31-16 -> year starting at -10000, which is couple of thousand years before recorded history
    15-14 -> quarter of year ( Q1 = 0x0, Q2 = 0x1, Q3 = 0x2, Q4 = 0x3
    13-12 -> month within the quarter (Jan/Apr/Jul/Oct = 0x0, Feb/May/Aug/Nov = 0x1,
                Mar/Jun/Sep/Dec = 0x2
    11- 7 -> day of month (ranging 1-31)
     6- 4 -> day of week, with Mon: 0x1 - Sunday 0x7 part of the weekEND, 0x0 -> not provided
     3- 0 -> reserved for future use (e.g. calendar type: julian, aztec), should be 0

    ToDo: provide Quarter and Quarters ( Q1, Q1-Q2, Q1-Q3, Q1-Q4 ) and routines to compare
          undecoded bitpatterns (primarily for hlmdb indices)
    """

    msgpack_type = 17

    @classmethod
    def pack(cls, obj):
        """
        assume obj is datetime.date
        """
        try:
            return msgpack.ExtType(cls.msgpack_type, struct.pack('>H', cls.date_num2(obj)))
        except ValueError:
            return msgpack.ExtType(cls.msgpack_type, struct.pack('>I', cls.date_num4(obj)))

    @classmethod
    def unpack(cls, code, data):
        """
        assume code is MsgPackDate.type
        """
        if len(data) == 2:
            return cls.num2_date(struct.unpack('>H', data)[0])
        elif len(data) == 4:
            bits = struct.unpack('>I', data)[0]
            return cls.num4_date(bits)

    @staticmethod
    def date_num2(dd):
        if not (2000 <= dd.year < 2127):  # 2127 reserved for yearless month/day info
            raise ValueError
        yb = (dd.year - 2000) << 9
        month = dd.month - 1
        qb, miqb = divmod(month, 3)
        qb = qb << 7
        miqb = miqb << 5
        dayb = dd.day
        return yb | qb | miqb | dayb

    @staticmethod
    def num2_date(bits):
        year = ((bits & 0xFE00) >> 9) + 2000
        assert year != 2127  # reserved
        return datetime.date(
            year, month=((bits & 0x0180) >> 7) * 3 + ((bits & 0x60) >> 5) + 1, day=bits & 0x1F,
        )

    @staticmethod
    def date_num4(dd):
        yb = (dd.year + 10000) << 16
        month = dd.month - 1
        qb, miqb = divmod(month, 3)
        qb = qb << 14
        miqb = miqb << 12
        dayb = dd.day << 7
        weekdayb = dd.isoweekday() << 4
        return yb | qb | miqb | dayb | weekdayb

    @staticmethod
    def num4_date(bits):
        return datetime.date(
            year=((bits & 0xFFFF_0000) >> 16) - 10000,
            month=((bits & 0xC000) >> 14) * 3 + ((bits & 0x3000) >> 12) + 1,
            day=(bits & 0x0F80) >> 7,
        )


class MsgPackDefault:
    def __init__(self):
        self.date = 17
        self._encode = {}  # from instance type to function packing
        self._decode = {}  # from numerical type to function unpacking
        self._encode[datetime.datetime] = MsgPackDefault.handle_naive_datetime
        self._encode[datetime.date] = MsgPackDate.pack
        self._decode[MsgPackDate.msgpack_type] = MsgPackDate.unpack

    def __call__(self, obj):
        registered = self._encode.get(type(obj))
        if registered is None:
            return obj
        retval = registered(obj)
        return retval

    def ext_hook(self, code, data):
        registered = self._decode.get(code)
        if registered is not None:
            retval = registered(code, data)
            if retval is not None:
                return retval
        return msgpack.ExtType(code, data)

    @staticmethod
    def handle_naive_datetime(obj):
        """
        only unaware datetimes are handed to __call__, no need to do:
           if obj.tzinfo is None or obj.tzinfo.utcoffset(obj) is None:
               return obj.replace(tzinfo=datetime.UTC)
           return obj.astimezone(datetime.UTC)
        """
        return obj.replace(tzinfo=datetime.UTC)


msgpack_default = MsgPackDefault()

pack = partial(msgpack.pack, default=msgpack_default, datetime=True)
packb = partial(msgpack.packb, default=msgpack_default, datetime=True)
unpackb_raw = partial(msgpack.unpackb, strict_map_key=False)
unpackb = partial(
    msgpack.unpackb, ext_hook=msgpack_default.ext_hook, strict_map_key=False, timestamp=3,
)


def hex(ba):
    return ''.join(['\\x{:02x}'.format(x) for x in ba])


Packer = partial(msgpack.Packer, default=msgpack_default, datetime=True)
Unpacker = partial(
    msgpack.Unpacker, ext_hook=msgpack_default.ext_hook, strict_map_key=False, timestamp=3,
)


def concat_dict(d, stream):
    """concatenate multiple dicts into a bytes stream saving key and value"""
    for k, v in d.items():
        pack(k, stream)
        pack(v, stream)


def unconcat_dict(byts):
    retval = {}
    unpacker = Unpacker()
    unpacker.feed(byts)
    while True:
        try:
            k = unpacker.unpack()
        except msgpack.OutOfData:
            break
        v = unpacker.unpack()
        retval[k] = v
    return retval


def unconcat_first_dict(byts):
    """
    return the first two items in the concatenated series seperately, and the rest as a dict
    """
    retval = {}
    unpacker = Unpacker()
    unpacker.feed(byts)
    k0 = unpacker.unpack()
    v0 = unpacker.unpack()
    while True:
        try:
            k = unpacker.unpack()
        except msgpack.OutOfData:
            break
        v = unpacker.unpack()
        retval[k] = v
    return k0, v0, retval


def unconcat_first(byts):
    unpacker = Unpacker()
    unpacker.feed(byts)
    k = unpacker.unpack()
    v = unpacker.unpack()
    return k, v
