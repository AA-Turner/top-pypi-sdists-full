"""`/setup` — interactive wizard for LLM API configuration.

Walks the user through:
1. Pick a backend (Anthropic API direct, or AWS Bedrock for GovCloud)
2. Anthropic path: paste API key, validate with a tiny test query, persist
3. Bedrock path: verify boto3 creds resolve, list available Claude models,
   record the chosen region, persist

Persistence targets:
- `~/.efterlev/credentials.toml` (mode 0600) — per-user store, picked up
  by the Anthropic client + the `/ai` backend chooser.
- The workspace's `.efterlev/config.toml` `[llm]` section — updated when
  a workspace exists, so the agents (`/agent gap`, `/agent document`,
  `/agent remediate`) honor the chosen backend without a separate
  `efterlev init --llm-backend bedrock` step.

Honest scope:
- Validation does one ~$0.0001 test query to confirm the credential works.
- The wizard does NOT modify the user's shell profile (.bashrc / .zshrc).
- Bedrock setup assumes the user has already configured AWS creds via
  `aws configure` or env vars.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from prompt_toolkit import prompt as ptk_prompt
from rich.text import Text

if TYPE_CHECKING:
    from efterlev.shell.commands import ShellContext

ACCENT = "color(73)"
MUTED = "color(244)"
ERROR = "bold red"


def _update_workspace_llm_config(ctx, backend: str, model: str, region: str | None) -> bool:
    """Patch `.efterlev/config.toml` `[llm]` section in place.

    Returns True when the workspace config was found and updated; False
    when there's no workspace yet (the change is then unnecessary — the
    next `efterlev init` will pick up the credentials.toml).

    Uses a minimal rewriter (not a full TOML parser → serializer round-
    trip) because we want to preserve the customer's other config
    settings + comments verbatim. The `[llm]` section is replaced
    wholesale; everything else is untouched.
    """
    import re

    config_path = ctx.root / ".efterlev" / "config.toml"
    if not config_path.is_file():
        return False

    body = config_path.read_text(encoding="utf-8")

    # Build the replacement [llm] block.
    new_lines = ["[llm]", f'backend = "{backend}"', f'model = "{model}"']
    if region:
        new_lines.append(f'region = "{region}"')
    new_block = "\n".join(new_lines) + "\n"

    # Replace existing [llm] section (up to the next [section] header or EOF).
    pattern = re.compile(r"^\[llm\][^\[]*", re.MULTILINE)
    if pattern.search(body):
        body = pattern.sub(new_block + "\n", body, count=1)
    else:
        # No [llm] section; append.
        if not body.endswith("\n"):
            body += "\n"
        body += "\n" + new_block

    config_path.write_text(body, encoding="utf-8")
    return True


def run_setup(ctx: ShellContext) -> bool:
    """Execute the wizard. Returns True if credentials were written.

    Ctrl+C at any prompt aborts cleanly; shell continues.
    """
    console = ctx.console
    console.print()
    console.print(Text("  LLM setup", style="bold"))
    console.print()
    console.print(
        Text(
            "  Efterlev needs an LLM for the Gap Agent, Documentation Agent,\n"
            "  Remediation Agent, and /ai queries. Four backends are supported:\n",
            style=MUTED,
        )
    )
    console.print(
        Text("    1. ", style=ACCENT)
        + Text("Anthropic API direct", style="bold")
        + Text(
            "      — ~5 min setup, pay-as-you-go, ~$1-2 per /agent gap run",
            style=MUTED,
        )
    )
    console.print(
        Text("    2. ", style=ACCENT)
        + Text("AWS Bedrock", style="bold")
        + Text(
            "              — for GovCloud / FedRAMP-boundary deployments",
            style=MUTED,
        )
    )
    console.print(
        Text("    3. ", style=ACCENT)
        + Text("Claude Code subscription", style="bold")
        + Text(
            " — uses your Pro/Max plan; no per-token cost; requires `claude` CLI",
            style=MUTED,
        )
    )
    console.print(
        Text("    4. ", style=ACCENT)
        + Text("OpenAI API", style="bold")
        + Text(
            "               — for teams without Claude access; gpt-5.4-mini recommended",
            style=MUTED,
        )
    )
    console.print()

    try:
        choice = ptk_prompt("  Which? [1/2/3/4]: ").strip()
    except (KeyboardInterrupt, EOFError):
        console.print(Text("  setup cancelled", style=MUTED))
        return False

    if choice == "1":
        return _setup_anthropic(ctx)
    if choice == "2":
        return _setup_bedrock(ctx)
    if choice == "3":
        return _setup_claude_code(ctx)
    if choice == "4":
        return _setup_openai(ctx)
    console.print(Text(f"  unknown choice {choice!r}; expected 1, 2, 3, or 4", style=ERROR))
    return False


def _setup_claude_code(ctx: ShellContext) -> bool:
    """Configure the claude_code backend (v0.1.148 / #353, v0.1.150 / #355).

    No credentials to enter — Claude Code handles its own OAuth. We:
      1. Verify the `claude` binary is on PATH
      2. Send a 2-token "hi" prompt through the env-stripped subprocess
         to confirm OAuth is signed in (costs $0 on subscription)
      3. If sign-in fails, point user at the EXACT command to run in
         their regular terminal (not the efterlev shell — that's a
         common confusion)
      4. Note that ANTHROPIC_API_KEY is auto-stripped (v0.1.149)
      5. Write workspace config
    """
    import os

    from efterlev.errors import AgentError
    from efterlev.llm.base import LLMMessage
    from efterlev.llm.claude_code_client import ClaudeCodeClient, claude_cli_available

    console = ctx.console
    console.print()
    console.print(Text("  Claude Code (subscription) setup", style="bold"))
    console.print()
    if not claude_cli_available():
        console.print(
            Text("  error: `claude` CLI not found on PATH.\n", style=ERROR)
            + Text("  Install Claude Code first: ", style=MUTED)
            + Text("https://claude.com/claude-code\n", style=ACCENT)
            + Text("  Then sign in with your Pro or Max account.\n", style=MUTED)
        )
        return False
    console.print(Text("  ✓ `claude` CLI detected on PATH.", style=ACCENT))

    # v0.1.150 / #355: probe sign-in state with a tiny prompt. On
    # subscription this is free; on a stale API key it 401s and we tell
    # the user how to fix it.
    console.print(Text("  Checking subscription sign-in...", style=MUTED))
    probe_client = ClaudeCodeClient()
    try:
        probe_client.complete(
            system="Respond with the single word: ok",
            messages=[LLMMessage(content="ping")],
            model="claude-haiku-4-5",
        )
    except AgentError as e:
        msg = str(e)
        if "401" in msg or "Invalid" in msg or "sign" in msg.lower():
            console.print()
            console.print(Text("  ✗ Claude Code is NOT signed in.\n", style=ERROR))
            console.print(
                Text("  To sign in:\n", style=MUTED)
                + Text("    1. Open a NEW terminal window (not this shell)\n", style=MUTED)
                + Text("    2. Run: ", style=MUTED)
                + Text("claude\n", style=ACCENT)
                + Text("    3. Follow the OAuth flow in your browser\n", style=MUTED)
                + Text("    4. Once signed in, come back here and run ", style=MUTED)
                + Text("/setup", style=ACCENT)
                + Text(" again\n", style=MUTED)
            )
            return False
        console.print()
        console.print(
            Text("  ✗ Claude Code probe failed: ", style=ERROR) + Text(msg[:200], style=MUTED)
        )
        return False
    console.print(Text("  ✓ Claude Code is signed in (probe responded).", style=ACCENT))

    if os.environ.get("ANTHROPIC_API_KEY"):
        console.print()
        console.print(
            Text("  note: ANTHROPIC_API_KEY is set in your environment.\n", style=MUTED)
            + Text(
                "  When efterlev calls `claude --print`, the env var is\n"
                "  stripped from the subprocess so subscription OAuth takes\n"
                "  effect. Your shell + other tools still see the variable\n"
                "  (v0.1.149 / #354).\n",
                style=MUTED,
            )
        )

    console.print()
    console.print(
        Text(
            "  Heads-up:\n"
            "  - This routes every LLM call through `claude --print`.\n"
            "  - Cost is your flat Pro/Max subscription; per-call billing is $0.\n"
            "  - Anthropic's subscription ToS doesn't explicitly bless third-\n"
            "    party tool integrations; use your judgment.\n",
            style=MUTED,
        )
    )

    # v0.1.160 / #365: align with v0.1.158 `efterlev init --llm-backend=
    # claude_code` which writes `fallback_model = "claude-opus-4-7"` on
    # this backend. On Claude Code Pro/Max all models bill against the
    # same subscription quota — Opus is free upside vs Sonnet. The
    # wizard previously wrote Sonnet here, which was inconsistent.
    if _update_workspace_llm_config(ctx, "claude_code", "claude-opus-4-7", region=None):
        console.print(
            Text("  ✓ updated ", style=ACCENT)
            + Text(".efterlev/config.toml", style=ACCENT)
            + Text(" [llm] section (backend=claude_code, model=claude-opus-4-7)", style=MUTED)
        )
    else:
        console.print(
            Text(
                "  note: no workspace at this root; backend choice will apply\n"
                "  to the next `/init` run.",
                style=MUTED,
            )
        )
    return True


def _setup_anthropic(ctx: ShellContext) -> bool:
    """Walk through Anthropic API key entry + validation + persistence."""
    console = ctx.console
    console.print()
    console.print(Text("  Anthropic API setup", style="bold"))
    console.print()
    console.print(
        Text("  1. Open this URL in your browser:\n", style=MUTED)
        + Text("       https://console.anthropic.com/settings/keys\n", style=ACCENT)
        + Text(
            "  2. Create a key (any name; 'efterlev' is fine).\n"
            "  3. Paste the key here — starts with `sk-ant-`.\n",
            style=MUTED,
        )
    )

    try:
        key = ptk_prompt("  API key: ", is_password=True).strip()
    except (KeyboardInterrupt, EOFError):
        console.print(Text("  setup cancelled", style=MUTED))
        return False

    if not key:
        console.print(Text("  no key entered; setup cancelled", style=MUTED))
        return False
    if not key.startswith("sk-ant-"):
        console.print(
            Text(
                f"  warning: key doesn't start with 'sk-ant-' (got prefix {key[:8]!r}); "
                "continuing anyway",
                style=MUTED,
            )
        )

    # Validate with a tiny query.
    console.print()
    console.print(Text("  Validating key with a 1-token test query...", style=MUTED))
    try:
        from anthropic import Anthropic

        client = Anthropic(api_key=key)
        response = client.messages.create(
            model="claude-haiku-4-5",
            max_tokens=1,
            messages=[{"role": "user", "content": "hi"}],
        )
        _ = response  # consume
    except Exception as e:
        console.print(Text(f"  ✗ validation failed: {type(e).__name__}: {e}", style=ERROR))
        console.print(
            Text(
                "    The key was NOT saved. Check it on the Anthropic console and re-run /setup.",
                style=MUTED,
            )
        )
        return False

    console.print(Text("  ✓ key works (model: claude-haiku-4-5)", style=ACCENT))

    # Persist.
    from efterlev.shell.credentials import (
        CREDENTIALS_PATH,
        Credentials,
        load_credentials,
        save_credentials,
    )

    existing = load_credentials()
    save_credentials(
        Credentials(
            anthropic_api_key=key,
            bedrock_region=existing.bedrock_region,  # preserve if already set
            default_model=existing.default_model,
        )
    )
    console.print(
        Text("  ✓ stored in ", style=ACCENT)
        + Text(str(CREDENTIALS_PATH), style="")
        + Text(" (mode 0600)", style=MUTED)
    )

    # If a workspace exists, point its [llm] section at the Anthropic backend
    # so agent commands honor the choice without a separate `efterlev init`.
    if _update_workspace_llm_config(ctx, "anthropic", "claude-opus-4-7", region=None):
        console.print(
            Text("  ✓ updated ", style=ACCENT)
            + Text(str(ctx.root / ".efterlev" / "config.toml"), style="")
            + Text(" [llm] section", style=MUTED)
        )

    console.print()
    console.print(
        Text("  Ready. Try ", style=MUTED)
        + Text('/ai "where do I start?"', style=ACCENT)
        + Text(" or ", style=MUTED)
        + Text("/agent gap", style=ACCENT)
        + Text(".", style=MUTED)
    )
    console.print()
    return True


def _setup_openai(ctx: ShellContext) -> bool:
    """Walk through OpenAI API key entry + validation + persistence.

    Parallels `_setup_anthropic`. Validates by listing models (free; also
    confirms whether the key's project has the recommended model enabled —
    the project-scoping gotcha the v0.1.213 `list_openai_models` diagnostic
    was built for), then pins `gpt-5.4-mini` (or `gpt-5` if that's the only
    validated model the key can reach) into the workspace [llm] section.
    """
    console = ctx.console
    console.print()
    console.print(Text("  OpenAI API setup", style="bold"))
    console.print()
    console.print(
        Text("  1. Open this URL in your browser:\n", style=MUTED)
        + Text("       https://platform.openai.com/api-keys\n", style=ACCENT)
        + Text(
            "  2. Create a key (any name; 'efterlev' is fine).\n"
            "  3. Paste the key here — starts with `sk-` (often `sk-proj-…`).\n",
            style=MUTED,
        )
    )

    try:
        key = ptk_prompt("  API key: ", is_password=True).strip()
    except (KeyboardInterrupt, EOFError):
        console.print(Text("  setup cancelled", style=MUTED))
        return False

    if not key:
        console.print(Text("  no key entered; setup cancelled", style=MUTED))
        return False
    if not key.startswith("sk-"):
        hint = ""
        if key.startswith("sk-ant-"):
            hint = " (that looks like an Anthropic key — use option 1 for Anthropic)"
        console.print(
            Text(
                f"  warning: key doesn't start with 'sk-' (got prefix {key[:7]!r})"
                f"{hint}; continuing anyway",
                style=MUTED,
            )
        )

    # Validate by listing models — free, and surfaces the project-scoping
    # gotcha (key valid but recommended model not enabled in its project).
    console.print()
    console.print(Text("  Validating key (listing available models)...", style=MUTED))
    try:
        from openai import OpenAI

        client = OpenAI(api_key=key)
        available = sorted(m.id for m in client.models.list())
    except Exception as e:
        console.print(Text(f"  ✗ validation failed: {type(e).__name__}: {e}", style=ERROR))
        console.print(
            Text(
                "    The key was NOT saved. Check it on the OpenAI dashboard and re-run /setup.",
                style=MUTED,
            )
        )
        return False

    # Pick the model: prefer the recommended gpt-5.4-mini, fall back to gpt-5
    # if that's the only validated model the key can reach.
    if "gpt-5.4-mini" in available:
        chosen_model = "gpt-5.4-mini"
        console.print(Text("  ✓ key works; gpt-5.4-mini is enabled", style=ACCENT))
    elif "gpt-5" in available:
        chosen_model = "gpt-5"
        console.print(
            Text("  ✓ key works, but gpt-5.4-mini is NOT enabled — using gpt-5", style=ACCENT)
            + Text(" (also validated v0.1.213, ~5x the cost)", style=MUTED)
        )
    else:
        chosen_model = "gpt-5.4-mini"
        console.print(
            Text(
                "  ⚠ key works, but neither gpt-5.4-mini nor gpt-5 is enabled for\n"
                "    this key's project. Writing gpt-5.4-mini anyway — enable it at\n"
                "    https://platform.openai.com/settings, or the first agent call\n"
                "    will return model_not_found.",
                style=MUTED,
            )
        )

    # Persist (preserve any already-configured fields).
    from efterlev.shell.credentials import (
        CREDENTIALS_PATH,
        Credentials,
        load_credentials,
        save_credentials,
    )

    existing = load_credentials()
    save_credentials(
        Credentials(
            anthropic_api_key=existing.anthropic_api_key,
            bedrock_region=existing.bedrock_region,
            default_model=existing.default_model,
            openai_api_key=key,
        )
    )
    console.print(
        Text("  ✓ stored in ", style=ACCENT)
        + Text(str(CREDENTIALS_PATH), style="")
        + Text(" (mode 0600)", style=MUTED)
    )

    if _update_workspace_llm_config(ctx, "openai", chosen_model, region=None):
        console.print(
            Text("  ✓ updated ", style=ACCENT)
            + Text(str(ctx.root / ".efterlev" / "config.toml"), style="")
            + Text(f" [llm] section (backend=openai, model={chosen_model})", style=MUTED)
        )

    console.print()
    console.print(
        Text("  Note: OpenAI is validated on one fixture (v0.1.213). For final\n", style=MUTED)
        + Text(
            "  3PAO submission, re-run on Anthropic / Bedrock / Claude Code and\n"
            "  diff. See LIMITATIONS.md “OpenAI backend”.\n",
            style=MUTED,
        )
    )
    console.print(
        Text("  Ready. Try ", style=MUTED)
        + Text('/ai "where do I start?"', style=ACCENT)
        + Text(" or ", style=MUTED)
        + Text("/agent gap", style=ACCENT)
        + Text(".", style=MUTED)
    )
    console.print()
    return True


def _setup_bedrock(ctx: ShellContext) -> bool:
    """Verify AWS Bedrock is reachable; record region preference."""
    console = ctx.console
    console.print()
    console.print(Text("  AWS Bedrock setup", style="bold"))
    console.print()
    console.print(
        Text(
            "  Bedrock uses your standard AWS credentials (via boto3). Before\n"
            "  running this wizard, make sure you've done:\n",
            style=MUTED,
        )
    )
    console.print(
        Text("    aws configure", style=ACCENT)
        + Text("                    # or set AWS_ACCESS_KEY_ID / _SECRET_ACCESS_KEY", style=MUTED)
    )
    console.print(
        Text("    # And requested model access for Claude in the Bedrock console:", style=MUTED)
    )
    console.print(
        Text("    https://console.aws.amazon.com/bedrock/home#/modelaccess", style=ACCENT)
    )
    console.print()

    try:
        region = ptk_prompt("  AWS region [us-east-1]: ").strip() or "us-east-1"
    except (KeyboardInterrupt, EOFError):
        console.print(Text("  setup cancelled", style=MUTED))
        return False

    # Verify boto3 can resolve creds + reach STS in this region.
    console.print()
    console.print(Text(f"  Verifying AWS credentials in {region}...", style=MUTED))
    try:
        import boto3
        from botocore.exceptions import BotoCoreError, ClientError

        sts = boto3.client("sts", region_name=region)
        identity = sts.get_caller_identity()
        account = identity.get("Account", "?")
        arn = identity.get("Arn", "?")
    except (BotoCoreError, ClientError) as e:
        console.print(Text(f"  ✗ AWS credentials not working: {e}", style=ERROR))
        console.print(
            Text(
                "    Run `aws configure` then re-run /setup.",
                style=MUTED,
            )
        )
        return False
    except ImportError:
        console.print(
            Text("  ✗ boto3 not installed. Run `pipx inject efterlev boto3` first.", style=ERROR)
        )
        return False

    console.print(Text(f"  ✓ AWS account {account} ({arn})", style=ACCENT))

    # Verify Bedrock InvokeModel is reachable (a 1-token test query against Haiku).
    console.print(
        Text(f"  Verifying Bedrock model access for Claude Haiku 4.5 in {region}...", style=MUTED)
    )
    try:
        bedrock = boto3.client("bedrock-runtime", region_name=region)
        bedrock.converse(
            modelId="us.anthropic.claude-haiku-4-5-20251001-v1:0",
            messages=[{"role": "user", "content": [{"text": "hi"}]}],
            inferenceConfig={"maxTokens": 1},
        )
    except ClientError as e:
        err_code = e.response.get("Error", {}).get("Code", "?")
        console.print(Text(f"  ✗ Bedrock InvokeModel failed ({err_code}): {e}", style=ERROR))
        console.print(
            Text(
                "    Likely cause: model access not granted in this region. Open\n"
                "    the link above and enable Claude Haiku 4.5 + Claude Sonnet 4.6.",
                style=MUTED,
            )
        )
        return False

    console.print(Text("  ✓ Bedrock Claude Haiku 4.5 reachable", style=ACCENT))

    # Persist.
    from efterlev.shell.credentials import (
        CREDENTIALS_PATH,
        Credentials,
        load_credentials,
        save_credentials,
    )

    existing = load_credentials()
    save_credentials(
        Credentials(
            anthropic_api_key=existing.anthropic_api_key,  # preserve if already set
            bedrock_region=region,
            default_model=existing.default_model,
        )
    )
    console.print(
        Text("  ✓ stored in ", style=ACCENT)
        + Text(str(CREDENTIALS_PATH), style="")
        + Text(" (mode 0600)", style=MUTED)
    )

    # If a workspace exists, point its [llm] section at Bedrock so agent
    # commands honor the choice without a separate `efterlev init`.
    bedrock_model = "us.anthropic.claude-haiku-4-5-20251001-v1:0"
    if _update_workspace_llm_config(ctx, "bedrock", bedrock_model, region=region):
        console.print(
            Text("  ✓ updated ", style=ACCENT)
            + Text(str(ctx.root / ".efterlev" / "config.toml"), style="")
            + Text(f" [llm] section (backend=bedrock, region={region})", style=MUTED)
        )

    console.print()
    console.print(
        Text("  Ready. ", style=MUTED)
        + Text('/ai "where do I start?"', style=ACCENT)
        + Text(" and ", style=MUTED)
        + Text("/agent gap", style=ACCENT)
        + Text(" now both route through Bedrock (Haiku 4.5).", style=MUTED)
    )
    console.print()
    return True
