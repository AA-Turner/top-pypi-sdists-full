"""Canonical origin-to-system-path routing for app-captured files."""

from __future__ import annotations

from .system_paths import SystemFolder, get_system_folder


SYSTEM_ORIGIN_FOLDERS: dict[str, str] = {
    "transcripts": "transcript_recordings",
}


def system_folder_for_origin(origin: str | None) -> SystemFolder | None:
    """Return the registered hidden folder for a recognized upload origin."""
    if not origin:
        return None
    name = SYSTEM_ORIGIN_FOLDERS.get(str(origin).strip().lower())
    return get_system_folder(name) if name else None


def relocate_under_system_origin(clean_path: str, origin: str | None) -> str:
    """Relocate app-captured content beneath its registered system root."""
    folder = system_folder_for_origin(origin)
    if folder is None:
        return clean_path
    segments = [segment for segment in clean_path.split("/") if segment]
    tail = segments[1:] if len(segments) > 1 else segments
    return folder.path(*tail)


__all__ = [
    "SYSTEM_ORIGIN_FOLDERS",
    "system_folder_for_origin",
    "relocate_under_system_origin",
]
