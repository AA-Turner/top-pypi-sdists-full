"""`.efterlev/config.toml` schema + read/write helpers.

v0 config is small: which baseline was selected, which LLM backend and model
to use, and where `efterlev scan` writes output. The Pydantic schema is
conservative — only fields that actually do something land here, per
CLAUDE.md's "keep it small; don't include settings that don't yet do
anything." Adding a field is a deliberate decision that lands with the code
that reads it.

Format: TOML. Read via stdlib `tomllib`; written via a small hand-rolled
formatter because Python's stdlib doesn't ship a TOML writer.
"""

from __future__ import annotations

import tomllib
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, ValidationError, model_validator

from efterlev.errors import ConfigError

DEFAULT_BASELINE = "fedramp-20x-moderate"
DEFAULT_ANTHROPIC_MODEL = "claude-opus-4-7"
DEFAULT_FALLBACK_MODEL = "claude-sonnet-4-6"

# Recommended OpenAI production model. v0.1.213 maintainer-validation on
# csp-starter-cfn: 95.8% precision + 100% recall, cheapest of the validated
# set (gpt-5 at 100%/95.8%, gpt-5.4-regular fails the citation validator).
# Used as the openai-backend default when the user doesn't pass --llm-model
# (notably the interactive `init` wizard, which never asks for a model).
DEFAULT_OPENAI_MODEL = "gpt-5.4-mini"
# Bedrock-shaped model ID for the Bedrock backend. The Anthropic short-form
# IDs the per-agent default_model values use (e.g. "claude-opus-4-7") are
# not valid Bedrock model identifiers, so the Bedrock backend always
# populates LLMConfig.model — None cannot fall through to the per-agent
# default the way it does for the Anthropic backend.
DEFAULT_BEDROCK_MODEL = "us.anthropic.claude-opus-4-7-v1:0"
# Default model for the `bedrock_openai` backend (OpenAI models served on
# Bedrock via the `bedrock-mantle` OpenAI Responses-API endpoint — AWS model
# card, launched 2026-06-01). gpt-5.5 is the default: the 2026-06-05 dispatch
# scored it 100% precision + 95.8% recall on csp-starter-cfn vs gpt-5.4 at
# 82.6% / 95.0% (gpt-5.4 over-flags procedural KSIs). Pass --llm-model
# openai.gpt-5.4 for the alternative. Commercial us-east-2 / us-west-2 only
# at launch (no GovCloud yet).
DEFAULT_BEDROCK_OPENAI_MODEL = "openai.gpt-5.5"


class LLMConfig(BaseModel):
    """Which LLM endpoint and model the generative agents call.

    `fallback_model` returned 2026-04-23 with the retry+fallback
    implementation in `llm.anthropic_client`. When the primary `model`
    fails three transient-retry attempts, `AnthropicClient` tries the
    fallback once before surfacing the error. Set to empty string
    (`fallback_model = ""`) to disable fallback entirely — useful when
    the deployment wants a single model identity in every provenance
    record.

    `backend` and `region` landed 2026-04-24 as part of SPEC-11. The
    Bedrock backend (SPEC-10) is required by the open-source launch
    posture to make GovCloud EC2 deployments possible without egress
    to anthropic.com. `region` is conditional: required when
    `backend == "bedrock"`, forbidden when `backend == "anthropic"`.
    The validator enforces the either-or at config-load time so
    misconfigured deployments fail fast rather than at first LLM call.

    Retry counts live as in-class constants in `anthropic_client.py`
    rather than in config, per the "keep it small" policy. If real-
    world operations reveal they need per-deployment tuning, they
    promote to config at that time.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    backend: Literal["anthropic", "bedrock", "claude_code", "openai", "bedrock_openai"] = (
        "anthropic"
    )
    # `bedrock_openai` (v0.1.216) routes calls to OpenAI models served on
    # AWS Bedrock via the `bedrock-mantle` OpenAI Responses-API endpoint
    # (NOT the Converse API the `bedrock` backend uses for Anthropic models).
    # Needs an AWS region (commercial us-east-2/us-west-2 at launch) and a
    # Bedrock API key (`AWS_BEARER_TOKEN_BEDROCK`). Default model
    # `openai.gpt-5.4`. Keeps OpenAI-model inference inside an AWS account
    # for customers who want Bedrock billing/governance without Anthropic
    # egress. See LIMITATIONS.md "OpenAI on Bedrock (bedrock_openai)".
    # `claude_code` (v0.1.148 / #353) routes calls through the local
    # `claude --print` subprocess so users with a Claude Pro/Max
    # subscription can run efterlev at no per-token cost. Requires
    # the `claude` binary installed and OAuth-authenticated; see
    # `efterlev.llm.claude_code_client`.
    # `openai` (v0.1.211; graduated v0.1.213) routes calls through the
    # OpenAI Chat Completions API for customers without Claude access.
    # Recommended model `gpt-5.4-mini` (95.8% precision + 100% recall on
    # csp-starter-cfn — single-fixture; gpt-5 is the safer-failure-mode
    # alternative). See LIMITATIONS.md "OpenAI backend" for the per-model
    # results and the Claude-canonical-for-3PAO-submission caveat.
    # `model` is the user's project-level model preference. None means
    # "use the agent's per-task default" — DocumentationAgent picks
    # Sonnet 4.6 for cost; Gap and Remediation pick Opus 4.7 for
    # reasoning quality. A non-None value overrides every agent's
    # default uniformly. Init writes None when the user does not pass
    # `--llm-model`, so the per-agent defaults stay live unless the
    # user explicitly opts into a single project-wide model.
    # Bedrock backend always populates this with a Bedrock-shaped
    # model ID (the Anthropic short-form IDs that the per-agent
    # defaults use are not valid Bedrock model identifiers).
    model: str | None = None
    fallback_model: str = DEFAULT_FALLBACK_MODEL
    region: str | None = None
    # v0.1.8: per-workspace max_tokens override for the gap-classification
    # call, which is the largest single completion the agent pipeline emits
    # (60 KSI verdicts + rationales in one shot). Default None means "use
    # the backend-aware default": 20480 on Anthropic API (non-streaming,
    # below the 10-minute streaming threshold), 32768 on Bedrock (no
    # equivalent threshold; Sonnet 4.6 in particular emits verbose
    # rationales that hit 20480). The v0.1.7 govnotes shakedown surfaced
    # Sonnet 4.6 truncating at 20480 with no override path. Set this
    # explicitly to override; leave None to inherit backend default.
    max_tokens: int | None = None

    @model_validator(mode="after")
    def _region_required_iff_bedrock(self) -> LLMConfig:
        if self.backend in ("bedrock", "bedrock_openai") and not self.region:
            raise ValueError(
                f"LLMConfig.region is required when backend is '{self.backend}'; "
                "set region to e.g. 'us-gov-west-1' or 'us-east-1' (bedrock) / "
                "'us-east-2' or 'us-west-2' (bedrock_openai)."
            )
        if self.backend in ("anthropic", "claude_code", "openai") and self.region is not None:
            raise ValueError(
                f"LLMConfig.region must be unset when backend is '{self.backend}' "
                "(region is only used by the Bedrock backends)."
            )
        if self.backend == "bedrock" and self.model is None:
            raise ValueError(
                "LLMConfig.model is required when backend is 'bedrock'; "
                "Bedrock model IDs differ from the Anthropic short-form IDs "
                f"the agent defaults use (e.g. '{DEFAULT_BEDROCK_MODEL}')."
            )
        if self.backend == "bedrock_openai" and self.model is None:
            raise ValueError(
                "LLMConfig.model is required when backend is 'bedrock_openai'; "
                "the agent defaults are Claude model IDs the Mantle endpoint "
                f"rejects. Set model to e.g. '{DEFAULT_BEDROCK_OPENAI_MODEL}'."
            )
        if self.backend == "openai" and self.model is None:
            # The per-agent default_model values are Claude short-form IDs
            # (claude-opus-4-7 / claude-sonnet-4-6) which the OpenAI API
            # 404s, so an openai config with model=None would fail at the
            # first agent call with a confusing cross-provider error. Reject
            # it here instead. `init` populates DEFAULT_OPENAI_MODEL for this
            # backend, so this only fires on a hand-edited or legacy config.
            raise ValueError(
                "LLMConfig.model is required when backend is 'openai'; the "
                "agent defaults are Claude model IDs that OpenAI rejects. "
                f"Set model to e.g. '{DEFAULT_OPENAI_MODEL}'."
            )
        return self


class ScanConfig(BaseModel):
    """Where `efterlev scan` reads from and writes to."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    target_dir: str = "."
    output_dir: str = "./out"


class BaselineConfig(BaseModel):
    """Which compliance baseline this workspace was initialized against."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    id: str = DEFAULT_BASELINE


class CadenceConfig(BaseModel):
    """Validation cadence declarations for the workspace.

    KSI-CSX-SUM (FedRAMP 20x cross-cutting requirement) asks providers to
    declare, per KSI, the cadence on which machine-based and non-machine-based
    validation processes run. Efterlev's per-KSI artifact embeds these values
    directly in `documentation-{ts}.json` so a 3PAO can read the cadence
    inline rather than chasing it through the customer's CI configuration.

    Both fields are free-text strings — different customers describe cadence
    differently (event-triggered, ISO 8601 duration, prose). The defaults
    describe Efterlev's typical CI integration; customers running the
    drop-in `pr-compliance-scan.yml` GitHub Action can leave them as-is, and
    customers with non-standard pipelines (Jenkins, GitLab, Drone) write
    their own values.

    Future shape (post-CR26 if FedRAMP publishes a strict format): a
    structured CadenceSpec with `mode ∈ {interval, trigger, manual}`.
    Today the artifact carries the customer's declared description verbatim.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    machine_validation_cadence: str = (
        "every PR via .github/workflows/pr-compliance-scan.yml; on save during "
        "dev via `efterlev report run --watch` (debounced 2s)"
    )
    non_machine_validation_cadence: str = (
        "Evidence Manifests reviewed at the `next_review` interval declared "
        "per manifest; Efterlev does not impose a global procedural cadence"
    )


class BoundaryConfig(BaseModel):
    """Authorization-boundary scoping declaration (Priority 4 of v1-readiness-plan).

    A FedRAMP customer typically has GovCloud Terraform in scope and commercial
    Terraform out of scope. This config declares which paths are inside the
    boundary so the scanner can mark Evidence accordingly. Without an explicit
    declaration (both lists empty), every Evidence is `boundary_undeclared` —
    findings still flow but the customer hasn't told us their scope.

    Patterns are gitignore-style (gitwildmatch). The same syntax customers
    expect from `.gitignore`: `boundary/**` matches anything under `boundary/`,
    `**/main.tf` matches all `main.tf` files anywhere, etc.

    Decision precedence: `exclude` wins. A path matching both an `include`
    pattern and an `exclude` pattern is `out_of_boundary`. An empty `include`
    with non-empty `exclude` means "everything except these"; an empty
    `exclude` with non-empty `include` means "only these"; both empty means
    `boundary_undeclared`.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    include: list[str] = Field(default_factory=list)
    exclude: list[str] = Field(default_factory=list)


class CacheConfig(BaseModel):
    """LLM response cache settings (v0.1.151 / #356).

    Default `mode = "on"` so repeated /report runs on the same workspace
    hit the on-disk cache (`<workspace>/.efterlev/llm-cache/`) instead of
    paying full LLM cost every time. Cache key is sha256 of the call
    shape with per-run nonces normalized out — see
    `efterlev.llm.cache._cache_key`.

    Override via `.efterlev/config.toml`:
      [cache]
      mode = "off"    # disable entirely
      mode = "record" # write-only (always call backend, populate cache)
      mode = "replay" # read-only (raise on miss; useful for tests)

    Or override per-shell-session via the `EFTERLEV_LLM_CACHE` env var,
    which wins over the config file. Env-var precedence preserves the
    v0.1.147 ad-hoc on/off control.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    mode: Literal["on", "off", "record", "replay"] = "on"


class ScopeConfig(BaseModel):
    """Shared-responsibility / inherited-control declaration (v0.1.171 / #377).

    FedRAMP runs on a shared-responsibility model: a CSP customer
    inherits certain controls from the cloud provider (e.g. an AWS
    serverless shop inherits host/hypervisor controls AWS manages). For
    such KSIs the honest status is "implemented (inherited)" with a
    documented basis — NOT "not applicable" (they DO apply; the CSP
    satisfies them) and NOT "not implemented" (the customer isn't
    failing them).

    `inherited` lists the KSI ids declared CSP-inherited. `efterlev
    scope apply` then writes an `implemented` claim + an
    inheritance-basis evidence record for each — UNLESS the scanner
    found customer-side evidence citing the KSI, which contradicts the
    "fully inherited" claim (the customer manages it themselves) and is
    flagged for review instead.

    `inherited_profile` records which built-in profile populated the
    list (e.g. "aws-serverless"), so `scope --show` can reproduce the
    per-KSI rationale and a reviewer can see the basis.

    Why not architecture→not_applicable: 20x KSIs are outcome-based and
    architecture-agnostic. Almost none are genuinely inapplicable to a
    serverless system — they're satisfied differently (managed
    platform) or inherited. Marking them n/a would be less accurate.
    See DECISIONS / design notes 2026-05-20.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    inherited: list[str] = Field(default_factory=list)
    inherited_profile: str | None = None


class ProfileOverrides(BaseModel):
    """A profile's optional overrides on the top-level Config.

    v0.1.166 / #371 — multi-environment support. Profiles live under
    `[profile.<name>]` in `.efterlev/config.toml`. Each field is
    optional; unset fields inherit from the top-level Config.

    Example TOML:

        [profile.staging]
        # Reuse top-level baseline + cadence; override boundary + scan dir.

        [profile.staging.boundary]
        include = ["infra/terraform/staging/**"]

        [profile.staging.scan]
        target_dir = "."
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    baseline: BaselineConfig | None = None
    boundary: BoundaryConfig | None = None
    scan: ScanConfig | None = None


class Config(BaseModel):
    """Top-level `.efterlev/config.toml` schema."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    llm: LLMConfig = Field(default_factory=LLMConfig)
    scan: ScanConfig = Field(default_factory=ScanConfig)
    baseline: BaselineConfig = Field(default_factory=BaselineConfig)
    boundary: BoundaryConfig = Field(default_factory=BoundaryConfig)
    cadence: CadenceConfig = Field(default_factory=CadenceConfig)
    cache: CacheConfig = Field(default_factory=CacheConfig)
    # v0.1.171 / #377: shared-responsibility inherited-control declaration.
    scope: ScopeConfig = Field(default_factory=ScopeConfig)
    # v0.1.166 / #371: named profiles for multi-environment scoping.
    # Keyed by profile name (str). When EFTERLEV_PROFILE selects a
    # named profile, its fields override the top-level equivalents.
    profile: dict[str, ProfileOverrides] = Field(default_factory=dict)


def load_config(path: Path) -> Config:
    """Read and parse `.efterlev/config.toml`; raise `ConfigError` on malformed input.

    v0.1.166 / #371: when `EFTERLEV_PROFILE` is set, the named profile's
    `[profile.<name>]` overrides are merged onto the returned Config so
    every downstream caller sees the profile-scoped boundary / baseline
    / scan-target without explicit threading. Backward-compatible:
    unset env var = no profile = top-level config returned unchanged.
    """
    if not path.is_file():
        raise ConfigError(f"config not found at {path}")
    try:
        with path.open("rb") as f:
            raw = tomllib.load(f)
    except tomllib.TOMLDecodeError as e:
        raise ConfigError(f"config at {path} is not valid TOML: {e}") from e
    try:
        config = Config.model_validate(raw)
    except ValidationError as e:
        raise ConfigError(f"config at {path} does not match schema: {e}") from e
    return _apply_active_profile(config, path)


def _apply_active_profile(config: Config, path: Path) -> Config:
    """If `EFTERLEV_PROFILE` is set, merge the named profile's overrides
    onto the top-level Config. Unset env var → return unchanged.

    Raises `ConfigError` if the env var names a profile not in the
    config (typo'd profile names should surface immediately, not
    silently scan the wrong thing).
    """
    from efterlev.profile import get_active_profile

    active = get_active_profile()
    if active is None:
        return config
    if active not in config.profile:
        available = sorted(config.profile.keys())
        msg = f"EFTERLEV_PROFILE={active!r} but no [profile.{active}] section in {path}. "
        if available:
            msg += f"Available profiles: {', '.join(available)}."
        else:
            msg += "No profiles are defined; add a [profile.<name>] section."
        raise ConfigError(msg)
    overrides = config.profile[active]
    # Merge: each non-None field on the override replaces the top-level
    # equivalent; None means "inherit unchanged."
    merged = config.model_dump(mode="python")
    if overrides.baseline is not None:
        merged["baseline"] = overrides.baseline.model_dump(mode="python")
    if overrides.boundary is not None:
        merged["boundary"] = overrides.boundary.model_dump(mode="python")
    if overrides.scan is not None:
        merged["scan"] = overrides.scan.model_dump(mode="python")
    return Config.model_validate(merged)


def save_config(config: Config, path: Path) -> None:
    """Write `config` as TOML to `path`. Creates parent directories."""
    path.parent.mkdir(parents=True, exist_ok=True)
    llm_lines = [
        "[llm]",
        f'backend = "{config.llm.backend}"',
    ]
    # Skip the `model` line when None — pydantic accepts a missing field via
    # the LLMConfig.model default, and writing `model = "None"` would be
    # interpreted as a literal string "None" by tomllib on the next load.
    # None means "use the agent's per-task default"; the absence of the line
    # is the canonical encoding of that intent.
    if config.llm.model is not None:
        llm_lines.append(f'model = "{config.llm.model}"')
    llm_lines.append(f'fallback_model = "{config.llm.fallback_model}"')
    # SPEC-11: emit region only for the Bedrock backends to keep the default
    # (anthropic) config visually minimal. Pydantic validator guarantees
    # region is set iff backend is a Bedrock backend.
    if config.llm.backend in ("bedrock", "bedrock_openai"):
        llm_lines.append(f'region = "{config.llm.region}"')
    lines = [
        "# Efterlev workspace config — written by `efterlev init`.",
        "# Edit freely; `efterlev` commands read this on every invocation.",
        "",
        *llm_lines,
        "",
        "[scan]",
        f'target_dir = "{config.scan.target_dir}"',
        f'output_dir = "{config.scan.output_dir}"',
        "",
        "[baseline]",
        f'id = "{config.baseline.id}"',
        "",
    ]
    # Emit `[boundary]` only when the customer has declared something. Empty
    # boundary is the default ("boundary_undeclared"); writing the header with
    # empty arrays would suggest a meaningful empty declaration when there
    # isn't one, and tomllib loads a missing section as the default
    # (BoundaryConfig() with empty lists) anyway.
    if config.boundary.include or config.boundary.exclude:
        boundary_lines = ["[boundary]"]
        if config.boundary.include:
            boundary_lines.append(_format_string_list("include", config.boundary.include))
        if config.boundary.exclude:
            boundary_lines.append(_format_string_list("exclude", config.boundary.exclude))
        boundary_lines.append("")
        lines.extend(boundary_lines)
    # Always emit `[cadence]` so customers see the values their attestation
    # artifact will carry and can edit them. Defaults describe Efterlev's
    # canonical CI integration; non-default values customize the artifact.
    machine_val = _toml_escape(config.cadence.machine_validation_cadence)
    non_machine_val = _toml_escape(config.cadence.non_machine_validation_cadence)
    cadence_lines = [
        "[cadence]",
        f"machine_validation_cadence = {machine_val}",
        f"non_machine_validation_cadence = {non_machine_val}",
        "",
    ]
    lines.extend(cadence_lines)
    # v0.1.151 / #356: emit [cache] so customers see (and can edit) the
    # mode. Default "on" means repeated /report runs replay from disk
    # for free; "off" disables, "record" / "replay" gate read vs write.
    cache_lines = [
        "[cache]",
        f'mode = "{config.cache.mode}"',
        "",
    ]
    lines.extend(cache_lines)

    # v0.1.171 / #377: emit [scope] only when the customer has declared
    # inherited controls. Default (empty) config has none; tomllib loads
    # a missing section as the default ScopeConfig() anyway.
    if config.scope.inherited:
        scope_lines = ["[scope]"]
        if config.scope.inherited_profile is not None:
            scope_lines.append(f'inherited_profile = "{config.scope.inherited_profile}"')
        scope_lines.append(_format_string_list("inherited", config.scope.inherited))
        scope_lines.append("")
        lines.extend(scope_lines)

    # v0.1.166 / #371: profile sections. Emit only when the customer
    # has declared at least one; default config has none.
    for profile_name in sorted(config.profile.keys()):
        overrides = config.profile[profile_name]
        lines.append(f"[profile.{profile_name}]")
        lines.append(
            f"# Active when EFTERLEV_PROFILE={profile_name!r} or "
            f"`--profile {profile_name}` is passed."
        )
        lines.append("")
        if overrides.baseline is not None:
            lines.append(f"[profile.{profile_name}.baseline]")
            lines.append(f'id = "{overrides.baseline.id}"')
            lines.append("")
        if overrides.boundary is not None:
            lines.append(f"[profile.{profile_name}.boundary]")
            if overrides.boundary.include:
                lines.append(_format_string_list("include", overrides.boundary.include))
            if overrides.boundary.exclude:
                lines.append(_format_string_list("exclude", overrides.boundary.exclude))
            lines.append("")
        if overrides.scan is not None:
            lines.append(f"[profile.{profile_name}.scan]")
            lines.append(f'target_dir = "{overrides.scan.target_dir}"')
            lines.append(f'output_dir = "{overrides.scan.output_dir}"')
            lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")


def _toml_escape(s: str) -> str:
    # TOML basic strings need backslash + quote escaping. The cadence
    # defaults contain backticks and parens but no quotes/backslashes; an
    # explicit escape pass keeps user-supplied values safe regardless.
    escaped = s.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def _format_string_list(field_name: str, values: list[str]) -> str:
    """Format a TOML list-of-strings on one line. e.g. include = ["a", "b"].

    Used for BoundaryConfig.include / exclude. Multi-line array would be
    valid TOML too but one-line is more grep-able for short lists, which
    is the expected scale for boundary declarations (a handful of
    patterns per project).
    """
    quoted = ", ".join(f'"{v}"' for v in values)
    return f"{field_name} = [{quoted}]"
