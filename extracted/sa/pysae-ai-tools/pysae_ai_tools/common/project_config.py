"""Per-repo configuration read from ``.pysae-ai-tools.yaml`` at the repository root.

This file is the per-project source of truth consumed by the ai-tools skills via
``detect_context``: domain labels, Slack routing, release config, deploy topology,
and behaviour flags (issues/MR creation, board sync, changelog, ai-notes…). Every
field defaults to the *current* behaviour, so a repo without the file — or with a
partial one — behaves exactly as before: the loader is purely additive and the
hardcoded fallbacks in ``detect_context`` keep applying for unmigrated repos.

The file does **not** drive CI pipelines (GitLab ``rules:`` cannot read it); it only
configures skills. See the project ticket / ``CLAUDE.md`` for the full convention.

``project.name`` and ``project.description`` are *i18n* fields: a plain string is a
value the LLM may translate to the target language; a ``{lang: value}`` mapping gives
explicit translations, falling back to the first entry when the requested language is
absent. Resolve them with :func:`resolve_i18n` (or the ``ProjectConfig`` helpers).
"""

import json
from collections.abc import Mapping
from enum import StrEnum
from pathlib import Path
from typing import Literal, Self
from urllib.parse import quote

import yaml
from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator

from ..config import resolve_clone_dir
from .glab_cache import _cache_read, _cache_write, _glab_api
from .group import ensure_group_namespace, resolve_group

CONFIG_FILENAMES = (".pysae-ai-tools.yaml", ".pysae-ai-tools.yml")
"""Accepted file names at the repository root, in lookup order."""

SCHEMA_VERSION = 1
"""Current ``version:`` of the config schema. A file declaring another value is rejected."""

# An i18n value: a translatable string, an explicit ``{lang: value}`` mapping, or absent.
I18nText = str | dict[str, str] | None


class ProjectConfigError(Exception):
    """Raised when a *present* ``.pysae-ai-tools.yaml`` is malformed or unsupported.

    An absent file is never an error (``load_project_config`` returns ``None``);
    callers such as ``detect_context`` catch this to degrade gracefully instead of
    crashing on a typo'd config.
    """


def resolve_i18n(value: I18nText, lang: str) -> str | None:
    """Resolve an i18n field (``name`` / ``description``) for ``lang``.

    - ``str`` → returned as-is (the caller / LLM translates it if needed).
    - mapping → ``value[lang]`` when present, else the **first entry** (declaration
      order) as the default fallback; ``None`` for an empty mapping.
    - ``None`` → ``None``.
    """
    if value is None:
        return None
    if isinstance(value, str):
        return value
    if lang in value:
        return value[lang]
    return next(iter(value.values()), None)


class _Model(BaseModel):
    """Base for every sub-model: ignore unknown keys so a newer file stays loadable."""

    model_config = ConfigDict(extra="ignore")


class Project(_Model):
    name: I18nText = None  # commercial name; str = LLM-translatable | {fr,en,it} = verbatim | None
    description: I18nText = None  # short description, same i18n rule as name
    stack: str | None = None  # python | node | mobile-capacitor — drives stack-specific skill behaviour
    # The repo's GitLab labels. **The first is the primary domain** (API/Op/Driver…);
    # any following entries are secondary labels (e.g. Scheduling, Security, Test).
    labels: list[str] = Field(default_factory=list)

    def domain_label(self) -> str | None:
        """The repo's primary domain label (the first of ``labels``), or ``None``."""
        return self.labels[0] if self.labels else None


class Changelog(_Model):
    enabled: bool = True  # keep a CHANGELOG (code-changelog / code-get-next-version)


class AiNotes(_Model):
    enabled: bool = True  # generate docs/ai-notes/ during code-implement


class SlackNotifications(_Model):
    mr_review: bool = True  # post the review-request message on a new MR (slack-ask-review)
    mep: bool = True  # broadcast deploys/releases to the #mep channel
    prerelease_review: bool = True  # post the pre-release review recap (code-review-pre-release)
    renovate: bool = True  # ping the tech channel for blocking Renovate MRs (major/security) — glab renovate-notify


class Slack(_Model):
    enabled: bool = True  # master switch — false disables every Slack interaction for the repo
    tech_channel: str | None = None  # repo tech channel name, e.g. "#tech-api"
    tech_channel_id: str | None = None  # its Slack ID, e.g. "C05SWB6MXE3"
    # Deploy/MEP broadcast channel — no schema default (ai-tools holds no channel ID);
    # every repo declares it explicitly in its config.
    mep_channel: str | None = None
    mep_channel_id: str | None = None
    notifications: SlackNotifications = Field(default_factory=SlackNotifications)


class ReleaseNotes(_Model):
    enabled: bool = True  # generate user-facing release notes (code-release-notes)
    languages: list[str] = Field(default_factory=lambda: ["fr", "en", "it"])  # note languages to emit
    prompt: str | None = None  # free-form guidance steering note generation


class ReleaseReview(_Model):
    enabled: bool = True  # run the pre-release review (code-review-pre-release)
    prompt: str | None = None  # free-form guidance steering the review


class Track(StrEnum):
    """A delivery target. **Declaration order is the canonical display order** (consumed as
    ``release_status.TRACK_ORDER``). Each member carries its notification picto (``emoji``)
    and human ``label`` — the single source of truth for track rendering.
    """

    WEB = ("web", ":globe_with_meridians:", "Web")
    SERVICE = ("service", ":gear:", "Service")
    PACKAGE = ("package", ":package:", "Package")
    APPLE = ("apple", ":apple:", "iOS")
    ANDROID = ("android", ":robot_face:", "Android")
    ANDROID_ENTERPRISE = ("android-enterprise", ":lock:", "Android (Enterprise)")

    emoji: str
    label: str

    # Defaults let mypy type the enum value-lookup ``Track("web")`` (1 arg); members always
    # pass the full triple, and value-lookup returns an existing member (never re-runs this).
    def __new__(cls, value: str, emoji: str = "", label: str = "") -> Self:
        obj = str.__new__(cls, value)
        obj._value_ = value
        obj.emoji = emoji
        obj.label = label
        return obj


class Stores(_Model):
    google_play_store: bool = False  # mobile only — offer to publish to the Google Play Store
    apple_app_store: bool = False  # mobile only — offer to publish to the Apple App Store


class Release(_Model):
    notes: ReleaseNotes = Field(default_factory=ReleaseNotes)
    # Free-form, project-specific instructions run on the release branch just before the
    # release notes are generated (ci-release Step 5b). Empty ⇒ no-op. An escape hatch for
    # per-repo pre-tag preparation the generic flow can't know about (e.g. pinning a
    # dependency off a canary build, regenerating a lockfile). Like any field, it may be
    # externalised — an ``overlay:`` reference (``OVERLAY_REF_PREFIX``) or a
    # ``.pysae-ai-tools/release.prompt.md`` overlay file — since the value gets long.
    prompt: str | None = None
    gitlab_release: bool = True  # create the GitLab Release object on tag
    tag_prefix: str = "v"  # version tag prefix (e.g. "v" → v6.0.0)
    allow_prerelease: bool = False  # allow prerelease versions (e.g. v6.0.0-beta)
    review: ReleaseReview = Field(default_factory=ReleaseReview)
    tracks: list[Track] = Field(default_factory=lambda: [Track.WEB])  # validated delivery targets
    stores: Stores = Field(default_factory=Stores)


class Design(_Model):
    enabled: bool = False  # React+Tailwind front eligible to design-generate
    web_root: str | None = None  # web dir (tailwind + index.css @theme + components/ui)
    pages_proto: bool = False  # design-pages.yml wired → proto served via GitLab Pages


class Environment(_Model):
    """A deploy environment and its (declarative) topology.

    The token expansion is generic: ``<env>`` → ``name``, or ``name-<slug>`` for a
    slug-bearing environment (e.g. review). No environment name is special-cased in code —
    the Pysae specifics (which envs, their namespaces/contexts, which carries a slug) live
    in the schema defaults below, overridable per repo.
    """

    name: str
    namespace: str | None = None  # k8s namespace (falls back to name)
    kube_context: str | None = None  # kubectl context (falls back to name)
    slug: bool = False  # deploy token becomes ``name-<slug>`` (per-MR review envs)

    def token(self, slug: str | None = None) -> str:
        """The ``<env>`` expansion: ``name`` (or ``name-<slug>`` for a slug env)."""
        return f"{self.name}-{slug}" if self.slug and slug else self.name

    def k8s_namespace(self) -> str:
        return self.namespace or self.name

    def context(self) -> str:
        return self.kube_context or self.name


def resolve_env(template: str, env: "Environment", slug: str | None = None) -> str:
    """Expand ``<env>`` / ``<slug>`` in a config string for a target environment.

    ``<env>`` → ``env.token(slug)`` (``name`` or ``name-<slug>`` for a slug env);
    ``<slug>`` → the slug. A string with no token is returned unchanged — e.g. a
    deployment that is not env-prefixed (``prefect-worker``). This is the single mechanism
    for per-env values following the ``<env>-<base>`` convention; irregular per-env values
    (URLs, …) stay as explicit ``{dev: …, prod: …}`` maps.
    """
    return template.replace("<env>", env.token(slug)).replace("<slug>", slug or "")


class K8sService(_Model):
    name: str
    description: str | None = None  # short technical blurb (e.g. "ingestion/export NDP")
    deployment: str | None = None  # ArgoCD app == k8s deployment, templated (e.g. "<env>-api-ndp")
    namespace: str | None = None  # fixed namespace for non-env-templated apps (infra: "ingress", …)
    ecr_image: str | None = None  # the image this service runs — an aws.ecr entry
    datadog_service: str | None = None

    def deployment_for(self, env: "Environment", slug: str | None = None) -> str | None:
        """Resolve the deployment / ArgoCD app name for ``env`` (``None`` if not deployed)."""
        return resolve_env(self.deployment, env, slug) if self.deployment else None


class K8s(_Model):
    # Deploy environments — no schema default (ai-tools holds no Pysae topology); every
    # deploying repo declares its own (a slug env expands <env> → name-<slug>).
    environments: list[Environment] = Field(default_factory=list)
    # Secret KEY names this repo's services consume (NAMES only, never values) — a single
    # repo-level list, parent of the services it feeds.
    secrets: list[str] = Field(default_factory=list)
    services: list[K8sService] = Field(default_factory=list)

    @field_validator("environments", mode="before")
    @classmethod
    def _coerce_env_names(cls, value: object) -> object:
        """Accept a bare list of names (``[dev, prod]``) as a shorthand for environments."""
        if isinstance(value, list):
            return [{"name": item} if isinstance(item, str) else item for item in value]
        return value

    def environment(self, name: str) -> Environment | None:
        return next((env for env in self.environments if env.name == name), None)


class OpenApi(_Model):
    """OpenAPI exposure for an API repo (e.g. pysae/api). Absent for non-API repos."""

    base_url: dict[str, str] = Field(default_factory=dict)  # {"dev": "...", "prod": "..."}
    versions: list[str] = Field(default_factory=list)
    visibilities: list[str] = Field(default_factory=list)
    spec_path: str | None = None  # pattern, e.g. "/api/docs/{version}/{visibility}/openapi.json"
    swagger_path: str | None = None  # pattern, e.g. "/api/docs/{version}/{visibility}/swagger-ui"


class AwsResource(_Model):
    """A named AWS resource (S3 bucket, SecretsManager secret) with an optional blurb."""

    name: str
    description: str | None = None


def _coerce_resource_names(value: object) -> object:
    """Accept a bare list of names (``[a, b]``) as shorthand for ``[{name: a}, …]``."""
    if isinstance(value, list):
        return [{"name": item} if isinstance(item, str) else item for item in value]
    return value


class S3(_Model):
    """S3 storage — the buckets this repo owns."""

    buckets: list[AwsResource] = Field(default_factory=list)

    @field_validator("buckets", mode="before")
    @classmethod
    def _coerce(cls, value: object) -> object:
        return _coerce_resource_names(value)


class Aws(_Model):
    """AWS resources a repo owns/declares — typically an infra repo (e.g. infra-common)."""

    s3: S3 = Field(default_factory=S3)  # S3 buckets (aws.s3.buckets)
    ecr: list[AwsResource] = Field(default_factory=list)  # ECR container images
    elasticache: list[AwsResource] = Field(default_factory=list)  # ElastiCache (Redis) clusters
    secrets: list[AwsResource] = Field(default_factory=list)  # SecretsManager secret stores (NOT key values)

    @field_validator("ecr", "elasticache", "secrets", mode="before")
    @classmethod
    def _coerce(cls, value: object) -> object:
        return _coerce_resource_names(value)


class PrefectWorker(_Model):
    """A Prefect work pool (the team calls these "workers")."""

    name: str
    type: str | None = None  # kubernetes | process | prefect-agent
    environment: str | None = None  # dev | prod | …


class PrefectFlow(_Model):
    """A Prefect flow with an optional description."""

    name: str
    description: str | None = None


class Prefect(_Model):
    """Prefect topology a repo owns (e.g. pysae/prefect)."""

    workers: list[PrefectWorker] = Field(default_factory=list)
    flows: list[PrefectFlow] = Field(default_factory=list)

    @field_validator("workers", "flows", mode="before")
    @classmethod
    def _coerce_names(cls, value: object) -> object:
        if isinstance(value, list):
            return [{"name": item} if isinstance(item, str) else item for item in value]
        return value


class Issues(_Model):
    enabled: bool = True  # let skills create GitLab issues for this repo
    # Default ``type::`` label for new/triaged issues here — a strong per-repo signal
    # (e.g. infra/tooling repos → "type::technical"). None = no default (classify normally).
    default_type: str | None = None


class MergeRequests(_Model):
    enabled: bool = True  # let skills create MRs for this repo


class Board(_Model):
    enabled: bool = True  # repo tracked on the board (column placement, audit)
    sync: bool = True  # auto-advance tickets across columns (workflow:: transitions)
    # Source-branch → deploy-branch mapping for issue-workflow-update: for a ticket's MR
    # merged into a source branch, its work is "shipped" once the merge commit reaches the
    # paired deploy branch (else the ticket waits in To deploy; a source with no deploy
    # branch means no deployment step, so a merged ticket closes directly). A ``*`` may be
    # used on both sides and must correspond (the source capture fills the deploy side),
    # e.g. ``support/*: deploy/support/*``. None → the tool's default mapping
    # (``main: deploy/prod`` + ``support/*: deploy/support/*``).
    deploy_branches: dict[str, str] | None = None
    # Does the project manage the ``workflow::To deploy`` column? ``True`` (default): a merged
    # ticket waits in To deploy until its merge commit reaches a deploy branch, then closes.
    # ``False``: the repo ships at merge, so the board skips To deploy entirely and the
    # tooling closes a merged ticket right away (merge-mr and issue-workflow-update alike).
    # Set it on a repo that deploys from the MR pipeline (Terraform apply, ArgoCD sync) —
    # merging only records work already live. A repo with no deploy branch at all is detected
    # as such anyway (see ``glab/deploy_branches.py``); the flag makes the intent explicit and
    # skips the branch lookups.
    to_deploy: bool = True
    # Name of a CI job that *is* the deployment, for a repo whose shipment is not a branch
    # movement: a merged ticket has shipped once that job succeeded on its MR's pipeline.
    # Set it on a repo that deploys from the MR pipeline yet does not deploy on every merge —
    # a Terraform repo whose ``apply_prod`` is a manual job, where merging means "shipped"
    # only if someone pressed it. The branch oracle cannot express that: there is no branch
    # to compare, so ``deploy_branches`` resolves to nothing and every merged ticket looks
    # shipped. None (default) → decide from the branch topology.
    shipped_when_job: str | None = None


class Autopilot(_Model):
    """Per-repo tuning of ``code-autopilot-batch``. Every default is the current global
    behaviour; a CLI flag on the batch always overrides the value resolved here."""

    enabled: bool = False  # repo participates in code-autopilot-batch
    max_tickets: int = 5  # cap on tickets processed per batch run
    concurrency: int = 4  # parallel phase-1 tickets (worktrees); 1 = sequential, dep-ordered
    min_success_probability: int = 50  # LLM success floor; candidates below it are escalated
    completeness: bool = True  # run the Sonnet spec-completeness audit
    # Post the batch report (per-ticket + summary) to Slack. A dedicated toggle on top of the
    # repo's `slack.enabled` master switch: `autopilot.slack: false` silences the batch report
    # while keeping other Slack interactions on; `slack.enabled: false` still silences everything.
    slack: bool = True
    # CI jobs to verify, three-state on each field (None = the whole CI, the current
    # behaviour; True = same, explicit; False = nothing; a list = exactly those jobs, [] = none):
    #   ci_jobs           — pre-merge, on the MR pipeline (/code-autopilot Step 5 + merge-gate re-CI)
    #   post_merge_ci_jobs — post-merge, on the main pipeline (the deploy watch)
    # A repo with no post-merge deploy sets `post_merge_ci_jobs: false`.
    ci_jobs: list[str] | bool | None = None
    post_merge_ci_jobs: list[str] | bool | None = None
    deploy_watch_timeout: str = "20m"  # post-merge watch budget (duration string)
    deploy_watch_max_retries: int = 3  # flaky-failure retries per watched post-merge job
    # Serial merge-gate strategy for the parallel batch: "rebase" (rebase on current main +
    # re-CI + merge, universal) or "train" (add to a GitLab merge train — opt-in, Premium+).
    merge_strategy: Literal["rebase", "train"] = "rebase"
    # Crash-safety checkpoint the in-session batch rewrites after each ticket (a JSON array
    # of Outcome objects). Defaults under the user home (same root as the config cache), NOT
    # inside a repo — the processing subagents run `git add`, so a repo-internal checkpoint
    # would land in a ticket's MR. A repo may override to any absolute path.
    checkpoint_path: str = Field(
        default_factory=lambda: str(Path.home() / ".cache" / "pysae-ai-tools" / "autopilot-batch" / "checkpoint.json")
    )


class Env(_Model):
    """Which env vars ``env activate`` / ``env dotenv`` load for this repo.

    ``variables`` is a whitelist of names (usual or canonical). ``None`` (default)
    loads every supported variable; an **empty list** loads none; a list restricts
    loading to exactly those. Note the semantic gap between ``None`` and ``[]``.
    """

    variables: list[str] | None = None


class ProjectConfig(_Model):
    """Full ``.pysae-ai-tools.yaml`` document. All sections default to current behaviour."""

    version: int = SCHEMA_VERSION  # schema version; an unsupported value makes load fail loudly
    project: Project = Field(default_factory=Project)
    changelog: Changelog = Field(default_factory=Changelog)
    ai_notes: AiNotes = Field(default_factory=AiNotes)
    slack: Slack = Field(default_factory=Slack)
    release: Release = Field(default_factory=Release)
    design: Design = Field(default_factory=Design)
    k8s: K8s = Field(default_factory=K8s)
    openapi: OpenApi | None = None
    aws: Aws | None = None
    prefect: Prefect | None = None
    issues: Issues = Field(default_factory=Issues)
    merge_requests: MergeRequests = Field(default_factory=MergeRequests)
    board: Board = Field(default_factory=Board)
    autopilot: Autopilot = Field(default_factory=Autopilot)
    env: Env = Field(default_factory=Env)

    def name_for(self, lang: str) -> str | None:
        """Resolve ``project.name`` for ``lang`` (see :func:`resolve_i18n`)."""
        return resolve_i18n(self.project.name, lang)

    def description_for(self, lang: str) -> str | None:
        """Resolve ``project.description`` for ``lang`` (see :func:`resolve_i18n`)."""
        return resolve_i18n(self.project.description, lang)


def effective_config(root: Path) -> ProjectConfig:
    """Return the effective config: the file merged over schema defaults.

    A missing file or a malformed one (``ProjectConfigError``) degrades to the pure
    schema defaults — so a broken file is never fatal and each field keeps its own
    default. This is the single resolution point used by the flag helpers.
    """
    try:
        cfg = load_project_config(root)
    except ProjectConfigError:
        cfg = None
    return cfg or ProjectConfig()


def flag_enabled(root: Path, *path: str) -> bool:
    """Resolve a boolean flag by attribute ``path`` (e.g. ``"board", "sync"``).

    Reads the effective config, so each flag falls back to **its own** schema default
    (``issues.enabled`` → ``True``, ``release.allow_prerelease`` → ``False``, …),
    never a blanket default. Raises ``AttributeError`` on an unknown path.
    """
    obj: object = effective_config(root)
    for attr in path:
        obj = getattr(obj, attr)
    return bool(obj)


def slack_enabled(root: Path, notification: str | None = None) -> bool:
    """Whether Slack — and optionally a specific notification — is on for the repo.

    ``slack.enabled: false`` disables everything; otherwise the individual
    ``slack.notifications.<notification>`` toggle is honoured. Degrades to the schema
    defaults (all on) for a missing/broken file, so it never silences by accident.
    """
    cfg = effective_config(root)
    if not cfg.slack.enabled:
        return False
    if notification is None:
        return True
    return bool(getattr(cfg.slack.notifications, notification))


def config_path(root: Path) -> Path | None:
    """Return the config file path under ``root`` (``.yaml`` then ``.yml``), or ``None``."""
    for name in CONFIG_FILENAMES:
        candidate = root / name
        if candidate.is_file():
            return candidate
    return None


def load_project_config(root: Path) -> ProjectConfig | None:
    """Load the effective config from ``root``; return ``None`` when nothing is configured.

    Reads ``.pysae-ai-tools.yaml`` and lets the ``.pysae-ai-tools/`` overlay directory
    override it (see :data:`OVERLAY_DIRNAME`) — either source alone is enough, so a repo
    configured only through the overlay directory still loads. Returns ``None`` when both
    are absent (the caller keeps the historical hardcoded defaults).

    Raises :class:`ProjectConfigError` when a present source is unusable: invalid YAML, a
    non-mapping document, an unsupported ``version``, or a value that violates the schema.
    """
    path = config_path(root)
    overlay_dir = root / OVERLAY_DIRNAME
    has_overlay = overlay_dir.is_dir() and any(child.is_file() for child in overlay_dir.iterdir())
    if path is None and not has_overlay:
        return None
    text = ""
    if path is not None:
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            raise ProjectConfigError(f"{path} could not be read: {exc}") from exc
    return parse_project_config(
        text,
        str(path or overlay_dir),
        overlay_dir=overlay_dir if has_overlay else None,
        resolve_root=root,
    )


class OverlayResolveError(ProjectConfigError):
    """Raised when an ``overlay:`` reference in a config value cannot be loaded.

    The value is valid config; only the referenced target is unreachable (missing file,
    network error, non-2xx). It subclasses :class:`ProjectConfigError` so the usual
    degrade-to-defaults path applies, while commands that read a value can surface it.
    """


OVERLAY_REF_PREFIX = "overlay:"
"""Explicit marker turning a config value into a reference to load. ``overlay:`` prefixes a
``file://`` path, a bare path (relative to the repo root), or an ``http(s)://`` URL — the
value becomes that target's content. The prefix disambiguates a reference from a value that
is *itself* a URL/path (e.g. ``openapi.base_url: https://api.pysae.com`` stays literal). It
applies to **every** config field, in the YAML or in a ``.pysae-ai-tools/`` overlay file."""


def _load_overlay_ref(target: str, root: Path) -> str:
    """Load the content behind an ``overlay:`` ``target`` (the part after the prefix)."""
    ref = target.strip()
    lowered = ref.lower()
    if lowered.startswith(("http://", "https://")):
        import httpx

        try:
            response = httpx.get(ref, timeout=10.0, follow_redirects=True)
            response.raise_for_status()
        except httpx.HTTPError as exc:
            raise OverlayResolveError(f"overlay URL {ref} could not be fetched: {exc}") from exc
        return response.text
    if lowered.startswith("file://"):
        ref = ref[len("file://") :]
    path = Path(ref)
    if not path.is_absolute():
        path = root / path
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        raise OverlayResolveError(f"overlay file {path} could not be read: {exc}") from exc


def resolve_overlay_refs(value: object, root: Path) -> object:
    """Recursively replace ``overlay:`` references in ``value`` with their loaded content.

    Walks strings, mappings and lists. A string starting with :data:`OVERLAY_REF_PREFIX`
    is replaced by the content of its target (``file://`` / bare path relative to ``root`` /
    ``http(s)://``); every other value is returned unchanged. Applies to all config fields,
    so any value can be externalised. Raises :class:`OverlayResolveError` on a bad target.
    """
    if isinstance(value, str):
        if value.startswith(OVERLAY_REF_PREFIX):
            return _load_overlay_ref(value[len(OVERLAY_REF_PREFIX) :], root)
        return value
    if isinstance(value, Mapping):
        return {key: resolve_overlay_refs(item, root) for key, item in value.items()}
    if isinstance(value, list):
        return [resolve_overlay_refs(item, root) for item in value]
    return value


def _git_root(start: Path) -> Path | None:
    """Return the nearest ancestor (incl. ``start``) holding a ``.git``, else None."""
    d = start
    while True:
        if (d / ".git").exists():
            return d
        if d.parent == d:
            return None
        d = d.parent


def find_config_upwards(start: Path) -> Path | None:
    """Find ``.pysae-ai-tools.yaml`` at ``start`` or a parent, bounded by the git repo.

    Walks up from ``start`` checking each directory, stopping at the git repository
    root (never climbing above it). When ``start`` is not inside a git repository,
    only ``start`` itself is inspected — the walk never leaves a repo.
    """
    start = start.resolve()
    root = _git_root(start)
    d = start
    while True:
        found = config_path(d)
        if found is not None:
            return found
        if root is None or d == root or d.parent == d:
            return None
        d = d.parent


def configured_env_variables(start: Path) -> list[str] | None:
    """Return ``env.variables`` from the repo config found upwards from ``start``.

    ``None`` when no config exists (or it is malformed, or the field is unset) —
    meaning "load every variable". An empty list means "load none". A malformed
    file degrades to ``None`` rather than raising.
    """
    path = find_config_upwards(start)
    if path is None:
        return None
    try:
        cfg = parse_project_config(path.read_text(encoding="utf-8"), str(path))
    except (ProjectConfigError, OSError, UnicodeDecodeError):
        return None
    return cfg.env.variables


OVERLAY_DIRNAME = ".pysae-ai-tools"
"""Sibling directory of the config file. Each file overrides the config value at the
dotted key given by its **stem** (name minus the final extension), taking precedence over
``.pysae-ai-tools.yaml``. The extension is free (``.txt``, ``.md``, …). A file whose last
stem segment is an integer is a **list element** (``release.tracks.0.txt`` +
``release.tracks.1.txt`` build ``release.tracks`` in index order). The file *content* is
the value — Pydantic coerces scalars (``slack.enabled`` ← ``false``), and a prompt value
may itself be a ``file://`` / ``http(s)://`` reference. It works even without a YAML file:
the sole presence of the directory is enough to configure a repo."""


def _set_nested(tree: dict[str, object], segments: list[str], value: object) -> None:
    node = tree
    for seg in segments[:-1]:
        child = node.get(seg)
        if not isinstance(child, dict):
            child = {}
            node[seg] = child
        node = child
    node[segments[-1]] = value


def _deep_merge(base: dict[str, object], over: Mapping[str, object]) -> dict[str, object]:
    for key, value in over.items():
        current = base.get(key)
        if isinstance(value, Mapping) and isinstance(current, dict):
            _deep_merge(current, value)
        else:
            base[key] = value
    return base


def build_dir_overlay(overlay_dir: Path) -> dict[str, object]:
    """Build a config-override tree from the files in a ``.pysae-ai-tools/`` directory.

    See :data:`OVERLAY_DIRNAME` for the naming convention. Returns an empty tree when the
    directory holds no usable file. Raises :class:`ProjectConfigError` if a file can't be
    read.
    """
    scalars: list[tuple[list[str], str]] = []
    element_lists: dict[tuple[str, ...], dict[int, str]] = {}
    for path in sorted(overlay_dir.iterdir()):
        if not path.is_file() or not path.stem:
            continue
        try:
            content = path.read_text(encoding="utf-8", errors="replace").strip()
        except OSError as exc:
            raise ProjectConfigError(f"{path} could not be read: {exc}") from exc
        segments = path.stem.split(".")
        if len(segments) > 1 and segments[-1].isdigit():
            element_lists.setdefault(tuple(segments[:-1]), {})[int(segments[-1])] = content
        else:
            scalars.append((segments, content))
    tree: dict[str, object] = {}
    for segments, value in scalars:
        _set_nested(tree, segments, value)
    for key, indexed in element_lists.items():
        _set_nested(tree, list(key), [indexed[index] for index in sorted(indexed)])
    return tree


def parse_project_config(
    text: str, source: str, overlay_dir: Path | None = None, resolve_root: Path | None = None
) -> ProjectConfig:
    """Parse + validate YAML ``text`` into a ``ProjectConfig`` (shared file/GitLab core).

    ``source`` is only used to label errors. When ``overlay_dir`` is given and exists, its
    files override the parsed values before validation (see :data:`OVERLAY_DIRNAME`). When
    ``resolve_root`` is given, ``overlay:`` references in any value are loaded relative to it
    (see :func:`resolve_overlay_refs`) — done for local loads, not remote GitLab ones. Raises
    ``ProjectConfigError`` on invalid YAML, a non-mapping document, an unsupported
    ``version``, a schema violation, or an unloadable ``overlay:`` reference.
    """
    try:
        loaded = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        raise ProjectConfigError(f"{source} is not valid YAML: {exc}") from exc
    if loaded is None:
        loaded = {}
    if not isinstance(loaded, Mapping):
        raise ProjectConfigError(f"{source} must be a YAML mapping, got {type(loaded).__name__}")
    raw: dict[str, object] = dict(loaded)
    if overlay_dir is not None and overlay_dir.is_dir():
        raw = _deep_merge(raw, build_dir_overlay(overlay_dir))
    if resolve_root is not None:
        resolved = resolve_overlay_refs(raw, resolve_root)
        assert isinstance(resolved, dict)
        raw = resolved
    version = raw.get("version", SCHEMA_VERSION)
    if version != SCHEMA_VERSION:
        raise ProjectConfigError(f"{source}: unsupported version {version!r} (expected {SCHEMA_VERSION})")
    try:
        return ProjectConfig.model_validate(raw)
    except ValidationError as exc:
        raise ProjectConfigError(f"{source}: invalid configuration:\n{exc}") from exc


def load_project_config_from_gitlab(
    project: str, ref: str | None = None, *, refresh: bool = False
) -> ProjectConfig | None:
    """Load ``.pysae-ai-tools.yaml`` from a GitLab ``project`` (path or ID) via ``glab``.

    Returns ``None`` only when the file is genuinely **absent** (404) on that ref.
    ``ref`` defaults to the project's default branch. Raises ``RuntimeError`` when glab
    is unavailable, the project can't be resolved (auth/typo), or the file fetch fails
    for any non-404 reason — so callers can tell "no config" (``None``) from "couldn't
    reach GitLab". ``ProjectConfigError`` on a malformed file.

    Successful results (a config or a confirmed 404 ``None``) are cached on disk for
    ``CACHE_TTL_SECONDS``; errors are never cached. ``refresh=True`` bypasses the cache.
    """
    cache_key = f"gl:{project}@{ref or 'default'}"
    if not refresh:
        cached = _cache_read(cache_key)
        if cached is not None:
            payload = cached.get("config")
            return parse_project_config_payload(payload) if isinstance(payload, dict) else None

    enc = quote(project, safe="") if "/" in project else project
    if ref is None:
        rc, out, err = _glab_api(f"projects/{enc}")
        if rc != 0:
            raise RuntimeError(f"cannot resolve GitLab project {project!r}: {err.strip() or 'glab error'}")
        try:
            ref = str(json.loads(out).get("default_branch") or "main")
        except (json.JSONDecodeError, AttributeError):
            ref = "main"
    file_path = quote(".pysae-ai-tools.yaml", safe="")
    rc, out, err = _glab_api(f"projects/{enc}/repository/files/{file_path}/raw?ref={ref}")
    if rc != 0:
        if "404" in err:
            _cache_write(cache_key, {"config": None})  # remember "no config" too
            return None
        raise RuntimeError(f"cannot read .pysae-ai-tools.yaml from {project}@{ref}: {err.strip() or 'glab error'}")
    cfg = parse_project_config(out, f"{project}:.pysae-ai-tools.yaml@{ref}")
    _cache_write(cache_key, {"config": cfg.model_dump(mode="json")})
    return cfg


def parse_project_config_payload(payload: dict[str, object]) -> ProjectConfig:
    """Rebuild a ``ProjectConfig`` from a cached ``model_dump`` payload (lenient)."""
    return ProjectConfig.model_validate(payload)


def local_checkout(project: str) -> Path | None:
    """Return the local clone path for a GitLab ``project`` path, if it exists.

    Maps ``pysae/api`` to ``<clone-dir>/pysae/api`` using the same clone-dir resolution
    as `glab clone-group` (env > config > OS default). ``None`` when not checked out.
    """
    candidate = resolve_clone_dir() / project
    return candidate if candidate.is_dir() else None


def load_project_config_for(project: str, ref: str | None = None, *, refresh: bool = False) -> ProjectConfig | None:
    """Resolve config for a GitLab ``project``: **local checkout first, else GitLab**.

    When the project is cloned locally (under the clone dir), read its on-disk file —
    fast, offline, reflects uncommitted edits (never cached). Otherwise fetch it from
    GitLab via `glab` (cached on disk, ``refresh=True`` to bypass). Returns ``None``
    when no config file exists in the resolved source.

    An explicit ``ref`` forces the GitLab path: a local checkout can only serve its
    current working tree, so honouring an arbitrary ref means going through GitLab.
    """
    if ref is None:
        local = local_checkout(project)
        if local is not None:
            return load_project_config(local)
    return load_project_config_from_gitlab(project, ref, refresh=refresh)


def discover_project_paths(group: str | None = None, *, refresh: bool = False) -> list[str]:
    """Return every project path of ``group`` (incl. subgroups), sorted, via ``glab``.

    ``group`` defaults to the resolved group (origin namespace / env / "pysae" — see
    :func:`pysae_ai_tools.common.group.resolve_group`). The group's project list changes
    rarely, so it is cached on disk for ``CACHE_TTL_SECONDS`` (``refresh=True`` bypasses).
    Raises ``RuntimeError`` when glab is unavailable or the call fails — callers that want
    a best-effort list should catch it.
    """
    group = group or resolve_group()
    cache_key = f"discover:{group}"
    if not refresh:
        cached = _cache_read(cache_key)
        if cached is not None:
            cached_paths = cached.get("paths")
            if isinstance(cached_paths, list):
                return [str(p) for p in cached_paths]

    rc, out, err = _glab_api(
        "--paginate", f"groups/{group}/projects?include_subgroups=true&archived=false&per_page=100"
    )
    if rc != 0:
        raise RuntimeError(f"cannot list {group} projects: {err.strip() or 'glab error'}")
    # ``glab api --paginate`` concatenates one JSON array per page with no separator
    # (``[...][...]``). Decode successive arrays with raw_decode — a regex split on
    # brackets is wrong because object values (descriptions, nested arrays) contain ``]``.
    paths: list[str] = []
    decoder = json.JSONDecoder()
    text = out.strip()
    idx = 0
    try:
        while idx < len(text):
            page, end = decoder.raw_decode(text, idx)
            if isinstance(page, list):
                for proj in page:
                    if isinstance(proj, dict) and proj.get("path_with_namespace"):
                        paths.append(str(proj["path_with_namespace"]))
            idx = end
            while idx < len(text) and text[idx].isspace():
                idx += 1
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"cannot parse {group} project list from glab: {exc}") from exc
    result = sorted(set(paths))
    _cache_write(cache_key, {"paths": result})
    return result


def resolve_project_path(path: str, group: str | None = None) -> str:
    """Resolve a project reference to the path it really has in ``group`` — subgroups included.

    ``ensure_group_namespace`` only prefixes the group, so a bare name that lives in a
    subgroup resolved to a path that does not exist (``infra-cluster`` →
    ``<group>/infra-cluster`` instead of ``<group>/infra/infra-cluster``). Match the leaf
    against the group's project list (cached, subgroups included) and keep the naive
    namespacing when the leaf is unknown, ambiguous, or already a real path — so an
    unreachable API degrades to the previous behaviour instead of failing.
    """
    naive = ensure_group_namespace(path, group or resolve_group())
    try:
        known = discover_project_paths(group)
    except RuntimeError:
        return naive
    if naive in known:
        return naive
    leaf = naive.rsplit("/", 1)[-1]
    matches = [p for p in known if p.rsplit("/", 1)[-1] == leaf]
    return matches[0] if len(matches) == 1 else naive


def aggregate_project_configs(
    paths: list[str], ref: str | None = None, *, refresh: bool = False, prefer_local: bool = False
) -> dict[str, ProjectConfig]:
    """Resolve each path's config; keep only those with one. Returns ``{path: ProjectConfig}``.

    For a cross-repo aggregate the **canonical** source is each repo's default branch on
    GitLab — local checkouts are incidental (a dev may have any of them on a feature branch,
    dirty, or absent), so by default we read from GitLab and ignore local state. Pass
    ``prefer_local=True`` to read the local checkout first (reflecting uncommitted edits),
    falling back to GitLab when a repo isn't cloned. An explicit ``ref`` always forces GitLab.

    Repos whose fetch raises (auth/network) are skipped rather than aborting. Per-repo
    GitLab fetches are cached (``refresh=True`` bypasses).
    """
    fetch = load_project_config_for if prefer_local else load_project_config_from_gitlab
    found: dict[str, ProjectConfig] = {}
    for path in paths:
        try:
            cfg = fetch(path, ref=ref, refresh=refresh)
        except (RuntimeError, ProjectConfigError):
            continue
        if cfg is not None:
            found[path] = cfg
    return found


def domain_labels(refresh: bool = False) -> list[str]:
    """The domain-label vocabulary — the **union of every repo's primary domain label**
    (``project.labels[0]``; secondary labels are excluded).

    Aggregated live across the group (cached; ``refresh=True`` rebuilds). ai-tools holds
    no hardcoded domain-label list — the vocabulary is whatever the configs declare.
    Returns a sorted list, or ``[]`` when the group listing can't be reached: a glab
    failure degrades to "vocabulary unavailable" rather than propagating — callers must
    treat an empty result as "can't validate against a vocabulary", not "no domains".
    """
    try:
        paths = discover_project_paths(refresh=refresh)
    except RuntimeError:
        return []
    configs = aggregate_project_configs(paths, refresh=refresh)
    return sorted({d for cfg in configs.values() if (d := cfg.project.domain_label())})
