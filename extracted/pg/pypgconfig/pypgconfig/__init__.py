from dataclasses import dataclass, field
from typing import Tuple, Optional, Dict, List
from pathlib import Path
import subprocess


@dataclass
class Flags:
    payload: str

    def __post_init__(self):
        pass


@dataclass
class Version:
    payload: str

    parsed_items: Tuple = field(init=False)

    def __post_init__(self):
        self.parsed_items = tuple((int(f) for f in self.payload.split(".")))

    @property
    def major(self) -> int:
        return self.parsed_items[0]

    @property
    def minor(self) -> int:
        return self.parsed_items[1]

    @property
    def patch(self) -> Optional[int]:
        try:
            return self.parsed_items[2]
        except IndexError:
            return None

    def __str__(self):
        return self.payload


@dataclass
class PgConfig:
    payload: str

    items: Dict[str, str] = field(default_factory=dict, init=False)
    version: Version = field(init=False)

    def __post_init__(self):
        for line in self.payload.splitlines():
            attr, content = line.split(" = ")

            self.items[attr] = content.lstrip().rstrip()
            if attr == "VERSION":
                self.version = Version(content.split(" ")[-1])

            if attr not in ["VERSION"]:
                # The attrs ignored here are parsed and accessed as properties
                setattr(self, attr, content)

    @property
    def libs(self) -> List[str]:
        """Input: -lpgcommon -lpgport -llz4 -lxml2 -lz -lreadline -lm to
        Output: ['pgcommon', 'pgport', 'lz4', 'xml2', 'z', 'readline', 'm']
        """
        return [l[2:] for l in self.items["LIBS"].split(" ")]

    @property
    def with_python(self) -> bool:
        return "--with-python" in self.CONFIGURE

    @property
    def pythonpath(self) -> Path:
        for f in self.CONFIGURE.split(" "):
            f = f.replace("'", "")
            if f.startswith("PYTHON"):
                return Path(f.replace("PYTHON=", ""))

    @property
    def pythonpath_matches(self):
        import sys

        return self.pythonpath.resolve() == Path(sys.executable).resolve()


def which_pgconfig() -> Path:
    output = subprocess.check_output(["which", "pg_config"], text=True).strip()
    return Path(str(output))


def detect():
    p = which_pgconfig()
    pg_config_output = subprocess.check_output(p, text=True)
    return PgConfig(pg_config_output)
