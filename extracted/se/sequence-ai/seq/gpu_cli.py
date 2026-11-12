"""
`seq gpu`: GPU machines you run yourself — `add` opens them near a place, `places` lists the cities a
place can be, `list` shows them, `ssh` opens a root shell on one, `remove` shuts one down. A machine
is a container you are root in, on one card; you install and run what you like, and `remove` ends the
machine and its disk. (`seq gpus`, plural, is a different command: the catalogue of cards and their
prices.)

In one sentence: `add` / `places` / `list` / `remove` each read or write one gateway route with the caller's key
through `sequence_ai.gpu.*` and print what they did; `ssh` adds your `~/.ssh` public key to the
machine (making one if you have none), asks the gateway for where to reach it, and hands off to the
system `ssh`.
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

Echo = Callable[..., None]


def _silent(*_args: Any, **_kwargs: Any) -> None:
    """The `echo` of a `seq --json` call: it returns what it read and prints nothing."""


def _usd(v: Any, fmt: Callable[[Any], str] = money) -> str:
    """An amount or a price-an-hour as sequence_ai/_core/money.py writes it; '—' where the platform did not say it."""
    return fmt(v) if isinstance(v, (int, float)) and not isinstance(v, bool) else "—"



def gpu_add(place: str, gpu: str, count: int = 1, *, base_url: str | None = None, echo: Echo = _silent) -> list:
    """`seq gpu add --place … --gpu … --count …`: open the machines near `place`, then say each one — its id, card and
    where it landed — and what one costs an hour. Returns the list sequence_ai.gpu.add did."""
    import sequence_ai

    machines = sequence_ai.gpu.add(place, gpu, count, base_url=base_url)
    for m in machines:
        echo(f"gpu {m.get('id')}  {m.get('gpu') or '—'} near {place} → {m.get('where') or '—'}  {m.get('status') or '—'}")
    priced = next((m for m in machines if m.get("usd_per_hour") is not None), None)
    if priced is not None:
        echo(f"{_usd(priced['usd_per_hour'], per_hour)} each — seq gpu list shows what they have cost and your limit")
    return machines



def gpu_places(text: str = "", limit: int = 8, *, base_url: str | None = None, echo: Echo = _silent) -> list:
    """`seq gpu places [words]`: the cities whose name or another name they go by starts with the words, those of their
    own name first, the largest first, one a line - its name, region and country, then its latitude and longitude,
    either of which `seq gpu add --place` takes, and "(as <that other name>)" for a city found by one ("paris": Warsaw,
    as Paris of the North). Returns the list sequence_ai.gpu.places read.
    {the user 11-11: "a city drop down list and auto fill the long and lat"}"""
    import sequence_ai

    cities = sequence_ai.gpu.places(text, limit, base_url=base_url)
    said = [", ".join(str(c[k]) for k in ("name", "region", "country") if c.get(k)) for c in cities]
    width = max((len(s) for s in said), default=0) + 2
    for name, c in zip(said, cities):
        also = f"  (as {c['also']})" if c.get("also") else ""
        echo(f"{name:{width}}{c['lat']:.4f}, {c['lon']:.4f}{also}")
    if not cities:
        echo(f"(no city's name or other name starts with {text!r} - name a larger city near it, "
             "or pass --place LAT,LON)")
    return cities



def gpu_list(*, base_url: str | None = None, echo: Echo = _silent) -> dict:
    """`seq gpu list`: your GPU machines in a table — id, where, card, status, when it started, what it has cost — and
    how many of your GPU limit they hold. Returns what sequence_ai.gpu.list read."""
    import sequence_ai

    out = sequence_ai.gpu.list(base_url=base_url)
    rows = out.get("gpus") or []
    iw = max([len("id")] + [len(str(m.get("id"))) for m in rows]) + 2
    ww = max([len("where")] + [len(str(m.get("where") or "—")) for m in rows]) + 2
    echo(f"{'id':{iw}}{'where':{ww}}{'gpu':9}{'status':10}{'started':18}spent")
    for m in rows:
        started = stamp(m.get("started_at")) if m.get("started_at") else "—"
        echo(f"{str(m.get('id')):{iw}}{str(m.get('where') or '—'):{ww}}{str(m.get('gpu') or '—'):9}"
             f"{str(m.get('status') or '—'):10}{started:18}{_usd(m.get('usd_so_far'))}")

        if m.get("status") == "failed" and m.get("reason"):
            echo(f"    ↳ {m['reason']}")
    if not rows:
        echo("(no GPU machines — open one with seq gpu add)")
    quota = out.get("quota") or {}
    if quota.get("limit") is not None:
        echo(f"GPUs  {quota.get('used', len(rows))} / {quota['limit']}")
    return out



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
    ~/.ssh/config Host block for it, without connecting. (A machine that is not running is refused by the gateway, said
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
    opts = ["-i", str(priv), "-o", "IdentitiesOnly=yes", "-o", "StrictHostKeyChecking=accept-new"]
    print(f"connecting to gpu {gpu_id} as {user} ({host}:{port})…", file=sys.stderr, flush=True)


    with tempfile.TemporaryDirectory() as tmp:
        cert_path = Path(tmp) / "gpu-cert.pub"
        cert_path.write_text(cert if cert.endswith("\n") else cert + "\n")
        argv = ["ssh", *opts, "-o", f"CertificateFile={cert_path}", "-p", str(port), f"{user}@{host}", *rest]
        return subprocess.call(argv)


def _ssh_print(gpu_id: str, host: Any, port: Any, user: str, priv: Path, cert: str) -> int:
    """`--print`: keep the certificate under the config directory your sign-ins live in (~/.config/sequences, never
    ~/.ssh) and print an ~/.ssh/config Host block that points at it, so VS Code Remote-SSH or a plain `ssh gpu-<id>`
    reaches the machine with your key. It does not connect; the block goes to stdout to paste, the note to stderr."""
    from sequence_ai._core import login as signin

    home = signin.path().parent
    home.mkdir(parents=True, mode=0o700, exist_ok=True)
    cert_path = home / f"gpu-{gpu_id}-cert.pub"
    cert_path.write_text(cert if cert.endswith("\n") else cert + "\n")
    print(f"Host gpu-{gpu_id}\n"
          f"  HostName {host}\n"
          f"  Port {port}\n"
          f"  User {user}\n"
          f"  IdentityFile {priv}\n"
          f"  CertificateFile {cert_path}")
    print(f"# paste into ~/.ssh/config, then `ssh gpu-{gpu_id}` or VS Code Remote-SSH reaches it; re-run "
          f"`seq gpu ssh {gpu_id} --print` when the certificate expires", file=sys.stderr, flush=True)
    return 0



def gpu_remove(gpu_id: str, *, base_url: str | None = None, echo: Echo = print) -> dict:
    """`seq gpu remove <id>`: shut the machine down now — it and its disk end, billing stops. Returns what
    sequence_ai.gpu.remove read."""
    import sequence_ai

    out = sequence_ai.gpu.remove(gpu_id, base_url=base_url)
    echo(f"removed gpu {gpu_id}")
    return out
