from typing import Any


class CaseInsensitiveDict(dict[str, Any]):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.update(*args, **kwargs)

    def __setitem__(self, key, value):
        super().__setitem__(key.lower(), value)

    def __getitem__(self, key):
        return super().__getitem__(key.lower())

    def __delitem__(self, key):
        return super().__delitem__(key.lower())

    def __contains__(self, key):
        return super().__contains__(key.lower())

    def get(self, key, default=None):
        return super().get(key.lower(), default)

    def update(self, other=None, **kwargs):
        if other:
            if hasattr(other, "keys"):
                for k in other:
                    self[k.lower()] = other[k]
            else:
                for k, v in other:
                    self[k.lower()] = v
        for k in kwargs:
            self[k.lower()] = kwargs[k]
