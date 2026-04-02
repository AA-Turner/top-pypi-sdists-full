import copy


class SimpleAttributeDict(dict):
    def __getattr__(self, item):
        return self[item]

    def __setattr__(self, key, value):
        self[key] = value

    def __deepcopy__(self, memo):
        copied = SimpleAttributeDict()
        for k, v in self.items():
            copied[copy.deepcopy(k, memo)] = copy.deepcopy(v, memo)
        return copied
