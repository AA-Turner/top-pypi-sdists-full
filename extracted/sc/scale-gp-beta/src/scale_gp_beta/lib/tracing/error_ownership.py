from __future__ import annotations

import os
import sysconfig
from types import TracebackType
from typing import Set, List, Type, Tuple, Literal, Optional, Sequence, cast
from dataclasses import dataclass

from .types import ErrorCategory
from .exceptions import CategorizedError

ERROR_CLASSIFIER_VERSION = "ownership-v1"
ERROR_CATEGORY_UNKNOWN: ErrorCategory = "unknown"
_ERROR_CATEGORIES = frozenset({"application", "platform", "unknown"})

ErrorCategorySource = Literal["explicit", "categorized_error", "stack_trace", "boundary", "mapping", "fallback"]
FrameOwnership = Literal["application", "platform", "ignored", "unresolved", "ambiguous"]


def _normalize_category(value: object) -> Optional[ErrorCategory]:
    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized in _ERROR_CATEGORIES:
            return cast(ErrorCategory, normalized)
    return None


def _normalize_module_prefix(value: str) -> str:
    normalized = value.strip().strip(".")
    if not normalized:
        raise ValueError("module ownership prefixes must be non-empty")
    return normalized


def _normalize_file_root(value: str) -> str:
    if not value or not os.path.isabs(value):
        raise ValueError("file ownership roots must be absolute")
    return os.path.normcase(os.path.normpath(value))


def _default_ignored_file_roots() -> Tuple[str, ...]:
    roots = {
        _normalize_file_root(path)
        for key, path in sysconfig.get_paths().items()
        if key in {"stdlib", "platstdlib", "purelib", "platlib"} and path and os.path.isabs(path)
    }
    return tuple(sorted(roots))


@dataclass(frozen=True)
class TracebackOwnershipPolicy:
    """Immutable, producer-neutral ownership rules for traceback frames.

    Explicit module ownership takes precedence over file-root and ignored-root
    rules, so producers can identify packages installed under site-packages or
    loaded from archives. Neutral defaults never assume an application or
    platform package.
    """

    application_module_prefixes: Tuple[str, ...] = ()
    platform_module_prefixes: Tuple[str, ...] = ()
    ignored_module_prefixes: Tuple[str, ...] = ()
    application_file_roots: Tuple[str, ...] = ()
    platform_file_roots: Tuple[str, ...] = ()
    ignored_file_roots: Tuple[str, ...] = _default_ignored_file_roots()
    infer_application_from_unowned_absolute_paths: bool = False
    archive_paths_are_unresolved: bool = True

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "application_module_prefixes",
            tuple(_normalize_module_prefix(value) for value in self.application_module_prefixes),
        )
        object.__setattr__(
            self,
            "platform_module_prefixes",
            tuple(_normalize_module_prefix(value) for value in self.platform_module_prefixes),
        )
        object.__setattr__(
            self,
            "ignored_module_prefixes",
            tuple(_normalize_module_prefix(value) for value in self.ignored_module_prefixes),
        )
        object.__setattr__(
            self,
            "application_file_roots",
            tuple(_normalize_file_root(value) for value in self.application_file_roots),
        )
        object.__setattr__(
            self,
            "platform_file_roots",
            tuple(_normalize_file_root(value) for value in self.platform_file_roots),
        )
        object.__setattr__(
            self,
            "ignored_file_roots",
            tuple(_normalize_file_root(value) for value in self.ignored_file_roots),
        )


DEFAULT_TRACEBACK_OWNERSHIP_POLICY = TracebackOwnershipPolicy()


@dataclass(frozen=True)
class ExceptionMapping:
    """A scope-specific exception mapping; never a global class-name heuristic."""

    scope: str
    exception_type: Type[BaseException]
    category: ErrorCategory
    include_subclasses: bool = False

    def __post_init__(self) -> None:
        if not self.scope.strip():
            raise ValueError("exception mapping scope must be non-empty")
        category = _normalize_category(self.category)
        if category not in ("application", "platform"):
            raise ValueError("exception mapping category must be 'application' or 'platform'")
        object.__setattr__(self, "scope", self.scope.strip())
        object.__setattr__(self, "category", category)


@dataclass(frozen=True)
class ErrorClassifierConfig:
    policy: TracebackOwnershipPolicy = DEFAULT_TRACEBACK_OWNERSHIP_POLICY
    mappings: Tuple[ExceptionMapping, ...] = ()

    def __init__(
        self,
        policy: TracebackOwnershipPolicy = DEFAULT_TRACEBACK_OWNERSHIP_POLICY,
        mappings: Sequence[ExceptionMapping] = (),
    ) -> None:
        normalized = tuple(mappings)
        seen: Set[Tuple[str, Type[BaseException]]] = set()
        for mapping in normalized:
            key = (mapping.scope, mapping.exception_type)
            if key in seen:
                raise ValueError("duplicate exception mapping for scope and exception type")
            seen.add(key)
        object.__setattr__(self, "policy", policy)
        object.__setattr__(self, "mappings", normalized)


DEFAULT_ERROR_CLASSIFIER_CONFIG = ErrorClassifierConfig()


@dataclass(frozen=True)
class ErrorClassification:
    category: ErrorCategory
    source: ErrorCategorySource
    reason: str
    classifier_version: str = ERROR_CLASSIFIER_VERSION


def _module_matches(module_name: Optional[str], prefixes: Tuple[str, ...]) -> bool:
    if module_name is None:
        return False
    return any(module_name == prefix or module_name.startswith(f"{prefix}.") for prefix in prefixes)


def _path_is_under(filename: str, roots: Tuple[str, ...]) -> bool:
    if not roots or not os.path.isabs(filename):
        return False
    normalized = os.path.normcase(os.path.normpath(filename))
    for root in roots:
        try:
            if os.path.commonpath((normalized, root)) == root:
                return True
        except ValueError:
            continue
    return False


def _is_archive_filename(filename: str) -> bool:
    normalized = filename.replace("\\", "/").lower()
    return any(marker in normalized for marker in (".zip/", ".whl/", ".pyz/"))


def _frame_ownership(
    traceback: TracebackType,
    policy: TracebackOwnershipPolicy,
) -> Tuple[FrameOwnership, str]:
    module_value = traceback.tb_frame.f_globals.get("__name__")
    module_name = module_value if isinstance(module_value, str) else None
    filename = traceback.tb_frame.f_code.co_filename

    application_module = _module_matches(module_name, policy.application_module_prefixes)
    platform_module = _module_matches(module_name, policy.platform_module_prefixes)
    application_file = _path_is_under(filename, policy.application_file_roots)
    platform_file = _path_is_under(filename, policy.platform_file_roots)

    if application_module and platform_module:
        return "ambiguous", "stack_ambiguous_owned_frame"
    if application_module:
        return "application", "application_module"
    if platform_module:
        return "platform", "platform_module"
    if application_file and platform_file:
        return "ambiguous", "stack_ambiguous_owned_frame"
    if application_file:
        return "application", "application_file_root"
    if platform_file:
        return "platform", "platform_file_root"

    if _module_matches(module_name, policy.ignored_module_prefixes):
        return "ignored", "ignored_module"
    if _path_is_under(filename, policy.ignored_file_roots):
        return "ignored", "ignored_file_root"

    if not filename or filename.startswith("<"):
        return "unresolved", "stack_unresolvable_frame"
    if policy.archive_paths_are_unresolved and _is_archive_filename(filename):
        return "unresolved", "stack_archive_frame"
    if policy.infer_application_from_unowned_absolute_paths and os.path.isabs(filename):
        return "application", "unowned_absolute_source"
    return "unresolved", "stack_unresolvable_frame"


def _stack_classification(
    exc: BaseException,
    policy: TracebackOwnershipPolicy,
) -> Tuple[Optional[ErrorClassification], str]:
    traceback = exc.__traceback__
    if traceback is None:
        return None, "stack_no_traceback"

    frames: List[TracebackType] = []
    while traceback is not None:
        frames.append(traceback)
        traceback = traceback.tb_next

    for frame in reversed(frames):
        ownership, rule_id = _frame_ownership(frame, policy)
        if ownership == "ignored":
            continue
        if ownership in ("ambiguous", "unresolved"):
            return None, rule_id
        return (
            ErrorClassification(
                category=cast(ErrorCategory, ownership),
                source="stack_trace",
                reason=f"stack_rule:{rule_id}",
            ),
            rule_id,
        )
    return None, "stack_no_owned_frame"


def _mapping_specificity(exc: BaseException, mapping: ExceptionMapping) -> Tuple[int, str]:
    try:
        distance = type(exc).__mro__.index(mapping.exception_type)
    except ValueError:
        distance = len(type(exc).__mro__)
    stable_name = f"{mapping.exception_type.__module__}.{mapping.exception_type.__qualname__}"
    return distance, stable_name


def classify_error(
    exc: BaseException,
    *,
    explicit_category: Optional[ErrorCategory] = None,
    boundary_category: Optional[ErrorCategory] = None,
    mapping_scope: Optional[str] = None,
    config: ErrorClassifierConfig = DEFAULT_ERROR_CLASSIFIER_CONFIG,
) -> ErrorClassification:
    """Classify exception ownership without inspecting messages or class names."""
    if explicit_category is not None:
        category = _normalize_category(explicit_category)
        if category is None:
            return ErrorClassification("unknown", "explicit", "invalid_explicit_category")
        return ErrorClassification(category, "explicit", "caller_explicit_category")

    if isinstance(exc, CategorizedError):
        category = _normalize_category(exc.error_category)
        if category is None:
            return ErrorClassification("unknown", "categorized_error", "invalid_canonical_category")
        return ErrorClassification(category, "categorized_error", "canonical_categorized_error")

    stack_classification, stack_failure_reason = _stack_classification(exc, config.policy)
    if stack_classification is not None:
        return stack_classification

    boundary = _normalize_category(boundary_category)
    if boundary is not None:
        return ErrorClassification(boundary, "boundary", "explicit_boundary_hint")

    if mapping_scope is not None:
        exact_matches = [
            mapping
            for mapping in config.mappings
            if mapping.scope == mapping_scope and type(exc) is mapping.exception_type
        ]
        subclass_matches = [
            mapping
            for mapping in config.mappings
            if mapping.scope == mapping_scope
            and mapping.include_subclasses
            and isinstance(exc, mapping.exception_type)
            and type(exc) is not mapping.exception_type
        ]
        matches = exact_matches or sorted(
            subclass_matches,
            key=lambda mapping: _mapping_specificity(exc, mapping),
        )
        if matches:
            return ErrorClassification(
                category=matches[0].category,
                source="mapping",
                reason="registered_exception_mapping",
            )

    return ErrorClassification("unknown", "fallback", stack_failure_reason)
