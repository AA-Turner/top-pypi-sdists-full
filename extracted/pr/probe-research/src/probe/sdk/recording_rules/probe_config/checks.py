# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Verdict:
    #: Probe records nothing about the path as usual (`read`, `hash` or `off`);
    #: at `hash` the SDK still records its identity (`identity_only`).
    excluded: bool
    rule: Rule | None = None
    #: The path the verdict was reached on (a closed parent folder, or the path).
    at: str = ""
    level: str = ON

    @property
    def source(self) -> str:
        return self.rule.where if self.rule is not None else ""

    @property
    def hidden(self) -> bool:
        """Probe never even reads the path (`off`)."""
        return self.level == OFF

    @property
    def identity_only(self) -> bool:
        """The SDK records the path's identity and nothing else (`hash`): path,
        sha256 or fingerprint, size and row count; never bytes or text."""
        return self.level == HASH

    @property
    def daemon_hidden(self) -> bool:
        """The daemon treats the path as `off`: `off` itself, and `hash`."""
        return self.level in (OFF, HASH)


NOT_EXCLUDED = Verdict(False)
#: What a check that broke answers: `off` (fail closed, as for an unreadable file).
CHECK_FAILED = Verdict(True, None, "", OFF)


def _verdict(rule: Rule | None, at: str) -> Verdict:
    if rule is None or rule.level == ON:
        return Verdict(False, rule, at, ON) if rule is not None else NOT_EXCLUDED
    return Verdict(True, rule, at, rule.level)


def daemon_view(verdict: Verdict) -> Verdict:
    """A verdict as the Probe daemon applies it: `hash` is `off` to the daemon
    (it never sees the path); every other level is itself."""
    if verdict.level == HASH:
        return Verdict(True, verdict.rule, verdict.at, OFF)
    return verdict


def stricter(a: Verdict, b: Verdict) -> Verdict:
    """The more restrictive of two verdicts (`a` on a tie). `read` and `hash`
    each allow what the other withholds, so where they meet the answer is
    `off`: never looser than either."""
    if a.level != b.level and {a.level, b.level} == {READ, HASH}:
        return Verdict(True, a.rule, a.at, OFF)
    return b if _RANK[b.level] > _RANK[a.level] else a


def _norm(path: str | os.PathLike, cwd: str | None = None) -> str:
    raw = os.fspath(path)
    if raw.startswith("~"):
        raw = os.path.expanduser(raw)
    if not os.path.isabs(raw):
        raw = os.path.join(cwd or os.getcwd(), raw)
    return os.path.normpath(raw)


def _parts(path: str) -> list[str]:
    """`/a/b/c` -> ['/', '/a', '/a/b', '/a/b/c']."""
    out = []
    current = path
    while True:
        out.append(current)
        parent = os.path.dirname(current)
        if parent == current:
            break
        current = parent
    out.reverse()
    return out


def _is_strict_ancestor(folder: str, of: str) -> bool:
    if folder == of:
        return False
    prefix = folder if folder.endswith(os.sep) else folder + os.sep
    return of.startswith(prefix)


def _rel(path: str, base: str) -> tuple[str, ...]:
    if path == base:
        return ()
    prefix = base if base.endswith(os.sep) else base + os.sep
    if path.startswith(prefix):
        return tuple(p for p in path[len(prefix):].split(os.sep) if p and p != ".")
    rel = os.path.relpath(path, base)
    return tuple(p for p in rel.split(os.sep) if p and p != ".")


def _decide(target: str, is_dir: bool, layers: list[tuple[str, tuple]]) -> Rule | None:
    """Last match wins across `layers` (shallow -> deep); the winning rule, or None.
    A winning negated rule returns as-is (the caller reads `negated`)."""
    for base, rules in reversed(layers):
        rel = _rel(target, base)
        if not rel:
            continue
        for rule in reversed(rules):
            if rule.matches(rel, is_dir):
                return rule
    return None


@dataclass(frozen=True)
class _Frame:
    """What a folder contributes to the paths inside it, worked out from its
    parent's frame: git's per-directory exclude stack (`dir.c` `prep_exclude`)."""

    folder: str
    #: The rules that apply inside this folder, shallow file first: (base, rules).
    layers: tuple
    #: The `off` rule that closed this folder or one above it: nothing inside is
    #: looked at, and nothing inside is turned back on.
    closed: Rule | None = None
    closed_at: str = ""
    #: The nearest rule (on this folder or one above) that set `read` or `on`:
    #: what an entry inside takes when no line matches it directly.
    inherited: Rule | None = None
    inherited_at: str = ""


class _Walk:
    """One session view (`skip`, `legacy`, `ttl`) applied to paths."""

    __slots__ = ("skip", "legacy", "ttl")

    def __init__(self, skip: frozenset, legacy: bool, ttl: float) -> None:
        self.skip, self.legacy, self.ttl = skip, legacy, ttl

    def root(self, folder: str) -> _Frame:
        return _Frame(folder, self._layers(folder, ()))

    def child(self, parent: _Frame, folder: str) -> _Frame:
        """The frame of `folder`, a folder directly inside `parent.folder`."""
        if parent.closed is not None:
            return _Frame(folder, parent.layers, parent.closed, parent.closed_at, parent.inherited, parent.inherited_at)
        found = _decide(folder, True, parent.layers)
        rule = _ceiling(found, parent)
        if rule is not None and rule.level == OFF:
            return _Frame(folder, parent.layers, rule, folder, parent.inherited, parent.inherited_at)
        if rule is None or (rule is parent.inherited and found is not rule):
            # No line, or a deeper `on` capped: the `read` folder stays the ceiling's place.
            inherited, inherited_at = parent.inherited, parent.inherited_at
        else:
            inherited, inherited_at = rule, folder
        return _Frame(folder, self._layers(folder, parent.layers), None, "", inherited, inherited_at)

    def entry(self, parent: _Frame, path: str, is_dir: bool) -> Verdict:
        """The verdict on `path`, an entry directly inside `parent.folder`."""
        if parent.closed is not None:
            return Verdict(True, parent.closed, parent.closed_at, OFF)
        rule = _ceiling(_decide(path, is_dir, parent.layers), parent)
        if rule is not None:
            return _verdict(rule, path)
        if parent.inherited is not None:
            return _verdict(parent.inherited, parent.inherited_at)
        return NOT_EXCLUDED

    def _layers(self, folder: str, layers: tuple) -> tuple:
        if folder in self.skip:
            return layers
        loaded = _load(folder, self.ttl)
        if loaded is None:
            return layers
        for message in loaded.warnings:
            _warn(message)
        rules = loaded.rules if self.legacy else tuple(r for r in loaded.rules if not r.legacy)
        return layers + ((folder, rules),) if rules else layers

    def one(self, stack: list, path: str, is_dir: bool) -> Verdict:
        """The verdict on `path`, reusing the frames already on `stack` for the
        folders it shares with the last path, and leaving its own there."""
        chain = _parts(path)
        if len(chain) < 2:
            return NOT_EXCLUDED
        folders = chain[:-1]
        keep = 0
        while keep < len(stack) and keep < len(folders) and stack[keep].folder == folders[keep]:
            keep += 1
        del stack[keep:]
        while len(stack) < len(folders):
            folder = folders[len(stack)]
            stack.append(self.root(folder) if not stack else self.child(stack[-1], folder))
        return self.entry(stack[-1], path, is_dir)


def _ceiling(rule: Rule | None, parent: _Frame) -> Rule | None:
    """A `read` or `hash` folder is a ceiling for the files inside it: a deeper
    `.probe.config` (one in that folder or below it) may narrow it to `off` but
    never set another level (`on`, or `hash` under `read` and `read` under
    `hash`, each of which lets something see more). Lines of the file that set
    the level may (`notebooks/ @probe read` then `notebooks/public.md @probe on`).
    Such a line from a deeper file is replaced by the rule it would override."""
    held = parent.inherited
    if rule is None or held is None or held.level not in _CEILINGS or rule.level in (OFF, held.level):
        return rule
    if rule.base != held.base and (rule.base == parent.inherited_at or _is_strict_ancestor(parent.inherited_at, rule.base)):
        return held
    return rule


def _check_one(path: str, is_dir: bool, skip: frozenset, legacy: bool, ttl: float = 0.0) -> Verdict:
    return _Walk(skip, legacy, ttl).one([], path, is_dir)


def check(
    path: str | os.PathLike,
    *,
    is_dir: bool | None = None,
    cwd: str | None = None,
    skip: "frozenset[str] | set[str] | None" = None,
    legacy: bool = False,
    ttl: float = 0.0,
    resolve: bool = True,
) -> Verdict:
    """Is `path` excluded by a `.probe.config`?

    `is_dir` None asks the disk (a missing path counts as a file). A path that
    goes through a symlink is checked as written AND as resolved (resolved
    BEFORE `..` collapses, so `link/../x` is the file the OS would open):
    excluded if either is. `skip`: folders whose files are set aside (the files
    above a session's launch folder the researcher answered `ignore` for, and
    only those). `legacy`: retired folder defaults count (agent sessions only).
    `resolve=False`: the caller already checks the resolved path itself (the
    SDK's write capture, which resolves every path once). Never raises."""
    try:
        raw = os.fspath(path)
        if raw.startswith("~"):
            raw = os.path.expanduser(raw)
        if not os.path.isabs(raw):
            raw = os.path.join(cwd or os.getcwd(), raw)
        full = os.path.normpath(raw)
        if is_dir is None:
            is_dir = os.path.isdir(full)
        skipped = frozenset(skip or ())
        verdict = _check_one(full, is_dir, skipped, legacy, ttl)
    except Exception:  # noqa: BLE001 - a check never breaks the caller, and fails closed
        return CHECK_FAILED
    if verdict.hidden or not resolve:
        return verdict
    try:
        real = _real(raw, ttl)
        if real != full:
            return stricter(verdict, _check_one(real, is_dir, skipped, legacy, ttl))
    except Exception:  # noqa: BLE001 - the path as given still decides
        pass
    return verdict


class Checker:
    """Many checks in a row, the way git checks them (`dir.c` `prep_exclude`):
    the folders of the last path stay on a stack, so the next path in the same
    folder costs one match instead of a walk to `/`. The answers are `check`'s
    exactly. It keeps nothing beyond itself: make one per batch (one snapshot,
    one walk, one tool output) and drop it."""

    def __init__(
        self,
        *,
        cwd: str | None = None,
        skip: "frozenset[str] | set[str] | None" = None,
        legacy: bool = False,
        ttl: float = 0.0,
        resolve: bool = True,
        daemon: bool = False,
    ) -> None:
        self.cwd = cwd
        self.resolve = resolve
        #: Answer as the daemon applies them (`daemon_view`: `hash` is `off`).
        self.daemon = daemon
        self._walk = _Walk(frozenset(skip or ()), legacy, ttl)
        self._given: list = []
        self._real: list = []
        #: Each folder's real path, once per batch (the folders of a batch repeat).
        self._real_dirs: dict[str, str] = {}

    def _resolved(self, raw: str) -> str:
        """`os.path.realpath(raw)`, with each folder's real path worked out once."""
        if ".." in raw.split(os.sep):
            return os.path.realpath(raw)
        folder, name = os.path.split(os.path.normpath(raw))
        real_dir = self._real_dirs.get(folder)
        if real_dir is None:
            if len(self._real_dirs) >= _CACHE_MAX:
                self._real_dirs.clear()
            real_dir = self._real_dirs[folder] = os.path.realpath(folder)
        joined = os.path.join(real_dir, name)
        return os.path.realpath(joined) if os.path.islink(joined) else joined

    def check(self, path: str | os.PathLike, *, is_dir: bool | None = None) -> Verdict:
        verdict = self._check(path, is_dir=is_dir)
        return daemon_view(verdict) if self.daemon else verdict

    def _check(self, path: str | os.PathLike, *, is_dir: bool | None = None) -> Verdict:
        try:
            raw = os.fspath(path)
            if raw.startswith("~"):
                raw = os.path.expanduser(raw)
            if not os.path.isabs(raw):
                raw = os.path.join(self.cwd or os.getcwd(), raw)
            full = os.path.normpath(raw)
            if is_dir is None:
                is_dir = os.path.isdir(full)
            verdict = self._walk.one(self._given, full, is_dir)
        except Exception:  # noqa: BLE001 - a check never breaks the caller, and fails closed
            return CHECK_FAILED
        if verdict.hidden or not self.resolve:
            return verdict
        try:
            real = self._resolved(raw)
            if real != full:
                return stricter(verdict, self._walk.one(self._real, real, is_dir))
        except Exception:  # noqa: BLE001 - the path as given still decides
            pass
        return verdict

    def closed(self, folder: str | os.PathLike) -> bool:
        """For a walk: is `folder` closed (`off`), so it is not entered at all?"""
        return self.check(folder, is_dir=True).hidden


_REAL_DIRS: dict[str, tuple[float, str]] = {}


def _real(full: str, ttl: float) -> str:
    """`os.path.realpath(full)`; on a hot path (`ttl` > 0) the folder's real path
    comes from a per-folder cache and only the last component is checked."""
    if ttl <= 0 or ".." in full.split(os.sep):
        return os.path.realpath(full)
    folder, name = os.path.split(full)
    now = time.monotonic()
    hit = _REAL_DIRS.get(folder)
    if hit is None or now - hit[0] >= ttl:
        if len(_REAL_DIRS) >= _CACHE_MAX:
            _REAL_DIRS.clear()
        hit = (now, os.path.realpath(folder))
        _REAL_DIRS[folder] = hit
    joined = os.path.join(hit[1], name)
    return os.path.realpath(joined) if os.path.islink(joined) else joined


def _concrete(tokens: tuple) -> str | None:
    """One name a segment glob matches (`*` and `?` as `x`), or None."""
    out = []
    for token in tokens:
        kind = token[0]
        if kind == "lit":
            out.append(token[1])
        elif kind in ("one", "star"):
            out.append("x")
        else:
            for ch in "xya0_Z9":
                if _token_eq(token, ch):
                    out.append(ch)
                    break
            else:
                for item in token[2]:
                    if item[0] != "cls" and _token_eq(token, item[0]):
                        out.append(item[0])
                        break
                else:
                    return None
    name = "".join(out)
    return name if name and "/" not in name else None


def _witness(rule: Rule, rel_full: tuple[str, ...]) -> list[str] | None:
    """Segments, relative to `full`, of one path INSIDE it that `rule`'s pattern
    matches, or None when the pattern can only match `full`'s ancestors or
    places beside it."""
    if not rule.anchored:
        name = _concrete(rule.segments[0])
        return [name] if name else None
    segs = rule.segments
    k = len(rel_full)

    @functools.lru_cache(maxsize=None)
    def rec(i: int, j: int) -> list[str] | None:
        if j == k:
            rest: list[str] = []
            for t in range(i, len(segs)):
                seg = segs[t]
                if seg == _GLOBSTAR:
                    if t == len(segs) - 1:
                        rest.append("x")
                    continue
                name = _concrete(seg)
                if name is None:
                    return None
                rest.append(name)
            return rest or ["x"]  # the pattern names `full` itself: try an entry in it
        if i == len(segs):
            return None
        seg = segs[i]
        if seg == _GLOBSTAR:
            return rec(i + 1, j) or rec(i, j + 1)
        return rec(i + 1, j + 1) if _match_segment(seg, rel_full[j]) else None

    found = rec(0, 0)
    return list(found) if found is not None else None


def _looser_inside(full: str, than: Verdict, skip: frozenset, legacy: bool, ttl: float) -> Verdict:
    """The least restrictive verdict some path INSIDE `full` actually gets, if
    looser than `than`. For each rule that sets a looser level (the folder's own
    file or one above), build one path inside `full` it matches and run the
    whole check on it: only a path that comes back looser proves it (order,
    depth and closed parents all count, as for any path)."""
    best = than
    for folder in _parts(full):
        if folder in skip:
            continue
        loaded = _load(folder, ttl)
        if loaded is None:
            continue
        rel = _rel(full, folder)
        for rule in loaded.rules:
            if _RANK[rule.level] >= _RANK[best.level] or (rule.legacy and not legacy):
                continue
            inside = _witness(rule, rel)
            if not inside:
                continue
            path = os.path.join(full, *inside)
            as_dir = rule.dir_only
            found = _check_one(path, as_dir, skip, legacy, ttl)
            if as_dir and _RANK[found.level] < _RANK[best.level]:
                found = stricter(found, _check_one(os.path.join(path, "x"), False, skip, legacy, ttl))
            if _RANK[found.level] < _RANK[best.level]:
                best = found
                if best.level == ON:
                    return best
    return best


def check_cwd(folder: str | os.PathLike, **kw) -> Verdict:
    """Is work run IN `folder` excluded? The folder itself is, or every entry in
    it would be (its own `*`, or a parent's `repo-b/**`). The level is the
    loosest any entry gets: an event in the folder may be about any of them."""
    verdict = check(folder, is_dir=True, **kw)
    if verdict.excluded:
        return verdict
    try:
        full = _norm(folder, kw.get("cwd"))
        skipped = frozenset(kw.get("skip") or ())
        legacy = bool(kw.get("legacy", False))
        ttl = float(kw.get("ttl", 0.0))
        probe_names = ("\u2063" * 8, "\u2063" * 9 + ".x")
        loosest: Verdict | None = None
        for name in probe_names:
            for as_dir in (False, True):
                child = _check_one(os.path.join(full, name), as_dir, skipped, legacy, ttl)
                if not child.excluded:
                    return NOT_EXCLUDED
                if loosest is None or _RANK[child.level] < _RANK[loosest.level]:
                    loosest = child
        if loosest is None:
            return NOT_EXCLUDED
        found = _looser_inside(full, loosest, skipped, legacy, ttl)
        if not found.excluded:
            return NOT_EXCLUDED
        return Verdict(True, found.rule, full, found.level)
    except Exception:  # noqa: BLE001
        return NOT_EXCLUDED


def off_inside(
    folder: str | os.PathLike,
    *,
    skip: "frozenset[str] | set[str] | None" = None,
    legacy: bool = False,
    ttl: float = 0.0,
    budget_s: float = 1.0,
    max_entries: int = 1_000_000,
) -> bool:
    """Is `folder`, or anything below it, at `off` -- or `hash`, which the
    daemon treats as `off` (the daemon's question: its only caller)? For a
    command that reads a whole tree (`rg`, `find`, `grep -r`, `git diff`): its
    output cannot be trusted to name every file it read, so such a command is
    refused, or its event dropped, when this is True. Skips what a search skips by default
    (hidden folders, `SCAN_SKIP_DIRS`). Exact when it finishes; True (fail
    closed) when it cannot finish in `budget_s` or `max_entries`. Never raises.

    Cheap when nothing can apply: the per-file walk runs only when an `off`
    rule above (or in) `folder` could reach inside it, or a `.probe.config`
    sits below it."""
    try:
        full = _norm(folder)
        real = os.path.realpath(full)
        if real != full and _off_inside_one(real, skip, legacy, ttl, budget_s, max_entries):
            return True
        return _off_inside_one(full, skip, legacy, ttl, budget_s, max_entries)
    except Exception:  # noqa: BLE001 - fail closed
        return True


def _off_inside_one(full: str, skip, legacy: bool, ttl: float, budget_s: float, max_entries: int) -> bool:
    """`off_inside` for one spelling of the folder."""
    checker = Checker(skip=skip, legacy=legacy, ttl=ttl, daemon=True)
    if checker.check(full, is_dir=True).hidden:
        return True
    deadline = time.monotonic() + budget_s
    stack: list = []
    checker._walk.one(stack, os.path.join(full, "x"), False)
    frame = stack[-1] if stack else None
    reaches = frame is not None and any(
        rule.level in (OFF, HASH) and (legacy or not rule.legacy) and rule.could_reach(_rel(full, base))
        for base, rules in frame.layers
        for rule in rules
    )
    if not reaches:
        # Only a `.probe.config` below `folder` could set something inside it.
        pending, seen = [full], 0
        while pending and not reaches:
            current = pending.pop()
            try:
                with os.scandir(current) as it:
                    for entry in it:
                        seen += 1
                        if seen > max_entries or time.monotonic() > deadline:
                            return True
                        if current != full and (
                            entry.name == CONFIG_NAME
                            or (legacy and entry.name == LEGACY_DIRNAME and legacy_default(current) in ("off", "read-only"))
                        ):
                            reaches = True
                            break
                        if entry.name in SCAN_SKIP_DIRS:  # where nobody keeps a `.probe.config`
                            continue
                        try:
                            if entry.is_dir(follow_symlinks=False):
                                pending.append(entry.path)
                        except OSError:
                            continue
            except OSError:
                continue
        if not reaches:
            return False
    pending, seen = [full], 0
    while pending:
        current = pending.pop()
        try:
            with os.scandir(current) as it:
                for entry in it:
                    seen += 1
                    if seen > max_entries or time.monotonic() > deadline:
                        return True
                    if entry.name == ".git":  # objects, never a file's name or text
                        continue
                    try:
                        is_dir = entry.is_dir(follow_symlinks=False)
                    except OSError:
                        continue
                    if checker.check(entry.path, is_dir=is_dir).hidden:
                        return True
                    if is_dir:
                        pending.append(entry.path)
        except OSError:
            continue
    return False


