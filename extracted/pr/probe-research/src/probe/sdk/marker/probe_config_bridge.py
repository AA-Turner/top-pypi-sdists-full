# ---------------------------------------------------------------------------
# `.probe.config`: paths Probe never records
# ---------------------------------------------------------------------------


#: The status-line segment while the parent question is open.
PARENT_STATUS_ASK = ".probe.config: ask"


def probe_config():
    """The `.probe.config` matcher: `probe.sdk.probe_config` in the SDK; beside
    the hooks (which cannot import `probe`), the vendored `_probe_config.py`,
    loaded by EXPLICIT path, never a bare import: sys.path can carry the user's
    project directory, and the status line runs this on every render."""
    try:
        from . import probe_config as module

        return module
    except ImportError:
        pass
    import importlib.util  # noqa: PLC0415
    import sys  # noqa: PLC0415

    key = "_probe_hooks._probe_config"
    module = sys.modules.get(key)
    if module is not None:
        return module
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_probe_config.py")
    spec = importlib.util.spec_from_file_location(key, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[key] = module
    try:
        spec.loader.exec_module(module)
    except BaseException:
        sys.modules.pop(key, None)
        raise
    return module


def parent_question_open(session_id: str) -> bool:
    """Was the parent question asked in this session and not answered yet? One
    small file read and nothing imported: the status line asks on every render."""
    if not valid_session_id(session_id):
        return False
    try:
        with open(sessions_dir() / (session_id + ".parent-config"), encoding="utf-8") as handle:
            data = json.load(handle)
    except (OSError, ValueError):
        return False
    return isinstance(data, dict) and "asked_at" in data and "decision" not in data


def record_launch_dir(session_id: str, cwd: str) -> bool:
    """Where a session started, written once at seed. Never raises."""
    if not valid_session_id(session_id) or not cwd:
        return False
    try:
        return probe_config().record_launch_dir(sessions_dir(), session_id, cwd)
    except Exception:  # noqa: BLE001
        return False


def parent_config_status(session_id: str) -> "tuple[str, list]":
    """`probe_config.parent_status` for this session; ("", []) when unknown."""
    if not valid_session_id(session_id):
        return "", []
    try:
        return probe_config().parent_status(sessions_dir(), session_id)
    except Exception:  # noqa: BLE001
        return "", []


def excluded(path, session_id: "str | None" = None, *, is_dir=None, cwd=None, as_cwd: bool = False):
    """`probe_config.session_check` for this session (all files apply without one)."""
    pc = probe_config()
    sid = session_id if session_id and valid_session_id(session_id) else None
    try:
        sessions = sessions_dir() if sid else None
    except Exception:  # noqa: BLE001
        sessions = None
    return pc.session_check(path, sessions, sid, is_dir=is_dir, cwd=cwd, as_cwd=as_cwd)


def verdict_source(verdict) -> str:
    """`~/code/.probe.config:1 (/*)`: where a verdict came from."""
    pc = probe_config()
    rule = getattr(verdict, "rule", None)
    if rule is None:
        return pc.CONFIG_NAME
    where = pc.shown(rule.source)
    return f"{where}:{rule.line} ({rule.pattern})" if rule.line else f"{where} ({rule.pattern})"


def parent_files_label(parents) -> str:
    """The files a parent question is about, as one message names them."""
    pc = probe_config()
    return ", ".join(pc.shown(p.path) for p in parents)


def excluded_context(session_id: str, cwd: "str | None") -> "str | None":
    """`EXCLUDED_CONTEXT` for a session starting in `cwd`: the `.probe.config`
    paths that reach it, as one line, or None. Files above the launch folder are
    left out once the researcher set them aside. Never raises."""
    try:
        pc = probe_config()
        start = pc.launch_dir(sessions_dir(), session_id) if valid_session_id(session_id) else None
        if not (start or cwd):
            return None
        _start, skip = pc.session_view(sessions_dir(), session_id) if valid_session_id(session_id) else (None, frozenset())
        summary = pc.summarize(start or cwd, skip=skip, legacy=True)
    except Exception:  # noqa: BLE001
        return None
    if not summary.entries:
        return None
    return EXCLUDED_CONTEXT.format(paths=", ".join(summary.entries) + (", and more" if summary.truncated else ""))


def take_parent_ask(session_id: str, statuses: "tuple[str, ...] | None" = None) -> "str | None":
    """`PARENT_ASK` when a file above the launch folder reaches this session and
    its status is one of `statuses` (default: not asked yet), marking it asked.
    The caller must deliver it. Never raises."""
    try:
        pc = probe_config()
        wanted = statuses or (pc.UNASKED,)
        status, parents = parent_config_status(session_id)
        if status not in wanted or not parents:
            return None
        pc.mark_asked(sessions_dir(), session_id, parents)
        return PARENT_ASK.format(files=parent_files_label(parents))
    except Exception:  # noqa: BLE001
        return None
