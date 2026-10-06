"""The site settings of Pikobs, read from site.cfg next to this file.

    from pikobs.configobs.site import setting
    setting("PIKOBS_DOC_URL")

site.cfg is written for bash, one ``NAME="${NAME:-value}"`` per line, so
the scripts can ``source`` it; this module reads the same file. An
environment variable of the same name wins over the file, and ${NAME} in a
value stands for a setting above it or an environment variable.

    python -m pikobs.configobs.site            # every setting, as resolved
"""
import os
import re

CFG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "site.cfg")
_LINE = re.compile(r'^\s*([A-Z_][A-Z0-9_]*)="(.*)"\s*$')
_DEFAULT = re.compile(r'^\$\{([A-Z_][A-Z0-9_]*):-(.*)\}$')
_REF = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}|\$([A-Za-z_][A-Za-z0-9_]*)")


def _expand(text, known):
    def sub(m):
        name = m.group(1) or m.group(2)
        if name in known:
            return known[name]
        if name == "HOME":
            return os.path.expanduser("~")
        if name == "USER":
            return os.environ.get("USER") or os.environ.get("LOGNAME") or ""
        return os.environ.get(name, "")
    return _REF.sub(sub, text)


def settings(path=CFG):
    """Every setting of site.cfg, with the environment applied."""
    out = {}
    with open(path) as fh:
        for line in fh:
            m = _LINE.match(line)
            if not m:
                continue
            name, value = m.group(1), m.group(2)
            d = _DEFAULT.match(value)
            if d and d.group(1) == name:
                value = os.environ.get(name) or _expand(d.group(2), out)
            else:
                value = _expand(value, out)
            out[name] = value
    return out


def setting(name, default=None):
    """One setting; `default` only when site.cfg does not have it."""
    return settings().get(name, default)


if __name__ == "__main__":
    for k, v in settings().items():
        print(f"{k}={v}")
