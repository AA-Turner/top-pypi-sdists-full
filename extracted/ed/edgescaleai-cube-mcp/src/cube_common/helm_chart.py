"""Pure Python Helm chart parsing, version bumping, and packaging.

Eliminates the need for the helm CLI for chart operations.
Uses only stdlib (re, tarfile, io, os) — no external dependencies.
"""

from __future__ import annotations

import io
import os
import re
import tarfile
from pathlib import Path


class ChartError(Exception):
    """Raised when a chart operation fails."""


def find_chart_yaml(path: str | None = None) -> str:
    """Find Chart.yaml. Returns absolute path.

    Search order:
    1. If path specified, use it directly (file or directory)
    2. ./Chart.yaml
    3. ./charts/*/Chart.yaml (if exactly one)
    """
    if path:
        p = Path(path)
        if p.is_file() and p.name == "Chart.yaml":
            return str(p.resolve())
        chart_yaml = p / "Chart.yaml"
        if chart_yaml.is_file():
            return str(chart_yaml.resolve())
        raise ChartError(f"Chart.yaml not found at: {path}")

    cwd = Path.cwd()
    if (cwd / "Chart.yaml").is_file():
        return str((cwd / "Chart.yaml").resolve())

    charts = list(cwd.glob("charts/*/Chart.yaml"))
    if len(charts) == 1:
        return str(charts[0].resolve())
    if len(charts) > 1:
        names = [str(c.parent.name) for c in charts]
        raise ChartError(f"Multiple charts found: {', '.join(names)}. Please specify which one.")

    raise ChartError("No Chart.yaml found. Run from a chart directory or specify the path.")


def parse_chart(chart_yaml: str) -> dict:
    """Parse Chart.yaml and return dict with name, version, appVersion, dir, path."""
    try:
        content = Path(chart_yaml).read_text()
    except OSError as e:
        raise ChartError(f"Cannot read {chart_yaml}: {e}")

    name_match = re.search(r"^name:\s*(.+)$", content, re.MULTILINE)
    version_match = re.search(r"^version:\s*(.+)$", content, re.MULTILINE)
    app_version_match = re.search(
        r'^appVersion:\s*["\']?([^"\']+)["\']?$', content, re.MULTILINE
    )

    if not name_match or not version_match:
        raise ChartError(f"Could not parse name/version from {chart_yaml}")

    return {
        "name": name_match.group(1).strip(),
        "version": version_match.group(1).strip(),
        "appVersion": app_version_match.group(1).strip() if app_version_match else None,
        "path": chart_yaml,
        "dir": str(Path(chart_yaml).parent),
    }


def bump_version(version: str, bump_type: str = "patch") -> str:
    """Bump a semver version string."""
    parts = version.split(".")
    if len(parts) != 3:
        return version

    major, minor, patch = int(parts[0]), int(parts[1]), int(parts[2])

    if bump_type == "major":
        return f"{major + 1}.0.0"
    elif bump_type == "minor":
        return f"{major}.{minor + 1}.0"
    else:
        return f"{major}.{minor}.{patch + 1}"


def update_chart_version(
    chart_yaml: str, new_version: str, new_app_version: str | None = None
) -> None:
    """Update version (and optionally appVersion) in Chart.yaml.

    A Chart.yaml with no appVersion line gets one appended. The result is
    re-read and checked, so a line the regexes cannot rewrite (a trailing
    comment, say) raises instead of leaving the chart pointing at the old
    image while the caller reports the new one.
    """
    try:
        original = content = Path(chart_yaml).read_text()
    except OSError as e:
        raise ChartError(f"Cannot read {chart_yaml}: {e}")

    content = re.sub(
        r"^(version:\s*).+$",
        rf"\g<1>{new_version}",
        content,
        flags=re.MULTILINE,
    )

    if new_app_version:
        content, replaced = re.subn(
            r"""^(appVersion:\s*)["\']?[^"\']+["\']?$""",
            rf'\g<1>"{new_app_version}"',
            content,
            flags=re.MULTILINE,
        )
        if not replaced and not re.search(r"^appVersion:", content, re.MULTILINE):
            content = content.rstrip("\n") + f'\nappVersion: "{new_app_version}"\n'

    Path(chart_yaml).write_text(content)

    written = parse_chart(chart_yaml)
    problem = None
    if written["version"] != new_version:
        problem = f"Could not set version to {new_version} in {chart_yaml}"
    elif new_app_version and written["appVersion"] != new_app_version:
        problem = (
            f"Could not set appVersion to {new_app_version} in {chart_yaml} "
            f"(it reads {written['appVersion']!r})"
        )
    if problem:
        Path(chart_yaml).write_text(original)
        raise ChartError(problem)


HELMIGNORE = ".helmignore"

# Helm always appends this rule after the chart's own (`Rules.AddDefaults`).
_HELM_DEFAULT_IGNORE_RULES = ("templates/.?*",)


class _IgnoreRule:
    """One `.helmignore` line, parsed the way Helm's `pkg/ignore` parses it."""

    def __init__(self, raw: str) -> None:
        self.raw = raw
        rule = raw
        self.negate = rule.startswith("!")
        if self.negate:
            rule = rule[1:]
        self.must_dir = rule.endswith("/")
        if self.must_dir:
            rule = rule[:-1]
        # A leading "/" anchors to the chart root; any "/" means a whole-path
        # match; no "/" means the pattern is tested against the basename only.
        self.basename_only = "/" not in rule
        self.regex = re.compile(_go_glob_to_regex(rule.lstrip("/"), raw))

    def matches(self, relpath: str) -> bool:
        target = relpath.rsplit("/", 1)[-1] if self.basename_only else relpath
        return self.regex.fullmatch(target) is not None


def _go_glob_to_regex(pattern: str, raw: str) -> str:
    """Translate a Go `filepath.Match` pattern (what Helm uses) to a regex.

    Not `fnmatch`: in Go, `*` and `?` never cross a `/`, and a class negates
    with `^`, not `!`.
    """

    def bad() -> ChartError:
        return ChartError(f"{HELMIGNORE}: invalid pattern {raw!r}")

    out: list[str] = []
    i, n = 0, len(pattern)
    while i < n:
        c = pattern[i]
        if c == "*":
            out.append("[^/]*")
        elif c == "?":
            out.append("[^/]")
        elif c == "\\":
            i += 1
            if i >= n:
                raise bad()
            out.append(re.escape(pattern[i]))
        elif c == "[":
            i += 1
            negated = i < n and pattern[i] == "^"
            if negated:
                i += 1
            ranges: list[str] = []
            count = 0
            while True:
                if i >= n:
                    raise bad()
                if pattern[i] == "]" and count > 0:
                    break
                lo, i = _class_char(pattern, i, bad)
                hi = lo
                if i < n and pattern[i] == "-":
                    hi, i = _class_char(pattern, i + 1, bad)
                count += 1
                if lo <= hi:  # Go accepts a reversed range; it just never matches.
                    ranges.append(re.escape(lo) if lo == hi else f"{re.escape(lo)}-{re.escape(hi)}")
            if ranges:
                out.append(f"[{'^' if negated else ''}{''.join(ranges)}]")
            else:
                out.append("[\\s\\S]" if negated else "(?!)")
        else:
            out.append(re.escape(c))
        i += 1
    return "".join(out)


def _class_char(pattern: str, i: int, bad) -> tuple[str, int]:
    """One (possibly escaped) character inside a `[...]` class, per Go's getEsc."""
    if i >= len(pattern) or pattern[i] in "-]":
        raise bad()
    if pattern[i] == "\\":
        i += 1
        if i >= len(pattern):
            raise bad()
    return pattern[i], i + 1


def load_helmignore(chart_dir: str) -> list[_IgnoreRule]:
    """Parse `<chart_dir>/.helmignore` (if any) plus Helm's default rule.

    Mirrors Helm v3 `pkg/ignore/rules.go`: blank lines and `#` comments are
    skipped, surrounding whitespace is trimmed, a UTF-8 BOM on the first line is
    dropped, and `**` is an error rather than a silent non-match.
    """
    lines: list[str] = []
    path = os.path.join(chart_dir, HELMIGNORE)
    if os.path.isfile(path):
        try:
            text = Path(path).read_text(encoding="utf-8-sig")
        except (OSError, UnicodeDecodeError) as e:
            raise ChartError(f"Cannot read {path}: {e}")
        lines = text.splitlines()

    rules: list[_IgnoreRule] = []
    for line in [*lines, *_HELM_DEFAULT_IGNORE_RULES]:
        rule = line.strip()
        if not rule or rule.startswith("#"):
            continue
        if "**" in rule:
            raise ChartError(
                f"{HELMIGNORE}: {rule!r} uses '**', which Helm does not support"
            )
        rules.append(_IgnoreRule(rule))
    return rules


def is_helm_ignored(relpath: str, is_dir: bool, rules: list[_IgnoreRule]) -> bool:
    """Whether Helm would leave `relpath` (chart-relative, `/`-separated) out.

    A line-for-line port of Helm's `Rules.Ignore`, INCLUDING its negation
    behaviour, which differs from .gitignore: a `!pattern` line does not
    re-include an earlier match — it ignores every path that does NOT match it.
    Copying that quirk is deliberate; the point is that this package holds
    exactly what `helm package` would, and `package_chart` refuses a result
    missing Chart.yaml, which is where the quirk usually bites.
    """
    for rule in rules:
        if rule.negate:
            if rule.must_dir and not is_dir:
                return True
            if not rule.matches(relpath):
                return True
            continue
        if rule.must_dir and not is_dir:
            continue
        if rule.matches(relpath):
            return True
    return False


# Chart directories whose contents Helm renders or installs; a file the rules
# drop from one of these changes what deploys, unlike a dropped build input.
_CHART_CONTENT_DIRS = ("templates/", "crds/", "charts/")
_MAX_NAMED_DROPS = 10


def _walk_chart(chart_dir: str, rules: list[_IgnoreRule] | None):
    """Yield `(abspath, relpath)` for each file the package would hold.

    With `rules=None`, nothing is ignored: every file on disk outside hidden
    directories and the top-level `.tgz`. One walk for both, so the warning
    below cannot disagree with what `package_chart` adds (a directory the rules
    prune takes every file under it, which a per-file check misses).
    """
    for root, dirs, files in os.walk(chart_dir):
        reldir = os.path.relpath(root, chart_dir)
        reldir = "" if reldir == "." else reldir.replace(os.sep, "/") + "/"

        dirs[:] = [
            d
            for d in dirs
            if not d.startswith(".")
            and not (rules is not None and is_helm_ignored(reldir + d, True, rules))
        ]

        for fname in files:
            # Skip the chart's OWN packaged output (a top-level <name>-<ver>.tgz),
            # but KEEP subchart dependency tarballs under charts/ (e.g.
            # charts/minio-17.0.19.tgz) — those must ship inside the package or
            # Helm fails to render with "missing in charts/ directory".
            if fname.endswith(".tgz") and not reldir:
                continue
            relpath = reldir + fname
            if rules is not None and is_helm_ignored(relpath, False, rules):
                continue
            yield os.path.join(root, fname), relpath


def helmignore_negation_warning(chart_dir: str) -> str | None:
    """A warning when the chart's `.helmignore` has a `!` line, else None.

    The quiet half of Helm's negation quirk: `!*.yaml`, written under gitignore
    semantics to mean "keep the YAML", keeps Chart.yaml (so `package_chart`'s
    guard passes) but prunes `templates/` itself, so no template ships and the
    rollout deploys nothing. Packaging still matches `helm package`; this only
    says so, and names the chart files (templates, CRDs, subcharts) left out.
    """
    rules = load_helmignore(chart_dir)
    negations = [r.raw for r in rules if r.negate]
    if not negations:
        return None
    kept = {rel for _, rel in _walk_chart(chart_dir, rules)}
    dropped = sorted(
        rel
        for _, rel in _walk_chart(chart_dir, None)
        if rel not in kept and rel.startswith(_CHART_CONTENT_DIRS)
    )
    message = (
        f"{HELMIGNORE} has '!' lines ({', '.join(negations)}). Helm reads '!pattern' "
        "as 'ignore every file that does NOT match it', not as a re-include."
    )
    if dropped:
        named = ", ".join(dropped[:_MAX_NAMED_DROPS])
        more = len(dropped) - _MAX_NAMED_DROPS
        message += (
            f" {len(dropped)} chart file(s) under templates/, crds/ or charts/ are "
            f"left out of the package: {named}" + (f", and {more} more." if more > 0 else ".")
        )
    return message


def package_chart(chart_dir: str, version: str | None = None) -> str:
    """Package a Helm chart directory into a .tgz archive.

    Returns the path to the created .tgz file. Pure Python — no helm CLI needed.
    Uses the same layout as `helm package`: {chart_name}-{version}.tgz
    containing {chart_name}/ as the top-level directory.

    Honors the chart's `.helmignore` as Helm does (see `is_helm_ignored`). That
    matters most when the chart directory is also the Docker build context:
    without it, build inputs such as a model bundle or a virtualenv ship inside
    the chart. Hidden directories are always skipped as well, which Helm does
    not do — kept from before `.helmignore` was honored, and it only ever makes
    the package smaller.
    """
    chart_yaml = os.path.join(chart_dir, "Chart.yaml")
    info = parse_chart(chart_yaml)
    chart_name = info["name"]
    chart_version = version or info["version"]
    rules = load_helmignore(chart_dir)

    tgz_name = f"{chart_name}-{chart_version}.tgz"
    tgz_path = os.path.join(chart_dir, tgz_name)

    has_chart_yaml = False
    try:
        with tarfile.open(tgz_path, "w:gz") as tar:
            for abspath, relpath in _walk_chart(chart_dir, rules):
                if relpath == "Chart.yaml":
                    has_chart_yaml = True
                # Archive name: chart_name/relative_path
                tar.add(abspath, arcname=f"{chart_name}/{relpath}")
    except BaseException:
        _remove_quietly(tgz_path)
        raise

    if not has_chart_yaml:
        _remove_quietly(tgz_path)
        raise ChartError(
            f"{HELMIGNORE} in {chart_dir} excludes Chart.yaml, so the package would "
            "not be a chart. Note that Helm treats a '!pattern' line as 'ignore "
            "everything that does not match', not as a re-include."
        )

    return tgz_path


def _remove_quietly(path: str) -> None:
    try:
        os.remove(path)
    except OSError:
        pass
