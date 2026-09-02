"""
InnoDay CLI Configuration Management

Handles configuration file management and secure credential storage.
Supports multiple named profiles (one per environment: local, dev, etc.).
"""

import copy
import json
import os
import re
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional

import keyring
from keyring.errors import NoKeyringError, PasswordDeleteError
from rich.console import Console

from src.cli.utils.project_context import (
    LegacyProjectFileError,
    load_project_context,
)

console = Console()

# Notices emitted while a CLIConfig is being *constructed* — the load-degraded
# warning, the api_url/api_port migrations, the board-secret purge — go to
# stderr, never stdout.
#
# `src/mcp/server.py` calls `load_config()` at module scope, which builds a
# CLIConfig during import, and that server speaks JSON-RPC over stdio where
# **stdout IS the protocol channel** (the rule is written down at
# `src/mcp/server.py`'s blastoff-capture comment). A single line of prose on
# fd 1 ahead of the handshake breaks the server — and the purge fires on
# exactly the machines it exists for, on their first start after upgrading.
#
# stderr is safe there and still reaches a human running `innoday`, so the
# notice is not lost; it just stops corrupting anything that reads stdout.
_notices = Console(stderr=True)

# The deployed API, and the one place its address is written down. It was
# spelled out in four (here, `commands/init.py`, and twice in
# `commands/config.py`) while `src/mcp/server.py` carried a fifth that
# disagreed (`http://localhost:8000`) -- so "what does a fresh install point
# at" had two answers depending on which door you came through.
DEFAULT_API_URL = "https://www.inno.day"


def is_local_api_url(api_url: str) -> bool:
    """True for a purely-local API target (localhost / 127.0.0.1 / ::1).

    A local API has no team secret, so the team-secret prompt/requirement is
    skipped for it. Robust against the port and scheme varying (the historical
    check compared against the exact literal ``http://localhost:8000`` only).
    """
    if not api_url:
        return False
    from urllib.parse import urlparse

    # urlparse needs a scheme to populate .hostname; tolerate a bare host:port.
    parsed = urlparse(api_url if "//" in api_url else f"//{api_url}", scheme="http")
    host = (parsed.hostname or "").lower()
    return host in ("localhost", "127.0.0.1", "::1", "0.0.0.0")


# Values baked into old config files by a stale default -- detected and migrated
# away from in _load_raw() rather than treated as a real user override.
#
# `http://localhost:8000` joined this list when the default became the deployed
# API. It is the more delicate of the two: unlike :8002 it is a *plausible* real
# choice, so migrating it could retarget someone deliberately running locally.
# It is still the right call -- that value only ever arrived by never having
# chosen, since anyone actually developing against a local server sets it through
# `config set api-url` or `--api-url`, which both write the same field and are
# indistinguishable afterwards. The migration prints what it changed, and
# re-pointing at localhost is one command.
_STALE_DEFAULT_API_URLS = ("http://localhost:8002", "http://localhost:8000")

# Kept as a single value for anything still importing it.
_STALE_DEFAULT_API_URL = _STALE_DEFAULT_API_URLS[0]

# Integration types whose credentials belong to a *board*. These may never be
# written to (or left in) ~/.innoday/config.json: they live in Supabase Vault,
# keyed per board, resolved server-side. Nothing writes a credential there any
# more (#729 removed the last writer, `add_organization_integration`), and
# nothing mints the empty `integrations` container either -- `innoday orgs
# setup` used to, and stopped in the same change. `_purge_local_board_secrets`
# removes any credential already on disk; an empty container it leaves alone.
#
# TODO(#733): delete this whole cluster once every config is stamped >= 0.1.331b0.
#
# Everything below -- both integration-type sets, `_DEAD_PROFILE_KEYS`,
# `_DEAD_TOP_LEVEL_KEYS`, `_strip_dead_blocks`, `_purge_local_board_secrets` and
# the six helpers and two reporters it calls, `dead_local_secrets` and the
# `config show` panel rendering it -- is a **migration, not a feature**. It is
# self-terminating: the removal is one-shot per config, so on a file written by
# a current CLI it finds nothing, reports nothing, and runs on every invocation
# for no reason.
#
# The criterion is `written_by_version`, which is why that stamp exists: a
# config only needs any of this if it was last written by a CLI predating the
# fix. Board credentials (#609) are long past. The `github`/`claude` half, and
# both dead blocks, need every config in use stamped >= 0.1.331b0 (#729).
#
# Two things not to get wrong, both in #733:
#   - Deleting it early abandons a real secret -- a PAT or API key left in
#     somebody's keyring with a pointer in a file nothing will ever clean
#     again. That is worse than the state before #609.
#   - `_strip_dead_blocks` runs BEFORE the purge scan. A future change that
#     made it drop `organizations[*].integrations` wholesale would leave the
#     purge unable to see the credentials inside, so it would stop clearing
#     keyring values while still reporting success. This is the reason the
#     empty `integrations: {}` container is deliberately left alone today.
#
# Written out rather than derived from `BoardType` on purpose: `src.domain.board`
# pulls in SQLModel/SQLAlchemy, which costs ~340ms of import time, and this
# module is imported by every CLI invocation and by the MCP server at startup.
# The cost of writing it out is that it can drift from the enum silently, so it
# is pinned by `tests/test_cli_choices_match_enums.py` — the file that exists
# because a hand-typed board-type list drifted before. Adding a fifth BoardType
# fails there, naming this constant.
BOARD_INTEGRATION_TYPES = frozenset({"jira", "trello", "linear", "notion"})

# Written by a wizard, read by nothing -- confirmed by grep across src/,
# scripts/ and the MCP server. #609 reported these and left them on disk,
# because deleting somebody's GitHub PAT unasked was not that change's call to
# make while the wizard writing them was still a live command. #729 deleted the
# wizard, which settles it: a credential with no writer and no reader is not a
# preference anybody is expressing, so these are purged like a board secret --
# entry popped, keyring value cleared. They are not *board* credentials, so
# the notice afterwards says something different about what to do next.
DEAD_INTEGRATION_TYPES = frozenset({"github", "claude"})

# Profile-aware flat config shape (the schema for a single profile)
_PROFILE_DEFAULTS: Dict[str, Any] = {
    "platform": {
        # The deployed API. `innoday init` already defaulted here while a
        # fresh profile defaulted to
        # localhost, so anyone who installed the CLI without running `init` -- or
        # whose config was created any other way -- got a client pointed at a
        # server that was not running, and had to discover `config set api-url`
        # from an error message. One default, and it is the one that works.
        "api_url": DEFAULT_API_URL,
        "api_timeout": 30.0,
    },
    "user": {"id": None, "email": None, "name": None},
    "organizations": {},
    "current_organization": None,
    "output": {"format": "table", "color": True},
}

# Profile keys, and top-level keys, that a config file on disk may still hold
# and that nothing reads. Popped on load (see `_strip_dead_blocks`) rather than
# merely left alone, because `save()` round-trips whatever the file holds --
# so without this they survive every future write.
#
# `session` held a thread id and a ten-entry history behind four accessors and
# a `save_session()`; none of the five had a caller anywhere. `platform_server`
# was write-only bookkeeping: `platform start` stamped it and then called a
# compose wrapper that re-derives the env file, never passes the project name
# to docker, and takes its ports from `docker-compose.yml`. Its `api_port`
# (8000) even contradicted `src/config/schema.py` (8002), so the panel showing
# it actively misinformed.
_DEAD_PROFILE_KEYS = ("session",)
_DEAD_TOP_LEVEL_KEYS = ("platform_server",)


class CLIConfig:
    """Configuration management for InnoDay CLI — profile-aware."""

    KEYRING_SERVICE = "innoday-cli"

    # Top-level default (wraps profiles)
    #
    # `current_profile` is the interactively-mutated "what am I on now"
    # pointer (changed by `config profile use`). `default_profile` is a
    # separate, stable pointer used for non-interactive/MCP resolution when
    # nothing else is specified -- deliberately absent here so existing
    # configs on disk (and fresh ones) don't declare it until a caller
    # explicitly opts in via set_default_profile().
    DEFAULT_CONFIG: Dict[str, Any] = {
        "current_profile": "default",
        "profiles": {
            "default": copy.deepcopy(_PROFILE_DEFAULTS),
        },
    }

    # Keep for backwards-compat reference in tests / external callers
    _PROFILE_DEFAULTS = _PROFILE_DEFAULTS

    def __init__(
        self,
        config_path: Optional[str] = None,
        profile: Optional[str] = None,
        detect_cwd_context: bool = False,
        allow_legacy_context: bool = False,
        **overrides,
    ):
        # When True, an outdated .innoday/project.yml (legacy schema) is skipped
        # silently instead of hard-exiting — used by the upgrade commands
        # (init/join/refresh) that regenerate the file. Every other command
        # hard-errors so the user is told to run `innoday refresh`.
        self._allow_legacy_context = allow_legacy_context
        # Set by _apply_cwd_project_context when the cwd's project.yml is an
        # outdated format and this isn't an upgrade command. The CLI entrypoint
        # checks it and exits with guidance; library callers can inspect it.
        self.legacy_context_error: Optional[Exception] = None
        self.config_path = self._get_config_path(config_path)
        # Set by _load_raw: True when an existing config file could not be read
        # or parsed, so save() must not overwrite it with defaults.
        self._load_degraded = False
        # Set by _load_raw: the dead top-level/profile blocks it popped out of
        # the file in memory, which `_purge_local_board_secrets` then writes
        # away. Initialised here because `_load_raw` returns early for a file
        # that does not exist or cannot be read, before it reaches the strip.
        self._stripped_dead_blocks: List[str] = []
        self._raw = self._load_raw()  # full file (all profiles)
        # Board secrets already on disk are removed here, before the active
        # profile's view is built from _raw -- so this invocation cannot read
        # one either, and a later save() cannot write one back.
        self.dead_local_secrets: List[Dict[str, str]] = []
        self._purge_local_board_secrets()
        self._current_profile = self._resolve_profile(profile)
        self._config = self._active_profile_config()
        # An explicit --organization flag is a one-shot, request-scoped
        # override. current_organization is never persisted to disk (save()
        # strips it, along with platform.project_id), so the override lives
        # only in this invocation's in-memory _config and can't leak into
        # permanently-sticky state on the next invocation.
        self._organization_override = overrides.get("organization")
        self._project_override = overrides.get("project_id")
        # Whether org/project context was actually resolved FOR THIS
        # INVOCATION (an explicit override, or a real .innoday/project.yml
        # match) -- there is no persisted-fallback tier. current_organization/
        # platform.project_id are never written to disk (see save()), so
        # get_current_organization()/get_current_project_id() only return a
        # value when one of these flags is True -- see
        # _apply_cwd_project_context.
        self._org_resolved_this_invocation = bool(self._organization_override)
        self._project_resolved_this_invocation = bool(self._project_override)
        self._apply_overrides(overrides)
        if detect_cwd_context:
            self._apply_cwd_project_context(overrides)
        self._color_enabled = self._config["output"]["color"]

    def _resolve_profile(self, profile: Optional[str]) -> str:
        """
        Resolve which profile is active, in precedence order:
          1. An explicit `profile=` constructor arg (from a --profile CLI flag)
          2. `current_profile` from disk, if it still points at a real profile
          3. `default_profile` from disk, if it still points at a real profile
          4. The hardcoded "default" literal

        Never uses bracket access on the raw config -- configs written before
        `default_profile` existed must not KeyError here.
        """
        profiles = self._raw.get("profiles", {})

        if profile and profile in profiles:
            return profile

        current = self._raw.get("current_profile")
        if current and current in profiles:
            return current

        default = self._raw.get("default_profile")
        if default and default in profiles:
            return default

        return "default"

    # ------------------------------------------------------------------
    # Path helpers
    # ------------------------------------------------------------------

    def _get_config_path(self, custom_path: Optional[str] = None) -> Path:
        if custom_path:
            return Path(custom_path)
        config_dir = Path.home() / ".innoday"
        config_dir.mkdir(parents=True, exist_ok=True)
        return config_dir / "config.json"

    # ------------------------------------------------------------------
    # Load / save
    # ------------------------------------------------------------------

    def _load_raw(self) -> Dict[str, Any]:
        """Load and migrate the full config file.

        Sets `self._load_degraded` when a file that EXISTS could not be read or
        parsed, so `save()` can refuse to overwrite it. A missing file is not
        degraded -- that is a legitimate first run, and defaults are the right
        answer.
        """
        self._load_degraded = False

        if not self.config_path.exists():
            return copy.deepcopy(self.DEFAULT_CONFIG)

        try:
            with open(self.config_path, "r") as f:
                raw = json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            # Falling back to defaults is fine for READING. What is not fine is
            # the next save() writing those defaults back over a file that still
            # holds every profile -- which is exactly how a real `dev` profile
            # (api_url, identity, orgs) was destroyed by an unrelated
            # `config set team-secret`. The warning below was the only signal,
            # and it is invisible the moment output is redirected.
            self._load_degraded = True
            _notices.print(
                f"[yellow]Warning: Could not load config: {e} — using defaults "
                f"for this command. Writes are blocked until it is fixed.[/yellow]"
            )
            return copy.deepcopy(self.DEFAULT_CONFIG)

        # Migrate old flat format → profiles wrapper
        if "profiles" not in raw:
            raw = {
                "current_profile": "default",
                "profiles": {"default": raw},
            }

        # Migrate away from api_url values that were only ever captured defaults,
        # never a real choice (PF-122 for :8002, and :8000 once the default became
        # the deployed API). A profile is touched only when its api_url is exactly
        # one of those, and the change is printed -- so a deliberate local setup is
        # one `config set api-url` away from being restored, and says so.
        # `profiles`, and each profile inside it, are whatever the file says
        # they are -- a half-written or hand-edited file can have a list here,
        # or a string where a profile should be. This loop used to assume both
        # were dicts and raised AttributeError during CLI startup if they were
        # not, which turned a damaged config into every command failing with a
        # traceback rather than a message.
        profiles = raw.get("profiles")
        for profile_name, profile_data in (
            profiles.items() if isinstance(profiles, dict) else ()
        ):
            if not isinstance(profile_data, dict):
                continue
            platform_cfg = profile_data.get("platform")
            if (
                isinstance(platform_cfg, dict)
                and platform_cfg.get("api_url") in _STALE_DEFAULT_API_URLS
            ):
                previous = platform_cfg["api_url"]
                platform_cfg["api_url"] = _PROFILE_DEFAULTS["platform"]["api_url"]
                _notices.print(
                    f"[yellow]Migrated profile '{profile_name}' api_url from "
                    f"{previous} to {_PROFILE_DEFAULTS['platform']['api_url']} "
                    f"(stale default, not a real override)[/yellow]"
                )

        self._stripped_dead_blocks = self._strip_dead_blocks(raw)

        return raw

    @staticmethod
    def _strip_dead_blocks(raw: Dict[str, Any]) -> List[str]:
        """Drop the config blocks nothing reads, in place, and say so once.

        Deleting the code that wrote `session` and `platform_server` does not
        get them off anybody's disk: `save()` writes back whatever `_raw`
        holds, so a file that has them keeps them forever. Nobody is going to
        hand-edit `~/.innoday/config.json`, so the file has to shed them
        itself -- the same reasoning as the board-secret purge below.

        Returns the key names it removed, so the caller can rewrite the file
        and *then* say so. Announcing here instead would claim a removal
        before the write that makes it true had been attempted -- the same
        false claim #614 was about, one layer over.

        Defensive about the file's shape for the same reason as the migration
        loop above -- a hand-edited `profiles` can be a list, or hold a string
        where a profile should be, and that must degrade rather than raise out
        of CLI startup.
        """
        removed: List[str] = []
        for key in _DEAD_TOP_LEVEL_KEYS:
            if raw.pop(key, None) is not None:
                removed.append(key)

        profiles = raw.get("profiles")
        for profile_data in profiles.values() if isinstance(profiles, dict) else ():
            if not isinstance(profile_data, dict):
                continue
            for key in _DEAD_PROFILE_KEYS:
                if profile_data.pop(key, None) is not None and key not in removed:
                    removed.append(key)

        return removed

    def _active_profile_config(self) -> Dict[str, Any]:
        """Return the active profile's config, merged with defaults."""
        # Defensive on both levels for the same reason as the migration loop
        # in `_load_raw`: a damaged `profiles` block must degrade to defaults
        # for this command, not raise a traceback out of CLI startup. `save()`
        # is separately blocked from overwriting an unreadable file.
        profiles = self._raw.get("profiles")
        profile_data = (
            profiles.get(self._current_profile) if isinstance(profiles, dict) else None
        )
        if not isinstance(profile_data, dict):
            profile_data = {}
        return self._merge_config(copy.deepcopy(_PROFILE_DEFAULTS), profile_data)

    # ------------------------------------------------------------------
    # Board-secret purge (#609)
    # ------------------------------------------------------------------

    def _purge_local_board_secrets(self) -> None:
        """Remove any board credential this config file still holds.

        Runs on every load because the machines holding these entries cannot
        be reached by hand. It is silent when there is nothing to do, and safe
        to run repeatedly -- the second run finds nothing and does not touch
        the file.

        Four things this has to get right, three of which were got wrong in a
        by-hand audit of one machine first:

        1. **Every profile, not `current_profile`.** The audit cleaned `dev`
           and reported done; `default` still held `bp -> jira`.
        2. **The keyring value, under the owning profile's namespace.** The
           stored value is a pointer, ``encrypted:<key>``, with the real
           secret in the OS keyring -- so dropping the JSON entry alone
           *orphans* the secret rather than removing it. The keyring username
           may be profile-prefixed (see `_keyring_key`), and the prefix that
           matters is the profile the entry belongs to, NOT the active one.
           `self.delete_credential()` would use the active profile and delete
           somebody else's entry, so it is deliberately not used here. Real
           keyrings also hold plenty of *unprefixed* entries (#614), so both
           names are tried -- see `_clear_keyring_pointers`. What is reported
           depends on what was actually deleted: announcing a removal that did
           not happen is the failure this whole purge exists to avoid.
        3. **Nothing unrelated may be lost.** This edits a real user's config,
           which holds their identity, org list and every profile. Only the
           board entries are popped; the file is otherwise round-tripped.
        4. **A malformed file must not break CLI startup.** An unparseable
           file is already handled upstream (`_load_degraded`, which also
           blocks the write below); a *structurally* odd one -- `profiles` a
           list, an integration a string -- is skipped rather than raised on.

        The scan is separated from the removal so the file's directory can be
        checked for writability *before* anything is deleted. A read-only
        directory used to leave the worst possible state behind: the keyring
        value gone, the pointer still on disk, and the same failed write
        re-attempted (and re-warned about) on every subsequent invocation,
        forever. Now the two halves either both happen or neither does.

        Past that check, the keyring is cleared before the file is rewritten.
        If the write still fails, what is left behind is a pointer to a secret
        that no longer exists -- inert, since nothing reads these entries any
        more, and retried on the next load. The other order would leave a live
        secret in the keyring with nothing pointing at it, which is the
        failure this is here to prevent.

        No backup file is written. A `.bak` would re-persist on disk exactly
        the pointers being removed while their keyring values are gone --
        dead weight that works against the point of the purge. The corruption
        risk a backup would cover is handled by writing atomically instead
        (`_write_raw_atomically`, pinned by
        `TestTheWriteIsAtomic`).

        The rewrite also persists whatever else `_load_raw` migrated in
        memory this invocation -- the profiles wrapper for a legacy flat
        config, a stale api_url, a stripped dead block. All of
        those were going to be written by the next explicit `save()` anyway;
        the purge just gets there first. Point 3 above means no *user* data is
        lost, not that the file comes back byte-identical apart from the
        board entry.

        Every message here goes to stderr (see `_notices`).
        """
        if self._load_degraded:
            return

        try:
            board_secrets, dead = self._scan_local_secrets()
        except Exception as e:
            _notices.print(
                f"[yellow]Warning: could not check {self.config_path} for "
                f"locally-stored credentials: {e}[/yellow]"
            )
            return

        # One removal pass over both kinds. They differ only in what the
        # notice afterwards tells the operator to do instead -- the popping,
        # the keyring clearing and the shared-pointer protection are the same
        # work, and duplicating it would give the `github`/`claude` half a
        # second implementation to drift from (and to get #614 wrong in again).
        doomed = board_secrets + dead

        # `_load_raw` may also have popped a dead block (`session`,
        # `platform_server`) out of `self._raw` in memory. That has to reach
        # the file, and this is the one place that writes on load: left to the
        # next explicit `save()`, a config whose owner only ever runs read
        # commands keeps the block -- and, worse, is told about it again on
        # every single invocation.
        if not doomed and not self._stripped_dead_blocks:
            return

        # Resolved, because config.json may be a symlink into a dotfiles repo:
        # the write lands in the *target's* directory, and it is that
        # directory's writability that decides whether this can work at all.
        target = self.config_path.resolve()
        if not os.access(target.parent, os.W_OK):
            # Silent when there is no secret at stake: a dead block that
            # cannot be written away is inert, and warning about it on every
            # command would be worse than leaving it there.
            if doomed:
                _notices.print(
                    f"[yellow]Warning: {self.config_path} still holds "
                    f"credentials, but {target.parent} is not writable, so "
                    f"nothing has been removed (the keyring entries are "
                    f"untouched and still match the file). Make the directory "
                    f"writable and run any innoday command again.[/yellow]"
                )
            return

        # Read before anything is popped: it has to see the file as it stands.
        kept_pointers = self._pointers_kept_by_surviving_entries(doomed)
        # Likewise before the write, which is what changes both of these.
        hazards = self._write_hazards(target)

        self._remove_local_secrets(doomed, kept_pointers)

        try:
            self._write_raw_atomically()
        except OSError as e:
            if doomed:
                self._report_unwritten_after_keyring_clear(
                    [entry for _, _, entry in doomed], e
                )
            return

        # Only now, past the write. `config show` renders this list under
        # "Secrets removed from this config file", so it may only ever hold
        # entries whose removal actually reached disk: both returns above leave
        # the entry in the file and its secret in the keyring, and the panel
        # claiming otherwise is the same #614 false claim the stderr path is
        # careful to avoid -- in the same invocation, contradicting it.
        self.dead_local_secrets = [entry for _, _, entry in dead]

        if self._stripped_dead_blocks:
            _notices.print(
                f"[yellow]Removed {', '.join(sorted(self._stripped_dead_blocks))} "
                f"from {self.config_path} — written by an older CLI, read by "
                f"nothing[/yellow]"
            )
        self._report_purged_secrets([entry for _, _, entry in doomed])
        for hazard in hazards:
            _notices.print(f"[yellow]{hazard}[/yellow]")

    def _write_hazards(self, target: Path) -> List[str]:
        """Things the atomic rewrite is about to do that the file's own state
        says it should not, phrased for the operator afterwards.

        Both are decided in favour of writing, and the decision is what is being
        recorded here -- neither used to be visible at all.

        **A read-only file is rewritten anyway.** `os.replace` needs no write
        permission on the file, only on its directory, so a `chmod 444` config
        was silently overridden (mode preserved afterwards, so nothing looked
        changed). Refusing instead would leave the secret on the machine
        indefinitely and re-warn on every command forever, which is the state
        this purge exists to end; the honest form is to do it and say so.

        **Hard links are severed.** `save()` writes through `open(path, "w")`
        and so keeps every name pointing at one inode; `os.replace` swaps the
        name and leaves the other names on the old inode. Atomicity is
        load-bearing here (there is no `.bak`, by design), so the write stays as
        it is -- but the other name keeps a copy of the file whose pointer now
        dangles. No secret survives in it; the keyring value really is gone.
        """
        hazards: List[str] = []
        try:
            info = target.stat()
        except OSError:
            return hazards
        if not os.access(target, os.W_OK):
            hazards.append(
                f"Note: {target} was read-only (mode {info.st_mode & 0o777:#o}) "
                f"and has been rewritten anyway to remove what it held that "
                f"nothing reads. Its mode is unchanged."
            )
        if info.st_nlink > 1:
            hazards.append(
                f"Note: {target} had {info.st_nlink} hard links. Only this name "
                f"now holds the purged contents — the other name(s) still hold "
                f"the old file, whose credential pointer no longer "
                f"resolves (the keyring value is gone either way)."
            )
        return hazards

    def _scan_local_secrets(self):
        """Find, without removing anything, every board secret and every dead
        `github`/`claude` entry in `self._raw`.

        Returns ``(board_secrets, dead)``. Both are lists of
        ``(integrations_dict, key, entry)`` -- the containing dict and the key
        as it actually appears in the file, so the removal pass does not have
        to find it a second time (and so a hand-written ``"Jira"`` can be
        matched case-insensitively but popped by its real key). They are
        returned apart only so the notice afterwards can say the right thing
        about each; both are removed.

        Anything in neither set -- `slack` today -- is left alone. #605 owns
        that one.
        """
        board_secrets = []
        dead = []
        profiles = self._raw.get("profiles")
        if not isinstance(profiles, dict):
            return board_secrets, dead

        for profile_name, profile_data in profiles.items():
            if not isinstance(profile_data, dict):
                continue
            organizations = profile_data.get("organizations")
            if not isinstance(organizations, dict):
                continue
            for org_alias, org_data in organizations.items():
                if not isinstance(org_data, dict):
                    continue
                integrations = org_data.get("integrations")
                if not isinstance(integrations, dict):
                    continue
                for integration_type in list(integrations):
                    entry = {
                        "profile": str(profile_name),
                        "organization": str(org_alias),
                        "integration": str(integration_type),
                    }
                    # Case-folded. `_lookup_organization_entry` twelve methods
                    # away already carries the same caveat: these keys are
                    # lowercase by convention only, and a file written before
                    # that convention held -- or edited by hand -- can say
                    # "Jira". An exact match would leave that secret on disk.
                    kind = str(integration_type).strip().lower()
                    if kind in DEAD_INTEGRATION_TYPES:
                        entry["kind"] = "dead"
                        dead.append((integrations, integration_type, entry))
                    elif kind in BOARD_INTEGRATION_TYPES:
                        entry["kind"] = "board"
                        board_secrets.append((integrations, integration_type, entry))
        return board_secrets, dead

    def _pointers_kept_by_surviving_entries(self, doomed_entries) -> set:
        """Every `encrypted:` pointer text still referenced by an integration
        entry that is *not* being purged.

        `_clear_keyring_pointers` deletes by pointer text, and a pointer is not
        private to the entry holding it: two entries can carry the same
        `encrypted:<key>` string, in which case deleting it for one destroys the
        secret the other still resolves. Observed as a `github` entry left
        dangling when the `jira` entry beside it was purged. Not reachable
        through the wizard that used to write these -- it minted
        `{org}_{type}_{key}`, so the type was always in the name -- but
        reachable in a hand-edited or legacy-written file, which is precisely
        the population this purge exists for.
        """
        doomed = {
            (e["profile"], e["organization"], key) for _, key, e in doomed_entries
        }
        kept: set = set()
        profiles = self._raw.get("profiles")
        if not isinstance(profiles, dict):
            return kept
        for profile_name, profile_data in profiles.items():
            if not isinstance(profile_data, dict):
                continue
            organizations = profile_data.get("organizations")
            if not isinstance(organizations, dict):
                continue
            for org_alias, org_data in organizations.items():
                if not isinstance(org_data, dict):
                    continue
                integrations = org_data.get("integrations")
                if not isinstance(integrations, dict):
                    continue
                for key, stored in integrations.items():
                    if (str(profile_name), str(org_alias), key) in doomed:
                        continue
                    if not isinstance(stored, dict):
                        continue
                    for value in stored.values():
                        if isinstance(value, str) and value.startswith("encrypted:"):
                            kept.add(value[len("encrypted:") :])
        return kept

    def _remove_local_secrets(self, doomed, kept_pointers=frozenset()) -> None:
        """Pop each scanned integration out of `self._raw`, clearing the
        keyring value it points at.

        Each entry is annotated in place with what actually happened to its
        keyring value (`entry["keyring"]`, and `entry["keyring_tried"]` when
        that was not "removed"), because the notice printed afterwards must
        not claim a removal that did not occur.
        """
        for integrations, key, entry in doomed:
            removed = integrations.pop(key, None)
            status, tried = self._clear_keyring_pointers(
                entry["profile"], removed, kept_pointers
            )
            entry["keyring"] = status
            if status != "removed":
                entry["keyring_tried"] = tried

    #: Which outcome a whole entry reports when its pointers disagree, worst
    #: first. "failed" and "shared" both mean a secret is still on the machine
    #: and must not be masked by a "removed" beside them; "absent" is the only
    #: one that may never overwrite anything.
    _KEYRING_OUTCOME_RANK = {
        "absent": 0,
        "no_keyring": 1,
        "removed": 2,
        "shared": 3,
        "failed": 4,
    }

    def _clear_keyring_pointers(
        self, profile_name: str, stored: Any, kept_pointers=frozenset()
    ):
        """Delete the keyring values an `encrypted:` pointer refers to.

        Returns ``(status, tried)`` -- ``status`` one of:

        - ``"removed"``    at least one keyring value was deleted *and verified
          gone*;
        - ``"absent"``     nothing was found to delete under any candidate name.
          Not a failure, and not a removal either;
        - ``"no_keyring"`` there is no reachable keyring backend, so no delete
          was even attempted. Distinct from ``"absent"``: a backend that is
          merely unreachable (D-Bus down, `PYTHON_KEYRING_BACKEND` misset) still
          has the secret in it, and saying "nothing was found" would be the
          same false claim #614 was about;
        - ``"shared"``     deliberately left alone, because a surviving entry
          still points at it (see `_pointers_kept_by_surviving_entries`);
        - ``"failed"``     an entry could not be deleted, or survived the
          delete. The secret is still on the machine.

        ``tried`` lists the candidate usernames, for a message the operator
        can act on.

        A keyring backend that is missing or locked must not break CLI
        startup, so nothing here raises.
        """
        status = "absent"
        tried: List[str] = []
        if not isinstance(stored, dict):
            return status, tried
        for value in stored.values():
            if not isinstance(value, str) or not value.startswith("encrypted:"):
                continue
            pointer = value[len("encrypted:") :]
            # Both naming conventions: real keyrings hold the same logical
            # secret prefixed *and* bare (#614 -- `brightpower_jira_api_token`
            # and `dev_brightpower_jira_api_token` on the same machine), so a
            # prefix-only delete leaves the real secret in place. Safe in a way
            # that using the *active* profile is not: the pointer text is
            # identical either way, so neither candidate can name a different
            # secret. The prefixed form comes from `_keyring_key`, the one
            # definition of it, so it cannot drift from `store_credential`.
            candidates = (self._keyring_key(pointer, profile_name), pointer)
            if pointer in kept_pointers:
                # Neither name, not just the bare one: which of the two a
                # surviving entry resolves depends on the *active* profile at
                # read time, so both can be the live secret.
                tried.extend(candidates)
                status = self._worse_keyring_outcome(status, "shared")
                continue
            for username in candidates:
                tried.append(username)
                status = self._worse_keyring_outcome(
                    status, self._delete_keyring_entry(username)
                )
        return status, tried

    @classmethod
    def _worse_keyring_outcome(cls, current: str, one: str) -> str:
        """Keep the worse of two outcomes, so a pointer with one value gone and
        another stuck (or deliberately kept) never reports success."""
        rank = cls._KEYRING_OUTCOME_RANK
        return one if rank.get(one, 0) > rank.get(current, 0) else current

    def _delete_keyring_entry(self, username: str) -> str:
        """Delete one keyring username, returning
        "removed"/"absent"/"no_keyring"/"failed".

        The delete is *verified* with a `get_password` read rather than trusted
        to have worked because it did not raise: #614 was found only because a
        hand-run delete failed loudly, and a silent success is what this must
        not reproduce. The read is of a name just deleted and is only compared
        against `None`; no secret value is read or logged.
        """
        try:
            keyring.delete_password(self.KEYRING_SERVICE, username)
        except PasswordDeleteError:
            # No such entry. Nothing here to leave behind.
            return "absent"
        except NoKeyringError:
            # No backend at all -- which is *not* the same as an empty one. On a
            # headless box with no Secret Service there is genuinely no secret;
            # on a machine whose D-Bus is down there is, and it survived. Only
            # the caller's wording can be honest about not knowing which.
            return "no_keyring"
        except Exception:
            return "failed"
        try:
            gone = keyring.get_password(self.KEYRING_SERVICE, username) is None
        except Exception:
            gone = False  # "removed" has to mean verified gone.
        return "removed" if gone else "failed"

    def _write_raw_atomically(self) -> None:
        """Write `self._raw` over the config file without a window in which
        the file is half-written, preserving its permissions.

        `self.config_path` is **resolved** first. `os.replace` swaps the name
        it is given, so on a `~/.innoday/config.json` symlinked into a
        dotfiles repo an unresolved write replaced the *link* with a regular
        file: the secret survived untouched in the link's target, the keyring
        value was deleted anyway, and the purge reported success. `save()` has
        always written *through* the link (`open(path, "w")`), so an
        unresolved write here would also be a behaviour change in the same
        file. Resolving keeps the temp file in the target's own directory,
        which is also what keeps `os.replace` on one filesystem.

        Atomicity is the property the "no `.bak`" decision rests on: a
        half-written config is unrecoverable without one, so there must be no
        moment at which the real path holds a partial file.
        `TestTheWriteIsAtomic` pins it by failing mid-write and asserting the
        original is byte-identical.
        """
        path = self.config_path.resolve()
        try:
            mode = path.stat().st_mode & 0o777
        except OSError:
            mode = 0o600

        fd, tmp_name = tempfile.mkstemp(
            dir=str(path.parent), prefix=".config-", suffix=".tmp"
        )
        try:
            with os.fdopen(fd, "w") as handle:
                json.dump(self._raw, handle, indent=2)
                # Durability, not just atomicity: without this a crash shortly
                # after the rename can leave a zero-length config on some
                # filesystems -- the rename having reached disk before the
                # bytes it points at.
                handle.flush()
                os.fsync(handle.fileno())
            os.chmod(tmp_name, mode)
            os.replace(tmp_name, path)
        except BaseException:
            try:
                os.unlink(tmp_name)
            except OSError:
                pass
            raise

    #: How each kind of purged entry is described, and what the operator is
    #: told to do instead. Keyed by `entry["kind"]` (see `_scan_local_secrets`).
    #: Written as data rather than as a second copy of the five branches below,
    #: which is how the `github`/`claude` half would acquire its own way of
    #: getting #614 wrong.
    _PURGE_VOCABULARY = {
        "board": (
            "board credential",
            "Board credentials are resolved server-side from Vault. Set one "
            "with 'innoday board set-cred'.",
        ),
        "dead": (
            "credential",
            "Nothing read it — the wizard that wrote it has been removed.",
        ),
    }

    def _report_purged_secrets(self, purged: List[Dict[str, str]]) -> None:
        """Say what was removed, once, at the moment it happens.

        The JSON entry is gone in all three cases -- it is the *keyring value*
        the wording differs about, because "removed" has to mean the secret is
        actually gone (#614). ``absent`` is reported as a stale entry rather
        than a failure: the end state is the one the operator wants, and
        warning about it would train them to ignore the warning that matters.
        """
        for entry in purged:
            status = entry.get("keyring", "removed")
            where = f"({entry['profile']} profile, org {entry['organization']})"
            noun, advice = self._PURGE_VOCABULARY[entry.get("kind", "board")]
            if status == "failed":
                tried = " or ".join(
                    f"'{name}'" for name in entry.get("keyring_tried", [])
                )
                _notices.print(
                    f"[red]Removed the locally-stored {entry['integration']} "
                    f"{noun} {where} from {self.config_path}, but "
                    f"could NOT delete its keyring value ({tried} in service "
                    f"'{self.KEYRING_SERVICE}') — delete it by hand.[/red]"
                )
            elif status == "shared":
                kept = " or ".join(
                    f"'{name}'" for name in entry.get("keyring_tried", [])
                )
                _notices.print(
                    f"[yellow]Removed the locally-stored {entry['integration']} "
                    f"{noun} entry {where}, and left its keyring "
                    f"value ({kept} in service '{self.KEYRING_SERVICE}') in "
                    f"place: another integration entry in {self.config_path} "
                    f"still points at the same secret. Remove it once that "
                    f"entry is gone.[/yellow]"
                )
            elif status == "no_keyring":
                tried = " or ".join(
                    f"'{name}'" for name in entry.get("keyring_tried", [])
                )
                _notices.print(
                    f"[yellow]Removed a stale {entry['integration']} {noun} "
                    f"entry {where} — no keyring backend could be "
                    f"reached, so nothing was deleted there. If this machine "
                    f"has one, {tried} in service '{self.KEYRING_SERVICE}' is "
                    f"still in it. {advice}[/yellow]"
                )
            elif status == "absent":
                _notices.print(
                    f"[yellow]Removed a stale {entry['integration']} {noun} "
                    f"entry {where} — nothing was found in the "
                    f"keyring to delete. {advice}[/yellow]"
                )
            else:
                _notices.print(
                    f"[yellow]Removed locally-stored {entry['integration']} "
                    f"{noun} {where} — {advice}[/yellow]"
                )

    def _report_unwritten_after_keyring_clear(
        self, entries: List[Dict[str, str]], error: BaseException
    ) -> None:
        """Say what the operator is left with when the rewrite fails.

        This branch used to print "removed locally-stored board credentials
        from the keyring, but could not rewrite …" unconditionally, which is
        the same false claim `_report_purged_secrets` was fixed for
        (#614). The keyring deletes have already run, so what survives in the
        file is a stale pointer -- harmless, and retried on the next command.
        The part worth saying out loud is a secret that survived a *failed*
        delete, because only the operator can finish that job.
        """
        stuck = [
            f"{e['integration']} ({e['profile']} profile, org {e['organization']})"
            for e in entries
            if e.get("keyring") == "failed"
        ]
        message = (
            f"Warning: could not rewrite {self.config_path}: {error}. Its "
            f"credential entries are still in the file, and will be retried on "
            f"the next innoday command."
        )
        if stuck:
            message += (
                f" The keyring value for {', '.join(stuck)} could not be deleted "
                f"either — delete it by hand."
            )
        colour = "red" if stuck else "yellow"
        _notices.print(f"[{colour}]{message}[/{colour}]")

    def _merge_config(
        self, default: Dict[str, Any], loaded: Dict[str, Any]
    ) -> Dict[str, Any]:
        result = default.copy()
        for key, value in loaded.items():
            if (
                key in result
                and isinstance(result[key], dict)
                and isinstance(value, dict)
            ):
                result[key] = self._merge_config(result[key], value)
            else:
                result[key] = value
        return result

    def _apply_overrides(self, overrides: Dict[str, Any]) -> None:
        if overrides.get("api_url"):
            self._config["platform"]["api_url"] = overrides["api_url"]
        # Deliberately does NOT touch current_organization here -- an
        # explicit --organization flag is applied as a request-scoped
        # override (self._organization_override, read by
        # get_current_organization()) and is never persisted. See
        # docs/VERSION_MANAGEMENT.md sibling doc CLAUDE.md's "CLI / client
        # identity" section for the full precedence rationale.

    def _apply_cwd_project_context(self, overrides: Dict[str, Any]) -> None:
        """
        Auto-resolve org/project from a workspace's .innoday/project.yml --
        mirrors the org.alias/project.innoday_id pattern pixelfuel-claude
        skills read directly. This is the ONLY source of org/project context
        besides an explicit --organization/--project flag for this
        invocation -- there is no persistent "switch" command, and no
        fallback to a previously-persisted current_organization/project_id
        either: a directory with no .innoday/project.yml and no explicit
        override resolves to "no organization/project selected," full stop,
        even if a prior session in a different directory left a value on
        disk. This prevents exactly the confusing case of a stale org from
        a previous project silently applying in an unrelated directory.

        Precedence, highest first:
          1. An explicit --organization/--project flag for this invocation
             only (never persisted -- see get_current_organization()/
             get_current_project_id())
          2. .innoday/project.yml auto-detected from --dir (or cwd if --dir
             wasn't passed)

        If neither resolves anything, get_current_organization()/
        get_current_project_id() return None for this invocation. Those
        fields are never written to disk in the first place -- save() strips
        current_organization and platform.project_id (`config set
        organization` is rejected outright, and the init wizard / `orgs
        env-setup` only cache the org's id/name lookup, not a current org),
        so there is nothing persisted to fall back to.

        `overrides["context_dir"]` (the --dir flag) gives the resolution a
        reference point other than the process's actual cwd -- useful when
        invoking innoday from a script/skill that hasn't itself chdir'd into
        the target project directory.
        """
        org_override = overrides.get("organization")

        context_dir = overrides.get("context_dir")
        start = Path(context_dir) if context_dir else None
        try:
            context = load_project_context(start)
        except LegacyProjectFileError as exc:
            # Don't hard-exit from inside the constructor (that would break
            # library/embedded/test construction that happens to sit under a
            # legacy workspace). ALWAYS record it — two distinct decisions read
            # this: (1) the CLI entrypoint hard-stops on it for commands that
            # aren't legacy-tolerant, and (2) the legacy-tolerant commands
            # (status/whoami) read it to DISPLAY a red "run refresh" note while
            # still running. `allow_legacy_context` only means "don't let the
            # entrypoint hard-stop"; it must NOT suppress recording, or those
            # commands would have nothing to show. Upgrade commands
            # (init/join/refresh) regenerate the file and simply never read it.
            self.legacy_context_error = exc
            return
        if context is None:
            return

        org_alias = context["org_alias"]

        # --organization selects the org; it must not silently discard the
        # directory's PROJECT as well. The two flags are independent, and
        # returning early here meant `--organization hs --dir <s4c-workspace>`
        # resolved no project at all -- so every project-scoped command
        # quietly answered organization-wide instead.
        #
        # The one case where the directory's project must NOT apply is a
        # genuine redirect: if the caller named a different org, this
        # directory's project belongs to someone else, and adopting it would
        # be a wrong answer wearing the right shape.
        if org_override and org_override.strip().lower() != org_alias.lower():
            return

        self._config["current_organization"] = org_alias
        self._org_resolved_this_invocation = True
        self._config.setdefault("organizations", {})
        if org_alias not in self._config["organizations"]:
            self._config["organizations"][org_alias] = {
                "id": context["org_id"],
                "name": context["org_name"],
            }

        if context["project_id"]:
            self._config["platform"]["project_id"] = context["project_id"]
            self._project_resolved_this_invocation = True

    def save(self, stamp_version: Optional[str] = None) -> None:
        """Write the active profile back into the full config and save.

        ``stamp_version`` overrides the ``written_by_version`` stamp, which
        otherwise records the *running* CLI. Only `innoday upgrade` needs it:
        that process is the old binary replacing itself, so the running version
        is precisely the wrong thing to record.

        Refuses to write when the load degraded to defaults (see `_load_raw`).
        Without that guard, a single unreadable read turns the very next
        `config set` -- a command about ONE key -- into a full overwrite of a
        file holding every profile, its identity and its org list. That is not
        hypothetical: it destroyed a working `dev` profile, and the resulting
        401s read as an auth problem rather than as data loss.
        """
        if self._load_degraded:
            raise RuntimeError(
                f"Refusing to overwrite {self.config_path}: it exists but could "
                f"not be read, so the in-memory config is defaults rather than "
                f"your real settings. Saving now would discard every profile in "
                f"that file. Fix or move the file, then retry."
            )
        try:
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            # Sync active profile data into the raw structure.
            #
            # current_organization and platform.project_id are strictly
            # invocation-scoped -- resolved from an explicit --organization/
            # --project flag or cwd's .innoday/project.yml for THIS process
            # only. They are deliberately NOT persisted: ~/.innoday/config.json
            # is shared across every terminal using this CLI install, so
            # writing a "current org" there is global mutable state that
            # concurrent shells in different projects would clobber. The
            # getters already refuse to read a stale persisted value as a
            # fallback (get_current_organization/get_current_project_id); this
            # closes the loop by never writing it in the first place. We strip
            # it from a copy of the blob so the in-memory self._config keeps the
            # keys for reads within this same invocation.
            if "profiles" not in self._raw:
                self._raw["profiles"] = {}
            persisted = copy.deepcopy(self._config)
            persisted.pop("current_organization", None)
            if isinstance(persisted.get("platform"), dict):
                persisted["platform"].pop("project_id", None)
            self._raw["profiles"][self._current_profile] = persisted
            self._raw["current_profile"] = self._current_profile
            # Which CLI last wrote this file.
            #
            # Without it there was no way to tell a config written by the
            # installed CLI from one written months and many schema changes ago
            # -- `innoday check` could report the *installed* version and the
            # *PyPI* version but had nothing to say about the config sitting
            # between them. A profile that predates a key's introduction reads as
            # a missing setting rather than as a stale file.
            from src.version import get_version

            self._raw["written_by_version"] = stamp_version or get_version()
            with open(self.config_path, "w") as f:
                json.dump(self._raw, f, indent=2)
            console.print(f"[green]Configuration saved to {self.config_path}[/green]")
        except IOError as e:
            console.print(f"[red]Error saving configuration: {e}[/red]")
            raise

    # ------------------------------------------------------------------
    # Profile management
    # ------------------------------------------------------------------

    def get_written_by_version(self) -> Optional[str]:
        """The CLI version that last wrote this config file, if it is stamped.

        None means the file predates the stamp -- itself a useful answer, and
        deliberately not conflated with "matches the installed version".
        """
        return self._raw.get("written_by_version")

    def set_written_by_version(self, version: str) -> None:
        """Stamp a version explicitly.

        `save()` already stamps the *running* version, which covers every normal
        write. `innoday upgrade` needs this because the process doing the
        reinstall is the OLD binary: by the time the new one is on disk, the
        version that should be recorded is not the one running.
        """
        # Through save(), not around it -- save() holds the degraded-load guard
        # that stops a single unreadable read turning this into a full overwrite.
        self.save(stamp_version=version)

    def get_current_profile(self) -> str:
        return self._current_profile

    def list_profiles(self) -> List[str]:
        return list(self._raw.get("profiles", {}).keys())

    def set_current_profile(self, name: str) -> None:
        """Switch active profile and reload config."""
        if name not in self._raw.get("profiles", {}):
            raise ValueError(f"Profile '{name}' does not exist. Create it first.")
        # Flush current profile data before switching
        self._raw["profiles"][self._current_profile] = self._config
        self._current_profile = name
        self._raw["current_profile"] = name
        self._config = self._active_profile_config()
        self._color_enabled = self._config["output"]["color"]
        self.save()

    def get_default_profile(self) -> Optional[str]:
        return self._raw.get("default_profile")

    def set_default_profile(self, name: str) -> None:
        """
        Repoint the stable default-profile pointer used by non-interactive
        and MCP callers when no --profile is explicitly given. Distinct from
        set_current_profile(): this never switches what the active session
        is on, it only changes what resolution falls back to next time
        nothing else is specified. Self-saving, like set_current_profile.
        """
        if name not in self._raw.get("profiles", {}):
            raise ValueError(f"Profile '{name}' does not exist. Create it first.")
        self._raw["default_profile"] = name
        self.save()

    def create_profile(self, name: str, api_url: Optional[str] = None) -> None:
        """Create a new profile with optional api_url override."""
        if "profiles" not in self._raw:
            self._raw["profiles"] = {}
        new_profile = copy.deepcopy(_PROFILE_DEFAULTS)
        if api_url:
            new_profile["platform"]["api_url"] = api_url
        self._raw["profiles"][name] = new_profile

    def delete_profile(self, name: str) -> None:
        if name == self._current_profile:
            raise ValueError(
                f"Cannot delete the active profile '{name}'. Switch first."
            )
        self._raw.get("profiles", {}).pop(name, None)

    def get_profile_config(self, name: str) -> Optional[Dict[str, Any]]:
        """Get a profile's raw config dict (merged with defaults)."""
        data = self._raw.get("profiles", {}).get(name)
        if data is None:
            return None
        return self._merge_config(copy.deepcopy(_PROFILE_DEFAULTS), data)

    # ------------------------------------------------------------------
    # Keyring — namespaced per profile
    # ------------------------------------------------------------------

    def _keyring_key(self, key: str, profile: Optional[str] = None) -> str:
        """The keyring username for `key`, namespaced by profile.

        The single definition of that format. `profile` overrides the active
        one for the sole caller that must not use it -- the board-secret purge
        (`_clear_keyring_pointers`), which deletes entries belonging to
        *another* profile and would otherwise delete somebody else's. It built
        this string by hand, which put the format in two places: change the
        separator or the service scheme and `store_credential` and the purge
        stop agreeing silently, leaving a secret behind while the purge reports
        success -- #614 exactly.
        """
        return f"{profile or self._current_profile}_{key}"

    def store_credential(self, key: str, value: str) -> None:
        try:
            keyring.set_password(self.KEYRING_SERVICE, self._keyring_key(key), value)
        except Exception as e:
            console.print(f"[red]Error storing credential '{key}': {e}[/red]")
            raise

    def get_credential(self, key: str) -> Optional[str]:
        try:
            return keyring.get_password(self.KEYRING_SERVICE, self._keyring_key(key))
        except Exception:
            return None

    def delete_credential(self, key: str) -> None:
        try:
            keyring.delete_password(self.KEYRING_SERVICE, self._keyring_key(key))
        except keyring.errors.PasswordDeleteError:
            pass
        except Exception as e:
            console.print(f"[red]Error deleting credential '{key}': {e}[/red]")
            raise

    # ------------------------------------------------------------------
    # CLI auth token (device-flow / PAT) — stored in the keyring, keyed
    # per profile like every other credential. Sent as
    # `Authorization: Bearer <token>` by the API client (see client.py).
    # ------------------------------------------------------------------

    CLI_TOKEN_KEY = "cli_token"

    def store_cli_token(self, token: str) -> None:
        """Persist the CLI auth token in the keyring for the active profile."""
        self.store_credential(self.CLI_TOKEN_KEY, token)

    def get_cli_token(self) -> Optional[str]:
        """Resolve the CLI auth token.

        Precedence: the `INNODAY_TOKEN` env var (for CI / one-shot use) wins
        over the keyring-stored value, mirroring how tools like `gh` let an
        env token override the stored credential.
        """
        env_token = os.environ.get("INNODAY_TOKEN")
        if env_token:
            return env_token
        return self.get_credential(self.CLI_TOKEN_KEY)

    def delete_cli_token(self) -> None:
        """Remove the keyring-stored CLI auth token for the active profile."""
        self.delete_credential(self.CLI_TOKEN_KEY)

    # ------------------------------------------------------------------
    # Platform configuration
    # ------------------------------------------------------------------

    @staticmethod
    def generate_alias(name: str) -> str:
        """Derive a URL-friendly org alias from a display name."""
        alias = re.sub(r"[^a-zA-Z0-9\s-]", "", name.lower())
        alias = re.sub(r"[\s-]+", "-", alias)
        return alias.strip("-") or "org"

    def get_api_url(self) -> str:
        return self._config["platform"]["api_url"]

    def set_api_url(self, url: str) -> None:
        self._config["platform"]["api_url"] = url

    #: Per-request timeout for a sync. A sync enumerates a GitHub organization
    #: server-side before answering, so it is not a read and must not inherit a
    #: read's budget -- BPAI measured ~32s against a 30s default, which is the
    #: worst possible margin: it failed every time, at the very end, with nothing
    #: in the message to suggest the work had nearly finished.
    SYNC_TIMEOUT_FLOOR = 300.0

    def get_api_timeout(self) -> float:
        return self._config["platform"].get("api_timeout", 30.0)

    def get_sync_timeout(self) -> float:
        """The timeout a sync should use: the configured value, or the floor.

        A floor rather than a replacement, so raising ``api_timeout`` past it
        still applies. Someone who has deliberately configured a longer timeout
        wants it everywhere, not everywhere except the slowest command.
        """
        return max(self.get_api_timeout(), self.SYNC_TIMEOUT_FLOOR)

    def set_api_timeout(self, timeout: float) -> None:
        self._config["platform"]["api_timeout"] = timeout

    def get_team_secret(self) -> Optional[str]:
        return self._config["platform"].get("team_secret")

    def set_team_secret(self, secret: str) -> None:
        self._config["platform"]["team_secret"] = secret

    def get_current_project_id(self) -> Optional[str]:
        """Resolved project id for this invocation: an explicit --project
        override, or a directory's .innoday/project.yml. No persisted
        fallback -- a stale platform.project_id from a prior invocation in
        a different directory is never returned here even if it's still on
        disk (see _apply_cwd_project_context)."""
        if not self._project_resolved_this_invocation:
            return None
        return self._project_override or self._config["platform"].get("project_id")

    def set_current_project_id(self, project_id: str) -> None:
        self._config["platform"]["project_id"] = project_id
        self._project_resolved_this_invocation = True

    def set_project_override(self, project_id: str) -> None:
        """Replace this invocation's --project value with a resolved UUID.

        Distinct from `set_current_project_id`, which writes the *workspace*
        slot: `get_current_project_id` returns the override in preference to it,
        so writing the workspace slot would leave an alias still winning. Nothing
        is persisted -- the override lives for this invocation only.
        """
        self._project_override = project_id
        self._project_resolved_this_invocation = True

    # ------------------------------------------------------------------
    # User configuration
    # ------------------------------------------------------------------

    def get_user_id(self) -> Optional[str]:
        return self._config["user"]["id"]

    def set_user_info(self, user_id: str, email: str, name: str) -> None:
        """Set the profile's identity in memory. **The caller must `save()`.**

        Deliberately not self-saving, matching every other field setter here
        (`set_api_url`, `set_team_secret`, `set_output_format`, ...); only the
        profile-structure setters (`set_current_profile`, `set_default_profile`)
        write, because they rearrange `_raw` rather than set one field. A
        self-saving setter would also make each call print "Configuration saved
        to ..." and rewrite the shared config file mid-wizard, several times per
        run.

        All three callers do save: `_non_interactive_init` and
        `_streamlined_init` in cli/commands/config.py, and `_persist_user` in
        cli/commands/session.py (which `login` and `whoami` share). #619 was not
        a missing save inside this method -- it was `config init` announcing
        success with `user_id` resolved to None, and `whoami` never calling this
        at all.
        """
        self._config["user"]["id"] = user_id
        self._config["user"]["email"] = email
        self._config["user"]["name"] = name

    def get_user_info(self) -> Dict[str, Optional[str]]:
        return self._config["user"]

    # ------------------------------------------------------------------
    # Organization management
    # ------------------------------------------------------------------

    # `add_organization_integration` was here (#729). It was the only thing
    # that ever wrote a credential into ~/.innoday/config.json: it refused the
    # four board types outright (#609) and accepted `github`, `slack` and
    # `claude`. Its three callers were the `innoday config integrations`
    # wizard, deleted with it -- a wizard that minted a GitHub PAT and a Claude
    # API key no code path has ever read back. `BOARD_INTEGRATION_TYPES` still
    # earns its place next to `DEAD_INTEGRATION_TYPES`: with no writer left,
    # the two constants decide what the load-time purge removes and which of
    # the two things it says about what it removed.
    #
    # `innoday board set-cred` is the replacement for a board credential; the
    # other two have no replacement because nothing wanted them.
    #
    # `innoday orgs setup` was a second writer of the *key* (never of a
    # credential): it minted an empty `integrations` dict beside the name and
    # id of every new org, re-establishing the dead shape. Removed with this,
    # so nothing writes the key at all now.

    def _lookup_organization_entry(self, org_key: str) -> Dict[str, Any]:
        """Look up an entry in the organizations config dict by key.

        Falls back to a case-insensitive match if an exact match misses --
        organization identifiers were historically called "slug" and are now
        "alias"; both are lowercase-sanitized by convention, but a config
        file written before that convention was consistently applied (or
        edited by hand) could have a differently-cased key still present.
        This keeps existing config files working without requiring a
        one-time migration script.
        """
        orgs = self._config.get("organizations", {})
        if org_key in orgs:
            return orgs[org_key]
        lowered = org_key.lower()
        for key, value in orgs.items():
            if key.lower() == lowered:
                return value
        return {}

    # `get_organization_integration` was here. It decrypted an org's stored
    # integration credentials out of the keyring, and #609 removed its last
    # caller: every one of the five was a sync/register path attaching a
    # laptop-resident board credential to a request. Deleted rather than left
    # callerless -- a credential reader that reads like existing
    # infrastructure is the thing somebody re-wires. Vault is the only source
    # of a board credential now, and the server is the only thing that reads
    # it. (The dead `github`/`claude` entries the wizard still writes are not
    # read by this or anything else; see `_purge_local_board_secrets`.)

    def get_current_organization(self) -> Optional[str]:
        """Resolved org alias for this invocation: an explicit --organization
        flag, or a directory's .innoday/project.yml (see
        _apply_cwd_project_context). No persisted fallback -- a stale
        current_organization from a prior invocation in a different
        directory is never returned here even if it's still on disk."""
        if not self._org_resolved_this_invocation:
            return None
        return self._organization_override or self._config["current_organization"]

    def set_current_organization(self, org_alias: str) -> None:
        self._config["current_organization"] = org_alias
        self._org_resolved_this_invocation = True

    def list_organizations(self) -> list:
        return list(self._config["organizations"].keys())

    def get_organization_id(self, org_alias: str) -> Optional[str]:
        return self._lookup_organization_entry(org_alias).get("id")

    def get_organization_details(self, org_alias: str) -> Optional[Dict[str, Any]]:
        return self._config.get("organizations", {}).get(org_alias)

    # ------------------------------------------------------------------
    # Output configuration
    # ------------------------------------------------------------------

    def get_output_format(self) -> str:
        return self._config["output"]["format"]

    def set_output_format(self, format_type: str) -> None:
        if format_type in ["table", "json", "csv"]:
            self._config["output"]["format"] = format_type

    def is_color_enabled(self) -> bool:
        return self._color_enabled

    def set_color_enabled(self, enabled: bool) -> None:
        self._color_enabled = enabled
        self._config["output"]["color"] = enabled

    # ------------------------------------------------------------------
    # State checks
    # ------------------------------------------------------------------

    def is_initialized(self) -> bool:
        return bool(
            self.get_user_id()
            and self.get_current_organization()
            and self.get_api_url()
        )

    # ------------------------------------------------------------------
    # Display
    # ------------------------------------------------------------------

    def display_config(self) -> None:
        from rich.panel import Panel
        from rich.table import Table

        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Setting", style="cyan")
        table.add_column("Value", style="white")

        table.add_row("Profile", f"[bold green]{self._current_profile}[/bold green]")
        # Say plainly when this is not the shipped default. The default is the
        # deployed API; anything else means this install is pointed somewhere
        # else -- a dev deployment or a localhost -- and that is the single most
        # consequential line in this table when someone is confused about why
        # they cannot see their data. Reporting it as a bare value let it read as
        # normal.
        api_url = self.get_api_url()
        default_api_url = _PROFILE_DEFAULTS["platform"]["api_url"]
        if api_url != default_api_url:
            table.add_row(
                "API URL",
                f"[yellow]{api_url}[/yellow]  [dim](not the default "
                f"{default_api_url})[/dim]",
            )
        else:
            table.add_row("API URL", api_url)
        user_info = self.get_user_info()
        user_display = (
            f"{user_info['name']} ({user_info['email']})"
            if user_info["name"]
            else "[red]Not set[/red]"
        )
        table.add_row("User", user_display)
        table.add_row("User ID", user_info["id"] or "[red]Not set[/red]")

        # A "Claude AI" row was here. It read
        # `organizations["developer"]["integrations"]` -- a hardcoded org
        # alias -- so on every machine that has ever run this it said "Not
        # configured", whatever the operator had set. It goes with the wizard
        # that wrote the entry (#729).
        orgs = self.list_organizations()
        table.add_row(
            "Organizations", ", ".join(orgs) if orgs else "[yellow]None[/yellow]"
        )
        table.add_row(
            "Current Org", self.get_current_organization() or "[yellow]None[/yellow]"
        )

        all_profiles = self.list_profiles()
        table.add_row("All Profiles", ", ".join(all_profiles))

        table.add_row("Output Format", self.get_output_format())
        table.add_row("Color Output", "Yes" if self.is_color_enabled() else "No")
        table.add_row(
            "Team Secret",
            "***" if self.get_team_secret() else "[yellow]Not set[/yellow]",
        )
        written_by = self.get_written_by_version()
        from src.version import get_version as _running_version

        running = _running_version()
        if written_by is None:
            table.add_row(
                "Config Written By",
                "[yellow]unstamped[/yellow]  [dim](predates version stamping)[/dim]",
            )
        elif written_by != running:
            table.add_row(
                "Config Written By",
                f"[yellow]{written_by}[/yellow]  [dim](running {running})[/dim]",
            )
        else:
            table.add_row("Config Written By", written_by)

        table.add_row("Config File", str(self.config_path))

        console.print(
            Panel(
                table,
                title=f"InnoDay CLI — Profile: {self._current_profile}",
                border_style="blue",
            )
        )

        # A "Platform Server" panel was here, showing an `environment`, two
        # ports, an env file and a compose project name that `platform start`
        # wrote and `compose.run_compose` then ignored, plus a
        # `last_health_check` no code path has ever written. Removed with the
        # config block behind it (#729).

        # Secrets this load found on disk and removed (#609, widened by #729).
        # The load-time notice names them on stderr as they go; this lays the
        # same list out properly for anyone reading `config show`.
        if self.dead_local_secrets:
            dead_table = Table(show_header=True, header_style="bold magenta")
            dead_table.add_column("Profile", style="cyan")
            dead_table.add_column("Organization", style="cyan")
            dead_table.add_column("Secret", style="white")
            for entry in self.dead_local_secrets:
                dead_table.add_row(
                    entry["profile"], entry["organization"], entry["integration"]
                )
            console.print(
                Panel(
                    dead_table,
                    title=("Secrets removed from this config file — nothing read them"),
                    border_style="yellow",
                )
            )

    # ------------------------------------------------------------------
    # Migration / legacy compat
    # ------------------------------------------------------------------

    def migrate_from_old_config(self, old_config: Dict[str, Any]) -> None:
        if "api" in old_config and "url" in old_config["api"]:
            self.set_api_url(old_config["api"]["url"])
        if "client" in old_config and old_config["client"].get("id"):
            self.set_current_organization(old_config["client"]["id"])
        if "output" in old_config:
            self._config["output"] = old_config["output"]
            if "color" in old_config["output"]:
                self._color_enabled = old_config["output"]["color"]
        console.print("[yellow]Configuration migrated to new format[/yellow]")
        console.print("[yellow]Please run 'innoday init' to complete setup[/yellow]")
