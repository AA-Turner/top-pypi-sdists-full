"""This module provides a function to create a function dynamically.

Copied from `dataclasses._create_fn` in Python 3.10.13.
"""

from dataclasses import MISSING


def create_fn(name, args, body, *, globals=None, locals=None, return_type=MISSING):
    # Note that we may mutate locals. Callers beware!
    # The only callers are internal to this module, so no
    # worries about external callers.
    if locals is None:
        locals = {}
    return_annotation = ""
    if return_type is not MISSING:
        locals["_return_type"] = return_type
        return_annotation = "->_return_type"
    args = ",".join(args)
    body = "\n".join(f"        {b}" for b in body)

    # Compute the text of the entire function.
    txt = f"    def {name}({args}){return_annotation}:\n{body}"

    local_vars = ", ".join(locals.keys())
    txt = f"def __create_fn__({local_vars}):\n{txt}\n    return {name}"
    ns = {}
    exec(txt, globals, ns)
    return ns["__create_fn__"](**locals)
