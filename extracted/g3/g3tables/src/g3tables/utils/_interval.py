import collections.abc
import typing
import re


class Interval(collections.abc.Sequence[str]):
    """
    Expands comma-separated and hyphen-separated string intervals to a list of
    string items with normalized indexation. For example, the interval
    "1A1-1A4, 1A7" is expanded to ["1A01", "1A02", "1A03", "1A04", "1A07"].

    - Each interval item should consist of an alphanumeric "base" followed by
    a numeric "index".
    - A non-empty base can contain any letters and numbers, but must end
    with a letter. Also, the base must be the same across the interval items,
    separated by a hyphen (-).
    - Index must be in the end of the item (thus, it cannot be followed by
    a non-numeric character).

    Args:
        interval (str): An interval to be parsed.

    Raises:
        ValueError: If the input is not a string,
        or if the bases of an interval are not identical.
        AttributeError: If an interval item cannot be split into
        a base and an index.
    """
    INTERVAL_SEPARATORS = ['-', '—']
    INDEX_PATTERN = re.compile("[0-9]+$")

    def __init__(self, interval: typing.Optional[str] = None) -> None:
        super().__init__()
        self._interval = self._check_interval_type(interval)
        self._items = self._parse_to_list()

    def __repr__(self) -> str:
        return self._interval

    def __str__(self) -> str:
        return str(self._items)

    def __getitem__(self, index):
        return self._items[index]

    def __len__(self) -> int:
        return len(self._items)

    @staticmethod
    def _check_interval_type(interval: typing.Optional[str]) -> str:
        if not interval:
            return ''
        if not isinstance(interval, str):
            raise ValueError(
                f'Input interval should be a string, '
                f'got type "{type(interval).__name__}."'
                )
        return interval.strip()

    def _get_sep(self, item: str):
        seps = self.INTERVAL_SEPARATORS
        return next((sep for sep in seps if sep in item), None)

    def _get_item_index(self, item: str) -> int:
        try:
            result = self.INDEX_PATTERN.search(item)
            assert result is not None
            return int(result.group())
        except AssertionError:
            raise TypeError(f'Cannot extract index from item {item}.')

    def _get_item_base(self, item: str):
        try:
            return self.INDEX_PATTERN.sub("", item, count=1)
        except Exception as err:
            raise AttributeError(
                f'Cannot extract interval base from interval {self._interval}.'
                ) from err

    def _parse_to_list(self):
        items = []
        for item in self._interval.split(sep=','):
            item = item.strip()
            if not item:
                continue
            sep = self._get_sep(item)
            if sep is None:
                items.append(item)
                continue
            boundaries = [boundary.strip() for boundary in item.split(sep=sep)]
            boundary_lower = self._get_item_index(boundaries[0])
            boundary_upper = self._get_item_index(boundaries[1])
            interval_base = self._get_item_base(boundaries[0])
            if interval_base != self._get_item_base(boundaries[1]):
                raise ValueError(
                    f'Cannot extract base from interval {self._interval}.'
                    )
            interval_range = range(boundary_lower, boundary_upper + 1)
            for i in interval_range:
                items.append(f'{interval_base}{i:02d}')
        return items
