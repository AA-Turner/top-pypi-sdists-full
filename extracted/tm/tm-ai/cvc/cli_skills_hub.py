"""
cvc.cli_skills_hub — `cvc skills hub ...` subcommand group (Phase C, items 3.11+3.12).

    cvc skills hub search <query>            # search GitHub + well-known + URL sources
    cvc skills hub inspect <identifier>      # show metadata + trust level
    cvc skills hub scan <identifier>         # download → quarantine → guard report
    cvc skills hub install <identifier>      # scan + install (refuses on CRITICAL)
    cvc skills hub install <id> --force      # override (still refuses on CRITICAL)
    cvc skills hub list-installed            # show installed skills + lock file
    cvc skills hub uninstall <name>          # remove an installed hub skill
    cvc skills hub update [name]             # re-fetch + re-scan; bump if changed

Routes all writes through the vendored quarantine → scan → install pipeline.
Both ``cvc`` (CLI) and ``cvc gateway start`` (dashboard) pick up new skills on
the next system-prompt rebuild — no daemon restart required.
"""

from __future__ import annotations

import os
import sys
import click
from pathlib import Path

# Mirror cli_skills.py: pin HERMES_HOME so the vendored substrate writes under ~/.cvc.
os.environ.setdefault("HERMES_HOME", os.path.expanduser("~/.cvc"))


# ---------------------------------------------------------------------------
# Source resolution
# ---------------------------------------------------------------------------

def _all_sources():
    """Return the search sources in priority order (trusted → community)."""
    from cvc.agent._vendor.hermes.tools.skills_hub import (
        GitHubAuth, GitHubSource, WellKnownSkillSource,
    )
    return [WellKnownSkillSource(), GitHubSource(GitHubAuth())]


def _source_for(identifier: str):
    """Pick the right source for an identifier (URL vs GitHub repo vs well-known)."""
    from cvc.agent._vendor.hermes.tools.skills_hub import (
        GitHubAuth, GitHubSource, WellKnownSkillSource, UrlSource,
    )
    if identifier.startswith(("http://", "https://")):
        return UrlSource(GitHubAuth())
    # Well-known first (cheaper, no network for catalog lookup)
    wk = WellKnownSkillSource()
    try:
        if wk.inspect(identifier):
            return wk
    except Exception:
        pass
    return GitHubSource(GitHubAuth())


# ---------------------------------------------------------------------------
# `cvc skills hub` group
# ---------------------------------------------------------------------------

@click.group("hub")
def hub_group() -> None:
    """Discover, scan, and install skills from remote registries (Phase C)."""
    pass


@hub_group.command("search")
@click.argument("query")
@click.option("--limit", default=10, type=int, help="Max results per source.")
@click.option("--source", default=None,
              help="Restrict to one source (github|wellknown|url).")
def hub_search(query: str, limit: int, source: str | None) -> None:
    """Search all enabled skill sources for QUERY."""
    from rich.console import Console
    from rich.table import Table
    from rich import box

    sources = _all_sources()
    if source:
        wanted = source.replace("_", "-").lower()
        sources = [s for s in sources if s.source_id().lower().startswith(wanted)
                   or wanted.startswith(s.source_id().lower().split("-")[0])]
        if not sources:
            click.echo(f"No matching source: {source}", err=True)
            sys.exit(1)

    rows: list[tuple[str, ...]] = []
    for src in sources:
        try:
            results = src.search(query, limit=limit) or []
        except Exception as exc:
            click.echo(f"[{src.source_id()}] search failed: {exc}", err=True)
            continue
        for m in results:
            rows.append((m.name, m.source, m.trust_level, m.identifier,
                         (m.description or "")[:60]))

    if not rows:
        click.echo("No results.")
        return

    console = Console()
    tbl = Table(title=f"Skill Hub Search — '{query}'",
                box=box.ROUNDED, border_style="cyan")
    for h in ("name", "source", "trust", "identifier", "description"):
        tbl.add_column(h, style="white", overflow="fold")
    for r in rows:
        tbl.add_row(*r)
    console.print(tbl)


@hub_group.command("inspect")
@click.argument("identifier")
def hub_inspect(identifier: str) -> None:
    """Show metadata for a skill without downloading the bundle."""
    src = _source_for(identifier)
    try:
        meta = src.inspect(identifier)
    except Exception as exc:
        click.echo(f"inspect failed: {exc}", err=True)
        sys.exit(1)
    if not meta:
        click.echo(f"Not found: {identifier}", err=True)
        sys.exit(1)
    click.echo(f"name         : {meta.name}")
    click.echo(f"source       : {meta.source}")
    click.echo(f"trust_level  : {meta.trust_level}")
    click.echo(f"identifier   : {meta.identifier}")
    click.echo(f"repo         : {meta.repo or '-'}")
    click.echo(f"path         : {meta.path or '-'}")
    click.echo(f"tags         : {', '.join(meta.tags) if meta.tags else '-'}")
    click.echo(f"description  : {meta.description}")


@hub_group.command("scan")
@click.argument("identifier")
def hub_scan(identifier: str) -> None:
    """Download to quarantine, run the security scanner, print the report.

    Does NOT install. Use ``cvc skills hub install`` to commit.
    """
    from cvc.agent._vendor.hermes.tools.skills_hub import quarantine_bundle
    from cvc.agent._vendor.hermes.tools.skills_guard import (
        scan_skill, format_scan_report,
    )

    src = _source_for(identifier)
    try:
        bundle = src.fetch(identifier)
    except Exception as exc:
        click.echo(f"fetch failed: {exc}", err=True)
        sys.exit(1)
    if not bundle:
        click.echo(f"Not found: {identifier}", err=True)
        sys.exit(1)

    qpath = quarantine_bundle(bundle)
    result = scan_skill(qpath, source=bundle.source)
    click.echo(format_scan_report(result))
    click.echo(f"\nquarantine: {qpath}")
    click.echo("(run `cvc skills hub install <id>` to commit, or delete the dir to discard)")


@hub_group.command("install")
@click.argument("identifier")
@click.option("--category", default="", help="Optional category subdir.")
@click.option("--force", is_flag=True,
              help="Allow install on WARN/SUSPICIOUS verdicts (CRITICAL is never bypassed).")
def hub_install(identifier: str, category: str, force: bool) -> None:
    """Fetch + quarantine + scan + install in one step.

    Refuses CRITICAL verdicts unconditionally. Lower-severity findings can be
    bypassed with --force. Always prints the scan report before installing.
    """
    from cvc.agent._vendor.hermes.tools.skills_hub import (
        quarantine_bundle, install_from_quarantine,
    )
    from cvc.agent._vendor.hermes.tools.skills_guard import (
        scan_skill, should_allow_install, format_scan_report,
    )

    src = _source_for(identifier)
    try:
        bundle = src.fetch(identifier)
    except Exception as exc:
        click.echo(f"fetch failed: {exc}", err=True)
        sys.exit(1)
    if not bundle:
        click.echo(f"Not found: {identifier}", err=True)
        sys.exit(1)

    qpath = quarantine_bundle(bundle)
    result = scan_skill(qpath, source=bundle.source)
    click.echo(format_scan_report(result))

    allow, reason = should_allow_install(result, force=force)
    if not allow:
        click.echo(f"\nREFUSED: {reason}", err=True)
        click.echo(f"Quarantine kept at: {qpath}", err=True)
        sys.exit(2)

    install_path = install_from_quarantine(qpath, bundle.name, category, bundle, result)
    click.echo(f"\n✓ installed: {bundle.name} → {install_path}")
    click.echo("  Skill will appear in the next system prompt rebuild")
    click.echo("  (next `cvc` chat turn, or `/refresh` in the dashboard).")

    # Bust the manifest cache so the next prompt rebuild picks up the new skill.
    try:
        from cvc.agent._vendor.hermes.agent.prompt_builder import (
            clear_skills_system_prompt_cache,
        )
        clear_skills_system_prompt_cache(clear_snapshot=True)
    except Exception:
        pass


@hub_group.command("list-installed")
def hub_list_installed() -> None:
    """Show skills installed via the hub (from the lock file)."""
    from cvc.agent._vendor.hermes.tools.skills_hub import HubLockFile
    from rich.console import Console
    from rich.table import Table
    from rich import box

    lock = HubLockFile()
    entries = lock.list_installed() if hasattr(lock, "list_installed") else []
    if not entries:
        # Fallback: try direct read of the lock data
        try:
            data = lock._load() if hasattr(lock, "_load") else {}
            entries = [{"name": k, **v} for k, v in (data.get("skills") or {}).items()]
        except Exception:
            entries = []

    if not entries:
        click.echo("No hub-installed skills yet.")
        return

    console = Console()
    tbl = Table(title="Hub-Installed Skills",
                box=box.ROUNDED, border_style="cyan")
    for h in ("name", "source", "trust", "verdict", "identifier"):
        tbl.add_column(h, style="white", overflow="fold")
    for e in entries:
        tbl.add_row(
            str(e.get("name", "?")),
            str(e.get("source", "?")),
            str(e.get("trust_level", "?")),
            str(e.get("scan_verdict", "?")),
            str(e.get("identifier", "?")),
        )
    console.print(tbl)


@hub_group.command("uninstall")
@click.argument("name")
def hub_uninstall(name: str) -> None:
    """Remove a hub-installed skill (and its lock entry)."""
    from cvc.agent._vendor.hermes.tools.skills_hub import (
        HubLockFile, SKILLS_DIR,
    )
    import shutil

    lock = HubLockFile()
    data = lock._load() if hasattr(lock, "_load") else {}
    entry = (data.get("skills") or {}).get(name)
    if not entry:
        click.echo(f"Not installed via hub: {name}", err=True)
        sys.exit(1)
    rel = entry.get("install_path") or name
    target = SKILLS_DIR / rel
    if target.exists():
        shutil.rmtree(target)
    # Remove lock entry
    if hasattr(lock, "remove_install"):
        lock.remove_install(name)
    else:
        data["skills"].pop(name, None)
        if hasattr(lock, "_save"):
            lock._save(data)
    click.echo(f"✓ uninstalled {name}")

    try:
        from cvc.agent._vendor.hermes.agent.prompt_builder import (
            clear_skills_system_prompt_cache,
        )
        clear_skills_system_prompt_cache(clear_snapshot=True)
    except Exception:
        pass


@hub_group.command("update")
@click.argument("name", required=False)
@click.option("--force", is_flag=True, help="Allow WARN/SUSPICIOUS on re-scan.")
def hub_update(name: str | None, force: bool) -> None:
    """Re-fetch + re-scan a hub-installed skill (or all of them)."""
    from cvc.agent._vendor.hermes.tools.skills_hub import (
        HubLockFile, quarantine_bundle, install_from_quarantine,
    )
    from cvc.agent._vendor.hermes.tools.skills_guard import (
        scan_skill, should_allow_install,
    )

    lock = HubLockFile()
    data = lock._load() if hasattr(lock, "_load") else {}
    installed = data.get("skills") or {}
    targets = [name] if name else list(installed.keys())
    if not targets:
        click.echo("Nothing to update.")
        return

    for n in targets:
        entry = installed.get(n)
        if not entry:
            click.echo(f"skip {n}: not in lock file", err=True)
            continue
        ident = entry.get("identifier")
        src = _source_for(ident)
        try:
            bundle = src.fetch(ident)
        except Exception as exc:
            click.echo(f"skip {n}: fetch failed: {exc}", err=True)
            continue
        if not bundle:
            click.echo(f"skip {n}: not found at source", err=True)
            continue
        qpath = quarantine_bundle(bundle)
        result = scan_skill(qpath, source=bundle.source)
        allow, reason = should_allow_install(result, force=force)
        if not allow:
            click.echo(f"skip {n}: {reason}", err=True)
            continue
        install_from_quarantine(qpath, bundle.name, "", bundle, result)
        click.echo(f"✓ updated {n} ({result.verdict})")

    try:
        from cvc.agent._vendor.hermes.agent.prompt_builder import (
            clear_skills_system_prompt_cache,
        )
        clear_skills_system_prompt_cache(clear_snapshot=True)
    except Exception:
        pass
