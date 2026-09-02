"""Core data structures and pairwise ranking logic for :mod:`localarena`."""

from __future__ import annotations

import json
import math
from collections.abc import Iterable, Iterator, Mapping
from dataclasses import dataclass, field
from enum import Enum
from itertools import combinations
from types import MappingProxyType
from typing import Any, TypedDict

SCHEMA_VERSION = 1
_MAX_SAFE_INTEGER = (1 << 53) - 1
_MAX_METADATA_DEPTH = 100
_BT_SCALE = 400.0
_BT_EDGE_PRIOR = 1.0
_BT_MAX_ITERATIONS = 200
_BT_TOLERANCE = 1e-6
_BT_LINE_SEARCH_FLOOR = 2.0**-40
_UINT32_MASK = (1 << 32) - 1


class Result(str, Enum):
    """The outcome of a match, expressed relative to its two sides."""

    LEFT = "left"
    RIGHT = "right"
    DRAW = "draw"

    def __str__(self) -> str:
        return self.value


class _FrozenDict(Mapping[str, object]):
    """A recursively immutable mapping used by public records."""

    __slots__ = ("__data",)

    def __init__(self, data: Mapping[str, object]) -> None:
        object.__setattr__(
            self,
            "_FrozenDict__data",
            MappingProxyType(dict(data)),
        )

    def __getitem__(self, key: str) -> object:
        return self.__data[key]

    def __iter__(self) -> Iterator[str]:
        return iter(self.__data)

    def __len__(self) -> int:
        return len(self.__data)

    def __repr__(self) -> str:
        return repr(self.__data)

    def __setattr__(self, name: str, value: object) -> None:
        raise TypeError("metadata is immutable")

    def __deepcopy__(self, memo: dict[int, object]) -> _FrozenDict:
        return self


def _validate_name(name: object, *, field_name: str = "name") -> str:
    if type(name) is not str:
        raise TypeError(f"{field_name} must be a string")
    if not name.strip():
        raise ValueError(f"{field_name} must not be empty or whitespace")
    return name


def _normalize_json(
    value: object,
    *,
    path: str,
    active: set[int],
    depth: int,
) -> object:
    if depth > _MAX_METADATA_DEPTH:
        raise ValueError(
            f"{path} exceeds the maximum metadata depth of {_MAX_METADATA_DEPTH}"
        )

    if value is None or type(value) is bool:
        return value
    if isinstance(value, str):
        return str(value)
    if type(value) is int:
        if abs(value) > _MAX_SAFE_INTEGER:
            raise ValueError(
                f"{path} must be within the interoperable JSON integer range"
            )
        return value
    if type(value) is float:
        if not math.isfinite(value):
            raise ValueError(f"{path} must be a finite number")
        if value.is_integer() and abs(value) > _MAX_SAFE_INTEGER:
            raise ValueError(
                f"{path} must be within the interoperable JSON integer range"
            )
        return value

    if isinstance(value, Mapping):
        identity = id(value)
        if identity in active:
            raise ValueError(f"{path} contains a circular reference")
        active.add(identity)
        try:
            normalized: dict[str, object] = {}
            for key, item in value.items():
                if type(key) is not str:
                    raise TypeError(f"{path} keys must be strings")
                normalized[key] = _normalize_json(
                    item,
                    path=f"{path}.{key}",
                    active=active,
                    depth=depth + 1,
                )
            return normalized
        finally:
            active.remove(identity)

    if isinstance(value, (list, tuple)):
        identity = id(value)
        if identity in active:
            raise ValueError(f"{path} contains a circular reference")
        active.add(identity)
        try:
            return [
                _normalize_json(
                    item,
                    path=f"{path}[{index}]",
                    active=active,
                    depth=depth + 1,
                )
                for index, item in enumerate(value)
            ]
        finally:
            active.remove(identity)

    raise TypeError(f"{path} contains a non-JSON value of type {type(value).__name__}")


def _normalize_metadata(
    metadata: Mapping[str, object] | None,
    *,
    path: str = "metadata",
) -> dict[str, object]:
    if metadata is None:
        return {}
    if not isinstance(metadata, Mapping):
        raise TypeError(f"{path} must be a mapping")
    normalized = _normalize_json(metadata, path=path, active=set(), depth=0)
    # A mapping input always normalizes to a plain dictionary.
    return normalized  # type: ignore[return-value]


def _freeze_json(value: object) -> object:
    if isinstance(value, dict):
        return _FrozenDict({key: _freeze_json(item) for key, item in value.items()})
    if isinstance(value, list):
        return tuple(_freeze_json(item) for item in value)
    return value


def _freeze_metadata(metadata: Mapping[str, object] | None) -> _FrozenDict:
    normalized = _normalize_metadata(metadata)
    frozen = _freeze_json(normalized)
    return frozen  # type: ignore[return-value]


def _thaw_json(value: object) -> object:
    if isinstance(value, Mapping):
        return {key: _thaw_json(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [_thaw_json(item) for item in value]
    return value


def _validate_finite_number(value: object, *, field_name: str) -> float:
    if type(value) not in (int, float):
        raise TypeError(f"{field_name} must be a number")
    try:
        number = float(value)
    except OverflowError as error:
        raise ValueError(f"{field_name} must be finite") from error
    if not math.isfinite(number):
        raise ValueError(f"{field_name} must be finite")
    return number


def _validate_configuration_number(
    value: object,
    *,
    field_name: str,
    positive: bool = False,
) -> float:
    number = _validate_finite_number(value, field_name=field_name)
    if positive and number <= 0:
        raise ValueError(f"{field_name} must be greater than zero")
    return number


def _portable_number(value: float) -> int | float:
    if abs(value) <= _MAX_SAFE_INTEGER and value.is_integer():
        return int(value)
    return value


def _coerce_result(result: Result | str) -> Result:
    if isinstance(result, Result):
        return result
    if type(result) is not str:
        raise TypeError("result must be a Result or string")
    try:
        return Result(result)
    except ValueError as error:
        values = ", ".join(repr(member.value) for member in Result)
        raise ValueError(f"result must be one of {values}") from error


@dataclass(frozen=True, slots=True)
class Contestant:
    """An immutable contestant descriptor."""

    name: str
    metadata: Mapping[str, object] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "name", _validate_name(self.name))
        object.__setattr__(self, "metadata", _freeze_metadata(self.metadata))


@dataclass(frozen=True, slots=True)
class Match:
    """An immutable recorded match."""

    id: int
    left: str
    right: str
    result: Result
    metadata: Mapping[str, object] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if type(self.id) is not int:
            raise TypeError("id must be an integer")
        if self.id < 1:
            raise ValueError("id must be greater than zero")
        left = _validate_name(self.left, field_name="left")
        right = _validate_name(self.right, field_name="right")
        if left == right:
            raise ValueError("left and right must be different contestants")
        object.__setattr__(self, "left", left)
        object.__setattr__(self, "right", right)
        object.__setattr__(self, "result", _coerce_result(self.result))
        object.__setattr__(self, "metadata", _freeze_metadata(self.metadata))


@dataclass(frozen=True, slots=True)
class Standing:
    """An immutable leaderboard row."""

    rank: int
    name: str
    rating: float
    wins: int
    losses: int
    draws: int
    matches: int
    metadata: Mapping[str, object] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if type(self.rank) is not int:
            raise TypeError("rank must be an integer")
        if self.rank < 1:
            raise ValueError("rank must be greater than zero")
        object.__setattr__(self, "name", _validate_name(self.name))
        object.__setattr__(
            self,
            "rating",
            _validate_finite_number(self.rating, field_name="rating"),
        )
        for field_name in ("wins", "losses", "draws", "matches"):
            value = getattr(self, field_name)
            if type(value) is not int:
                raise TypeError(f"{field_name} must be an integer")
            if value < 0:
                raise ValueError(f"{field_name} must not be negative")
        if self.wins + self.losses + self.draws != self.matches:
            raise ValueError("wins, losses, and draws must sum to matches")
        object.__setattr__(self, "metadata", _freeze_metadata(self.metadata))

    @property
    def played(self) -> int:
        """Compatibility alias for :attr:`matches`."""

        return self.matches

    @property
    def score(self) -> float:
        """Return match points using one point per win and half per draw."""

        return self.wins + (self.draws / 2)


class BradleyTerryStanding(TypedDict):
    """One portable row from a batch Bradley-Terry fit."""

    rank: int
    name: str
    rating: float
    confidence_lower: float
    confidence_upper: float
    matches: int
    component: int
    inconclusive: bool


@dataclass(slots=True)
class _Stats:
    played: int = 0
    wins: int = 0
    draws: int = 0
    losses: int = 0


class _XorShift32:
    """Small reproducible PRNG mirrored by the JavaScript implementation."""

    __slots__ = ("_state",)

    def __init__(self, seed: int) -> None:
        state = seed & _UINT32_MASK
        self._state = state if state else 0x6D2B79F5

    def next(self) -> int:
        state = self._state
        state ^= (state << 13) & _UINT32_MASK
        state ^= state >> 17
        state ^= (state << 5) & _UINT32_MASK
        self._state = state & _UINT32_MASK
        return self._state


def _component_seed(seed: int, names: tuple[str, ...]) -> int:
    """Mix a user seed with component names without process-randomized hashes."""

    value = 2_166_136_261
    for name in names:
        for character in name:
            code_point = ord(character)
            for shift in (0, 8, 16, 24):
                value ^= (code_point >> shift) & 0xFF
                value = (value * 16_777_619) & _UINT32_MASK
        value ^= 0xFF
        value = (value * 16_777_619) & _UINT32_MASK
    return (seed ^ value) & _UINT32_MASK


def _quantile(values: list[float], probability: float) -> float:
    """Return a linearly interpolated quantile using a portable definition."""

    ordered = sorted(values)
    position = (len(ordered) - 1) * probability
    lower_index = math.floor(position)
    upper_index = math.ceil(position)
    if lower_index == upper_index:
        return ordered[lower_index]
    fraction = position - lower_index
    return (
        ordered[lower_index] * (1 - fraction)
        + ordered[upper_index] * fraction
    )


def _fit_bradley_terry(
    size: int,
    edges: tuple[tuple[int, int], ...],
    counts: list[int],
    left_points: list[float],
) -> list[float]:
    """Fit regularized Bradley-Terry log abilities with damped Newton steps.

    A single virtual draw on every observed comparison edge keeps estimates
    finite under complete separation while preserving symmetry and match-order
    invariance.
    """

    if size == 1:
        return [0.0]

    augmented = tuple(
        (
            left,
            right,
            counts[edge_index] + _BT_EDGE_PRIOR,
            left_points[edge_index] + (_BT_EDGE_PRIOR / 2),
        )
        for edge_index, (left, right) in enumerate(edges)
    )
    log_abilities = [0.0] * size

    for _ in range(_BT_MAX_ITERATIONS):
        gradient = [0.0] * size
        information = [
            [0.0] * (size - 1)
            for _ in range(size - 1)
        ]
        objective = 0.0

        for left, right, count, left_score in augmented:
            difference = log_abilities[left] - log_abilities[right]
            if difference >= 0:
                exponential = math.exp(-difference)
                probability = 1 / (1 + exponential)
            else:
                exponential = math.exp(difference)
                probability = exponential / (1 + exponential)
            softplus = max(difference, 0.0) + math.log1p(
                math.exp(-abs(difference))
            )
            objective += left_score * difference - count * softplus

            residual = left_score - (count * probability)
            gradient[left] += residual
            gradient[right] -= residual
            weight = count * probability * (1 - probability)
            if left < size - 1:
                information[left][left] += weight
            if right < size - 1:
                information[right][right] += weight
            if left < size - 1 and right < size - 1:
                information[left][right] -= weight
                information[right][left] -= weight

        if max(abs(value) for value in gradient) <= _BT_TOLERANCE:
            break

        reduced_direction = _solve_positive_definite(
            information,
            gradient[:-1],
        )
        direction = [*reduced_direction, 0.0]
        center = sum(direction) / size
        direction = [value - center for value in direction]
        directional_derivative = sum(
            gradient[index] * direction[index]
            for index in range(size)
        )
        if (
            not math.isfinite(directional_derivative)
            or directional_derivative <= 0
        ):
            raise RuntimeError(
                "Bradley-Terry optimization produced no ascent direction"
            )

        step = 1.0
        while step >= _BT_LINE_SEARCH_FLOOR:
            candidate = [
                log_abilities[index] + (step * direction[index])
                for index in range(size)
            ]
            candidate_objective = _bradley_terry_objective(
                candidate,
                augmented,
            )
            if candidate_objective >= (
                objective + (1e-4 * step * directional_derivative)
            ):
                log_abilities = candidate
                break
            step /= 2
        else:
            raise RuntimeError(
                "Bradley-Terry optimization line search did not converge"
            )
    else:
        raise RuntimeError(
            "Bradley-Terry optimization did not converge"
        )

    multiplier = _BT_SCALE / math.log(10)
    return [multiplier * value for value in log_abilities]


def _bradley_terry_objective(
    log_abilities: list[float],
    observations: tuple[tuple[int, int, float, float], ...],
) -> float:
    total = 0.0
    for left, right, count, left_score in observations:
        difference = log_abilities[left] - log_abilities[right]
        softplus = max(difference, 0.0) + math.log1p(
            math.exp(-abs(difference))
        )
        total += left_score * difference - count * softplus
    return total


def _solve_positive_definite(
    matrix: list[list[float]],
    right_hand_side: list[float],
) -> list[float]:
    """Solve one symmetric positive-definite system by Cholesky factorization."""

    size = len(right_hand_side)
    lower = [[0.0] * size for _ in range(size)]
    for row in range(size):
        for column in range(row + 1):
            value = matrix[row][column] - sum(
                lower[row][index] * lower[column][index]
                for index in range(column)
            )
            if row == column:
                if not math.isfinite(value) or value <= 0:
                    raise RuntimeError(
                        "Bradley-Terry information matrix was not "
                        "positive definite"
                    )
                lower[row][column] = math.sqrt(value)
            else:
                lower[row][column] = value / lower[column][column]

    intermediate = [0.0] * size
    for row in range(size):
        intermediate[row] = (
            right_hand_side[row]
            - sum(
                lower[row][column] * intermediate[column]
                for column in range(row)
            )
        ) / lower[row][row]

    solution = [0.0] * size
    for row in range(size - 1, -1, -1):
        solution[row] = (
            intermediate[row]
            - sum(
                lower[column][row] * solution[column]
                for column in range(row + 1, size)
            )
        ) / lower[row][row]
    return solution


def expected_score(rating: float, opponent_rating: float) -> float:
    """Return the standard Elo expected score for ``rating``.

    The numerically stable form remains defined even for very large, but
    finite, rating differences.
    """

    own = _validate_finite_number(rating, field_name="rating")
    opponent = _validate_finite_number(
        opponent_rating, field_name="opponent_rating"
    )
    exponent = (opponent - own) / 400
    # Clamp at the IEEE-754 base-10 boundary used by the JavaScript package.
    # This also avoids platform-specific subnormal rounding in portable runs.
    if exponent >= 308:
        return 0
    if exponent <= -308:
        return 1
    return 1 / (1 + (10**exponent))


def round_robin(
    contestants: Iterable[str],
    rounds: int = 1,
) -> tuple[tuple[str, str], ...]:
    """Build a deterministic round-robin schedule.

    Caller order is preserved within each repetition. Every pair's orientation
    is reversed on odd-numbered repetitions so repeated schedules balance
    left/right placement.
    """

    if type(rounds) is not int:
        raise TypeError("rounds must be an integer")
    if rounds < 1:
        raise ValueError("rounds must be at least one")
    if rounds > _MAX_SAFE_INTEGER:
        raise ValueError("rounds must be within the interoperable integer range")
    if isinstance(contestants, (str, bytes, bytearray)):
        raise TypeError("contestants must be an iterable of names")
    try:
        names = tuple(
            _validate_name(name, field_name="contestant")
            for name in contestants
        )
    except TypeError as error:
        if "contestant" in str(error):
            raise
        raise TypeError("contestants must be an iterable of names") from error
    if len(set(names)) != len(names):
        raise ValueError("contestant names must be unique")

    base = tuple(combinations(names, 2))
    schedule: list[tuple[str, str]] = []
    for repetition in range(rounds):
        if repetition % 2:
            schedule.extend((right, left) for left, right in base)
        else:
            schedule.extend(base)
    return tuple(schedule)


class Arena:
    """A deterministic Elo arena with complete, replayable match history."""

    def __init__(
        self,
        contestants: (
            Iterable[str] | Mapping[str, Mapping[str, object] | None]
        ),
        *,
        initial_rating: float = 1000,
        k_factor: float = 32,
    ) -> None:
        self._initial_rating = _validate_configuration_number(
            initial_rating,
            field_name="initial_rating",
        )
        self._k_factor = _validate_configuration_number(
            k_factor,
            field_name="k_factor",
            positive=True,
        )
        self._contestants: dict[str, Contestant] = {}
        self._ratings: dict[str, float] = {}
        self._stats: dict[str, _Stats] = {}
        self._matches: list[Match] = []

        if isinstance(contestants, Mapping):
            for name, metadata in contestants.items():
                self.add(name, metadata)
            return
        if isinstance(contestants, (str, bytes, bytearray)):
            raise TypeError(
                "contestants must be an iterable of names or a metadata mapping"
            )
        try:
            for name in contestants:
                self.add(name)
        except TypeError as error:
            if "name must be a string" in str(error):
                raise
            raise TypeError(
                "contestants must be an iterable of names or a metadata mapping"
            ) from error

    @property
    def initial_rating(self) -> float:
        return self._initial_rating

    @property
    def k_factor(self) -> float:
        return self._k_factor

    @property
    def contestants(self) -> tuple[Contestant, ...]:
        """Return contestants in registration order."""

        return tuple(self._contestants.values())

    @property
    def matches(self) -> tuple[Match, ...]:
        """Return immutable match records in chronological order."""

        return tuple(self._matches)

    def __len__(self) -> int:
        return len(self._contestants)

    def add(
        self,
        name: str,
        metadata: Mapping[str, object] | None = None,
    ) -> Contestant:
        """Register and return a contestant."""

        validated_name = _validate_name(name)
        if validated_name in self._contestants:
            raise ValueError(f"contestant {validated_name!r} already exists")
        contestant = Contestant(
            validated_name,
            metadata if metadata is not None else {},
        )
        self._contestants[validated_name] = contestant
        self._ratings[validated_name] = self._initial_rating
        self._stats[validated_name] = _Stats()
        return contestant

    def rating(self, name: str) -> float:
        """Return the current rating for a registered contestant."""

        validated_name = _validate_name(name)
        try:
            return self._ratings[validated_name]
        except KeyError:
            raise KeyError(f"unknown contestant {validated_name!r}") from None

    def record(
        self,
        left: str,
        right: str,
        result: Result | str,
        metadata: Mapping[str, object] | None = None,
    ) -> Match:
        """Record a match, update both ratings, and return its immutable row."""

        left_name = self._registered_name(left, field_name="left")
        right_name = self._registered_name(right, field_name="right")
        if left_name == right_name:
            raise ValueError("left and right must be different contestants")
        outcome = _coerce_result(result)
        normalized_metadata = _normalize_metadata(metadata)

        left_expected = expected_score(
            self._ratings[left_name], self._ratings[right_name]
        )
        if outcome is Result.LEFT:
            left_score = 1.0
        elif outcome is Result.RIGHT:
            left_score = 0.0
        else:
            left_score = 0.5
        adjustment = self._k_factor * (left_score - left_expected)

        match = Match(
            id=len(self._matches) + 1,
            left=left_name,
            right=right_name,
            result=outcome,
            metadata=normalized_metadata,
        )

        next_left_rating = self._ratings[left_name] + adjustment
        next_right_rating = self._ratings[right_name] - adjustment
        if not math.isfinite(next_left_rating) or not math.isfinite(
            next_right_rating
        ):
            raise OverflowError("rating update produced a non-finite rating")

        self._ratings[left_name] = next_left_rating
        self._ratings[right_name] = next_right_rating
        self._apply_stats(left_name, right_name, outcome)
        self._matches.append(match)
        return match

    def history(self) -> tuple[Match, ...]:
        """Return the same immutable chronological data as :attr:`matches`."""

        return self.matches

    def standings(self) -> tuple[Standing, ...]:
        """Return leaderboard rows sorted by rating descending, then name."""

        ordered_names = sorted(
            self._contestants,
            key=lambda name: (-self._ratings[name], name),
        )
        return tuple(
            Standing(
                rank=rank,
                name=name,
                rating=self._ratings[name],
                wins=self._stats[name].wins,
                losses=self._stats[name].losses,
                draws=self._stats[name].draws,
                matches=self._stats[name].played,
                metadata=self._contestants[name].metadata,
            )
            for rank, name in enumerate(ordered_names, start=1)
        )

    def leaderboard(self) -> tuple[Standing, ...]:
        """Alias for :meth:`standings`."""

        return self.standings()

    def bradley_terry(
        self,
        *,
        confidence: float = 0.95,
        bootstrap_samples: int = 1_000,
        seed: int = 0,
    ) -> tuple[BradleyTerryStanding, ...]:
        """Return order-invariant Bradley-Terry ratings and confidence bounds.

        Confidence intervals use a seeded cluster-parametric bootstrap.
        Disconnected comparison components are numbered deterministically and
        ranked separately, so ``rank`` restarts at one for every component.
        ``inconclusive`` is true when a global comparison is impossible, a
        contestant has no matches, or confidence intervals overlap within the
        same component.
        """

        confidence_value = _validate_finite_number(
            confidence,
            field_name="confidence",
        )
        if not 0 < confidence_value < 1:
            raise ValueError("confidence must be between zero and one")
        if type(bootstrap_samples) is not int:
            raise TypeError("bootstrap_samples must be an integer")
        if not 2 <= bootstrap_samples <= _MAX_SAFE_INTEGER:
            raise ValueError("bootstrap_samples must be at least two")
        if type(seed) is not int:
            raise TypeError("seed must be an integer")
        if not 0 <= seed <= _UINT32_MASK:
            raise ValueError("seed must be an unsigned 32-bit integer")

        names = tuple(sorted(self._contestants))
        if not names:
            return ()

        adjacency = {name: set() for name in names}
        for match in self._matches:
            adjacency[match.left].add(match.right)
            adjacency[match.right].add(match.left)

        components: list[tuple[str, ...]] = []
        remaining = set(names)
        while remaining:
            first = min(remaining)
            pending = [first]
            component: set[str] = set()
            while pending:
                name = pending.pop()
                if name in component:
                    continue
                component.add(name)
                pending.extend(
                    sorted(adjacency[name] - component, reverse=True)
                )
            remaining -= component
            components.append(tuple(sorted(component)))

        disconnected = len(components) > 1
        alpha = (1 - confidence_value) / 2
        output: list[BradleyTerryStanding] = []

        for component_id, component in enumerate(components, start=1):
            name_indexes = {
                name: index for index, name in enumerate(component)
            }
            grouped_observations: list[
                tuple[int, int, float, str | None]
            ] = []
            match_counts = [0] * len(component)
            for match in self._matches:
                if (
                    match.left not in name_indexes
                    or match.right not in name_indexes
                ):
                    continue
                left = name_indexes[match.left]
                right = name_indexes[match.right]
                if left > right:
                    left, right = right, left
                    left_won = match.result is Result.RIGHT
                else:
                    left_won = match.result is Result.LEFT
                if match.result is Result.DRAW:
                    left_score = 0.5
                else:
                    left_score = 1.0 if left_won else 0.0
                group: str | None = None
                localarena = match.metadata.get("localarena")
                if (
                    isinstance(localarena, Mapping)
                    and localarena.get("kind") == "task-score"
                    and type(localarena.get("task_id")) is str
                ):
                    group = f"task:{localarena['task_id']}"
                grouped_observations.append(
                    (left, right, left_score, group)
                )
                match_counts[left] += 1
                match_counts[right] += 1
            grouped_observations.sort(
                key=lambda item: (
                    item[0],
                    item[1],
                    item[2],
                    item[3] or "",
                )
            )
            observations = [
                (left, right, score)
                for left, right, score, _ in grouped_observations
            ]
            bootstrap_groups: dict[
                str, list[tuple[int, int, float]]
            ] = {}
            for index, (left, right, score, group) in enumerate(
                grouped_observations
            ):
                group_key = group or f"match:{index:020d}"
                bootstrap_groups.setdefault(group_key, []).append(
                    (left, right, score)
                )

            edges = tuple(
                sorted({(left, right) for left, right, _ in observations})
            )
            edge_indexes = {
                edge: index for index, edge in enumerate(edges)
            }
            counts = [0] * len(edges)
            left_points = [0.0] * len(edges)
            for left, right, score in observations:
                edge_index = edge_indexes[(left, right)]
                counts[edge_index] += 1
                left_points[edge_index] += score

            deltas = _fit_bradley_terry(
                len(component),
                edges,
                counts,
                left_points,
            )
            ratings = [
                self._initial_rating + delta for delta in deltas
            ]
            edge_probabilities = [
                expected_score(deltas[left], deltas[right])
                for left, right in edges
            ]
            samples: list[list[float]] = [
                [] for _ in component
            ]
            if observations:
                generator = _XorShift32(_component_seed(seed, component))
                bootstrap_keys = sorted(bootstrap_groups)
                for _ in range(bootstrap_samples):
                    sampled_counts = [0] * len(edges)
                    sampled_points = [0.0] * len(edges)
                    for _ in bootstrap_keys:
                        group_key = bootstrap_keys[
                            generator.next() % len(bootstrap_keys)
                        ]
                        simulated_scores: dict[int, float] = {}
                        for left, right, _ in bootstrap_groups[group_key]:
                            edge_index = edge_indexes[(left, right)]
                            sampled_counts[edge_index] += 1
                            if edge_index not in simulated_scores:
                                uniform = generator.next() / (1 << 32)
                                simulated_scores[edge_index] = (
                                    1.0
                                    if uniform
                                    < edge_probabilities[edge_index]
                                    else 0.0
                                )
                            sampled_points[edge_index] += simulated_scores[
                                edge_index
                            ]
                    sample_deltas = _fit_bradley_terry(
                        len(component),
                        edges,
                        sampled_counts,
                        sampled_points,
                    )
                    for index, delta in enumerate(sample_deltas):
                        samples[index].append(
                            self._initial_rating + delta
                        )

            component_rows: list[BradleyTerryStanding] = []
            for index, name in enumerate(component):
                if samples[index]:
                    lower = _quantile(samples[index], alpha)
                    upper = _quantile(samples[index], 1 - alpha)
                else:
                    lower = ratings[index]
                    upper = ratings[index]
                component_rows.append(
                    {
                        "rank": 0,
                        "name": name,
                        "rating": ratings[index],
                        "confidence_lower": lower,
                        "confidence_upper": upper,
                        "matches": match_counts[index],
                        "component": component_id,
                        "inconclusive": False,
                    }
                )

            component_rows.sort(
                key=lambda row: (-float(row["rating"]), str(row["name"]))
            )
            previous_rating: float | None = None
            previous_rank = 0
            for index, row in enumerate(component_rows):
                rating = float(row["rating"])
                if (
                    previous_rating is None
                    or abs(rating - previous_rating) > 1e-9
                ):
                    previous_rank = index + 1
                row["rank"] = previous_rank
                previous_rating = rating

            for row in component_rows:
                overlaps = any(
                    row is not other
                    and float(row["confidence_lower"])
                    <= float(other["confidence_upper"])
                    and float(other["confidence_lower"])
                    <= float(row["confidence_upper"])
                    for other in component_rows
                )
                row_samples = samples[name_indexes[str(row["name"])]]
                degenerate_uncertainty = (
                    bool(row_samples)
                    and max(row_samples) - min(row_samples) <= 1e-9
                )
                row["inconclusive"] = (
                    disconnected
                    or int(row["matches"]) == 0
                    or overlaps
                    or degenerate_uncertainty
                )
            output.extend(component_rows)

        return tuple(output)

    def next_pair(self) -> tuple[str, str] | None:
        """Choose the least-played unordered pair deterministically."""

        names = sorted(self._contestants)
        if len(names) < 2:
            return None

        pair_matches: dict[tuple[str, str], int] = {}
        for match in self._matches:
            pair = tuple(sorted((match.left, match.right)))
            pair_matches[pair] = pair_matches.get(pair, 0) + 1

        def priority(pair: tuple[str, str]) -> tuple[int, int, int, str, str]:
            left, right = pair
            left_total = self._stats[left].played
            right_total = self._stats[right].played
            return (
                pair_matches.get(pair, 0),
                left_total + right_total,
                max(left_total, right_total),
                left,
                right,
            )

        return min(combinations(names, 2), key=priority)

    def snapshot(self) -> dict[str, object]:
        """Return a detached, JSON-compatible schema-v1 snapshot."""

        return {
            "schema_version": SCHEMA_VERSION,
            "initial_rating": _portable_number(self._initial_rating),
            "k_factor": _portable_number(self._k_factor),
            "contestants": [
                {
                    "name": contestant.name,
                    "metadata": _thaw_json(contestant.metadata),
                }
                for contestant in sorted(
                    self._contestants.values(),
                    key=lambda contestant: contestant.name,
                )
            ],
            "matches": [
                {
                    "id": match.id,
                    "left": match.left,
                    "right": match.right,
                    "result": match.result.value,
                    "metadata": _thaw_json(match.metadata),
                }
                for match in self._matches
            ],
        }

    def to_json(self, *, indent: int | None = None) -> str:
        """Serialize :meth:`snapshot` to deterministic JSON."""

        if indent is not None:
            if type(indent) is not int:
                raise TypeError("indent must be an integer or None")
            if indent < 0:
                raise ValueError("indent must not be negative")
        options: dict[str, Any] = {
            "ensure_ascii": False,
            "allow_nan": False,
            "indent": indent,
        }
        if indent is None:
            options["separators"] = (",", ":")
        return json.dumps(self.snapshot(), **options)

    @classmethod
    def from_snapshot(cls, snapshot: Mapping[str, object]) -> Arena:
        """Validate schema-v1 data and reconstruct ratings by replaying history."""

        root = _require_mapping(snapshot, path="snapshot")
        _require_fields(
            root,
            {
                "schema_version",
                "initial_rating",
                "k_factor",
                "contestants",
                "matches",
            },
            path="snapshot",
        )
        version = root["schema_version"]
        if type(version) is not int:
            raise TypeError("snapshot.schema_version must be an integer")
        if version != SCHEMA_VERSION:
            raise ValueError(
                f"unsupported schema_version {version!r}; expected {SCHEMA_VERSION}"
            )

        contestants_data = root["contestants"]
        matches_data = root["matches"]
        if type(contestants_data) is not list:
            raise TypeError("snapshot.contestants must be a list")
        if type(matches_data) is not list:
            raise TypeError("snapshot.matches must be a list")

        arena = cls(
            [],
            initial_rating=root["initial_rating"],  # type: ignore[arg-type]
            k_factor=root["k_factor"],  # type: ignore[arg-type]
        )
        for index, raw_contestant in enumerate(contestants_data):
            path = f"snapshot.contestants[{index}]"
            contestant = _require_mapping(raw_contestant, path=path)
            _require_fields(contestant, {"name", "metadata"}, path=path)
            metadata = _require_mapping(
                contestant["metadata"], path=f"{path}.metadata"
            )
            arena.add(contestant["name"], metadata)  # type: ignore[arg-type]

        for index, raw_match in enumerate(matches_data):
            path = f"snapshot.matches[{index}]"
            match = _require_mapping(raw_match, path=path)
            _require_fields(
                match,
                {"id", "left", "right", "result", "metadata"},
                path=path,
            )
            expected_id = index + 1
            match_id = match["id"]
            if type(match_id) is not int:
                raise TypeError(f"{path}.id must be an integer")
            if match_id != expected_id:
                raise ValueError(
                    f"{path}.id must be contiguous; expected {expected_id}"
                )
            if type(match["result"]) is not str:
                raise TypeError(f"{path}.result must be a string")
            metadata = _require_mapping(match["metadata"], path=f"{path}.metadata")
            recorded = arena.record(
                match["left"],  # type: ignore[arg-type]
                match["right"],  # type: ignore[arg-type]
                match["result"],
                metadata,
            )
            if recorded.id != match_id:  # Defensive assertion for subclasses.
                raise ValueError(f"{path}.id could not be reproduced")
        return arena

    @classmethod
    def from_json(cls, payload: str | bytes | bytearray) -> Arena:
        """Parse strict JSON and delegate to :meth:`from_snapshot`."""

        if not isinstance(payload, (str, bytes, bytearray)):
            raise TypeError("payload must be str, bytes, or bytearray")

        def reject_constant(value: str) -> object:
            raise ValueError(f"non-standard JSON constant {value!r} is not allowed")

        def reject_duplicate_keys(
            pairs: list[tuple[str, object]],
        ) -> dict[str, object]:
            parsed: dict[str, object] = {}
            for key, value in pairs:
                if key in parsed:
                    raise ValueError(f"duplicate JSON key {key!r}")
                parsed[key] = value
            return parsed

        try:
            decoded = json.loads(
                payload,
                parse_constant=reject_constant,
                object_pairs_hook=reject_duplicate_keys,
            )
        except (json.JSONDecodeError, UnicodeDecodeError) as error:
            raise ValueError(f"invalid JSON: {error}") from error
        return cls.from_snapshot(decoded)

    def _registered_name(self, name: object, *, field_name: str) -> str:
        validated_name = _validate_name(name, field_name=field_name)
        if validated_name not in self._contestants:
            raise KeyError(f"unknown contestant {validated_name!r}")
        return validated_name

    def _apply_stats(self, left: str, right: str, result: Result) -> None:
        left_stats = self._stats[left]
        right_stats = self._stats[right]
        left_stats.played += 1
        right_stats.played += 1
        if result is Result.LEFT:
            left_stats.wins += 1
            right_stats.losses += 1
        elif result is Result.RIGHT:
            right_stats.wins += 1
            left_stats.losses += 1
        else:
            left_stats.draws += 1
            right_stats.draws += 1


def _require_mapping(value: object, *, path: str) -> Mapping[str, object]:
    if not isinstance(value, Mapping):
        raise TypeError(f"{path} must be a mapping")
    for key in value:
        if type(key) is not str:
            raise TypeError(f"{path} keys must be strings")
    return value


def _require_fields(
    value: Mapping[str, object],
    expected: set[str],
    *,
    path: str,
) -> None:
    actual = set(value)
    missing = sorted(expected - actual)
    extra = sorted(actual - expected)
    if not missing and not extra:
        return
    details: list[str] = []
    if missing:
        details.append(f"missing {', '.join(missing)}")
    if extra:
        details.append(f"unexpected {', '.join(extra)}")
    raise ValueError(f"{path} has invalid fields: {'; '.join(details)}")
