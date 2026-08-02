"""Scan a skill directory and produce a structured report for review.

Used by the ``clawd-skill-review`` skill — replaces the previous shell
script under ``claude_plugin/skills/clawd-skill-review/scripts/``.

Also carries the deterministic **description-quality lint** that guards
natural-language triggering: the ``description`` frontmatter is the only signal
that routes a user's phrasing to a skill, so a thin description means the skill
silently fails to trigger. ``--all`` scans every bundled skill and ``--check``
turns a sub-threshold description into a non-zero exit (CI guardrail). The
convention the score enforces lives in
``claude_plugin/skills/references/skill-description.md``.
"""

import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Annotated

import typer

from ..common.skills import invalid_assistants


def _skill_invalid_assistants(skill_dir: Path) -> list[str]:
    """The ``assistants:`` values of a skill that are not recognised targets (empty when
    the field is absent or every value is valid). A non-empty list fails ``--check``."""
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        return []
    return invalid_assistants(skill_md.read_text(encoding="utf-8", errors="replace"))


# Patterns flagged as potential hardcoded values worth turning into config.
_HARDCODED_PATTERN = re.compile(r"[A-Z][A-Z0-9]{6,}|C[0-9A-Z]{10}|https?://[^ ]+")

# --- Description-quality thresholds (see references/skill-description.md) ---
# These are the ENFORCED floor (the lint blocks below them); the convention recommends
# aiming higher (≥6 trigger phrases). The floor flags genuinely-thin descriptions that
# fail to trigger, not merely terse-but-working ones.
_MIN_WORDS = 30
_MIN_TRIGGER_PHRASES = 4
# Quoted trigger phrases: 'like this' or "like this" (the phrase bank).
_TRIGGER_PHRASE_RE = re.compile(r"'[^']{2,}'|\"[^\"]{2,}\"")
# A slash alias such as /ci-deploy or /mr.
_SLASH_ALIAS_RE = re.compile(r"/[a-z][a-z-]{1,}")
# French signal: accented letters, or FR words that do NOT occur in English. Only
# unambiguous French markers belong here — function words (la/le/une/est/sur/…) and
# FR-only verbs/adjectives catch accent-free French like "la prod est lente". English-
# shared tokens (prod/perfs/tickets/cache) are deliberately excluded: an English-only
# description containing them must NOT pass the French gate.
_FR_ACCENT_RE = re.compile(r"[àâäçéèêëîïôöùûü]", re.IGNORECASE)
_FR_WORD_RE = re.compile(
    r"\b(fais|lance|crée|cree|déploie|deploie|redéploie|redeploie|montre|vérifie|verifie|"
    r"trouve|ouvre|mets|résous|resous|redémarre|redemarre|prochaine|nouvelle|quelle|quoi|"
    r"pourquoi|ça|sur|la|le|les|une|des|du|est|avec|pour|dans|mon|mes|ma|cette|cet|"
    r"rame|lente|lent|rapport|souci)\b",
    re.IGNORECASE,
)
# English signal: the canonical trigger scaffolding and common EN trigger words.
_EN_WORD_RE = re.compile(
    r"\b(use when|the user says|or wants to|create|open|deploy|review|check|find|show|run|fix)\b",
    re.IGNORECASE,
)


@dataclass
class DescriptionScore:
    """Deterministic quality signals for a skill's ``description`` frontmatter."""

    present: bool
    words: int = 0
    trigger_phrases: int = 0
    has_use_when: bool = False
    has_slash_alias: bool = False
    has_fr: bool = False
    has_en: bool = False

    @property
    def failures(self) -> list[str]:
        """Human-readable list of the thresholds this description misses (empty = OK)."""
        if not self.present:
            return ["description field MISSING"]
        out: list[str] = []
        if self.words < _MIN_WORDS:
            out.append(f"too short ({self.words} words < {_MIN_WORDS})")
        if self.trigger_phrases < _MIN_TRIGGER_PHRASES:
            out.append(f"too few trigger phrases ({self.trigger_phrases} < {_MIN_TRIGGER_PHRASES})")
        if not self.has_use_when:
            out.append("no 'use when' trigger clause")
        if not self.has_slash_alias:
            out.append("no /slash alias")
        if not self.has_fr:
            out.append("no French trigger phrases")
        if not self.has_en:
            out.append("no English trigger phrases")
        return out

    @property
    def ok(self) -> bool:
        return not self.failures


def _extract_description(md_text: str) -> str | None:
    """Return the ``description`` value from the YAML frontmatter, or None if absent.

    Handles the folded-scalar form (``description: >`` / ``|`` followed by an indented
    block) as well as a single-line ``description: ...``. Avoids a YAML dependency on the
    frontmatter parsing so a malformed (but present) block still scores rather than crashing.
    """
    lines = md_text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    # Frontmatter spans from line 1 to the next '---'.
    end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
    if end is None:
        return None
    fm = lines[1:end]
    for i, line in enumerate(fm):
        if not line.startswith("description:"):
            continue
        rest = line[len("description:") :].strip()
        if rest and rest not in (">", "|", ">-", "|-", ">+", "|+"):
            return rest
        # Folded/literal block: gather the following more-indented lines.
        block: list[str] = []
        for follow in fm[i + 1 :]:
            if follow.strip() == "":
                block.append("")
                continue
            if not follow.startswith((" ", "\t")):
                break
            block.append(follow.strip())
        return " ".join(b for b in block if b).strip()
    return None


def score_description(description: str | None) -> DescriptionScore:
    """Score a description string against the deterministic trigger-quality signals."""
    if description is None:
        return DescriptionScore(present=False)
    return DescriptionScore(
        present=True,
        words=len(description.split()),
        trigger_phrases=len(_TRIGGER_PHRASE_RE.findall(description)),
        has_use_when=bool(re.search(r"use when", description, re.IGNORECASE)),
        has_slash_alias=bool(_SLASH_ALIAS_RE.search(description)),
        has_fr=bool(_FR_ACCENT_RE.search(description) or _FR_WORD_RE.search(description)),
        has_en=bool(_EN_WORD_RE.search(description)),
    )


def _scan_one(skill_dir: Path) -> DescriptionScore:
    """Print the full structured report for one skill and return its description score."""
    skill_name = skill_dir.name
    skill_md = skill_dir / "SKILL.md"

    print(f"=== SKILL: {skill_name} ===\n")

    # --- File inventory ---
    print("## File inventory")
    files = sorted(p for p in skill_dir.rglob("*") if p.is_file())
    for f in files:
        rel = f.relative_to(skill_dir)
        try:
            text = f.read_text(encoding="utf-8", errors="replace")
            lines = text.count("\n") + (1 if text and not text.endswith("\n") else 0)
        except OSError:
            lines = 0
        try:
            size = f.stat().st_size
        except OSError:
            size = 0
        print(f"  {rel}  ({lines} lines, {size}B)")
    print()

    # --- Structure signals ---
    print("## Structure signals")

    # Scripts present? (excluding self)
    self_path = Path(__file__).resolve()
    script_count = sum(1 for f in files if f.suffix in {".sh", ".py", ".js", ".ts"} and f.resolve() != self_path)
    print(f"  scripts: {script_count}")

    references_dir = skill_dir / "references"
    if references_dir.is_dir():
        ref_files = [p for p in references_dir.rglob("*") if p.is_file()]
        if ref_files:
            print(f"  references/: {len(ref_files)} files")
        else:
            print("  references/: EMPTY (directory exists but contains no files)")
    else:
        print("  references/: absent")

    assets_dir = skill_dir / "assets"
    if assets_dir.is_dir():
        asset_files = [p for p in assets_dir.rglob("*") if p.is_file()]
        print(f"  assets/: {len(asset_files)} files")
    else:
        print("  assets/: absent")

    print(f"  config.json: {'present' if (skill_dir / 'config.json').is_file() else 'absent'}")
    print()

    # --- SKILL.md analysis ---
    if not skill_md.is_file():
        print("  WARNING: No SKILL.md found!")
        return DescriptionScore(present=False)

    md_text = skill_md.read_text(encoding="utf-8", errors="replace")
    md_lines = md_text.splitlines()
    print("## SKILL.md metrics")
    print(f"  total_lines: {len(md_lines)}")

    # Frontmatter description (between first and second --- delimiter) + quality score.
    score = score_description(_extract_description(md_text))
    print(f"  description_field: {'present' if score.present else 'MISSING'}")
    print("## Description quality")
    print(f"  words: {score.words}")
    print(f"  trigger_phrases: {score.trigger_phrases}")
    print(f"  has_use_when: {'yes' if score.has_use_when else 'no'}")
    print(f"  has_slash_alias: {'yes' if score.has_slash_alias else 'no'}")
    print(f"  triggers_fr: {'yes' if score.has_fr else 'no'}")
    print(f"  triggers_en: {'yes' if score.has_en else 'no'}")
    if score.ok:
        print("  verdict: OK")
    else:
        print(f"  verdict: WEAK — {'; '.join(score.failures)}")

    # Section detection
    print()
    print("## Sections detected")
    for idx, line in enumerate(md_lines, start=1):
        if line.startswith("## "):
            print(f"  {idx}:{line}")

    print()
    print("## Content signals")

    md_lower = md_text.lower()
    has_gotchas_section = any(line.startswith("## Gotchas") for line in md_lines)
    print(f"  has_gotchas_section: {'yes' if has_gotchas_section else 'no'}")
    print(f"  gotchas_mentions: {md_lower.count('gotcha')}")
    print(f"  example_mentions: {md_lower.count('example')}")
    hook_mentions = md_lower.count("hook") + md_lower.count("pretooluse") + md_lower.count("posttooluse")
    print(f"  hook_mentions: {hook_mentions}")

    # Skill references like /skill-name
    skill_refs = len(re.findall(r"/[a-z][-a-z]+", md_text))
    print(f"  skill_references: {skill_refs}")

    memory_pattern = re.compile(r"CLAUDE_PLUGIN_DATA|\.log|\.jsonl|history|persist", re.IGNORECASE)
    print(f"  memory_mentions: {len(memory_pattern.findall(md_text))}")

    dual_pattern = re.compile(r"CI.*mode|headless|local.*mode|interactive.*mode", re.IGNORECASE)
    print(f"  dual_mode_mentions: {len(dual_pattern.findall(md_text))}")

    # Hardcoded value scan — SKILL.md + every .md under references/
    scan_targets: list[Path] = [skill_md]
    if references_dir.is_dir():
        scan_targets.extend(sorted(references_dir.rglob("*.md")))

    total = 0
    for ref_file in scan_targets:
        if not ref_file.is_file():
            continue
        text = ref_file.read_text(encoding="utf-8", errors="replace")
        count = sum(1 for _ in _HARDCODED_PATTERN.finditer(text))
        if count > 0:
            rel = ref_file.relative_to(skill_dir)
            print(f"  hardcoded_in {rel}: {count}")
        total += count
    print(f"  potential_hardcoded_values_total: {total}")

    print(f"\n=== END {skill_name} ===")
    return score


def _bundled_skills_root() -> Path:
    """The plugin's bundled skills directory (``pysae_ai_tools/claude_plugin/skills``)."""
    return Path(__file__).resolve().parent.parent / "claude_plugin" / "skills"


def _skill_dirs(root: Path) -> list[Path]:
    """Every immediate sub-directory of ``root`` that holds a ``SKILL.md``."""
    return sorted(p for p in root.iterdir() if p.is_dir() and (p / "SKILL.md").is_file())


def main(
    skill_dir: Annotated[
        Path | None,
        typer.Argument(help="Skill directory to scan (or the skills root with --all). Defaults to the bundled skills."),
    ] = None,
    all_skills: Annotated[
        bool,
        typer.Option("--all", help="Scan every bundled skill and print a one-line description verdict per skill."),
    ] = False,
    check: Annotated[
        bool,
        typer.Option(
            "--check", help="Exit non-zero if any scanned skill's description is below the quality threshold."
        ),
    ] = False,
) -> None:
    """Scan a skill (or all skills) and report structure + description-trigger quality.

    Default: a full structured report for one skill on stdout (exit 0). ``--all`` scans every
    bundled skill (or every skill under ``skill_dir`` when given) and prints a compact verdict
    line each. ``--check`` makes a sub-threshold description fail the command — the CI guardrail
    for natural-language triggering (see references/skill-description.md).
    """
    if all_skills:
        root = skill_dir if skill_dir is not None else _bundled_skills_root()
        if not root.is_dir():
            print(f"ERROR: {root} is not a directory", file=sys.stderr)
            raise typer.Exit(code=1)
        dirs = _skill_dirs(root)
        if not dirs:
            print(f"ERROR: no skills (sub-dir with a SKILL.md) under {root}", file=sys.stderr)
            raise typer.Exit(code=1)
        weak: list[str] = []
        bad_assistants: list[str] = []
        for d in dirs:
            md = d / "SKILL.md"
            score = score_description(_extract_description(md.read_text(encoding="utf-8", errors="replace")))
            invalid = _skill_invalid_assistants(d)
            if score.ok:
                print(f"  OK    {d.name:34} ({score.words}w, {score.trigger_phrases} triggers)")
            else:
                weak.append(d.name)
                print(f"  WEAK  {d.name:34} {'; '.join(score.failures)}")
            if invalid:
                bad_assistants.append(d.name)
                print(f"  ASSISTANTS  {d.name:34} unknown target(s): {', '.join(invalid)}")
        print(f"\n{len(dirs)} skills scanned — {len(weak)} weak, {len(bad_assistants)} with invalid assistants.")
        if check and (weak or bad_assistants):
            if weak:
                print(f"FAIL: {len(weak)} skill description(s) below threshold: {', '.join(weak)}", file=sys.stderr)
            if bad_assistants:
                print(
                    f"FAIL: {len(bad_assistants)} skill(s) with invalid assistants: {', '.join(bad_assistants)}",
                    file=sys.stderr,
                )
            raise typer.Exit(code=1)
        return

    if skill_dir is None or not skill_dir.is_dir():
        print(f"ERROR: {skill_dir} is not a directory", file=sys.stderr)
        raise typer.Exit(code=1)
    score = _scan_one(skill_dir)
    invalid = _skill_invalid_assistants(skill_dir)
    if check and (not score.ok or invalid):
        if not score.ok:
            print(f"FAIL: {skill_dir.name} description below threshold: {'; '.join(score.failures)}", file=sys.stderr)
        if invalid:
            print(f"FAIL: {skill_dir.name} has invalid assistants: {', '.join(invalid)}", file=sys.stderr)
        raise typer.Exit(code=1)


if __name__ == "__main__":
    typer.run(main)
