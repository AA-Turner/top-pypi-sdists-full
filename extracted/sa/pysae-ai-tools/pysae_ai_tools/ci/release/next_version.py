"""Compute the next semver version for a GitLab project.

Usage:
    pysae-ai-tools ci_release next_version [--project-id ID] [--bump major|minor|patch]
        [--version v1.2.3] [--prerelease beta]

Examples:
    pysae-ai-tools ci_release next_version                          # patch bump from latest tag
    pysae-ai-tools ci_release next_version --bump minor             # minor bump
    pysae-ai-tools ci_release next_version --version v2.0.0         # explicit version
    pysae-ai-tools ci_release next_version --version v6.0.0-beta.1  # explicit prerelease
    pysae-ai-tools ci_release next_version --bump major --prerelease beta  # v5.x -> v6.0.0-beta.1
    pysae-ai-tools ci_release next_version --prerelease beta        # v6.0.0-beta.1 -> v6.0.0-beta.2
    pysae-ai-tools ci_release next_version                          # v6.0.0-beta.2 -> v6.0.0 (finalize)
    pysae-ai-tools ci_release next_version --project-id 14366711    # for a specific project

Output (JSON):
    {"latest_tag": "v1.2.3", "new_version": "v1.2.4", "bump": "patch", "is_prerelease": false}
"""

import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Annotated

import typer
from commitizen.config import BaseConfig
from commitizen.cz.conventional_commits.conventional_commits import ConventionalCommitsCz

from ...common.glab.runner import GLAB_MISSING_RC, GLAB_TIMEOUT_RC, GlabResult, resolve_current_project, run_glab
from ...common.project_config import effective_config

_CZ = ConventionalCommitsCz(BaseConfig())  # type: ignore[no-untyped-call, unused-ignore]
_BUMP_PATTERN = re.compile(_CZ.bump_pattern)
_BUMP_MAP = _CZ.bump_map
_BUMP_PRIORITY = {"PATCH": 1, "MINOR": 2, "MAJOR": 3}

# A semver tag with an optional ``-<prerelease>`` suffix. The prerelease part is
# kept loose (any dotted alphanumeric identifier) so explicit versions like
# ``v6.0.0-beta.1`` / ``v6.0.0-rc.2`` parse; the ``.N`` counter we *generate* is
# split out separately by :func:`parse_version`.
_SEMVER_RE = re.compile(r"^v?(\d+)\.(\d+)\.(\d+)(?:-(?P<pre>[0-9A-Za-z][0-9A-Za-z.-]*))?$")
# Trailing ``.<digits>`` counter inside a prerelease identifier (``beta.1`` → ``beta`` + ``1``).
_PRERELEASE_COUNTER_RE = re.compile(r"^(?P<label>.*?)\.(?P<num>\d+)$")

# A support-line spec: ``v5``, ``v5.x``, ``v5.x.x``, ``v5.2`` or ``v5.2.x``. The major is
# always pinned; the minor is pinned only when it is a literal digit (``x`` / absent = free).
# A literal patch digit (``v5.2.3``) is rejected by :func:`parse_support_line` — a fully pinned
# version is not a support line.
_SUPPORT_LINE_RE = re.compile(r"^v?(\d+)(?:\.(\d+|x))?(?:\.(\d+|x))?$", re.IGNORECASE)
# A ``glab`` stderr line that is only a severity header (``ERROR``), carrying no message.
_STDERR_LEVEL_RE = re.compile(r"^(?:error|erreur|warning|warn|fatal|x|!)[:\s]*$", re.IGNORECASE)
_BUMP_RANK = {"patch": 1, "minor": 2, "major": 3}


@dataclass(frozen=True)
class Version:
    """A parsed semver version, with an optional ``-<label>.<num>`` prerelease.

    ``label``/``num`` are both ``None`` for a final release (``v6.0.0``). A
    prerelease we generate always carries a label, and usually a counter too
    (``v6.0.0-beta.1`` → label ``beta``, num ``1``); an explicit version whose
    suffix has no trailing counter (``v6.0.0-beta``) keeps ``num`` ``None``.

    A **purely numeric** prerelease identifier (``v5.3.16-1``) is a valid semver
    prerelease whose single identifier is the number itself, compared numerically
    (``-2 < -10``). We model it as ``label=None`` + ``num`` set — keeping the
    digits out of ``label`` (where they would sort lexically, ``"10" < "2"``).
    This is the bare ``-N`` hotfix shorthand.
    """

    major: int
    minor: int
    patch: int
    label: str | None = None
    num: int | None = None

    @property
    def is_prerelease(self) -> bool:
        # Only a *beta* (alpha/beta/rc) is a prerelease: it precedes its final
        # release and ships markdown-only notes. A final release has no suffix; a
        # hotfix (``-hotfix.N`` / bare ``-N``) is a store-bound *post-release*, not a
        # prerelease — it is published after the final and outranks it.
        return self.label is not None and not self.is_hotfix

    @property
    def is_hotfix(self) -> bool:
        """A store-bound post-release build of the same X.Y.Z: ``-hotfix.N`` or bare ``-N``.

        A hotfix is published **after** its final release and outranks it (mirroring the
        Android versionCode scheme where a hotfix stays at the final stage, 7, with a
        non-zero counter). It is therefore **not** a prerelease: it ships the store
        release notes and publishes to the stores like a final release. It is either the
        ``hotfix`` label (``v5.3.16-hotfix.2``) or a purely numeric identifier
        (``v5.3.16-1`` → ``label=None``, ``num=1``). A dotted label like ``-1.2``
        (``label="1"``) is not a hotfix — aligned with :func:`code.changelog.is_hotfix_tag`.
        """
        if self.label is not None:
            return self.label.lower() == "hotfix"
        return self.num is not None

    def base_str(self) -> str:
        """The final-release string for this version's base (``v6.0.0``)."""
        return f"v{self.major}.{self.minor}.{self.patch}"

    def __str__(self) -> str:
        base = self.base_str()
        if self.label is None:
            return f"{base}-{self.num}" if self.num is not None else base
        if self.num is None:
            return f"{base}-{self.label}"
        return f"{base}-{self.label}.{self.num}"


def parse_version(version: str) -> Version:
    """Parse a semver string (optional ``v`` prefix, optional prerelease) into a :class:`Version`.

    Raises ``ValueError`` on anything that is not ``[v]MAJOR.MINOR.PATCH`` with an
    optional ``-<prerelease>`` suffix.
    """
    match = _SEMVER_RE.match(version.strip())
    if not match:
        raise ValueError(f"Invalid semver: {version}")
    major, minor, patch = int(match.group(1)), int(match.group(2)), int(match.group(3))
    pre = match.group("pre")
    if pre is None:
        return Version(major, minor, patch)
    counter = _PRERELEASE_COUNTER_RE.match(pre)
    if counter:
        return Version(major, minor, patch, counter.group("label"), int(counter.group("num")))
    # A purely numeric identifier (``-1``) is the bare hotfix shorthand: keep the
    # number in ``num`` so it compares numerically, not lexically as a label.
    if pre.isdigit():
        return Version(major, minor, patch, None, int(pre))
    return Version(major, minor, patch, pre, None)


def _version_sort_key(v: Version) -> tuple[int, int, int, int, str, int]:
    """Sort key ordering a base's versions: ``beta < final < hotfix``.

    A beta precedes its final release (``v6.0.0-beta.1 < v6.0.0-beta.2 < v6.0.0``);
    a hotfix is a *post-release* and outranks the final (``v5.3.16 < v5.3.16-1 <
    v5.3.16-2``), mirroring the Android versionCode scheme. Within a class, compare
    by (label, num): betas by ``alpha < beta < rc`` then counter, numeric hotfix ids
    by value (``-2 < -10``). Across bases, major/minor/patch dominate.
    """
    if v.is_prerelease:
        klass = 0  # beta (alpha/beta/rc) — precedes the final release
    elif v.is_hotfix:
        klass = 2  # hotfix — post-release, outranks the final
    else:
        klass = 1  # final release
    return (v.major, v.minor, v.patch, klass, v.label or "", v.num or 0)


@dataclass(frozen=True)
class SupportRange:
    """The version range a ``support/*`` branch is allowed to release within.

    ``major`` is always pinned. ``minor`` is pinned (a release stays on ``vMAJOR.MINOR.*``)
    when the support line names it as a digit; it is ``None`` (the whole major is open,
    ``vMAJOR.*.*``) when the line uses ``x`` or omits it.
    """

    major: int
    minor: int | None

    def contains(self, version: Version) -> bool:
        if version.major != self.major:
            return False
        return self.minor is None or version.minor == self.minor

    def max_bump(self) -> str:
        """The highest bump that keeps the next version inside the range.

        A minor-pinned line (``v5.2.x``) only ever patches; a major-only line
        (``v5.x.x``) allows minor too. A support line never allows ``major`` — that
        would leave the line entirely.
        """
        return "patch" if self.minor is not None else "minor"

    def __str__(self) -> str:
        return f"v{self.major}.x.x" if self.minor is None else f"v{self.major}.{self.minor}.x"


def parse_support_line(line: str) -> SupportRange:
    """Parse a support-line spec (``v5`` / ``v5.x`` / ``v5.x.x`` / ``v5.2`` / ``v5.2.x``).

    Tolerates a leading ``support/``. Raises ``ValueError`` on a fully pinned version
    (``v5.2.3``) or anything that is not a recognised support-line shape.
    """
    stripped = line.strip()
    if stripped.startswith("support/"):
        stripped = stripped[len("support/") :]
    match = _SUPPORT_LINE_RE.match(stripped)
    if not match:
        raise ValueError(f"Invalid support line: {line} (expected vMAJOR, vMAJOR.x, vMAJOR.MINOR or vMAJOR.MINOR.x)")
    major = int(match.group(1))
    minor_part, patch_part = match.group(2), match.group(3)
    if patch_part is not None and patch_part.lower() != "x":
        raise ValueError(f"Invalid support line: {line} (a fully pinned version is not a support line)")
    minor = int(minor_part) if minor_part is not None and minor_part.lower() != "x" else None
    return SupportRange(major, minor)


def compute_next(latest: Version, bump: str, prerelease: str) -> Version:
    """Compute the next version from ``latest``, a ``bump`` and an optional ``prerelease`` label.

    - ``latest`` is **final** + ``prerelease`` set → apply ``bump`` to get the base,
      then start the prerelease line (``v5.4.0`` +major +beta → ``v6.0.0-beta.1``).
    - ``latest`` is **final**, no ``prerelease`` → plain ``bump`` (current behaviour).
    - ``latest`` is a **prerelease** + same ``prerelease`` label → increment the
      counter (``v6.0.0-beta.1`` → ``v6.0.0-beta.2``); ``bump`` is ignored — we stay
      on the same base.
    - ``latest`` is a **prerelease** + a *different* ``prerelease`` label → start that
      label at ``.1`` on the same base (``v6.0.0-beta.3`` +rc → ``v6.0.0-rc.1``),
      **provided the new label ranks above the current one** — switching backward
      (``rc`` → ``beta``) raises ``ValueError`` rather than silently emitting a
      version that sorts below the existing tag (use ``--version`` to force it).
    - ``latest`` is a **prerelease**, no ``prerelease`` → **finalize**: drop the
      suffix (``v6.0.0-beta.2`` → ``v6.0.0``); ``bump`` is ignored.
    """
    if latest.is_prerelease:
        if not prerelease:
            return Version(latest.major, latest.minor, latest.patch)
        if prerelease == latest.label:
            return Version(latest.major, latest.minor, latest.patch, latest.label, (latest.num or 0) + 1)
        candidate = Version(latest.major, latest.minor, latest.patch, prerelease, 1)
        # Switching label must move forward (beta → rc), never backward: a lower
        # label would sort below the existing tag and regress the changelog label.
        if _version_sort_key(candidate) <= _version_sort_key(latest):
            raise ValueError(
                f"prerelease label {prerelease!r} regresses below the current {str(latest)!r} "
                f"(would produce {str(candidate)!r}); use a higher label or pass --version to force it"
            )
        return candidate
    base = parse_version(bump_version(latest.major, latest.minor, latest.patch, bump))
    if prerelease:
        return Version(base.major, base.minor, base.patch, prerelease, 1)
    return base


def _get_project_id() -> str:
    """Get project ID from glab repo view."""
    return resolve_current_project()[0]


class TagLookupError(RuntimeError):
    """The project's tag list could not be read, so no base tag can be *proven*.

    Raised instead of treating an unreadable list as an empty one: a ``glab`` that is
    absent, unauthenticated or looking at an inaccessible project answers nothing —
    and a version bumped from a base nobody could read is a wrong number returned as
    a success, indistinguishable from a real one. A list that *was* read and holds no
    semver tag is a different thing entirely: a proven first release.
    """


def _glab_error_detail(stderr: str) -> str:
    """The informative part of a ``glab`` stderr block, on one line.

    ``glab`` frames its errors: blank line, a bare ``ERROR`` header, blank line, then
    the message padded over several lines. Reading the first line alone therefore
    yields ``ERROR`` and says nothing — so drop the framing and join what is left.
    """
    lines = [
        " ".join(line.split())
        for line in stderr.splitlines()
        if line.strip() and not _STDERR_LEVEL_RE.match(line.strip())
    ]
    return " ".join(lines)[:200]


def _glab_failure_cause(res: GlabResult) -> str:
    """Name why a ``glab`` call failed, so the error says which of the causes it was."""
    if res.returncode == GLAB_MISSING_RC:
        return "glab n'est pas installé"
    if res.returncode == GLAB_TIMEOUT_RC:
        return "glab a dépassé son timeout"
    detail = _glab_error_detail(res.stderr) or f"code de sortie {res.returncode}"
    return f"l'appel glab a échoué ({detail})"


def _fetch_latest_tag(project_id: str, support_range: SupportRange | None = None) -> str:
    """Fetch the latest semver tag from the project, prereleases included.

    Picks the highest tag by semver precedence (``v6.0.0-beta.2 < v6.0.0``) rather
    than trusting the API ordering, so an in-flight prerelease line is detected as
    the latest tag and ``next-version`` can iterate/finalize it.

    When ``support_range`` is set, only tags inside that range are considered — so a
    ``support/v5.2.x`` release bumps from the highest ``v5.2.*`` tag, never from a
    later ``v6.x`` on the main line.

    Returns the highest matching tag, or ``""`` when the list **was read** and holds
    no usable base — the caller may then treat it as a first release. Raises
    :class:`TagLookupError` when the list could not be read at all (``glab`` absent or
    unauthenticated, project inaccessible, unparsable answer): an empty result must be
    a proven fact, never the shape a failed call happens to take.
    """
    hint = (
        "Authentifie glab (glab auth login) ou vérifie l'accès au projet ; "
        "sinon passe --version vX.Y.Z / --base-tag vX.Y.Z pour fixer la base explicitement."
    )
    res = run_glab("api", f"projects/{project_id}/repository/tags?per_page=100&order_by=version", timeout=15)
    if not res.ok:
        raise TagLookupError(
            f"Impossible de lister les tags du projet {project_id} : {_glab_failure_cause(res)} — "
            f"impossible de prouver que le projet n'a aucun tag. {hint}"
        )
    try:
        tags = json.loads(res.stdout)
    except json.JSONDecodeError:
        raise TagLookupError(
            f"Réponse inattendue en listant les tags du projet {project_id} (JSON invalide ou vide) — "
            f"impossible de prouver que le projet n'a aucun tag. {hint}"
        ) from None
    if not isinstance(tags, list):
        raise TagLookupError(
            f"Réponse inattendue en listant les tags du projet {project_id} (liste attendue, reçu "
            f"{type(tags).__name__}) — impossible de prouver que le projet n'a aucun tag. {hint}"
        )

    best: tuple[tuple[int, int, int, int, str, int], str] | None = None
    for tag in tags:
        name: str = tag.get("name", "") if isinstance(tag, dict) else ""
        try:
            parsed = parse_version(name)
        except ValueError:
            continue
        if support_range is not None and not support_range.contains(parsed):
            continue
        key = _version_sort_key(parsed)
        if best is None or key > best[0]:
            best = (key, name)
    return best[1] if best else ""


def _bump_for_message(message: str) -> str | None:
    """Return ``MAJOR`` / ``MINOR`` / ``PATCH`` for a single conventional commit line.

    Strips the leading ``* `` bullet (if present) and delegates to commitizen's
    ``bump_pattern`` / ``bump_map`` (the same logic used by ``cz bump``).
    Returns ``None`` for non-bumping types (e.g. ``tech``, ``docs``, ``chore``)
    and for lines that don't match conventional commits at all.
    """
    if message.startswith("* "):
        message = message[2:]
    m = _BUMP_PATTERN.match(message)
    if not m:
        return None
    head = m.group(0).rstrip(":")
    for pattern, bump in _BUMP_MAP.items():
        if re.match(pattern, head):
            return str(bump)
    return None


def suggest_bump_from_changelogs(ref: str = "main") -> str:
    """Analyze changelog entries on a git ref to suggest the bump type.

    Reads changelogs/ from the given ref (default: main) using git,
    not the local filesystem — ensures the release version is based
    on what's merged, not the current branch. For hotfix flows, pass
    the hotfix branch name as ``ref`` so the bump reflects the entries
    added on top of the base tag (the changelogs/ folder is pruned at
    each release, so any file present on the hotfix branch is by
    definition new since the last release).

    Rules (delegated to commitizen's ``ConventionalCommitsCz.bump_map``):
    - ``* type(scope)?!: …`` or ``BREAKING[\\- ]CHANGE:`` footer -> major
    - ``* feat(scope)?: …`` -> minor
    - ``* fix|refactor|perf(scope)?: …`` -> patch
    - Any other type (``tech``, ``docs``, ``chore``, …) -> patch (default)
    - No entries -> patch

    The highest bump across all entries wins.

    Returns: "major", "minor", or "patch".
    """
    try:
        result = subprocess.run(
            ["git", "ls-tree", "--name-only", ref, "changelogs/"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )
        if result.returncode != 0 or not result.stdout.strip():
            return "patch"
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return "patch"

    highest = "PATCH"

    for filepath in result.stdout.strip().splitlines():
        if not filepath.endswith(".md"):
            continue
        try:
            cat_result = subprocess.run(
                ["git", "show", f"{ref}:{filepath}"],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=5,
            )
            if cat_result.returncode != 0:
                continue
            content = cat_result.stdout
        except (subprocess.TimeoutExpired, FileNotFoundError):
            continue

        # Footer-style breaking change marker (multi-line — appears below the bullet)
        if re.search(r"^BREAKING[\- ]CHANGE:", content, re.MULTILINE):
            return "major"

        for line in content.splitlines():
            line = line.strip()
            if not line.startswith("* "):
                continue
            bump = _bump_for_message(line)
            if bump and _BUMP_PRIORITY[bump] > _BUMP_PRIORITY[highest]:
                highest = bump
                if highest == "MAJOR":
                    return "major"

    return highest.lower()


def bump_version(major: int, minor: int, patch: int, bump: str) -> str:
    """Compute the next version string."""
    if bump == "major":
        return f"v{major + 1}.0.0"
    if bump == "minor":
        return f"v{major}.{minor + 1}.0"
    return f"v{major}.{minor}.{patch + 1}"


@dataclass(frozen=True)
class NextVersionResult:
    """Typed contract for a successful ``next-version`` computation.

    ``is_prerelease`` / ``is_hotfix`` / ``first_release`` are real booleans here;
    :meth:`to_dict` serialises them as ``"true"`` / ``"false"`` strings on the wire
    because downstream consumers (``/code-get-next-version``, ``/ci-release``) and this
    module's own :func:`main` gate on the string form
    (``result["is_prerelease"] == "true"``). The force-bump trio
    (``version_{patch,minor,major}``) is present only when the latest tag is a
    final release — all three are set together or all left ``None``.

    ``first_release`` states that ``latest_tag`` is **not** a tag the project carries:
    the tag list was read and holds no semver tag, so the base defaulted to ``v0.0.0``.
    Consumers that need a real released tag (the hotfix flow) must gate on this field —
    reading ``latest_tag == "v0.0.0"`` cannot tell that base apart from a project that
    genuinely tagged ``v0.0.0``.
    """

    latest_tag: str
    new_version: str
    bump: str
    is_prerelease: bool
    is_hotfix: bool
    prerelease_label: str
    final_version: str
    support_line: str
    clamped_from: str
    first_release: bool = False
    version_patch: str | None = None
    version_minor: str | None = None
    version_major: str | None = None

    def to_dict(self) -> dict[str, str]:
        out: dict[str, str] = {
            "latest_tag": self.latest_tag,
            "new_version": self.new_version,
            "bump": self.bump,
            "is_prerelease": "true" if self.is_prerelease else "false",
            "is_hotfix": "true" if self.is_hotfix else "false",
            "first_release": "true" if self.first_release else "false",
            "prerelease_label": self.prerelease_label,
            "final_version": self.final_version,
            "support_line": self.support_line,
            "clamped_from": self.clamped_from,
        }
        if self.version_patch is not None and self.version_minor is not None and self.version_major is not None:
            out["version_patch"] = self.version_patch
            out["version_minor"] = self.version_minor
            out["version_major"] = self.version_major
        return out


def _result(
    latest_tag: str,
    new: Version,
    bump: str,
    *,
    base: Version | None = None,
    support_line: str = "",
    clamped_from: str = "",
    first_release: bool = False,
) -> NextVersionResult:
    """Build the typed result. ``base`` (a final version) feeds the force-bump fields.

    ``support_line`` echoes the constraining range (empty on a normal release),
    ``clamped_from`` carries the bump that was requested before clamping it down to
    the range (empty when no clamp happened), and ``first_release`` marks a
    ``latest_tag`` the project does not actually carry (no semver tag at all).
    """
    version_patch = version_minor = version_major = None
    if base is not None and not base.is_prerelease:
        version_patch = bump_version(base.major, base.minor, base.patch, "patch")
        version_minor = bump_version(base.major, base.minor, base.patch, "minor")
        version_major = bump_version(base.major, base.minor, base.patch, "major")
    return NextVersionResult(
        latest_tag=latest_tag,
        new_version=str(new),
        bump=bump,
        is_prerelease=new.is_prerelease,
        is_hotfix=new.is_hotfix,
        prerelease_label=new.label or "",
        final_version=new.base_str(),
        support_line=support_line,
        clamped_from=clamped_from,
        first_release=first_release,
        version_patch=version_patch,
        version_minor=version_minor,
        version_major=version_major,
    )


def next_version(
    project_id: str = "",
    bump: str = "",
    explicit_version: str = "",
    base_tag: str = "",
    ref: str = "",
    prerelease: str = "",
    support_line: str = "",
) -> dict[str, str]:
    """Compute the next version for a project.

    Returns a dict with: latest_tag, new_version, bump, is_prerelease, is_hotfix,
    first_release, prerelease_label, final_version, support_line, clamped_from (and
    version_{patch,minor,major} when the latest tag is a final release), or a single
    ``error`` key. The base tag is read, never guessed: a project whose tag list cannot
    be read (``glab`` absent or unauthenticated, project inaccessible) yields an
    ``error`` (exit 1). Only a list that *was* read and holds no semver tag falls back
    to a ``v0.0.0`` base, flagged ``first_release`` so a caller needing a real released
    tag can tell it apart from a project that genuinely tagged ``v0.0.0``.

    ``base_tag`` overrides the auto-detected latest tag — used for hotfix flows
    where the version is bumped from a specific older tag rather than the most
    recent one. ``ref`` overrides the git ref used to read changelogs (default
    ``main``) — for hotfixes this is the hotfix branch where the entry was added.
    ``prerelease`` (e.g. ``beta``/``rc``) produces or iterates a prerelease line;
    see :func:`compute_next`.

    ``support_line`` (``v5.2.x`` / ``v5.x.x`` / …) constrains the release to a
    ``support/*`` branch's range: the base tag is the highest tag *inside* the range,
    the bump is clamped to what stays inside it (a minor-pinned line only patches),
    and the computed version is verified to fall inside it.
    """
    support_range: SupportRange | None = None
    if support_line:
        try:
            support_range = parse_support_line(support_line)
        except ValueError as exc:
            return {"error": str(exc)}

    if explicit_version:
        try:
            parsed = parse_version(explicit_version)
        except ValueError:
            return {"error": f"Format de version invalide : {explicit_version} (attendu: vX.Y.Z ou vX.Y.Z-label.N)"}
        if support_range is not None and not support_range.contains(parsed):
            return {"error": f"La version {explicit_version} est hors de la plage support {support_range}."}
        return _result("", parsed, "explicit", support_line=support_line).to_dict()

    first_release = False
    if base_tag:
        try:
            parsed_base = parse_version(base_tag)
        except ValueError:
            return {"error": f"Format de base-tag invalide : {base_tag} (attendu: vX.Y.Z)"}
        if support_range is not None and not support_range.contains(parsed_base):
            return {"error": f"Le base-tag {base_tag} est hors de la plage support {support_range}."}
        latest_tag = base_tag if base_tag.startswith("v") else f"v{base_tag}"
    else:
        if not project_id:
            project_id = _get_project_id()
        if not project_id:
            return {"error": "Impossible de detecter le project_id. Utilise --project-id."}

        try:
            latest_tag = _fetch_latest_tag(project_id, support_range)
        except TagLookupError as exc:
            return {"error": str(exc)}
        if not latest_tag:
            if support_range is not None:
                return {"error": f"Aucun tag dans la plage support {support_range} — impossible de déterminer la base."}
            # The tag list was read and holds no semver tag: a genuine first release.
            latest_tag = "v0.0.0"
            first_release = True

    try:
        latest = parse_version(latest_tag)
    except ValueError as exc:
        return {"error": str(exc)}

    # Continuing/finalizing a prerelease line stays on the same base — the bump is
    # irrelevant there, so we never read the changelogs for it. The base came from an
    # in-range tag, so the result stays in range without an extra check.
    if latest.is_prerelease:
        try:
            new = compute_next(latest, "", prerelease)
        except ValueError as exc:
            return {"error": str(exc)}
        return _result(latest_tag, new, "prerelease" if prerelease else "release", support_line=support_line).to_dict()

    # Latest is a final release: resolve the bump (auto from changelogs if absent).
    if not bump:
        bump = suggest_bump_from_changelogs(ref=ref or "main")
    if bump not in ("major", "minor", "patch"):
        return {"error": f"Type de bump invalide : {bump} (attendu: major, minor, patch)"}

    # Clamp the bump down to what the support range allows (a feat on a v5.2.x line
    # would otherwise produce v5.3.0). The branch name is authoritative on the range;
    # we record the requested bump in ``clamped_from`` so the caller can warn.
    clamped_from = ""
    if support_range is not None:
        max_bump = support_range.max_bump()
        if _BUMP_RANK[bump] > _BUMP_RANK[max_bump]:
            clamped_from = bump
            bump = max_bump

    new = compute_next(latest, bump, prerelease)
    if support_range is not None and not support_range.contains(new):
        return {"error": f"La version calculée {new} est hors de la plage support {support_range}."}
    return _result(
        latest_tag,
        new,
        "prerelease" if prerelease else bump,
        base=latest,
        support_line=support_line,
        clamped_from=clamped_from,
        first_release=first_release,
    ).to_dict()


def main(
    project_id: Annotated[str, typer.Option("--project-id", help="GitLab project ID")] = "",
    bump: Annotated[str, typer.Option("--bump", help="Bump type (auto-detected from changelogs if omitted)")] = "",
    version: Annotated[str, typer.Option("--version", help="Explicit version (skip bump)")] = "",
    base_tag: Annotated[
        str,
        typer.Option(
            "--base-tag",
            help="Base tag to bump from (hotfix flow); defaults to the project's latest semver tag.",
        ),
    ] = "",
    ref: Annotated[
        str,
        typer.Option(
            "--ref",
            help="Git ref to read changelogs from (default: main). Pass the hotfix branch in hotfix flows.",
        ),
    ] = "",
    prerelease: Annotated[
        str,
        typer.Option(
            "--prerelease",
            help="Produce/iterate a prerelease line with this label (e.g. beta, rc). "
            "From a final tag it appends -<label>.1 to the bumped base; from a prerelease "
            "of the same label it increments the counter. Omit it on a prerelease line to finalize.",
        ),
    ] = "",
    support_line: Annotated[
        str,
        typer.Option(
            "--support-line",
            help="Constrain to a support/* branch's range (e.g. v5.2.x or v5.x.x): base off the "
            "highest tag inside the range and clamp the bump to stay inside it.",
        ),
    ] = "",
) -> None:
    """Compute the next semver version."""
    if bump and bump not in ("major", "minor", "patch"):
        print(f"Invalid bump type: {bump}. Must be one of: major, minor, patch", file=sys.stderr)
        raise typer.Exit(code=1)

    result = next_version(
        project_id=project_id,
        bump=bump,
        explicit_version=version,
        base_tag=base_tag,
        ref=ref,
        prerelease=prerelease,
        support_line=support_line,
    )

    # Gate betas behind release.allow_prerelease (default false): refuse to resolve a
    # beta (alpha/beta/rc) for a repo that hasn't opted in. A *hotfix* (``-hotfix.N`` /
    # ``-N``) is a store-bound post-release — not a prerelease — so ``is_prerelease`` is
    # already false for it and it bypasses this gate. Read the config from the current
    # directory (the repo the skill runs in).
    if "error" not in result and result.get("is_prerelease") == "true":
        if not effective_config(Path.cwd()).release.allow_prerelease:
            result = {
                "error": (
                    f"La version {result['new_version']} est une pré-release mais "
                    "release.allow_prerelease est false pour ce repo. "
                    "Active le flag dans .pysae-ai-tools.yaml pour autoriser les pré-releases."
                )
            }

    if result.get("clamped_from"):
        print(
            f"⚠️  bump {result['clamped_from']} clampé à {result['bump']} pour rester dans la plage "
            f"support {result['support_line']} → {result['new_version']}",
            file=sys.stderr,
        )

    json.dump(result, sys.stdout, indent=2)
    sys.stdout.write("\n")

    if "error" in result:
        raise typer.Exit(code=1)
