"""Observation-scope matching and candidate-filter evaluation."""

from __future__ import annotations

import hashlib
import re
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import UTC, datetime

from agentic_devtools.cli.ci.reconciliation.models import RepositoryTarget, TriStateValue

_ALLOWED_OPERANDS = {
    "target_branch_match",
    "author_association",
    "draft_state",
    "mergeability_state",
    "unresolved_reviews",
    "labels",
}
_TOKEN_PATTERN = re.compile(r"\(|\)|AND|OR|NOT|[A-Za-z_][A-Za-z0-9_]*")


@dataclass(frozen=True)
class ScopeSnapshot:
    """Immutable scope snapshot with deterministic fingerprint."""

    repositories: tuple[str, ...]
    target_branches: tuple[str, ...]
    candidate_filter_expression: str
    fingerprint: str
    epoch_id: str
    captured_at_utc_z: str


class _Parser:
    def __init__(self, tokens: list[str]) -> None:
        self._tokens = tokens
        self._index = 0

    def _peek(self) -> str | None:
        return self._tokens[self._index] if self._index < len(self._tokens) else None

    def _consume(self, expected: str | None = None) -> str:
        token = self._peek()
        if token is None:
            raise ValueError("unexpected end of expression")
        if expected is not None and token != expected:
            raise ValueError(f"expected {expected!r}, got {token!r}")
        self._index += 1
        return token

    def parse(self) -> tuple:
        expr = self._parse_or()
        if self._peek() is not None:
            raise ValueError(f"unexpected token {self._peek()!r}")
        return expr

    def _parse_or(self) -> tuple:
        left = self._parse_and()
        while self._peek() == "OR":
            self._consume("OR")
            right = self._parse_and()
            left = ("OR", left, right)
        return left

    def _parse_and(self) -> tuple:
        left = self._parse_not()
        while self._peek() == "AND":
            self._consume("AND")
            right = self._parse_not()
            left = ("AND", left, right)
        return left

    def _parse_not(self) -> tuple:
        if self._peek() == "NOT":
            self._consume("NOT")
            return ("NOT", self._parse_not())
        return self._parse_term()

    def _parse_term(self) -> tuple:
        token = self._peek()
        if token == "(":
            self._consume("(")
            expr = self._parse_or()
            self._consume(")")
            return expr
        if token is None:
            raise ValueError("missing operand")
        self._consume()
        if token not in _ALLOWED_OPERANDS:
            raise ValueError(f"unsupported operand: {token}")
        return ("OPERAND", token)


def _to_bool(value: TriStateValue) -> int:
    if value == TriStateValue.TRUE:
        return 1
    if value == TriStateValue.FALSE:
        return -1
    return 0


def _from_bool(value: int) -> TriStateValue:
    if value > 0:
        return TriStateValue.TRUE
    if value < 0:
        return TriStateValue.FALSE
    return TriStateValue.UNKNOWN


def _eval(node: tuple, operands: Mapping[str, TriStateValue]) -> TriStateValue:
    operator = node[0]
    if operator == "OPERAND":
        return operands.get(node[1], TriStateValue.UNKNOWN)
    if operator == "NOT":
        value = _eval(node[1], operands)
        return _from_bool(-_to_bool(value))
    left = _eval(node[1], operands)
    right = _eval(node[2], operands)
    if operator == "AND":
        if TriStateValue.FALSE in {left, right}:
            return TriStateValue.FALSE
        if TriStateValue.UNKNOWN in {left, right}:
            return TriStateValue.UNKNOWN
        return TriStateValue.TRUE
    if TriStateValue.TRUE in {left, right}:
        return TriStateValue.TRUE
    if TriStateValue.UNKNOWN in {left, right}:
        return TriStateValue.UNKNOWN
    return TriStateValue.FALSE


def _collect_operands(node: tuple) -> set[str]:
    operator = node[0]
    if operator == "OPERAND":
        return {node[1]}
    if operator == "NOT":
        return _collect_operands(node[1])
    return _collect_operands(node[1]) | _collect_operands(node[2])


def evaluate_candidate_filter(
    expression: str,
    operands: Mapping[str, TriStateValue],
) -> tuple[TriStateValue, tuple[str, ...]]:
    """Evaluate candidate-filter expression with tri-state semantics."""
    tokens = []
    position = 0
    for match in _TOKEN_PATTERN.finditer(expression):
        if expression[position : match.start()].strip():
            return TriStateValue.UNKNOWN, ("invalid candidate-filter syntax",)
        token = match.group(0)
        tokens.append(token.upper() if token.upper() in {"AND", "OR", "NOT"} else token)
        position = match.end()
    if expression[position:].strip():
        return TriStateValue.UNKNOWN, ("invalid candidate-filter syntax",)
    try:
        ast_tree = _Parser(tokens).parse()
    except ValueError as exc:
        return TriStateValue.UNKNOWN, (str(exc),)
    result = _eval(ast_tree, operands)
    referenced = _collect_operands(ast_tree)
    missing = tuple(sorted(name for name in referenced if name not in operands))
    if missing:
        return (
            TriStateValue.UNKNOWN if result != TriStateValue.FALSE else result,
            tuple(f"missing operand value: {name}" for name in missing),
        )
    return result, ()


def matches_observation_scope(
    *,
    repository: str,
    target_branch: str,
    targets: tuple[RepositoryTarget, ...],
) -> bool:
    """Return whether repository/branch belongs to configured scope."""
    return any(
        target.enabled and target.repository == repository and target.target_branch == target_branch
        for target in targets
    )


def create_scope_snapshot(
    *,
    targets: tuple[RepositoryTarget, ...],
    candidate_filter_expression: str,
    now: datetime | None = None,
) -> ScopeSnapshot:
    """Create deterministic scope fingerprint and epoch identifier."""
    current = (now or datetime.now(UTC)).astimezone(UTC)
    repositories = tuple(sorted({target.repository for target in targets if target.enabled}))
    branches = tuple(sorted({target.target_branch for target in targets if target.enabled}))
    canonical = "|".join(
        f"{target.repository}:{target.target_branch}:{int(target.enabled)}"
        for target in sorted(targets, key=lambda item: (item.repository, item.target_branch, item.enabled))
    )
    digest = hashlib.sha256(f"{canonical}|{candidate_filter_expression}".encode()).hexdigest()
    captured_at_utc_z = current.replace(microsecond=0).isoformat().replace("+00:00", "Z")
    return ScopeSnapshot(
        repositories=repositories,
        target_branches=branches,
        candidate_filter_expression=candidate_filter_expression,
        fingerprint=digest,
        epoch_id=digest[:12],
        captured_at_utc_z=captured_at_utc_z,
    )
