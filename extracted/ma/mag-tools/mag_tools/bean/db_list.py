from typing import  Iterator, Optional, TypeVar, Generic

from mag_tools.bean.db_page import DbPage

T = TypeVar('T')

class DbList(Generic[T]):
    def __init__(self, data: list[T] = None, page: Optional[DbPage] = None, total_count: int = -1):
        self.__data = data if data is not None else []
        self.__page = page if page is not None else DbPage(1, 10)
        self.total_count = total_count

    def set_page(self, page: DbPage):
        self.__page = page if page is not None else DbPage(1, 10)

    @property
    def size(self) -> int:
        return len(self.__data)

    def add(self, e: T):
        self.__data.append(e)

    def get(self, idx: int) -> T:
        if idx < 0 or idx >= self.size:
            return None
        return self.__data[idx]

    @property
    def is_empty(self) -> bool:
        return self.size == 0

    def clear(self):
        self.__data.clear()
        self.total_count = 0
        self.__page = None

    @property
    def data(self) -> list[T]:
        if self.__page:
            start = (self.__page.index - 1) * self.__page.size
            end = start + self.__page.size
            return self.__data[start:end]
        return self.__data

    def __iter__(self) -> Iterator[T]:
        return iter(self.__data)

    def __getitem__(self, idx: int) -> T:
        return self.get(idx)

    def __setitem__(self, idx: int, value: T):
        if 0 <= idx < self.size:
            self.__data[idx] = value
        else:
            raise IndexError("Index out of range")

    def __delitem__(self, idx: int):
        if 0 <= idx < self.size:
            del self.__data[idx]
        else:
            raise IndexError("Index out of range")
