"""
`seq account set | delete` and seq.account_person / account_set / account_delete: the console's Account page from the
command line - who you are; your name, time zone and clock; your email; your photo; your storage limit; and the
account's deletion. Each
needs you signed in (`seq login`): a key cannot change the account.


In one sentence: each function asks the platform as you (deployments_cli._call with person=True) to change what the
Account page changes - the same row, so the console reads what the CLI set - and returns you as the platform then has
you; nothing is printed unless asked (`echo`).

    seq.account_set(time_zone="Asia/Tokyo", clock=12)      # the CLI's times then follow them (seq/clock.py)
"""
from __future__ import annotations

import pathlib
from typing import Any, Callable

from seq.deployments_cli import _call

Echo = Callable[[str], Any] | None
_UNSET: Any = object()

PHOTO_TYPES = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp"}


def _say(echo: Echo, line: str) -> None:
    if echo is not None:
        echo(line)


def show_person(me: dict, echo: Echo) -> None:
    """You, in the lines `seq account` says you in: your account's id, your email, your name, your time zone and clock -
    this machine's and 24-hour where never chosen."""
    _say(echo, f"account   {me.get('account_id') or '—'}")
    _say(echo, f"email     {me.get('email') or '—'}")
    _say(echo, f"name      {me.get('name') or '—'}" + ("  (photo set)" if me.get("photo") else ""))
    zone = me.get("time_zone") or "this machine's"
    clk = f"{me['clock']}-hour" if me.get("clock") in (12, 24) else "24-hour (never chosen)"
    _say(echo, f"times     {zone}, {clk}")


def account_person(*, base_url: str | None = None, echo: Echo = None) -> dict:
    """You, as the Account page shows you: {account_id, email, name, time_zone, clock, photo}. Your time zone and clock
    are kept with this machine's sign-in as they are read (remember), so every command after prints its times on them."""
    me = _call("GET", "/v1/account/person", base_url, person=True) or {}
    remember(me, base_url=base_url)
    show_person(me, echo)
    return me


def remember(me: dict, *, base_url: str | None = None) -> None:
    """Your time zone and clock (`me` as /v1/account/person says you) kept beside this machine's sign-in, and the times
    printed from now on put on them (seq/clock.py) - read by `seq login`, `seq account` and `seq account set`, and at the
    start of every command after (cli._your_clock). A key cannot read them: without a sign-in the times are this
    machine's.
"""
    from sequence_ai._core import login as signin

    from seq import clock
    from seq.login_cli import _base

    prefs = {"time_zone": me.get("time_zone") or None, "clock": me.get("clock") if me.get("clock") in (12, 24) else None}
    signin.keep(_base(base_url), prefs=prefs)
    clock.use(**prefs)


def account_set(*, name: Any = _UNSET, email: Any = _UNSET, photo: Any = _UNSET, time_zone: Any = _UNSET,
                clock: Any = _UNSET, storage_limit: Any = _UNSET, base_url: str | None = None,
                echo: Echo = None) -> dict:
    """Change what the Account page changes, only what is named: `name`; `time_zone` ("Asia/Tokyo", or "local" / None
    for this machine's); `clock` (12 or 24, or None: never chosen - 24-hour); `email` (a link goes to the old address
    and one to the new, and the change is made once both are opened); `photo` (a PNG, JPEG or WebP file of 2 MB at
    most, made 256 x 256 as the console makes it, or None to remove it); `storage_limit` (everything the account stores
    counts toward it: a number of GB, or a size such as "500GB" or "2TB", with no ceiling of the platform's - storage is
    billed by the GB - or "plan" / None for the plan's own; in force at once). Returns you as the platform then has
    you."""
    from sequence_ai.errors import InvalidRequest

    from seq import storage_note



    if all(v is _UNSET for v in (name, email, photo, time_zone, clock, storage_limit)):
        raise InvalidRequest("nothing to change: --name, --email, --photo, --time-zone, --clock or --storage-limit")
    try:
        limit = storage_note.parse_size(storage_limit) if storage_limit is not _UNSET else _UNSET
    except ValueError as exc:
        raise InvalidRequest(str(exc)) from None
    removed = photo is not _UNSET and (photo is None or str(photo).lower() == "none")
    upload = _photo(photo) if photo is not _UNSET and not removed else None
    profile = {k: v for k, v in (("name", name), ("time_zone", time_zone), ("clock", clock)) if v is not _UNSET}
    if profile:
        if profile.get("time_zone") == "local":
            profile["time_zone"] = None
        _call("PATCH", "/v1/account/profile", base_url, profile, person=True)
    if email is not _UNSET:
        out = _call("POST", "/v1/account/email", base_url, {"email": email}, person=True) or {}
        _say(echo, f"a link went to your old address and one to {out.get('email') or email}: the change is made once "
                   "both are opened")
    if removed:
        _call("DELETE", "/v1/account/photo", base_url, person=True)
        _say(echo, "photo removed")
    elif upload is not None:
        _call("PUT", "/v1/account/photo", base_url, person=True, upload=upload)
        _say(echo, "photo set")
    if limit is not _UNSET:
        st = _call("PUT", "/v1/account/storage-limit", base_url, {"limit_bytes": limit}, person=True) or {}
        _say(echo, storage_line(st))
        said = storage_note.note(st)
        if said:
            _say(echo, said)
    return account_person(base_url=base_url, echo=echo)


def _photo(photo: Any) -> tuple[bytes, str]:
    """A photo file's bytes and type; InvalidRequest for one that is not a PNG, JPEG or WebP file on this machine."""
    from sequence_ai.errors import InvalidRequest

    path = pathlib.Path(photo).expanduser()
    kind = PHOTO_TYPES.get(path.suffix.lower())
    if kind is None:
        raise InvalidRequest(f"{path.name}: a photo is a .png, .jpg or .webp file")
    if not path.is_file():
        raise InvalidRequest(f"{path}: no such file")
    return path.read_bytes(), kind


def storage_line(st: dict) -> str:
    """The storage limit as it now is, and whose: "storage limit 500.00 GB, your own limit (your plan's: 100.00 GB) ·
    85.00 GB stored"."""
    from seq import deps_cost, storage_note

    return (f"storage limit {deps_cost.size(st.get('limit_bytes'))}, {storage_note.whose(st)} · "
            f"{deps_cost.size(st.get('used_bytes'))} stored")


def account_delete(*, base_url: str | None = None, echo: Echo = None, opener: Any = None) -> dict:
    """Delete the account - on the console's Account page, where you confirm it: the page said and opened in your
    browser, and nothing deleted from here. Before: `seq account delete --confirm ID` deleted it from the terminal.
    
"""
    from seq.billing_cli import _open
    from seq.login_cli import _base
    from sequence_ai._core import login as signin
    from sequence_ai.errors import InvalidRequest

    root = signin.console(_base(base_url))
    if root is None:
        raise InvalidRequest("this platform's console is not known on this machine: sign in (seq login), then run "
                             "seq account delete again")
    _say(echo, "the account is deleted on the console's Account page, where you confirm it:")
    _open(root + "account/", echo, opener)
    return {"url": root + "account/"}