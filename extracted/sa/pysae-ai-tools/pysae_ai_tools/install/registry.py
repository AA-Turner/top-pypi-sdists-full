"""Declarative registry of installable tools.

Holds the orchestration-only metadata for every tool the meta-installer knows
about: its name, install module, mode (required/optional), category,
default-selection, one-line description and tool dependencies. Environment-
variable metadata is **not** declared here — each tool module is the single
source of truth for its own env vars (their names, phase and help text); the
:class:`Tool` entry surfaces them lazily through the :attr:`Tool.env` view.

Also hosts :func:`_instance`, the single typed entry point used across the
meta-installer to reach a tool module's :class:`~common.base.BaseTool`.
"""

import importlib
import shutil
from dataclasses import dataclass, field
from enum import StrEnum
from typing import cast

from .common.base import BaseTool


class Mode(StrEnum):
    REQUIRED = "required"
    OPTIONAL = "optional"


class Category(StrEnum):
    """High-level family of an install entry — used to group output.

    - ``LANGUAGE`` — language toolchain (uv, python, fnm, node, …).
    - ``CLI`` — locally-installed binary (aws, kubectl, terraform, …).
    - ``MCP`` — locally-installed MCP server registered in each present assistant's
      store (``~/.claude.json`` for Claude, ``~/.codex/config.toml`` for Codex).
    - ``PLUGIN`` — per-assistant skills deployment: the Claude Code plugin
      (skills marketplace) under ``~/.claude/plugins/`` and
      ``~/.local/share/pysae-ai-tools/``, and the Codex skills under
      ``~/.agents/skills``.
    - ``EMBEDDED`` — local integrations with no standalone artifact (no
      binary on PATH, no MCP server, no skill): assistant hooks
      (``mcp-cleanup-hook``, ``usage-guard``, ``activity-tracker``), shell
      wiring (``pysae-env-shell``), cron entries (``usage-primer``) and pure
      env-var groupings (``slack-env``).
    """

    LANGUAGE = "language"
    CLI = "cli"
    MCP = "mcp"
    PLUGIN = "plugin"
    EMBEDDED = "embedded"


def _instance(module_path: str) -> BaseTool:
    """Import a tool module and return its ``tool`` instance.

    Every install module exposes exactly one :class:`BaseTool` under the
    attribute ``tool``; the orchestrator drives everything through that typed
    contract — no ``getattr`` probing of module-level symbols.
    """
    mod = importlib.import_module(module_path)
    return cast(BaseTool, mod.tool)


# ---------------------------------------------------------------------------
# Environment metadata (sourced from each tool module)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ToolEnv:
    """A tool's effective environment-variable metadata, resolved from its module.

    - ``pre`` — vars resolved **before** the binary is installed (gates the
      install in non-interactive mode).
    - ``post`` — vars resolved **after** the binary is in place (best-effort).
    - ``optional`` — tunables asked at configure-time; never gate the install.
    - ``help`` — ``var → how to obtain it`` hints.
    """

    pre: tuple[str, ...] = ()
    post: tuple[str, ...] = ()
    optional: tuple[str, ...] = ()
    help: dict[str, str] = field(default_factory=dict)

    @property
    def all(self) -> tuple[str, ...]:
        return self.pre + self.post + self.optional


def _module_env(module_path: str, category: Category) -> ToolEnv:
    """Read a tool module's declared environment-variable metadata.

    The tool class is the single source of truth: it declares
    ``env_pre_configure`` / ``env_post_configure`` / ``env_optional`` as class
    attributes (with help either inline on its ``env_vars`` or in an ``env_help``
    class attribute). MCP servers bake their secrets into the assistant config
    at configure time, so every env var they declare gates the install (``pre``)
    unless the class says otherwise.
    """
    try:
        instance = _instance(module_path)
    except Exception:  # noqa: BLE001
        return ToolEnv()

    pre = tuple(getattr(instance, "env_pre_configure", ()) or ())
    post = tuple(getattr(instance, "env_post_configure", ()) or ())
    optional = tuple(getattr(instance, "env_optional", ()) or ())
    help_map = dict(instance.env_help)

    # MCP servers no longer bake secrets at configure time — the shim resolves them
    # at launch — so their env vars never gate the install. They stay available as
    # ``optional`` metadata (help text) without being prompted for.
    if not (pre or post or optional) and category is Category.MCP:
        optional = tuple(instance.env_required)

    return ToolEnv(pre=pre, post=post, optional=optional, help=help_map)


# ---------------------------------------------------------------------------
# Tool registry entry
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Tool:
    """One install-* skill to orchestrate — orchestration metadata only.

    Environment-variable metadata is owned by the tool module (see
    :func:`_module_env`) and surfaced lazily through :attr:`env`. The
    ``env_pre_configure`` / ``env_post_configure`` / ``env_optional`` /
    ``env_help`` fields are an explicit override used for synthetic entries
    (tests); left empty, the metadata is read from the tool module.
    """

    name: str
    module: str  # import path, e.g. "pysae_ai_tools.install.glab"
    mode: Mode = Mode.OPTIONAL
    category: Category = Category.CLI
    default_selected: bool = True  # pre-checked in the first-run interactive checklist
    description: str = ""  # one-line summary shown in the configure checklist
    # Names of other TOOLS this tool's installer needs on PATH beforehand
    # (e.g. codex's installer pipes through jq). Each is installed just before
    # this tool's binary when missing, regardless of registry order or whether
    # it's in the user's selection. Must be acyclic.
    depends: tuple[str, ...] = ()
    # Explicit env override (default: read from the tool module).
    env_pre_configure: tuple[str, ...] = ()
    env_post_configure: tuple[str, ...] = ()
    env_optional: tuple[str, ...] = ()
    env_help: dict[str, str] = field(default_factory=dict)

    @property
    def env(self) -> ToolEnv:
        """Effective env metadata: the explicit override if any, else the module's."""
        if self.env_pre_configure or self.env_post_configure or self.env_optional or self.env_help:
            return ToolEnv(
                pre=tuple(self.env_pre_configure),
                post=tuple(self.env_post_configure),
                optional=tuple(self.env_optional),
                help=dict(self.env_help),
            )
        return _module_env(self.module, self.category)

    @property
    def env_vars(self) -> tuple[str, ...]:
        """All env vars declared by this tool, regardless of phase."""
        return self.env.all

    @property
    def installed(self) -> bool:
        """Lightweight presence check — no ``get_state()``, no network calls.

        Answers "is this tool *here* on the system?" only — without
        verifying auth, config, or version freshness. Use
        :attr:`configured` when full readiness matters.

        - ``EMBEDDED`` → always True (no install).
        - ``CLI`` → any binary the tool declares via ``binary_names()`` on PATH.
        - ``MCP`` → server entry registered on any active target (Claude's
          ``~/.claude.json`` or Codex's ``~/.codex/config.toml``). Multi-server
          MCPs are considered installed when at least one of their server names
          is present.
        """
        if self.category is Category.EMBEDDED:
            return True

        try:
            instance = _instance(self.module)
        except Exception:  # noqa: BLE001
            return False

        if self.category is Category.MCP:
            from .common.assistants import active_assistants
            from .common.mcp_manifest import deployed_plugin_servers
            from .common.skills_deploy import claude_plugin_manifest_path

            names = instance.mcp_server_names()
            # Present when carried in a store we write to (Codex) or declared by the
            # deployed Claude plugin manifest.
            if any(a.mcp.get(name) is not None for a in active_assistants() for name in names):
                return True
            declared = deployed_plugin_servers(claude_plugin_manifest_path())
            return any(name in declared for name in names)

        return any(shutil.which(b) is not None for b in instance.binary_names())

    @property
    def configured(self) -> bool:
        """Heavy readiness check — calls ``get_state()`` (may hit network).

        Returns True when the tool is installed *and* its state reports
        no pending install/update. Use when a downstream step needs the
        tool fully ready (auth ok, config in place, etc.).
        """
        try:
            return _instance(self.module).get_state().installed
        except Exception:  # noqa: BLE001
            return False


# Order matters: foundational tools first, dependents next.
TOOLS: tuple[Tool, ...] = (
    # Tier 1 — auth foundations (REQUIRED: many downstream tools need these)
    # uv must run first: python relies on it.
    Tool(
        "uv",
        "pysae_ai_tools.install.uv",
        Mode.REQUIRED,
        category=Category.LANGUAGE,
        description="uv — Astral Python toolchain (gestionnaire d'interpréteurs et CLIs Python)",
    ),
    # aws must run early: kubectl/EKS, mongodb-atlas-mcp (Secrets Manager), secrets read/write all depend on it.
    Tool(
        "aws",
        "pysae_ai_tools.install.aws_cli",
        Mode.REQUIRED,
        category=Category.CLI,
        description="AWS CLI — auth EKS, Secrets Manager, S3",
    ),
    Tool(
        "git",
        "pysae_ai_tools.install.git",
        Mode.REQUIRED,
        category=Category.CLI,
        description="Git — version control",
    ),
    Tool(
        "fnm",
        "pysae_ai_tools.install.fnm",
        Mode.REQUIRED,
        category=Category.LANGUAGE,
        description="fnm — Fast Node Manager (gestionnaire de versions Node)",
    ),
    Tool(
        "node",
        "pysae_ai_tools.install.node",
        Mode.REQUIRED,
        category=Category.LANGUAGE,
        description="Node.js (LTS) — runtime ; installe fnm si node manque",
    ),
    Tool(
        "python",
        "pysae_ai_tools.install.python",
        Mode.REQUIRED,
        category=Category.LANGUAGE,
        description="Python 3.14 — interpréteur géré par uv",
    ),
    Tool(
        "claude-code",
        "pysae_ai_tools.install.claude_code",
        Mode.OPTIONAL,
        category=Category.CLI,
        # Optional like every assistant CLI — the package is assistant-agnostic (Claude and
        # Codex are peers; neither is required). Anthropic's official installer is idempotent;
        # running it again bumps to the latest version, no env vars to gate.
        description="Claude Code CLI — Anthropic's terminal AI coding assistant",
    ),
    Tool(
        "codex",
        "pysae_ai_tools.install.codex",
        Mode.OPTIONAL,
        category=Category.CLI,
        # Installed via npm (idempotent; running it again bumps to the latest
        # version), no env vars to gate. Node is a required tool, so npm is
        # always available.
        description="Codex CLI — OpenAI's terminal AI coding assistant",
    ),
    Tool(
        "codex-flow",
        "pysae_ai_tools.install.codex_flow",
        Mode.OPTIONAL,
        category=Category.CLI,
        default_selected=False,
        # Community npm package (Workflow mirror for Codex) — opt-in, local/dev only,
        # never in CI. Installed via npm like codex; needs Node, and registers itself
        # with the Codex CLI when present.
        depends=("node", "codex"),
        description="codex-flow — Workflow-mirror runtime for Codex (parallel autopilot-batch)",
    ),
    Tool(
        "claude-plugin",
        "pysae_ai_tools.install.claude_plugin",
        Mode.OPTIONAL,
        category=Category.PLUGIN,
        # Auto-detects editable mode from the running package — installs
        # via symlinks when pysae_ai_tools itself is editable, deep-copies
        # otherwise. Must run after claude-code (uses ``claude plugin
        # marketplace add``).
        description="Pysae Claude Code skills + marketplace",
    ),
    Tool(
        "codex-plugin",
        "pysae_ai_tools.install.codex_plugin",
        Mode.OPTIONAL,
        category=Category.PLUGIN,
        # No-op when the codex CLI is absent. Deploys the Codex-targeted skills
        # (converted from the canonical Claude SKILL.md) into ``$HOME/.agents/skills``.
        # Runs after codex so the CLI-presence check reflects a just-installed CLI.
        description="Pysae Codex skills (converted from the Claude source)",
    ),
    Tool(
        "glab",
        "pysae_ai_tools.install.glab",
        Mode.OPTIONAL,
        category=Category.CLI,
        description="GitLab CLI — MRs, issues, pipelines",
    ),
    Tool(
        "gh",
        "pysae_ai_tools.install.gh",
        Mode.OPTIONAL,
        category=Category.CLI,
        default_selected=False,
        description="GitHub CLI — PRs, issues, releases",
    ),
    # Tier 2 — Kubernetes stack (depends on aws for EKS)
    Tool(
        "kubectl",
        "pysae_ai_tools.install.kubectl",
        Mode.OPTIONAL,
        category=Category.CLI,
        description="kubectl — Kubernetes CLI (pods, logs, exec) ; configure les contextes EKS pysae-dev/pysae-prod",
    ),
    Tool(
        "helm",
        "pysae_ai_tools.install.helm",
        Mode.OPTIONAL,
        category=Category.CLI,
        description="Helm — Kubernetes chart templating and releases",
    ),
    Tool(
        "argocd",
        "pysae_ai_tools.install.argocd",
        Mode.OPTIONAL,
        category=Category.CLI,
        description="ArgoCD CLI — GitOps deployments",
    ),
    # Tier 3 — generic tools
    Tool(
        "docker",
        "pysae_ai_tools.install.docker",
        Mode.OPTIONAL,
        category=Category.CLI,
        default_selected=False,
        description="Docker — containers",
    ),
    Tool(
        "terraform",
        "pysae_ai_tools.install.terraform",
        Mode.OPTIONAL,
        category=Category.CLI,
        description="Terraform — infrastructure as code",
    ),
    Tool(
        "prefect",
        "pysae_ai_tools.install.prefect",
        Mode.OPTIONAL,
        category=Category.CLI,
        description="Prefect CLI — workflow orchestration",
    ),
    Tool(
        "mongo-tools",
        "pysae_ai_tools.install.mongo_tools",
        Mode.OPTIONAL,
        category=Category.CLI,
        description="MongoDB tools — mongodump/restore/export",
    ),
    Tool(
        "atlas",
        "pysae_ai_tools.install.atlas_cli",
        Mode.OPTIONAL,
        category=Category.CLI,
        description="MongoDB Atlas CLI — manage clusters, users, network access (dev/prod/org profiles)",
    ),
    Tool(
        "jq",
        "pysae_ai_tools.install.jq",
        Mode.OPTIONAL,
        category=Category.CLI,
        description="jq — command-line JSON processor",
    ),
    Tool(
        "postman",
        "pysae_ai_tools.install.postman",
        Mode.OPTIONAL,
        category=Category.CLI,
        default_selected=False,
        description="Postman / Newman CLI",
    ),
    Tool(
        "bruno",
        "pysae_ai_tools.install.bruno",
        Mode.OPTIONAL,
        category=Category.CLI,
        default_selected=False,
        description="Bruno — client API open-source (alternative à Postman)",
    ),
    # Tier 4 — MCP servers (no env vars needed)
    Tool(
        "chrome-mcp",
        "pysae_ai_tools.install.chrome_mcp",
        Mode.OPTIONAL,
        category=Category.MCP,
        # Launches Chrome on a dedicated, persistent ``--user-data-dir``
        # (Claude's own profile) so sign-ins survive across runs.
        description="MCP — Chrome DevTools (browser automation)",
    ),
    # Kubernetes MCP : split dev / prod, each pinned to its kubeconfig
    # context (pysae-dev / pysae-prod). Mirrors the mongo dev/prod split —
    # prod is read-only. Auth rides the kubeconfig, so no env vars.
    Tool(
        "kubernetes-mcp-dev",
        "pysae_ai_tools.install.kubernetes_mcp_dev",
        Mode.OPTIONAL,
        category=Category.MCP,
        description="MCP — Kubernetes dev (pods, logs, exec ; contexte pysae-dev, read/write)",
    ),
    Tool(
        "kubernetes-mcp-prod",
        "pysae_ai_tools.install.kubernetes_mcp_prod",
        Mode.OPTIONAL,
        category=Category.MCP,
        description="MCP — Kubernetes prod (contexte pysae-prod, read-only)",
    ),
    # Tier 5 — MCP servers requiring secrets
    Tool(
        "gitlab-mcp",
        "pysae_ai_tools.install.gitlab_mcp",
        Mode.OPTIONAL,
        category=Category.MCP,
        description="MCP — GitLab API (MRs, issues, jobs)",
    ),
    Tool(
        "datadog-mcp",
        "pysae_ai_tools.install.datadog_mcp",
        Mode.OPTIONAL,
        category=Category.MCP,
        description="MCP — Datadog logs, metrics, monitors",
    ),
    Tool(
        "postman-mcp",
        "pysae_ai_tools.install.postman_mcp",
        Mode.OPTIONAL,
        category=Category.MCP,
        default_selected=False,
        description="MCP — Postman collections and specs",
    ),
    # MongoDB MCP : split dev / prod — un utilisateur peut n'avoir accès
    # qu'à l'URI de dev (pas à celui de prod).
    Tool(
        "mongo-mcp-dev",
        "pysae_ai_tools.install.mongo_mcp_dev",
        Mode.OPTIONAL,
        category=Category.MCP,
        description="MCP — MongoDB queries (dev, read/write)",
    ),
    Tool(
        "mongo-mcp-prod",
        "pysae_ai_tools.install.mongo_mcp_prod",
        Mode.OPTIONAL,
        category=Category.MCP,
        description="MCP — MongoDB queries (prod, read-only)",
    ),
    # MongoDB Atlas MCP : split dev / prod / org — un utilisateur peut n'avoir
    # accès qu'à certaines clés (les clés org sont opt-in). Chaque serveur pull
    # ses clés depuis AWS Secrets Manager à l'install — no env required.
    Tool(
        "mongodb-atlas-mcp-dev",
        "pysae_ai_tools.install.mongodb_atlas_mcp_dev",
        Mode.OPTIONAL,
        category=Category.MCP,
        description="MCP — MongoDB Atlas cluster admin (dev)",
    ),
    Tool(
        "mongodb-atlas-mcp-prod",
        "pysae_ai_tools.install.mongodb_atlas_mcp_prod",
        Mode.OPTIONAL,
        category=Category.MCP,
        description="MCP — MongoDB Atlas cluster admin (prod)",
    ),
    Tool(
        "mongodb-atlas-mcp-org",
        "pysae_ai_tools.install.mongodb_atlas_mcp_org",
        Mode.OPTIONAL,
        category=Category.MCP,
        default_selected=False,
        description="MCP — MongoDB Atlas organisation admin (opt-in)",
    ),
    # Tier 6 — outils embarqués (pas d'install locale, juste un groupage
    # d'env vars consommées par les sous-commandes Pysae).
    Tool(
        "slack-env",
        "pysae_ai_tools.install.slack",
        Mode.OPTIONAL,
        category=Category.EMBEDDED,
        description="Slack — env vars pour les commandes `pysae-ai-tools slack` (appels API directs)",
    ),
    Tool(
        "mcp-cleanup-hook",
        "pysae_ai_tools.install.mcp_cleanup_hook",
        Mode.OPTIONAL,
        category=Category.EMBEDDED,
        description="Hook SessionEnd qui kill les MCP serveurs orphelins (libère la RAM, Linux + macOS)",
    ),
    Tool(
        "pysae-env-shell",
        "pysae_ai_tools.install.shell_init",
        Mode.OPTIONAL,
        category=Category.EMBEDDED,
        description="`pysae-env` (activate/deactivate sans eval) dans tous les shells installés (+ shim .bat cmd.exe)",
    ),
    Tool(
        "usage-primer",
        "pysae_ai_tools.install.usage_primer",
        Mode.OPTIONAL,
        category=Category.EMBEDDED,
        default_selected=False,
        # Needs the `claude` binary to fire the priming request (see usage/prime.py).
        depends=("claude-code",),
        description="Amorçage auto des fenêtres 5H via cron (3 fenêtres sur les heures de travail au lieu de 2)",
    ),
    Tool(
        "usage-guard",
        "pysae_ai_tools.install.usage_guard",
        Mode.OPTIONAL,
        category=Category.EMBEDDED,
        default_selected=False,
        description="Notifications de conso 5H/hebdo + blocage des tool calls au seuil (hooks Claude Code)",
    ),
    Tool(
        "activity-tracker",
        "pysae_ai_tools.install.activity_tracker_hook",
        Mode.OPTIONAL,
        category=Category.EMBEDDED,
        default_selected=False,
        description="Suivi d'activité (hooks tracker PostToolUse + Stop, journalisés localement)",
    ),
)


TOOL_NAMES = [t.name for t in TOOLS]


def _find_tool(name: str) -> Tool | None:
    """Find a tool by name."""
    for t in TOOLS:
        if t.name == name:
            return t
    return None


# Display order for category sections — languages first (they bootstrap
# the rest), then CLIs, MCPs, plugins, embedded entries.
CATEGORY_ORDER: tuple[Category, ...] = (
    Category.LANGUAGE,
    Category.CLI,
    Category.MCP,
    Category.PLUGIN,
    Category.EMBEDDED,
)


def _tools_by_category(tools: tuple[Tool, ...] = TOOLS) -> dict[Category, list[Tool]]:
    """Group ``tools`` by category, preserving original order within each."""
    grouped: dict[Category, list[Tool]] = {c: [] for c in CATEGORY_ORDER}
    for t in tools:
        grouped.setdefault(t.category, []).append(t)
    return grouped
