# config.py

import platform


class Config:
    def __init__(self):
        self.cfg = None
        self.desc = []
        if platform.system() == "Windows":
            self.path = "".join([_ + "\\" for _ in __file__.split("\\")][:-1]) + "data\\.config"
        else:
            self.path = "".join([_ + "/" for _ in __file__.split("/")][:-1]) + "data/.config"
        self.load_cfg()

    def __getitem__(self, item):
        return self.cfg[item]

    def __setitem__(self, key, value):
        self.cfg[key] = value
        return None

    def __len__(self):
        return len(self.cfg)

    def __repr__(self):
        return f"Class Config from {__name__}\nPath: '{self.path}'\nValues: {self.cfg}"

    def update(self):
        self.load_cfg()

    def load_cfg(self):
        try:
            with open(self.path, "r") as f:
                content = f.read().split(";\n")
                values = {}
                for field in content:
                    if field != "":
                        values[field.split(": ")[0]] = field.split(": ")[1]
                self.cfg = values
        except FileNotFoundError:
            raise Exception(f"Couldn't find config file at {self.path}")

    def write_cfg(self):
        try:
            with open(self.path, "w") as f:
                string = ""
                for key in self.cfg:
                    string += key + ": " + self.cfg[key] + ";\n"
                f.write(string)
        except FileNotFoundError:
            raise Exception(f"Couldn't find config file at {self.path}")
