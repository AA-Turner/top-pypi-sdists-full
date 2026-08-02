"""Centralised description and resolver chains for known env vars.

Each entry declares an ordered list of :class:`Resolver` strategies that
``pysae-ai-tools env resolve`` will try to obtain a value when the variable
is missing from the current environment. Resolvers are tried in order; the
first one producing a non-empty value wins.

Resolver kinds:

- :class:`UserSecretResolver` / :class:`SecretResolver` — read a key from an
  AWS Secrets Manager secret **in-process** via
  :mod:`pysae_ai_tools.env.secret_store`. ``UserSecretResolver`` targets the
  caller's per-user secret ``iam/<user>[/<env>]/<theme>``; ``SecretResolver``
  targets an explicit secret id. Both share the parallel preload cache, so a
  secret referenced by several vars is fetched once. Prefer these over a
  ``CommandResolver`` for anything backed by AWS Secrets Manager.
- :class:`CommandResolver` — runs a shell command (timeout 15s) whose stdout
  becomes the value. Reserved for genuine subprocess flows (e.g. Slack OAuth).
- :class:`ManualResolver` — terminal fallback that never produces a value. Its
  ``instructions`` string is shown to the user when every automatic resolver
  has failed (and by interactive prompts as a hint). Place it last.

Each :class:`CommandResolver` carries its own ``label`` (shown in the
"✓ $VAR resolved …" notice).
"""

import os
import shutil
import subprocess
from abc import ABC, abstractmethod
from dataclasses import dataclass

import typer

from . import trace


class Resolver(ABC):
    """One strategy for obtaining an env var's value.

    Every kind is self-describing and self-executing: :meth:`run` obtains the
    value (or ``None``), :attr:`default_label` is the trace/notice text when no
    explicit ``label`` was given, :attr:`source_description` is the value-free
    "where it reads from" line for ``env list``, and :meth:`secret_id` names the
    AWS secret the run would touch (for the parallel preload) or ``None``. Adding
    a new kind therefore means writing one dataclass here — no ``match`` in
    ``resolve.py`` / ``list_cmd.py`` to extend.
    """

    @abstractmethod
    def run(self, var: str) -> str | None:
        """Try to resolve ``var``; on success set ``os.environ[var]`` and return the value."""

    @property
    @abstractmethod
    def default_label(self) -> str:
        """Trace/notice text used when this resolver carries no explicit ``label``."""

    @property
    @abstractmethod
    def source_description(self) -> str:
        """One-line, value-free description of where this resolver reads from (``env list``)."""

    @property
    def display_label(self) -> str:
        """The explicit ``label`` when set, else :attr:`default_label`."""
        return getattr(self, "label", "") or self.default_label

    def secret_id(self) -> str | None:
        """AWS secret id this resolver would fetch, or ``None`` when it fetches none.

        May raise :class:`secret_store.SecretError` when the id cannot be
        computed yet (e.g. no AWS username); callers warming the preload cache
        treat that as "skip".
        """
        return None


@dataclass(frozen=True)
class CommandResolver(Resolver):
    """Shell command resolver — stdout becomes the value.

    ``timeout`` overrides the default 15 s wait when the command is expected
    to take longer (e.g. interactive OAuth flows).

    ``depends_on`` lists env vars that must be resolved before the command
    runs. Each dependency is looked up through :func:`try_auto_resolve` and
    injected into the subprocess environment via ``os.environ``.

    ``requires_tty`` marks commands that fundamentally need a human (browser
    OAuth, paste-a-secret prompts). When set, the resolver is skipped
    cleanly in non-interactive runs (CI, ``--set`` mode, no TTY) instead
    of being launched and timing out.
    """

    command: str
    label: str
    timeout: int = 15
    depends_on: tuple[str, ...] = ()
    requires_tty: bool = False

    @property
    def default_label(self) -> str:
        return "automatically"

    @property
    def source_description(self) -> str:
        return self.label or f"shell command ({self.command.split()[0]})"

    def run(self, var: str) -> str | None:
        from .resolve import try_auto_resolve

        label = trace.expand_label(self.display_label)
        if self.requires_tty and trace.is_non_interactive():
            trace.pending(label)
            trace.skipped(label, "non-interactive run — command needs a TTY")
            return None

        for dep in self.depends_on:
            if not os.environ.get(dep):
                try_auto_resolve(dep)

        if self.requires_tty:
            return self._run_interactive(var, label)

        trace.pending(label)
        try:
            result = subprocess.run(
                self.command.split(),
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=self.timeout,
            )
        except subprocess.TimeoutExpired:
            trace.failure(label, f"timed out after {self.timeout}s")
            return None
        except FileNotFoundError:
            trace.failure(label, f"command not found: {self.command.split()[0]}")
            return None
        if result.returncode != 0:
            stderr = (result.stderr or "").strip().splitlines()
            detail = stderr[-1] if stderr else f"exit code {result.returncode}"
            trace.failure(label, detail)
            return None
        if not (result.stdout or "").strip():
            trace.failure(label, "empty output")
            return None

        value = result.stdout.strip()
        os.environ[var] = value
        trace.success(label)
        return value

    def _run_interactive(self, var: str, label: str) -> str | None:
        """Run a ``requires_tty`` command, letting its stderr reach the terminal.

        Interactive resolvers (browser OAuth via ``slack get-token``) print their
        guidance — the authorize URL, "opening the browser…", "waiting for the
        callback…" — on **stderr**, and emit the resolved value on **stdout**.
        Capturing both (as the batch path does) hides the guidance, so the user is
        left staring at a spinner while a hidden browser flow blocks for minutes.

        So here we pipe stdout only (to read the value) and let stderr through to
        the terminal, and we skip the spinner — the subprocess owns the terminal
        for the duration of the flow.
        """
        trace.emit(
            f"    ↻ {label} — flow interactif, suivez les instructions ci-dessous…",
            color=typer.colors.YELLOW,
        )
        try:
            result = subprocess.run(
                self.command.split(),
                stdout=subprocess.PIPE,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=self.timeout,
            )
        except subprocess.TimeoutExpired:
            trace.failure(label, f"timed out after {self.timeout}s")
            return None
        except FileNotFoundError:
            trace.failure(label, f"command not found: {self.command.split()[0]}")
            return None
        if result.returncode != 0:
            trace.failure(label, f"exit code {result.returncode}")
            return None
        value = (result.stdout or "").strip()
        if not value:
            trace.failure(label, "empty output")
            return None
        os.environ[var] = value
        trace.success(label)
        return value


@dataclass(frozen=True)
class ManualResolver(Resolver):
    """Terminal resolver — informational only, surfaces manual instructions."""

    instructions: str

    @property
    def default_label(self) -> str:
        return "saisie manuelle"

    @property
    def source_description(self) -> str:
        return "manual step"

    def run(self, var: str) -> str | None:
        """Never produces a value — its instructions are surfaced elsewhere."""
        return None


@dataclass(frozen=True)
class LiteralResolver(Resolver):
    """Static-value resolver — always returns ``value``.

    Useful for sensible defaults (e.g. ``AWS_PROFILE=pysae``) so the rest
    of the chain can rely on the variable being set.
    """

    value: str
    label: str = ""  # auto-generated as ``default '{value}'`` when empty

    @property
    def default_label(self) -> str:
        return f"default {self.value!r}"

    @property
    def source_description(self) -> str:
        return f"default {self.value!r}"

    def run(self, var: str) -> str | None:
        label = self.display_label
        trace.pending(label)
        os.environ[var] = self.value
        trace.success(label)
        return self.value


@dataclass(frozen=True)
class GlabAuthResolver(Resolver):
    """Read the GitLab token from ``glab`` and prompt ``glab auth login`` on miss.

    Tries ``glab config get token --host <host>`` first. When no token is
    on file *and* stdin is a TTY (and trace is not silenced), launches
    ``glab auth login --hostname <host>`` interactively so the user can
    complete the OAuth/token flow without leaving the install run, then
    re-reads the token. ``glab`` must be on PATH; a missing binary is
    reported as a clean failure and the resolver chain falls through.
    """

    host: str = "gitlab.com"
    label: str = ""  # "from glab CLI ({host})" when empty

    @property
    def default_label(self) -> str:
        return f"from glab CLI ({self.host})"

    @property
    def source_description(self) -> str:
        return f"glab CLI ({self.host})"

    def _get_token(self) -> str | None:
        """Read the stored token for ``host`` via ``glab config get``.

        Returns ``None`` when glab is missing, the call fails, or the token
        is empty.
        """
        from ..common.glab.runner import run_glab

        res = run_glab("config", "get", "token", "--host", self.host, timeout=10)
        if not res.ok:
            return None
        return res.stdout or None

    def run(self, var: str) -> str | None:
        label = self.display_label
        trace.pending(label)

        token = self._get_token()
        if token:
            os.environ[var] = token
            trace.success(label)
            return token

        if trace.is_non_interactive():
            trace.skipped(label, "non-interactive run — `glab auth login` needs a TTY")
            return None

        trace.failure(label, "not authenticated — launching `glab auth login`")
        if shutil.which("glab") is None:
            trace.failure(label, "glab not installed")
            return None

        # Pre-answer every glab prompt that has a sensible default — host, git
        # protocol, API protocol, container-registry domains. The only prompts
        # that remain are those without a CLI flag in glab (notably the
        # Token/Web login choice and the post-auth "Authenticate Git" yes/no).
        auth_cmd = [
            "glab",
            "auth",
            "login",
            "--hostname",
            self.host,
            "--git-protocol",
            "https",
            "--api-protocol",
            "https",
            "--container-registry-domains",
            "gitlab.com,gitlab.com:443,registry.gitlab.com",
        ]
        try:
            rc = subprocess.call(auth_cmd)
        except OSError as exc:
            trace.failure(f"glab auth login ({self.host})", str(exc))
            return None
        if rc != 0:
            trace.failure(f"glab auth login ({self.host})", f"exit code {rc}")
            return None

        token = self._get_token()
        if not token:
            trace.failure(label, "token still empty after auth login")
            return None
        os.environ[var] = token
        trace.success(f"after `glab auth login --hostname {self.host}`")
        return token


@dataclass(frozen=True)
class AwsConfigResolver(Resolver):
    """Read AWS CLI config (``~/.aws/credentials`` / ``~/.aws/config``).

    Reads ``aws configure get <aws_key>`` against the user's default profile
    (this tool does not manage ``AWS_PROFILE``). When ``interactive_prompt``
    is set and stdin is a TTY, the resolver prompts the user on a miss and
    persists the entered values via ``aws configure set`` so the next call
    hits the standard AWS files.
    """

    aws_key: str  # field in AWS files (e.g. "aws_access_key_id")
    interactive_prompt: str = ""  # "" | "credentials"
    label: str = ""

    @property
    def default_label(self) -> str:
        return "from AWS config (profil par défaut)"

    @property
    def source_description(self) -> str:
        return f"AWS config ({self.aws_key})"

    def run(self, var: str) -> str | None:
        from . import aws

        label = self.display_label
        trace.pending(label)

        value = aws.aws_configure_get(self.aws_key)
        if value:
            os.environ[var] = value
            trace.success(label)
            return value

        trace.failure(label, "absent du fichier AWS")

        if self.interactive_prompt == "credentials" and aws.stdin_is_tty() and not trace.is_silent():
            if aws.prompt_aws_credentials():
                # Re-read the requested field from the freshly written profile.
                entered = aws.aws_configure_get(self.aws_key)
                if entered:
                    os.environ[var] = entered
                    trace.success("saisi par l'utilisateur, écrit dans ~/.aws/credentials")
                    return entered

        return None


@dataclass(frozen=True)
class UserSecretResolver(Resolver):
    """Read a key from the caller's per-user secret ``iam/<user>[/<env>]/<theme>``.

    Resolved **in-process** via :mod:`pysae_ai_tools.env.secret_store` (no CLI
    subprocess), so the value benefits from the parallel preload cache and a
    secret shared by several vars is fetched once. Prefer this over a
    ``CommandResolver`` invoking ``secrets read-user``.
    """

    theme: str
    key: str
    env: str | None = None
    label: str = ""  # "from AWS Secrets Manager (iam/<user>[/env]/theme)" when empty

    @property
    def _secret_path(self) -> str:
        return f"iam/<user>/{self.env}/{self.theme}" if self.env else f"iam/<user>/{self.theme}"

    @property
    def default_label(self) -> str:
        return f"from AWS Secrets Manager ({self._secret_path})"

    @property
    def source_description(self) -> str:
        return f"AWS Secrets Manager {self._secret_path} ({self.key})"

    def secret_id(self) -> str | None:
        from . import secret_store

        return secret_store.user_secret_id(self.theme, self.env)

    def run(self, var: str) -> str | None:
        from . import secret_store

        label = trace.expand_label(self.display_label)
        trace.pending(label)
        try:
            secret_id = secret_store.user_secret_id(self.theme, self.env)
            value = secret_store.get_key(secret_id, self.key)
        except secret_store.SecretError as exc:
            trace.failure(label, str(exc))
            return None
        os.environ[var] = value
        trace.success(label)
        return value


@dataclass(frozen=True)
class SecretResolver(Resolver):
    """Read a key from an explicit AWS secret id, in-process and cached."""

    secret_id_value: str
    key: str
    label: str = ""  # "from AWS Secrets Manager (<secret_id>)" when empty

    @property
    def default_label(self) -> str:
        return f"from AWS Secrets Manager ({self.secret_id_value})"

    @property
    def source_description(self) -> str:
        return f"AWS Secrets Manager {self.secret_id_value} ({self.key})"

    def secret_id(self) -> str | None:
        return self.secret_id_value

    def run(self, var: str) -> str | None:
        from . import secret_store

        label = self.display_label
        trace.pending(label)
        try:
            value = secret_store.get_key(self.secret_id_value, self.key)
        except secret_store.SecretError as exc:
            trace.failure(label, str(exc))
            return None
        os.environ[var] = value
        trace.success(label)
        return value


# Slack user-token scopes requested via the OAuth v2 flow — see the
# ``SLACK_USER_TOKEN`` resolver below. Kept as a tuple so the source of
# truth is a real Python list, not a stringly-typed sub-argument of a
# shell command.
SLACK_USER_SCOPES: tuple[str, ...] = (
    "channels:history",
    "groups:history",
    "im:history",
    "im:read",
    "im:write",
    "mpim:history",
    "chat:write",
    "users:read",
    "users:read.email",
)


@dataclass(frozen=True)
class EnvVarSpec:
    """Human description + ordered resolver chain for an env var.

    When ``cache=True``, a successful resolution is persisted to
    ``~/.config/pysae-ai-tools/env-cache.json`` (0600 perms) and read back
    on subsequent calls, skipping the resolver chain. Opt-in only — reserve
    for values that are expensive to re-obtain and whose source of truth
    is not already on disk (e.g. interactive OAuth tokens). Never enable
    caching for values that can be rotated upstream (AWS secrets, MCP
    config) — you'd hide the rotation from the caller.

    ``environment`` scopes this variable to ``"dev"``, ``"prod"``, or ``None``
    (environment-agnostic — available in every environment). ``resolved_name``
    is the common name it goes by (e.g. ``MONGO_URI_DEV`` → ``MONGO_URI``);
    ``None`` means the variable's own name. Together they let an environment-aware
    consumer expose ``MONGO_URI_DEV`` as ``MONGO_URI`` when resolving ``dev``.
    """

    description: str
    resolvers: tuple[Resolver, ...] = ()
    cache: bool = False
    environment: str | None = None
    resolved_name: str | None = None


ENV_CONFIG: dict[str, EnvVarSpec] = {
    "AWS_DEFAULT_REGION": EnvVarSpec(
        description="Région AWS (lue dans ~/.aws/config, défaut Pysae : eu-west-3)",
        resolvers=(
            AwsConfigResolver(aws_key="region", label="from ~/.aws/config"),
            LiteralResolver(value="eu-west-3", label="default 'eu-west-3' (Paris)"),
        ),
    ),
    "AWS_ACCESS_KEY_ID": EnvVarSpec(
        description="AWS Access Key ID (lu / écrit dans ~/.aws/credentials)",
        resolvers=(
            AwsConfigResolver(
                aws_key="aws_access_key_id",
                interactive_prompt="credentials",
                label="from ~/.aws/credentials",
            ),
            ManualResolver(
                instructions=(
                    "Configure d'abord avec `aws configure` "
                    "(ou `pysae-ai-tools env resolve AWS_ACCESS_KEY_ID` en interactif)."
                ),
            ),
        ),
    ),
    "AWS_SECRET_ACCESS_KEY": EnvVarSpec(
        description="AWS Secret Access Key (lu / écrit dans ~/.aws/credentials)",
        resolvers=(
            AwsConfigResolver(
                aws_key="aws_secret_access_key",
                interactive_prompt="credentials",
                label="from ~/.aws/credentials",
            ),
            ManualResolver(
                instructions=(
                    "Configure d'abord avec `aws configure` "
                    "(ou `pysae-ai-tools env resolve AWS_ACCESS_KEY_ID` en interactif "
                    "— la commande prompt à la fois la clé et le secret)."
                ),
            ),
        ),
    ),
    "DD_API_KEY": EnvVarSpec(
        description="Datadog API Key",
        resolvers=(
            UserSecretResolver(
                theme="datadog",
                key="datadog-api-key",
                label="from AWS Secrets Manager (iam/<user>/datadog)",
            ),
            ManualResolver(instructions="Datadog → Organization Settings → API Keys → New Key"),
        ),
    ),
    "DD_APP_KEY": EnvVarSpec(
        description="Datadog Application Key",
        resolvers=(
            UserSecretResolver(
                theme="datadog",
                key="datadog-app-key",
                label="from AWS Secrets Manager (iam/<user>/datadog)",
            ),
            ManualResolver(instructions="Datadog → Organization Settings → Application Keys → New Key"),
        ),
    ),
    "AIRTABLE_API_KEY": EnvVarSpec(
        description="Airtable personal access token (Customer Service base, read scope)",
        resolvers=(
            UserSecretResolver(
                theme="airtable",
                key="airtable-api-key",
                label="from AWS Secrets Manager (iam/<user>/airtable)",
            ),
            ManualResolver(instructions="https://airtable.com/create/tokens → scope data.records:read on the CS base"),
        ),
    ),
    "ANTHROPIC_ADMIN_API_KEY": EnvVarSpec(
        description="Anthropic Admin API key (organization usage & cost reports)",
        resolvers=(
            UserSecretResolver(
                theme="anthropic",
                key="anthropic-admin-api-key",
                label="from AWS Secrets Manager (iam/<user>/anthropic)",
            ),
            ManualResolver(
                instructions="console.anthropic.com → Settings → API Keys → Admin Keys (admin role required)"
            ),
        ),
    ),
    "GITLAB_PERSONAL_ACCESS_TOKEN": EnvVarSpec(
        description="GitLab Personal Access Token",
        resolvers=(
            GlabAuthResolver(host="gitlab.com"),
            ManualResolver(
                instructions=(
                    "run `glab auth login --hostname gitlab.com` first "
                    "(or GitLab → Preferences → Access Tokens → New Token with api scope)"
                ),
            ),
        ),
    ),
    "POSTMAN_API_KEY": EnvVarSpec(
        description="Postman API Key",
        resolvers=(
            UserSecretResolver(
                theme="postman",
                key="postman-api-key",
                label="from AWS Secrets Manager (iam/<user>/postman)",
            ),
            ManualResolver(instructions="Postman → Settings → API Keys → Generate API Key"),
        ),
    ),
    "MONGO_URI_DEV": EnvVarSpec(
        description="URI de connexion à MongoDB (dev)",
        resolvers=(
            UserSecretResolver(
                theme="mongo",
                key="api-mongo-uri",
                env="dev",
                label="from AWS Secrets Manager (iam/<user>/dev/mongo)",
            ),
        ),
        environment="dev",
        resolved_name="MONGO_URI",
    ),
    "MONGO_URI_PROD": EnvVarSpec(
        description="URI de connexion à MongoDB (prod)",
        resolvers=(
            UserSecretResolver(
                theme="mongo",
                key="api-mongo-uri",
                env="prod",
                label="from AWS Secrets Manager (iam/<user>/prod/mongo)",
            ),
        ),
        environment="prod",
        resolved_name="MONGO_URI",
    ),
    "MONGODB_ATLAS_PUBLIC_API_KEY_DEV": EnvVarSpec(
        description="Clé publique d'API MongoDB Atlas (dev)",
        resolvers=(
            UserSecretResolver(
                theme="atlas",
                key="mongodb-atlas-public-key",
                env="dev",
                label="from AWS Secrets Manager (iam/<user>/dev/atlas)",
            ),
        ),
        environment="dev",
        resolved_name="ATLAS_PUBLIC_KEY",
    ),
    "MONGODB_ATLAS_PRIVATE_API_KEY_DEV": EnvVarSpec(
        description="Clé privée d'API MongoDB Atlas (dev)",
        resolvers=(
            UserSecretResolver(
                theme="atlas",
                key="mongodb-atlas-private-key",
                env="dev",
                label="from AWS Secrets Manager (iam/<user>/dev/atlas)",
            ),
        ),
        environment="dev",
        resolved_name="ATLAS_PRIVATE_KEY",
    ),
    "MONGODB_ATLAS_PUBLIC_API_KEY_PROD": EnvVarSpec(
        description="Clé publique d'API MongoDB Atlas (prod)",
        resolvers=(
            UserSecretResolver(
                theme="atlas",
                key="mongodb-atlas-public-key",
                env="prod",
                label="from AWS Secrets Manager (iam/<user>/prod/atlas)",
            ),
        ),
        environment="prod",
        resolved_name="ATLAS_PUBLIC_KEY",
    ),
    "MONGODB_ATLAS_PRIVATE_API_KEY_PROD": EnvVarSpec(
        description="Clé privée d'API MongoDB Atlas (prod)",
        resolvers=(
            UserSecretResolver(
                theme="atlas",
                key="mongodb-atlas-private-key",
                env="prod",
                label="from AWS Secrets Manager (iam/<user>/prod/atlas)",
            ),
        ),
        environment="prod",
        resolved_name="ATLAS_PRIVATE_KEY",
    ),
    "MONGODB_ATLAS_PROJECT_ID_DEV": EnvVarSpec(
        description="ID du projet MongoDB Atlas (dev) — écrit dans le profil atlas CLI pour éviter --projectId",
        resolvers=(
            UserSecretResolver(
                theme="atlas",
                key="mongodb-atlas-pysae-project-id",
                env="dev",
                label="from AWS Secrets Manager (iam/<user>/dev/atlas)",
            ),
        ),
        environment="dev",
        resolved_name="MONGODB_ATLAS_PROJECT_ID",
    ),
    "MONGODB_ATLAS_PROJECT_ID_PROD": EnvVarSpec(
        description="ID du projet MongoDB Atlas (prod) — écrit dans le profil atlas CLI pour éviter --projectId",
        resolvers=(
            UserSecretResolver(
                theme="atlas",
                key="mongodb-atlas-pysae-project-id",
                env="prod",
                label="from AWS Secrets Manager (iam/<user>/prod/atlas)",
            ),
        ),
        environment="prod",
        resolved_name="MONGODB_ATLAS_PROJECT_ID",
    ),
    "MONGODB_ATLAS_ORG_PUBLIC_API_KEY": EnvVarSpec(
        description="Clé publique d'API MongoDB Atlas au niveau organisation (couvre tous les projets)",
        resolvers=(
            UserSecretResolver(
                theme="atlas",
                key="mongodb-atlas-org-public-key",
                label="from AWS Secrets Manager (iam/<user>/atlas)",
            ),
        ),
        resolved_name="ATLAS_PUBLIC_KEY",
    ),
    "MONGODB_ATLAS_ORG_PRIVATE_API_KEY": EnvVarSpec(
        description="Clé privée d'API MongoDB Atlas au niveau organisation (couvre tous les projets)",
        resolvers=(
            UserSecretResolver(
                theme="atlas",
                key="mongodb-atlas-org-private-key",
                label="from AWS Secrets Manager (iam/<user>/atlas)",
            ),
        ),
        resolved_name="ATLAS_PRIVATE_KEY",
    ),
    "MONGODB_ATLAS_ORG_ID": EnvVarSpec(
        description="ID de l'organisation MongoDB Atlas — écrit dans le profil atlas CLI pour éviter --orgId",
        resolvers=(
            UserSecretResolver(
                theme="atlas",
                key="mongodb-atlas-org-id",
                label="from AWS Secrets Manager (iam/<user>/atlas)",
            ),
        ),
    ),
    "ARGOCD_AUTH_TOKEN_DEV": EnvVarSpec(
        description="Token argocd (dev)",
        resolvers=(
            UserSecretResolver(
                theme="argocd",
                key="argocd-auth-token",
                env="dev",
                label="from AWS Secrets Manager (iam/<user>/dev/argocd)",
            ),
            ManualResolver(
                instructions=(
                    "Génère un token sur le serveur dev avec "
                    "`argocd account generate-token --account <ton-compte>` "
                    "(le résultat sera mis en cache local — auto-réutilisé tant qu'AWS est inaccessible)."
                ),
            ),
        ),
        environment="dev",
        resolved_name="ARGOCD_AUTH_TOKEN",
    ),
    "ARGOCD_AUTH_TOKEN_PROD": EnvVarSpec(
        description="Token argocd (prod)",
        resolvers=(
            UserSecretResolver(
                theme="argocd",
                key="argocd-auth-token",
                env="prod",
                label="from AWS Secrets Manager (iam/<user>/prod/argocd)",
            ),
            ManualResolver(
                instructions=(
                    "Génère un token sur le serveur prod avec "
                    "`argocd account generate-token --account <ton-compte>` "
                    "(le résultat sera mis en cache local — auto-réutilisé tant qu'AWS est inaccessible)."
                ),
            ),
        ),
        environment="prod",
        resolved_name="ARGOCD_AUTH_TOKEN",
    ),
    "ARGOCD_SERVER_DEV": EnvVarSpec(
        description="Serveur ArgoCD (dev)",
        resolvers=(
            UserSecretResolver(
                theme="argocd",
                key="argocd-server",
                env="dev",
                label="from AWS Secrets Manager (iam/<user>/dev/argocd)",
            ),
        ),
        environment="dev",
        resolved_name="ARGOCD_SERVER",
    ),
    "ARGOCD_SERVER_PROD": EnvVarSpec(
        description="Serveur ArgoCD (prod)",
        resolvers=(
            UserSecretResolver(
                theme="argocd",
                key="argocd-server",
                env="prod",
                label="from AWS Secrets Manager (iam/<user>/prod/argocd)",
            ),
        ),
        environment="prod",
        resolved_name="ARGOCD_SERVER",
    ),
    "SLACK_USER_TOKEN": EnvVarSpec(
        description="Slack user token (OAuth v2, interactive browser flow)",
        resolvers=(
            CommandResolver(
                command=f"pysae-ai-tools slack get-token --user-only --user-scopes {','.join(SLACK_USER_SCOPES)}",
                label="from Slack OAuth (browser)",
                timeout=300,
                depends_on=("SLACK_CLIENT_ID", "SLACK_CLIENT_SECRET"),
                requires_tty=True,
            ),
        ),
        cache=True,
    ),
    "SLACK_BOT_TOKEN": EnvVarSpec(
        description="Slack Bot token",
        resolvers=(
            SecretResolver(
                secret_id_value="ai-tools/slack",
                key="slack-app-token",
                label="from AWS Secrets Manager (ai-tools/slack)",
            ),
            CommandResolver(
                command="pysae-ai-tools slack get-token",
                label="from Slack OAuth (browser)",
                timeout=300,
                depends_on=("SLACK_CLIENT_ID", "SLACK_CLIENT_SECRET"),
                requires_tty=True,
            ),
            ManualResolver(
                instructions="https://api.slack.com/apps/A0B05GC22TS → OAuth & Permissions",
            ),
        ),
    ),
    "SLACK_CLIENT_ID": EnvVarSpec(
        description="Slack App Client ID",
        resolvers=(
            SecretResolver(
                secret_id_value="ai-tools/slack",
                key="slack-client-id",
                label="from AWS Secrets Manager (ai-tools/slack)",
            ),
            ManualResolver(
                instructions="https://api.slack.com/apps/A0B05GC22TS → Basic Information → App Credentials",
            ),
        ),
    ),
    "SLACK_CLIENT_SECRET": EnvVarSpec(
        description="Slack App Client Secret",
        resolvers=(
            SecretResolver(
                secret_id_value="ai-tools/slack",
                key="slack-client-secret",
                label="from AWS Secrets Manager (ai-tools/slack)",
            ),
            ManualResolver(
                instructions="https://api.slack.com/apps/A0B05GC22TS → Basic Information → App Credentials",
            ),
        ),
    ),
    "AUTH0_MGMT_RO_CLIENT_ID": EnvVarSpec(
        description="Auth0 read-only Management M2M client id (pysae-tooling-auth0-ro)",
        resolvers=(
            SecretResolver(
                secret_id_value="pysae/tooling/auth0-readonly",
                key="client-id",
                label="from AWS Secrets Manager (pysae/tooling/auth0-readonly)",
            ),
        ),
    ),
    "AUTH0_MGMT_RO_CLIENT_SECRET": EnvVarSpec(
        description="Auth0 read-only Management M2M client secret (pysae-tooling-auth0-ro)",
        resolvers=(
            SecretResolver(
                secret_id_value="pysae/tooling/auth0-readonly",
                key="client-secret",
                label="from AWS Secrets Manager (pysae/tooling/auth0-readonly)",
            ),
        ),
    ),
    "AUTH0_MGMT_RO_TOKEN": EnvVarSpec(
        # No `cache=True`: the minted token expires (~24h) and the env cache has
        # no TTL — caching would re-serve a stale token and cause 401s. Minting
        # is a single ~200ms client_credentials POST, so we mint on demand.
        description="Auth0 read-only Management API token (minted via client_credentials)",
        resolvers=(
            CommandResolver(
                command="pysae-ai-tools auth0 token --raw",
                label="from Auth0 client_credentials",
                timeout=30,
                depends_on=("AUTH0_MGMT_RO_CLIENT_ID", "AUTH0_MGMT_RO_CLIENT_SECRET"),
            ),
        ),
    ),
    "FIGMA_TOKEN": EnvVarSpec(
        # A Figma PAT reads every file its holder can see, so it is shared and
        # read-only by construction. Rotated by hand in the Figma UI: no provider
        # can mint one, hence a plain secret rather than a CommandResolver.
        description="Figma personal access token (read scopes) for the comment-triggered agent",
        resolvers=(
            SecretResolver(
                secret_id_value="pysae/figma/tooling",
                key="pat",
                label="from AWS Secrets Manager (pysae/figma/tooling)",
            ),
        ),
    ),
    "FIGMA_WEBHOOK_PASSCODE": EnvVarSpec(
        # Shared secret echoed by Figma in the body of every webhook call. Figma
        # sends no HMAC signature, so this passcode is the only authentication.
        description="Shared passcode validating incoming Figma webhook calls",
        resolvers=(
            SecretResolver(
                secret_id_value="pysae/figma/tooling",
                key="webhook_passcode",
                label="from AWS Secrets Manager (pysae/figma/tooling)",
            ),
        ),
    ),
}


def get_manual_instructions(var: str) -> str | None:
    """Return the ManualResolver instructions for `var`, if any."""
    spec = ENV_CONFIG.get(var)
    if spec is None:
        return None
    for resolver in spec.resolvers:
        if isinstance(resolver, ManualResolver):
            return resolver.instructions
    return None
