"""PodcastMaker — FlowTask component for generating podcast audio from any text content.

Delegates all script generation and TTS synthesis to ``BasicAgent.speech_report()``.
The component is a thin wrapper: reads rows from a DataFrame, optionally configures
speakers on the agent, calls ``speech_report()`` per row, and returns a DataFrame
with ``podcast_path``, ``script_path``, and ``podcast_error`` columns.

Failed episodes (e.g. Google TTS 429 / 503 errors) are kept in the output DataFrame
with ``podcast_path=None``, ``script_path=None``, and ``podcast_error`` set to the
full exception message.  Each failure is also appended to a daily JSONL audit log at::

    STATIC_DIR/{agent_id}/podcast_failures/failures_<YYYYMMDD>.jsonl

YAML usage example::

    - QueryToPandas:
        query: SELECT title, summary FROM reports WHERE published_at >= NOW() - INTERVAL '7 days'

    - PodcastMaker:
        text_column: summary
        title_column: title
        output_column: podcast_result
        podcast_instructions: podcast_script.txt  # loaded from {agent_id}/prompts/
        max_lines: 20
        num_speakers: 2
        speakers:
          interviewer:
            name: Alex
            role: interviewer
            characteristic: engaging and curious
            gender: male
            voice: puck           # optional — any TTSVoice value
          interviewee:
            name: Jordan
            role: interviewee
            characteristic: knowledgeable and concise
            gender: female
            voice: kore           # optional
        llm:
          llm: google
          model: gemini-2.5-flash  # controls script generation only, NOT TTS model
"""
import asyncio
import json
import re
from collections.abc import Callable
from datetime import date, datetime
from io import BytesIO
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd
from parrot.conf import AGENTS_DIR, STATIC_DIR

from ..exceptions import ComponentError, ConfigError
from ..interfaces.parrot import AgentBase
from .flow import FlowComponent


class PodcastMaker(AgentBase, FlowComponent):
    """Generate podcast audio episodes from any tabular text content.

    Wraps ``BasicAgent.speech_report()`` as a FlowTask component.  For each
    row in the input DataFrame the agent generates a conversational script and
    synthesises it to audio.  The TTS model is always determined by the agent
    internally — the ``llm:`` block controls only the script-generation LLM.

    Failed episodes (common with Google TTS rate limits) are not discarded.
    They remain in the output DataFrame with ``podcast_path=None``,
    ``script_path=None``, and ``podcast_error`` populated.  A daily JSONL
    audit log is also written to ``STATIC_DIR/{agent_id}/podcast_failures/``
    so operators can identify which episodes need to be re-run.

    Args:
        text_column (str): Column containing the source text per episode. Required.
        title_column (str, optional): Column used as the episode title in logs.
        output_column (str): Column added to the result DataFrame with the source
            text. Default: ``podcast_result``.
        podcast_instructions (str): Prompt filename (from ``{agent_id}/prompts/``)
            or inline instruction text for ``speech_report()``.
            Default: ``for_podcast.txt``.
        max_lines (int): Maximum dialogue lines in the generated script. Default: ``20``.
        num_speakers (int): Number of speakers (max 2 for Gemini TTS). Default: ``2``.
        speakers (dict, optional): Speaker definitions keyed by role
            (``interviewer`` / ``interviewee``).  Each entry supports ``name``,
            ``role``, ``characteristic``, ``gender``, and optional ``voice``
            (any value from ``parrot.models.google.TTSVoice``).
            When omitted, the ``BasicAgent`` defaults (Lydia + Brian) are used.
        as_bytes (bool): When ``True``, read the generated audio file into a
            ``BytesIO`` object and add it to the output DataFrame as ``file_data``
            (with ``content_type: audio/wav``).  The ``podcast_path`` column is
            still populated for auditing.  Default: ``False``.
        filename_column (str, optional): Column whose value is used to rename
            the generated audio file on disk (slugified, e.g. ``"Costco Canada"``
            → ``costco_canada.wav``).  Useful for making files human-readable.
            When combined with ``as_bytes``, the rename happens first so
            ``podcast_path`` reflects the new name.
        llm (dict): LLM config for script generation — ``llm``, ``model``,
            ``temperature``.  Does **not** affect the TTS model.

    Example YAML::

        - PodcastMaker:
            text_column: summary
            title_column: report_title
            output_column: podcast_result
            podcast_instructions: weekly_digest.txt
            max_lines: 15
            num_speakers: 2
            speakers:
              interviewer:
                name: Alex
                role: interviewer
                characteristic: engaging and curious
                gender: male
                voice: puck
              interviewee:
                name: Jordan
                role: interviewee
                characteristic: knowledgeable and concise
                gender: female
                voice: kore
            llm:
              llm: google
              model: gemini-2.5-flash
    """

    _version = "1.2.0"
    _agent_name: str = "PodcastMaker"
    agent_id: str = "podcast_maker"

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ) -> None:
        self.text_column: str = kwargs.get("text_column", "text")
        self.title_column: Optional[str] = kwargs.get("title_column")
        self.output_column: str = kwargs.get("output_column", "podcast_result")
        self.podcast_instructions: str = kwargs.get("podcast_instructions", "for_podcast.txt")
        self.max_lines: int = int(kwargs.get("max_lines", 20))
        self.num_speakers: int = int(kwargs.get("num_speakers", 2))
        self.as_bytes: bool = bool(kwargs.get("as_bytes", False))
        self.filename_column: Optional[str] = kwargs.get("filename_column")
        # Optional speaker override from YAML
        self._speakers_cfg: Optional[Dict[str, Any]] = kwargs.get("speakers")
        # Parse llm config dict — AgentBase expects llm to be a provider string,
        # not the full dict from YAML ({llm: google, model: gemini-2.5-flash}).
        llm_cfg = kwargs.get("llm")
        if isinstance(llm_cfg, dict):
            kwargs["llm"] = llm_cfg.get("llm", "google")
            if llm_cfg.get("model"):
                kwargs["model"] = llm_cfg.get("model")
        super().__init__(loop=loop, job=job, stat=stat, **kwargs)

    @staticmethod
    def _slugify(value: str) -> str:
        """Convert a string to a safe filename slug.

        Args:
            value: Raw string (e.g. column value like ``"Costco Canada"``).

        Returns:
            Lowercase, underscore-separated safe filename (e.g. ``"costco_canada"``).
        """
        value = re.sub(r"[^\w\s-]", "", str(value)).strip().lower()
        return re.sub(r"[\s-]+", "_", value)

    def _define_tools(self, base_dir: Path) -> list:
        """No external tools needed — podcast generation is self-contained in BasicAgent."""
        return []

    def _write_failure_log(self, title: str, text: str, exc: Exception) -> None:
        """Append one entry to the daily JSONL failure log.

        Args:
            title: Episode title (from ``title_column`` or row index).
            text: Full source text (first 120 chars stored in log).
            exc: The exception that caused the failure.
        """
        log_dir = Path(STATIC_DIR) / self.agent_id / "podcast_failures"
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / f"failures_{date.today():%Y%m%d}.jsonl"

        entry = {
            "ts": datetime.utcnow().isoformat(timespec="seconds"),
            "title": title,
            "text_snippet": text[:120],
            "error": str(exc),
            "retry": False,
        }
        with log_file.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(entry) + "\n")
        self.logger.debug("PodcastMaker: failure logged → %s", log_file)

    async def close(self) -> None:
        """No persistent resources to release."""

    async def start(self, **kwargs) -> bool:
        """Validate input DataFrame, initialise the agent, and apply speaker config.

        Returns:
            True if initialisation succeeded.

        Raises:
            ComponentError: If no input data is provided.
            ConfigError: If ``text_column`` is missing from the input DataFrame.
        """
        if self.previous:
            self.data = self.input

        if not isinstance(self.data, pd.DataFrame) or self.data.empty:
            raise ComponentError("PodcastMaker: no input data — connect a previous step.")

        if self.text_column not in self.data.columns:
            raise ConfigError(
                f"PodcastMaker: text_column '{self.text_column}' not found. "
                f"Available: {list(self.data.columns)}"
            )

        # AgentBase.start() creates and configures self._agent
        await super().start(**kwargs)

        # Resolve the prompt file using PodcastMaker's own agent_id so it
        # looks in AGENTS_DIR/podcast_maker/prompts/ instead of the internal
        # agent's agent_id directory (which defaults to "agent").
        prompt_path = AGENTS_DIR / self.agent_id / "prompts" / self.podcast_instructions
        try:
            self._resolved_podcast_instructions: str = prompt_path.read_text(encoding="utf-8")
            self.logger.debug("PodcastMaker: loaded prompt from %s", prompt_path)
        except FileNotFoundError:
            self.logger.warning(
                "PodcastMaker: prompt file not found at %s — passing filename to agent",
                prompt_path,
            )
            self._resolved_podcast_instructions = self.podcast_instructions

        # Override speakers on the agent if configured in YAML
        if self._speakers_cfg and self._agent:
            self._agent.speakers = self._speakers_cfg
            self.logger.info(
                "PodcastMaker: speakers overridden → %s",
                list(self._speakers_cfg.keys()),
            )

        return True

    async def run(self) -> pd.DataFrame:
        """Generate a podcast episode for each row in the input DataFrame.

        Calls ``BasicAgent.speech_report()`` per row.  Successful rows receive
        ``podcast_path`` and ``script_path`` from the returned dict.  Failed rows
        (e.g. Google TTS 429 errors) receive ``podcast_path=None``,
        ``script_path=None``, and ``podcast_error`` set to the full exception
        message.  All rows — success and failure — are included in the output
        DataFrame.  Each failure is also appended to the daily JSONL audit log.

        Returns:
            DataFrame with original columns plus ``output_column``,
            ``podcast_path``, ``script_path``, and ``podcast_error``.
        """
        results: List[Dict[str, Any]] = []

        async with self._agent:
            for idx, row in self.data.iterrows():
                source_text = str(row.get(self.text_column, "") or "").strip()
                if not source_text:
                    self.logger.warning("PodcastMaker: empty text at row %s, skipping.", idx)
                    continue

                if self.title_column:
                    _title = row.get(self.title_column)
                    episode_title = (
                        str(_title) if _title is not None and not pd.isna(_title)
                        else f"episode_{idx}"
                    )
                else:
                    episode_title = f"episode_{idx}"
                self.logger.info("PodcastMaker: generating episode '%s'", episode_title)

                podcast_path: Optional[Path] = None
                script_path: Optional[Path] = None
                podcast_error: Optional[str] = None

                try:
                    result: Dict[str, Any] = await self._agent.speech_report(
                        report=source_text,
                        max_lines=self.max_lines,
                        num_speakers=self.num_speakers,
                        podcast_instructions=self._resolved_podcast_instructions,
                    )
                    podcast_path = str(result.get("podcast_path")) if result.get("podcast_path") else None
                    script_path = str(result.get("script_path")) if result.get("script_path") else None

                    # Rename generated file to a human-readable name
                    if podcast_path and self.filename_column:
                        col_value = row.get(self.filename_column)
                        if col_value is not None and not pd.isna(col_value):
                            slug = self._slugify(str(col_value))
                            old_p = Path(podcast_path)
                            new_p = old_p.parent / f"{slug}{old_p.suffix}"
                            try:
                                old_p.rename(new_p)
                                podcast_path = str(new_p)
                                self.logger.debug(
                                    "PodcastMaker: renamed %s → %s",
                                    old_p.name, new_p.name,
                                )
                            except OSError as rename_err:
                                self.logger.warning(
                                    "PodcastMaker: could not rename %s — %s",
                                    old_p, rename_err,
                                )
                except Exception as exc:
                    podcast_error = str(exc)
                    self.logger.error(
                        "PodcastMaker: episode '%s' (row %s) failed — %s",
                        episode_title,
                        idx,
                        exc,
                        exc_info=True,
                    )
                    self._write_failure_log(episode_title, source_text, exc)

                # Load audio into memory if requested
                file_data: Optional[BytesIO] = None
                if podcast_path and self.as_bytes:
                    import aiofiles
                    try:
                        async with aiofiles.open(podcast_path, "rb") as fh:
                            file_data = BytesIO(await fh.read())
                        self.logger.debug(
                            "PodcastMaker: loaded '%s' into memory (%d bytes)",
                            Path(podcast_path).name,
                            file_data.getbuffer().nbytes,
                        )
                    except OSError as read_err:
                        self.logger.warning(
                            "PodcastMaker: could not read %s into memory — %s",
                            podcast_path, read_err,
                        )

                result_row = row.to_dict()
                result_row[self.output_column] = source_text
                result_row["podcast_path"] = podcast_path
                result_row["script_path"] = script_path
                result_row["podcast_error"] = podcast_error
                if self.as_bytes:
                    result_row["file_data"] = file_data
                    result_row["content_type"] = "audio/wav"
                    # UploadToS3 uses downloaded_filename to identify each row
                    result_row["downloaded_filename"] = (
                        Path(podcast_path).name if podcast_path else None
                    )
                results.append(result_row)

        df = pd.DataFrame(results)
        # Guarantee podcast_error column is always present even if all rows succeeded
        if "podcast_error" not in df.columns:
            df["podcast_error"] = None

        self._result = df
        self.add_metric("NUMROWS", len(self._result))
        self.add_metric("NUMCOLS", len(self._result.columns))

        if self._debug:
            self._print_data_(self._result, "PodcastMaker Result")

        return self._result
