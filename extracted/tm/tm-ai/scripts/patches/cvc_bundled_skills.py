#!/usr/bin/env python3
"""
CVC override patch: agent/skill_utils.py
========================================

Injects the bundled_skills tree lookup at the end of
`get_external_skills_dirs()`. The CVC wheel ships `<cvc>/bundled_skills/`
and ships it on every install — this injection makes sure those skills
are always visible to the runtime, regardless of any other config.

What this replaces:
  The previous override pattern wholesale-replaced skill_utils.py with
  a CVC-modified copy. When the ref added new functions (like
  `is_skill_support_path`) or changed other parts of the file, our
  override silently removed them, breaking imports in other modules.

  This patch is surgical: it adds the bundled_skills block near the
  end of `get_external_skills_dirs()` and leaves the rest of the file
  exactly as the ref ships it.

Anchor:
  Ref's `get_external_skills_dirs()` ends with the cache_key writeback
  block:
      if cache_key is not None:
          _EXTERNAL_DIRS_CACHE[cache_key] = list(result)
      return result

  We insert the bundled_skills block immediately before the cache writeback.

Format: a function that takes the ref's file contents and returns the
patched contents. No imports from the file itself — pure text surgery.
"""
from __future__ import annotations


INJECTION_BLOCK = '''
    # ── CVC bundled skill tree (always available — ships with the wheel) ──
    # The vendored runtime resolves its package root via __file__, so this
    # works in both editable and wheel installs:
    #   /.../cvc/agent/_vendor/hermes/agent/skill_utils.py
    #   → /.../cvc/agent/_vendor/hermes/agent
    #   → /.../cvc/agent/_vendor/hermes
    #   → /.../cvc/agent/_vendor
    #   → /.../cvc/agent
    #   → /.../cvc                       ← bundled_skills lives here
    try:
        # skill_utils.py sits at .../cvc/agent/_vendor/hermes/agent/
        # Walk up to find a directory that contains a `bundled_skills/` child.
        bundled = None
        cur = Path(__file__).resolve().parent
        for _ in range(8):  # bound the walk
            candidate = cur / "bundled_skills"
            if candidate.is_dir():
                bundled = candidate
                break
            cur = cur.parent
        if bundled is not None and bundled not in seen:
            seen.add(bundled)
            result.insert(0, bundled)  # bundled wins on name collision
    except Exception as e:
        logger.debug("bundled_skills discovery failed: %s", e)

'''

# Anchor: the cache writeback — present in every ref version we've seen.
# We insert immediately before this block, so the cache writeback still
# captures the final `result` list (which now includes the bundled dir).
ANCHOR = """    if cache_key is not None:
        _EXTERNAL_DIRS_CACHE[cache_key] = list(result)
    return result"""


def apply(content: str) -> str:
    """Insert the bundled_skills lookup into get_external_skills_dirs().

    Idempotent: if the bundled_skills block is already there, the file
    is returned unchanged. If the anchor is missing (refactor changed the
    function shape), raise — this is a hard break we want to catch.
    """
    if "bundled_skills discovery failed" in content:
        return content
    if ANCHOR not in content:
        raise RuntimeError(
            "CVC patch anchor not found in agent/skill_utils.py — "
            "ref changed get_external_skills_dirs() shape. Update "
            "scripts/patches/cvc_bundled_skills.py to match."
        )
    return content.replace(ANCHOR, INJECTION_BLOCK + ANCHOR)


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("usage: cvc_bundled_skills.py <path-to-skill_utils.py>")
        sys.exit(1)
    path = sys.argv[1]
    with open(path) as f:
        before = f.read()
    after = apply(before)
    if after == before:
        print(f"already patched: {path}")
    else:
        with open(path, "w") as f:
            f.write(after)
        print(f"patched: {path} (+{len(after) - len(before)} bytes)")
