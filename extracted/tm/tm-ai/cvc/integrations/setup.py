"""
Interactive setup helpers for CVC channels.

Used by ``cvc setup`` (via ``cvc.cli``) and reachable directly from any
script that wants to drive a user through channel configuration.

The wizard introspects each adapter's :attr:`BaseChannelAdapter.config_schema`
attribute — every field declares its key, label, help text, secret flag,
kind, and required/default — so adding a new channel's CLI prompts is
zero additional work: just add the schema to the adapter class and the
setup wizard picks it up.

Config persistence:
  Channel configs live at ``~/.cvc/channels/<name>.yaml`` (one file
  per adapter). The gateway loads every present file at startup and
  passes the dict to the matching adapter. This isolates secrets from
  the main ``~/.cvc/config.yaml`` and makes per-channel rotation
  trivial — delete one file, the channel stops.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple


logger = logging.getLogger(__name__)


try:
    import yaml  # PyYAML — already a CVC core dep
except Exception:  # noqa: BLE001
    yaml = None  # type: ignore[assignment]


# Type alias for the optional prompt callback. The CLI passes in
# ``click.prompt``; tests can pass any object with the same shape.
PromptFn = Callable[..., str]


class WizardCancelled(Exception):
    """Raised by the wizard when the user cancels (Ctrl+C, Escape,
    EOF on stdin).

    The wizard callers catch this and route the user back to the
    enclosing menu rather than treating it as a real exception. This
    keeps Ctrl+C from killing the entire ``cvc setup`` session — it
    just unwinds one level.
    """


# ─────────────────────────────────────────────────────────────────────────────
# Per-channel config file helpers
# ─────────────────────────────────────────────────────────────────────────────


def channels_dir() -> Path:
    """``~/.cvc/channels`` — created on demand."""
    p = Path.home() / ".cvc" / "channels"
    p.mkdir(parents=True, exist_ok=True)
    return p


def channels_config_path(name: str) -> Path:
    """The yaml file holding one channel's config."""
    return channels_dir() / f"{name}.yaml"


def read_channels_config(name: str) -> Dict[str, Any]:
    """Load the saved config for *name* (empty dict if not present)."""
    return read_channels_config_from_path(channels_config_path(name))


def read_channels_config_from_path(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    try:
        text = path.read_text(encoding="utf-8")
        if yaml is not None:
            data = yaml.safe_load(text)
            return dict(data) if isinstance(data, dict) else {}
        # Fallback: minimal JSON-ish parse (still valid YAML for primitives).
        try:
            data = json.loads(text)
        except Exception:
            return {}
        return dict(data) if isinstance(data, dict) else {}
    except Exception as exc:  # noqa: BLE001
        logger.warning("channels_config: failed to read %s: %s", path, exc)
        return {}


def save_channels_config(name: str, config: Dict[str, Any]) -> Path:
    """Persist *config* for *name* and return the file path."""
    return save_channels_config_to_path(channels_config_path(name), config)


def save_channels_config_to_path(path: Path, config: Dict[str, Any]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    if yaml is not None:
        path.write_text(
            yaml.dump(dict(config), default_flow_style=False, allow_unicode=True, sort_keys=False),
            encoding="utf-8",
        )
    else:
        path.write_text(json.dumps(dict(config), indent=2, ensure_ascii=False), encoding="utf-8")
    try:
        path.chmod(0o600)  # secrets: owner read/write only
    except OSError:
        pass
    return path


def list_all_saved_channels() -> List[Tuple[str, Path]]:
    """Return ``[(name, path)]`` for every channel yaml file on disk.

    Auto-cleans the ``*.yaml.yaml`` shadow files that older setup-wizard
    versions (or the ``save_channels_config`` path passed where a name
    was expected) can leave behind. Those shadows NEVER match the
    gateway loader's ``*.yaml`` glob, so they silently disable the
    channel — a dangerous footgun. The cleanup is best-effort: any
    failure to delete just logs and continues.
    """
    out: List[Tuple[str, Path]] = []
    if not channels_dir().exists():
        return out
    # Pre-cleanup: remove any *.yaml.yaml shadow files from prior bugs.
    try:
        for _shadow in channels_dir().glob("*.yaml.yaml"):
            try:
                _shadow.unlink()
                logger.info("Removed stale channel shadow: %s", _shadow.name)
            except OSError as _e:
                logger.warning("Could not remove shadow %s: %s", _shadow.name, _e)
    except Exception as _e:  # noqa: BLE001
        logger.warning("Channel shadow cleanup skipped: %s", _e)
    for p in sorted(channels_dir().glob("*.yaml")):
        out.append((p.stem, p))
    return out


def schema_for(channel_name: str) -> List[Dict[str, Any]]:
    """Return the config_schema for *channel_name* (empty list if unknown)."""
    from .bootstrap import get_registry
    reg = get_registry()
    adapter = reg.get(channel_name)
    if adapter is None:
        return []
    return list(getattr(adapter, "config_schema", []) or [])


# ─────────────────────────────────────────────────────────────────────────────
# Setup listing + prompting
# ─────────────────────────────────────────────────────────────────────────────


def list_channels_for_setup() -> List[Tuple[str, str, str]]:
    """Return ``[(registry_name, display_name, description)]`` for every
    registered channel — sorted with Telegram first, then alphabetical.

    Used by the CLI to build the "Pick a channel" submenu.
    """
    from .bootstrap import get_registry

    reg = get_registry()
    out: List[Tuple[str, str, str]] = []
    for name in reg.list_names():
        adapter = reg.get(name)
        if adapter is None:
            continue
        out.append((
            adapter.name,
            getattr(adapter, "display_name", adapter.name),
            getattr(adapter, "description", ""),
        ))
    # Priority: telegram first, then alphabetical.
    out.sort(key=lambda t: (t[0] != "telegram", t[0]))
    return out


def run_channel_setup(
    channel_name: str,
    prompt_fn: Optional[PromptFn] = None,
    confirm_fn: Optional[Callable[[str, bool], bool]] = None,
    existing: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Drive a user through one channel's config_schema prompts and
    return the resulting config dict.

    Args:
        channel_name: the registry name (e.g. ``"telegram"``).
        prompt_fn: optional callable matching the :data:`PromptFn`
            signature. Used by tests/scripts. Defaults to a Rich-
            based prompt that handles hidden input, defaults, and
            secret masking correctly — bypasses click's broken
            ``hide_input=True`` + ``show_default=True`` combination.
        confirm_fn: ``(message, default) -> bool`` callable. Defaults
            to Rich's Confirm.
        existing: optional dict of previously-saved config values for
            this channel (read from ``~/.cvc/channels/<name>.yaml``).
            When supplied, each field's *existing* value is shown as the
            default — empty input keeps the value, typing a new one
            overwrites. Secrets show a masked placeholder ("●●●●●●●●")
            instead of the actual token, with "(press Enter to keep
            current value)" as the prompt suffix. This is what fixes
            the "wizard re-asks for the token on every re-run" bug —
            the second run sees the saved token, masks it, and lets
            the user press Enter to skip re-typing.

    Returns:
        A dict mapping the adapter's config keys to the values the
        user entered. Empty if the channel name is unknown or the user
        skipped a required field.
    """
    from .bootstrap import get_registry

    reg = get_registry()
    adapter = reg.get(channel_name)
    if adapter is None:
        raise KeyError(f"no channel registered: {channel_name}")
    schema: List[Dict[str, Any]] = list(getattr(adapter, "config_schema", []) or [])
    if not schema:
        logger.info("channel %r has no config schema — nothing to set up", channel_name)
        return {}

    if prompt_fn is None:
        prompt_fn = _default_prompt
    if confirm_fn is None:
        confirm_fn = _default_confirm

    existing = dict(existing or {})
    result: Dict[str, Any] = {}
    print()  # blank line before prompts
    try:
        for field in schema:
            key = field["key"]
            label = field.get("label", key)
            help_text = field.get("help", "")
            kind = field.get("kind", "str")
            schema_default = field.get("default")
            # `required` defaults to False here because the adapter
            # schemas that DON'T mark a field required (parse_mode,
            # stream_edits, webhook_url, etc.) all rely on a schema-level
            # default and treat empty input as "use the default". Default
            # to True was wrong — it made every unmarked field block on
            # empty input, which fights the "press Enter to keep"
            # contract we just added.
            required = bool(field.get("required", False))
            secret = bool(field.get("secret", False))
            choices = field.get("choices")

            # Resolve the effective default + display value.
            #   1. existing[key] wins (last-saved wins, even over schema default).
            #   2. schema_default next (from the adapter class).
            #   3. None (prompt will require non-empty input).
            if key in existing and existing[key] is not None:
                effective_default = existing[key]
            elif schema_default is not None:
                effective_default = schema_default
            else:
                effective_default = None
            has_default = effective_default is not None

            # What to DISPLAY in the prompt suffix. For secrets we
            # never echo the real value — show a mask + a hint so the
            # user knows the field is already filled and they can
            # press Enter to keep it. For non-secrets we show the
            # effective default verbatim. For list[str] we never pass
            # the mask as the prompt default (otherwise click/Rich
            # would substitute it as the user's "answer", giving us
            # the bug we saw in the screenshot where the secret mask
            # leaked into allowlist as garbage).
            if has_default:
                if secret:
                    display_default = "●●●●●●●●"
                    keep_hint = "  [dim](press Enter to keep current value)[/dim]"
                else:
                    display_default = str(effective_default)
                    keep_hint = ""
            else:
                display_default = None
                keep_hint = ""

            # CRITICAL: when the field kind is a list (comma-separated
            # input), and we have NO existing value to display, don't
            # show ANY default — otherwise Rich's `default=...` would
            # substitute the mask as the user's first list item, which
            # is exactly what produced ['●●●●●●●●'] in the prior bug.
            # For non-secret lists with a real default we'd need a
            # different rendering, but for now we keep this safe: only
            # render `show_default` when the field is a simple str/int/
            # bool kind (not list or dict).
            show_default = has_default and kind in {"str", "int", "float", "bool"}

            if help_text:
                print(f"  [dim]{help_text}[/dim]")

            while True:
                raw = prompt_fn(
                    f"  {label}{keep_hint}",
                    default=display_default if show_default else None,
                    hide_input=secret,
                    show_default=show_default,
                    type=None,
                )
                raw = (raw or "").strip()

                # Empty input handling.
                #   (a) No default + empty → required field, must re-prompt.
                #   (b) Default present + empty → KEEP the default
                #       (the bug fix: was infinite-loop).
                #   (c) Default present + empty + optional → keep.
                if not raw:
                    if has_default:
                        result[key] = effective_default
                        break
                    if required:
                        print(f"  [yellow]This field is required.[/yellow]")
                        continue
                    break

                try:
                    coerced = _coerce(raw, kind, choices)
                except ValueError as exc:
                    print(f"  [red]✗ {exc}[/red]")
                    continue
                if coerced is None and not required:
                    result.pop(key, None)
                else:
                    result[key] = coerced
                break
    except (WizardCancelled, KeyboardInterrupt, EOFError) as _exc:
        # The user pressed Ctrl+C or hit Escape mid-wizard. We don't
        # save anything (we never reached the persist step). Always
        # re-raise as WizardCancelled so callers only need to catch
        # one exception type — they don't have to handle bare
        # KeyboardInterrupt (which would normally exit Python).
        # The original cause is preserved via __cause__.
        print()  # newline so the next menu doesn't start on the same line
        raise WizardCancelled() from _exc

    # ── Live validation (best-effort, never blocks) ──────────────────────
    #
    # After every field is collected, give the channel's validator a
    # chance to prove the config actually works (Telegram: real
    # ``Bot.get_me()`` call; SMTP: STARTTLS probe; etc.). If the
    # validator returns a non-empty error string we raise
    # ``WizardCancelled`` so the wizard exits cleanly without saving
    # — the user can re-run and fix the bad field. If the validator
    # returns ``None`` (no validator installed for this channel) we
    # skip silently to preserve backwards compatibility with the
    # existing channels that haven't migrated yet.
    if result:
        validation_err = validate_channel_config(channel_name, result)
        if validation_err:
            print(f"  [bold #CC3333]✗ Live validation failed:[/bold #CC3333] {validation_err}")
            print()
            print("  [dim]Nothing was saved. Re-run the wizard and paste a fresh token.[/dim]")
            raise WizardCancelled() from None

    return result


def truncate_for_display(value: Any, max_len: int = 40) -> str:
    """Pretty-print a config value for the "existing config" summary."""
    if value is None:
        return "—"
    if isinstance(value, list):
        if len(value) == 0:
            return "[]"
        if len(value) == 1:
            return f"[{truncate_for_display(value[0], max_len)}]"
        return f"[{truncate_for_display(value[0], max_len)}, … (+{len(value) - 1})]"
    if isinstance(value, dict):
        return "{…}"
    s = str(value)
    if len(s) > max_len:
        return s[: max_len - 1] + "…"
    return s


def _coerce(raw: str, kind: str, choices: Optional[List[Any]]) -> Any:
    """Convert a raw prompt string into the typed value the adapter wants."""
    if not raw:
        return None
    if choices is not None and raw not in {str(c) for c in choices}:
        raise ValueError(f"must be one of: {', '.join(str(c) for c in choices)}")
    if kind == "str":
        return raw
    if kind == "int":
        try:
            return int(raw)
        except ValueError:
            raise ValueError(f"expected an integer, got {raw!r}")
    if kind == "bool":
        truthy = {"1", "true", "yes", "y", "on"}
        falsy = {"0", "false", "no", "n", "off"}
        low = raw.lower()
        if low in truthy:
            return True
        if low in falsy:
            return False
        raise ValueError(f"expected true/false, got {raw!r}")
    if kind == "list[str]":
        return [s.strip() for s in raw.split(",") if s.strip()]
    if kind == "json":
        try:
            return json.loads(raw)
        except json.JSONDecodeError as exc:
            raise ValueError(f"invalid JSON: {exc}")
    # Unknown kind — fall back to string.
    return raw


def _default_prompt(
    text: str,
    default: Any = None,
    hide_input: bool = False,
    show_default: bool = False,
    type: Any = None,
) -> str:
    """One-liner prompt that gets out of click's way.

    click.prompt is broken for our needs because:

      1. With ``hide_input=True`` and ``show_default=True`` it uses
         ``getpass`` which CANNOT echo a default — the user sees an
         empty field with no hint of what's there. Pressing Enter
         then either (a) submits an empty string (so click treats
         it as missing → "This field is required") or (b) submits
         the default string itself, which gets fed into the next
         prompt's parser. Both produce exactly the buggy double-
         prompt pattern in the screenshot.

      2. With ``hide_input=False`` and ``show_default=True`` click
         displays the default and substitutes it on Enter — fine
         for non-secrets, but for the secret we still need to hide
         the user's input.

    The fix: a single Rich-based prompt that knows it owns the
    whole line. We:

      - Print the prompt with the default rendered AFTER the colon
        (never as the input). For secrets, render the mask.
      - Use Rich's ``Console.input`` (works on TTY, falls back to
        stdin in scripts) WITHOUT hide_input — typing just doesn't
        echo for the user to see, but the data flows correctly.
      - For TRUE secrets we additionally mask on-screen using a
        ``password=True`` argument that Rich's Prompt supports.

    This is what makes the wizard feel like Hermes: paste your
    token once, press Enter through every other field, done.
    """
    # Build the on-screen suffix: `` [●●●●●●●●]`` for secrets,
    # `` [markdownv2]`` for non-secrets with a default.
    suffix = ""
    if show_default and default is not None:
        suffix = f" [dim][{default}][/dim]"
    prompt_text = f"{text}{suffix}: "

    try:
        from rich.console import Console
        from rich.prompt import Prompt as _RichPrompt
        console = Console()
        # Rich's Prompt handles hide_input correctly via getpass
        # but unlike click it ALSO honours a default — the user
        # sees the default in the prompt and pressing Enter returns
        # it. The password flag masks the actual typing.
        #
        # CRITICAL: when password=True, we DO NOT pass `default=...`
        # to Rich. Rich's password mode uses a different code path
        # that reads the password via getpass WITHOUT skipping
        # escape sequences, and the rendered default (with our dim
        # ANSI codes) can leak back as the password value. We
        # already render the default ourselves in the prompt_text
        # suffix, so the user sees it. Pressing Enter returns ""
        # and our outer wizard loop's "has_default + empty →
        # keep" branch takes over.
        if hide_input:
            ans = _RichPrompt.ask(
                prompt_text,
                console=console,
                password=True,
                show_default=False,
                show_choices=False,
                default="",
            )
        else:
            ans = _RichPrompt.ask(
                prompt_text,
                console=console,
                password=False,
                default=str(default) if default is not None else "",
                show_default=False,
                show_choices=False,
            )
        return str(ans or "").strip()
    except (KeyboardInterrupt, EOFError):
        # Ctrl+C / Escape / EOF. Raise WizardCancelled so the
        # outer loop unwinds to the main menu instead of treating
        # this as empty input (which would be re-prompted).
        raise WizardCancelled() from None
    except Exception:
        # Fallback when Rich is unavailable / not on a TTY: plain
        # input() with the default shown. No masking in this path —
        # we still treat the value as a "secret" by not displaying
        # the typed characters (input() on a TTY echoes them; we
        # accept that risk rather than block the wizard).
        try:
            return input(prompt_text).strip()
        except (KeyboardInterrupt, EOFError):
            raise WizardCancelled() from None


def _default_confirm(text: str, default: bool = False) -> bool:
    try:
        suffix = " [Y/n]" if default else " [y/N]"
        ans = input(f"{text}{suffix}: ").strip().lower()
        if not ans:
            return default
        return ans in {"y", "yes"}
    except (KeyboardInterrupt, EOFError):
        # Cancellation propagates to the wizard caller, which
        # decides whether to return to the menu or exit.
        raise WizardCancelled() from None


# ─────────────────────────────────────────────────────────────────────────────
# Live config validation
# ─────────────────────────────────────────────────────────────────────────────
#
# ``validate_channel_config(name, config)`` is called by the wizard
# AFTER ``run_channel_setup`` collects every field but BEFORE the
# config is persisted to ``~/.cvc/channels/<name>.yaml``. The hook
# gives the adapter a chance to prove the config actually works —
# Telegram calls ``Bot.get_me()``, Discord would open a websocket,
# SMTP would try STARTTLS, etc. — and surface a clear error
# otherwise.
#
# Returning ``""`` (empty string) means "looks good". Returning a
# non-empty string is the user-facing error to display (it goes
# through the wizard's normal error formatting). Returning ``None``
# means "this channel has no validator installed, skip silently".
#
# This is the fix for the "I pasted a token and the gateway
# crashed an hour later" class of bug: we fail LOUDLY at the
# moment the user is still in front of the terminal, with the
# exact API error from Telegram, instead of letting bad config
# ship into the channels yaml and only blowing up at gateway
# startup.

import asyncio


def validate_channel_config(name: str, config: Dict[str, Any]) -> Optional[str]:
    """Run a live smoke test for *name* with *config*.

    Returns:
        ``""``     — config looks good.
        ``None``   — no validator registered for this channel
                     (silent skip, backwards-compatible).
        ``str``    — user-facing error message to show.
    """
    handler = _VALIDATORS.get(name)
    if handler is None:
        # No validator installed for this channel — silent skip so
        # adapters that haven't migrated yet aren't broken.
        return None
    try:
        return handler(dict(config)) or ""
    except Exception as exc:  # noqa: BLE001
        # Validator itself blew up. Don't crash the wizard — show
        # the error and let the user decide whether to keep going.
        return f"validation check crashed: {exc}"


def _validate_telegram(cfg: Dict[str, Any]) -> Optional[str]:
    """Call ``Bot.get_me()`` to prove the bot_token is real and live.

    A revoked/typoed token returns ``Unauthorized`` from Telegram's
    API. We surface that verbatim so the user knows exactly what
    went wrong (revoked? wrong format? bot deleted?). We also
    print the bot's ``@username`` and numeric ID on success so the
    user has positive confirmation they typed the right token.

    Also validates the allowlist field — every entry must be a
    bare integer (user ID) or a ``-100…`` prefixed group chat ID.
    This catches the common "I pasted my @username instead of my
    numeric ID" mistake before the wizard saves anything.
    """
    token = (cfg.get("bot_token") or "").strip()
    if not token:
        return "bot_token is empty — nothing to validate"
    # Quick format check before hitting the API. Telegram tokens
    # look like ``123456789:AA...`` — if it doesn't match, fail
    # fast without burning an API call.
    if ":" not in token or not token.split(":", 1)[0].isdigit():
        return (
            "Token doesn't look like a Telegram bot token. "
            "Expected format: <bot_id>:<44-ish-char secret>. "
            "Get one fresh from @BotFather (/newbot → /revoke → /token)."
        )

    # ── Validate allowlist format ──────────────────────────────────
    # Catch the very common "I pasted @myusername instead of my
    # numeric ID" mistake. A real Telegram user ID is a positive
    # integer; a group chat ID is a negative integer prefixed by
    # -100 (Telegram's supergroup convention).
    allowlist = cfg.get("allowlist") or []
    if not allowlist:
        return (
            "allowlist is empty — at least one user ID is required. "
            "Open @userinfobot on Telegram, send /start, and copy the Id "
            "it shows you. Then run `cvc channel-setup telegram` again."
        )
    for entry in allowlist:
        s = str(entry).strip()
        if not s:
            continue
        if not s.lstrip("-").isdigit():
            return (
                f"allowlist entry {entry!r} is not a numeric Telegram ID. "
                "Telegram user IDs are integers like 123456789. "
                "Group chat IDs start with -100. "
                "Find your ID by messaging @userinfobot or @RawDataBot on Telegram."
            )

    try:
        from telegram import Bot as _TgBot  # python-telegram-bot
    except Exception as exc:  # noqa: BLE001
        return (
            f"python-telegram-bot is not installed ({exc}). "
            "Run `pip install 'python-telegram-bot[webhooks]>=22.0'`."
        )

    async def _call() -> Tuple[Optional[str], Optional[str]]:
        bot = _TgBot(token=token)
        try:
            me = await bot.get_me()
            username = getattr(me, "username", None) or "?"
            bot_id = getattr(me, "id", None)
            return None, f"@{username} (id {bot_id})"
        except Exception as exc:  # noqa: BLE001
            # Return the actual API error — it's already user-friendly
            # from python-telegram-bot (e.g. "Unauthorized: ...").
            return str(exc).strip() or exc.__class__.__name__, None
        finally:
            try:
                await bot.shutdown()
            except Exception:
                pass

    try:
        err, ok = asyncio.run(_call())
    except RuntimeError as exc:
        # asyncio.run() can choke inside an existing event loop
        # (e.g. when the wizard is invoked from inside another
        # async context). Fall back to a fresh loop in a thread.
        import threading

        box: list = []

        def _runner() -> None:
            loop = asyncio.new_event_loop()
            try:
                asyncio.set_event_loop(loop)
                box.append(loop.run_until_complete(_call()))
            finally:
                loop.close()

        t = threading.Thread(target=_runner, daemon=True)
        t.start()
        t.join(timeout=15)
        if not box:
            return "Telegram validation timed out after 15s"
        err, ok = box[0]

    if err:
        return f"Telegram rejected the token: {err}"
    if ok:
        print(f"  [bold #55AA55]✓[/bold #55AA55] Token is live — bot is {ok}")
    return ""


# Registry of validators. Adding a new channel is one line:
# _VALIDATORS["discord"] = _validate_discord  (etc.)
_VALIDATORS: Dict[str, Callable[[Dict[str, Any]], Optional[str]]] = {
    "telegram": _validate_telegram,
}
