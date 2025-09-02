# -*- coding: utf8 -*-

import json
import datetime
from enum import Enum
import struct

class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Enum):
            return obj.name
        elif isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        elif isinstance(obj, object):
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)

class DefaultJsonObject(object):
    def __repr__(self):
        return json.dumps(self, cls=MyEncoder, indent=2)


class VectorUtils:
    @staticmethod
    def floats_to_bytes(floats):
        if not isinstance(floats, (list, tuple)) or not all(isinstance(f, float) for f in floats):
            raise TypeError("Input must be a list/tuple of floats")
        if len(floats) == 0:
            raise ValueError("vector is empty")
        return bytearray(struct.pack('<' + 'f' * len(floats), *floats))

    @staticmethod
    def bytes_to_floats(byte_data):
        if not isinstance(byte_data, bytearray):
            raise TypeError("Input must be a bytearray object")
        num_floats = len(byte_data) // 4
        if len(byte_data) % 4 != 0 or num_floats == 0:
            raise ValueError("bytes length is not multiple of 4(SIZE_OF_FLOAT32) or length is 0")
        floats = struct.unpack('<' + 'f' * num_floats, byte_data)
        return list(floats)

def get_now_utc_datetime():
    return datetime.datetime.now(datetime.timezone.utc)
