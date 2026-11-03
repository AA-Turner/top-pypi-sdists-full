# ---------------------------------------------------------------------------
# Files
# ---------------------------------------------------------------------------


@dataclass
class _Loaded:
    key: tuple
    rules: tuple
    warnings: tuple
    digest: str


_CACHE: dict[str, _Loaded] = {}
_CACHE_MAX = 4096
_WARNED: set[str] = set()
#: When each folder was last stat'ed (monotonic), for callers that accept a
#: slightly stale answer on a hot path (`ttl`): the SDK's capture asks on every
#: file it walks and every read it records.
_CHECKED: dict[str, float] = {}
#: One loader at a time: a reader in another thread must never see a folder
#: stamped as checked before its answer is cached (threaded data loaders).
_LOCK = threading.RLock()


def _after_fork_in_child() -> None:
    global _LOCK
    _LOCK = threading.RLock()


if hasattr(os, "register_at_fork"):
    os.register_at_fork(after_in_child=_after_fork_in_child)


def _warn(message: str) -> None:
    """Once per message per process, to stderr. Never raises."""
    if message in _WARNED:
        return
    _WARNED.add(message)
    try:
        print(f"probe: {message}", file=sys.stderr)
    except Exception:  # noqa: BLE001 - a warning never breaks a check
        pass


#: stat errors that mean "there is no such file here" (absent), as opposed to
#: one that exists and cannot be read (fails closed): a path too long to hold
#: one, a component that is a file, a name the file system refuses.
_ABSENT_ERRNOS = frozenset(
    e for e in (errno.ENOENT, errno.ENOTDIR, errno.ENAMETOOLONG, errno.EINVAL, getattr(errno, "EILSEQ", None))
    if e is not None
)


def _stat_key(path: str) -> tuple | None:
    """None when no file is there (one `lstat`: the common case costs one
    syscall); a key that changes with the file otherwise. A dangling symlink
    (dotfiles on an unmounted share) is a file that cannot be read: it fails
    closed, never reads as absent."""
    try:
        st = os.lstat(path)
    except OSError as exc:
        return None if exc.errno in _ABSENT_ERRNOS else ("error", type(exc).__name__)
    except ValueError:  # an embedded NUL: no such file
        return None
    if stat.S_ISLNK(st.st_mode):
        try:
            st = os.stat(path)
        except OSError:
            return ("dangling",)
    return (st.st_mode, st.st_ino, st.st_size, st.st_mtime_ns)


def _read_text(path: str) -> str:
    flags = os.O_RDONLY | getattr(os, "O_NONBLOCK", 0) | getattr(os, "O_CLOEXEC", 0)
    fd = os.open(path, flags)
    try:
        info = os.fstat(fd)
        if not stat.S_ISREG(info.st_mode):
            raise OSError("not a regular file")
        if info.st_size > MAX_BYTES:
            raise OSError(f"over {MAX_BYTES} bytes")
        raw = b""
        while len(raw) <= MAX_BYTES:
            chunk = os.read(fd, 64 * 1024)
            if not chunk:
                break
            raw += chunk
        if len(raw) > MAX_BYTES:
            raise OSError(f"over {MAX_BYTES} bytes")
    finally:
        os.close(fd)
    if raw.startswith((b"\xff\xfe", b"\xfe\xff")):
        return raw.decode("utf-16")
    if b"\x00" in raw:
        raise OSError("holds NUL bytes (UTF-16 without a BOM?)")
    return raw.decode("utf-8-sig")


def legacy_default(folder: str) -> str | None:
    """The retired folder default in `<folder>/.probe/config.json`, as the stored
    word (`full` | `read-only` | `off`), or None when there is none or it is not
    one. Never raises."""
    path = os.path.join(folder, LEGACY_DIRNAME, LEGACY_FILENAME)
    try:
        if not os.path.isfile(path) or os.path.getsize(path) > 64 * 1024:
            return None
        with open(path, encoding="utf-8") as handle:
            data = json.load(handle)
    except (OSError, ValueError):
        return None
    defaults = data.get("defaults") if isinstance(data, dict) else None
    if not isinstance(defaults, dict):
        return None
    for key in ("session_state", "session_tracking"):
        value = defaults.get(key)
        if value is True:
            return "full"
        if value is False:
            return "off"
        if isinstance(value, str):
            word = value.strip().lower()
            if word in ("full", "on", "daemon"):
                return "full"
            if word in ("read-only", "read", "readonly"):
                return "read-only"
            if word == "off":
                return "off"
    return None


def _load(folder: str, ttl: float = 0.0) -> _Loaded | None:
    """The rules a folder contributes, cached by the file's stat. None when the
    folder holds neither a `.probe.config` nor a retired folder default.

    `ttl` > 0 reuses the last answer for a folder stat'ed less than `ttl`
    seconds ago, without touching the disk."""
    return _load_unlocked(folder, ttl)


def _load_unlocked(folder: str, ttl: float) -> _Loaded | None:
    if ttl > 0:
        last = _CHECKED.get(folder)
        if last is not None and time.monotonic() - last < ttl:
            return _CACHE.get(folder)
    checked_at = time.monotonic()
    path = os.path.join(folder, CONFIG_NAME)
    legacy_path = os.path.join(folder, LEGACY_DIRNAME, LEGACY_FILENAME)
    key = (_stat_key(path), _stat_key(legacy_path))
    if key == (None, None):
        with _LOCK:
            _CACHE.pop(folder, None)
            _stamp(folder, checked_at)
        return None
    hit = _CACHE.get(folder)
    if hit is not None and hit.key == key:
        _stamp(folder, checked_at)
        return hit
    rules: list[Rule] = []
    warnings: list[str] = []
    digest = hashlib.sha256()
    if key[1] is not None:
        legacy = legacy_default(folder)
        if legacy in ("off", "read-only"):
            word = "off" if legacy == "off" else "read"
            rules.append(_everything(folder, legacy_path, f"retired folder default `{word}`", legacy=True))
            digest.update(f"legacy:{legacy}".encode())
    if key[0] is not None:
        try:
            text = _read_text(path)
        except (OSError, UnicodeDecodeError) as exc:
            reason = str(exc) or type(exc).__name__
            warnings.append(
                f"`{path}` could not be read ({reason}), so everything under `{folder}` counts as excluded."
            )
            rules.append(_everything(folder, path, "unreadable"))
            digest.update(b"unreadable")
        else:
            digest.update(text.encode("utf-8", "surrogatepass"))
            default = OFF
            for number, raw in enumerate(text.splitlines(), start=1):
                word = setting_line(raw)
                if word is not None:
                    default = level_of(word) or OFF
                    if level_of(word) is None:
                        warnings.append(
                            f"`{path}:{number}`: `{word}` is not a level (on, read, hash, off), so the lines "
                            "after it count as `off`."
                        )
                    continue
                try:
                    rule, note = _parse(raw, folder, path, number, default)
                except _BadPattern:
                    warnings.append(f"`{path}:{number}` is not a valid pattern and was skipped.")
                    continue
                if note:
                    warnings.append(f"`{path}:{number}`: {note}")
                if rule is not None:
                    rules.append(rule)
    loaded = _Loaded(key=key, rules=tuple(rules), warnings=tuple(warnings), digest=digest.hexdigest())
    with _LOCK:
        if len(_CACHE) >= _CACHE_MAX:
            _CACHE.clear()
            _CHECKED.clear()
        _CACHE[folder] = loaded
        _stamp(folder, checked_at)
    return loaded


def _stamp(folder: str, at: float) -> None:
    """Mark a folder's answer fresh, AFTER it is cached."""
    if len(_CHECKED) >= _CACHE_MAX:
        _CHECKED.clear()
    _CHECKED[folder] = at


