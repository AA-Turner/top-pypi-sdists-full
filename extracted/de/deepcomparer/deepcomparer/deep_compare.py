from typing import Any, Iterable


def deep_compare(
        obj1: Any,
        obj2: Any,
        ignore_order=False,
) -> bool:
    res = _rec_helper(obj1, obj2, ignore_order)
    return res


def _rec_helper(
        obj1: Any,
        obj2: Any,
        ignore_order: bool,
) -> bool:
    if type(obj1) != type(obj2):
        return False

    if type(obj1) in [str, int, float]:
        return obj1 == obj2

    if isinstance(obj1, dict):
        for key in obj1.keys():
            if key not in obj2:
                return False
            if not _rec_helper(obj1[key], obj2[key], ignore_order):
                return False
        return True

    if isinstance(obj1, Iterable):
        obj1 = list(obj1)
        obj2 = list(obj2)
        if len(obj1) != len(obj2):
            return False
        if len(obj1) == 0:
            return True

    if isinstance(obj1, list) and not ignore_order:
        return _rec_same_order_list_helper(ignore_order, obj1, obj2)

    if isinstance(obj1, list) and ignore_order:
        return _rec_list_helper(ignore_order, obj1, obj2)

    if hasattr(obj1, '__dict__'):
        return _rec_helper(vars(obj1), vars(obj2), ignore_order)

    return obj1 == obj2


def _rec_same_order_list_helper(ignore_order, obj1, obj2):
    for sub_obj1, sub_obj2 in zip(obj1, obj2):
        if not _rec_helper(sub_obj1, sub_obj2, ignore_order):
            return False
    return True


def _rec_list_helper(ignore_order, obj1, obj2):
    obj1 = list(obj1)
    obj2 = list(obj2)
    equal_indexes = (None, None)
    for index1 in range(len(obj1)):
        sub_obj_1 = obj1[index1]
        for index2 in range(len(obj2)):
            sub_obj_2 = obj2[index2]
            if _rec_helper(sub_obj_1, sub_obj_2, ignore_order):
                equal_indexes = (index1, index2)
                break
        if equal_indexes != (None, None):
            break
    if equal_indexes == (None, None):
        return False
    index1, index2 = equal_indexes
    obj1.pop(index1)
    obj2.pop(index2)
    return _rec_helper(obj1, obj2, ignore_order)
