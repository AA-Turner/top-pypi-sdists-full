from __future__ import annotations
import sys


def dispatch(args: list[str]) -> dict:
    if args and args[0] == "record":
        return _record(args[1:])
    return _list()


def _list() -> dict:
    from kanban_framework.cli.main import _get_version
    return {
        "version": _get_version(),
        "python": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        "platform": sys.platform,
    }


def _record(args: list[str]) -> dict:
    if not args:
        return {"error": "version required"}
    version = args[0]
    title = ""
    task_id = ""
    i = 1
    while i < len(args):
        if args[i] == "--title" and i + 1 < len(args):
            title = args[i + 1]
            i += 2
        elif args[i] == "--task" and i + 1 < len(args):
            task_id = args[i + 1]
            i += 2
        else:
            i += 1

    from kanban_framework.infra.filesystem import Filesystem
    fs = Filesystem(Filesystem.find_project_root())
    # Write to framework source versions/, not user's .kanban/versions/
    versions_dir = fs.kanban_dir / "versions"
    if versions_dir.is_symlink():
        versions_dir = versions_dir.resolve()
    if not versions_dir.is_dir():
        # Fallback: locate versions/ from the installed package
        import kanban_framework as _kf
        pkg_versions = _kf.__path__[0].replace("/kanban_framework", "/versions")
        pkg_versions_path = __import__("pathlib").Path(pkg_versions)
        if pkg_versions_path.is_dir():
            versions_dir = pkg_versions_path
        else:
            versions_dir.mkdir(parents=True, exist_ok=True)

    if not version.startswith("v"):
        version = f"v{version}"

    content_parts = [f"# {version}\n"]
    if title:
        content_parts.append(f"\n## {title}\n")
    if task_id:
        content_parts.append(f"\nTask: {task_id}\n")
    content_parts.append("\n")
    (versions_dir / f"{version}.md").write_text(
        "".join(content_parts), encoding="utf-8"
    )
    return {"version": version, "recorded": True}
