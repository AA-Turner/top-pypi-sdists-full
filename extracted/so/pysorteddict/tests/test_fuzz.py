import builtins
import decimal
import math
import random
import re
import string

import pytest

from pysorteddict import SortedDict

unsupported_types = {bool, bytearray, complex, dict, Exception, frozenset, list, set, tuple, type}
# Needs to be ordered. See https://github.com/pytest-dev/pytest-xdist/issues/432.
supported_types = [bytes, int, float, str, decimal.Decimal]
all_types = [*unsupported_types.union(supported_types)]


class TestFuzz:
    def _gen(self, key_type: type | None = None):
        match key_type := key_type or self._rg.choice((bytes, frozenset, int, list, set, tuple, str)):
            case builtins.bool:
                return bool(self._rg.getrandbits(1))
            case builtins.bytearray | builtins.frozenset | builtins.list | builtins.set | builtins.tuple:
                return key_type(self._gen(bytes))
            case builtins.complex:
                return self._gen(float) + self._gen(float) * 1j
            case builtins.bytes:
                return self._rg.randbytes(self._rg.randrange(16, 32))
            case builtins.dict:
                return {b: b for b in self._gen(bytes)}
            case builtins.Exception:
                return Exception()
            case builtins.int:
                return self._rg.randrange(1_000, 2_000)
            case builtins.float | decimal.Decimal:
                # I want a non-negligible repetition chance. Hence the kludge.
                return key_type(self._rg.choices([*range(1_000), "-inf", "inf", "nan"], [1] * 1_002 + [100])[0])
            case builtins.str:
                return "".join(self._rg.choices(string.ascii_lowercase, k=self._rg.randrange(20, 30)))
            case builtins.type:
                return self._rg.choice(all_types)
            case _:
                raise RuntimeError(key_type)

    @pytest.mark.parametrize("key_type", supported_types)
    def test_fuzz(self, key_type: type):
        self._rg = random.Random(f"{__name__}-{key_type.__name__}")
        self.key_type = key_type
        self._test___new__()

        attrs = {*dir(SortedDict)}.difference((
            "__class__", "__dict__", "__dir__", "__doc__", "__eq__", "__format__", "__ge__", "__getattr__",
            "__getattribute__", "__getstate__", "__gt__", "__hash__", "__init__", "__init_subclass__", "__le__",
            "__len__", "__lt__", "__ne__", "__reduce__", "__reduce_ex__", "__repr__", "__setattr__", "__sizeof__",
            "__str__", "__subclasshook__", "__weakref__", "items", "key_type", "values",
        ))  # fmt: skip
        for attr in self._rg.choices([*attrs], k=50_000):
            getattr(self, f"_test_{attr}")()

            with pytest.raises(TypeError, match="^unhashable type: 'pysorteddict.SortedDict'$"):
                hash(self.sorted_dict)
            if self.is_sorted_dict_new:
                assert self.sorted_dict.key_type is None
            else:
                assert self.sorted_dict.key_type is self.key_type

            sorted_normal_dict = dict(sorted(self.normal_dict.items()))
            assert len(self.sorted_dict) == len(sorted_normal_dict)
            assert repr(self.sorted_dict) == f"SortedDict({sorted_normal_dict})"
            assert self.sorted_dict.items() == [*sorted_normal_dict.items()]
            assert self.sorted_dict.values() == [*sorted_normal_dict.values()]

    def _test___contains__(self):
        for key_type in all_types:
            key = self._gen(key_type)
            if self.is_sorted_dict_new:
                with pytest.raises(RuntimeError, match="^key type not set: insert at least one item first$"):
                    key in self.sorted_dict  # noqa: B015
                continue
            if key_type is not self.key_type:
                with pytest.raises(
                    TypeError,
                    match=re.escape(f"got key {key!r} of type {key_type!r}, want key of type {self.key_type!r}"),
                ):
                    key in self.sorted_dict  # noqa: B015
                continue
            if (key_type is float or key_type is decimal.Decimal) and math.isnan(key):
                with pytest.raises(ValueError, match=re.escape(f"got bad key {key!r} of type {key_type!r}")):
                    key in self.sorted_dict  # noqa: B015
                continue
            if self.normal_dict:
                assert self._rg.choice([*self.normal_dict]) in self.sorted_dict
            assert (key in self.sorted_dict) == (key in self.normal_dict)

    def _test___delattr__(self):
        with pytest.raises(AttributeError):
            delattr(self.sorted_dict, "key_type")
        for attr in ("clear", "copy", "items", "keys", "values"):
            with pytest.raises(AttributeError):
                delattr(self.sorted_dict, attr)

    def _test___delitem__(self):
        for key_type in all_types:
            key = self._gen(key_type)
            if self.is_sorted_dict_new:
                with pytest.raises(RuntimeError, match="^key type not set: insert at least one item first$"):
                    del self.sorted_dict[key]
                continue
            if key_type is not self.key_type:
                with pytest.raises(
                    TypeError,
                    match=re.escape(f"got key {key!r} of type {key_type!r}, want key of type {self.key_type!r}"),
                ):
                    del self.sorted_dict[key]
                continue
            if (key_type is float or key_type is decimal.Decimal) and math.isnan(key):
                with pytest.raises(ValueError, match=re.escape(f"got bad key {key!r} of type {key_type!r}")):
                    del self.sorted_dict[key]
                continue
            if key not in self.normal_dict:
                with pytest.raises(KeyError, match=re.escape(repr(key))):
                    del self.sorted_dict[key]
                continue
            del self.normal_dict[key]
            del self.sorted_dict[key]

    def _test___getitem__(self):
        for key_type in all_types:
            key = self._gen(key_type)
            if self.is_sorted_dict_new:
                with pytest.raises(RuntimeError, match="^key type not set: insert at least one item first$"):
                    self.sorted_dict[key]
                continue
            if key_type is not self.key_type:
                with pytest.raises(
                    TypeError,
                    match=re.escape(f"got key {key!r} of type {key_type!r}, want key of type {self.key_type!r}"),
                ):
                    self.sorted_dict[key]
                continue
            if (key_type is float or key_type is decimal.Decimal) and math.isnan(key):
                with pytest.raises(ValueError, match=re.escape(f"got bad key {key!r} of type {key_type!r}")):
                    self.sorted_dict[key]
                continue
            if key not in self.normal_dict:
                with pytest.raises(KeyError, match=re.escape(repr(key))):
                    self.sorted_dict[key]
                continue
            assert self.sorted_dict[key] == self.normal_dict[key]

    def _test___new__(self):
        self.normal_dict = {}
        self.sorted_dict = SortedDict()
        self.sorted_dict_keys = self.sorted_dict.keys()
        self.is_sorted_dict_new = True

    def _test___setitem__(self):
        for key_type in all_types:
            key, value = self._gen(key_type), self._gen()
            if self.is_sorted_dict_new and key_type in unsupported_types:
                with pytest.raises(
                    TypeError,
                    match=re.escape(f"got key {key!r} of unsupported type {key_type!r}"),
                ):
                    self.sorted_dict[key] = value
                continue
            if not self.is_sorted_dict_new and key_type is not self.key_type:
                with pytest.raises(
                    TypeError,
                    match=re.escape(f"got key {key!r} of type {key_type!r}, want key of type {self.key_type!r}"),
                ):
                    self.sorted_dict[key] = value
                continue
            if (
                (key_type is float or key_type is decimal.Decimal)
                and math.isnan(key)
                and (self.is_sorted_dict_new or self.key_type is key_type)
            ):
                with pytest.raises(ValueError, match=re.escape(f"got bad key {key!r} of type {key_type!r}")):
                    self.sorted_dict[key] = value
                continue
            if key_type is self.key_type:
                self.normal_dict[key] = value
                self.sorted_dict[key] = value
                self.is_sorted_dict_new = False

    def _test_clear(self):
        self.normal_dict.clear()
        self.sorted_dict.clear()

    def _test_copy(self):
        self.sorted_dict = self.sorted_dict.copy()
        self.sorted_dict_keys = self.sorted_dict.keys()

    def _test_keys(self):
        sorted_normal_dict_keys = sorted(self.normal_dict.keys())
        assert repr(self.sorted_dict_keys) == f"SortedDictKeys({sorted_normal_dict_keys})"
        assert len(self.sorted_dict_keys) == len(sorted_normal_dict_keys)
        assert [*self.sorted_dict_keys] == sorted_normal_dict_keys


if __name__ == "__main__":
    pytest.main()
