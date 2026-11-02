# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import inspect
import operator
import sys
import threading
import time
from collections import defaultdict
from collections.abc import Callable
from dataclasses import InitVar, dataclass, field, fields, replace
from enum import Enum, auto
from functools import partial, reduce
from importlib import import_module
from types import CodeType

from contrast_fireball import (
    CreateMetricParams,
    Library,
    LogRecordEventType,
    MetricKind,
    MetricValueType,
    RecordedMetric,
    ShieldDefinition,
)

from contrast import SecurityException
from contrast.agent import sys_monitoring
from contrast.agent.scope import SHIELD_SCOPE
from contrast.agent.sys_monitoring import CONTRAST_TOOL_ID
from contrast.reporting import fireball
from contrast.utils.configuration_utils import str_to_enum
from contrast.utils.decorators import fail_loudly, fail_quietly
from contrast.utils.stack_trace_utils import build_stack
from contrast_vendor import structlog as logging
from contrast_vendor.wrapt import register_post_import_hook

if sys.version_info[:2] < (3, 12):
    raise ImportError("CVE Shields require Python 3.12+")

logger = logging.getLogger("contrast")


class Mode(Enum):
    OFF = auto()
    MONITOR = auto()
    BLOCK = auto()


str_to_mode = str_to_enum(Mode)


@dataclass(frozen=True)
class RuleLocation:
    """
    A vulnerable function location and the permissions denied while executing inside it.
    """

    module: str
    attribute: str
    denied: frozenset[str] = frozenset()


@dataclass(frozen=True, eq=False)
class Rule:
    """
    An installed CVE shield rule. Rules compare by identity, so each installation is
    distinct from any earlier one with the same fields. A call that was in flight when
    a rule was retired can leave it active in that context's scope, and an identical
    rule added back later must not revive that activation. Use same_as to compare the
    definitions of two rules.
    """

    id: str
    library_name: str
    library_version: str
    library_hash: str
    locations: tuple[RuleLocation, ...]
    max_supported_behavior: Mode = Mode.OFF
    mode: Mode = Mode.OFF

    def key(self) -> tuple[str, str]:
        return self.id, self.library_hash

    def same_as(self, other: "Rule | None") -> bool:
        """Return whether the other rule has the same fields as this one."""
        return other is not None and all(
            getattr(self, f.name) == getattr(other, f.name) for f in fields(self)
        )


DEFAULT_RATE_LIMIT_WINDOW_MS = 3_600_000

CVE_ENTERED_METRIC = CreateMetricParams(
    name="cve.entered.count",
    kind=MetricKind.Counter,
    value_type=MetricValueType.Int,
    description="Count of entries into a CVE rule's vulnerable scope.",
    unit="{entry}",
)
"""
https://github.com/Contrast-Security-Inc/secobs-semantic-conventions/blob/main/docs/actions/cve-shield.md#metric-cveenteredcount
"""

CVE_EXPLOITED_METRIC = CreateMetricParams(
    name="cve.exploited.count",
    kind=MetricKind.Counter,
    value_type=MetricValueType.Int,
    description="Count of capability violations that are exploited while in a CVE rule's scope.",
    unit="{violation}",
)
"""
https://github.com/Contrast-Security-Inc/secobs-semantic-conventions/blob/main/docs/actions/cve-shield.md#metric-cveexploitedcount
"""

CVE_BLOCKED_METRIC = CreateMetricParams(
    name="cve.blocked.count",
    kind=MetricKind.Counter,
    value_type=MetricValueType.Int,
    description="Count of capability violations that are blocked while in a CVE rule's scope.",
    unit="{violation}",
)
"""
https://github.com/Contrast-Security-Inc/secobs-semantic-conventions/blob/main/docs/actions/cve-shield.md#metric-cveblockedcount
"""


def _rule_from_definition(
    definition: ShieldDefinition, library: Library
) -> Rule | None:
    """
    Return the rule for a definition and the library it applies to, or None if the
    definition removes the rule or turns it off.
    """
    if _is_removal(definition) or str_to_mode(definition["mode"]) == Mode.OFF:
        return None
    locations = tuple(
        RuleLocation(module, attribute, frozenset(scope_method["denied"]))
        for scope_method in definition["scope_methods"]
        for module, attribute in _parse_methods(scope_method["method"])
    )
    if not locations:
        return None
    return Rule(
        id=definition["id"],
        library_name=library.file,
        library_version=library.version,
        library_hash=library.hash,
        locations=locations,
        # Without a max supported behavior, never block.
        max_supported_behavior=(
            str_to_mode(definition.get("max_supported_behavior")) or Mode.MONITOR
        ),
        mode=str_to_mode(definition["mode"]),
    )


def _parse_methods(methods: list[dict[str, str]]) -> list[tuple[str, str]]:
    """
    Return the (module, dotted attribute) of each scope method. TeamServer sends each
    method either as `module` and `attribute` keys or as a single `module:attribute`
    value. Methods in any other form are skipped.
    """
    parsed = []
    for method in methods:
        if "module" in method and "attribute" in method:
            parsed.append((method["module"], method["attribute"]))
            continue
        module, sep, attribute = method.get("value", "").partition(":")
        if sep and module and attribute:
            parsed.append((module, attribute))
        else:
            logger.debug("Skipping unrecognized CVE shield method", method=method)
    return parsed


def _is_removal(definition: ShieldDefinition) -> bool:
    return (
        not definition["scope_methods"]
        or str_to_mode(definition.get("max_supported_behavior")) == Mode.OFF
    )


class Scope(dict[Rule, list[tuple[CodeType, frozenset[str]]]]):
    """
    Maps each active rule to a stack of (code, denied) pairs, one per currently nested
    activation of that rule, innermost last. A rule is removed once its stack is empty,
    so every rule in the scope is active.

    The union of every entry's denied set is what's actually denied while inside the
    innermost location, since an outer location's denial still applies while nested
    inside another location for the same rule. The innermost entry's code object is
    used to attribute permission (exploited) events to the function we're executing in.
    """


def active_rules() -> list[Rule]:
    """Return a list of currently active rules in the shield scope."""
    shield_scope = SHIELD_SCOPE.get()
    if shield_scope is None:
        return []
    return list(shield_scope)


_LOCAL_EVENTS: int = (
    sys.monitoring.events.PY_START
    | sys.monitoring.events.PY_RESUME
    | sys.monitoring.events.PY_RETURN
    | sys.monitoring.events.PY_YIELD
)
"""
Bitmask of sys.monitoring events we set per code object via set_local_events.
"""

_GLOBAL_EVENTS: int = sys.monitoring.events.PY_UNWIND | sys.monitoring.events.PY_THROW
"""
Bitmask of sys.monitoring we set globally via set_events. This is generally not
preferable, but some events (like PY_UNWIND and PY_THROW) can only be set globally.
"""

if sys.version_info[:2] >= (3, 15):
    # All events can be applied locally in Python 3.15+.
    # Using local events has better performance because
    # our callbacks will only be invoked for functions
    # we're interested in, not everything.
    _LOCAL_EVENTS |= _GLOBAL_EVENTS
    _GLOBAL_EVENTS = sys.monitoring.events.NO_EVENTS


_removed_rules: set[Rule] = set()
"""
Every rule removed at runtime, either outright or because a changed definition replaced
it. This holds rules rather than (CVE id, library) keys so that retiring a rule doesn't
also retire its replacement, which has the same key. Rules compare by identity, so a
rule is never un-removed, even when an identical one is installed later. It is
module-level state because it's read by PermissionReporter, which is created before the
CVECodeInstrument exists, and by import hooks, which can't be unregistered once
installed.
"""


def _is_removed(rule: Rule) -> bool:
    if not _removed_rules:
        # Removal is rare, so skip hashing the rule in the common case.
        return False
    return rule in _removed_rules


@dataclass
class CVECodeInstrument:
    reporter: fireball.Client
    libraries: InitVar[list[Library] | None] = None
    """
    The application's libraries. Shield definitions only apply to these.
    """

    _libraries: dict[str, Library] = field(init=False, repr=False)
    """
    The application's libraries, keyed by hash. Fireball only looks up shield
    definitions by hash, so TeamServer binds every definition to its library's hash.
    """

    event_register: dict[int, Callable] = field(
        default_factory=dict, init=False, repr=False
    )
    """
    Mapping from sys.monitoring event type to our currently registered callback
    """

    rule_registry: dict[CodeType, dict[Rule, frozenset[str]]] = field(
        default_factory=dict, init=False, repr=False
    )
    """
    Mapping from each instrumented code object to its rules, each with the permissions
    denied at that location. Copied into the Scope when a rule activates.
    """

    rules: dict[tuple[str, str], Rule] = field(
        default_factory=dict, init=False, repr=False
    )
    """
    Every installed rule, keyed by (CVE id, library hash). Unlike rule_registry, this
    includes rules whose modules haven't been imported yet, so a definition can be
    compared against the rule it would change or remove.
    """

    seen_rules: set = field(default_factory=set, init=False, repr=False)
    """
    Set of rules we've hit at runtime. We only want to report each rule once.
    """

    pending_exit_logs: set[Rule] = field(default_factory=set, init=False, repr=False)
    """
    Rules whose first entry was logged, but whose matching exit hasn't been logged yet.
    Logging only that exit keeps the exit log off the hot path.
    """

    _lock: threading.RLock = field(
        default_factory=threading.RLock, init=False, repr=False
    )
    """
    Serializes rule removal and installation with import-hook instrumentation. wrapt
    runs post-import hooks outside of its own lock, so without this a hook could check
    that a rule is live, lose a race with remove_rule, and then instrument the retired
    rule after removal already scanned the registry.
    """

    _global_events_enabled: bool = field(default=False, init=False, repr=False)
    """
    Whether we've enabled globally-monitored events (e.g. PY_UNWIND) yet.
    """

    _entered_metric_enabled: bool = field(default=False, init=False, repr=False)
    """
    Whether the cve.entered.count metric was created, and can be recorded into.
    """

    def __post_init__(self, libraries: list[Library] | None) -> None:
        """
        Register callbacks for particular sys.monitoring events. This does not yet
        enable the events themselves though; that happens later when we call `set*`.
        """
        if not sys_monitoring.is_enabled():
            raise Exception(
                "contrast.agent.sys_monitoring must be enabled to instrument CVE code"
            )

        self._libraries = {library.hash: library for library in libraries or ()}

        try:
            for event, callback in {
                sys.monitoring.events.PY_START: self.on_py_start,
                sys.monitoring.events.PY_RESUME: self.on_py_resume,
                sys.monitoring.events.PY_RETURN: self.on_py_return,
                sys.monitoring.events.PY_YIELD: self.on_py_yield,
                sys.monitoring.events.PY_UNWIND: self.on_py_unwind,
                sys.monitoring.events.PY_THROW: self.on_py_throw,
            }.items():
                old_callback = sys.monitoring.register_callback(
                    CONTRAST_TOOL_ID, event, callback
                )
                if old_callback is not None:
                    sys.monitoring.register_callback(
                        CONTRAST_TOOL_ID, event, old_callback
                    )
                    raise ValueError(
                        f"Callback {old_callback} already registered for {event}"
                    )
                self.event_register[event] = callback
        except Exception:
            # If we fail to register any callback, we should unregister any that were
            # registered before raising the exception.
            self.disable()
            raise

        self._entered_metric_enabled = bool(
            self.reporter.create_metric(CVE_ENTERED_METRIC)
        )

    def disable(self) -> None:
        """Uninstrument all code objects and unregister CVE code event callbacks."""
        # disable local events
        for code in list(self.rule_registry):
            self.uninstrument(code)

        self._disable_global_events()

        # deregister callbacks
        for event, callback in self.event_register.items():
            old_callback = sys.monitoring.register_callback(
                CONTRAST_TOOL_ID, event, None
            )
            if old_callback not in (callback, None):
                logger.debug(
                    "Unexpected callback found while unregistering, putting it back",
                    old_callback=old_callback,
                )
                sys.monitoring.register_callback(CONTRAST_TOOL_ID, event, old_callback)

    @fail_loudly()
    def instrument(
        self,
        code: CodeType,
        rules: list[Rule],
        denied: dict[Rule, frozenset[str]],
    ) -> None:
        """
        Instrument the given code object as a CVE function for the provided rules.

        The rules will be activated when the code is entered and deactivated when the
        code is exited. Calling this more than once for the same code object merges the
        new rules into the existing set, so a code object targeted by multiple rules is
        registered with sys.monitoring exactly once.

        `denied` maps each rule to the permissions denied at this location.
        Pass an empty dict when a rule denies nothing here.
        """
        if not self._global_events_enabled:
            self._enable_global_events()

        existing = self.rule_registry.get(code)
        if existing is None:
            if (events := sys.monitoring.get_local_events(CONTRAST_TOOL_ID, code)) and (
                overlapping_events := events & _LOCAL_EVENTS
            ):
                raise Exception(
                    f"Events {overlapping_events} are already registered on code {code}"
                )
            self.rule_registry[code] = {
                rule: denied.get(rule, frozenset()) for rule in rules
            }
            sys.monitoring.set_local_events(
                CONTRAST_TOOL_ID, code, events | _LOCAL_EVENTS
            )
        else:
            # Assign a new container rather than mutating, another thread may be
            # iterating the old one in _activate_rules or _deactivate_rules.
            self.rule_registry[code] = existing | {
                rule: existing.get(rule, frozenset()) | denied.get(rule, frozenset())
                for rule in rules
            }

    def _enable_global_events(self) -> None:
        sys.monitoring.set_events(
            CONTRAST_TOOL_ID,
            sys.monitoring.get_events(CONTRAST_TOOL_ID) | _GLOBAL_EVENTS,
        )
        self._global_events_enabled = True

    def _disable_global_events(self) -> None:
        registered_global_events = (
            reduce(operator.or_, self.event_register, 0) & _GLOBAL_EVENTS
        )
        sys.monitoring.set_events(
            CONTRAST_TOOL_ID,
            sys.monitoring.get_events(CONTRAST_TOOL_ID) & ~registered_global_events,
        )
        self._global_events_enabled = False

    def apply_definitions(self, definitions: list[ShieldDefinition]) -> None:
        """
        Apply a (possibly partial) list of shield definitions to the application's
        libraries. Each definition adds, changes or removes the rule for its CVE and
        library, and rules missing from the list are left alone. Definitions that don't
        match any of the libraries are ignored.

        A definition that produces the same rule as the installed one is unchanged.
        """
        for definition in definitions:
            library_hash = definition.get("library", {}).get("hash", "").lower()
            if (library := self._libraries.get(library_hash)) is None:
                logger.debug(
                    "Ignoring CVE shield definition for an unknown library",
                    id=definition["id"],
                    library=definition.get("library"),
                )
                continue
            rule = _rule_from_definition(definition, library)
            if rule is None:
                self.remove_rule(definition["id"], library.hash)
            elif not rule.same_as(self.rules.get(rule.key())):
                self.install_rule(rule)

    def install_rule(self, rule: Rule) -> None:
        """
        Install a rule, replacing the installed rule for the same CVE and library, if
        any. Each module the rule targets is instrumented when it's imported, or right
        away if it already has been.

        The new rule is installed before the old one is retired, so code targeted by
        both is never left uninstrumented in between. A call that starts in that brief
        window is in scope for both rules.
        """
        entries_by_module: dict[str, list[tuple[str, frozenset[str]]]] = defaultdict(
            list
        )
        for location in rule.locations:
            entries_by_module[location.module].append(
                (location.attribute, location.denied)
            )

        # An import hook for a module that's already in sys.modules runs right away,
        # even if the module is still being imported and doesn't define the targeted
        # functions yet. Wait for any such import to finish first. This can't happen
        # under the lock, since that import may run hooks that need it.
        for module_name in entries_by_module:
            _wait_for_import(module_name)

        with self._lock:
            if _is_removed(rule):
                # The same rule may be added back after it was removed. It can still be
                # active in the scope of a call that was in flight at the time, so
                # install a new rule instead of reviving the removed one.
                rule = replace(rule)
            old = self.rules.get(rule.key())
            self.rules[rule.key()] = rule
            # Hooks for imported modules run right away, under this (reentrant) lock.
            # wrapt never holds its own lock while running a hook, so this can't
            # deadlock with an import on another thread.
            for module_name, entries in entries_by_module.items():
                register_post_import_hook(
                    partial(self._instrument_module, rule, entries), module_name
                )
            if old is not None:
                _removed_rules.add(old)
                self._retire_rules(lambda r: r == old)

    @fail_quietly("Failed to instrument CVE shield code on import")
    def _instrument_module(
        self, rule: Rule, entries: list[tuple[str, frozenset[str]]], module
    ) -> None:
        """
        Post-import hook that instruments the code object for each (function, denied)
        entry of the rule within the module.
        """
        # Hold the lock across the check and the instrumentation so remove_rule can't
        # retire the rule in between.
        with self._lock:
            if _is_removed(rule):
                return
            for function_name, denied in entries:
                if (code := _resolve_code(module, function_name)) is not None:
                    self.instrument(code, [rule], denied={rule: denied})

    def remove_rule(self, cve_id: str, library_hash: str) -> None:
        """
        Remove the rule(s) for the given CVE and library, uninstrumenting any code
        object left without rules. Removing an unknown rule is a no-op.
        """
        key = (cve_id, library_hash)
        with self._lock:
            # The rule may not be in rule_registry yet if its module hasn't been
            # imported, retiring it stops its import hook from instrumenting it later.
            if (rule := self.rules.pop(key, None)) is not None:
                _removed_rules.add(rule)
            self._retire_rules(lambda r: r.key() == key)

    def _retire_rules(self, is_retired: Callable[[Rule], bool]) -> None:
        """
        Remove the instrumented rules matching `is_retired`, uninstrumenting any code
        object left without rules. The caller must hold the lock.

        Removal is rare, so we walk the whole registry instead of maintaining a reverse
        index from rule to code objects, trading CPU for memory.
        """
        for code, rules in list(self.rule_registry.items()):
            rules_to_remove = {rule for rule in rules if is_retired(rule)}
            if not rules_to_remove:
                continue
            _removed_rules.update(rules_to_remove)
            # Assign a new container rather than mutating, another thread may be
            # iterating the old one in _activate_rules or _deactivate_rules.
            if remaining := {
                rule: denied
                for rule, denied in rules.items()
                if rule not in rules_to_remove
            }:
                self.rule_registry[code] = remaining
            else:
                self.uninstrument(code)

        if not self.rule_registry and self._global_events_enabled:
            # PY_UNWIND and PY_THROW fire for every frame, so stop paying for them.
            self._disable_global_events()

    def uninstrument(self, code: CodeType) -> None:
        events = sys.monitoring.get_local_events(CONTRAST_TOOL_ID, code)
        events_without_cve_code = events & ~_LOCAL_EVENTS
        sys.monitoring.set_local_events(CONTRAST_TOOL_ID, code, events_without_cve_code)
        self.rule_registry.pop(code, None)

    def on_py_start(self, code: CodeType, instruction_offset: int) -> object:
        """
        Callback for PY_START events on instrumented code. Activates the rules
        registered for the code object.
        """
        if (shield_scope := SHIELD_SCOPE.get()) is None:
            shield_scope = Scope()
            SHIELD_SCOPE.set(shield_scope)

        if rules := self.rule_registry.get(code):
            self._activate_rules(code, shield_scope, rules, is_new_call=True)

    def on_py_resume(self, code: CodeType, instruction_offset: int) -> object:
        """
        Callback for PY_RESUME. Fires when a generator or coroutine resumes after a
        suspension; reactivates the rules, mirroring on_py_start for the initial entry.
        A resumption continues an earlier call, so it doesn't count as a new entry.
        """
        if (shield_scope := SHIELD_SCOPE.get()) is None:
            shield_scope = Scope()
            SHIELD_SCOPE.set(shield_scope)

        if rules := self.rule_registry.get(code):
            self._activate_rules(code, shield_scope, rules, is_new_call=False)

    def on_py_throw(
        self, code: CodeType, instruction_offset: int, exc: BaseException
    ) -> None:
        """
        Callback for PY_THROW, fired when a generator/coroutine is resumed via
        throw() (including close()). Unlike a normal resumption, PY_RESUME does
        not fire in this case, so we activate the rule here instead, otherwise
        code that runs as a result of the injected exception (e.g. a finally
        block) would be missed.
        """
        # Fast path: this is a global event, so it fires for every throw() into
        # any generator/coroutine in the process, not just instrumented ones.
        if (rules := self.rule_registry.get(code)) is None:
            return

        if (shield_scope := SHIELD_SCOPE.get()) is None:
            shield_scope = Scope()
            SHIELD_SCOPE.set(shield_scope)

        self._activate_rules(code, shield_scope, rules, is_new_call=False)

    @fail_quietly()
    def _activate_rules(
        self,
        code: CodeType,
        shield_scope: Scope,
        rules: dict[Rule, frozenset[str]],
        *,
        is_new_call: bool,
    ) -> None:
        """
        Activate the rules for the code object.

        `is_new_call` is True for the start of a call (PY_START), and False when a
        suspended generator/coroutine is resumed (PY_RESUME, PY_THROW). Only a new
        call that enters a rule's scope from outside of it (i.e. not a nested or
        recursive call to a location for an already-active rule) is counted by the
        cve.entered.count metric.
        """
        if is_new_call and self._entered_metric_enabled:
            self._record_entered(shield_scope, rules)

        for rule, denied in rules.items():
            shield_scope.setdefault(rule, []).append((code, denied))
            if rule not in self.seen_rules:
                self.seen_rules.add(rule)
                self.pending_exit_logs.add(rule)
                logger.debug("Entered new rule", rule=rule, code=code)

                self.reporter.new_log_record_event(
                    fireball.LogRecordEvent(
                        event_type=LogRecordEventType.CveShield,
                        event_details={
                            "cve.id": rule.id,
                            "cve.shield.permission": "Entered",
                            "cve.shield.result": "monitored",
                            "cve.shield.mode": rule.mode.name.lower(),
                            "cve.shield.max_supported_behavior": rule.max_supported_behavior.name.lower(),
                            "cve.code.namespace": inspect.getmodule(code).__name__,
                            "cve.code.function": code.co_name,
                            "cve.library.hash": rule.library_hash,
                            "cve.library.name": rule.library_name,
                            "cve.library.version": rule.library_version,
                        },
                        stack=build_stack(),
                    ),
                    trace=None,
                )

    def _record_entered(
        self, shield_scope: Scope, rules: dict[Rule, frozenset[str]]
    ) -> None:
        if entered := [
            RecordedMetric(
                name=CVE_ENTERED_METRIC.name,
                value=1,
                attributes={"cve.id": rule.id, "cve.mode": rule.mode.name.lower()},
            )
            for rule in rules
            if rule not in shield_scope
        ]:
            self.reporter.record_metrics(entered)

    def deactivate_rules(
        self,
        code: CodeType,
        instruction_offset: int,
        _,  # this arg differs depending on the event, but we don't need it
    ) -> None:
        """
        Pop the scope entry for each rule registered for the code object.

        Shared callback for several "exiting function" events, such as PY_RETURN and
        PY_UNWIND.
        """
        # We need to keep the early exit / fast path here as fast as possible, because
        # this function fires every time for global events.
        if (
            # these cases can be hit for PY_UNWIND (for an uninstrumented function) or
            # in an edge case where events were enabled for a function mid-call.
            (rules := self.rule_registry.get(code)) is None
            or (shield_scope := SHIELD_SCOPE.get()) is None
        ):
            return

        self._deactivate_rules(code, shield_scope, rules)

    @fail_quietly()
    def _deactivate_rules(
        self, code: CodeType, shield_scope: Scope, rules: dict[Rule, frozenset[str]]
    ):
        for rule in rules:
            if not (stack := shield_scope.get(rule)):
                logger.debug(
                    "function exit without matching PY_START",
                    rule=rule,
                    code=code,
                )
                continue
            stack.pop()
            if not stack:
                del shield_scope[rule]
                if rule in self.pending_exit_logs:
                    self.pending_exit_logs.discard(rule)
                    logger.debug("Exited rule", rule=rule, code=code)

    on_py_return = deactivate_rules
    """
    Callback for PY_RETURN. Note that this is a local event and should be set per code
    object.
    """

    on_py_yield = deactivate_rules
    """
    Callback for PY_YIELD. Fires when a generator or coroutine suspends; deactivates
    the rule for the duration of the suspension, matching on_py_resume below.
    """

    on_py_unwind = deactivate_rules
    """
    Callback for PY_UNWIND. This event can only be set globally.
    """


class RateLimiter:
    """
    Sliding window rate limiter for capability events, with one window per (rule,
    capability, mode). The first event starts a window and is allowed, and events
    arriving before the window ends are suppressed. Including the mode in the key means
    a change of the rule's effective mode starts a fresh window.

    This is lock free. Two threads racing at the start of a window may both be allowed,
    which is harmless for a rate limit.
    """

    def __init__(self, window_ms: int = DEFAULT_RATE_LIMIT_WINDOW_MS):
        self.window_ms = window_ms
        self._window_ends: dict[tuple[tuple[str, str], str], tuple[Mode, int]] = {}

    def allow(self, rule: Rule, capability: str, now: int | None = None) -> bool:
        """Return True if an event should be emitted, False if it's suppressed."""
        now = time.monotonic_ns() // 1_000_000 if now is None else now
        key = (rule.key(), capability)
        previous_mode, window_end = self._window_ends.get(key, (rule.mode, 0))
        if previous_mode == rule.mode and now < window_end:
            return False
        self._window_ends[key] = (rule.mode, now + self.window_ms)
        return True


@dataclass
class PermissionReporter:
    """
    Reports CVE shield permission (capability) events, rate-limited per (rule,
    permission) pair. Kept separate from CVECodeInstrument because it only depends on
    the reporter and the SHIELD_SCOPE contextvar, so it can be constructed
    synchronously at agent init time, before the instrument exists.
    """

    reporter: fireball.Client
    rate_limiter: RateLimiter = field(default_factory=RateLimiter, repr=False)

    _metrics: dict[str, CreateMetricParams] = field(
        default_factory=dict, init=False, repr=False
    )
    """
    The result-specific metrics that were successfully created, keyed by result.
    """

    def __post_init__(self) -> None:
        for result, params in (
            ("exploited", CVE_EXPLOITED_METRIC),
            ("blocked", CVE_BLOCKED_METRIC),
        ):
            if self.reporter.create_metric(params):
                self._metrics[result] = params

    @fail_quietly()
    def report_permission(
        self, permission: str, dangerous_namespace: str, dangerous_function: str
    ) -> None:
        """
        Emit a permission (capability) event for each active rule that denies this
        permission at any of the (possibly nested) locations currently active for it,
        unless it's rate limited. Nested locations for the same rule are all still "in
        scope", so a permission denied by an outer location remains denied while
        executing inside an inner one, even if the inner location doesn't deny it
        itself. The reported result is `monitored`, `exploited` or `blocked`
        depending on the rule's mode and `max_supported_behavior`.

        Events are rate limited per (rule, permission). Denied permissions (exploited
        or blocked) always increment their metric, whether or not the event is rate
        limited.
        """
        if not (shield_scope := SHIELD_SCOPE.get()):
            return

        blocked_rules = []
        metrics: list[RecordedMetric] = []

        # Copy the items, since a removed rule is popped from the scope as we go.
        for rule, stack in list(shield_scope.items()):
            if _is_removed(rule):
                # a call that was in flight when the rule was removed never exits it.
                # exit here for possible performance improvement in long-running cases.
                shield_scope.pop(rule, None)
                continue
            match (rule.mode, rule.max_supported_behavior):
                case (_, Mode.MONITOR):
                    result = "monitored"
                case (Mode.MONITOR, Mode.BLOCK):
                    result = "exploited"
                case (Mode.BLOCK, Mode.BLOCK):
                    result = "blocked"
                case _:
                    raise ValueError(
                        f"Unexpected rule modes: {rule.mode} (max: {rule.max_supported_behavior})"
                    )
            denied = frozenset.union(*(entry_denied for _, entry_denied in stack))
            # always report permissions when in monitor mode. The backend is trying to learn
            # what capabilities are "normal/expected/baseline" before creating a denylist.
            if result != "monitored" and permission not in denied:
                continue
            if result == "blocked":
                blocked_rules.append(rule)
            if (metric := self._metrics.get(result)) is not None:
                metrics.append(
                    RecordedMetric(
                        name=metric.name,
                        value=1,
                        attributes={
                            "cve.id": rule.id,
                            "cve.mode": rule.mode.name.lower(),
                            "capability": permission,
                        },
                    )
                )
            if not self.rate_limiter.allow(rule, permission):
                continue

            caller = stack[-1][0]
            module = inspect.getmodule(caller)
            namespace = module.__name__ if module is not None else ""
            function = caller.co_name

            logger.debug(
                "CVE shield permission used in scope",
                rule=rule,
                permission=permission,
                dangerous_function=f"{dangerous_namespace}.{dangerous_function}",
            )
            self.reporter.new_log_record_event(
                fireball.LogRecordEvent(
                    event_type=LogRecordEventType.CveShield,
                    event_details={
                        "cve.id": rule.id,
                        "cve.shield.permission": permission,
                        "cve.shield.result": result,
                        "cve.shield.mode": rule.mode.name.lower(),
                        "cve.shield.max_supported_behavior": rule.max_supported_behavior.name.lower(),
                        "cve.code.namespace": namespace,
                        "cve.code.function": function,
                        "cve.code.dangerous.namespace": dangerous_namespace,
                        "cve.code.dangerous.function": dangerous_function,
                        "cve.library.name": rule.library_name,
                        "cve.library.version": rule.library_version,
                        "cve.library.hash": rule.library_hash,
                    },
                    stack=build_stack(),
                ),
                trace=None,
            )
        if metrics:
            self.reporter.record_metrics(metrics)
        if blocked_rules:
            raise CapabilityBlockedException(permission, blocked_rules)


class CapabilityBlockedException(SecurityException):
    def __init__(self, capability: str, rules: list[Rule]):
        super().__init__(
            f"Contrast CVE Shield blocked the {capability} capability due to {','.join(rule.id for rule in rules)}."
        )


_instrument: CVECodeInstrument | None = None
"""
The CVECodeInstrument created by enable, or None if shields are disabled.
"""


def enable(reporter: fireball.Client, libraries: list[Library]) -> CVECodeInstrument:
    """
    Create the CVECodeInstrument for the given libraries. Shield definitions are applied
    to it by update_definitions as the settings thread receives them.

    Fireball only looks up definitions for libraries reported to it, so this must be
    called before the libraries are reported. Then no definitions can arrive before
    there's an instrument to apply them to.
    """
    global _instrument
    _instrument = CVECodeInstrument(reporter, libraries)
    return _instrument


def update_definitions(definitions: list[ShieldDefinition]) -> None:
    """
    Apply shield definitions received from Fireball, which looks them up when libraries
    are reported and then periodically. Fireball sends every definition each time any
    of them changes, and a removed definition is sent with mode OFF.
    """
    if _instrument is None:
        # Shields are disabled.
        return
    logger.debug("Received CVE shield definitions", count=len(definitions))
    _instrument.apply_definitions(definitions)


def _wait_for_import(module_name: str) -> None:
    """
    Wait for an import of the module that's in progress on another thread to finish.
    Modules that aren't in sys.modules are left alone, so this only imports a module
    itself if another thread's import of it fails.
    """
    if module_name not in sys.modules:
        return
    try:
        # Python waits for the other thread's import to finish, then returns the module.
        import_module(module_name)
    except Exception:
        # The other thread's import failed, and our attempt to import it again also
        # failed. The import hook still instruments the module if it's imported later.
        logger.debug(
            "Failed waiting for import of CVE shield module",
            module=module_name,
            exc_info=True,
        )


def _resolve_code(module, function_name: str) -> CodeType | None:
    """Resolve a dotted function/method name within a module to its code object."""
    try:
        obj = reduce(getattr, function_name.split("."), module)
    except AttributeError:
        logger.debug(
            "Could not resolve CVE shield location",
            module=getattr(module, "__name__", module),
            function=function_name,
        )
        return None
    obj = inspect.unwrap(obj)
    return getattr(obj, "__code__", None)
