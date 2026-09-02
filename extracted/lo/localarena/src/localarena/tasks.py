"""Prompt tasks and deterministic scoring for live evaluations."""

from __future__ import annotations

import json
import math
import re
import unicodedata
from collections import Counter
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from typing import Protocol

from .generation import (
    ChatMessage,
    GenerationResult,
    _freeze_json,
    _freeze_json_object,
    _thaw_json,
)


def _non_empty_string(value: object, field_name: str) -> str:
    if type(value) is not str:
        raise TypeError(f"{field_name} must be a string")
    if not value.strip():
        raise ValueError(f"{field_name} must not be empty or whitespace")
    return value


def _message_dict(message: ChatMessage) -> dict[str, str]:
    return {"role": message.role, "content": message.content}


@dataclass(frozen=True, slots=True)
class Score:
    """A normalized task score.

    ``value`` is always in the inclusive ``0..1`` range. ``passed`` is kept
    separate because some rubric scores are meaningful without a binary pass
    threshold.
    """

    value: float
    passed: bool | None = None
    reason: str = ""
    metadata: Mapping[str, object] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if type(self.value) not in (int, float):
            raise TypeError("value must be a number")
        normalized = float(self.value)
        if not math.isfinite(normalized) or not 0 <= normalized <= 1:
            raise ValueError("value must be finite and between zero and one")
        if self.passed is not None and type(self.passed) is not bool:
            raise TypeError("passed must be a boolean or None")
        if type(self.reason) is not str:
            raise TypeError("reason must be a string")
        object.__setattr__(self, "value", normalized)
        object.__setattr__(
            self,
            "metadata",
            _freeze_json_object(self.metadata, field_name="metadata"),
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "value": self.value,
            "passed": self.passed,
            "reason": self.reason,
            "metadata": _thaw_json(self.metadata),
        }

    def __deepcopy__(self, memo: dict[int, object]) -> Score:
        memo[id(self)] = self
        return self

    @classmethod
    def from_dict(cls, value: Mapping[str, object]) -> Score:
        return cls(
            value=value["value"],  # type: ignore[arg-type]
            passed=value.get("passed"),  # type: ignore[arg-type]
            reason=value.get("reason", ""),  # type: ignore[arg-type]
            metadata=value.get("metadata", {}),  # type: ignore[arg-type]
        )


class Evaluator(Protocol):
    """Score one generated answer for one prompt task."""

    @property
    def name(self) -> str:
        ...

    def evaluate(
        self,
        task: PromptTask,
        generation: GenerationResult,
    ) -> Score:
        ...

    def to_config(self) -> dict[str, object]:
        ...


@dataclass(frozen=True, slots=True)
class PromptTask:
    """One provider-independent prompt and its optional scoring rule."""

    id: str
    messages: tuple[ChatMessage, ...]
    evaluator: Evaluator | None = None
    metadata: Mapping[str, object] = field(default_factory=dict)
    _evaluator_config: Mapping[str, object] | None = field(
        init=False,
        repr=False,
        compare=False,
    )

    def __post_init__(self) -> None:
        object.__setattr__(self, "id", _non_empty_string(self.id, "id"))
        if isinstance(self.messages, (str, bytes, bytearray)):
            raise TypeError("messages must be a sequence of ChatMessage values")
        messages = tuple(self.messages)
        if not messages:
            raise ValueError("messages must not be empty")
        if not all(isinstance(message, ChatMessage) for message in messages):
            raise TypeError("messages must contain only ChatMessage values")
        object.__setattr__(self, "messages", messages)
        if self.evaluator is None:
            evaluator_config = None
        else:
            if (
                not callable(getattr(self.evaluator, "evaluate", None))
                or not callable(getattr(self.evaluator, "to_config", None))
            ):
                raise TypeError(
                    "evaluator must implement evaluate() and to_config()"
                )
            evaluator_name = getattr(self.evaluator, "name", None)
            if type(evaluator_name) is not str or not evaluator_name:
                raise TypeError("evaluator.name must be a non-empty string")
            config = self.evaluator.to_config()
            if not isinstance(config, Mapping):
                raise TypeError("evaluator.to_config() must return a mapping")
            evaluator_config = _freeze_json_object(
                config,
                field_name="evaluator config",
            )
            if evaluator_config.get("type") != evaluator_name:
                raise ValueError(
                    "evaluator config type must match evaluator.name"
                )
        object.__setattr__(self, "_evaluator_config", evaluator_config)
        object.__setattr__(
            self,
            "metadata",
            _freeze_json_object(self.metadata, field_name="metadata"),
        )

    @classmethod
    def from_text(
        cls,
        id: str,
        prompt: str,
        *,
        system: str | None = None,
        evaluator: Evaluator | None = None,
        metadata: Mapping[str, object] | None = None,
    ) -> PromptTask:
        messages: list[ChatMessage] = []
        if system is not None:
            messages.append(ChatMessage("system", system))
        messages.append(ChatMessage("user", prompt))
        return cls(
            id=id,
            messages=tuple(messages),
            evaluator=evaluator,
            metadata=metadata or {},
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "id": self.id,
            "messages": [_message_dict(message) for message in self.messages],
            "evaluator": (
                _thaw_json(self._evaluator_config)
                if self._evaluator_config is not None
                else None
            ),
            "metadata": _thaw_json(self.metadata),
        }

    def __deepcopy__(self, memo: dict[int, object]) -> PromptTask:
        memo[id(self)] = self
        return self


def _normalize_text(
    value: str,
    *,
    strip: bool,
    ignore_case: bool,
) -> str:
    if strip:
        value = value.strip()
    if ignore_case:
        value = value.casefold()
    return value


def _references(
    value: str | Sequence[str],
    *,
    field_name: str = "expected",
    allow_string: bool = True,
) -> tuple[str, ...]:
    if isinstance(value, str) and allow_string:
        references = (value,)
    elif isinstance(value, Sequence) and not isinstance(
        value,
        (str, bytes, bytearray),
    ):
        references = tuple(value)
    else:
        expected_type = "a string or sequence" if allow_string else "a sequence"
        raise TypeError(f"{field_name} must be {expected_type} of strings")
    if not references:
        raise ValueError(f"{field_name} must contain one or more strings")
    for index, reference in enumerate(references):
        _non_empty_string(reference, f"{field_name}[{index}]")
    return references


@dataclass(frozen=True, slots=True)
class ExactMatch:
    """Pass when the complete generated text matches ``expected``."""

    expected: str
    strip: bool = True
    ignore_case: bool = False

    def __post_init__(self) -> None:
        if type(self.expected) is not str:
            raise TypeError("expected must be a string")
        if type(self.strip) is not bool or type(self.ignore_case) is not bool:
            raise TypeError("strip and ignore_case must be booleans")

    @property
    def name(self) -> str:
        return "exact"

    def evaluate(
        self,
        task: PromptTask,
        generation: GenerationResult,
    ) -> Score:
        del task
        actual = _normalize_text(
            generation.text,
            strip=self.strip,
            ignore_case=self.ignore_case,
        )
        expected = _normalize_text(
            self.expected,
            strip=self.strip,
            ignore_case=self.ignore_case,
        )
        passed = actual == expected
        return Score(
            1 if passed else 0,
            passed=passed,
            reason="exact match" if passed else "answer did not exactly match",
        )

    def to_config(self) -> dict[str, object]:
        return {
            "type": self.name,
            "expected": self.expected,
            "strip": self.strip,
            "ignore_case": self.ignore_case,
        }


@dataclass(frozen=True, slots=True)
class Match:
    """Match generated text against any accepted reference."""

    expected: str | Sequence[str]
    mode: str = "exact"
    strip: bool = True
    ignore_case: bool = False

    def __post_init__(self) -> None:
        references = _references(self.expected)
        if self.mode not in ("exact", "begin", "end", "any"):
            raise ValueError("mode must be 'exact', 'begin', 'end', or 'any'")
        if type(self.strip) is not bool or type(self.ignore_case) is not bool:
            raise TypeError("strip and ignore_case must be booleans")
        object.__setattr__(self, "expected", references)

    @property
    def name(self) -> str:
        return "match"

    def evaluate(
        self,
        task: PromptTask,
        generation: GenerationResult,
    ) -> Score:
        del task
        actual = _normalize_text(
            generation.text,
            strip=self.strip,
            ignore_case=self.ignore_case,
        )
        references = tuple(
            _normalize_text(
                reference,
                strip=self.strip,
                ignore_case=self.ignore_case,
            )
            for reference in self.expected
        )
        if self.mode == "exact":
            passed = any(actual == reference for reference in references)
        elif self.mode == "begin":
            passed = any(
                actual.startswith(reference) for reference in references
            )
        elif self.mode == "end":
            passed = any(actual.endswith(reference) for reference in references)
        else:
            passed = any(reference in actual for reference in references)
        return Score(
            1 if passed else 0,
            passed=passed,
            reason=(
                f"{self.mode} match"
                if passed
                else f"answer did not satisfy {self.mode} match"
            ),
        )

    def to_config(self) -> dict[str, object]:
        return {
            "type": self.name,
            "expected": list(self.expected),
            "mode": self.mode,
            "strip": self.strip,
            "ignore_case": self.ignore_case,
        }


# The package root already uses ``Match`` for an arena match record.
# ``TextMatch`` is the unambiguous public name for this evaluator.
TextMatch = Match


def _normalized_choice(value: str, *, ignore_case: bool) -> str:
    return _normalize_text(value, strip=False, ignore_case=ignore_case)


def _is_choice_word_character(value: str) -> bool:
    category = unicodedata.category(value)
    return (
        category[0] in {"L", "M", "N"}
        or category == "Pc"
        or value in {"\u200c", "\u200d"}
    )


def _leading_choice(
    value: str,
    choices: Sequence[str],
    *,
    ignore_case: bool,
) -> str | None:
    source = value.lstrip()
    candidates = [source]
    if source and source[0] in "([{":
        candidates.append(source[1:].lstrip())
    normalized_choices = sorted(
        (
            (_normalized_choice(choice, ignore_case=ignore_case), choice)
            for choice in choices
        ),
        key=lambda item: len(item[0]),
        reverse=True,
    )
    for candidate in candidates:
        normalized = _normalized_choice(candidate, ignore_case=ignore_case)
        for label, original in normalized_choices:
            if not normalized.startswith(label):
                continue
            remainder = normalized[len(label) :]
            if not remainder or not _is_choice_word_character(remainder[0]):
                return original
    return None


@dataclass(frozen=True, slots=True)
class ChoiceMatch:
    """Match a boundary-safe choice label at the start of the answer."""

    expected: Sequence[str]
    choices: Sequence[str]
    ignore_case: bool = True

    def __post_init__(self) -> None:
        expected = _references(self.expected, allow_string=False)
        choices = _references(
            self.choices,
            field_name="choices",
            allow_string=False,
        )
        if type(self.ignore_case) is not bool:
            raise TypeError("ignore_case must be a boolean")
        normalized_choices = tuple(
            _normalized_choice(choice, ignore_case=self.ignore_case)
            for choice in choices
        )
        if len(set(normalized_choices)) != len(normalized_choices):
            raise ValueError("choices must be unique after normalization")
        allowed = set(normalized_choices)
        normalized_expected = tuple(
            _normalized_choice(reference, ignore_case=self.ignore_case)
            for reference in expected
        )
        if len(set(normalized_expected)) != len(normalized_expected):
            raise ValueError("expected must be unique after normalization")
        if any(reference not in allowed for reference in normalized_expected):
            raise ValueError("expected choice labels must occur in choices")
        object.__setattr__(self, "expected", expected)
        object.__setattr__(self, "choices", choices)

    @property
    def name(self) -> str:
        return "choice"

    def evaluate(
        self,
        task: PromptTask,
        generation: GenerationResult,
    ) -> Score:
        del task
        choice = _leading_choice(
            generation.text,
            self.choices,
            ignore_case=self.ignore_case,
        )
        normalized_expected = {
            _normalized_choice(reference, ignore_case=self.ignore_case)
            for reference in self.expected
        }
        passed = (
            choice is not None
            and _normalized_choice(choice, ignore_case=self.ignore_case)
            in normalized_expected
        )
        metadata: dict[str, object] = {}
        if choice is not None:
            metadata["choice"] = choice
        return Score(
            1 if passed else 0,
            passed=passed,
            reason=(
                "leading choice matched"
                if passed
                else (
                    "leading choice did not match"
                    if choice is not None
                    else "no leading choice found"
                )
            ),
            metadata=metadata,
        )

    def to_config(self) -> dict[str, object]:
        return {
            "type": self.name,
            "expected": list(self.expected),
            "choices": list(self.choices),
            "ignore_case": self.ignore_case,
        }


@dataclass(frozen=True, slots=True)
class ExtractMatch:
    """Extract a regular-expression capture and match any reference."""

    expected: str | Sequence[str]
    pattern: str
    group: int = 1
    strip: bool = True
    ignore_case: bool = False

    def __post_init__(self) -> None:
        references = _references(self.expected)
        _non_empty_string(self.pattern, "pattern")
        if type(self.group) is not int or self.group < 0:
            raise TypeError("group must be a non-negative integer")
        if type(self.strip) is not bool or type(self.ignore_case) is not bool:
            raise TypeError("strip and ignore_case must be booleans")
        re.compile(self.pattern, re.IGNORECASE if self.ignore_case else 0)
        object.__setattr__(self, "expected", references)

    @property
    def name(self) -> str:
        return "extract"

    def evaluate(
        self,
        task: PromptTask,
        generation: GenerationResult,
    ) -> Score:
        del task
        expression = re.compile(
            self.pattern,
            re.IGNORECASE if self.ignore_case else 0,
        )
        match = expression.search(generation.text)
        if match is None:
            return Score(
                0,
                passed=False,
                reason="extraction pattern did not match",
            )
        try:
            extracted = match.group(self.group)
        except IndexError:
            extracted = None
        if extracted is None:
            return Score(
                0,
                passed=False,
                reason="extraction capture group was unavailable",
            )
        actual = _normalize_text(
            extracted,
            strip=self.strip,
            ignore_case=self.ignore_case,
        )
        passed = any(
            actual
            == _normalize_text(
                reference,
                strip=self.strip,
                ignore_case=self.ignore_case,
            )
            for reference in self.expected
        )
        return Score(
            1 if passed else 0,
            passed=passed,
            reason=(
                "extracted answer matched"
                if passed
                else "extracted answer did not match"
            ),
        )

    def to_config(self) -> dict[str, object]:
        return {
            "type": self.name,
            "expected": list(self.expected),
            "pattern": self.pattern,
            "group": self.group,
            "strip": self.strip,
            "ignore_case": self.ignore_case,
        }


def _token_f1(
    actual: Sequence[str],
    expected: Sequence[str],
) -> tuple[float, float, float]:
    if not actual or not expected:
        return 0.0, 0.0, 0.0
    overlap = sum((Counter(actual) & Counter(expected)).values())
    precision = overlap / len(actual)
    recall = overlap / len(expected)
    if overlap == 0:
        return 0.0, precision, recall
    return 2 * precision * recall / (precision + recall), precision, recall


_TOKEN_WHITESPACE = re.compile(
    "[\u0009-\u000d\u0020\u0085\u00a0\u1680"
    "\u2000-\u200a\u2028\u2029\u202f\u205f\u3000]+"
)


@dataclass(frozen=True, slots=True)
class TokenF1:
    """Score whitespace-token F1 against the best accepted reference."""

    expected: str | Sequence[str]
    threshold: float = 1
    ignore_case: bool = True

    def __post_init__(self) -> None:
        references = _references(self.expected)
        if (
            type(self.threshold) not in (int, float)
            or not math.isfinite(float(self.threshold))
        ):
            raise TypeError("threshold must be a finite number")
        if not 0 <= self.threshold <= 1:
            raise ValueError("threshold must be between zero and one")
        if type(self.ignore_case) is not bool:
            raise TypeError("ignore_case must be a boolean")
        object.__setattr__(self, "expected", references)
        object.__setattr__(self, "threshold", float(self.threshold))

    @property
    def name(self) -> str:
        return "token_f1"

    def evaluate(
        self,
        task: PromptTask,
        generation: GenerationResult,
    ) -> Score:
        del task

        def tokenize(value: str) -> tuple[str, ...]:
            normalized = _normalize_text(
                value,
                strip=False,
                ignore_case=self.ignore_case,
            )
            return tuple(
                token for token in _TOKEN_WHITESPACE.split(normalized) if token
            )

        actual = tokenize(generation.text)
        best_f1 = 0.0
        best_precision = 0.0
        best_recall = 0.0
        best_reference = 0
        for index, reference in enumerate(self.expected):
            f1, precision, recall = _token_f1(actual, tokenize(reference))
            if f1 > best_f1:
                best_f1 = f1
                best_precision = precision
                best_recall = recall
                best_reference = index
        passed = best_f1 >= self.threshold
        return Score(
            best_f1,
            passed=passed,
            reason=(
                "token F1 met threshold"
                if passed
                else "token F1 did not meet threshold"
            ),
            metadata={
                "precision": best_precision,
                "recall": best_recall,
                "reference_index": best_reference,
                "threshold": self.threshold,
            },
        )

    def to_config(self) -> dict[str, object]:
        return {
            "type": self.name,
            "expected": list(self.expected),
            "threshold": self.threshold,
            "ignore_case": self.ignore_case,
        }


@dataclass(frozen=True, slots=True)
class Contains:
    """Pass when all or any required strings occur in the answer."""

    expected: str | Sequence[str]
    mode: str = "all"
    ignore_case: bool = False

    def __post_init__(self) -> None:
        if isinstance(self.expected, str):
            values = (self.expected,)
        elif isinstance(self.expected, Sequence):
            values = tuple(self.expected)
        else:
            raise TypeError("expected must be a string or sequence of strings")
        if not values or not all(type(value) is str and value for value in values):
            raise ValueError("expected must contain one or more non-empty strings")
        if self.mode not in ("all", "any"):
            raise ValueError("mode must be 'all' or 'any'")
        if type(self.ignore_case) is not bool:
            raise TypeError("ignore_case must be a boolean")
        object.__setattr__(self, "expected", values)

    @property
    def name(self) -> str:
        return "contains"

    def evaluate(
        self,
        task: PromptTask,
        generation: GenerationResult,
    ) -> Score:
        del task
        haystack = (
            generation.text.casefold()
            if self.ignore_case
            else generation.text
        )
        needles = tuple(
            value.casefold() if self.ignore_case else value
            for value in self.expected
        )
        matches = tuple(needle in haystack for needle in needles)
        passed = all(matches) if self.mode == "all" else any(matches)
        matched = sum(matches)
        return Score(
            1 if passed else 0,
            passed=passed,
            reason=f"matched {matched} of {len(matches)} required strings",
            metadata={"matched": matched, "total": len(matches)},
        )

    def to_config(self) -> dict[str, object]:
        return {
            "type": self.name,
            "expected": list(self.expected),
            "mode": self.mode,
            "ignore_case": self.ignore_case,
        }


@dataclass(frozen=True, slots=True)
class RegexMatch:
    """Pass when a regular expression matches the generated text."""

    pattern: str
    ignore_case: bool = False
    full_match: bool = False

    def __post_init__(self) -> None:
        _non_empty_string(self.pattern, "pattern")
        if type(self.ignore_case) is not bool or type(self.full_match) is not bool:
            raise TypeError("ignore_case and full_match must be booleans")
        re.compile(self.pattern, re.IGNORECASE if self.ignore_case else 0)

    @property
    def name(self) -> str:
        return "regex"

    def evaluate(
        self,
        task: PromptTask,
        generation: GenerationResult,
    ) -> Score:
        del task
        expression = re.compile(
            self.pattern,
            re.IGNORECASE if self.ignore_case else 0,
        )
        match = (
            expression.fullmatch(generation.text)
            if self.full_match
            else expression.search(generation.text)
        )
        passed = match is not None
        return Score(
            1 if passed else 0,
            passed=passed,
            reason="regular expression matched"
            if passed
            else "regular expression did not match",
        )

    def to_config(self) -> dict[str, object]:
        return {
            "type": self.name,
            "pattern": self.pattern,
            "ignore_case": self.ignore_case,
            "full_match": self.full_match,
        }


@dataclass(frozen=True, slots=True)
class JsonMatch:
    """Validate JSON, and optionally compare it to an expected JSON value."""

    expected: object = field(default=None)
    compare: bool = False

    @property
    def name(self) -> str:
        return "json"

    def __post_init__(self) -> None:
        if type(self.compare) is not bool:
            raise TypeError("compare must be a boolean")
        if self.compare:
            try:
                normalized = json.loads(
                    json.dumps(self.expected, allow_nan=False)
                )
            except (TypeError, ValueError) as error:
                raise TypeError("expected must be a JSON value") from error
            object.__setattr__(self, "expected", _freeze_json(normalized))

    def evaluate(
        self,
        task: PromptTask,
        generation: GenerationResult,
    ) -> Score:
        del task
        try:
            actual = json.loads(
                generation.text,
                parse_constant=_reject_json_constant,
                object_pairs_hook=_unique_json_object,
            )
        except (json.JSONDecodeError, ValueError) as error:
            if isinstance(error, json.JSONDecodeError):
                reason = (
                    f"invalid JSON at line {error.lineno}, "
                    f"column {error.colno}"
                )
            else:
                reason = str(error)
            return Score(
                0,
                passed=False,
                reason=reason,
            )
        passed = not self.compare or _json_equal(
            actual,
            _thaw_json(self.expected),
        )
        return Score(
            1 if passed else 0,
            passed=passed,
            reason="valid JSON"
            if not self.compare
            else ("JSON matched" if passed else "JSON did not match"),
        )

    def to_config(self) -> dict[str, object]:
        config: dict[str, object] = {
            "type": self.name,
            "compare": self.compare,
        }
        if self.compare:
            config["expected"] = _thaw_json(self.expected)
        return config


def _reject_json_constant(value: str) -> object:
    raise ValueError(f"invalid JSON constant {value}")


def _unique_json_object(
    pairs: list[tuple[str, object]],
) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key {key!r}")
        result[key] = value
    return result


def _json_equal(left: object, right: object) -> bool:
    if type(left) is bool or type(right) is bool:
        return type(left) is bool and type(right) is bool and left == right
    if type(left) in (int, float) and type(right) in (int, float):
        return left == right
    if left is None or right is None:
        return left is None and right is None
    if type(left) is str or type(right) is str:
        return type(left) is str and type(right) is str and left == right
    if isinstance(left, list) or isinstance(right, list):
        return (
            isinstance(left, list)
            and isinstance(right, list)
            and len(left) == len(right)
            and all(
                _json_equal(left_item, right_item)
                for left_item, right_item in zip(left, right)
            )
        )
    if isinstance(left, Mapping) or isinstance(right, Mapping):
        return (
            isinstance(left, Mapping)
            and isinstance(right, Mapping)
            and set(left) == set(right)
            and all(_json_equal(left[key], right[key]) for key in left)
        )
    return False


@dataclass(frozen=True, slots=True)
class NumericMatch:
    """Pass when the answer is within ``tolerance`` of a numeric target."""

    expected: float
    tolerance: float = 0

    def __post_init__(self) -> None:
        for field_name in ("expected", "tolerance"):
            value = getattr(self, field_name)
            if type(value) not in (int, float) or not math.isfinite(float(value)):
                raise TypeError(f"{field_name} must be a finite number")
        if self.tolerance < 0:
            raise ValueError("tolerance must not be negative")
        object.__setattr__(self, "expected", float(self.expected))
        object.__setattr__(self, "tolerance", float(self.tolerance))

    @property
    def name(self) -> str:
        return "numeric"

    def evaluate(
        self,
        task: PromptTask,
        generation: GenerationResult,
    ) -> Score:
        del task
        try:
            actual = float(generation.text.strip())
        except ValueError:
            return Score(0, passed=False, reason="answer was not a number")
        if not math.isfinite(actual):
            return Score(0, passed=False, reason="answer was not finite")
        difference = abs(actual - self.expected)
        passed = difference <= self.tolerance
        return Score(
            1 if passed else 0,
            passed=passed,
            reason=(
                "numeric answer matched"
                if passed
                else f"absolute error {difference:g} exceeded tolerance"
            ),
            metadata={"actual": actual, "absolute_error": difference},
        )

    def to_config(self) -> dict[str, object]:
        return {
            "type": self.name,
            "expected": self.expected,
            "tolerance": self.tolerance,
        }


def evaluator_from_config(config: Mapping[str, object] | None) -> Evaluator | None:
    """Build a deterministic evaluator from a JSON configuration object."""

    if config is None:
        return None
    if not isinstance(config, Mapping):
        raise TypeError("evaluator must be an object or null")
    evaluator_type = config.get("type")
    if evaluator_type == "none":
        _require_config_keys(config, {"type"}, "none evaluator")
        return None
    if type(evaluator_type) is not str:
        raise TypeError("evaluator.type must be a string")
    if evaluator_type == "exact":
        _require_config_keys(
            config,
            {"type", "expected", "strip", "ignore_case"},
            "exact evaluator",
        )
        return ExactMatch(
            expected=_required(config, "expected", "exact evaluator"),  # type: ignore[arg-type]
            strip=config.get("strip", True),  # type: ignore[arg-type]
            ignore_case=config.get("ignore_case", False),  # type: ignore[arg-type]
        )
    if evaluator_type == "contains":
        _require_config_keys(
            config,
            {"type", "expected", "mode", "ignore_case"},
            "contains evaluator",
        )
        return Contains(
            expected=_required(config, "expected", "contains evaluator"),  # type: ignore[arg-type]
            mode=config.get("mode", "all"),  # type: ignore[arg-type]
            ignore_case=config.get("ignore_case", False),  # type: ignore[arg-type]
        )
    if evaluator_type == "match":
        _require_config_keys(
            config,
            {"type", "expected", "mode", "strip", "ignore_case"},
            "match evaluator",
        )
        return Match(
            expected=_required(config, "expected", "match evaluator"),  # type: ignore[arg-type]
            mode=config.get("mode", "exact"),  # type: ignore[arg-type]
            strip=config.get("strip", True),  # type: ignore[arg-type]
            ignore_case=config.get("ignore_case", False),  # type: ignore[arg-type]
        )
    if evaluator_type == "choice":
        _require_config_keys(
            config,
            {"type", "expected", "choices", "ignore_case"},
            "choice evaluator",
        )
        return ChoiceMatch(
            expected=_required(config, "expected", "choice evaluator"),  # type: ignore[arg-type]
            choices=_required(config, "choices", "choice evaluator"),  # type: ignore[arg-type]
            ignore_case=config.get("ignore_case", True),  # type: ignore[arg-type]
        )
    if evaluator_type == "extract":
        _require_config_keys(
            config,
            {
                "type",
                "expected",
                "pattern",
                "group",
                "strip",
                "ignore_case",
            },
            "extract evaluator",
        )
        return ExtractMatch(
            expected=_required(config, "expected", "extract evaluator"),  # type: ignore[arg-type]
            pattern=_required(config, "pattern", "extract evaluator"),  # type: ignore[arg-type]
            group=config.get("group", 1),  # type: ignore[arg-type]
            strip=config.get("strip", True),  # type: ignore[arg-type]
            ignore_case=config.get("ignore_case", False),  # type: ignore[arg-type]
        )
    if evaluator_type == "token_f1":
        _require_config_keys(
            config,
            {"type", "expected", "threshold", "ignore_case"},
            "token_f1 evaluator",
        )
        return TokenF1(
            expected=_required(config, "expected", "token_f1 evaluator"),  # type: ignore[arg-type]
            threshold=config.get("threshold", 1),  # type: ignore[arg-type]
            ignore_case=config.get("ignore_case", True),  # type: ignore[arg-type]
        )
    if evaluator_type == "regex":
        _require_config_keys(
            config,
            {"type", "pattern", "ignore_case", "full_match"},
            "regex evaluator",
        )
        return RegexMatch(
            pattern=_required(config, "pattern", "regex evaluator"),  # type: ignore[arg-type]
            ignore_case=config.get("ignore_case", False),  # type: ignore[arg-type]
            full_match=config.get("full_match", False),  # type: ignore[arg-type]
        )
    if evaluator_type == "json":
        _require_config_keys(
            config,
            {"type", "expected", "compare"},
            "json evaluator",
        )
        return JsonMatch(
            expected=config.get("expected"),
            compare=config.get("compare", "expected" in config),  # type: ignore[arg-type]
        )
    if evaluator_type == "numeric":
        _require_config_keys(
            config,
            {"type", "expected", "tolerance"},
            "numeric evaluator",
        )
        return NumericMatch(
            expected=_required(config, "expected", "numeric evaluator"),  # type: ignore[arg-type]
            tolerance=config.get("tolerance", 0),  # type: ignore[arg-type]
        )
    raise ValueError(f"unsupported evaluator type: {evaluator_type!r}")


def _require_config_keys(
    config: Mapping[str, object],
    allowed: set[str],
    field_name: str,
) -> None:
    extra = sorted(set(config) - allowed)
    if extra:
        raise ValueError(
            f"{field_name} contains unsupported fields: {', '.join(extra)}"
        )


def _required(
    config: Mapping[str, object],
    key: str,
    field_name: str,
) -> object:
    if key not in config:
        raise ValueError(f"{field_name} requires {key}")
    return config[key]
