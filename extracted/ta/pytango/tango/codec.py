# SPDX-FileCopyrightText: All Contributors to the PyTango project
# SPDX-License-Identifier: LGPL-3.0-or-later

try:
    from warnings import deprecated
except ImportError:
    from typing_extensions import deprecated

__all__ = ("dumps", "loads")


@deprecated("loads function was an experimental API - scheduled for removal in PyTango 11.0.0")
def loads(fmt, data):
    if fmt.startswith("pickle"):
        import pickle

        loads = pickle.loads
    elif fmt.startswith("json"):
        import json

        loads = json.loads
    else:
        raise TypeError(f"Format '{fmt}' not supported")
    return loads(data)


@deprecated("dumps function was an experimental API - scheduled for removal in PyTango 11.0.0")
def dumps(fmt, obj):
    if fmt.startswith("pickle"):
        import pickle

        ret = fmt, pickle.dumps(obj, protocol=pickle.HIGHEST_PROTOCOL)
        return ret
    elif fmt.startswith("json"):
        import json

        return fmt, json.dumps(obj)
    raise TypeError(f"Format '{fmt}' not supported")
