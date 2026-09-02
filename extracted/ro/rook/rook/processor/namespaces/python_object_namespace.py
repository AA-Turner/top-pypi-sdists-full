import six

from .namespace import Namespace

from rook.exceptions import RookKeyNotFound, RookAttributeNotFound, RookInvalidMethodArguments
from ..namespace_serializer_base import NamespaceSerializerBase
from .variable_types import LIST_TYPE, DICT_TYPE


class PythonObjectNamespace(Namespace):
    class ObjectDumpConfig(object):

        STRICT_MAX_DEPTH = 2
        STRICT_MAX_WIDTH = 10
        STRICT_MAX_COLLECTION_DEPTH = 2
        STRICT_MAX_STRING = 128

        DEFAULT_MAX_DEPTH = 4
        DEFAULT_MAX_WIDTH = 10
        DEFAULT_MAX_COLLECTION_DEPTH = 4
        DEFAULT_MAX_STRING = 512

        TOLERANT_MAX_DEPTH = 5
        TOLERANT_MAX_WIDTH = 20
        TOLERANT_MAX_COLLECTION_DEPTH = 5
        TOLERANT_MAX_STRING = 4 * 1024

        UNLIMITED_STRING = 64 * 1024
        UNLIMITED_COLLECTION_WIDTH = 100

        def __init__(self, max_depth=None, max_width=None, max_collection_dump=None, max_string=None):
            self.max_depth = max_depth or self.DEFAULT_MAX_DEPTH
            self.max_width = max_width or self.DEFAULT_MAX_WIDTH
            self.max_collection_dump = max_collection_dump or self.DEFAULT_MAX_COLLECTION_DEPTH
            self.max_string = max_string or self.DEFAULT_MAX_STRING

        def __eq__(self, other):
            return type(self) == type(other) and self.max_depth == other.max_depth and \
                   self.max_width == other.max_width and self.max_collection_dump == other.max_collection_dump and \
                   self.max_string == other.max_string

        @classmethod
        def strict_limits(cls, obj):
            return cls(
                cls.STRICT_MAX_DEPTH,
                cls.STRICT_MAX_WIDTH,
                cls.STRICT_MAX_COLLECTION_DEPTH,
                cls.STRICT_MAX_STRING)

        @classmethod
        def default_limits(cls, obj):
            return cls(
                cls.DEFAULT_MAX_DEPTH,
                cls.DEFAULT_MAX_WIDTH,
                cls.DEFAULT_MAX_COLLECTION_DEPTH,
                cls.DEFAULT_MAX_STRING)

        @classmethod
        def tolerant_limits(cls, obj):
            return cls(
                cls.TOLERANT_MAX_DEPTH,
                cls.TOLERANT_MAX_WIDTH,
                cls.TOLERANT_MAX_COLLECTION_DEPTH,
                cls.TOLERANT_MAX_STRING)

        @classmethod
        def tailor_limits(cls, obj):
            obj_class = type(obj)
            if obj_class in NamespaceSerializerBase.STRING_TYPES or obj_class in NamespaceSerializerBase.BINARY_TYPES:
                return PythonObjectNamespace.ObjectDumpConfig(1, 0, 0, cls.UNLIMITED_STRING)
            if (obj_class in LIST_TYPE or obj_class in DICT_TYPE) and len(obj) > cls.TOLERANT_MAX_WIDTH:
                return PythonObjectNamespace.ObjectDumpConfig(max_width=cls.UNLIMITED_COLLECTION_WIDTH)
            else:
                return PythonObjectNamespace.ObjectDumpConfig.tolerant_limits(obj)

    def __init__(self, obj, dump_config=None, methods=()):
        super(PythonObjectNamespace, self).__init__(methods + self.METHODS)
        self.obj = obj
        self.obj_class = type(obj)
        self.dump_config = dump_config or self.ObjectDumpConfig()

    if six.PY3:
        def _read_attr_unsafe(self, name):
            return object.__getattribute__(self.obj, name)
    else:
        def _read_attr_unsafe(self, name):
            # In python 2, you don't technically have to inherit from `object`, so some methods aren't using
            # `__getattribute__` like object does. Therefore, we must use the unsafe alternatives
            return getattr(self.obj, name)

    def read_attribute(self, name):
        try:
            obj_dict = self._read_attr_unsafe('__dict__')
            if obj_dict is not None and name in obj_dict:
                return PythonObjectNamespace(obj_dict[name])
        except AttributeError:
            pass  # Try using __slots__

        try:
            obj_slots = self._read_attr_unsafe('__slots__')
            if obj_slots is not None and name in obj_slots:
                # Once we verified it is using slots, it's safe to go through getattr
                return PythonObjectNamespace(getattr(self.obj, name))
        except AttributeError:
            pass  # Go through to the end

        raise RookAttributeNotFound(name)

    def read_key(self, key):
        try:
            return PythonObjectNamespace(self.obj[key])
        except (KeyError, IndexError, TypeError):
            # If key is a string and object is a dictionary check if any key within the dictionary stringifies to key
            key_class = type(key)
            if key_class in six.string_types and self.obj_class in DICT_TYPE:
                for iteratorKey in self.obj:
                    if str(iteratorKey) == key:  # The str() is the important part
                        return PythonObjectNamespace(self.obj[iteratorKey])

            raise RookKeyNotFound(key)

    def type(self, args=None):
        return PythonObjectNamespace(str(self.obj_class))

    def size(self, args=None):
        return PythonObjectNamespace(len(self.obj))

    def depth(self, args):
        try:
            self.dump_config.max_depth = int(args)
        except ValueError:
            raise RookInvalidMethodArguments('depth()', args)

        return self

    def width(self, args):
        try:
            self.dump_config.max_width = int(args)
        except ValueError:
            raise RookInvalidMethodArguments('width()', args)

        return self

    def collection_dump(self, args):
        try:
            self.dump_config.max_collection_dump = int(args)
        except ValueError:
            raise RookInvalidMethodArguments('collection_dump()', args)

        return self

    def string(self, args):
        try:
            self.dump_config.max_string = int(args)
        except ValueError:
            raise RookInvalidMethodArguments('string()', args)

        return self

    def limit(self, args):
        try:
            self.dump_config = PythonObjectNamespace.dump_configs[args.lower()]
        except KeyError:
            raise RookInvalidMethodArguments('limit()', args)

        return self

    def __nonzero__(self):
        return bool(self.obj)

    if six.PY3:
        __bool__ = __nonzero__

    dump_configs = {
        '': ObjectDumpConfig.default_limits(ObjectDumpConfig),
        'strict': ObjectDumpConfig.strict_limits(ObjectDumpConfig),
        'default': ObjectDumpConfig.default_limits(ObjectDumpConfig),
        'tolerant': ObjectDumpConfig.tolerant_limits(ObjectDumpConfig)}

    METHODS = (type, size, depth, width, collection_dump, string, limit)
