"""
`seq policy ls | versions | source | rollback | stop | start | rename | rm | traffic` — your deployments on the platform:
see them and their versions and the code each version runs, go back to an earlier version, stop and start them, rename
or delete one, split traffic.

In one sentence: `ls` reads GET /v1/deployments (your own, newest first: state, version, card, weights origin) →
`rm <name>` calls DELETE /v1/deployments/{name}, which stops its workers now (billed up to that moment), releases its
secrets and weights copy, stops its storage billing and frees the name and the quota slot. Each call takes `echo=`
for its human lines and returns what it read, which `seq --json` prints instead.

"""
from __future__ import annotations

import io
import os
import pathlib
import tarfile
from typing import Any

import httpx

from seq import columns, safe_path
from seq._account import auth_headers, credential
from seq._gateway import DEFAULT_BASE_URL
from seq.errors import raise_for, unreachable
from sequence_ai._core.names import segment
from sequence_ai.errors import InternalError, InvalidRequest, NotFound, SequencesError



_NOTICE_HEADER = "X-Deploy-Notice"


def _call(method: str, path: str, base_url: str | None, body: dict | None = None, *, raw: bool = False,
          content: bool = False, person: bool = False, upload: tuple[bytes, str] | None = None,
          timeout: float = 60) -> Any:
    """One platform call: what it answered (with `raw`, its text — a CSV export; with `content`, its bytes — a version's
    source; a JSON object with the notice the platform sent beside it, as its `notice`), or the exception the one mapping makes
    of a refusal — whose message is the platform's own reason, never the key; one for want of GPUs says which limit,
    in one sentence (sequence_ai/_core/capacity.py). Sent as the key, else your `seq login` sign-in; with `person`
    (what only you may do), as your sign-in alone (seq/_account.credential). `upload` (bytes, content type) is sent
    as the body itself, in place of JSON. `timeout`: how long its answer is waited for (a command's run: shell_cli)."""
    base = (base_url or os.environ.get("SEQUENCES_BASE_URL") or DEFAULT_BASE_URL).rstrip("/")
    key = credential(None, base, person=person)
    from seq._http import RetryReads

    sent = {"content": upload[0], "headers": {"Content-Type": upload[1]}} if upload is not None else {"json": body}
    try:

        with httpx.Client(headers=auth_headers(key), timeout=timeout, transport=RetryReads()) as client:
            r = client.request(method, f"{base}{path}", **sent)
    except httpx.TransportError as exc:
        raise unreachable(base, exc) from None
    raise_for(r)
    if content or raw:
        return r.content if content else r.text
    got = r.json()
    notice = r.headers.get(_NOTICE_HEADER)
    if notice and isinstance(got, dict):
        got["notice"] = notice
    return got


def _unpack(data: bytes, dest: pathlib.Path) -> list[str]:
    """The download's files written under `dest`, its top folder (`<name>-v<n>/`) left out: files and folders only, and
    none whose path would land outside `dest` - on Windows too, where "\\" separates and "C:" names a drive
    (safe_path). Returns their paths."""
    out = []
    with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as tf:
        for member in tf.getmembers():
            parts = (safe_path.parts_of(member.name) or [])[1:]
            if not parts or not (member.isfile() or member.isdir()):
                continue
            target = dest.joinpath(*parts)
            if member.isdir():
                target.mkdir(parents=True, exist_ok=True)
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(tf.extractfile(member).read())
            target.chmod((member.mode & 0o777) | 0o600)
            out.append("/".join(parts))
    return out


def _is_code_of(dest: pathlib.Path, files: list[str], want: str) -> bool:
    """Whether the unpacked code - build-context/ left out, the Dockerfile's context and not the code - is the tree the
    version recorded (GET .../versions rows' code.sha256, the number `seq deploy` prints as "tree sha256"): its hash
    over the files a tree holds (seq.source), or over every file the platform sent, whichever way it was taken."""
    from seq.source import file_sha256, files_sha256, tree_files

    sent = files_sha256((f, (dest / f).stat().st_size, file_sha256(dest / f)) for f in files
                        if not f.startswith("build-context/"))
    tree = files_sha256((rel, path.stat().st_size, file_sha256(path)) for rel, path in tree_files(dest)
                        if not rel.startswith("build-context/"))
    return want in (sent, tree)


def source(name: str, version: int | None = None, out: str | None = None, base_url: str | None = None,
           echo=print) -> dict:
    """`seq policy source <name>[@vN] [-o PATH]`: the code a version runs, as it deployed it - the version serving
    unless NAME@vN names another - downloaded (GET /v1/deployments/{name}/versions/{n}/source, checked by the
    platform against what the version deployed) and unpacked into DIR, `./<name>-v<n>` unless -o names one; a folder
    that holds anything is refused, so nothing of yours is written over. Returns {name, version, dir, files}.
    """
    rows = _call("GET", f"/v1/deployments/{segment(name)}/versions", base_url)["data"]
    if version is None:
        version = next((r["version"] for r in rows if r.get("state") in ("serving", "stopped")), None)
        if version is None:
            raise InvalidRequest(f"no version of {name} serves yet; name one: {name}@vN",
                                 hint=f"seq policy versions {name}")

    want = (next((r for r in rows if r.get("version") == int(version)), {}).get("code") or {}).get("sha256")
    dest = pathlib.Path(out or f"{name}-v{version}")
    if dest.exists() and (not dest.is_dir() or any(dest.iterdir())):
        raise InvalidRequest(f"{dest} already holds files; name a new or empty folder with -o")
    data = _call("GET", f"/v1/deployments/{segment(name)}/versions/{int(version)}/source", base_url, content=True)
    dest.mkdir(parents=True, exist_ok=True)
    files = _unpack(data, dest)
    if want and not _is_code_of(dest, files, want):
        raise InternalError(f"the files in {dest}/ are not the code v{version} of {name} deployed (its tree sha256 "
                            f"{want[:12]}); do not run them, and tell us")
    size = sum((dest / f).stat().st_size for f in files)
    echo(f"{name} v{version}: {len(files)} file{'' if len(files) == 1 else 's'} ({size:,} bytes) in {dest}/ - the code "
         "it runs, as it deployed it" + (f"; tree sha256 {want[:12]}, the same as the version's" if want else ""))
    return {"name": name, "version": int(version), "dir": str(dest), "files": files,
            **({"tree_sha256": want} if want else {})}


def page_query(limit: int | None, cursor: str | None) -> str:
    """A list request's paging as a query string: `limit` rows from the `cursor` the previous page printed - the pages
    the console's pager steps through. Empty when neither is given (the gateway's 50 from the
    start)."""
    from urllib.parse import urlencode

    q = {k: v for k, v in (("limit", limit), ("cursor", cursor)) if v is not None}
    return f"?{urlencode(q)}" if q else ""


def weights_cell(row: dict) -> str:
    """A deployment's or a version's weights as `seq policy ls` and `seq policy versions` list them: weights in named
    parts each by its name with its size, the first among them (the platform's weights_parts) - else the one origin,
    with the commit it is pinned to where the platform says it.
"""
    parts = row.get("weights_parts")
    if parts:
        return ", ".join(f"{name}: {(part or {}).get('uri') or '-'}" + (f" ({part_size(part)})" if (part or {}).get(
            "bytes") is not None else "") for name, part in parts.items())
    return (row.get("weights") or "") + (f"  ({row['weights_revision'][:12]})" if row.get("weights_revision") else "")


def part_size(part: dict | None) -> str:
    """A weights part's size as the platform read it, as a delete's list says a size (_gb); "size not read" for none."""
    size = (part or {}).get("bytes")
    return _gb(int(size) / 1e9) if size is not None else "size not read"


def list_remote(base_url: str | None = None, echo=print, *, limit: int | None = None,
                cursor: str | None = None) -> dict:
    """`seq policy ls [--limit N] [--cursor C]`: print one page of the caller's deployments, newest first, then where the
    page sits and the flag for the next one; return the page as the gateway sent it ({"data": [...], "total": N,
    "offset": 0, "next_cursor": "50" or None}).
"""
    from seq.listing import _footer

    out = _call("GET", "/v1/deployments" + page_query(limit, cursor), base_url)
    rows = out["data"]
    if not rows:
        echo("no deployments yet — `seq deploy <folder> [--name <name>]`" if not cursor else "no deployments on this page")
        return out

    head = ["name", "status", "ver", "gpu", "weights"]
    cells = [[r["name"],
              "stopped" if r.get("stopped") else r["status"], "v" + str(r.get("version") or 1),
              str(r.get("gpu") or "-"),
              weights_cell(r)]
             for r in rows]
    widths = columns.widths([head, *cells])
    w = widths[0]
    echo(columns.line(head, widths))
    for r, row in zip(rows, cells):
        echo(columns.line(row, widths))
        if r.get("status") == "failed" and r.get("error"):
            echo(f"{'':{w}}  ↳ {error_line(r['error'])}")
        latest = r.get("latest")
        if latest:

            what = "building" if latest["status"] == "building" else \
                f"failed: {error_line(latest.get('error'), width=90)}"
            echo(f"{'':{w}}  ↳ v{latest['version']} {what}")
        if r.get("template_update"):
            u = r["template_update"]
            echo(f"{'':{w}}  ↳ {u['name']} {u['version']} is available (runs {u['from']}) — seq policy upgrade "
                 f"{r['name']}")
    _footer(out, len(rows), echo)
    return out


def error_line(error: Any, stage: str | None = None, width: int = 100) -> str:
    """A build's error in the one line a list gives it: its first line, without the step's name before it when the list
    names that step already ("failed in its image step"), and without the colon that leads its own lines below - the
    build's log, which `--build` shows - so a line never ends on a colon with nothing after it. The platform keeps an
    image build's error as "image: the image build failed:\n<its log>": the builder's own first line, the step's
    phase before it, its log below.
"""
    first = next((ln.strip() for ln in str(error or "").splitlines() if ln.strip()), "")
    if stage and first.startswith(f"{stage}: "):
        first = first[len(stage) + 2:]
    return first.removesuffix(":").rstrip()[:width]


def versions(name: str, base_url: str | None = None, echo=print) -> dict:
    """`seq policy versions <name>`: a deployment's versions, newest first - building, serving, every earlier one kept until
    it is deleted, one on its way out ("deleting") - each
    with its card, template version and weights, and its build: how long it took, why it was built (the files,
    checkpoint, card or template it changed) and the step a failed one stopped in; then the builds of versions no longer
    kept (GET .../versions and .../builds). Returns both, {"versions", "builds"}.
    WHY one command: `seq policy versions` and `seq policy builds` listed the same versions twice, each with half of what
    a version is.

    """
    from seq.deploy_cli import elapsed
    from seq.listing import edited_label
    from seq.upgrade_cli import template_lines

    out = _call("GET", f"/v1/deployments/{segment(name)}/versions", base_url)
    rows = out["data"]
    try:
        built = _call("GET", f"/v1/deployments/{segment(name)}/builds", base_url).get("builds") or []
    except SequencesError:
        built = []
    by_version = {b.get("version"): b for b in built}
    took = {id(r): (elapsed(b["duration_s"]) if isinstance((b := by_version.get(r["version"]) or {}).get("duration_s"),
                                                            (int, float)) else "-") for r in rows}


    tpl = {id(r): f"{r['template']['name']} {r['template']['version']}" if r.get("template")
           else edited_label(r["edited_from"]) if r.get("edited_from") else "-" for r in rows}

    head = ["ver", "state", "gpu", "template", "took", "weights"]
    cells = [["v" + str(r["version"]), r["state"], str(r.get("gpu") or "-"), tpl[id(r)], took[id(r)],
              weights_cell(r)] for r in rows]
    widths = columns.widths([head, *cells])
    lead = widths[0]
    echo(columns.line(head, widths))
    for r, row in zip(rows, cells):
        echo(columns.line(row, widths))
        b = by_version.get(r["version"]) or {}
        if b:
            echo(f"{'':{lead}}  ↳ built: {why_said(b.get('why'))}")
            if image := image_said(b.get("why")):
                echo(f"{'':{lead}}  ↳ image: {image}")
        if b.get("failed_stage"):
            first = error_line(b.get("error"), b["failed_stage"])
            echo(f"{'':{lead}}  ↳ failed in its {b['failed_stage']} step" + (f": {first}" if first else ""))
        elif r.get("error"):
            echo(f"{'':{lead}}  ↳ {error_line(r['error'])}")

    listed = {r["version"] for r in rows}
    older = [b for b in built if b.get("version") not in listed]
    if older:
        echo("builds of versions no longer kept:")
        gone = [["v" + str(b.get("version")), str(b.get("state") or "-"),
                 elapsed(b["duration_s"]) if isinstance(b.get("duration_s"), (int, float)) else "-",
                 why_said(b.get("why"))] for b in older]
        gone_widths = columns.widths(gone)
        for b, row in zip(older, gone):
            echo(columns.line(row, gone_widths))
            if image := image_said(b.get("why")):
                echo(f"{'':{gone_widths[0]}}  ↳ image: {image}")


            if b.get("replaced_by") is not None:
                first = error_line(b.get("error"), b.get("failed_stage"))
                where = f"failed in its {b['failed_stage']} step" if b.get("failed_stage") else "failed"
                echo(f"{'':{gone_widths[0]}}  ↳ {where}" + (f": {first}" if first else "")
                     + f"; replaced by v{b['replaced_by']}")
    if any(r["state"] == "kept" for r in rows):
        echo(f"go back to one with `seq policy rollback {name}@v<ver>` (no rebuild)")
    if built:
        echo(f"a build's steps: seq policy logs {name}@v<ver> --build")
    serving_row = next((r for r in rows if r["state"] == "serving"), None)
    for line in template_lines(None if serving_row is None else serving_row.get("template"),
                               out.get("template_update"), name)[1:]:
        echo(line.strip())
    return {"versions": rows, "builds": built}


def _names(paths: list, verb: str) -> str | None:
    if not paths:
        return None
    shown = ", ".join(str(p) for p in paths[:3]) + (f" and {len(paths) - 3} more" if len(paths) > 3 else "")
    return f"{shown} {verb}"


def why_said(why: dict | None) -> str:
    """Why a version was built, in a few words, from its build history's `why` (GET .../builds): which files of its
    changed, whether its checkpoint, its card or its image's definition did, a template upgrade with the versions it
    moved between, a redeploy of the same - against the version it names."""
    why = why or {}
    since = why.get("since_version")
    if why.get("trigger") is None and since is None:
        return "the version before it is no longer kept"
    files = why.get("files") or {}
    if since is None:
        return f"first version: {len(files.get('added') or [])} files" if why.get("files") else "first version"
    said = []
    tpl = why.get("template")
    if isinstance(tpl, dict):
        said.append(f"template upgrade: {tpl.get('name')} {tpl.get('from')} → {tpl.get('to')}")
    if why.get("files"):
        said += [x for x in (_names(files.get("changed") or [], "changed"), _names(files.get("added") or [], "added"),
                             _names(files.get("removed") or [], "removed")) if x]
    elif why.get("code") == "changed":
        said.append("code changed")
    if why.get("checkpoint") == "changed":
        said.append("new checkpoint")
    card = why.get("card")
    if isinstance(card, dict):
        said.append(f"card {', '.join(card.get('from') or []) or 'none'} → {', '.join(card.get('to') or []) or 'none'}")
    if (why.get("image_detail") or {}).get("definition") == "changed":
        said.append("image definition changed")
    if why.get("unchanged") and not said:
        said.append("nothing of yours changed" + (", the platform updated" if why.get("platform") == "changed" else ""))
    return (", ".join(said) or "rebuilt") + f" (vs v{since})"


def image_said(why: dict | None) -> str | None:
    """What changed in a version's image definition, as its build history says it (`why.image_detail.said`: its base
    image, its Python, the packages and system packages it installs, its environment, its steps), printed as it is on
    one line under its `built:` line; None when its definition did not change, or the platform does not say.
    """
    detail = (why or {}).get("image_detail") or {}
    said = detail.get("said")
    if detail.get("definition") != "changed" or not isinstance(said, str) or not said.strip():
        return None
    return " ".join(said.split("\n")).strip()


def rollback(name: str, to: int | None = None, base_url: str | None = None, echo=print) -> dict:
    """`seq policy rollback NAME[@vN]`: serve a kept version again (`to`; the newest earlier one by default) — no
    rebuild: it serves from now on, robots move to it at their next episode, and when none of its workers is running one
    starts first.
"""
    out = _call("POST", f"/v1/deployments/{segment(name)}/rollback", base_url, {"version": to})
    kept = ", ".join(f"v{v}" for v in out["kept_versions"])
    v = out["version"]
    echo(f"{out['name']} now serves v{v}" + (f" (kept: {kept})" if kept else ""))
    echo(f"robots move to v{v} at their next episode; when no worker of v{v} is running, one starts first (a cold start)")
    if (out.get("dropped") or {}).get("message"):

        echo(out["dropped"]["message"])
    return out


def stop(name: str, base_url: str | None = None, echo=print) -> dict:
    """End every worker now and refuse connects until `seq policy start`. A version still building goes on."""
    out = _call("POST", f"/v1/deployments/{segment(name)}/stop", base_url)
    n = out["workers_stopped"]
    echo(f"stopped {out['name']}" + (f" (ended {n} worker{'s' if n != 1 else ''})" if n else "") +
         f" — `seq policy start {out['name']}` lets robots connect again")
    if building := still_building(out):
        echo(building)
    return out


def still_building(out: dict) -> str | None:
    """What a stop leaves going, said: a version on its way in - beside the serving one (`latest`), or the first one (the
    deployment itself building) - finishes and is checked as usual, its check billed like any worker, and once it passes
    it is the version that serves when the deployment starts. None when no version builds. A stop never ends a build:
    the gateway promotes and bills a version whatever its deployment's stop (build_flow._refresh_pending, _bill_check).
    """
    name, latest = out.get("name"), out.get("latest") or {}
    if latest.get("status") == "building" and latest.get("version") is not None:
        v = latest["version"]
    elif out.get("status") == "building" and out.get("version") is not None:
        v = out["version"]
    else:
        return None
    return (f"v{v} is still building: it finishes and is checked as usual, its check billed like any worker; once it "
            f"passes, v{v} is the version that serves when you start {name}")


def rename(name: str, new: str, base_url: str | None = None, echo=print) -> dict:
    """`seq policy rename <name> <new>`: the deployment's new name — what robots connect by. Its workers end (the next
    connect starts one); its versions, keys and settings stay with it."""
    out = _call("POST", f"/v1/deployments/{segment(name)}/rename", base_url, {"name": new})
    echo(f"renamed {out['renamed_from']} → {out['name']} (ended {out['workers_stopped']} worker(s)) — "
         f"robots now connect with model={out['name']!r}; keys bound to it keep working")
    return out


def start(name: str, base_url: str | None = None, echo=print) -> dict:
    out = _call("POST", f"/v1/deployments/{segment(name)}/start", base_url)
    echo(f"started {out['name']} — the next connect starts a worker of v{out['version']}")
    return out


def rm(name: str, base_url: str | None = None, echo=print, *, force: bool = False, dry_run: bool = False) -> dict:
    """Delete one deployment by name, for good - refused while robots are connected to it or evals run on it, unless
    `force` - having listed first what the delete touches (GET .../deletion, _deletion_said); `dry_run` lists it and deletes
    nothing. A platform from before has no such read: the delete goes on unlisted, and a dry run says it cannot list. A
    NAME@vN deletes that version alone (_rm_version).
"""
    from seq.cli_parser import at_version

    base, version = at_version(name)
    if version is not None:
        return _rm_version(base, version, base_url, echo, dry_run=dry_run)
    try:
        plan = _call("GET", f"/v1/deployments/{segment(name)}/deletion", base_url)
    except NotFound as exc:
        if exc.message.strip().lower() != "not found":
            raise
        plan = None
    if plan is not None:
        echo(f"deleting policy {plan['deployment']} " + ("would:" if dry_run else "will:"))
        for line in _deletion_said(plan, force=force):
            echo(f"  {line}")
    if dry_run:
        if plan is None:
            echo(f"this platform cannot list what deleting {name} touches yet; nothing was deleted")
        return plan or {}
    out = _call("DELETE", f"/v1/deployments/{segment(name)}" + ("?force=true" if force else ""), base_url)
    stopped = out["workers_stopped"]
    echo(f"deleted {out['deleted']} for good" + (f" (stopped {stopped} worker{'s' if stopped != 1 else ''})" if stopped else ""))
    for e in out.get("evals_canceled") or []:
        echo(f"  canceled eval {e}")

    if out.get("dataset"):
        echo(f"  its captured data stays as the dataset {out['dataset']}, billed as storage until you delete it with "
             "seq volume rm")
    return out


def _rm_version(name: str, version: int, base_url: str | None, echo, *, dry_run: bool = False) -> dict:
    """`seq policy rm NAME@vN`: that version deleted for good, the policy and its other versions staying (DELETE
    .../versions/N) - one kept goes once its workers have ended, a failed one at once; the one serving is refused, as one
    still building is."""
    out = _call("DELETE", f"/v1/deployments/{segment(name)}/versions/{int(version)}" + ("?dry_run=true" if dry_run else ""),
                base_url)
    if dry_run:
        echo(f"deleting {name}@v{version} would delete that version for good: nothing can bring it back; {name} and its "
             "other versions stay")
    elif out.get("state") == "deleting":
        echo(f"deleted {name}@v{version} for good: what it holds goes once its workers have ended, and nothing can "
             "bring it back")
    else:
        echo(f"deleted {name}@v{version} for good")
    return out


def _deletion_said(plan: dict, *, force: bool = False) -> list[str]:
    """What a delete touches, a line each in plain words, from the platform's list (GET .../deletion): that it is for good,
    the robots connected and the evals running (refused, or ended with --force), the workers it stops, the robot keys it
    deletes, the versions and stored files it deletes, its captured data kept as a dataset, the evals whose reports stay -
    and its name and quota place, free. A part the platform could not read is said so, never as none.
"""
    def n(count: int, what: str) -> str:
        return f"{count} {what}{'' if count == 1 else 's'}"

    out = ["delete it for good: nothing can bring it back"]
    robots = plan.get("robots") or 0
    if robots:
        are = "is" if robots == 1 else "are"
        out.append(f"disconnect the {n(robots, 'robot')} connected now" if force else
                   f"be refused while {n(robots, 'robot')} {are} connected (--force disconnects them)")
    for e in plan.get("evals_running") or []:
        out.append(f"cancel eval {e}" if force else f"be refused while eval {e} runs or waits on it (--force cancels it)")
    workers = plan.get("workers")
    if workers is None:
        out.append("stop its running workers now, billed up to then (how many could not be read)")
    elif workers:
        out.append(f"stop its {n(workers, 'running worker')} now, billed up to then")
    keys = plan.get("keys")
    if keys is None:
        out.append("delete its keys (which ones could not be read)")
    elif keys:
        out.append(f"delete its robot key{'' if len(keys) == 1 else 's'}: "
                   + ", ".join(f"{k.get('name') or 'unnamed'} ({k['key']})" for k in keys))
    numbers = plan.get("versions") or []
    if numbers:
        out.append(f"delete its version{'' if len(numbers) == 1 else 's'} " + ", ".join(f"v{v}" for v in numbers)
                   + (", and stop the build that is running" if plan.get("build_in_flight") else ""))
    storage = plan.get("storage")
    if storage is None:
        out.append("delete the files it stores - their billing stops now (their size could not be read)")
    elif storage:
        out.append(f"delete its weights copy ({_gb(storage['weights_gb'])}) - its billing stops now")
    if plan.get("dataset"):
        out.append(f"keep its captured data as the dataset {plan['dataset']}: it is never deleted with the policy, "
                   "and is billed as storage until you delete it with seq volume rm")


    evals = plan.get("evals")
    if evals is None:
        out.append("keep the reports and recordings of the evals that ran it (how many could not be read): "
                   "the recordings are billed as storage until you delete those evals")
    elif evals:
        out.append(f"keep the reports and recordings of the {n(evals, 'eval')} that ran it: the recordings are billed as storage until you delete those evals")
    out.append("free its name and its place in your quota")
    return out


def _gb(gb: float) -> str:
    """A size as a delete's list says it: "12.4 GB", or "4.0 MB" under a tenth of a GB - one decimal there, as
    `seq volume ls` reads a size."""
    return f"{gb:.1f} GB" if gb >= 0.1 else f"{gb * 1000:.1f} MB"



def fork(source: str, name: str, *, base_url: str | None = None, echo=None) -> dict:
    """A new policy `name`, copied from `source` as it serves - its code, its settings and a copy of its weights, all
    its own: nothing of it moves `source` or any of its robots' keys, which stay `source`'s.
"""
    out = _call("POST", f"/v1/deployments/{segment(source)}/fork", base_url, {"name": name})
    if echo is not None:
        echo(f"{name}: a copy of {source}, building as a policy of its own - `seq policy status {name}` follows it; "
             f"give a robot a key to it with `seq robot add --policy {name}`")
    return out
