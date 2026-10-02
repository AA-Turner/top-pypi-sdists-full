"""mirror-public.yml's push trigger must cover everything the render reads.

Same contract as test_deploy_scope.py, same failure it prevents: the workflow's
`on.push.paths` hand-lists the mirror surface, and mirror_render.py's
RENDER_ITEMS is the surface's actual definition. Add a render item without
widening the trigger and human-merged changes to that file silently stop
auto-syncing to the public repo — delivered only by the next release or a
manual dispatch someone has to remember.
"""

from __future__ import annotations

import fnmatch
import importlib.util
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
_WORKFLOW = _ROOT.parent / ".github" / "workflows" / "mirror-public.yml"
_PREFIX = "agent/"

spec = importlib.util.spec_from_file_location("mirror_render", _ROOT / "tools" / "mirror_render.py")
mirror_render = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mirror_render)


def _workflow_push_paths() -> list[str]:
    """The `on.push.paths` globs, read without a YAML dependency (the block is
    a flat list of quoted strings — same tiny reader as test_deploy_scope)."""
    paths: list[str] = []
    inside = False
    for line in _WORKFLOW.read_text().splitlines():
        stripped = line.strip()
        if stripped == "paths:":
            inside = True
            continue
        if not inside:
            continue
        if stripped.startswith("- "):
            item = stripped[2:].strip()
            if item.startswith(("'", '"')):
                quote = item[0]
                end = item.find(quote, 1)
                item = item[1:end] if end > 0 else item.strip(quote)
            else:
                item = item.split("#", 1)[0].strip()
            if item:
                paths.append(item)
        elif stripped and not stripped.startswith("#"):
            break
    return paths


def _covered(file: str, globs: list[str]) -> bool:
    for glob in globs:
        if glob.endswith("/**"):
            if file.startswith(glob[:-2]):
                return True
        elif fnmatch.fnmatch(file, glob) or file == glob:
            return True
    return False


def test_workflow_declares_push_paths():
    paths = _workflow_push_paths()
    assert paths, f"no on.push.paths found in {_WORKFLOW.name}"


def test_push_trigger_covers_every_render_item():
    globs = _workflow_push_paths()
    uncovered = sorted(
        rel for rel, _dest in mirror_render.RENDER_ITEMS if not _covered(_PREFIX + rel, globs)
    )
    assert not uncovered, (
        f"{len(uncovered)} render item(s) are NOT in mirror-public.yml's push "
        "paths, so human-merged changes to them would never auto-mirror:\n  "
        + "\n  ".join(uncovered)
        + "\n\nAdd them to on.push.paths (or drop them from RENDER_ITEMS)."
    )


def test_push_trigger_covers_the_renderer_itself():
    globs = _workflow_push_paths()
    assert _covered(f"{_PREFIX}tools/mirror_render.py", globs), (
        "a change to the renderer must re-sync the mirror"
    )
