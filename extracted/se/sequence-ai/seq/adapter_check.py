"""
`seq adapter check <adapter>`: an adapter checked here, without an eval, a GPU or a connection
.

In one sentence: the class is imported as an eval's benchmark machine imports it - a local file, or a registered
version's (name[@vN]) - so @seq.adapter holds it to what an adapter is → its two methods are reported, the one that turns
the env's observation into the policy's input and the one that turns the policy's answer into the env's actions → its
pairs and the parameters its __init__ declares beside them. An adapter missing a method fails at the import; one that
declares no pairs fails here, as `seq deploy` would refuse it.
WHY nothing more is run: an adapter is two functions of your own, run by an eval as they are - there is no transform
pipeline left to walk step by step.
"""
from __future__ import annotations

import re
from typing import Any, Callable

from sequence_ai._core.names import segment



_REF = re.compile(r"[A-Za-z][A-Za-z0-9._-]{0,63}(?:@v[1-9][0-9]*)?")


def is_registered(target: str) -> bool:
    """name or name@vN (a registered adapter), as opposed to a file, file.py:Class or pkg.module[:Class] here: a name
    with a version or a hyphen is registered (no module has one); a bare word is a module only when one is found."""
    import importlib.util
    import os

    from seq.adapter_cli import is_file_ref

    if is_file_ref(target) or ":" in target or not _REF.fullmatch(target):
        return False
    if "@v" in target or "-" in target:
        return True
    try:
        return importlib.util.find_spec(target) is None and not os.path.exists(target + ".py")
    except (ImportError, ValueError):
        return True


def load_registered(ref: str, *, base_url: str | None = None) -> type:
    """A registered version's file (name@vN, or name for its latest), imported as an eval's benchmark machine imports
    it, so @seq.adapter holds it to what an adapter is here too."""
    import importlib.util
    import os
    import sys
    import tempfile

    from seq.adapter_cli import _client
    from sequence_ai.errors import InvalidRequest

    name, _, ver = ref.partition("@v")
    got = _client(None, base_url)._request("GET", f"/v1/adapters/{segment(name)}/source",
                                           params={"version": int(ver)} if ver else {})
    module = f"seq_adapter_{re.sub(r'[^0-9A-Za-z_]', '_', got['name'])}_v{int(got['version'])}"
    path = os.path.join(tempfile.mkdtemp(prefix="seq-adapter-"), module + ".py")
    with open(path, "w", encoding="utf-8") as f:
        f.write(got["source"])
    spec = importlib.util.spec_from_file_location(module, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[module] = mod
    spec.loader.exec_module(mod)
    cls = getattr(mod, got["class_name"], None)
    if cls is None:
        raise InvalidRequest(f"{ref}: its file defines no class {got['class_name']!r}")
    return cls



def run(cls: type, *, echo: Callable[[str], None] = print) -> dict:
    """`seq adapter check`: the adapter's name, its two methods, its pairs and its parameters, printed. Raises
    InvalidRequest when it declares no pairs - no version registers without them, as no eval runs one
; returns what it read otherwise. Nothing is sent."""
    from seq.adapter_cli import NO_PAIRS, _print_body, registration_body
    from sequence_ai.errors import InvalidRequest

    full = registration_body(cls, require_pairs=False)
    body = {k: v for k, v in full.items() if k not in ("source", "override")}
    _print_body(body, cls, echo=echo)
    params: dict[str, Any] = body.get("params") or {}
    if params:
        echo("params      " + ", ".join(f"{k}: {p.get('type')} = {p.get('default')!r}" for k, p in params.items())
             + "  (an eval may set these: --param adapter.NAME=VALUE)")
    if full.get("pairs") is None:
        raise InvalidRequest(f"it declares no pairs: {NO_PAIRS}", details={"problems": [f"no pairs: {NO_PAIRS}"]})
    echo("ok: both methods are marked and take what they are handed; nothing was sent (`seq deploy` registers it)")
    return {"adapter": body}
