"""Shared pull request title helpers for the AI PR pipeline."""


def is_wip_title(title: str) -> bool:
    """Return True when a PR title is marked work-in-progress."""
    return title.upper().startswith("[WIP]")


def wip_normalized_title(title: str) -> str:
    """Return the title text remaining after stripping a ``[WIP]`` prefix.

    Returns an empty string both when ``title`` is not a WIP title and when
    the ``[WIP]`` prefix has no title text left to preserve (e.g. ``"[WIP]"``
    or ``"[WIP]   "``). Callers use this to detect a WIP title that cannot be
    published, because the prefix is all there is.
    """
    if not is_wip_title(title):
        return ""
    return title[5:].strip()
