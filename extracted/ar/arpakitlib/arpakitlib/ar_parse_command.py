# arpakit
import os
import shlex

from pydantic import BaseModel

_ARPAKIT_LIB_MODULE_VERSION = "3.0"


class BadCommandFormat(Exception):
    pass


class ParsedCommand(BaseModel):
    command: str
    full_command: str
    key_to_value: dict[str, str | None] = {}
    values_without_key: list[str] = []

    @property
    def keys(self) -> list[str]:
        return [k for k, v in self.key_to_value.items() if v is not None]

    @property
    def flags(self) -> list[str]:
        return [k for k, v in self.key_to_value.items() if v is None]

    @property
    def values(self) -> list[str]:
        return [self.key_to_value[k] for k in self.keys]

    def get_value_by_key(self, key: str) -> str | None:
        return self.key_to_value.get(key)

    def get_value_by_keys(self, keys: list[str]) -> str | None:
        for key in keys:
            if self.key_exists(key=key):
                return self.get_value_by_key(key=key)
        return None

    def key_exists(self, key: str) -> bool:
        return key in self.key_to_value.keys()

    def keys_exists(self, keys: list[str]) -> bool:
        for key in keys:
            if key in self.keys:
                return True
        return False

    def has_flag(self, flag: str) -> bool:
        return flag in self.flags

    def get_value_by_index(self, index: int) -> str | None:
        if index >= len(self.values_without_key):
            return None
        return self.values_without_key[index]


def parse_command(text: str) -> ParsedCommand:
    text = text.removeprefix("/")
    text = " ".join([text_.strip() for text_ in text.split(" ") if text_.strip()]).strip()

    parts = shlex.split(text)
    if not parts:
        raise BadCommandFormat("not parts")
    if len(parts[0]) == 1:
        raise BadCommandFormat("len(parts[0]) == 1")

    res = ParsedCommand(full_command=parts[0], command=os.path.basename(parts[0]).removeprefix("/"))

    last_key: str | None = None
    for part in parts[1:]:
        part = part.strip()

        if not part:
            raise BadCommandFormat("not part")
        if part == "-" or part == "--":
            raise BadCommandFormat("part == '-' or part == '--'")

        if part.startswith("-") or part.startswith("--"):  # if it is key
            if part.startswith("-"):
                part = part[1:]
            if part.startswith("-"):
                part = part[1:]
            if part.startswith("-"):
                raise BadCommandFormat("a lots of -")

            if part in res.key_to_value:
                raise BadCommandFormat(f"{part} in {res.key_to_value}")

            res.key_to_value[part] = None
            last_key = part

            continue

        if last_key is not None:  # if it is value
            res.key_to_value[last_key] = part
            last_key = None
            continue

        res.values_without_key.append(part)  # if it is values_without_key

    return res


def __example():
    pass


if __name__ == '__main__':
    __example()
