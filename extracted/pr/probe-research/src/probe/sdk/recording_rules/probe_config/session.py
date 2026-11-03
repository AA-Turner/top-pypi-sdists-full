# ---------------------------------------------------------------------------
# Files above the launch folder
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ParentFile:
    path: str  # the `.probe.config` (or retired default) path
    folder: str
    digest: str


def parents_reaching(launch_dir: str | os.PathLike) -> list[ParentFile]:
    """The files strictly above `launch_dir` whose rules can exclude the launch
    folder or anything inside it. Shallow first. Never raises."""
    try:
        launch = _norm(launch_dir)
    except Exception:  # noqa: BLE001
        return []
    out: list[ParentFile] = []
    walk = _Walk(frozenset(), True, 0.0)
    frame = None
    for folder in _parts(launch)[:-1]:
        try:
            frame = walk.root(folder) if frame is None else walk.child(frame, folder)
        except Exception:  # noqa: BLE001
            break
        if frame.closed is not None:
            break  # a closed folder: its file, and every file below it, is never read
        try:
            loaded = _load(folder)
        except Exception:  # noqa: BLE001
            continue
        if loaded is None or not loaded.rules:
            continue
        rel = _rel(launch, folder)
        if any(rule.could_reach(rel) for rule in loaded.rules):
            name = os.path.join(folder, CONFIG_NAME)
            if not os.path.lexists(name):
                name = os.path.join(folder, LEGACY_DIRNAME, LEGACY_FILENAME)
            out.append(ParentFile(path=name, folder=folder, digest=loaded.digest))
    return out


def parents_key(parents: Iterable[ParentFile]) -> dict[str, str]:
    return {p.path: p.digest for p in parents}


# ---------------------------------------------------------------------------
# A session's view: where it started, and the researcher's answer
# ---------------------------------------------------------------------------


def _session_file(sessions_dir: str | os.PathLike, session_id: str, suffix: str) -> Path:
    return Path(sessions_dir) / (session_id + suffix)


def _publish(path: Path, payload: str) -> bool:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_name(f".{path.name}.{os.getpid()}.tmp")
        tmp.write_text(payload, encoding="utf-8")
        os.replace(tmp, path)
        return True
    except OSError:
        return False


def launch_dir(sessions_dir: str | os.PathLike, session_id: str) -> str | None:
    try:
        text = _session_file(sessions_dir, session_id, LAUNCH_SUFFIX).read_text(encoding="utf-8").strip()
    except (OSError, ValueError):
        return None
    return text if text and os.path.isabs(text) else None


def record_launch_dir(sessions_dir: str | os.PathLike, session_id: str, cwd: str) -> bool:
    """Write where a session started, once. A resume keeps the first."""
    if not cwd or not session_id:
        return False
    path = _session_file(sessions_dir, session_id, LAUNCH_SUFFIX)
    if path.exists():
        return False
    try:
        folder = _norm(cwd)
    except Exception:  # noqa: BLE001
        return False
    return _publish(path, folder + "\n")


def _read_answer(sessions_dir: str | os.PathLike, session_id: str) -> dict:
    try:
        data = json.loads(_session_file(sessions_dir, session_id, PARENT_SUFFIX).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return data if isinstance(data, dict) else {}


def parent_status(sessions_dir: str | os.PathLike, session_id: str) -> tuple[str, list[ParentFile]]:
    """(`UNASKED` | `PENDING` | `FOLLOW` | `IGNORE` | "", files) for a session.

    "" when no file above the launch folder reaches it (nothing to ask). An
    answer given for other files (one changed or appeared since) is void:
    `UNASKED` again."""
    start = launch_dir(sessions_dir, session_id)
    if not start:
        return "", []
    parents = parents_reaching(start)
    if not parents:
        return "", []
    data = _read_answer(sessions_dir, session_id)
    if data.get("files") != parents_key(parents):
        return UNASKED, parents
    decision = data.get("decision")
    if decision in (FOLLOW, IGNORE):
        return decision, parents
    return PENDING, parents


def mark_asked(sessions_dir: str | os.PathLike, session_id: str, parents: list[ParentFile]) -> bool:
    """Record that the question went out for exactly these files."""
    return _publish(
        _session_file(sessions_dir, session_id, PARENT_SUFFIX),
        json.dumps({"files": parents_key(parents), "asked_at": time.time()}),
    )


def record_answer(sessions_dir: str | os.PathLike, session_id: str, decision: str) -> tuple[bool, list[ParentFile]]:
    """Store the researcher's answer for the files that reach this session now."""
    if decision not in (FOLLOW, IGNORE):
        raise ValueError(decision)
    start = launch_dir(sessions_dir, session_id)
    parents = parents_reaching(start) if start else []
    ok = _publish(
        _session_file(sessions_dir, session_id, PARENT_SUFFIX),
        json.dumps({"files": parents_key(parents), "decision": decision, "answered_at": time.time()}),
    )
    return ok, parents


def session_view(sessions_dir: str | os.PathLike | None, session_id: str | None) -> tuple[str | None, frozenset]:
    """(launch folder, folders set aside) for a session: the folders of the
    files above its launch folder the researcher answered `ignore` for, while
    exactly those files still reach it."""
    if sessions_dir is None or not session_id:
        return None, frozenset()
    start = launch_dir(sessions_dir, session_id)
    if not start:
        return None, frozenset()
    status, parents = parent_status(sessions_dir, session_id)
    if status != IGNORE:
        return start, frozenset()
    folders = {p.folder for p in parents}
    # A path checked through its real location (`/home` a symlink on a cluster)
    # must find the same folders set aside.
    for folder in list(folders):
        try:
            folders.add(os.path.realpath(folder))
        except (OSError, ValueError):
            pass
    return start, frozenset(folders)


def session_check(
    path: str | os.PathLike,
    sessions_dir: str | os.PathLike | None,
    session_id: str | None,
    *,
    is_dir: bool | None = None,
    cwd: str | None = None,
    as_cwd: bool = False,
) -> Verdict:
    """`check` as this session sees it. Inside an agent session the retired
    folder defaults count and an `ignore` answer sets aside the files it was
    about; with no session, every file applies and retired defaults do not."""
    _start, skip = session_view(sessions_dir, session_id)
    legacy = bool(session_id)
    if as_cwd:
        return check_cwd(path, cwd=cwd, skip=skip, legacy=legacy)
    return check(path, is_dir=is_dir, cwd=cwd, skip=skip, legacy=legacy)


# ---------------------------------------------------------------------------
# What a session is told at start
# ---------------------------------------------------------------------------


#: Beside a `hash` place in a summary: Probe records only its files' identity.
HASH_ONLY_SUFFIX = " (hash only: identity, never content)"


@dataclass
class Summary:
    entries: list[str] = field(default_factory=list)
    truncated: bool = False


def _display(path: str) -> str:
    home = os.path.expanduser("~")
    if home and home != "/" and (path == home or path.startswith(home + os.sep)):
        return "~" + path[len(home):]
    return path


def describe_rule(rule: Rule) -> str:
    """A rule as a place: `~/code/repo-a/data/`, or `*.ckpt under ~/code`."""
    if rule.line == 0:
        return _display(rule.base) + "/ (all of it)"
    body = rule.text or (rule.pattern[1:] if rule.negated else rule.pattern)
    if rule.anchored:
        return _display(os.path.join(rule.base, body.lstrip("/")))
    return f"{body} under {_display(rule.base)}"


def summarize(
    launch: str | os.PathLike,
    *,
    skip: "frozenset[str] | None" = None,
    legacy: bool = True,
    budget_s: float = 0.2,
    max_entries: int = 12,
    max_dirs: int = 20000,
) -> Summary:
    """What reaches a session started in `launch`: the excluding rules of the
    files above it (unless set aside) and of the files below it, found by a scan
    capped at `budget_s` and `max_dirs`. Never raises."""
    out = Summary()
    try:
        start = _norm(launch)
    except Exception:  # noqa: BLE001
        return out
    seen: set[str] = set()

    def add(rule: Rule) -> None:
        if rule.level == ON:
            return
        text = describe_rule(rule) + (HASH_ONLY_SUFFIX if rule.level == HASH else "")
        if text in seen:
            return
        if len(out.entries) >= max_entries:
            out.truncated = True
            return
        seen.add(text)
        out.entries.append(text)

    skipped = frozenset(skip or ())
    verdict = check_cwd(start, skip=skipped, legacy=legacy)
    if verdict.excluded and verdict.rule is not None:
        out.entries.append(f"this folder ({_display(start)})" + (HASH_ONLY_SUFFIX if verdict.identity_only else ""))
        seen.add(out.entries[-1])
    for parent in parents_reaching(start):
        if parent.folder in skipped:
            continue
        loaded = _load(parent.folder)
        rel = _rel(start, parent.folder)
        for rule in loaded.rules if loaded else ():
            if (legacy or not rule.legacy) and rule.could_reach(rel):
                add(rule)
    deadline = time.monotonic() + budget_s
    walk = _Walk(skipped, legacy, 0.0)
    frames: list = []
    walk.one(frames, os.path.join(start, "x"), False)  # the frames down to `start`
    stack = [frames[-1]] if frames and frames[-1].closed is None else []
    visited = 0
    while stack:
        if time.monotonic() > deadline or visited >= max_dirs:
            out.truncated = True
            break
        frame = stack.pop()
        visited += 1
        loaded = _load(frame.folder)
        if loaded is not None and frame.folder not in skipped:
            for rule in loaded.rules:
                if legacy or not rule.legacy:
                    add(rule)
        try:
            with os.scandir(frame.folder) as it:
                for entry in it:
                    if entry.name in SCAN_SKIP_DIRS:
                        continue
                    try:
                        if entry.is_dir(follow_symlinks=False):
                            child = walk.child(frame, entry.path)
                            if child.closed is None:  # a closed folder is never entered
                                stack.append(child)
                    except OSError:
                        continue
        except OSError:
            continue
    return out
