import json
from collections.abc import Iterable
from io import IOBase
from typing import Any


class Dict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.__none_props__ = {}
        self.update(*args, **kwargs)

    def update(self, *args, **kwargs):
        result = {}
        for k, v in dict(*args, **kwargs).items():
            if isinstance(v, dict) and not isinstance(v, Dict):
                result[k] = Dict(v)
            elif isinstance(v, list) and not isinstance(v, List):
                result[k] = List(v)
            elif isinstance(v, NoneProp):
                continue
            else:
                result[k] = v

        super().update(result)

    def __repr__(self):
        return pprint(self, indent=None)

    def __dir__(self):
        result = list(super().__dir__())
        result.remove("__none_props__")
        return result

    def __missing__(self, key):
        return self.__getattr__(key)

    def __getattr__(self, key):
        if key in self:
            value = self[key]
        elif key in self.__none_props__:
            value = self.__none_props__[key]
        else:
            value = self.__none_props__[key] = NoneProp(self, key)
        return value

    def __setitem__(self, key, value):
        self.update({key: value})

    def __setattr__(self, key, value):
        if key == "__none_props__":
            super().__setattr__(key, value)
        else:
            if key in dir(self):
                raise AttributeError('"%s" is a protected method. Use key indexing to set attribute.' % key)
            self.update({key: value})


class List(list):
    def __init__(self, iterable: Iterable | None = None):
        iterable = iterable or ()

        for x in iterable:
            self.append(x)

    def append(self, item):
        self.insert(len(self), item)

    def extend(self, lst):
        for item in lst:
            self.append(item)

    def __setitem__(self, index, item):
        if isinstance(item, dict) and not isinstance(item, Dict):
            item = Dict(item)
        elif isinstance(item, list) and not isinstance(item, List):
            item = List(item)

        super().__setitem__(index, item)

    def insert(self, index, item):
        if isinstance(item, dict) and not isinstance(item, Dict):
            item = Dict(item)
        elif isinstance(item, list) and not isinstance(item, List):
            item = List(item)

        super().insert(index, item)


class NoneProp:
    def __init__(self, parent: "Dict | NoneProp", key: str):
        self.__parent__ = parent
        self.__key__ = key

    def __repr__(self):
        return ""

    def __str__(self):
        return ""

    def __eq__(self, obj):
        return obj is None

    def __lt__(self, obj):
        return obj is not None

    def __gt__(self, obj):
        return False

    def __bool__(self):
        return False

    def __len__(self):
        return 0

    def __iter__(self):
        yield from []

    def __contains__(self, key):
        return False

    def __setattr__(self, key, value):
        if key == "__parent__" or key == "__key__":
            super().__setattr__(key, value)
        else:
            parent = self.__parent__
            keys = [self.__key__]
            while not isinstance(parent, Dict):
                keys.append(parent.__key__)
                parent = parent.__parent__

            getattr(parent, "__none_props__", {}).pop(keys[-1], None)

            result = {key: value}

            for k in keys:
                result = {k: result}

            parent.update(result)

    def __delattr__(self, key):
        pass

    def __getattr__(self, key):
        return NoneProp(self, key)

    def __getitem__(self, key):
        return self.__getattr__(key)

    def __setitem__(self, key, value):
        self.__setattr__(key, value)


def parse(data: Any):
    if isinstance(data, dict):
        return Dict(data)
    elif isinstance(data, list):
        return List(data)
    else:
        return data


def loads(s: str | bytes | bytearray, *args, **kwargs):
    return parse(json.loads(s, *args, **kwargs))


def load(fp: IOBase, *args, **kwargs):
    return parse(json.load(fp, *args, **kwargs))


def dumps(obj: Any, *args, **kwargs):
    return json.dumps(obj, *args, **kwargs)


def dump(obj: Any, fp: IOBase, *args, **kwargs):
    return json.dump(obj, fp, *args, **kwargs)


def pprint(data: list | dict, *args, indent: int | str | None = 4, **kwargs):
    return json.dumps(data, *args, indent=indent, **kwargs)
