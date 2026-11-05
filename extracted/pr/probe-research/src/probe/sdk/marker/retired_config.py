# ---------------------------------------------------------------------------
# `.probe.config`, removed 2026-11-04: one notice when an old file is found
# ---------------------------------------------------------------------------
#
# Probe no longer reads the file. A researcher who wrote one still believes those
# folders are kept out, so a session that starts under one says once that they are
# recorded (T3, 2026-11-04). Looked for by name only, never parsed.

#: The researcher's line (T3, Richard 2026-11-04).
RETIRED_CONFIG_NOTICE = (
    "Probe no longer reads .probe.config (removed 2026-11-04): folders it marked off are recorded."
)
RETIRED_CONFIG_NAME = ".probe.config"
#: Folders walked up from the launch folder, at most.
RETIRED_CONFIG_MAX_DEPTH = 64


def find_retired_config(cwd: "str | None") -> "str | None":
    """The first `.probe.config` in `cwd` or a folder above it, else `~/.probe.config`; None when
    there is none. One lstat per folder. Never raises."""
    candidates = []
    try:
        folder = os.path.abspath(cwd) if cwd else ""
        for _ in range(RETIRED_CONFIG_MAX_DEPTH if folder else 0):
            candidates.append(os.path.join(folder, RETIRED_CONFIG_NAME))
            parent = os.path.dirname(folder)
            if parent == folder:
                break
            folder = parent
        candidates.append(os.path.join(os.path.expanduser("~"), RETIRED_CONFIG_NAME))
    except Exception:  # noqa: BLE001
        return None
    for path in candidates:
        try:
            os.lstat(path)
        except OSError:
            continue
        return path
    return None


def take_retired_config_notice(session_id: str, cwd: "str | None") -> "str | None":
    """`RETIRED_CONFIG_NOTICE` the first time a session starts under a `.probe.config`, else
    None; a resume or a compaction asks again and gets None. The caller must deliver it.
    Never raises."""
    if not valid_session_id(session_id) or find_retired_config(cwd) is None:
        return None
    try:
        sessions = sessions_dir()
        sessions.mkdir(parents=True, exist_ok=True)
        os.close(os.open(str(sessions / (session_id + ".config-notice")), os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600))
    except OSError:
        return None
    return RETIRED_CONFIG_NOTICE
