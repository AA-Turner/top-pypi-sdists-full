import json
import re
from dataclasses import dataclass
from pathlib import Path

import typer

_SKILLS_DIR = ("pysae_ai_tools", "claude_plugin", "skills")
_SKILL_ROW = re.compile(r"^\|\s*`([a-z0-9-]+)`\s*\|", re.MULTILINE)
_H2 = re.compile(r"^## .*$", re.MULTILINE)
_SKILLS_HEADING = re.compile(r"^## Skills\b")
_LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")  # liens, pas les images ![..](..)
_FENCE = re.compile(r"^\s{0,3}(`{3,}|~{3,})")  # ouverture/fermeture de bloc fenced
_INLINE_CODE = re.compile(r"(`+)[^\n]*?\1")  # span de code inline `…` / ``…``


def _strip_code(text: str) -> str:
    """Neutralise les zones de code avant la détection de liens.

    Un ``[x](y.py)`` qui n'est qu'un exemple dans un bloc fenced ou un span
    inline n'est pas un vrai lien : on retire ces zones pour éviter les faux
    positifs. Les blocs indentés (4 espaces) ne sont volontairement pas gérés,
    car ils se confondent avec les listes à puces et masqueraient de vrais liens.
    """
    kept: list[str] = []
    fence: str | None = None
    for line in text.splitlines():
        marker = _FENCE.match(line)
        if fence is None:
            if marker:
                fence = marker.group(1)[0]
                continue
            kept.append(line)
        elif marker and marker.group(1)[0] == fence:
            fence = None
    return _INLINE_CODE.sub(" ", "\n".join(kept))


@dataclass(frozen=True)
class DocsReport:
    verdict: str
    findings: list[str]


def actual_skills(root: Path) -> set[str]:
    """Noms des skills réellement présents (un dossier avec un SKILL.md)."""
    d = root.joinpath(*_SKILLS_DIR)
    if not d.is_dir():
        return set()
    return {p.name for p in d.iterdir() if (p / "SKILL.md").is_file()}


def readme_skill_names(readme: str) -> set[str]:
    """Skills cités en 1re colonne des tables des sections Skills du README.

    La recherche est bornée à chaque section dont le titre commence par
    ``## Skills`` et s'arrête au prochain titre de niveau 2 : les autres
    sections (catalogue des outils gérés, table des labels d'agent…) emploient
    le même format de tableau ``| `nom` |`` sans être des skills. À défaut de
    toute section ``## Skills``, tout le document est scanné.
    """
    headings = list(_H2.finditer(readme))
    if not any(_SKILLS_HEADING.match(h.group(0)) for h in headings):
        return set(_SKILL_ROW.findall(readme))
    names: set[str] = set()
    for i, heading in enumerate(headings):
        if not _SKILLS_HEADING.match(heading.group(0)):
            continue
        end = headings[i + 1].start() if i + 1 < len(headings) else len(readme)
        names.update(_SKILL_ROW.findall(readme[heading.end() : end]))
    return names


def skill_drift(root: Path) -> list[str]:
    """C2 : la table des skills du README doit refléter les skills réels."""
    skills = actual_skills(root)
    if not skills:
        return []
    readme_path = root / "README.md"
    referenced = readme_skill_names(readme_path.read_text(encoding="utf-8")) if readme_path.is_file() else set()
    out = [f"C2 skill `{s}` absent du README" for s in sorted(skills - referenced)]
    out += [f"C2 README cite le skill `{s}` qui n'existe pas" for s in sorted(referenced - skills)]
    return out


def _doc_files(root: Path) -> list[Path]:
    files = [p for p in (root / "README.md", root / "CLAUDE.md") if p.is_file()]
    docs = root / "docs"
    if docs.is_dir():
        files += sorted(docs.rglob("*.md"))
    # Les SKILL.md et leurs références : un lien mort y casse le skill au runtime,
    # pas seulement la lecture de la doc.
    skills = root.joinpath(*_SKILLS_DIR)
    if skills.is_dir():
        files += sorted(skills.rglob("*.md"))
    return files


def broken_links(root: Path) -> list[str]:
    """C3 : liens markdown relatifs pointant vers un fichier inexistant."""
    out: list[str] = []
    for md in _doc_files(root):
        content = _strip_code(md.read_text(encoding="utf-8", errors="replace"))
        for m in _LINK.finditer(content):
            target = m.group(1).split("#", 1)[0].strip()
            # ignorer URLs, placeholders angle-bracket (<url>) et cibles non-chemins
            if not target or " " in target or "://" in target or target.startswith(("mailto:", "<")):
                continue
            if not (md.parent / target).exists():
                out.append(f"C3 lien mort dans {md.relative_to(root)} : {target}")
    return out


def run_docs_check(root: str = ".") -> DocsReport:
    base = Path(root)
    findings = skill_drift(base) + broken_links(base)
    return DocsReport(verdict="DRIFT" if findings else "SYNCED", findings=findings)


def main(root: str = ".") -> None:
    """Vérifie que la doc est synchronisée avec le code (skills, liens)."""
    report = run_docs_check(root)
    typer.echo(json.dumps({"verdict": report.verdict, "findings": report.findings}, indent=2, ensure_ascii=False))
    raise typer.Exit(code=1 if report.verdict == "DRIFT" else 0)
