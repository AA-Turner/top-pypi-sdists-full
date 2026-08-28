"""Read the three uploaded files from an app folder, turning every failure into data.

The contract of this module is that it **never raises**. A malformed ``widgets.json`` must not
prevent the rest of the suite from running and reporting on everything else — the same reasoning as
:func:`~matrice_analytics.engine.testing.generate._resolve_app`, which turns a manifest load failure
into a :class:`CheckResult` rather than an exception.

Error messages deliberately echo the ones the real upload path produces, so an author who hits a
failure here recognises it when fe-market rejects the same file.
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from matrice_analytics.engine.appconfig.models import (
    METRICS_FILENAME,
    POST_PROCESSING_FILENAME,
    WIDGETS_FILENAME,
    ConfigProblem,
    MetricEntry,
    PostProcessingConfig,
    WidgetEntry,
)

logger = logging.getLogger(__name__)

__all__ = ["AppConfigBundle", "load_app_config"]


@dataclass(frozen=True)
class AppConfigBundle:
    """The three sibling files as parsed, plus everything wrong with them.

    A ``None`` collection means the file was absent or could not be parsed at all — distinct from
    an empty tuple, which means the file was a well-formed empty array.
    """

    root: Path
    metrics: tuple[MetricEntry, ...] | None = None
    widgets: tuple[WidgetEntry, ...] | None = None
    post_processing: PostProcessingConfig | None = None
    problems: tuple[ConfigProblem, ...] = ()
    #: Filenames that are simply not on disk. Not a problem in itself — the caller decides.
    missing: tuple[str, ...] = ()

    @property
    def all_present(self) -> bool:
        return not self.missing

    @property
    def none_present(self) -> bool:
        return len(self.missing) == 3

    @property
    def errors(self) -> tuple[ConfigProblem, ...]:
        return tuple(problem for problem in self.problems if problem.severity == "error")

    @property
    def warnings(self) -> tuple[ConfigProblem, ...]:
        return tuple(problem for problem in self.problems if problem.severity == "warning")

    @property
    def metric_keys(self) -> frozenset[str]:
        return frozenset(entry.key for entry in self.metrics or ())


def load_app_config(root: str | Path) -> AppConfigBundle:
    """Parse ``metrics.json``, ``widgets.json`` and ``post_processing_config.json`` from a folder."""
    folder = Path(root)
    problems: list[ConfigProblem] = []
    missing: list[str] = []

    metrics = _load_array(folder / METRICS_FILENAME, MetricEntry, problems, missing)
    widgets = _load_array(folder / WIDGETS_FILENAME, WidgetEntry, problems, missing)
    post_processing = _load_post_processing(folder / POST_PROCESSING_FILENAME, problems, missing)

    return AppConfigBundle(
        root=folder,
        metrics=metrics,
        widgets=widgets,
        post_processing=post_processing,
        problems=tuple(problems),
        missing=tuple(missing),
    )


def _read_json(path: Path, problems: list[ConfigProblem], missing: list[str]) -> Any:
    """Return the decoded JSON, or :data:`_ABSENT` / :data:`_BROKEN` sentinels."""
    if not path.is_file():
        missing.append(path.name)
        return _ABSENT

    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        problems.append(ConfigProblem(path.name, f"could not be read as UTF-8 text: {exc}"))
        return _BROKEN

    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        problems.append(
            ConfigProblem(path.name, f"is not valid JSON: {exc.msg} (line {exc.lineno}, column {exc.colno})")
        )
        return _BROKEN


class _Sentinel:
    __slots__ = ("_name",)

    def __init__(self, name: str) -> None:
        self._name = name

    def __repr__(self) -> str:  # pragma: no cover - debugging aid
        return self._name


_ABSENT = _Sentinel("<absent>")
_BROKEN = _Sentinel("<broken>")


def _load_array(
    path: Path,
    model: type[MetricEntry] | type[WidgetEntry],
    problems: list[ConfigProblem],
    missing: list[str],
) -> tuple[Any, ...] | None:
    raw = _read_json(path, problems, missing)
    if isinstance(raw, _Sentinel):
        return None

    if not isinstance(raw, list):
        # The wording is the upload path's own, so the failure is recognisable in both places.
        problems.append(
            ConfigProblem(
                path.name,
                f"must contain a JSON array; found {type(raw).__name__}. Wrapping the array in an "
                f"object is the usual cause and the upload rejects it too.",
            )
        )
        return None

    entries: list[Any] = []
    for index, item in enumerate(raw):
        where = f"{path.name}[{index}]"
        if not isinstance(item, dict):
            problems.append(ConfigProblem(where, f"must be an object; found {type(item).__name__}"))
            continue
        try:
            entry = model.model_validate(item)
        except ValidationError as exc:
            problems.append(ConfigProblem(where, _format_validation_error(exc)))
            continue
        _warn_on_extra_keys(entry, where, problems)
        entries.append(entry)

    return tuple(entries)


def _load_post_processing(path: Path, problems: list[ConfigProblem], missing: list[str]) -> PostProcessingConfig | None:
    raw = _read_json(path, problems, missing)
    if isinstance(raw, _Sentinel):
        return None

    if isinstance(raw, list):
        # `parsePostProcessing` takes element 0 and discards the rest without saying so
        # (version-form.tsx:268-275). Mirroring that silently would hide a real mistake.
        if not raw:
            problems.append(ConfigProblem(path.name, "is an empty array; it must be a JSON object"))
            return None
        problems.append(
            ConfigProblem(
                path.name,
                f"is an array of {len(raw)}; the upload reads only element 0 and discards the rest. "
                f"Make it a JSON object.",
                severity="warning",
            )
        )
        raw = raw[0]

    if not isinstance(raw, dict):
        problems.append(ConfigProblem(path.name, f"must be a JSON object; found {type(raw).__name__}"))
        return None

    try:
        config = PostProcessingConfig.model_validate(raw)
    except ValidationError as exc:
        problems.append(ConfigProblem(path.name, _format_validation_error(exc)))
        return None

    return config


def _warn_on_extra_keys(entry: MetricEntry | WidgetEntry, where: str, problems: list[ConfigProblem]) -> None:
    extra = entry.extra_keys()
    if not extra:
        return
    problems.append(
        ConfigProblem(
            where,
            f"has key(s) the platform does not read: {', '.join(repr(key) for key in extra)}. "
            f"They are stored verbatim and ship to production.",
            severity="warning",
        )
    )


def _format_validation_error(exc: ValidationError) -> str:
    parts = []
    for error in exc.errors():
        location = ".".join(str(item) for item in error["loc"]) or "(root)"
        parts.append(f"{location}: {error['msg']}")
    return "; ".join(parts)
