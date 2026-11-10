# SPDX-FileCopyrightText: All Contributors to the PyTango project
# SPDX-License-Identifier: LGPL-3.0-or-later

"""Case-insensitive list and dict containers."""


class CaselessList(list):
    """A case insensitive lists that has some caseless methods. Only allows
    strings as list members. Most methods that would normally return a list,
    return a CaselessList. (Except list() and lowercopy())
    Sequence Methods implemented are :
    __contains__, remove, count, index, append, extend, insert,
    __getitem__, __setitem__
    __add__, __radd__, __iadd__, __mul__, __rmul__
    Plus Extra methods:
    findentry, copy , lowercopy, list
    Inherited methods :
    __imul__, __len__, __iter__, pop, reverse, sort
    """

    def __init__(self, inlist=None):
        list.__init__(self)
        if inlist is None:
            inlist = []
        for entry in inlist:
            if not isinstance(entry, str):
                raise TypeError(
                    f'Members of this object must be strings. You supplied "{entry}" which is "{type(entry)}"'
                )
            self.append(entry)

    def findentry(self, item):
        """A caseless way of checking if an item is in the list or not.
        It returns None or the entry."""
        if not isinstance(item, str):
            raise TypeError(f'Members of this object must be strings. You supplied "{type(item)}"')
        for entry in self:
            if item.lower() == entry.lower():
                return entry
        return None

    def __contains__(self, item):
        """A caseless way of checking if a list has a member in it or not."""
        return any(item.lower() == entry.lower() for entry in self)

    def remove(self, item):
        """Remove the first occurence of an item, the caseless way."""
        for entry in self:
            if item.lower() == entry.lower():
                list.remove(self, entry)
                return
        raise ValueError(": list.remove(x): x not in list")

    def copy(self):
        """Return a CaselessList copy of self."""
        return CaselessList(self)

    def list(self):
        """Return a normal list version of self."""
        return list(self)

    def lowercopy(self):
        """Return a lowercase (list) copy of self."""
        return [entry.lower() for entry in self]

    def append(self, item):
        """Adds an item to the list and checks it's a string."""
        if not isinstance(item, str):
            raise TypeError(f'Members of this object must be strings. You supplied "{type(item)}"')
        list.append(self, item)

    def extend(self, item):
        """Extend the list with another list. Each member of the list must be
        a string."""
        if not isinstance(item, list):
            raise TypeError(f'You can only extend lists with lists. You supplied "{type(item)}"')
        for entry in item:
            if not isinstance(entry, str):
                raise TypeError(f'Members of this object must be strings. You supplied "{type(entry)}"')
            list.append(self, entry)

    def count(self, item):
        """Counts references to 'item' in a caseless manner.
        If item is not a string it will always return 0."""
        if not isinstance(item, str):
            return 0
        count = 0
        for entry in self:
            if item.lower() == entry.lower():
                count += 1
        return count

    def index(self, item, minindex=0, maxindex=None):
        """Provide an index of first occurence of item in the list. (or raise
        a ValueError if item not present)
        If item is not a string, will raise a TypeError.
        minindex and maxindex are also optional arguments
        s.index(x[, i[, j]]) return smallest k such that s[k] == x and i <= k < j
        """
        if maxindex is None:
            maxindex = len(self)
        minindex = max(0, minindex)
        maxindex = min(len(self), maxindex)
        if not isinstance(item, str):
            raise TypeError(f'Members of this object must be strings. You supplied "{type(item)}"')
        for index in range(minindex, maxindex):
            if item.lower() == self[index].lower():
                return index
        raise ValueError(": list.index(x): x not in list")

    def insert(self, i, x):
        """s.insert(i, x) same as s[i:i] = [x]
        Raises TypeError if x isn't a string."""
        if not isinstance(x, str):
            raise TypeError(f'Members of this object must be strings. You supplied "{type(x)}"')
        list.insert(self, i, x)

    def __setitem__(self, index, value):
        """For setting values in the list.
        index must be an integer or (extended) slice object. (__setslice__ used
        for simple slices)
        If index is an integer then value must be a string.
        If index is a slice object then value must be a list of strings - with
        the same length as the slice object requires.
        """
        if isinstance(index, int):
            if not isinstance(value, str):
                raise TypeError(f'Members of this object must be strings. You supplied "{type(value)}"')
            list.__setitem__(self, index, value)
        elif isinstance(index, slice):
            if not hasattr(value, "__len__"):
                raise TypeError("Value given to set slice is not a sequence object.")
            for entry in value:
                if not isinstance(entry, str):
                    raise TypeError(f'Members of this object must be strings. You supplied "{type(entry)}"')
            list.__setitem__(self, index, value)
        else:
            raise TypeError("Indexes must be integers or slice objects.")

    def __getitem__(self, index):
        """For fetching indexes.
        If a slice is fetched then the list returned is a CaselessList."""
        if not isinstance(index, slice):
            return list.__getitem__(self, index)
        else:
            return CaselessList(list.__getitem__(self, index))

    def __add__(self, item):
        """To add a list, and return a CaselessList.
        Every element of item must be a string."""
        return CaselessList(list.__add__(self, item))

    def __radd__(self, item):
        """To add a list, and return a CaselessList.
        Every element of item must be a string."""
        return CaselessList(list(item) + list(self))

    def __iadd__(self, item):
        """To add a list in place."""
        for entry in item:
            self.append(entry)
        return self

    def __mul__(self, item):
        """To multiply itself, and return a CaselessList.
        Every element of item must be a string."""
        return CaselessList(list.__mul__(self, item))

    def __rmul__(self, item):
        """To multiply itself, and return a CaselessList.
        Every element of item must be a string."""
        return CaselessList(list.__rmul__(self, item))


class CaselessDict(dict):
    def __init__(self, other=None):
        if other:
            # Doesn't do keyword args
            if isinstance(other, dict):
                for k, v in other.items():
                    dict.__setitem__(self, k.lower(), v)
            else:
                for k, v in other:
                    dict.__setitem__(self, k.lower(), v)

    def __getitem__(self, key):
        return dict.__getitem__(self, key.lower())

    def __setitem__(self, key, value):
        dict.__setitem__(self, key.lower(), value)

    def __contains__(self, key):
        return dict.__contains__(self, key.lower())

    def __delitem__(self, k):
        dict.__delitem__(self, k.lower())

    def get(self, key, def_val=None):
        return dict.get(self, key.lower(), def_val)

    def setdefault(self, key, def_val=None):
        return dict.setdefault(self, key.lower(), def_val)

    def update(self, other):
        for k, v in other.items():
            dict.__setitem__(self, k.lower(), v)

    def fromkeys(self, iterable, value=None):
        d = CaselessDict()
        for k in iterable:
            dict.__setitem__(d, k.lower(), value)
        return d

    def pop(self, key, def_val=None):
        return dict.pop(self, key.lower(), def_val)

    def keys(self):
        return CaselessList(dict.keys(self))
