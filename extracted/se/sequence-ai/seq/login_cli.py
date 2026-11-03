"""
`seq login` and `seq logout`: you sign in on this machine as you do on the console - by a
code you confirm there - and sign out again; and who `seq account` says you are.

In one sentence: `seq login` asks the platform for a sign-in (a code, and the console page to confirm it on), opens
that page in your browser, and asks every few seconds until you approve it there → the session you are given is kept
on this machine (sequence_ai/_core/login.py), never printed → every command with no key runs as you → `seq logout`
ends it here; `seq logout ID` ends another machine's, as `seq account` lists them.

WHY no flags: the one way that works everywhere - a laptop opens the page itself, a machine over SSH prints it to open
on any other - so there is nothing to choose.
"""
from __future__ import annotations

import os
import socket
import time
import webbrowser
from typing import Any, Callable
from urllib.parse import quote

import httpx

from sequence_ai._core import login as signin
from sequence_ai._core.transport import DEFAULT_BASE_URL, _version
from sequence_ai.errors import AuthError, NotFound, Unavailable
from seq._account import auth_headers, public_headers
from seq.deployments_cli import _call
from seq.errors import raise_for, unreachable

Echo = Callable[[str], Any] | None


def _say(echo: Echo, line: str) -> None:
    if echo is not None:
        echo(line)


def _base(base_url: str | None) -> str:
    return (base_url or os.environ.get("SEQUENCES_BASE_URL") or DEFAULT_BASE_URL).rstrip("/")


def _device() -> str:
    """This machine as the console's page names it: its host name."""
    return (socket.gethostname() or "a machine").strip()[:80] or "a machine"


def _post(base: str, path: str, body: dict, bearer: str | None = None) -> httpx.Response:
    from seq._http import RetryReads

    try:
        with httpx.Client(headers=auth_headers(bearer) if bearer else public_headers(), timeout=30,
                          transport=RetryReads()) as c:
            return c.post(f"{base}{path}", json=body)
    except httpx.TransportError as exc:
        raise unreachable(base, exc) from None


def _console_root(url: str) -> str | None:
    """The console's root, from the page a sign-in is confirmed on (`<root>device/?code=…`): where its Account and
    Billing pages are."""
    i = url.find("/device/") if isinstance(url, str) else -1
    return url[: i + 1] if i > 0 and url.startswith("https://") else None


def login(*, base_url: str | None = None, echo: Echo = print, open_page: Callable[[str], Any] | None = None,
          sleep: Callable[[float], Any] | None = None, profile: str | None = None) -> dict:
    """Sign in on this machine: the page to confirm the code on is opened (or printed), and the platform asked until
    you approve it there. Returns {email, login_id}; refused when the code is denied or lapses first. `profile` signs in
    under that name and makes it the active one; without it, the active profile."""
    open_page = open_page or webbrowser.open
    sleep = sleep or time.sleep
    base = _base(base_url)
    name = signin._named(profile) if profile else signin.profile()
    r = _post(base, "/v1/login", {"device": _device(), "client": f"seq {_version()}"[:40]})
    raise_for(r)
    started = r.json()
    url, code = started["verify_url"], started["user_code"]



    _say(echo, f"open {url} and confirm {code}")
    from seq._replay_player.cli import _remote

    if not _remote():
        try:
            if open_page(url):
                _say(echo, "(opened in your browser)")
        except Exception:
            pass
    deadline = time.monotonic() + float(started.get("expires_in") or 600)
    while time.monotonic() < deadline:
        sleep(float(started.get("interval") or 5))
        try:
            r = _post(base, "/v1/login/token", {"device_code": started["device_code"]})
        except Unavailable:
            continue
        if r.status_code == 202:
            continue
        raise_for(r)
        got = r.json()
        before = signin.saved(base, profile=name)
        root = _console_root(url)
        signin.save(base, {"access_token": got["access_token"], "refresh_token": got["refresh_token"],
                           "expires_at": got["expires_at"], "email": got.get("email"), "user_id": got.get("user_id"),
                           "login_id": got.get("login_id"), **({"console": root} if root else {})}, profile=name)
        if profile:
            signin.activate(name)
        if before and before.get("login_id") and before.get("login_id") != got.get("login_id"):



            old = str(before["login_id"])
            try:
                _call("DELETE", f"/v1/account/logins/{quote(old, safe='')}", base, person=True)
            except NotFound:
                pass
            except Exception:
                _say(echo, f"the sign-in this one replaces ({old[:8]}) could not be ended: "
                           f"seq logout {old[:8]} ends it")

        try:
            from seq.person_cli import account_person

            account_person(base_url=base, echo=None)
        except Exception:
            pass
        _say(echo, f"signed in as {got.get('email')}")
        return {"email": got.get("email"), "login_id": got.get("login_id")}
    from sequence_ai.errors import Gone

    raise Gone("the sign-in code lapsed before it was approved - run seq login again")


def _resolve(login_id: str, base: str) -> dict:
    """One of your sign-ins by its id or the first characters of it, as `seq account` shows them."""
    from sequence_ai.errors import InvalidRequest, NotFound

    mine = login_list(base_url=base, echo=None)
    hits = [x for x in mine if str(x.get("id", "")).startswith(login_id.strip())] if login_id.strip() else []
    if not hits:
        raise NotFound(f"no sign-in of yours starts with {login_id!r} - seq account lists them")
    if len(hits) > 1:
        raise InvalidRequest(f"{login_id!r} names {len(hits)} sign-ins - give more of its id")
    return hits[0]


def logout(login_id: str | None = None, *, base_url: str | None = None, echo: Echo = print,
           profile: str | None = None) -> dict:
    """Sign out: this machine's sign-in ended on the platform and removed here - or, given one of the ids `seq account`
    lists, that sign-in ended wherever it is. Signed out is said only when the platform ended it (or it had ended
    already); when the platform did not, or could not be reached, the sign-in is kept here to try again and the refusal
    says so (Unavailable). {cl6 SDK scan #1 10-29: "signed out" was said whatever the platform answered}"""
    base = _base(base_url)
    if login_id:
        hit = _resolve(login_id, base)
        _call("DELETE", f"/v1/account/logins/{quote(str(hit['id']), safe='')}", base, person=True)
        _say(echo, f"signed out {hit.get('device')}")
        if (signin.saved(base) or {}).get("login_id") == hit["id"]:
            signin.drop(base)
        return {"signed_out": hit.get("device"), "login_id": hit["id"]}
    name = signin._named(profile) if profile else signin.profile()
    entry = signin.saved(base, profile=name)
    if entry is None:
        _say(echo, "not signed in on this machine" + (f" in profile {name}" if profile else ""))
        return {"signed_out": None}
    who = entry.get("email") or "this machine's sign-in"
    retry = ("it stays signed in here to try again: seq logout once more, or Sign out on the console's Account page "
             "(seq account names this machine's)")
    try:
        token = signin.Login(base, name).token()
    except AuthError:
        token = None
    already = token is None
    if token is not None:
        try:
            r = _post(base, "/v1/logout", {}, bearer=token)
        except Exception as exc:
            raise Unavailable(f"the platform could not be reached to end {who}; {retry}") from exc
        try:
            said = (r.json() or {}).get("signed_out") if r.status_code < 300 else None
        except ValueError:
            said = None
        if r.status_code == 401:
            already = True
        elif r.status_code >= 300 or said is False:
            raise Unavailable(f"the platform did not end {who} (answered {r.status_code}); {retry}")
    signin.drop(base, profile=name)
    _say(echo, f"signed out {entry.get('email') or ''}".rstrip()
         + (" (its sign-in had ended already)" if already else ""))
    return {"signed_out": entry.get("email"), "login_id": entry.get("login_id")}


def login_list(*, base_url: str | None = None, echo: Echo = None) -> list[dict]:
    """Your seq sign-ins in force, newest first: each one's id, machine, address, when it signed in and was last used,
    and `this` for this machine's. Needs you signed in."""
    return list((_call("GET", "/v1/account/logins", _base(base_url), person=True) or {}).get("logins") or [])


def login_revoke(login_id: str, *, base_url: str | None = None, echo: Echo = None) -> dict:
    """One of your seq sign-ins ended, by its id (or its first characters): another machine's, or a lost one's."""
    return logout(login_id, base_url=base_url, echo=echo)


def you(*, base_url: str | None = None, echo: Echo = print) -> dict | None:
    """Who this machine is signed in as, and your seq sign-ins - the lines `seq account` heads with; None when only a
    key is in use."""
    from seq import clock

    base = _base(base_url)
    entry = signin.saved(base)
    if entry is None:
        return None
    _say(echo, f"you       {entry.get('email')} - signed in with seq on this machine")
    try:
        logins = login_list(base_url=base)
    except Exception:
        logins = []
    for x in logins:
        _say(echo, f"  {str(x.get('id', ''))[:8]}  {x.get('device')}  signed in {clock.stamp(x.get('signed_in_at'))}"
                   f" · last used {clock.stamp(x.get('last_used_at'))}" + ("  (this machine)" if x.get("this") else ""))
    return {"email": entry.get("email"), "logins": logins}


def account(*, base_url: str | None = None, echo: Echo = print) -> dict:
    """`seq account`: who you are when signed in (you), then the account's own lines (capacity_cli.account). With a key
    in $SEQUENCES_API_KEY the lines are that key's account - a key wins over the sign-in (_account.credential) - so your
    sign-in is said in one line after them, not as their head: a CI key's account is never shown under your name.
    {cl6 SDK scan #10 10-29: with both, the key's account was headed with the sign-in's "you" and its sign-ins}"""
    from seq import capacity_cli

    if os.environ.get("SEQUENCES_API_KEY"):
        out = capacity_cli.account(base_url=base_url, echo=echo)
        entry = signin.saved(_base(base_url))
        if entry is not None:
            _say(echo, f"(the account of the key in $SEQUENCES_API_KEY; signed in with seq as {entry.get('email')}, "
                       "unset it to see yours)")
        return out if isinstance(out, dict) else {"account": out}
    who = you(base_url=base_url, echo=echo)
    out = capacity_cli.account(base_url=base_url, echo=echo)
    return {**(out if isinstance(out, dict) else {"account": out}), **({"you": who} if who else {})}


def profile_list(*, base_url: str | None = None, echo: Echo = print) -> list[dict]:
    """`seq profile list`: each profile, who is signed in under it at which platform address, the active one marked."""
    active, out = signin.profile(), []
    for name, logins in signin.profiles():
        mark = "*" if name == active else " "
        kept = {a: e for a, e in logins.items() if isinstance(e, dict) and e.get("refresh_token")}
        for address, entry in sorted(kept.items()):
            _say(echo, f"{mark} {name:<8} {entry.get('email') or 'signed in'} at {address}")
            out.append({"profile": name, "active": name == active, "address": address, "email": entry.get("email")})
        if not kept:
            _say(echo, f"{mark} {name:<8} signed in nowhere")
            out.append({"profile": name, "active": name == active, "address": None, "email": None})
    return out


def profile_activate(name: str, *, base_url: str | None = None, echo: Echo = print) -> dict:
    """`seq profile activate NAME`: the profile every later seq on this machine signs in as; SEQUENCES_PROFILE still
    wins for a process that sets it."""
    signin.activate(name)
    _say(echo, f"profile {name} is active: seq signs in as it"
         + ("" if signin.saved(_base(base_url), profile=name) else " - seq login signs you in under it"))
    return {"active": name}


def profile_current(*, base_url: str | None = None, echo: Echo = print) -> dict:
    """`seq profile current`: the profile seq signs in as now."""
    name = signin.profile()
    _say(echo, name)
    return {"profile": name}
