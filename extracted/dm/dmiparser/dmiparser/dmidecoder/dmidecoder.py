import json
import shlex
from subprocess import check_output
from typing import List, Optional

from dmiparser import DmiParser

__all__ = ["DmiDecoder"]


class DmiDecoder:
    """This is a simple dmiparser wrapper"""

    def __init__(self, arguments: Optional[str] = None, command: str = "dmidecode", **kwargs) -> None:
        """
        @param arguments: command's extra arguments like "-t 4"
        @param command: an executable dmidecode command
        @param kwargs: these will pass to dmiparser
        """
        argv: List[str] = shlex.split(command)

        if arguments:
            argv.extend(shlex.split(arguments))

        text = check_output(argv, shell=False, encoding="utf8")
        parser = DmiParser(text, **kwargs)
        self._text = str(parser)
        self._data = json.loads(self._text)

    @property
    def text(self) -> str:
        """
        @return: dmidecode output parsed JSON text
        """
        return self._text

    @property
    def data(self) -> list:
        """
        @return: dmidecode output parsed JSON object
        """
        return self._data

    @property
    def sections(self) -> list:
        """
        @return: a list for all section id and section name
        """
        return [(x["handle"]["id"], x["name"]) for x in self.data]

    def get(self, *keys: str, id: str = "", name: str = "") -> list:
        """get information for a section

        @param keys: hash keys for a section
        @param id: section id like '0x0020'
        @param name: section name like 'Processor Information'
        @return: section information values
        """
        if len(keys) == 0:
            raise TypeError("get() requires at least one key, got 0")

        data = self._data
        values = []

        for d in data:
            if id and id != d["handle"]["id"]:
                continue

            if name and name != d["name"]:
                continue

            d_ = d

            for k in keys:
                try:
                    d_ = d_[k]
                except (KeyError, TypeError):
                    d_ = None
                    break

            if d_ is not None:
                if isinstance(d_, list):
                    values.extend(d_)
                else:
                    values.append(d_)

        return values

    def getProp(self, prop: str, id: str = "", name: str = "") -> list:
        """get values for a section property

        @param prop: property name
        @param id: section id like '0x0020'
        @param name: section name like 'Processor Information'
        @return: section property values
        """
        keys = ["props"]
        keys.extend([prop, "values"])

        return self.get(*keys, id=id, name=name)
