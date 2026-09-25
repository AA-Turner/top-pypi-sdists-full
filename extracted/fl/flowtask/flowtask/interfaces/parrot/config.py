"""Shared YAML configuration for parrot-backed FlowTask components (FEAT-557).

This module owns the four configuration blocks that every component invoking an
ai-parrot agent needs, so each new component stops re-implementing them:

``agent_class``
    Dotted path of the ``BasicAgent`` subclass to instantiate. Plugin agents
    living in ``PLUGINS_DIR/agents`` are importable as ``agents.<module>``.
``llm_config``
    Provider/model plus the tuning kwargs parrot resolves in ``Chatbot.__init__``
    (they must reach the *constructor*; setting them afterwards has no effect),
    and the two podcast-only models.
``podcast``
    Agent attributes (speakers, contexts, lengths) and the kwargs of
    ``BasicAgent.speech_report()``, including where the audio and script files
    are written — parrot defaults those to its own ``STATIC_DIR``, which is not
    where a task wants them.
``notification``
    Delivery of the agent's results through the agent's own
    ``NotificationMixin.send_notification()`` over email, Telegram or MS Teams.

The mixin is deliberately framework-agnostic: it never touches ``FlowComponent``
and performs no I/O beyond reading card templates and creating output
directories, so it can be unit-tested without a task, a task store or an LLM.
"""
from __future__ import annotations

import copy
import importlib
import json
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Optional, Union

from pydantic import BaseModel, ConfigDict, Field, ValidationError, model_validator
from typing_extensions import Literal

from notify.models import CardAction, Chat, TeamsChannel, TeamsSection, TeamsWebhook
from parrot.bots.agent import BasicAgent

from ...exceptions import ComponentError, ConfigError


class SafeDict(dict):
    """``format_map`` helper that leaves unknown placeholders untouched.

    Defined here rather than imported from ``flowtask.utils`` because that one
    lives in a compiled Cython module (``flowtask.types.typedefs``) which the
    test suite stubs out; ``ProductReportBot`` keeps a local copy for the same
    reason. Rendering a notification must never explode over a column the row
    happens not to carry.
    """

    def __missing__(self, key: str) -> str:
        return "{" + key + "}"


#: Attributes of a ``BasicAgent`` instance that the ``podcast:`` block may set.
PODCAST_AGENT_ATTRIBUTES: tuple = (
    "speakers",
    "speech_context",
    "speech_system_prompt",
    "speech_length",
    "num_speakers",
)

#: ``llm_config`` keys consumed by ``speech_report()`` rather than the constructor.
PODCAST_MODEL_KEYS: tuple = ("podcast_script_model", "podcast_tts_model")

#: Default sub-directories under the component base directory.
DEFAULT_PODCAST_SUBDIR: str = "outputs/podcasts"
DEFAULT_SCRIPT_SUBDIR: str = "outputs/generated_scripts"


# --------------------------------------------------------------------------- #
#  Configuration models
# --------------------------------------------------------------------------- #
class SpeakerConfig(BaseModel):
    """One fictional speaker of the generated conversation."""

    name: str
    role: Literal["interviewer", "interviewee"]
    characteristic: str
    gender: Literal["female", "male", "neutral"] = "neutral"


class PodcastConfig(BaseModel):
    """The ``podcast:`` block."""

    model_config = ConfigDict(extra="forbid")

    speakers: Optional[Dict[str, SpeakerConfig]] = None
    speech_context: Optional[str] = None
    speech_system_prompt: Optional[str] = None
    speech_length: Optional[int] = Field(default=None, ge=1)
    num_speakers: Optional[int] = Field(default=None, ge=1, le=2)
    max_lines: Optional[int] = Field(default=None, ge=1)
    instructions: Optional[str] = None
    output_directory: Optional[str] = None
    script_directory: Optional[str] = None


class AgentLLMConfig(BaseModel):
    """The ``llm_config:`` block. Unknown keys are forwarded to the constructor."""

    model_config = ConfigDict(extra="allow")

    llm: str = "google"
    model: Optional[str] = None
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None
    top_p: Optional[float] = None
    top_k: Optional[int] = None
    podcast_script_model: Optional[str] = None
    podcast_tts_model: Optional[str] = None


class TeamsChannelRecipient(BaseModel):
    """A Teams channel addressed through the Graph API."""

    type: Literal["channel"]
    name: str
    team_id: str
    channel_id: str


class TeamsWebhookRecipient(BaseModel):
    """A Teams incoming webhook."""

    type: Literal["webhook"]
    uri: str


#: Keys `TeamsCard.addSection()` / `addAction()` accept — anything else is a
#: TypeError at send time, which `send_notification` would swallow into an error
#: outcome. Validating here turns that into a ConfigError at parse time.
#: `notify.models` are `datamodel` classes, not pydantic — they expose
#: `__fields__`, not `model_fields`.
TEAMS_SECTION_KEYS: frozenset = frozenset(TeamsSection.__fields__)
TEAMS_ACTION_KEYS: frozenset = frozenset(CardAction.__fields__)


class TeamsCardConfig(BaseModel):
    """An Adaptive Card, declared inline or loaded from ``card_template``.

    This is parrot's card dialect (`sections` with `activityTitle`/`text`/`facts`,
    `actions` with `type`/`title`/`url`/`data`), because delivery goes through
    ``NotificationMixin.build_teams_card``. It is NOT the dialect
    ``SendNotify`` accepts (`facts` and `body` at the card level, facts shaped
    ``{title, value}``) — see ``flowtask/components/SendNotify/component.py:170``.
    Copying a card spec between the two components does not work, so the
    validator below rejects the wrong dialect explicitly.
    """

    model_config = ConfigDict(extra="forbid")

    title: str
    text: str = ""
    summary: Optional[str] = None
    sections: Optional[List[Dict[str, Any]]] = None
    actions: Optional[List[Dict[str, Any]]] = None
    version: str = "1.5"

    @model_validator(mode="after")
    def _check_card_dialect(self) -> "TeamsCardConfig":
        """Reject section/action keys `notify` would raise a TypeError over."""
        for index, section in enumerate(self.sections or []):
            unknown = set(section) - TEAMS_SECTION_KEYS
            if unknown:
                raise ValueError(
                    f"sections[{index}] has unsupported key(s) {sorted(unknown)}; "
                    f"allowed: {sorted(TEAMS_SECTION_KEYS)}. Facts are declared "
                    "inside a section as facts: [{name, value}]"
                )
        for index, action in enumerate(self.actions or []):
            unknown = set(action) - TEAMS_ACTION_KEYS
            if unknown:
                raise ValueError(
                    f"actions[{index}] has unsupported key(s) {sorted(unknown)}; "
                    f"allowed: {sorted(TEAMS_ACTION_KEYS)}"
                )
            if not action.get("title"):
                raise ValueError(f"actions[{index}] requires a 'title'")
            if not action.get("type"):
                raise ValueError(f"actions[{index}] requires a 'type', e.g. Action.OpenUrl")
        return self


class NotificationChannel(BaseModel):
    """One delivery channel of the ``notification.channels`` list."""

    model_config = ConfigDict(extra="forbid")

    provider: Literal["email", "telegram", "teams"]
    recipients: Union[
        str,
        int,
        TeamsChannelRecipient,
        TeamsWebhookRecipient,
        List[Union[str, int, TeamsChannelRecipient, TeamsWebhookRecipient]],
    ]
    message: Optional[str] = None
    subject: Optional[str] = None
    template: Optional[str] = None
    disable_notification: Optional[bool] = None
    provider_options: Optional[Dict[str, Any]] = None
    card: Optional[TeamsCardConfig] = None
    card_template: Optional[str] = None
    attach_columns: List[str] = Field(default_factory=list)
    with_attachments: bool = True
    extra: Dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def _check_provider_keys(self) -> "NotificationChannel":
        """Reject keys the target provider cannot honour.

        ``send_notification`` silently ignores what it does not understand, so a
        misrouted key (a ``subject`` on Telegram, ``provider_options`` on email)
        would look configured and never take effect. Fail at parse time instead.
        """
        allowed = {
            "email": {"subject", "template"},
            "telegram": {"disable_notification", "provider_options"},
            "teams": {"card", "card_template"},
        }[self.provider]
        for key in ("subject", "template", "disable_notification", "provider_options", "card", "card_template"):
            if key in allowed:
                continue
            if getattr(self, key, None) is not None:
                raise ValueError(f"'{key}' is not supported by provider '{self.provider}'")
        if self.card is not None and self.card_template is not None:
            raise ValueError("'card' and 'card_template' are mutually exclusive")

        recipients = self.recipients if isinstance(self.recipients, list) else [self.recipients]
        if not recipients:
            raise ValueError("'recipients' cannot be empty")
        for recipient in recipients:
            is_teams_object = isinstance(recipient, (TeamsChannelRecipient, TeamsWebhookRecipient))
            if is_teams_object and self.provider != "teams":
                raise ValueError(
                    "channel/webhook recipients are only valid for provider "
                    f"'teams', not '{self.provider}'"
                )
            if self.provider == "teams" and isinstance(recipient, str) and "@" not in recipient:
                # parrot's _parse_recipients drops these silently — refuse them here.
                raise ValueError(
                    "teams recipients must be an e-mail address or a "
                    "{type: channel, ...} / {type: webhook, ...} object, "
                    f"got '{recipient}'"
                )
        return self


class NotificationConfig(BaseModel):
    """The ``notification:`` block.

    Not to be confused with the parrot dataclass of the same name
    (``parrot.notifications.NotificationConfig``), which is unrelated.
    """

    model_config = ConfigDict(extra="forbid")

    mode: Literal["per_row", "summary"] = "per_row"
    when: Literal["success", "error", "always"] = "success"
    fail_on_error: bool = False
    summary_max_rows: int = Field(default=20, ge=1)
    max_attachments: int = Field(default=10, ge=0)
    url_prefix: Optional[str] = None
    url_token: Optional[str] = None
    channels: List[NotificationChannel] = Field(..., min_length=1)


class NotificationReport(BaseModel):
    """Duck-typed ``report=`` argument for ``send_notification``.

    ``NotificationMixin._extract_message_content`` reads ``.output`` and
    ``.files`` off whatever is passed as ``report``; this is the smallest object
    that satisfies it.
    """

    output: str = ""
    files: List[str] = Field(default_factory=list)


class NotificationOutcome(BaseModel):
    """Result of one ``send_notification`` call."""

    provider: str
    status: Literal["success", "error"]
    error: Optional[str] = None


# --------------------------------------------------------------------------- #
#  Mixin
# --------------------------------------------------------------------------- #
class ParrotAgentConfigMixin:
    """Parse and route the parrot YAML blocks for a FlowTask component.

    Place it *first* in the MRO so it consumes its own kwargs before
    ``FlowComponent`` re-applies the raw kwargs as instance attributes::

        class ParrotAgent(ParrotAgentConfigMixin, AgentBase, FlowComponent):
            ...

    Subclasses that ship their own LLM defaults (``ProductReportBot`` uses
    ``openai/gpt-4o``) declare them in :attr:`llm_config_defaults`; the YAML
    always wins over them.
    """

    #: Per-component defaults merged *under* the YAML ``llm_config``.
    llm_config_defaults: Dict[str, Any] = {}

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        # `llm:` may be a provider string (AgentBase reads it that way) or a
        # dict, in which case it is an alias of `llm_config`. Normalise before
        # the rest of the MRO sees it.
        raw_llm = kwargs.get("llm")
        raw_config: Dict[str, Any] = dict(kwargs.get("llm_config") or {})
        if isinstance(raw_llm, dict):
            raw_config = {**raw_llm, **raw_config}
            kwargs["llm"] = raw_config.get("llm")

        self.agent_class: Optional[str] = kwargs.get("agent_class")
        self.agent_kwargs: Dict[str, Any] = dict(kwargs.get("agent_kwargs") or {})
        self.agent_llm_config: AgentLLMConfig = self._build(
            AgentLLMConfig, {**self.llm_config_defaults, **raw_config}, "llm_config"
        )
        self.podcast_config: PodcastConfig = self._build(
            PodcastConfig, dict(kwargs.get("podcast") or {}), "podcast"
        )
        notification = kwargs.get("notification")
        self.notification_config: Optional[NotificationConfig] = (
            self._build(NotificationConfig, dict(notification), "notification") if notification else None
        )
        super().__init__(*args, **kwargs)

    # -- parsing helpers ---------------------------------------------------- #
    def _build(self, model: type, payload: Dict[str, Any], block: str) -> Any:
        """Validate one YAML block, reporting errors as ``ConfigError``."""
        try:
            return model(**payload)
        except ValidationError as exc:
            raise ConfigError(
                f"{self.__class__.__name__}: invalid '{block}' configuration: {exc}"
            ) from exc

    # -- agent class -------------------------------------------------------- #
    def resolve_agent_class(self, default: type) -> type:
        """Import the class named by ``agent_class``, or return ``default``.

        Accepts ``module.Class`` and ``module:Class``. Plugin agents live in
        ``PLUGINS_DIR/agents`` and are importable as ``agents.<module>``, so a
        bare ``epson_product.EpsonProductReport`` is retried with that prefix.

        Raises:
            ConfigError: path is not dotted, nothing importable, the class is
                missing, or it is not a ``BasicAgent`` subclass. The message
                lists every attempt so a typo is obvious.
        """
        if not self.agent_class:
            return default
        path = str(self.agent_class).replace(":", ".")
        module_path, _, class_name = path.rpartition(".")
        if not module_path:
            raise ConfigError(
                f"{self.__class__.__name__}: agent_class must be a dotted path "
                f"'module.Class', got '{self.agent_class}'"
            )
        candidates = [module_path]
        if not module_path.startswith("agents."):
            candidates.append(f"agents.{module_path}")
        # importing flowtask.plugins puts PLUGINS_DIR on sys.path
        from ... import plugins  # noqa: F401  pylint: disable=import-outside-toplevel

        errors: List[str] = []
        for candidate in candidates:
            try:
                module = importlib.import_module(candidate)
            except ImportError as exc:
                errors.append(f"{candidate}: {exc}")
                continue
            agent_cls = getattr(module, class_name, None)
            if agent_cls is None:
                errors.append(f"{candidate}: class '{class_name}' not found")
                continue
            if not (isinstance(agent_cls, type) and issubclass(agent_cls, BasicAgent)):
                raise ConfigError(
                    f"{self.__class__.__name__}: agent_class '{self.agent_class}' "
                    "must be a subclass of BasicAgent"
                )
            return agent_cls
        raise ConfigError(
            f"{self.__class__.__name__}: unable to load agent_class "
            f"'{self.agent_class}': {'; '.join(errors)}"
        )

    # -- LLM ---------------------------------------------------------------- #
    def agent_constructor_kwargs(self, **overrides: Any) -> Dict[str, Any]:
        """Build the kwargs the agent constructor must receive.

        ``temperature``/``max_tokens``/``top_p``/``top_k`` are resolved *once*
        by ``Chatbot.__init__``; assigning them to the instance afterwards has
        no effect, which is why they belong here and not in a post-hoc setattr.

        The two ``podcast_*_model`` keys are deliberately excluded — they are
        ``speech_report()`` arguments, not constructor arguments.
        """
        cfg = self.agent_llm_config
        kwargs: Dict[str, Any] = {
            "use_llm": cfg.llm,
            "llm": cfg.llm,  # provider name, not a client instance
        }
        if cfg.model is not None:
            kwargs["model"] = cfg.model
        for key in ("temperature", "max_tokens", "top_p", "top_k"):
            value = getattr(cfg, key)
            if value is not None:
                kwargs[key] = value
        # unknown llm_config keys are forwarded verbatim (extra="allow")
        for key, value in (cfg.model_extra or {}).items():
            if key not in PODCAST_MODEL_KEYS and value is not None:
                kwargs[key] = value
        kwargs.update(self.agent_kwargs)
        kwargs.update(overrides)
        return kwargs

    # -- podcast ------------------------------------------------------------ #
    def apply_podcast_config(self, agent: BasicAgent) -> BasicAgent:
        """Copy the configured podcast attributes onto an agent instance.

        ``speakers`` is deep-copied: ``BasicAgent.speech_report()`` writes
        ``speaker["gender"]`` back into the dict it is given, so sharing the
        YAML dict (or the class-level default) would leak mutations across
        rows, agents and runs.
        """
        podcast = self.podcast_config
        for attr in PODCAST_AGENT_ATTRIBUTES:
            value = getattr(podcast, attr, None)
            if value is None:
                continue
            if attr == "speakers":
                value = {
                    key: speaker.model_dump() if isinstance(speaker, BaseModel) else copy.deepcopy(speaker)
                    for key, speaker in value.items()
                }
            setattr(agent, attr, value)
        return agent

    def _resolve_directory(
        self, configured: Optional[str], base_dir: Optional[Path], default_subdir: str
    ) -> Optional[Path]:
        """Resolve one output directory, creating it."""
        if configured:
            path = Path(configured)
            if not path.is_absolute():
                if base_dir is None:
                    return None
                path = Path(base_dir) / path
        elif base_dir is None:
            return None
        else:
            path = Path(base_dir) / default_subdir
        path = path.resolve()
        path.mkdir(parents=True, exist_ok=True)
        return path

    def speech_report_kwargs(self, base_dir: Optional[Path] = None) -> Dict[str, Any]:
        """Build the kwargs of ``BasicAgent.speech_report()``.

        ``speech_report`` defaults both output directories to parrot's own
        ``STATIC_DIR/<agent_id>/…``, which is inside the ai-parrot install
        rather than the task. Passing ``base_dir`` makes them resolve under the
        task instead (``outputs/podcasts`` and ``outputs/generated_scripts``
        unless the ``podcast:`` block says otherwise).
        """
        podcast = self.podcast_config
        kwargs: Dict[str, Any] = {}
        max_lines = podcast.max_lines if podcast.max_lines is not None else podcast.speech_length
        if max_lines is not None:
            kwargs["max_lines"] = max_lines
        if podcast.num_speakers is not None:
            kwargs["num_speakers"] = podcast.num_speakers
        if podcast.instructions is not None:
            kwargs["podcast_instructions"] = podcast.instructions
        if self.agent_llm_config.podcast_script_model is not None:
            kwargs["script_model"] = self.agent_llm_config.podcast_script_model
        if self.agent_llm_config.podcast_tts_model is not None:
            kwargs["tts_model"] = self.agent_llm_config.podcast_tts_model
        output_directory = self._resolve_directory(podcast.output_directory, base_dir, DEFAULT_PODCAST_SUBDIR)
        if output_directory is not None:
            kwargs["output_directory"] = output_directory
        script_directory = self._resolve_directory(podcast.script_directory, base_dir, DEFAULT_SCRIPT_SUBDIR)
        if script_directory is not None:
            kwargs["directory"] = script_directory
        return kwargs

    # -- notification ------------------------------------------------------- #
    def resolve_notification_secrets(self, resolver: Callable[[Any], Any]) -> None:
        """Resolve mask/variable placeholders in the secret-shaped fields only.

        Called once from ``start()`` with the component's
        ``mask_replacement_recursively``. ``message``, ``subject`` and ``card``
        are deliberately excluded so row placeholders such as ``{model}``
        survive until send time.
        """
        config = self.notification_config
        if config is None:
            return
        if config.url_prefix:
            config.url_prefix = resolver(config.url_prefix)
        if config.url_token:
            config.url_token = resolver(config.url_token)
        for channel in config.channels:
            if channel.provider_options:
                channel.provider_options = resolver(channel.provider_options)
            recipients = channel.recipients if isinstance(channel.recipients, list) else [channel.recipients]
            for recipient in recipients:
                if isinstance(recipient, TeamsWebhookRecipient):
                    recipient.uri = resolver(recipient.uri)

    def load_card_templates(self, templates_dir: Path) -> None:
        """Replace each ``card_template`` with the card it points at.

        Keeps Adaptive Card JSON out of the task YAML. After this runs a
        templated channel is indistinguishable from one with an inline ``card``.
        """
        config = self.notification_config
        if config is None:
            return
        for channel in config.channels:
            if not channel.card_template:
                continue
            path = Path(templates_dir) / channel.card_template
            try:
                payload = json.loads(path.read_text(encoding="utf-8"))
            except FileNotFoundError as exc:
                raise ConfigError(
                    f"{self.__class__.__name__}: card_template '{channel.card_template}' not found in {templates_dir}"
                ) from exc
            except (json.JSONDecodeError, OSError) as exc:
                raise ConfigError(
                    f"{self.__class__.__name__}: card_template '{channel.card_template}' is not readable JSON: {exc}"
                ) from exc
            channel.card = self._build(TeamsCardConfig, payload, f"card_template:{channel.card_template}")
            channel.card_template = None

    def should_notify(self, succeeded: bool) -> bool:
        """Apply ``notification.when`` to one outcome."""
        config = self.notification_config
        if config is None:
            return False
        if config.when == "always":
            return True
        return succeeded if config.when == "success" else not succeeded

    def result_urls(self, context: Dict[str, Any], columns: Iterable[str]) -> Dict[str, str]:
        """Expose ``{<column>_url}`` for every attachment column.

        A Teams Adaptive Card cannot carry an attachment, so the only way to
        make a generated podcast playable from the card is an HTTP link. Empty
        when ``url_prefix`` is unset — the placeholder is then left intact by
        ``SafeDict``.
        """
        config = self.notification_config
        if config is None or not config.url_prefix:
            return {}
        prefix = config.url_prefix.rstrip("/")
        urls: Dict[str, str] = {}
        for column in columns:
            value = context.get(column)
            if isinstance(value, (list, tuple)):
                value = next((item for item in value if item), None)
            if not value:
                continue
            path = Path(str(value))
            url = f"{prefix}/{path.parent.name}/{path.name}" if path.parent.name else f"{prefix}/{path.name}"
            if config.url_token:
                url += ("&" if "?" in url else "?") + f"token={config.url_token}"
            urls[f"{column}_url"] = url
        return urls

    @staticmethod
    def _files_from(context: Dict[str, Any], columns: Iterable[str]) -> List[str]:
        """Collect existing-looking file paths named by ``attach_columns``."""
        files: List[str] = []
        for column in columns:
            value = context.get(column)
            if not value:
                continue
            items = value if isinstance(value, (list, tuple)) else [value]
            files.extend(str(item) for item in items if item)
        return files

    @staticmethod
    def _render(value: Any, context: Dict[str, Any]) -> Any:
        """Format strings with the context, leaving unknown placeholders alone."""
        if isinstance(value, str):
            return value.format_map(SafeDict(**context))
        if isinstance(value, dict):
            return {k: ParrotAgentConfigMixin._render(v, context) for k, v in value.items()}
        if isinstance(value, list):
            return [ParrotAgentConfigMixin._render(item, context) for item in value]
        return value

    def _recipients_for(self, channel: NotificationChannel) -> Any:
        """Map YAML recipients onto the models ``send_notification`` expects."""
        raw = channel.recipients if isinstance(channel.recipients, list) else [channel.recipients]
        recipients: List[Any] = []
        for item in raw:
            if isinstance(item, TeamsChannelRecipient):
                recipients.append(
                    TeamsChannel(name=item.name, team_id=item.team_id, channel_id=item.channel_id)
                )
            elif isinstance(item, TeamsWebhookRecipient):
                recipients.append(TeamsWebhook(uri=item.uri))
            elif channel.provider == "telegram":
                recipients.append(Chat(chat_id=str(item)))
            else:
                # email, and Teams e-mail addresses: parrot's _parse_recipients
                # turns these into Actor objects itself.
                recipients.append(item)
        return recipients

    def notification_calls(self, context: Dict[str, Any], result: Any = None) -> List[Dict[str, Any]]:
        """Turn the ``notification`` block into ``send_notification`` kwargs.

        Pure — it performs no I/O, which is what makes the routing testable
        without a notification provider. ``result_urls()`` is merged into the
        context first so a card action can reference ``{podcast_path_url}``.
        """
        config = self.notification_config
        if config is None:
            return []
        calls: List[Dict[str, Any]] = []
        for channel in config.channels:
            local_context = {**context, **self.result_urls(context, channel.attach_columns)}
            files = self._files_from(local_context, channel.attach_columns)
            message: Any = self._render(channel.message, local_context) if channel.message else ""
            call: Dict[str, Any] = {
                "recipients": self._recipients_for(channel),
                "provider": channel.provider,
                "with_attachments": channel.with_attachments,
            }
            if channel.card is not None:
                card = self._render(channel.card.model_dump(exclude_none=True), local_context)
                message = BasicAgent.build_teams_card(**card)
            if files:
                output = message if isinstance(message, str) else ""
                call["report"] = NotificationReport(output=output, files=files)
            elif result is not None and hasattr(result, "files"):
                call["report"] = result
            call["message"] = message
            if channel.subject:
                call["subject"] = self._render(channel.subject, local_context)
            if channel.template:
                call["template"] = channel.template
            if channel.disable_notification is not None:
                call["disable_notification"] = channel.disable_notification
            if channel.provider_options:
                call["provider_options"] = channel.provider_options
            call.update(channel.extra)
            calls.append(call)
        return calls

    async def send_configured_notifications(
        self, agent: BasicAgent, context: Dict[str, Any], result: Any = None
    ) -> List[NotificationOutcome]:
        """Deliver one notification per configured channel.

        ``send_notification`` never raises — it returns
        ``{"status": "error", ...}`` — so every return value is classified with
        ``notification_succeeded()``, otherwise a failed delivery looks like a
        success. Channels are independent: one failing channel never prevents
        the others, and ``fail_on_error`` only raises once all were attempted.
        """
        config = self.notification_config
        if config is None:
            return []
        outcomes: List[NotificationOutcome] = []
        for call in self.notification_calls(context, result=result):
            provider = call.get("provider", "unknown")
            try:
                returned = await agent.send_notification(**call)
            except Exception as exc:  # noqa: BLE001 — a channel must not abort the rest
                outcomes.append(NotificationOutcome(provider=provider, status="error", error=str(exc)))
                continue
            if agent.notification_succeeded(returned):
                outcomes.append(NotificationOutcome(provider=provider, status="success"))
            else:
                error = returned.get("error") if isinstance(returned, dict) else None
                outcomes.append(
                    NotificationOutcome(
                        provider=provider,
                        status="error",
                        error=str(error) if error else "unknown error",
                    )
                )
        if config.fail_on_error:
            failed = [outcome for outcome in outcomes if outcome.status == "error"]
            if failed:
                detail = "; ".join(f"{o.provider}: {o.error}" for o in failed)
                raise ComponentError(f"{self.__class__.__name__}: notification delivery failed — {detail}")
        return outcomes

    def _summary_dataframe_attachment(self, df: Any, directory: Path, fmt: str = "csv") -> Path:
        """Write a result DataFrame to disk so a summary can attach it.

        Deliberately *not* called by ``ParrotAgent.run()`` (FEAT-557 Q5): it
        exists so a component extending ``ParrotAgent`` can opt in on demand.
        """
        directory = Path(directory)
        directory.mkdir(parents=True, exist_ok=True)
        path = directory / f"results.{fmt}"
        if fmt == "csv":
            df.to_csv(path, index=False)
        elif fmt in ("xlsx", "xls"):
            df.to_excel(path, index=False)
        else:
            raise ConfigError(f"{self.__class__.__name__}: unsupported summary attachment format '{fmt}'")
        return path
