"""Definition of ListQuerySet."""

from collections import OrderedDict
from dataclasses import dataclass
from typing import Any


class QuerySetQueryStub:
    """A stub to implement the query property."""

    def __init__(self) -> None:
        self.select_related = None
        self.order_by = []


@dataclass
class _FilterObj:
    """A filter object."""

    field: str
    lookup: str
    value: str

    def is_matching(self, obj: Any) -> bool:
        """Return True, when obj is matching this filter, else False."""
        obj_value = str(getattr(obj, self.field))
        if self.lookup == "exact":
            return self.value == obj_value

        if self.lookup == "contains":
            return self.value in obj_value

        if self.lookup == "icontains":
            return self.value.lower() in obj_value.lower()

        raise NotImplementedError(f"Unknown lookup: {self.lookup}")

    @classmethod
    def create(cls, key: str, value: Any) -> "_FilterObj":
        """Create new filter from key/value pair."""
        parts = key.split("__")

        if len(parts) == 1:
            field = key
            lookup = "exact"

        elif len(parts) == 2:
            field, lookup = parts

        else:
            raise ValueError(f"Invalid key in filter: {key}")

        return cls(field=field, lookup=lookup, value=str(value))


class ListAsQuerySet(list):
    """Masquerade a list as QuerySet.

    Args:
        - model: Django model (mandatory)
        - is_distinct: Whether result should be distinct (optional)
    """

    def __init__(self, *args, model, **kwargs):
        self.model = model
        self.is_distinct = kwargs.pop("is_distinct", False)
        self.query = QuerySetQueryStub()

        super().__init__(*args, **kwargs)
        self._id_mapper = {str(obj.id): n for n, obj in enumerate(self)}
        self._list_size = len(self)

    def all(self) -> "ListAsQuerySet":
        """:private:"""
        if self.is_distinct:
            return self._make_list_distinct(self)
        return self

    def count(self) -> int:
        """:private:"""
        return self._list_size

    def _clone(self):
        return self._make_clone()

    def _make_clone(self, new_list: list = None) -> "ListAsQuerySet":
        if new_list is None:
            new_list = self
        obj = type(self)(list(new_list), model=self.model, is_distinct=self.is_distinct)
        return obj

    def create(self, *args, **kwargs) -> Any:
        """:private:"""
        raise NotImplementedError("ListAsQuerySet can not write to the database.")

    def distinct(self) -> "ListAsQuerySet":
        """:private:"""
        self.is_distinct = True
        return self

    def first(self) -> Any:
        """:private:"""
        try:
            return self[0]
        except IndexError:
            return None

    def filter(self, *args, **kwargs) -> "ListAsQuerySet":
        """:private:"""
        if args:
            raise NotImplementedError(
                f"filter with positional args not supported: {args=} {kwargs=}"
            )

        if not kwargs:
            return self

        filter_objs = [_FilterObj.create(key, value) for key, value in kwargs.items()]

        new_list = [
            obj
            for obj in self
            if all(filter_obj.is_matching(obj) for filter_obj in filter_objs)
        ]

        return self._make_clone(new_list=new_list)

    def get(self, *args, **kwargs) -> Any:
        """:private:"""
        try:
            return self[self._id_mapper[str(kwargs["id"])]]
        except KeyError:
            raise self.model.DoesNotExist from None

    def last(self) -> Any:
        """:private:"""
        try:
            return self[-1]
        except IndexError:
            return None

    def none(self) -> "ListAsQuerySet":
        """:private:"""
        return self._make_clone(new_list=[])

    def order_by(self, *args, **kwargs):
        """:private:"""
        if not args and not kwargs:
            return self

        if kwargs:
            raise NotImplementedError("order with kw args not supported.")

        new_list = list(self)
        for prop in reversed(args):
            if prop[0:1] == "-":
                reverse = True
                prop_2 = prop[1:]
            else:
                reverse = False
                prop_2 = prop

            # pylint: disable = cell-var-from-loop
            new_list.sort(key=lambda d: getattr(d, prop_2), reverse=reverse)

        return self._make_clone(new_list=new_list)

    def values(self, *args):
        """:private:"""
        result = list(self._values(*args))
        if self.is_distinct:
            return list(
                OrderedDict((frozenset(item.items()), item) for item in result).values()
            )
        return result

    def _values(self, *args):
        result = (
            {k: v for k, v in obj.__dict__.items() if not args or k in args}
            for obj in self
        )
        return result

    def values_list(self, *args, **kwargs):
        """:private:"""
        items = (tuple(obj.values()) for obj in self._values(*args))
        if kwargs.get("flat"):
            if len(args) > 1:
                raise TypeError(
                    "'flat' is not valid when values_list is called with "
                    "more than one field."
                )
            items = (obj[0] for obj in items)
            if self.is_distinct:
                return self._make_list_distinct(items)

        result = list(items)
        return result

    @staticmethod
    def _make_list_distinct(items):
        return list(dict.fromkeys(items))
