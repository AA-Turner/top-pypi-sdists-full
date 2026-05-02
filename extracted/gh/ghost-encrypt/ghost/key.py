# key.py

try:
    from .config import Config
except ImportError:
    from config import Config
from random import choice


class Key:
    def __init__(self, string_key: str = None):
        self.string = string_key
        self.cfg = Config()
        if not self.string:
            self.key_len = int(self.cfg["key_size"])
            self.generate()
        self.string.replace("\"", "").replace("'", "")

    def __len__(self):
        return len(self.string)

    def __repr__(self):
        return self.string

    def __getitem__(self, item):
        return self.string[item]

    def generate(self):
        self.string = "".join(choice([_ for _ in self.cfg["chars"]]) for _ in range(self.key_len))
