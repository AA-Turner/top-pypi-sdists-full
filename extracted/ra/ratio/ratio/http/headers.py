import contextlib
from typing import Set, Iterator, Any


EncodedHeader = tuple[bytes, bytes]
Header = tuple[str, str]
DISALLOWED_HEADER_NAME_CHARACTERS = r'(),/:;<=>?@[\]{}"'


def _assert_valid_header_name(value: str) -> None:
    is_valid = not any(
        map(lambda character: character in DISALLOWED_HEADER_NAME_CHARACTERS, value)
    )

    if not is_valid:
        raise ValueError(f'Invalid name for HTTP header: "{value}"')


class Headers:
    __collection: dict[str, Set[str]]

    def __init__(self, initial: dict[str, Set[str]] | None = None):
        if initial is None:
            initial = {}

        for header_name in initial:
            _assert_valid_header_name(header_name)

        self.__collection = {key.lower(): value for key, value in initial.items()}

    def __iter__(self) -> Iterator[tuple[str, Set[str]]]:
        yield from self.__collection.items()

    def __contains__(self, item: Any) -> bool:
        return self.get(item) is not None

    def __len__(self) -> int:
        return sum([len(item) for item in self.__collection.values()])

    def add(self, name: str, value: str) -> None:
        normalized_name = name.lower()
        _assert_valid_header_name(normalized_name)

        if self.__collection.get(normalized_name, None) is not None:
            self.__collection[normalized_name].add(value)
        else:
            self.__collection[normalized_name] = {value}

    def get(self, name: str) -> Set[str] | None:
        return self.__collection.get(name.lower(), None)

    def put(self, name: str, value: Set[str]) -> None:
        normalized_name = name.lower()
        _assert_valid_header_name(normalized_name)

        self.__collection[normalized_name] = value

    def remove(self, name: str) -> None:
        with contextlib.suppress(KeyError):
            del self.__collection[name.lower()]

    def encode(self) -> list[EncodedHeader]:
        return [
            (name.lower().encode("utf-8"), value.encode("utf-8"))
            for name in self.__collection
            for value in self.__collection[name]
        ]
