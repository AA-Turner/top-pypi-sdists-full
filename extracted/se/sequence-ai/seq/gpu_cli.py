"""
`seq gpu`: GPU machines you run yourself — `add` opens them near a place in the US, `places` lists the
US cities a place can be, `list` shows those live and `history` those over, `allow` changes who reaches
their ports, `ssh` opens a root shell on one, `save` keeps one's disk as a snapshot (`saved` lists them),
`remove` shuts one down. A machine is a container you are root in, on one card; you install and run
what you like, and `remove` ends the machine and its disk. (`seq gpus`, plural, is a different command:
the catalogue of cards and their prices.)

In one sentence: each command reads or writes gateway routes with the caller's key through `sequence_ai.gpu.*` and prints
what they did - `add` waits until its machines run, and Ctrl-C meanwhile cancels those not running; `ssh` adds your
`~/.ssh` public key to the machine (making one if you have none), asks the gateway for where to reach it, and hands off to
the system `ssh`.
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Callable

from sequence_ai._core.money import money, per_hour
from sequence_ai._core.names import segment
from sequence_ai.errors import Unavailable

from seq.clock import stamp
from seq.deployments_cli import _call
from seq.errors import GpuCancelled

Echo = Callable[..., None]
EVERYWHERE = "0.0.0.0/0"
OPEN_TO_ALL = "its ports are open to every address (0.0.0.0/0): authenticate in your server"
WAIT_SAID_S = 60.0


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



def _expected_ms(m: dict) -> Any:
    e = m.get("expected_rtt")
    return e.get("ms") if isinstance(e, dict) else None


def _line(m: dict) -> str:
    """One GPU on a line, as `seq gpu add` says it: id, card, the place asked for, status, its address, its ports, the round
    trip expected from near its place (`expected_rtt`, measured there) and what it costs an hour.
"""
    bits = [str(m.get("id")), str(m.get("gpu") or "—"), str(m.get("place") or "—"), _status(m)]
    if m.get("host"):
        bits.append(str(m["host"]))
    if m.get("address"):
        bits.append(str(m["address"]))
    if m.get("ports"):
        bits.append("ports " + ",".join(str(p) for p in m["ports"]))
    if isinstance(_expected_ms(m), (int, float)) and not isinstance(_expected_ms(m), bool):
        bits.append(f"expected {_ms(_expected_ms(m))}")
    bits.append(_usd(m.get("usd_per_hour"), per_hour))
    return "  ".join(bits)


def _unmeasured(m: dict) -> str | None:
    """Where nothing was measured near its place, said so (`expected_rtt` with no "ms"); None where something was, or the
    platform could not say.
"""
    e = m.get("expected_rtt")
    if not isinstance(e, dict) or _expected_ms(m) is not None:
        return None
    return (f"no round trip was measured within {e.get('within_km')} km of {m.get('place') or 'the place asked'} in the "
            f"last {e.get('days')} days")


def gpu_add(place: str, gpu: str, count: int = 1, snapshot: str | None = None, ports: list | None = None,
            allow: list | None = None, run: str | None = None, name: str | None = None, wait: bool = True, *,
            base_url: str | None = None, echo: Echo = _silent) -> list:
    """`seq gpu add --place … --gpu … [--count N] [--from NAME] [--port P]... [--allow CIDR]... [--run CMD] [--name NAME]
    [--no-wait]`:
    open the machines near `place` and, unless `--no-wait`, wait until each runs - saying so on stderr each minute - then
    say each on a line (_line), and that nothing was measured near its place where nothing was. One that failed to start
    ends the command in its error, those that run said first; Ctrl-C cancels those not running, says which and what each
    was billed (GpuCancelled), and exits 130, those that run said first. Returns what it said, as sequence_ai.gpu.add
    answers it.

"""
    import sequence_ai

    machines = sequence_ai.gpu.add(place, gpu, count, snapshot=snapshot, ports=ports, allow=allow, run=run, name=name, wait=False,
                                   base_url=base_url)
    if allow and EVERYWHERE in allow:
        _note(OPEN_TO_ALL)
    if wait and machines:
        ids = [str(m.get("id")) for m in machines]
        one = len(ids) == 1
        _note(f"{', '.join(ids)} starting: waiting until {'it runs' if one else 'they run'} (--no-wait returns once "
              f"{'it is' if one else 'each is'} asked for: seconds, not the minute or two {'it takes' if one else 'each takes'}"
              " to run)")
        said = [0.0]

        def waiting(seconds: float, starting: list) -> None:
            if seconds - said[0] >= WAIT_SAID_S:
                said[0] = seconds
                _note(f"still starting after {seconds / 60:.0f} min: {', '.join(starting)}")

        try:
            machines = sequence_ai.gpu._running(machines, said=waiting, base_url=base_url)
        except KeyboardInterrupt as stop:
            for m in getattr(stop, "running", None) or []:
                echo(_line(m))
            raise GpuCancelled(getattr(stop, "cancelled", None) or [], getattr(stop, "not_cancelled", None) or [],
                               getattr(stop, "billed", None) or {}) from None
        except Unavailable as exc:
            for m in (exc.details or {}).get("gpus") or []:
                if m.get("status") == "running":
                    echo(_line(m))
            raise
    for m in machines:
        echo(_line(m))
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



def gpu_places(text: str = "", limit: int = 8, *, base_url: str | None = None, echo: Echo = _silent) -> list:
    """`seq gpu places [words]`: the US cities whose name or another name they go by starts with the words, those of
    their own name first, the largest first, one a line - its name, state and country, then its latitude and longitude,
    either of which `seq gpu add --place` takes, and "(as <that other name>)" for a city found by one ("big apple": New
    York City, as Big Apple). Returns the list sequence_ai.gpu.places read.
    {the user 11-11: "a city drop down list and auto fill the long and lat"; the user 11-12: "we shouldnt allow
    locaiton out of us"}"""
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
    """GPUs a row each — id, the place asked for, card, status, when it started (and ended), and for one live where it is
    reached, its ports, its robots and what it started from; then what it cost — and why one ended as it did under its row,
    the platform's word for it."""
    heads = ["id", "place", "gpu", "status", "started"] + (["ended"] if ended else ["address", "ports", "robots", "image"])
    cells = [[str(m.get("id")), str(m.get("place") or "—"), str(m.get("gpu") or "—"), _status(m),
              stamp(m.get("started_at")) if m.get("started_at") else "—"]
             + ([stamp(m.get("ended_at")) if m.get("ended_at") else "—"] if ended else
                [str(m.get("host") or m.get("address") or "—"), ",".join(str(p) for p in m.get("ports") or []) or "—",
                 _robots(m), str(m.get("image") or "—")])
             for m in rows]


    widths = [max([len(h)] + [len(c[i]) for c in cells]) + 2 for i, h in enumerate(heads)]
    echo("".join(f"{h:{w}}" for h, w in zip(heads, widths)) + "spent")
    for m, c in zip(rows, cells):
        echo("".join(f"{v:{w}}" for v, w in zip(c, widths)) + _usd(m.get("usd_so_far")))
        if m.get("reason"):
            echo(f"    ↳ {m['reason']}")


def gpu_list(*, base_url: str | None = None, echo: Echo = _silent) -> dict:
    """`seq gpu list`: your GPU machines that are live, in a table — id, the place you asked for, card, status, when it
    started, its address and ports, the robots on them and their round trip as the GPU measures it, what it started from,
    what it has cost — and how many of your GPU limit they hold. Those over are `seq gpu history`'s. Returns what
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
        echo(f"GPUs  {quota.get('used', len(rows))} / {quota['limit']}")
    return out


def gpu_history(limit: int | None = None, cursor: str | None = None, *, base_url: str | None = None,
                echo: Echo = _silent) -> dict:
    """`seq gpu history [--limit N] [--cursor C]`: your GPU machines that are over, kept 30 days, the one ended last
    first — id, the place you asked for, card, status, when it started and ended, what it cost in all, and why one
    failed — a page at a time. Returns what sequence_ai.gpu.history read. {the user 11-12: "if it is closed we should
    have a history secciton instead of these thse should only be live"}"""
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



def _ssh_key() -> tuple[Path, Path]:
    """Your SSH key pair under ~/.ssh — (public, private): id_ed25519 first, then id_rsa, then id_ecdsa, then any
    *.pub; a new ed25519 key is made (no passphrase) when you have none. Only the public half is ever read and sent;
    the private half stays on disk for the system ssh to use."""
    d = Path.home() / ".ssh"
    for name in ("id_ed25519.pub", "id_rsa.pub", "id_ecdsa.pub"):
        pub = d / name
        if pub.exists():
            return pub, pub.with_suffix("")
    found = sorted(d.glob("*.pub")) if d.exists() else []
    if found:
        return found[0], found[0].with_suffix("")
    d.mkdir(mode=0o700, exist_ok=True)
    priv = d / "id_ed25519"
    print(f"no SSH key in ~/.ssh — making {priv}", file=sys.stderr, flush=True)
    subprocess.run(["ssh-keygen", "-t", "ed25519", "-f", str(priv), "-N", "", "-C", "sequence-gpu"],
                   check=True, stdout=subprocess.DEVNULL)
    return priv.with_suffix(".pub"), priv


def gpu_ssh(gpu_id: str, words: list[str], *, do_print: bool = False, base_url: str | None = None) -> int:
    """`seq gpu ssh <id> [-- COMMAND]`: send your public key to the machine (POST /v1/gpus/{id}/ssh), which the
    platform signs into a certificate, then hand off to the system ssh as root — a shell, or one command after `--`.
    Its exit code is the ssh's own. `--print` (do_print) instead keeps the certificate under ~/.config/sequences and prints an
    ~/.ssh/config Host block for it, named by its id, without connecting. (A machine that is not running is refused by the gateway, said
    as it comes.)"""
    path = f"/v1/gpus/{segment(gpu_id, 'gpu id')}/ssh"
    pub, priv = _ssh_key()
    info = _call("POST", path, base_url, {"public_key": pub.read_text().strip()})
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
