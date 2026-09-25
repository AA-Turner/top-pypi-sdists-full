"""ParrotAgent — invoke any ai-parrot agent method from a FlowTask YAML step.

Every parrot integration in FlowTask so far is a bespoke component with the
agent class and the invoked method hardcoded: ``NextStopAgent`` always calls
``NextStop.report()``, ``PodcastMaker`` always calls
``BasicAgent.speech_report()``, ``ProductReportBot`` always runs a fixed
PDF/PPT/PODCAST flow. Using a plugin agent from ``PLUGINS_DIR/agents`` or
calling a different method meant writing a new component.

``ParrotAgent`` is that generalisation: the agent class, the method, its static
and per-row arguments and the delivery of the results all come from YAML.
"""
import asyncio
import json
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd

from parrot.bots.agent import BasicAgent          # verified: flowtask/interfaces/parrot/agent.py:16
from parrot.tools.abstract import AbstractTool    # verified: flowtask/interfaces/parrot/agent.py:18

from ..exceptions import ComponentError, ConfigError, DataNotFound
from ..interfaces.flow import FlowComponent
from ..interfaces.parrot import AgentBase, ParrotAgentConfigMixin
from ..interfaces.parrot.config import SafeDict

#: Accepted values of the ``on_error`` parameter.
ON_ERROR_MODES = ("raise", "skip", "store")


class ParrotAgent(ParrotAgentConfigMixin, AgentBase, FlowComponent):
    """ParrotAgent

    Overview:
        Invoke any public method of any ``BasicAgent`` subclass from YAML, once
        per input row or once when there is no input, and optionally deliver the
        results by email, Telegram or MS Teams.

    .. table:: Properties
       :widths: auto

    +--------------------+----------+-----------+---------------------------------------------------------------+
    | Name               | Required | Type      | Description                                                   |
    +====================+==========+===========+===============================================================+
    | agent_class        |   No     | str       | Dotted path of the agent (``module.Class`` or ``module:Class``|
    |                    |          |           | ). Plugin agents in ``PLUGINS_DIR/agents`` also resolve under |
    |                    |          |           | the ``agents.`` prefix. Defaults to ``BasicAgent``.           |
    +--------------------+----------+-----------+---------------------------------------------------------------+
    | agent_name         |   No     | str       | Display name given to the agent.                              |
    +--------------------+----------+-----------+---------------------------------------------------------------+
    | agent_id           |   No     | str       | Agent identifier used for prompts and generated files.        |
    +--------------------+----------+-----------+---------------------------------------------------------------+
    | agent_kwargs       |   No     | dict      | Extra keyword arguments passed to the agent constructor.      |
    +--------------------+----------+-----------+---------------------------------------------------------------+
    | method             |   Yes    | str       | Public method to invoke on the agent.                         |
    +--------------------+----------+-----------+---------------------------------------------------------------+
    | method_kwargs      |   No     | dict      | Static keyword arguments for every call.                      |
    +--------------------+----------+-----------+---------------------------------------------------------------+
    | row_kwargs         |   No     | list/dict | ``{argument: column}`` mapping, or a list when both names     |
    |                    |          |           | match. Values come from the input DataFrame row.              |
    +--------------------+----------+-----------+---------------------------------------------------------------+
    | prompt_file        |   No     | str       | Prompt read from ``<taskstore>/<program>/prompts/``, formatted|
    |                    |          |           | with the row and passed as ``prompt_argument``.               |
    +--------------------+----------+-----------+---------------------------------------------------------------+
    | prompt_argument    |   No     | str       | Argument receiving the prompt. Default ``question``.          |
    +--------------------+----------+-----------+---------------------------------------------------------------+
    | output_column      |   No     | str       | Column receiving the serialised result. Default ``result``.   |
    +--------------------+----------+-----------+---------------------------------------------------------------+
    | on_error           |   No     | str       | ``raise`` | ``skip`` | ``store``. Default ``store``.          |
    +--------------------+----------+-----------+---------------------------------------------------------------+
    | llm_config         |   No     | dict      | Provider, model and tuning kwargs for the agent constructor.  |
    +--------------------+----------+-----------+---------------------------------------------------------------+
    | podcast            |   No     | dict      | Speakers, lengths and output directories for ``speech_report``|
    +--------------------+----------+-----------+---------------------------------------------------------------+
    | notification       |   No     | dict      | Delivery of the results (email / telegram / teams).           |
    +--------------------+----------+-----------+---------------------------------------------------------------+

    Return the output of the agent method in ``output_column``, alongside every
    column of the input DataFrame.

    :consumes: any
    :produces: dataframe

    Notes:
        Per-row notifications are sent while the task is still running, so a
        re-run of the task re-sends them.

        MS Teams credentials are global (``TEAMS_NOTIFY_*``); a missing value
        produces an error outcome per channel, not a configuration error.

    Example:

    .. code-block:: yaml

        ParrotAgent:
          agent_class: agents.epson_product.EpsonProductReport
          method: speech_report
          row_kwargs: {report: transcript}
          podcast:
            speech_length: 24
            num_speakers: 2
            output_directory: outputs/podcasts
          llm_config:
            llm: google
            model: gemini-2.5-flash
    """

    _agent_name: str = "ParrotAgent"          # verified: flowtask/interfaces/parrot/agent.py:28
    agent_id: str = "parrot_agent"            # verified: flowtask/interfaces/parrot/agent.py:29
    _agent_class: type = BasicAgent           # verified: flowtask/interfaces/parrot/agent.py:30

    def __init__(self, loop=None, job=None, stat=None, **kwargs: Any) -> None:
        self.method: Optional[str] = kwargs.get("method")
        self.method_kwargs: Dict[str, Any] = dict(kwargs.get("method_kwargs") or {})
        # NOTE: stored private on purpose. FlowComponent re-applies the raw YAML
        # kwargs as attributes after super().__init__(), so a public
        # `self._row_kwargs` would be silently reverted to the unnormalised value
        # (spec §7, "store config under names that do not collide").
        self._row_kwargs: Dict[str, str] = self._normalise_row_kwargs(kwargs.get("row_kwargs"))
        self.prompt_file: Optional[str] = kwargs.get("prompt_file")
        self.prompt_argument: str = kwargs.get("prompt_argument", "question")
        self.output_column: str = kwargs.get("output_column", "result")
        self.on_error: str = kwargs.get("on_error", "store")

        # Validate here rather than at the first row: a typo must not surface
        # only after an LLM call has already been paid for.
        if not self.method or not isinstance(self.method, str):
            raise ConfigError("ParrotAgent: 'method' is required and must be a string")
        if self.method.startswith("_"):
            raise ConfigError(
                f"ParrotAgent: 'method' cannot be a private attribute, got '{self.method}'"
            )
        if self.on_error not in ON_ERROR_MODES:
            raise ConfigError(
                f"ParrotAgent: on_error must be one of {ON_ERROR_MODES}, got '{self.on_error}'"
            )

        # AgentBase.start() needs a destination (agent.py:163-167); reuse the
        # podcast output directory when one is declared so the YAML only has to
        # name a path once. An explicit `destination` still wins.
        podcast_output = (kwargs.get("podcast") or {}).get("output_directory")
        if podcast_output and "destination" not in kwargs:
            self.destination = podcast_output

        self._resolved_prompt: Optional[str] = None
        super().__init__(loop=loop, job=job, stat=stat, **kwargs)

    @staticmethod
    def _normalise_row_kwargs(value: Any) -> Dict[str, str]:
        """Accept either ``[col, ...]`` or ``{argument: column}``."""
        if not value:
            return {}
        if isinstance(value, dict):
            return {str(k): str(v) for k, v in value.items()}
        if isinstance(value, (list, tuple)):
            return {str(item): str(item) for item in value}
        raise ConfigError(
            f"ParrotAgent: row_kwargs must be a list or a mapping, got {type(value).__name__}"
        )

    def _define_tools(self, base_dir: Path) -> List[AbstractTool]:
        """Return an empty list — agents declare their own tools."""
        return []

    async def create_agent(
        self,
        llm: Any = None,
        model: str = None,
        tools: Optional[List[Any]] = None,
        backstory: Optional[str] = None,
    ) -> BasicAgent:
        """Instantiate the configured agent class with full constructor kwargs.

        Overrides ``AgentBase.create_agent`` (agent.py:114), which passes
        neither ``agent_id`` nor ``use_llm`` nor the tuning kwargs. Parrot
        resolves ``temperature``/``max_tokens``/``top_p``/``top_k`` once in
        ``Chatbot.__init__`` (abstract.py:507-520), so they only take effect
        when they arrive as constructor arguments.
        """
        agent_cls = self.resolve_agent_class(self._agent_class)
        agent_kwargs = self.agent_constructor_kwargs(
            name=self._agent_name,
            agent_id=self.agent_id,
            backstory=backstory or self._backstory,
        )
        try:
            agent = agent_cls(**agent_kwargs)
        except Exception as exc:
            raise ComponentError(
                f"ParrotAgent: cannot build {agent_cls.__name__}: {exc}"
            ) from exc
        agent.set_response(self._agent_response)      # verified: parrot/bots/agent.py:416
        self.apply_podcast_config(agent)
        try:
            await agent.configure()                   # verified: parrot/bots/agent.py:154
        except Exception as exc:
            raise ComponentError(
                f"ParrotAgent: cannot configure {agent_cls.__name__}: {exc}"
            ) from exc
        self._agent = agent
        self.logger.info(
            "ParrotAgent: using %s.%s", agent_cls.__module__, agent_cls.__name__
        )
        return agent

    async def start(self, **kwargs: Any) -> bool:
        """Bind the input, build the agent and validate everything callable.

        Raises:
            DataNotFound: a ``row_kwargs`` column is missing from the input.
            ConfigError: the configured method does not exist or is not callable.
        """
        if self.previous:
            self.data = self.input

        has_input = isinstance(self.data, pd.DataFrame)
        if has_input and self._row_kwargs:
            missing = [c for c in self._row_kwargs.values() if c not in self.data.columns]
            if missing:
                raise DataNotFound(
                    f"ParrotAgent: row_kwargs column(s) {missing} not found. "
                    f"Available: {list(self.data.columns)}"
                )
        if not has_input and self._row_kwargs:
            raise ConfigError(
                "ParrotAgent: row_kwargs requires an input DataFrame — connect a previous step."
            )

        # AgentBase.start() sets self.directory/self.destination and builds the agent
        await super().start(**kwargs)

        method = getattr(self._agent, self.method, None)
        if method is None or not callable(method):
            raise ConfigError(
                f"ParrotAgent: agent {type(self._agent).__name__} has no callable "
                f"method '{self.method}'"
            )

        if self.prompt_file:
            self._resolved_prompt = self._load_prompt(self.prompt_file)

        if self.notification_config is not None:
            # Resolve the secret-shaped fields once. Row placeholders such as
            # {model} are deliberately left alone until send time.
            self.resolve_notification_secrets(self.mask_replacement_recursively)
            self.load_card_templates(Path(self.directory) / "templates")
            self._warn_on_dead_links()

        return True

    def _warn_on_dead_links(self) -> None:
        """Warn when a card links to a result URL that cannot be built.

        A Teams Adaptive Card cannot carry an attachment, so a podcast is only
        playable from the card through an HTTP link. Without ``url_prefix`` the
        ``{<column>_url}`` placeholder survives verbatim and the action renders
        a dead link — silently, which is the worst outcome.
        """
        config = self.notification_config
        if config is None or config.url_prefix:
            return
        for channel in config.channels:
            if channel.card is None:
                continue
            if "_url}" in json.dumps(channel.card.model_dump(), default=str):
                self.logger.warning(
                    "ParrotAgent: a %s card references a result URL but "
                    "notification.url_prefix is not set — the link will not resolve.",
                    channel.provider,
                )

    def _load_prompt(self, prompt_file: str) -> str:
        """Read a prompt from ``<taskstore>/<program>/prompts/``.

        ``BasicAgent.open_prompt`` reads ``AGENTS_DIR/<agent_id>/prompts``
        instead, which is not where a task keeps its own prompts.
        """
        path = Path(self.directory) / "prompts" / prompt_file
        try:
            content = path.read_text(encoding="utf-8")
        except FileNotFoundError as exc:
            raise ConfigError(
                f"ParrotAgent: prompt_file '{prompt_file}' not found at {path}"
            ) from exc
        self.logger.debug("ParrotAgent: loaded prompt from %s", path)
        return content

    @staticmethod
    def _serialise(result: Any) -> Any:
        """Reduce an agent result to something a DataFrame cell can hold."""
        if result is None:
            return None
        if hasattr(result, "model_dump"):
            return result.model_dump(mode="json")
        if isinstance(result, dict):
            return result
        if hasattr(result, "output"):
            return result.output
        if isinstance(result, (str, int, float, bool)):
            return result
        return str(result)

    def _build_call_kwargs(self, row: Dict[str, Any]) -> Dict[str, Any]:
        """Merge the call arguments, lowest precedence first."""
        call_kwargs: Dict[str, Any] = dict(self.method_kwargs)
        if self.method == "speech_report":
            # Only speech_report understands these; passing them to an arbitrary
            # method would be a TypeError.
            call_kwargs.update(self.speech_report_kwargs(base_dir=Path(self.directory)))
        for argument, column in self._row_kwargs.items():
            call_kwargs[argument] = row.get(column)
        if self._resolved_prompt is not None:
            call_kwargs[self.prompt_argument] = self._resolved_prompt.format_map(SafeDict(**row))
        return call_kwargs

    async def _invoke(self, row: Dict[str, Any]) -> Any:
        """Call the agent method once, awaiting it when it is a coroutine."""
        method = getattr(self._agent, self.method)
        returned = method(**self._build_call_kwargs(row))
        if asyncio.iscoroutine(returned):
            returned = await returned
        return returned

    async def run(self) -> pd.DataFrame:
        """Invoke the agent once per input row, or once when there is no input.

        Returns the input DataFrame with ``output_column`` appended — every
        input column is preserved so downstream steps (``TableOutput``,
        ``CopyToPg``, ``SendNotify``) still see what they were given.
        """
        has_input = isinstance(self.data, pd.DataFrame)
        rows: List[Dict[str, Any]] = (
            self.data.to_dict("records") if has_input else [{}]
        )

        keep: List[int] = []
        results: List[Any] = []
        errors: List[Optional[str]] = []
        notifications: List[Optional[str]] = []
        success_count = 0

        for index, row in enumerate(rows):
            outcome_json: Optional[str] = None
            try:
                returned = await self._invoke(row)
            except Exception as exc:
                self.logger.error("ParrotAgent: row %s failed: %s", index, exc)
                if self.on_error == "raise":
                    raise ComponentError(
                        f"ParrotAgent: row {index} failed calling '{self.method}': {exc}"
                    ) from exc
                if self.on_error == "skip":
                    continue
                keep.append(index)
                results.append(None)
                errors.append(str(exc))
                notifications.append(await self._notify_row(row, None, str(exc)))
                continue

            success_count += 1
            serialised = self._serialise(returned)
            keep.append(index)
            results.append(serialised)
            errors.append(None)
            outcome_json = await self._notify_row(row, returned, None, serialised=serialised)
            notifications.append(outcome_json)

        df = self._assemble(has_input, rows, keep, results, errors, notifications)
        await self._notify_summary(df, len(rows), success_count)
        return df

    def _assemble(
        self,
        has_input: bool,
        rows: List[Dict[str, Any]],
        keep: List[int],
        results: List[Any],
        errors: List[Optional[str]],
        notifications: List[Optional[str]],
    ) -> pd.DataFrame:
        """Build the output frame, preserving every input column."""
        if has_input:
            df = self.data.iloc[keep].copy() if len(keep) != len(rows) else self.data.copy()
        else:
            df = pd.DataFrame(index=range(len(keep)))
        df[self.output_column] = results
        if self.on_error == "store":
            df[f"{self.output_column}_error"] = errors
        if self.notification_config is not None and self.notification_config.mode == "per_row":
            df[f"{self.output_column}_notifications"] = notifications
        self._result = df
        return df

    def _base_context(self) -> Dict[str, Any]:
        """Task-level values every notification context starts from."""
        return {
            **(getattr(self, "_variables", None) or {}),
            "task": self.StepName or "",
            "program": self._program,
        }

    async def _notify_row(
        self,
        row: Dict[str, Any],
        result: Any,
        error: Optional[str],
        serialised: Any = None,
    ) -> Optional[str]:
        """Deliver one row's result, returning the outcomes as JSON.

        Context precedence, lowest first: task variables, the row's columns,
        the serialised result's fields, then ``result``/``error``.
        """
        config = self.notification_config
        if config is None or config.mode != "per_row":
            return None
        if not self.should_notify(error is None):
            return None

        context = self._base_context()
        context.update(row)
        if isinstance(serialised, dict):
            context.update(serialised)
        context["result"] = serialised if isinstance(serialised, str) else ""
        context["error"] = error or ""

        outcomes = await self.send_configured_notifications(self._agent, context, result)
        return json.dumps([outcome.model_dump() for outcome in outcomes])

    async def _notify_summary(self, df: pd.DataFrame, count: int, success_count: int) -> None:
        """Deliver a single notification describing the whole run."""
        config = self.notification_config
        if config is None or config.mode != "summary":
            return
        if not self.should_notify(success_count > 0):
            return

        context = self._base_context()
        context.update(
            {
                "count": count,
                "success_count": success_count,
                "error_count": count - success_count,
                "results": self._results_table(df, config.summary_max_rows),
                "result": "",
                "error": "",
            }
        )
        # Attachment columns hold one path per row; a summary attaches them all,
        # capped so a large run cannot mail hundreds of files. A dict result
        # keeps its fields inside `output_column` rather than as columns of
        # their own, so look there too — otherwise `attach_columns` would work
        # per row (where the result is merged into the context) but not here.
        for column in {c for ch in config.channels for c in ch.attach_columns}:
            values = self._collect_paths(df, column)
            if values:
                context[column] = values[: config.max_attachments]

        outcomes = await self.send_configured_notifications(self._agent, context)
        self.logger.info(
            "ParrotAgent: summary notification sent — %s",
            ", ".join(f"{o.provider}={o.status}" for o in outcomes) or "no channels",
        )

    def _collect_paths(self, df: pd.DataFrame, column: str) -> List[Any]:
        """Gather one attachment column's values across every row."""
        if column in df.columns:
            return [value for value in df[column].tolist() if value]
        values: List[Any] = []
        for item in df.get(self.output_column, pd.Series(dtype=object)).tolist():
            if isinstance(item, dict) and item.get(column):
                values.append(item[column])
        return values

    @staticmethod
    def _results_table(df: pd.DataFrame, max_rows: int) -> str:
        """Render the first `max_rows` rows as a markdown table."""
        if df.empty:
            return "_no rows_"
        try:
            return df.head(max_rows).to_markdown(index=False)
        except ImportError:
            # to_markdown needs `tabulate`; a summary must not fail over formatting.
            return df.head(max_rows).to_string(index=False)

    async def close(self) -> None:
        """Release the agent context if one was entered."""
        self._agent = None
