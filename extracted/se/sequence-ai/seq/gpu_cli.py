"""
`seq gpu`: GPU machines you run yourself — `add` opens them near a place in the US, `places` lists the
US cities a place can be, `list` shows those live and `history` those over, `allow` changes who reaches
their ports, `ssh` opens a root shell on one, `save` keeps one's disk as a snapshot (`saved` lists them),
`remove` shuts one down. A machine is a container you are root in, with its cards - 1, 2, 4 or 8 of one kind; you
install and run what you like, and `remove` ends the machine and its disk. (`seq gpus`, plural, is a different command:
the catalogue of cards and their prices.)

In one sentence: each command reads or writes gateway routes with the caller's key through `sequence_ai.gpu.*` and prints
what they did - `add` waits until its machines run, and Ctrl-C meanwhile cancels those not running; `ssh` adds your
`~/.ssh` public key to the machine (making one if you have none), asks the gateway for where to reach it, and hands off to
the system `ssh`.
"""
from __future__ import annotations

import os
import signal
import subprocess
import sys
import tempfile
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Callable, Iterator

from sequence_ai._core.money import money, per_hour
from sequence_ai._core.names import segment
from sequence_ai.errors import Unavailable

from seq.clock import stamp
from seq.deployments_cli import _call
from seq.errors import GpuCancelled, GpuNotCancelled

Echo = Callable[..., None]
EVERYWHERE = "0.0.0.0/0"
OPEN_TO_ALL = "its ports are open to every address (0.0.0.0/0): authenticate in your server"
WAIT_SAID_S = 60.0
STOPPING = ("stopping: the platform is adding it now - what it adds is removed as soon as it answers, in a few seconds "
            "(Ctrl-C again leaves what it adds as it is)")


def _silent(*_args: Any, **_kwargs: Any) -> None:
    """The `echo` of a `seq --json` call: it returns what it read and prints nothing."""


def _usd(v: Any, fmt: Callable[[Any], str] = money) -> str:
    """An amount or a price-an-hour as sequence_ai/_core/money.py writes it; '—' where the platform did not say it."""
    return fmt(v) if isinstance(v, (int, float)) and not isinstance(v, bool) else "—"


def _note(text: str) -> None:
    """A line for whoever runs the command, on stderr: what it prints on stdout stays its answer, `--json`'s too."""
    print(text, file=sys.stderr, flush=True)


def _ms(v: Any) -> str:
    """A round trip in milliseconds as it is said: whole from 1 ms ("expected 9 ms"), a tenth below; '—' for none.
"""
    if not isinstance(v, (int, float)) or isinstance(v, bool):
        return "—"
    return f"{v:.0f} ms" if v >= 1 else f"{v:.1f} ms"


def _status(m: dict) -> str:
    """Its status, and "run failing" for one whose command exited within 10 s five times running and is not started again."""
    return "run failing" if m.get("run") == "failing" else str(m.get("status") or "—")


@contextmanager
def _held(said: str) -> Iterator[Callable[[], bool]]:
    """A first Ctrl-C held while an add is asked: the platform adds the GPUs all the same once it has the request, and a
    command stopped then never hears their ids - they would start, and be billed once they run, after it said
    "cancelled". Held, it is said (`said`) and the add's answer awaited, so what it added can be removed; a second goes
    through. Where no handler can be set (not the main thread), a Ctrl-C goes through as ever. The handler before is set
    back.
"""
    pressed: list = []

    def hold(_signum: int, _frame: Any) -> None:
        if pressed:
            raise KeyboardInterrupt
        pressed.append(True)
        _note(said)

    try:
        before = signal.signal(signal.SIGINT, hold)
    except ValueError:
        yield lambda: False
        return
    try:
        yield lambda: bool(pressed)
    finally:
        signal.signal(signal.SIGINT, before if before is not None else signal.default_int_handler)



def _expected_ms(m: dict) -> Any:
    e = m.get("expected_rtt")
    return e.get("ms") if isinstance(e, dict) else None


def _cards(m: dict) -> int:
    """How many cards a GPU machine has: its `cards`, which the platform gives each; 1 for one it does not say
    it of."""
    n = m.get("cards")
    return n if isinstance(n, int) and not isinstance(n, bool) and n > 0 else 1


def _card(m: dict) -> str:
    """A GPU machine's cards as said in a table or a line: its card's name, and how many where it has more than one -
    "L4", "L4 × 4"."""
    name = str(m.get("gpu") or "—")
    return f"{name} × {_cards(m)}" if _cards(m) > 1 else name


def _price(m: dict, cards: dict) -> str:
    """What a GPU costs an hour, as its owner reads it: its card's own price, as the price list says it (`cards`,
    sequence_ai.gpu._card_prices), times its cards where it has more than one, and its CPU and memory on top - never the
    one total the platform bills it at, which read as the card's (an L4's "$1.22/h", where the card is $0.80). A card
    costs the same alone or among eight. '—' where the price list could not be read.


"""
    card = cards.get(str(m.get("gpu")))
    if card is None:
        return "—"
    each = f"{per_hour(card)} + CPU and memory"
    return f"{_cards(m)} × {each}" if _cards(m) > 1 else each


def _line(m: dict, cards: dict | None = None) -> str:
    """One GPU on a line, as `seq gpu add` says it: id, its cards (_card: "L4 × 4" for a machine of four), the place asked
    for, status, its address, its ports, the round trip expected from near its place (`expected_rtt`, measured there) and
    what it costs an hour (_price, by `cards`).

"""
    bits = [str(m.get("id")), _card(m), str(m.get("place") or "—"), _status(m)]
    if m.get("host"):
        bits.append(str(m["host"]))
    if m.get("address"):
        bits.append(str(m["address"]))
    if m.get("address6"):
        bits.append(str(m["address6"]))
    if m.get("ports"):
        bits.append("ports " + ",".join(str(p) for p in m["ports"]))
    if isinstance(_expected_ms(m), (int, float)) and not isinstance(_expected_ms(m), bool):
        bits.append(f"expected {_ms(_expected_ms(m))}")
    bits.append(_price(m, cards or {}))
    return "  ".join(bits)


def _unmeasured(m: dict) -> str | None:
    """Where nothing was measured near its place, said so (`expected_rtt` with no "ms"); None where something was, or the
    platform could not say.
"""
    e = m.get("expected_rtt")
    if not isinstance(e, dict) or _expected_ms(m) is not None:
        return None
    return f"no round trip is known yet near {m.get('place') or 'the place asked'}"


def gpu_add(place: str, gpu: str, count: int = 1, snapshot: str | None = None, ports: list | None = None,
            allow: list | None = None, run: str | None = None, name: str | None = None, wait: bool = True, *,
            base_url: str | None = None, echo: Echo = _silent) -> list:
    """`seq gpu add --place … --gpu … [--count N] [--from NAME] [--port P]... [--allow CIDR]... [--run CMD] [--name NAME]
    [--no-wait]`:
    open a machine of `count` cards near `place` - 1, 2, 4 or 8, any other count the platform's refusal, said as it
    words it, exit 2 - and, unless `--no-wait`, wait until it runs - saying so on stderr each minute - then say it on a
    line with its cards (_line), and that nothing was measured near its place where nothing was. One that failed to start
    ends the command in its error; Ctrl-C cancels it if it does not run yet, says so and what it was billed
    (GpuCancelled), and exits 130, one that ran by then said - one while the add is asked is held until the platform
    answers, then what it added is cancelled so (_held); a second then stops it, said not cancelled (GpuNotCancelled).
    Returns what it said, as sequence_ai.gpu.add answers it, a list of one.


"""
    import sequence_ai

    machines: list = []
    cards: dict = {}
    try:
        with _held(STOPPING) as pressed:
            machines = sequence_ai.gpu.add(place, gpu, count, snapshot=snapshot, ports=ports, allow=allow, run=run,
                                           name=name, wait=False, base_url=base_url)
        if pressed():
            raise KeyboardInterrupt
        cards = sequence_ai.gpu._card_prices(base_url=base_url)
        if allow and EVERYWHERE in allow:
            _note(OPEN_TO_ALL)
        if wait and machines:
            ids = [str(m.get("id")) for m in machines]
            _note(f"{', '.join(ids)} starting: waiting until it runs (--no-wait returns once it is asked for: seconds, "
                  "not the minute or two it takes to run)")
            said = [0.0]

            def waiting(seconds: float, starting: list) -> None:
                if seconds - said[0] >= WAIT_SAID_S:
                    said[0] = seconds
                    _note(f"still starting after {seconds / 60:.0f} min: {', '.join(starting)}")

            machines = sequence_ai.gpu._running(machines, said=waiting, base_url=base_url)
    except KeyboardInterrupt as stop:
        if not hasattr(stop, "cancelled"):
            if not machines:
                raise GpuNotCancelled() from None
            stop = sequence_ai.gpu._stopped(machines, stop, base_url=base_url)
        for m in getattr(stop, "running", None) or []:
            echo(_line(m, cards))
        raise GpuCancelled(getattr(stop, "cancelled", None) or [], getattr(stop, "not_cancelled", None) or [],
                           getattr(stop, "billed", None) or {}) from None
    for m in machines:
        echo(_line(m, cards))
    unmeasured = _unmeasured(machines[0]) if machines else None
    if unmeasured:
        echo(unmeasured)
    return machines



def gpu_allow(gpu_id: str, ranges: list, *, base_url: str | None = None, echo: Echo = _silent) -> dict:
    """`seq gpu allow <id> CIDR...`: who reaches the GPU's ports from now on, in place of those it had - said once the GPU
    confirmed it, or that it had not yet.
"""
    import sequence_ai

    out = sequence_ai.gpu.allow(gpu_id, ranges, base_url=base_url)
    if EVERYWHERE in ranges:
        _note(OPEN_TO_ALL)
    said = ", ".join(str(a) for a in (out.get("allow") or ranges))
    if out.get("applied"):
        echo(f"{gpu_id}: its ports are open to {said} alone")
    else:
        echo(f"{gpu_id}: its ports are to be open to {said} alone - the GPU has not confirmed it yet (one starting "
             "takes them as it starts); run this again to be sure")
    return out



def gpu_follow_token(gpu_id: str, robot: str, *, revoke: bool = False, base_url: str | None = None,
                     echo: Echo = _silent) -> dict:
    """`seq gpu follow-token <id> --robot NAME [--revoke]`: one of your robots made a follow token - printed once, for the robot
    alone -, with which it lets its own address into this GPU's allow list as its network changes it; `--revoke`, it
    follows no more."""
    import sequence_ai

    if revoke:
        out = sequence_ai.gpu.follow_revoke(gpu_id, robot, base_url=base_url)
        echo(f"{gpu_id}: robot {robot} follows it no more - its follow token works no more"
             + (", and where it was let in from is taken away" if out.get("applied") else
                "; the GPU has not confirmed its address is taken away yet (one starting takes it as it starts)"))
        return out
    out = sequence_ai.gpu.follow_token(gpu_id, robot, base_url=base_url)
    if "applied" in out:
        echo(f"{gpu_id}: robot {robot}'s earlier follow token works no more"
             + (", and where it let the robot in from is taken away" if out["applied"] else
                "; the GPU has not confirmed its address is taken away yet"))
    echo(f"{gpu_id}: robot {robot}'s follow token - shown once; keep it on the robot alone:")
    echo(str(out.get("token")))
    echo(f"On the robot, as it starts and whenever it cannot reach the GPU: {sequence_ai.gpu.FOLLOW_ENV}=<token> seq gpu "
         "follow, or sequence_ai.gpu.follow(token). It lets in the robot's own address alone, in place of where it was "
         "let in from before.")
    return out


def gpu_follow(*, token: str | None = None, address: str | None = None, line: str | None = None,
               base_url: str | None = None, echo: Echo = _silent) -> dict:
    """`seq gpu follow [--token T] [--address ADDRESS] [--line INTERFACE]`, on a robot: its own address - by `line`
    alone, given one - let into the allow list of the GPU its follow token is for (sequence_ai.gpu.follow), said with
    where it reaches the GPU; over IPv4, the shared address's note (sequence_ai.gpu.FOLLOW_CGNAT) on stderr, as a line
    of ours and not a Python warning."""
    import warnings

    import sequence_ai

    with warnings.catch_warnings(record=True):
        warnings.simplefilter("always")
        out = sequence_ai.gpu.follow(token, to=address, base_url=base_url, **({"line": line} if line else {}))
    where = " ".join(str(a) for a in (out.get("host") or out.get("address"), out.get("address6")) if a)
    ports = ",".join(str(p) for p in out.get("ports") or [])
    by = f" by {out['line']}" if out.get("line") else ""
    said = f"{out.get('id')}: robot {out.get('robot')} is let in{by} from {out.get('range')}"
    if out.get("applied"):
        echo(said + (f" - reach it at {where}" if where else "") + (f", ports {ports}" if ports else ""))
    else:
        echo(said + " - the GPU has not confirmed it yet (one starting takes it as it starts); run this again to be sure")
    if ":" not in str(out.get("range") or ""):
        _note(sequence_ai.gpu.FOLLOW_CGNAT)
    return out



def gpu_places(text: str = "", limit: int = 8, *, base_url: str | None = None, echo: Echo = _silent) -> list:
    """`seq gpu places [words]`: the US cities whose name or another name they go by starts with the words, those of
    their own name first, the largest first, one a line - its name, state and country, then its latitude and longitude,
    either of which `seq gpu add --place` takes, and "(as <that other name>)" for a city found by one ("big apple": New
    York City, as Big Apple). Returns the list sequence_ai.gpu.places read.
    
"""
    import sequence_ai

    cities = sequence_ai.gpu.places(text, limit, base_url=base_url)
    said = [", ".join(str(c[k]) for k in ("name", "region", "country") if c.get(k)) for c in cities]
    width = max((len(s) for s in said), default=0) + 2
    for name, c in zip(said, cities):
        also = f"  (as {c['also']})" if c.get("also") else ""
        echo(f"{name:{width}}{c['lat']:.4f}, {c['lon']:.4f}{also}")
    if not cities:
        echo(f"(no US city's name or other name starts with {text!r} - name a larger US city near it, "
             "or pass --place LAT,LON in the US)")
    return cities



def _robots(m: dict) -> str:
    """The robots its machine says are connected to its ports and their median round trip ("3 · 9 ms"), "0" for none, '—'
    while it has said nothing lately.
"""
    r = m.get("robots")
    if not isinstance(r, dict):
        return "—"
    n = int(r.get("count") or 0)
    return f"{n} · {_ms(r.get('rtt_p50_ms'))}" if n else "0"


def _table(rows: list, echo: Echo, *, ended: bool) -> None:
    """GPUs a row each — id, the place asked for, its cards ("L4 × 4", _card), status, when it started (and ended), and for
    one live where it is reached, its ports, its robots and what it started from; then what it cost — and why one ended as
    it did under its row, the platform's word for it."""
    heads = ["id", "place", "gpu", "status", "started"] + (["ended"] if ended else ["address", "ports", "robots", "image"])
    cells = [[str(m.get("id")), str(m.get("place") or "—"), _card(m), _status(m),
              stamp(m.get("started_at")) if m.get("started_at") else "—"]
             + ([stamp(m.get("ended_at")) if m.get("ended_at") else "—"] if ended else
                [" ".join(str(a) for a in (m.get("host") or m.get("address"), m.get("address6")) if a) or "—",
                 ",".join(str(p) for p in m.get("ports") or []) or "—",
                 _robots(m), str(m.get("image") or "—")])
             for m in rows]


    widths = [max([len(h)] + [len(c[i]) for c in cells]) + 2 for i, h in enumerate(heads)]
    echo("".join(f"{h:{w}}" for h, w in zip(heads, widths)) + "spent")
    for m, c in zip(rows, cells):
        echo("".join(f"{v:{w}}" for v, w in zip(c, widths)) + _usd(m.get("usd_so_far")))
        if m.get("reason"):
            echo(f"    ↳ {m['reason']}")
        if not ended and isinstance(m.get("follow"), dict) and m["follow"]:


            echo("    ↳ followed by " + ", ".join(_followed_from(r, v) for r, v in sorted(m["follow"].items())))


def _followed_from(robot: str, where: Any) -> str:
    """One robot of a GPU's list, where it was let in from: "arm-1 from 203.0.113.9/32", "arm-1 (not yet)", or, by its
    lines, "arm-1 by eth0 from 2001:db8:7::/64 and by wwan0 from 198.51.100.4/32"."""
    if isinstance(where, dict) and where:
        return robot + " " + " and ".join(f"by {n} from {v}" if v else f"by {n} (not yet)"
                                          for n, v in sorted(where.items()))
    return f"{robot} from {where}" if where and not isinstance(where, dict) else f"{robot} (not yet)"


def gpu_list(*, base_url: str | None = None, echo: Echo = _silent) -> dict:
    """`seq gpu list`: your GPU machines that are live, in a table — id, the place you asked for, its cards, status, when
    it started, its address and ports, the robots on them and their round trip as the GPU measures it, what it started
    from, what it has cost — and how many cards of your GPU limit they hold, a machine of four holding four. Those over are
    `seq gpu history`'s. Returns what
    sequence_ai.gpu.list read.
"""
    import sequence_ai

    out = sequence_ai.gpu.list(base_url=base_url)
    rows = out.get("gpus") or []
    _table(rows, echo, ended=False)
    if not rows:
        echo("(no GPU machine is live — open one with seq gpu add; seq gpu history lists those over)")
    elif any(isinstance(m.get("robots"), dict) for m in rows):
        echo("robots: those connected to its ports, and their median round trip as the GPU measures it")
    quota = out.get("quota") or {}
    if quota.get("limit") is not None:
        echo(f"GPU limit  {quota.get('used', sum(_cards(m) for m in rows))} / {quota['limit']} cards")
    return out


def gpu_history(limit: int | None = None, cursor: str | None = None, *, base_url: str | None = None,
                echo: Echo = _silent) -> dict:
    """`seq gpu history [--limit N] [--cursor C]`: your GPU machines that are over, kept 30 days, the one ended last
    first — id, the place you asked for, its cards, status, when it started and ended, what it cost in all, and why one
    failed — a page at a time. Returns what sequence_ai.gpu.history read.
"""
    import sequence_ai

    out = sequence_ai.gpu.history(limit, cursor, base_url=base_url)
    rows = out.get("gpus") or []
    _table(rows, echo, ended=True)
    if not rows:
        echo("(no GPU machine is over in the last 30 days)")
    if out.get("next_cursor"):
        echo(f"more: seq gpu history --cursor {out['next_cursor']}")
    return out



FOLLOW_S = 2.0
LOGS_PAGE = 1000


def _logged(e: dict) -> str:
    """One entry as a line: its time, then an event as said, or `| ` and a line its command printed."""
    text = str(e.get("text") or "")
    return f"{stamp(e.get('at'), unit='second')}  {text if e.get('kind') == 'event' else '| ' + text}"


def gpu_logs(gpu_id: str, *, since: str | None = None, follow: bool = False, base_url: str | None = None,
             echo: Echo = _silent, sleep: Callable[[float], None] | None = None) -> dict:
    """`seq gpu logs <id> [--since WHEN] [--follow]`: a GPU machine's log, oldest first — what happened to it and what
    its command printed — all of it from `since`, then, with `follow`, what comes as it comes, until it ends (or ^C).
    Returns what sequence_ai.gpu.logs read, its entries all of them. Kept 90 days after it ends.
"""
    import time

    import sequence_ai

    wait = time.sleep if sleep is None else sleep
    out = sequence_ai.gpu.logs(gpu_id, since=since, limit=LOGS_PAGE, base_url=base_url)
    entries: list = []
    while True:
        new = list(out.get("entries") or [])
        for e in new:
            echo(_logged(e))
        entries += new
        if len(new) >= LOGS_PAGE:
            out = sequence_ai.gpu.logs(gpu_id, after=out.get("next"), limit=LOGS_PAGE, base_url=base_url)
            continue
        if not follow or (out.get("ended") and not new):
            break
        try:
            wait(FOLLOW_S)
        except KeyboardInterrupt:
            break
        out = sequence_ai.gpu.logs(gpu_id, after=out.get("next"), limit=LOGS_PAGE, base_url=base_url)
    if not entries:
        echo("(nothing in its log" + (" since then" if since else "") + ")")
    return {**out, "entries": entries}



def _ssh_key() -> tuple[Path, Path] | None:
    """Your SSH key pair under ~/.ssh — (public, private): id_ed25519 first, then id_rsa, then id_ecdsa, then any
    *.pub; None when you have none (gpu_ssh makes one: _made, _kept). Only the public half is ever read and sent; the
    private half stays on disk for the system ssh to use."""
    d = Path.home() / ".ssh"
    for name in ("id_ed25519.pub", "id_rsa.pub", "id_ecdsa.pub"):
        pub = d / name
        if pub.exists():
            return pub, pub.with_suffix("")
    found = sorted(d.glob("*.pub")) if d.exists() else []
    return (found[0], found[0].with_suffix("")) if found else None


def _made(aside: Path) -> Path:
    """A new ed25519 key, no passphrase, made in `aside` - a directory of this run's, not ~/.ssh: its public half."""
    priv = aside / "id_ed25519"
    subprocess.run(["ssh-keygen", "-t", "ed25519", "-f", str(priv), "-N", "", "-C", "sequence-gpu"],
                   check=True, stdout=subprocess.DEVNULL)
    return priv.with_suffix(".pub")


def _kept(made: Path) -> tuple[Path, Path]:
    """The key _made made (`made` its public half), kept in ~/.ssh as id_ed25519 - (public, private) - and never over a
    file there: one that took the name while this ran (another `seq gpu ssh` that made one) is left as it is, said."""
    d = Path.home() / ".ssh"
    d.mkdir(mode=0o700, exist_ok=True)
    priv = d / "id_ed25519"
    try:
        for src, dst, mode in ((made.with_suffix(""), priv, 0o600), (made, priv.with_suffix(".pub"), 0o644)):
            with os.fdopen(os.open(dst, os.O_WRONLY | os.O_CREAT | os.O_EXCL, mode), "wb") as f:
                f.write(src.read_bytes())
    except FileExistsError:
        raise Unavailable(f"{priv} was made while this ran - run `seq gpu ssh` again to use it") from None
    print(f"no SSH key in ~/.ssh — made {priv}", file=sys.stderr, flush=True)
    return priv.with_suffix(".pub"), priv


def gpu_ssh(gpu_id: str, words: list[str], *, do_print: bool = False, base_url: str | None = None) -> int:
    """`seq gpu ssh <id> [-- COMMAND]`: send your public key to the machine (POST /v1/gpus/{id}/ssh), which the
    platform signs into a certificate, then hand off to the system ssh as root — a shell, or one command after `--`.
    Its exit code is the ssh's own. `--print` (do_print) instead keeps the certificate under ~/.config/sequences and prints an
    ~/.ssh/config Host block for it, named by its id, without connecting. (A machine that is not running is refused by the gateway, said
    as it comes.) With no key in ~/.ssh, one is made aside and kept there once the platform answered for that
    machine: one that is not there, or does not run, is refused with ~/.ssh as it was.

"""
    path = f"/v1/gpus/{segment(gpu_id, 'gpu id')}/ssh"
    key = _ssh_key()
    if key is None:
        with tempfile.TemporaryDirectory() as aside:
            made = _made(Path(aside))
            info = _call("POST", path, base_url, {"public_key": made.read_text().strip()})
            key = _kept(made)
    else:
        info = _call("POST", path, base_url, {"public_key": key[0].read_text().strip()})
    priv = key[1]
    host, port, user = info.get("host"), info.get("port"), info.get("user") or "root"


    cert = info.get("certificate")
    if not cert:
        raise Unavailable("the machine returned no SSH certificate - run `seq gpu ssh` again in a moment")
    if do_print:
        return _ssh_print(gpu_id, host, port, user, priv, cert)
    rest = words[1:] if words[:1] == ["--"] else words
    opts = ["-i", str(priv), "-o", "IdentitiesOnly=yes", "-o", "StrictHostKeyChecking=accept-new",
            "-o", f'UserKnownHostsFile="{_known_hosts(gpu_id)}"']
    print(f"connecting to {gpu_id} as {user} ({host}:{port})…", file=sys.stderr, flush=True)


    with tempfile.TemporaryDirectory() as tmp:
        cert_path = Path(tmp) / "gpu-cert.pub"
        cert_path.write_text(cert if cert.endswith("\n") else cert + "\n")
        argv = ["ssh", *opts, "-o", f"CertificateFile={cert_path}", "-p", str(port), f"{user}@{host}", *rest]
        return subprocess.call(argv)


def _own(gpu_id: str, suffix: str) -> Path:
    """A file of this GPU's under the config directory your sign-ins live in (~/.config/sequences), never ~/.ssh: its
    certificate (`--print`) or its known_hosts. `seq gpu remove` removes them with it."""
    from sequence_ai._core import login as signin

    home = signin.path().parent
    home.mkdir(parents=True, mode=0o700, exist_ok=True)
    return home / f"gpu-{segment(gpu_id, 'gpu id')}-{suffix}"


def _known_hosts(gpu_id: str) -> Path:
    """This GPU's own known_hosts: the host key ssh learns on its first connect, kept for its next ones - in ~/.ssh it
    would be the user's file written, and the address and port of a GPU removed, handed to another later, would read as
    "REMOTE HOST IDENTIFICATION HAS CHANGED".
"""
    return _own(gpu_id, "known_hosts")


def _ssh_print(gpu_id: str, host: Any, port: Any, user: str, priv: Path, cert: str) -> int:
    """`--print`: keep the certificate under the config directory your sign-ins live in (~/.config/sequences, never
    ~/.ssh) and print an ~/.ssh/config Host block, named by the GPU's id, that points at it and at this GPU's own
    known_hosts, where the first connect keeps its host key as `seq gpu ssh` does (accept-new: no question asked, so
    `ssh -o BatchMode=yes` connects too) - so VS Code Remote-SSH or a plain `ssh <id>` reaches the machine with your key.
    It does not connect; the block goes to stdout to paste, the note to stderr.
"""
    cert_path = _own(gpu_id, "cert.pub")
    cert_path.write_text(cert if cert.endswith("\n") else cert + "\n")
    print(f"Host {gpu_id}\n"
          f"  HostName {host}\n"
          f"  Port {port}\n"
          f"  User {user}\n"
          f"  IdentityFile {priv}\n"
          f"  CertificateFile {cert_path}\n"
          f'  UserKnownHostsFile "{_known_hosts(gpu_id)}"\n'
          f"  StrictHostKeyChecking accept-new")
    print(f"# paste into ~/.ssh/config, then `ssh {gpu_id}` or VS Code Remote-SSH reaches it; re-run "
          f"`seq gpu ssh {gpu_id} --print` when the certificate expires", file=sys.stderr, flush=True)
    return 0



def gpu_save(gpu_id: str, name: str, replace: bool = False, *, base_url: str | None = None, echo: Echo = _silent) -> dict:
    """`seq gpu save <id> --name NAME [--replace]`: keep the GPU's disk, what was installed over its base image, as a
    snapshot to start others from (`seq gpu add --from NAME`); it saves in the background, the GPU running meanwhile.
    Returns what sequence_ai.gpu.save read."""
    import sequence_ai

    out = sequence_ai.gpu.save(gpu_id, name, replace, base_url=base_url)
    echo(f"saving {gpu_id} as {name}: it keeps running meanwhile - seq gpu saved shows when it is ready")
    return out


def _gb(v: Any) -> str:
    return f"{v:.1f} GB" if isinstance(v, (int, float)) and not isinstance(v, bool) else "—"


def gpu_saved(*, base_url: str | None = None, echo: Echo = _silent) -> dict:
    """`seq gpu saved`: your snapshots, a row each - name, status, size, the card and base image it was saved from, when,
    and what it costs a month - and why one failed under its row. Returns what sequence_ai.gpu.saved read.
    
"""
    import sequence_ai

    out = sequence_ai.gpu.saved(base_url=base_url)
    rows = out.get("snapshots") or []
    heads = ["name", "status", "size", "from", "saved"]
    cells = [[str(s.get("name")), str(s.get("status") or "—"), _gb(s.get("size_gb")),
              " ".join(str(s[k]) for k in ("gpu", "image") if s.get(k)) or "—",
              stamp(s.get("saved_at")) if s.get("saved_at") else "—"] for s in rows]
    if not rows:
        echo("(no snapshot - seq gpu save <id> --name NAME keeps a GPU's disk to start others from)")
        return out
    widths = [max([len(h)] + [len(c[i]) for c in cells]) + 2 for i, h in enumerate(heads)]
    echo("".join(f"{h:{w}}" for h, w in zip(heads, widths)) + "a month")
    for s, c in zip(rows, cells):
        echo("".join(f"{v:{w}}" for v, w in zip(c, widths)) + _usd(s.get("usd_per_month")))
        if s.get("reason"):
            echo(f"    ↳ {s['reason']}")
    return out


def gpu_saved_remove(name: str, *, base_url: str | None = None, echo: Echo = _silent) -> dict:
    """`seq gpu saved remove NAME`: delete the snapshot; its storage stops being billed. Returns what
    sequence_ai.gpu.remove_saved read."""
    import sequence_ai

    out = sequence_ai.gpu.remove_saved(name, base_url=base_url)
    echo(f"removed snapshot {name}")
    return out



def gpu_remove(gpu_id: str, force: bool = False, *, base_url: str | None = None, echo: Echo = print) -> dict:
    """`seq gpu remove <id> [--force]`: shut the machine down now — it and its disk end, billing stops — and remove this
    GPU's own files `seq gpu ssh` kept (its known_hosts, its `--print` certificate). One being saved is refused unless
    `--force`, which gives that snapshot up. Returns what sequence_ai.gpu.remove read."""
    import sequence_ai

    out = sequence_ai.gpu.remove(gpu_id, force=force, base_url=base_url)
    for suffix in ("known_hosts", "known_hosts.old", "cert.pub"):
        _own(gpu_id, suffix).unlink(missing_ok=True)
    echo(f"removed {gpu_id}")
    return out
