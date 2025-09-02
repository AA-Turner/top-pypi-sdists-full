# Basic Flattening Utility
# Author: Spencer Hanson, for Swimlane


import re
import json
from types import FunctionType, LambdaType, MethodType, CodeType, GeneratorType, TracebackType, FrameType
from types import GetSetDescriptorType, MemberDescriptorType
from datetime_parser import try_parse_dt
from dict_plus import SortedDictPlus
import pendulum
import datetime

BinaryType = bytes
TextType = str

# Remapping of types from py2 to py3
import types
from builtins import str as unicode

NoneType = type(None)
TypeType = NoneType
BooleanType = type(True)
IntType = int
LongType = float
FloatType = LongType
ComplexType = NoneType
ClassType = type
InstanceType = getattr(types, "InstanceType", object)
UnboundMethodType = types.FunctionType
ModuleType = NoneType
FileType = NoneType
XRangeType = NoneType
BufferType = NoneType
SliceType = NoneType
EllipsisType = NoneType
DictProxyType = NoneType
NotImplementedType = NoneType
StringTypes = str
TupleType = tuple
ListType = list
DictType = dict


"""
Flattener file to provide utilites for dealing with messy JSON
"""


class BasicList(object):
    """Class to keep track of Lists of Basic Types
    """

    def __init__(self, v):
        self.v = v


class Flattener(object):
    """
    Flattener class to easily flatten JSON
    """

    BASIC_TYPES = (NoneType, TypeType, BooleanType, IntType, LongType, FloatType, ComplexType, FunctionType, LambdaType,
                   GeneratorType, CodeType, ClassType, InstanceType, MethodType, UnboundMethodType, ModuleType,
                   FileType, XRangeType, SliceType, EllipsisType, TracebackType, FrameType, BufferType, DictProxyType,
                   NotImplementedType, GetSetDescriptorType, MemberDescriptorType, StringTypes, BinaryType, TextType,
                   BasicList)

    LIST_TYPES = (TupleType, ListType, set, frozenset)

    DICT_TYPES = (DictType, SortedDictPlus)

    def __init__(self, prefix=None, stringify_lists=True, shallow_flatten=False,
                 keep_simple_lists=True, autoparse_dt_strs=False, special_dt_formats=None, oldest_dt_allowed=None,
                 ignore_dt_formats=None, flatten_type_override=None, remove_single_lists=True):
        """
        Create a new Flattener object with specific options

        Args:
            prefix: Prefix to add to the data after flattening
            stringify_lists: Should we turn lists with basic types into CSVs? Defaults to True
            shallow_flatten: Should we ignore the first level of nesting, and only flatten each element within it?
            Used for lists of dictionaries
            keep_simple_lists: If a list in the resulting flattened dict is only integers or only strings, even if
            stringify_lists is True, keep this list
            autoparse_dt_strs: Do we attempt to automatically parse datetime looking strings/ints/floats to ISO8601?
            special_dt_formats: List of string formats to attempt parsing on for auto DT parsing. Will be ignored if
            autoparse_dt_strs is False
            oldest_dt_allowed: String of the oldest datetime that is allowed to be parsed. Defaults to 2005
            ignore_dt_formats: A list of formats to ignore when autoconverting a string to a timestamp
            flatten_type_override: A dictionary of {Type: func(data)->flattened data} for a given type
        """

        self._basic_types = list(Flattener.BASIC_TYPES)
        self._list_types = list(Flattener.LIST_TYPES)
        self._dict_types = list(Flattener.DICT_TYPES)

        self._type_override = {
            datetime.datetime: lambda x: str(x)
        }

        self.prefix = prefix
        self.stringify_lists = stringify_lists
        self.shallow_flatten = shallow_flatten
        self.keep_simple_lists = keep_simple_lists
        self.autoparse_dt_strs = autoparse_dt_strs
        self.remove_single_lists = remove_single_lists

        if ignore_dt_formats:
            if not isinstance(ignore_dt_formats, list):
                raise ValueError("Invalid ignored datetime format!, Must be list!")
            self.ignore_dt_formats = ignore_dt_formats
        else:
            self.ignore_dt_formats = None

        if special_dt_formats:
            if not isinstance(special_dt_formats, list):
                raise ValueError("Invalid special datetime format!, Must be list!")

            self.special_dt_formats = special_dt_formats
        else:
            self.special_dt_formats = []

        if oldest_dt_allowed:
            self.oldest_dt_allowed = pendulum.parse(oldest_dt_allowed, strict=False)
        else:
            self.oldest_dt_allowed = pendulum.parse("2005")

        if flatten_type_override:
            self._type_override.update(flatten_type_override)

        # Validate the type override mapping by removing any duplicate types from the other types
        for k, v in self._type_override.items():
            for typelist in [self._basic_types, self._list_types, self._dict_types]:
                if k in typelist:
                    idx = typelist.index(k)
                    typelist.pop(idx)

        # Convert types to tuples
        self._basic_types = tuple(self._basic_types)
        self._list_types = tuple(self._list_types)
        self._dict_types = tuple(self._dict_types)

    def _try_parse_dt(self, value, is_number=False):
        """ See docstring of swimbundle_utils.helpers.try_parse_dt"""
        return try_parse_dt(
            value, is_number=is_number,
            ignore_dt_formats=self.ignore_dt_formats,
            special_dt_formats=self.special_dt_formats,
            oldest_dt_allowed=self.oldest_dt_allowed
        )

    def combine_list(self, data, key):
        """Combine a list or listdict into a dict entry to be flattened.

        Examples:

            Combine a list into a key::

                >>>combine_list([1,2,3], "a")
                {"a": "1,2,3"}

                >>>combine_list(["A","B"], "test")
                {"test": "A,B"}

                >>>combine_list([{"a": 1, "b": 2}, {"a": 3, "b": 4}])
                {"a": [1,3], "b": [2,4]}

        Args:
            data: List data to combine
            key: Key to combine the data into

        Returns:
            Dict with combined data from the list

        """
        if not isinstance(data, ListType):
            raise Exception("Can't combine non-list!")
        if len(data) > 0 and isinstance(data[0], DictType):
            return combine_listdict(data)
        else:
            return {key: data}

    def flatten(self, data, prefix=None, shallow_flatten=None):
        """General flattening function
        Method to flatten a dict like or listdict

        Makes the keys lowercase, removes .'s and replaces spaces with underscores::

            a["b C.D"] = {"e": f} -> a["b_cd_e"] = f


        All values are basic types of string or integer
        Lists will be flattened into CSV strings
        Works recursively on list-dicts and inner dicts

        Args:
            data: List of dictionaries or dictionary to flatten
            prefix: Prefix to add to the data after flattening
            shallow_flatten: Should we ignore the first level of nesting, and only flatten each element within it?
            Used for lists of dictionaries

        Returns:
            Single level dictionary/List of single level dictionaries

        """
        if data is None:
            return None

        if self.prefix and prefix is None:  # prefix has priority over self.prefix
            prefix = self.prefix

        if shallow_flatten is None:  # Same with shallow flatten
            shallow_flatten = self.shallow_flatten

        if shallow_flatten:
            return [self.flatten(item, prefix=prefix, shallow_flatten=False) for item in data]

        # result = None
        is_basictype = False
        if isinstance(data, self._dict_types):
            # Dict types
            data = SortedDictPlus(data)
            result = self.flatten_dict(data, prefix)

            for k, v in result.iteritems():  # Convert BasicList back to regular list to complete flattening
                if isinstance(v, BasicList):
                    result[k] = v.v

        elif isinstance(data, self._list_types):
            # Complex list-like types
            listd = [self.flatten(item, prefix=prefix) for item in list(data)]
            result = combine_listdict(listd)

        elif isinstance(data, self._basic_types):
            result = data  # Basic types
            is_basictype = True
        elif type(data) in self._type_override:
            result = self._type_override[type(data)](data)
        else:
            raise Exception("Don't know how to flatten {}".format(data.__class__))  # Unknown type

        # Assumes that the dict has been flattened at least a bit, before attempting to stringify lists
        if self.stringify_lists and not is_basictype:
            if isinstance(result, DictType):  # if there is a list within the dict
                for k, v in result.items():
                    if isinstance(result[k], list):
                        stringify_list = True

                        if self.keep_simple_lists:
                            stringify_list = not is_simplelist(v)

                        if stringify_list:
                            result[k] = ",".join(unicode(vi) for vi in v)

            else:
                new_result = []
                basictype_list = True  # Is our list something like [1, 2] or ["a", "b"] not [{"a": 1}, "b"]
                for item in iter(result):
                    if not isinstance(item, self._basic_types):
                        basictype_list = False
                    if isinstance(item, list):
                        new_result.append(",".join(unicode(vi) for vi in item))
                    else:
                        new_result.append(item)

                if basictype_list:
                    if self.keep_simple_lists and not is_simplelist(result):
                        new_result = ",".join([str(el) for el in new_result])

                result = new_result

        return result

    def flatten_dict(self, data, prefix=None):
        """Internal single dict flattening function used recursively

        Args:
            data: data to flatten
            prefix: Key prefix

        Returns:
            Flattened dict

        """

        flat_dict = SortedDictPlus()

        for k, v in data.items():
            k = k.replace('.', '').replace(' ', '_')  # Reformat the key
            k = prefix + "_" + k if prefix else k

            if isinstance(v, DictType):  # Dict within dict
                sub_dict = self.flatten_dict(v, prefix=k)
                # Combine the flat_dict with the flattened sub_dict
                flat_dict.update(sub_dict)
                flat_dict = flatten_single_lists(flat_dict, self.remove_single_lists)

            elif isinstance(v, ListType):
                if self.keep_simple_lists and is_simplelist(v):  # If it's a basic list, it's a base case
                    flat_dict[k] = BasicList(v)
                else:
                    # Not a simple list, could still be a basic list after flattening elements
                    flat_els = []
                    for el in v:
                        flat_els.append(self.flatten(el, prefix=k, shallow_flatten=False))

                    if len(flat_els) > 0 and isinstance(flat_els[0], DictType):  # List of dicts
                        flat_dict.update(self.combine_list(flat_els, k))
                    else:
                        flat_dict[k] = BasicList(flat_els)  # Keep list

            else:  # Base case, unflattenable value
                if self.autoparse_dt_strs:
                    if isinstance(v, StringTypes):  # Attempt to parse string into datetime
                        v = self._try_parse_dt(v)
                    elif isinstance(v, (IntType, FloatType)):  # Attempt to parse int/float into a timestamp datetime
                        v = self._try_parse_dt(v, is_number=True)
                if type(v) in self._type_override:
                    flat_dict[k] = self._type_override[type(v)](v)
                else:
                    flat_dict[k] = v

        return flat_dict


def do_flatten(data, prefix=None, stringify_lists=True, shallow_flatten=False,
               keep_simple_lists=True, autoparse_dt_strs=False, special_dt_formats=None, oldest_dt_allowed=None,
               ignore_dt_formats=None, flatten_type_override=None, add_raw_json=True, remove_single_lists=True):
    """
    Simple alias for creating a flattener then running flatten() with options
    add_raw_json:  Add a raw_json key that contains the json dump of the raw data, Defaults to True
    """

    fl = Flattener(prefix=prefix, stringify_lists=stringify_lists, shallow_flatten=shallow_flatten,
                   keep_simple_lists=keep_simple_lists, autoparse_dt_strs=autoparse_dt_strs,
                   special_dt_formats=special_dt_formats, oldest_dt_allowed=oldest_dt_allowed,
                   ignore_dt_formats=ignore_dt_formats, flatten_type_override=flatten_type_override,
                   remove_single_lists=remove_single_lists)

    if add_raw_json:
        if shallow_flatten:
            for element in data:
                if "raw_json" in element:
                    if not isinstance(element['raw_json'], str):
                        element['raw_json'] = json.dumps(element['raw_json'])
                else:
                    element['raw_json'] = json.dumps(element)
        else:
            if "raw_json" in data:
                if not isinstance(data['raw_json'], str):
                    data['raw_json'] = json.dumps(data['raw_json'])
            else:
                data['raw_json'] = json.dumps(data)

    flattened = fl.flatten(data)

    if add_raw_json:
        if shallow_flatten:
            for element in flattened:
                if 'raw_json' in element:
                    element['raw_json'] = json.loads(element['raw_json'])
        else:
            if 'raw_json' in flattened:
                flattened['raw_json'] = json.loads(flattened['raw_json'])

    return flattened


def hoist_key(key, from_list):
    """Hoist out a specific key within a given listdict

    Examples:

        To hoist the key "a"::

            >>>hoist_key("a", [{"a": 1, "b": 4},{"a": 2}, ..])
            [1,2,3]

    Args:
        key: Key to grab from each dict within the list of dictionaries
        from_list: listdict to source from

    Returns:
        list of hoisted values

    """
    hoisted = []
    for element in from_list:
        if key not in element:
            raise Exception("Key {} not found in dict {}".format(key, element))
        hoisted.append(element[key])
    return hoisted


def hoist_keys(key_list, from_list):
    """Hoist out a specific keys within a given listdict

    Examples:

        To hoist out multiple keys::

            >>>hoist_keys(["a", "b"], [{"a": 1, "b": 4},{"a": 2, "b": 2, "c": 3}, ..])
            [[1,2],[4,2]]  #[[all a keys], [all b keys]]

    Args:
        key_list: List of keys to hoist from the list of dictionaries
        from_list: List of dictionaries that have the specified key in it

    Returns:
        List of the list of hoisted keys

    """
    hoisted = []
    for key in key_list:
        hoisted.append(hoist_key(key, from_list))
    return hoisted


def replace_dict_prefix(prefix, replace_val, from_dict):
    """Change a similar prefix on keys within a dict to something else, say ``annoying_stuff_ -> a_``

    Examples:

        Remove the annoying_stuff prefix::

            >>>{"annoying_stuff_important_stuff": "data", "annoying_stuff_asdf": "data2"}
            {"a_important_stuff": "data", "a_asdf": "data2"}

    Args:
        prefix: Prefix to replace
        replace_val: Prefix to replace with
        from_dict: Dictionary to replace prefix on

    Returns:
        Changed from_dict

    """
    for k in from_dict.keys():
        if k.startswith(prefix):
            newk = k.replace(prefix, replace_val, 1)
            if newk in from_dict:
                raise Exception("Can't remove prefix, results in namespace collision!")
            from_dict[newk] = from_dict.pop(k)
    return from_dict


def merge_dicts(d1, d2):
    """Merge dict d1 with dict d2. If they share keys, treat it as a listdict

    Args:
        d1: dict1
        d2: dict2

    Returns:
        Combined dict result
    """

    # First, we check if they share any keys (could be a listdict)
    shared_keys = set(d1.keys()).intersection(set(d2.keys()))
    if shared_keys:
        # They share keys, so we must combine them accordingly
        return combine_listdict([d1, d2], use_placeholder=False)
    else:
        # No shared keys, just merging dicts together
        d1.update(d2)
        return d1


def flatten_single_lists(data, remove_single_lists=True):
    """Flatten lists within a dict that only contain one element

    Examples:

        Flatten the data::

            >>>flatten_single_lists({"a": [1], "b": 2, "c":[3,4]})
            {"a": 1, "b": 2, "c": [3, 4]}

    Args:
        data: Dict data to flatten lists in

    Returns:
        More flattened data

    """
    if not isinstance(data, SortedDictPlus):
        data = SortedDictPlus(data)
    if remove_single_lists:
        for k, v in data.items():
            if isinstance(v, ListType):
                if len(v) == 1:  # Single entry list, can reduce to basic type
                    data[k] = v[0]
    return data


def is_simplelist(data):
    """Determine whether a list is a simple list. A simple list is a list of purely integers or purely strings
    Not to be confused with a basic list, which is a list of basic types
    Args:
        data: List to check

    Returns:
        True if it is a basic list, else False
    """
    if not len(data) > 0:
        return False  # Not a basic list because it's empty

    is_basic = True

    type_match = data[0]
    if not isinstance(type_match, int) and not isinstance(type_match, StringTypes):
        is_basic = False  # Type of data in list isnt int or str
    else:
        for datai in data:
            if not isinstance(datai, type(type_match)):
                is_basic = False

    return is_basic


def combine_listdict(data, use_placeholder=True):
    """Combine a listdict into a single dictionary, NOT flattening.
        If use_placeholder is True, then None will be inserted inbetween missing values in the list of dicts

    Examples:

        If you have data like so::

            [{"e": f_0, "g": h_0, ..}, {"e": f_1, "g": h_1, ..}]

        You will get a new dict c, like::

            c["e"] =  [f0, f1, ...]
            c["g"] =  [h0, h1, ...]

        If your data is incomplete, with use_placeholder=True, such as::

            [{"a": a_0, "b": b_0}, {"a": a_1}, {"a": a_2, "b": b_2}, ..]

        The resulting dict c will look like::

            c["a"] = [a_0, a_1, a_2]
            c["b"] = [b_0, None, b_2]

        Otherwise, with use_placeholder::

            c["a"] = [a_0, a_1, a_2]
            c["b"] = [b_0, b_2]


    Args:
        data: List of DictPlus's to combine into a single dictionary

    Returns:
        Combined dictionary
    """
    if not isinstance(data, ListType) or (len(data) > 0 and not isinstance(data[0], DictType)):
        return data  # Can't combine non-listdict, so return base list

    all_keys = set()  # Set of all keys within the entire listdict
    for el in data:
        for k, v in el.items():
            all_keys.add(k)

    result = SortedDictPlus()
    for el in data:
        # If an element of the list is not a dict, this isn't a true listdict and cannot be flattened
        if not isinstance(el, DictType):
            raise Exception("Cannot flatten nonpure listdict!")
        seen_keys = []

        def add_key_to_result(nk, nv, res):
            if nk in res:
                if isinstance(nv, ListType) or isinstance(nv, BasicList):
                    if isinstance(nv, BasicList):
                        nv = nv.v

                    existing_list = res[nk]
                    new_list = nv

                    """
                    Special case when:
                    {
                    "a_id": val,
                    "a": {
                        "id": val,
                        "other": [list val]
                    }
                    Collision of sub-listdict and and reformatted superkey lead to two keys being mapped to 'a_id'.
                    One option is to combine like [val1, val2] but can lead to [val, []] which isn't flattened
                    Other option is to extend like [val1].extend([val2]) but those "a_id" and "a": "id" might not be
                     related.

                    - Solution attempts to combine the lists before failing raising and exception


                    The "other": [] is required, since the flattening treats "a" like as a dict-list, therefore "id"
                    is turned into a list (until flattening of subdict "a" is complete) which causes this error

                    """
                    if len(existing_list) > 0:
                        if len(new_list) > 0:
                            # Both lists have content, if they're the same content type we can reasonably assume we can
                            # Combine them. Assuming that the list is homogeneous by first element

                            existing_list_basictyped = isinstance(existing_list[0], Flattener.BASIC_TYPES)
                            new_list_basictyped = isinstance(new_list[0], Flattener.BASIC_TYPES)
                            if not existing_list_basictyped or not new_list_basictyped:
                                # Lists are not simple enough to combine, must fail
                                raise Exception(
                                    "Lists contain nonbasic types, must manually simplify. Error on key '{}'".format(
                                        nk))

                            if type(existing_list[0]) == type(new_list[0]):
                                # Types match, and they're both basictyped, can combine
                                res[nk].extend(nv)
                            else:
                                raise Exception(
                                    "Lists contain incompatible types, must manually simplify. Error on key '{}'".format(
                                        nk))

                        else:
                            # Trying to add empty data, can just do nothing
                            return
                    else:  # Existing list is empty, can just extend value
                        res[nk].extend(nv)
                else:  # New value isn't a list
                    res[nk].append(nv)
            else:  # New key isn't in result
                if isinstance(nv, ListType):
                    res[nk] = nv
                elif isinstance(nv, BasicList):
                    res[nk] = nv.v
                else:
                    res[nk] = [nv]

        for k, v in el.items():
            seen_keys.append(k)
            add_key_to_result(k, v, result)

        # Add None to keys that didn't show up in this index of the listdict
        # So that [{a:1}, {b:4}, {a:2,b:5}] -> {a:[1,None,2],b:[None,4,5]}
        if use_placeholder:
            none_keys = list(all_keys.difference(seen_keys))
            for k in none_keys:
                add_key_to_result(k, None, result)

    return result


def clean_xmltodict_result(data, to_remove_list=None):
    """Helper method to clean the output of an xmltodict with messy '#' and '@' trailing

    Args:
        data: dict
        to_remove_list: list of strings to replace with underscores in the resulting dict

    Returns:
        Cleaned dictionary

    """
    keys_to_delete = []
    pairs_to_add = []

    for k, v in data.items():
        match = re.match(".*_([@#].*$)", k)  # Ends with _#text or _@property
        if match:
            # Remove the '#' or '@' ie  asdf_@property -> asdf_property
            pairs_to_add.append((k.replace(match.groups()[0], match.groups()[0][1:]), v))
            keys_to_delete.append(k)

    for k in keys_to_delete:
        data.pop(k)

    for k, v in pairs_to_add:
        if k in data:
            raise Exception("Cannot clean {}, results in namespace collision".format(k))
        data[k] = v

    data = SortedDictPlus(data)
    if not to_remove_list:
        to_remove_list = []

    to_remove_list.extend(["@", "-", ":", "#", "$", "%"])
    to_remove_list = list(set(to_remove_list))  # Make sure we don't have duplicates

    def new_kv(k, v):  # Replace all invalid characters with underscores
        for to_remove in to_remove_list:
            k = k.replace(to_remove, "_")
        return k, v

    data.map(new_kv)

    return data


def _place_key(dic, key_list, val):
    """
    turns flattened dictionary into a nested dictionary.

    """
    if len(key_list) == 1:
        dic[key_list[0]] = val
        return
    if key_list[0] not in dic:
        dic[key_list[0]] = {}
    _place_key(dic[key_list[0]], key_list[1:], val)
    return


def unflatten(flattened_dict, delimiter='_'):
    """turns flattened dictionary into a nested dictionary.
    For example:
        flattened dictionary: {"type_id": 2,"type_name":"Fake Name"}
        output: {"type":{"id":2,"name":"Fake Name"}}.
    """
    new_dict = {}
    for w, val in flattened_dict.items():
        keys = w.split(delimiter)
        _place_key(new_dict, keys, val)
    return new_dict


def extend_nested_lists(nest_list):
    """
    Return a flattened nested list, where the nested list looks like
    [
     [val1, val2,
     [val3, val4]
    ]  =>
    Into something like
    [val1, val2, val3, val4]

    Args:
        nest_list: nested list in format described above

    Returns: flattened list of values

    """
    ldata = []
    for inner_list in nest_list:
        for val in inner_list:
            ldata.append(val)

    return ldata
