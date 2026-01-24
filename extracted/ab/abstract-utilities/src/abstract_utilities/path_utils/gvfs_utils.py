from pathlib import Path

def find_gvfs_sftp(host: str, user: str) -> Path | None:
    gvfs_root = Path("/run/user") / str(os.getuid()) / "gvfs"
    if not gvfs_root.exists():
        return None

    for p in gvfs_root.iterdir():
        if p.name.startswith(f"sftp:host={host},user={user}"):
            return p

    return None
def resolve_solcatcher_root() -> Path:
    gvfs = find_gvfs_sftp("192.168.0.100", "solcatcher")

    if not gvfs:
        raise RuntimeError(
            "GVFS SFTP mount not available. "
            "Open Nautilus → click the server first."
        )

    root = gvfs / "mnt/24T/ABSTRACT_ENDEAVORS"
    if not root.exists():
        raise RuntimeError("Solcatcher root missing inside GVFS mount")

    return root
def ensure_solcatcher_importable():
    root = resolve_solcatcher_root()
    src = root / "scripts/RABBIT/aggregator/src"

    if str(src) not in sys.path:
        sys.path.insert(0, str(src))
