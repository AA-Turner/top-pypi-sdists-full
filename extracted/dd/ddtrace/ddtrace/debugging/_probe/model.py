import abc
from dataclasses import dataclass
from dataclasses import field
from dataclasses import fields
from enum import Enum
from pathlib import Path
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Mapping
from typing import Optional
from typing import Tuple
from typing import Union

from ddtrace.debugging._expressions import DDExpression
from ddtrace.internal.compat import maybe_stringify
from ddtrace.internal.logger import get_logger
from ddtrace.internal.module import _resolve
from ddtrace.internal.rate_limiter import BudgetRateLimiterWithJitter as RateLimiter
from ddtrace.internal.safety import _isinstance
from ddtrace.internal.utils.cache import cached


log = get_logger(__name__)

DEFAULT_PROBE_RATE = 5000.0
DEFAULT_SNAPSHOT_PROBE_RATE = 1.0
DEFAULT_TRIGGER_PROBE_RATE = 1.0 / 60.0  # 1 per minute
DEFAULT_PROBE_CONDITION_ERROR_RATE = 1.0 / 60 / 5


@cached()
def _resolve_source_file(_path: str) -> Optional[Path]:
    """Resolve the source path for the given path.

    This recursively strips parent directories until it finds a file that
    exists according to sys.path.
    """
    path = Path(_path)
    if path.is_file():
        return path.resolve()

    for relpath in (path.relative_to(_) for _ in path.parents):
        resolved_path = _resolve(relpath)
        if resolved_path is not None:
            return resolved_path

    return None


MAXLEVEL = 2
MAXSIZE = 100
MAXLEN = 255
MAXFIELDS = 20


@dataclass
class CaptureLimits:
    max_level: int = MAXLEVEL
    max_size: int = MAXSIZE
    max_len: int = MAXLEN
    max_fields: int = MAXFIELDS


DEFAULT_CAPTURE_LIMITS = CaptureLimits()


# NOTE: Probe dataclasses are mutable, but have an identity, so can be hashed.
# When defining a probe class, the `eq` parameter of the `dataclass` decorator
# should be set to `False` to allow the `__hash__` method from the base Probe
# class to be used.


@dataclass
class Probe(abc.ABC):
    __context_creator__ = False

    probe_id: str
    version: int
    tags: Dict[str, Any] = field(compare=False)

    def update(self, other: "Probe") -> None:
        """Update the mutable fields from another probe."""
        if self.probe_id != other.probe_id:
            log.error("Probe ID mismatch when updating mutable fields")
            return

        if self.version == other.version:
            return

        for attrib in (f.name for f in fields(self) if f.compare):
            setattr(self, attrib, getattr(other, attrib))

    def is_global_rate_limited(self) -> bool:
        return False

    def __hash__(self):
        return hash(self.probe_id)


class AbstractProbeMixIn(abc.ABC):
    def __post_init__(self):
        ...


@dataclass
class RateLimitMixin(AbstractProbeMixIn):
    rate: float
    limiter: RateLimiter = field(init=False, repr=False, compare=False)

    def __post_init__(self):
        super().__post_init__()
        self.limiter = RateLimiter(
            limit_rate=self.rate,
            tau=1.0 / self.rate if self.rate else 1.0,
            on_exceed=lambda: log.warning("Rate limit exceeded for %r", self),
            call_once=True,
            raise_on_exceed=False,
        )


@dataclass
class ProbeConditionMixin(AbstractProbeMixIn):
    """Conditional probe.

    If the condition is ``None``, then this is equivalent to a non-conditional
    probe.
    """

    condition: Optional[DDExpression]
    condition_error_rate: float = field(compare=False)
    condition_error_limiter: RateLimiter = field(init=False, repr=False, compare=False)

    def __post_init__(self):
        super().__post_init__()
        self.condition_error_limiter = RateLimiter(
            limit_rate=self.condition_error_rate,
            tau=1.0 / self.condition_error_rate if self.condition_error_rate else 1.0,
            on_exceed=lambda: log.debug("Condition error rate limit exceeded for %r", self),
            call_once=True,
            raise_on_exceed=False,
        )


@dataclass
class ProbeLocationMixin(AbstractProbeMixIn):
    def location(self) -> Tuple[Optional[str], Optional[Union[str, int]]]:
        """Return a tuple of (location, sublocation) for the probe.
        For example, line probe returns the (file, line) and method probe return (module, method)
        """
        return (None, None)


@dataclass
class LineLocationMixin(ProbeLocationMixin):
    source_file: str = field(compare=False)
    line: int = field(compare=False)
    resolved_source_file: Optional[Path] = field(init=False, compare=False)

    def __post_init__(self):
        super().__post_init__()
        self.resolved_source_file = _resolve_source_file(self.source_file)

    def location(self):
        return (maybe_stringify(self.resolved_source_file), self.line)


class ProbeEvalTiming(str, Enum):
    DEFAULT = "DEFAULT"
    ENTRY = "ENTRY"
    EXIT = "EXIT"


@dataclass
class FunctionLocationMixin(ProbeLocationMixin):
    module: str = field(compare=False)
    func_qname: str = field(compare=False)

    def location(self):
        return (self.module, self.func_qname)


@dataclass
class TimingMixin(AbstractProbeMixIn):
    evaluate_at: ProbeEvalTiming


class MetricProbeKind(str, Enum):
    COUNTER = "COUNT"
    GAUGE = "GAUGE"
    HISTOGRAM = "HISTOGRAM"
    DISTRIBUTION = "DISTRIBUTION"


@dataclass
class MetricProbeMixin(AbstractProbeMixIn):
    kind: str
    name: str
    value: Optional[DDExpression]


@dataclass(eq=False)
class MetricLineProbe(Probe, LineLocationMixin, MetricProbeMixin, ProbeConditionMixin):
    pass


@dataclass(eq=False)
class MetricFunctionProbe(Probe, FunctionLocationMixin, TimingMixin, MetricProbeMixin, ProbeConditionMixin):
    pass


@dataclass
class TemplateSegment(abc.ABC):
    @abc.abstractmethod
    def eval(self, scope: Mapping[str, Any]) -> str:
        pass


@dataclass
class LiteralTemplateSegment(TemplateSegment):
    str_value: str

    def eval(self, scope: Mapping[str, Any]) -> Any:
        return self.str_value


@dataclass
class ExpressionTemplateSegment(TemplateSegment):
    expr: DDExpression

    def eval(self, scope: Mapping[str, Any]) -> Any:
        return self.expr.eval(scope)


@dataclass
class StringTemplate:
    template: str
    segments: List[TemplateSegment]

    def render(self, scope: Mapping[str, Any], serializer: Callable[[Any], str]) -> str:
        def _to_str(value):
            return value if _isinstance(value, str) else serializer(value)

        return "".join([_to_str(s.eval(scope)) for s in self.segments])


@dataclass
class LogProbeMixin(AbstractProbeMixIn):
    template: str
    segments: List[TemplateSegment]
    take_snapshot: bool
    limits: CaptureLimits = field(compare=False)

    @property
    def __budget__(self) -> int:
        return 10 if self.take_snapshot else 100


@dataclass(eq=False)
class LogLineProbe(Probe, LineLocationMixin, LogProbeMixin, ProbeConditionMixin, RateLimitMixin):
    def is_global_rate_limited(self) -> bool:
        return self.take_snapshot


@dataclass(eq=False)
class LogFunctionProbe(Probe, FunctionLocationMixin, TimingMixin, LogProbeMixin, ProbeConditionMixin, RateLimitMixin):
    def is_global_rate_limited(self) -> bool:
        return self.take_snapshot


@dataclass
class SpanProbeMixin:
    pass


@dataclass(eq=False)
class SpanFunctionProbe(Probe, FunctionLocationMixin, SpanProbeMixin, ProbeConditionMixin):
    __context_creator__: bool = field(default=True, init=False, repr=False, compare=False)


class SpanDecorationTargetSpan(str, Enum):
    ROOT = "ROOT"
    ACTIVE = "ACTIVE"


@dataclass
class SpanDecorationTag:
    name: str
    value: StringTemplate


@dataclass
class SpanDecoration:
    when: Optional[DDExpression]
    tags: List[SpanDecorationTag]


@dataclass
class SpanDecorationMixin:
    target_span: SpanDecorationTargetSpan
    decorations: List[SpanDecoration]


@dataclass(eq=False)
class SpanDecorationLineProbe(Probe, LineLocationMixin, SpanDecorationMixin):
    pass


@dataclass(eq=False)
class SpanDecorationFunctionProbe(Probe, FunctionLocationMixin, TimingMixin, SpanDecorationMixin):
    pass


@dataclass
class SessionMixin:
    session_id: str
    level: int


@dataclass(eq=False)
class TriggerLineProbe(Probe, LineLocationMixin, SessionMixin, ProbeConditionMixin, RateLimitMixin):
    pass


@dataclass(eq=False)
class TriggerFunctionProbe(Probe, FunctionLocationMixin, SessionMixin, ProbeConditionMixin, RateLimitMixin):
    pass


LineProbe = Union[LogLineProbe, MetricLineProbe, SpanDecorationLineProbe, TriggerLineProbe]
FunctionProbe = Union[
    LogFunctionProbe, MetricFunctionProbe, SpanFunctionProbe, SpanDecorationFunctionProbe, TriggerFunctionProbe
]


class ProbeType(str, Enum):
    LOG_PROBE = "LOG_PROBE"
    METRIC_PROBE = "METRIC_PROBE"
    SPAN_PROBE = "SPAN_PROBE"
    SPAN_DECORATION_PROBE = "SPAN_DECORATION_PROBE"
    TRIGGER_PROBE = "TRIGGER_PROBE"
