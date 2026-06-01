"""`/ai <question>` — single-shot AI Q&A with workspace context.

Per the locked design: single-shot (no persistent chat), grounded in
the current workspace snapshot, AI prints suggested commands rather
than auto-running them. Default model: Sonnet 4.6 (good balance of
quality and cost for Q&A).

System prompt is composed from three parts:
1. Static domain primer (Efterlev concepts: KSIs, FRMR, agents, the pipeline)
2. Live workspace snapshot (state, evidence count, classifications if any)
3. Live slash command catalog (every command with its summary)

What the AI never sees:
- Raw evidence content (privacy: might contain redacted secrets in metadata)
- Provenance record bodies (too much; suggest /provenance show <id> instead)
- Full FRMR catalog (~1MB; too expensive)
- Session command history (v1 is single-shot)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from rich.text import Text

if TYPE_CHECKING:
    from efterlev.shell.commands import ShellContext

ACCENT = "color(73)"
MUTED = "color(244)"
ERROR = "bold red"

DEFAULT_ANTHROPIC_MODEL = "claude-sonnet-4-6"
DEFAULT_BEDROCK_MODEL = "us.anthropic.claude-haiku-4-5-20251001-v1:0"


DOMAIN_PRIMER = """\
You are the Efterlev shell assistant. Efterlev is an open-source FedRAMP 20x
compliance scanner: it reads AWS infrastructure-as-code (Terraform, CloudFormation,
CDK Python) and classifies it against the 60 Key Security Indicators (KSIs) of
FedRAMP 20x, drafts FRMR-compatible attestations, and proposes Terraform remediations.

Key concepts:
- KSI = Key Security Indicator (e.g. KSI-CNA-RNT "Restricting Network Traffic")
- FRMR = the machine-readable format FedRAMP 20x is standardizing on
- 3PAO = Third-Party Assessment Organization (independent auditor)
- POA&M = Plan of Action and Milestones (the punch list of open gaps)
- The pipeline is: init → scan → agent gap → agent document → poam
- "Gap Agent" classifies KSIs against evidence (uses Claude Opus by default)
- "Documentation Agent" drafts FRMR JSON + HTML report
- "Remediation Agent" produces Terraform diffs that close specific gaps

Your job: help the user use Efterlev. You are NOT a general-purpose assistant.
If asked something off-topic (general AWS, non-Efterlev compliance, etc.), give
a brief one-sentence answer and steer back to Efterlev.

Behavior rules:
- Be terse. Default to 2-3 sentence responses. Expand only when explaining a concept.
- When you suggest a command, format it as `/command` so the UI highlights it.
- Never claim a command exists that's not in the catalog below.
- Never auto-run anything; you only suggest.
- Cite real numbers when the workspace snapshot gives them (e.g. evidence count).
- When suggesting /agent gap, mention the cost (~$1-2 on Opus, ~$0.40 on Bedrock Haiku).
- Use plain text. No emojis. No markdown tables.
"""


def _build_workspace_section(ctx: ShellContext) -> str:
    """Snapshot the workspace state in compact JSON-ish form for the prompt."""
    import json

    from efterlev.shell.state import read_snapshot

    snap = read_snapshot(ctx.root)
    data = {
        "root": str(snap.root),
        "initialized": snap.initialized,
        "baseline": snap.baseline,
        "evidence_count": snap.evidence_count,
        "claim_count": snap.claim_count,
        "last_scan_at": snap.last_scan_at.isoformat() if snap.last_scan_at else None,
        "cumulative_cost_usd": round(snap.total_cost_usd, 4)
        if snap.total_cost_usd is not None
        else None,
        "models_used": sorted(snap.cost_by_model.keys()),
    }
    return "Current workspace state (live, just-read):\n" + json.dumps(data, indent=2)


def _build_command_catalog() -> str:
    """Render the slash-command registry as a catalog string for the prompt."""
    from efterlev.shell.commands import COMMANDS

    lines = ["Available slash commands (the AI suggests these by name):"]
    for c in COMMANDS:
        arg = f" {c.arg_hint}" if c.arg_hint else ""
        lines.append(f"  {c.name}{arg}  — {c.summary}")
    return "\n".join(lines)


def _build_system_prompt(ctx: ShellContext) -> str:
    return (
        DOMAIN_PRIMER + "\n\n" + _build_workspace_section(ctx) + "\n\n" + _build_command_catalog()
    )


def run_ai_query(ctx: ShellContext, question: str) -> bool:
    """Send a single-shot Q&A to whichever LLM backend `/setup` configured.

    Resolution order:
      1. Anthropic API direct (when ANTHROPIC_API_KEY env or credentials.toml
         has a key). Sonnet 4.6 default; streams natively.
      2. AWS Bedrock (when credentials.toml has bedrock_region but no
         Anthropic key). Haiku 4.5 default; non-streaming (Bedrock Converse
         is one-shot, but we batch-print the result and append the cost
         line the same way).
      3. Neither → point at /setup.
    """
    console = ctx.console

    if not question.strip():
        from efterlev.shell.layout import render_error

        render_error(
            console,
            "/ai needs a question",
            hint='try /ai "how do I start?"',
        )
        return False

    # Pick a backend based on what /setup configured.
    from efterlev.shell.credentials import load_credentials, resolve_anthropic_api_key

    creds = load_credentials()
    api_key = resolve_anthropic_api_key()

    if api_key:
        return _run_anthropic_query(ctx, question, api_key)
    if creds.has_bedrock:
        return _run_bedrock_query(ctx, question, creds.bedrock_region or "us-east-1")

    from efterlev.shell.layout import render_error

    render_error(
        console,
        "no LLM backend configured",
        hint="run /setup to configure Anthropic API or AWS Bedrock (~5 min)",
    )
    return False


def _run_anthropic_query(ctx: ShellContext, question: str, api_key: str) -> bool:
    """Anthropic API direct path. Streams the response."""
    console = ctx.console
    system_prompt = _build_system_prompt(ctx)

    try:
        from anthropic import Anthropic
    except ImportError:
        from efterlev.shell.layout import render_error

        render_error(console, "anthropic SDK not installed")
        return False

    client = Anthropic(api_key=api_key)

    console.print()
    try:
        with client.messages.stream(
            model=DEFAULT_ANTHROPIC_MODEL,
            max_tokens=1024,
            system=system_prompt,
            messages=[{"role": "user", "content": question}],
        ) as stream:
            for text_delta in stream.text_stream:
                console.print(text_delta, end="")
            console.print()
            final_message = stream.get_final_message()
    except Exception as e:
        from efterlev.shell.layout import render_error

        render_error(
            console,
            f"/ai query failed: {type(e).__name__}: {e}",
            hint="check your API key with /setup, or your network",
        )
        return False

    in_toks = final_message.usage.input_tokens
    out_toks = final_message.usage.output_tokens
    _emit_cost_line(ctx, DEFAULT_ANTHROPIC_MODEL, in_toks, out_toks)
    return False


def _run_bedrock_query(ctx: ShellContext, question: str, region: str) -> bool:
    """AWS Bedrock path. Non-streaming; prints the full response after the call."""
    console = ctx.console
    system_prompt = _build_system_prompt(ctx)

    try:
        import boto3
        from botocore.exceptions import BotoCoreError, ClientError
    except ImportError:
        from efterlev.shell.layout import render_error

        render_error(
            console,
            "boto3 not installed",
            hint="install with `pipx inject efterlev boto3`",
        )
        return False

    bedrock = boto3.client("bedrock-runtime", region_name=region)
    console.print()
    try:
        response = bedrock.converse(
            modelId=DEFAULT_BEDROCK_MODEL,
            system=[{"text": system_prompt}],
            messages=[{"role": "user", "content": [{"text": question}]}],
            inferenceConfig={"maxTokens": 1024},
        )
    except (BotoCoreError, ClientError) as e:
        from efterlev.shell.layout import render_error

        render_error(
            console,
            f"/ai query failed: {type(e).__name__}: {e}",
            hint="check your AWS credentials with /setup, or your network",
        )
        return False

    # Bedrock Converse returns one block; print it.
    text = ""
    for block in response.get("output", {}).get("message", {}).get("content", []):
        text += block.get("text", "")
    console.print(text)

    usage = response.get("usage", {})
    in_toks = int(usage.get("inputTokens", 0))
    out_toks = int(usage.get("outputTokens", 0))
    _emit_cost_line(ctx, DEFAULT_BEDROCK_MODEL, in_toks, out_toks)
    return False


def _emit_cost_line(ctx: ShellContext, model: str, in_toks: int, out_toks: int) -> None:
    """Print the one-line cost summary + append to receipts.log."""
    from efterlev.llm.pricing import estimate_cost_usd

    cost = estimate_cost_usd(model, in_toks, out_toks)
    cost_str = f"~${cost:.4f}" if cost is not None else "pricing not registered"

    ctx.console.print()
    ctx.console.print(
        Text(
            f"  [{model} · {in_toks:,} in / {out_toks:,} out · {cost_str}]",
            style=MUTED,
        )
    )
    ctx.console.print()

    _append_to_receipts(ctx, model, in_toks, out_toks)


def _append_to_receipts(ctx: ShellContext, model: str, in_tok: int, out_tok: int) -> None:
    """Best-effort: write the /ai call to .efterlev/receipts.log so /cost sees it.

    Silently no-ops when the workspace isn't initialized — /ai works without
    /init (e.g. asking "where do I start?" before any setup), so the cost
    tracking is opportunistic, not load-bearing.
    """
    receipts_dir = ctx.root / ".efterlev"
    if not receipts_dir.is_dir():
        return
    import json
    from datetime import UTC, datetime

    entry = {
        "ts": datetime.now(UTC).isoformat(),
        "model": model,
        "input_tokens": in_tok,
        "output_tokens": out_tok,
        "source": "shell_ai",
    }
    try:
        with open(receipts_dir / "receipts.log", "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
    except OSError:
        pass  # non-fatal
