"""CLI argument dataclasses with layered profile resolution.

Hierarchy:
    PlatformArgs       → profile selection + identity (registry commands)
    PlatformScopeArgs  → + workspace/project context (most subcommands)
    TuiArgs            → + session launch flags (root ``dn`` command)

Resolution produces a ``Profile`` with overrides applied.
Session creation uses ``Profile.validate_scope()`` + ``ApiClient``.
"""

from __future__ import annotations

import os
import typing as t
from dataclasses import dataclass

import cyclopts

from dreadnode.app.config import DEFAULT_PLATFORM_URL, Profile, ProfileError, UserConfig

if t.TYPE_CHECKING:
    from dreadnode.app.api.client import ApiClient

# ---------------------------------------------------------------------------
# Arg dataclasses
# ---------------------------------------------------------------------------

ARGS_GROUP = cyclopts.Group("Platform")


@cyclopts.Parameter(name="*")
@dataclass
class PlatformArgs:
    """Identity + context flags shared by all commands."""

    profile: t.Annotated[
        str | None,
        cyclopts.Parameter(
            group=ARGS_GROUP,
            help="Use a saved profile by name",
        ),
    ] = None
    server: t.Annotated[
        str | None,
        cyclopts.Parameter(
            group=ARGS_GROUP,
            help="Platform API URL",
        ),
    ] = None
    api_key: t.Annotated[
        str | None,
        cyclopts.Parameter(
            group=ARGS_GROUP,
            help="API key for authentication",
        ),
    ] = None
    organization: t.Annotated[
        str | None,
        cyclopts.Parameter(
            group=ARGS_GROUP,
            help="Organization slug override",
        ),
    ] = None

    def resolve(self) -> Profile:
        """Find base profile + apply CLI arg / env var overrides.  No network calls."""
        # --- Validate mutual exclusion (explicit args only) ---
        if self.profile and self.server:
            raise ProfileError("--profile and --server are mutually exclusive")
        if self.profile and self.api_key:
            raise ProfileError("--profile and --api-key are mutually exclusive")
        if self.api_key and not self.server:
            raise ProfileError("--api-key requires --server")

        # --- Env vars ---
        env_server = os.environ.get("DREADNODE_SERVER")
        env_api_key = os.environ.get("DREADNODE_API_KEY")
        env_org = os.environ.get("DREADNODE_ORGANIZATION")
        env_ws = os.environ.get("DREADNODE_WORKSPACE")
        env_proj = os.environ.get("DREADNODE_PROJECT")

        # --- Find base profile ---
        if self.server and self.api_key:
            # Raw credentials — skip config entirely
            base = Profile(url=self.server, api_key=self.api_key)
        else:
            config = UserConfig.read()
            if self.profile:
                base = config.get(self.profile)
                if base is None:
                    raise ProfileError(f"profile not found: {self.profile}")
                if not base.api_key:
                    raise ProfileError(
                        f"profile '{self.profile}' is disconnected — use /login to re-authenticate"
                    )
            elif self.server:
                match = config.find_by_url(self.server)
                base = match[1] if match else Profile(url=self.server)
            else:
                result = config.active_profile
                base = (
                    result[1] if result and result[1].api_key else Profile(url=DEFAULT_PLATFORM_URL)
                )

        # --- Overlay: arg > env > base defaults ---
        ws = getattr(self, "workspace", None)
        proj = getattr(self, "project", None)
        return base.with_overrides(
            url=self.server or env_server,
            api_key=self.api_key or env_api_key,
            organization=self.organization or env_org,
            workspace=ws or env_ws,
            project=proj or env_proj,
        )

    def connect(self) -> tuple[ApiClient, Profile]:
        """Resolve args, validate scope, and return ``(api_client, profile)``."""
        from dreadnode.app.api.client import ApiClient

        profile = self.resolve()
        if not profile.url or not profile.api_key:
            raise RuntimeError(
                "Platform credentials required. Use --profile, --server/--api-key, "
                "or log in with `dn login`."
            )
        api = ApiClient(profile.url, api_key=profile.api_key)
        profile.validate_scope(api)
        return api, profile


@cyclopts.Parameter(name="*")
@dataclass
class PlatformScopeArgs(PlatformArgs):
    """Adds workspace/project context for commands that need them."""

    workspace: t.Annotated[
        str | None,
        cyclopts.Parameter(
            group=ARGS_GROUP,
            help="Workspace slug override",
        ),
    ] = None
    project: t.Annotated[
        str | None,
        cyclopts.Parameter(
            group=ARGS_GROUP,
            help="Project slug override",
        ),
    ] = None


TUI_GROUP = cyclopts.Group("Session")
RESUME_PICK_SENTINEL = "__dreadnode_pick_session__"


@cyclopts.Parameter(name="*")
@dataclass
class TuiArgs(PlatformScopeArgs):
    """Full launch args for the TUI."""

    runtime_server: t.Annotated[
        str | None,
        cyclopts.Parameter(
            group=TUI_GROUP,
            help="Runtime server URL (`dreadnode serve`)",
        ),
    ] = None
    resume: t.Annotated[
        str | None,
        cyclopts.Parameter(
            alias="-r",
            group=TUI_GROUP,
            help="Resume a previous session by ID (prefix match supported)",
        ),
    ] = None
    model: t.Annotated[
        str | None,
        cyclopts.Parameter(group=TUI_GROUP, help="Select model at launch"),
    ] = None
    agent: t.Annotated[
        str | None,
        cyclopts.Parameter(group=TUI_GROUP, help="Select agent at launch"),
    ] = None
    capabilities_dirs: t.Annotated[
        list[str] | None,
        cyclopts.Parameter(
            name="--capabilities-dir",
            group=TUI_GROUP,
            negative_iterable=(),
            help="Additional capabilities directory (repeatable)",
        ),
    ] = None
    capabilities: t.Annotated[
        list[str] | None,
        cyclopts.Parameter(
            name="--capability",
            group=TUI_GROUP,
            negative_iterable=(),
            help="Enable specific capability (repeatable, exclusive)",
        ),
    ] = None
    capability_flags: t.Annotated[
        list[str] | None,
        cyclopts.Parameter(
            name="--capability-flag",
            group=TUI_GROUP,
            negative_iterable=(),
            help="Override capability flag (repeatable, format: capability.flag=true|false)",
        ),
    ] = None
    prompt: t.Annotated[
        str | None,
        cyclopts.Parameter(
            group=TUI_GROUP,
            help="Prompt to send (auto-sends in TUI, executes with --print)",
        ),
    ] = None
    system_prompt: t.Annotated[
        str | None,
        cyclopts.Parameter(
            group=TUI_GROUP,
            help="Append custom instructions to generated system prompt",
        ),
    ] = None
    print_mode: t.Annotated[
        bool,
        cyclopts.Parameter(
            name="--print",
            group=TUI_GROUP,
            negative=(),
            help="Headless mode: execute --prompt, print response to stdout, exit",
        ),
    ] = False
    auto: t.Annotated[
        bool,
        cyclopts.Parameter(
            group=TUI_GROUP,
            negative=(),
            help="Launch in autonomous mode: the agent runs without human prompts, bounded by --max-steps",
        ),
    ] = False
    max_steps: t.Annotated[
        int | None,
        cyclopts.Parameter(
            group=TUI_GROUP,
            help="Step budget for autonomous mode (defaults to 30)",
        ),
    ] = None
    policy: t.Annotated[
        str | None,
        cyclopts.Parameter(
            group=TUI_GROUP,
            help="Session policy name to launch with. Overrides --auto when set.",
        ),
    ] = None
    policy_arg: t.Annotated[
        list[str] | None,
        cyclopts.Parameter(
            name="--policy-arg",
            group=TUI_GROUP,
            negative_iterable=(),
            help="Policy parameter as key=value (repeatable). Forwarded to the policy spec.",
        ),
    ] = None
    project_memory_preload_limit: t.Annotated[
        int,
        cyclopts.Parameter(
            group=TUI_GROUP,
            validator=cyclopts.validators.Number(gte=1, lte=200),
            help="Project memories to preload for each new session",
        ),
    ] = 20
