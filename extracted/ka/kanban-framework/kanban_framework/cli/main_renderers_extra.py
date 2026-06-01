"""Extended renderers — knowledge and dashboard display functions."""
from __future__ import annotations

from kanban_framework.cli.main_renderers import _format_table, _render_json_fallback


def _render_dashboard(data: dict):
    """Render dashboard command results."""
    d = data.get("dashboard", data)

    if "deployed_to" in d:
        print(f"  Deployed to: {d['deployed_to']}")
        print(f"  Files copied: {d.get('copied', 0)}, skipped: {d.get('skipped', 0)}")
        return

    if "started" in d:
        if d["started"]:
            print(f"  Dashboard started (pid {d.get('pid', '?')}, port {d.get('port', 3000)})")
            print(f"  Open http://localhost:{d.get('port', 3000)}")
        else:
            print(f"  Dashboard already running (pid {d.get('pid', '?')})")
        return

    if "stopped" in d:
        if d["stopped"]:
            print(f"  Dashboard stopped (pid {d.get('pid', '?')})")
        else:
            print(f"  Dashboard not running ({d.get('reason', '')})")
        return

    if d.get("help"):
        print(f"\n  {d.get('message', '')}")
        print()
        for cmd, desc in d.get("commands", {}).items():
            print(f"    {cmd.ljust(10)} {desc}")
        if d.get("default"):
            print(f"\n  {d['default']}")
        return

    if "error" in d:
        print(f"  Error: {d['error']}")
        if d.get("help_hint"):
            print(f"  {d['help_hint']}")
        return

    if "deployed" in d and "running" in d:
        dep = "yes" if d.get("deployed") else "no"
        run = "running" if d.get("running") else "stopped"
        pid = d.get("pid")
        print(f"  Deployed: {dep} | Status: {run}")
        if pid:
            print(f"  PID: {pid}")
        print(f"  Dir: {d.get('deploy_dir', '?')}")
        return

    total = d.get("total", 0)
    by_phase = d.get("by_phase", {})
    print(f"\n  Dashboard — {total} tasks")
    for phase, count in by_phase.items():
        print(f"    {phase}: {count}")


def _render_knowledge(data: dict) -> None:
    """Render kanban knowledge help and command results."""
    if "subcommands" in data:
        print(f"\n  {data.get('description', '')}")
        token_guide = data.get("token_guide")
        subs = data["subcommands"]
        max_len = max(len(k) for k in subs.keys())
        for cmd, desc in sorted(subs.items()):
            print(f"  {cmd.ljust(max_len + 2)} {desc}")
        if token_guide:
            print(f"\n  Token: {token_guide}")
        print(f"\n  kanban knowledge help <subcommand> 查看单条命令详细帮助")
        print(f"  完整参考: references/knowledge-cli-reference.md")
        return

    if "usage" in data and "examples" in data:
        print(f"\n  {data.get('description', '')}")
        print(f"\n  Usage: {data['usage']}")
        if data.get("examples"):
            print(f"\n  Examples:")
            for ex in data["examples"]:
                print(f"    $ {ex}")
        return

    if "entry" in data:
        e = data["entry"]
        print(f"\n  {e.get('id', '?')} — {e.get('title', '?')}")
        print(f"  Domain: {e.get('domain', '?')} | Category: {e.get('category', '?')}")
        print(f"  Severity: {e.get('severity', '?')} | Status: {e.get('status', '?')}")
        tags = e.get("tags", [])
        if tags:
            print(f"  Tags: {', '.join(tags) if isinstance(tags, list) else tags}")
        content = e.get("content", "")
        if content:
            print(f"\n  {content}")
        code = e.get("code_example", "")
        if code:
            print(f"\n  --- code_example ---")
            for line in code.split("\n"):
                print(f"  {line}")
        refs = e.get("referenced_count", 0)
        if refs:
            print(f"\n  Referenced: {refs} times, last by {e.get('last_referenced_by', '-')}")
        return

    if "results" in data and "summary" in data:
        count = data.get("count", 0)
        mode = data.get("mode") or data.get("intent") or ""
        keyword = data.get("keyword") or data.get("query") or data.get("tag") or data.get("task") or data.get("domain") or ""
        summary_only = data.get("summary_only", False)
        print(f"\n  Results: {count} entries")
        if keyword:
            print(f"  Query: {keyword}" + (f" ({mode})" if mode else ""))
        if summary_only:
            print(f"  Mode: --summary-only (omit content/code_example)")
        summary = data.get("summary", [])
        if summary:
            print()
            for s in summary:
                rel = s.get("relevance", 0)
                if isinstance(rel, (int, float)):
                    rel_str = f"{rel:.2f}"
                else:
                    rel_str = str(rel)
                print(f"  {s['id']}  {rel_str}  {s.get('title', '')}")
        if count > len(summary):
            print(f"\n  ... and {count - len(summary)} more entries")
        print(f"\n  Use --json for full output or kanban knowledge get <id> for details")
        return

    if "domains" in data and not data.get("results"):
        domains = data["domains"]
        if isinstance(domains, list):
            for d in domains:
                if isinstance(d, dict):
                    print(f"  {d.get('name', d.get('domain', '?'))}  {d.get('count', '')}")
                else:
                    print(f"  {d}")
            print(f"\n  Total: {len(domains)} domains")
        return

    if "categories" in data and "severities" in data:
        cats = data["categories"]
        sevs = data["severities"]
        print(f"\n  Categories:")
        for k, v in cats.items():
            print(f"    {k:20s} {v}")
        print(f"\n  Severities:")
        for k, v in sevs.items():
            print(f"    {k:20s} {v}")
        return

    _render_json_fallback("knowledge", data)
