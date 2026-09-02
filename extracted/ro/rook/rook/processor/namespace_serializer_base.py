import datetime
import decimal
from types import FunctionType, MethodType, ModuleType
from google.protobuf.reflection import GeneratedProtocolMessageType
from google.protobuf.internal import api_implementation

if api_implementation.Type() == "upb":
    import google

import six

if six.PY2:
    from types import TypeType

try:
    import numpy
except ImportError:
    numpy = None

try:
    import torch
except ImportError:
    torch = None

try:
    import multidict
except ImportError:
    multidict = None

try:
    from bson import ObjectId
    from bson.raw_bson import RawBSONDocument
except ImportError:
    ObjectId = None
    RawBSONDocument = None


class NamespaceSerializerBase(object):
    BUILTIN_ATTRIBUTES_IGNORE = {
        '__dict__',
        '__module__',
        '__weakref__',
        '__name__',
        '__doc__',
        '__qualname__',
        '__spec__',
        '__defaults__',
        '__code__',
        '__globals__',
        '__closure__',
        '__annotations__',
        '__kwdefaults__',
        '__bases__'}

    GETATTR_ALLOWLIST = {
        'py4j.java_gateway.JVMView'
    }

    try:
        # Py2 objects
        BINARY_TYPES = (buffer, bytearray)
        STRING_TYPES = (basestring, str, unicode)
        CODE_TYPES = (FunctionType, MethodType, TypeType, ModuleType, six.MovedModule)
        PRIMITIVE_TYPES = (type(None), int, bool, long, float, str, unicode, complex, decimal.Decimal) + BINARY_TYPES + CODE_TYPES + (datetime.datetime,)

    except NameError:
        # Py3 objects
        BINARY_TYPES = (bytearray, bytes, bytes)
        STRING_TYPES = (str, )
        CODE_TYPES = (FunctionType, MethodType, type, ModuleType, six.MovedModule)
        PRIMITIVE_TYPES = (type(None), int, bool, float, str, complex, decimal.Decimal) + BINARY_TYPES + CODE_TYPES + (datetime.datetime,)

    def __init__(self, use_string_cache=False):
        self.use_string_cache = use_string_cache
        self.string_cache = {}

        if use_string_cache:
            # Lock the 0 index since some variant will have no originalType (container for example)
            self.string_cache[""] = 0

        self.estimated_pending_bytes = 0

    def get_string_cache(self):
        return self.string_cache

    def get_estimated_pending_bytes(self):
        return self.estimated_pending_bytes

    def _get_string_index_in_cache(self, string_to_cache):
        index = self.string_cache.get(string_to_cache, None)
        if index is None:
            index = len(self.string_cache)
            # We estimate each character is one byte in utf-8 and overhead is 5 bytes
            self.estimated_pending_bytes += len(string_to_cache) + 5
            self.string_cache[string_to_cache] = index

        return index

    def is_in_get_attr_allowlist(self, obj_name):
        return obj_name in self.GETATTR_ALLOWLIST

    if six.PY3:
        @staticmethod
        def get_attr_safe(obj, name):
            try:
                return object.__getattribute__(obj, name)
            except AttributeError:
                return None

        @staticmethod
        def has_attr_safe(obj, name):
            try:
                object.__getattribute__(obj, name)
                return True
            except AttributeError:
                return False
    else:
        # In python 2, you don't technically have to inherit from `object`, so some methods aren't using
        # `__getattribute__` like object does. Therefore, we must use the unsafe alternatives
        class OldStyleClass:
            pass
        instance = type(OldStyleClass())

        @staticmethod
        def get_attr_safe(obj, name):
            try:
                return object.__getattribute__(obj, name)
            except AttributeError:
                try:
                    # If obj inherits from object, we are done
                    if type(obj) is not NamespaceSerializerBase.instance:
                        return None
                    # Else, use the unsafe method
                    return getattr(obj, name)
                # If an exception is thrown from `__getattr__`, the type of the exception will not
                # be `AttributeError`, so we must catch 'em all
                except Exception as e:
                    return None

        @staticmethod
        def has_attr_safe(obj, name):
            return hasattr(obj, name)

    def _get_object_width(self, obj):
        object_width = 0
        obj_dict = self.get_attr_safe(obj, '__dict__')
        obj_slots = self.get_attr_safe(obj, '__slots__')

        if obj_dict:
            object_width += len(obj_dict)
        if obj_slots:
            object_width += len(obj_slots)
        return object_width

    if six.PY2:
        @staticmethod
        def normalize_string(obj):
            if isinstance(obj, str):
                return unicode(obj, errors="replace")
            else:
                return unicode(obj)
    else:
        @staticmethod
        def normalize_string(obj):
            return obj

    if numpy is not None:
        @staticmethod
        def is_numpy_obj(obj_mro):
            return numpy.generic in obj_mro

        @staticmethod
        def is_numpy_array(obj_class):
            return obj_class is numpy.ndarray

    else:
        @staticmethod
        def is_numpy_obj(obj_mro):
            return False

        @staticmethod
        def is_numpy_array(obj_class):
            return False

    if torch is not None:
        @staticmethod
        def is_torch_obj(obj_class):
            try:
                module = object.__getattribute__(obj_class, '__module__')
            except AttributeError:
                return False

            return module.startswith('torch')
    else:
        @staticmethod
        def is_torch_obj(obj_class):
            return False

    if multidict is not None:
        @staticmethod
        def is_multidict_obj(obj_class):
            return obj_class in (multidict.MultiDict, multidict.CIMultiDict,
                                 multidict.MultiDictProxy,
                                 multidict.CIMultiDictProxy)
    else:
        @staticmethod
        def is_multidict_obj(obj_class):
            return False

    if api_implementation.Type() == "upb":
        @staticmethod
        def is_protobuf_obj(obj_class):
            return isinstance(obj_class, google._upb._message.MessageMeta)
    else:
        @staticmethod
        def is_protobuf_obj(obj_class):
            return isinstance(obj_class, GeneratedProtocolMessageType)

    if not ObjectId or not RawBSONDocument:
        @staticmethod
        def is_bson(obj_class):
            return False
    else:
        @staticmethod
        def is_bson(obj_class):
            return obj_class in (ObjectId, RawBSONDocument)
