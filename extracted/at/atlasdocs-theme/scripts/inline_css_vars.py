"""
inline_css_vars.py — resolve CSS custom properties and write extra.min.css

Collects all --variable definitions from :root and [data-md-color-scheme="default"]
blocks, resolves transitive references, then replaces every var(--name) and
var(--name, fallback) usage throughout the file. Variables that cannot be
resolved (e.g. Material theme vars not defined in extra.css) are left as-is
or replaced with their fallback value if one is provided.

Usage:
    python scripts/inline_css_vars.py
    python scripts/inline_css_vars.py path/to/extra.css path/to/extra.min.css
"""

import re
import sys
from pathlib import Path

# ── helpers ──────────────────────────────────────────────────────────────────

def extract_blocks(css):
    """Yield (selector, block_body) for each top-level rule block."""
    i = 0
    n = len(css)
    while i < n:
        # skip whitespace / comments between blocks
        m = re.search(r'[^\s]', css[i:])
        if m is None:
            break
        i += m.start()

        # find the opening brace
        brace = css.find('{', i)
        if brace == -1:
            break

        selector = css[i:brace].strip()
        depth = 1
        j = brace + 1
        while j < n and depth > 0:
            if css[j] == '{':
                depth += 1
            elif css[j] == '}':
                depth -= 1
            j += 1

        yield selector, css[brace + 1:j - 1]
        i = j


def collect_vars(css, target_selectors):
    """
    Return a dict of --name → value for declarations found in blocks whose
    selector matches any of target_selectors (checked with str.startswith after
    stripping).  Values have !important stripped.
    """
    var_re = re.compile(r'(--[\w-]+)\s*:\s*(.+?)(?:\s*!important)?\s*;', re.DOTALL)
    result = {}

    for selector, body in extract_blocks(css):
        sel = selector.strip()
        if any(sel == t or sel.startswith(t) for t in target_selectors):
            for m in var_re.finditer(body):
                name = m.group(1).strip()
                value = m.group(2).strip()
                result[name] = value

    return result


def resolve(vars_dict, max_passes=15):
    """
    Iteratively replace var(--x) references inside values with their resolved
    counterparts.  Stops when nothing changes or max_passes is reached.
    """
    var_ref_re = re.compile(r'var\((--[\w-]+)(?:\s*,\s*[^)]+)?\)')

    for _ in range(max_passes):
        changed = False
        new = {}
        for name, value in vars_dict.items():
            def sub(m):
                ref = m.group(1)
                if ref in vars_dict:
                    return vars_dict[ref]
                # keep original — unresolvable (e.g. Material theme vars)
                return m.group(0)
            resolved_value = var_ref_re.sub(sub, value)
            new[name] = resolved_value
            if resolved_value != value:
                changed = True
        vars_dict = new
        if not changed:
            break

    return vars_dict


def inline_vars(css, resolved):
    """
    Replace every var(--name) and var(--name, fallback) in css with the
    resolved value.  If --name is not in resolved, use the fallback if
    provided, otherwise leave the var() call intact.
    """
    def replacer(m):
        name = m.group(1)
        fallback = m.group(2)  # may be None
        if name in resolved:
            return resolved[name]
        if fallback is not None:
            return fallback.strip()
        return m.group(0)   # unresolvable, no fallback — keep as-is

    # Match var(--name) and var(--name, fallback)
    # Fallback may itself contain nested var() — handle one level deep
    pattern = re.compile(
        r'var\(\s*(--[\w-]+)\s*(?:,\s*((?:[^()]*|\([^()]*\))*))?\)',
        re.DOTALL,
    )
    return pattern.sub(replacer, css)


# ── main ─────────────────────────────────────────────────────────────────────

def main():
    here = Path(__file__).parent
    default_src = here.parent / 'atlasdocs_theme' / 'assets' / 'stylesheets' / 'extra.css'
    default_dst = default_src.parent / 'extra.min.css'

    src = Path(sys.argv[1]) if len(sys.argv) > 1 else default_src
    dst = Path(sys.argv[2]) if len(sys.argv) > 2 else default_dst

    css = src.read_text(encoding='utf-8')

    # Collect from :root (all instances) and the default light-mode block.
    # Dark-mode (slate) overrides are intentionally excluded so we get the
    # light-mode values as the canonical resolved set.
    target_selectors = [
        ':root',
        '[data-md-color-scheme="default"]',
    ]
    raw_vars = collect_vars(css, target_selectors)
    print(f'  collected {len(raw_vars)} variable definitions')

    resolved = resolve(raw_vars)
    still_unresolved = sum(1 for v in resolved.values() if 'var(--' in v)
    print(f'  {still_unresolved} variable(s) still reference unresolvable external vars')

    result = inline_vars(css, resolved)

    dst.write_text(result, encoding='utf-8')
    print(f'  wrote {dst}  ({dst.stat().st_size:,} bytes)')


if __name__ == '__main__':
    main()
