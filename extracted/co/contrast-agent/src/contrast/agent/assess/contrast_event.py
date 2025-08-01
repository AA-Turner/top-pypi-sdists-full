# Copyright © 2025 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from __future__ import annotations
import copy
from dataclasses import dataclass, field
from itertools import chain
from pathlib import PurePath
import re
import reprlib
import threading
import time
from typing import (
    Any,
    Callable,
    Literal,
    Union,
)
from collections.abc import Mapping, Sequence
from contrast.agent.assess.tag import Tag

from contrast.agent.policy.constants import (
    OBJECT,
    RETURN,
)

from contrast.agent.assess.truncate import truncate_tainted_string
from contrast.agent.assess.utils import get_properties

from contrast.agent.policy.policy_node import PolicyNode
from contrast.utils.assess.duck_utils import len_or_zero
from contrast.utils.base64_utils import B64_NONE_STRING, base64_encode
from contrast.utils.stack_trace_utils import (
    StackSummary,
    acceptable_frame,
    build_stack,
    to_assess_stack,
)
from contrast_fireball import (
    AssessEvent,
    AssessEventAction,
    AssessEventSource,
    AssessObject,
    AssessParentObject,
    AssessSignature,
    AssessTaintRange,
    RouteSource,
    SourceType,
)
from contrast_vendor import structlog as logging
from contrast_vendor.webob.util import html_escape

logger = logging.getLogger("contrast")

INIT = "__init__"
INITIALIZERS = (INIT, "__new__")
NONE_STRING = str(None)


class Repr(reprlib.Repr):
    def repr_str(self, x, level):
        return x

    def repr_bytes(self, x, level):
        return x.decode(errors="replace")

    def repr_bytearray(self, x, level):
        return self.repr_bytes(x, level)

    def repr_instance(self, x, level):
        return f"{x.__class__.__module__}.{x.__class__.__qualname__}@{id(x):#x}"

    def repr_bool(self, x, level):
        return str(x)

    def repr_float(self, x, level):
        return str(x)

    def repr_NoneType(self, x, level):
        return "None"

    def repr_Pattern(self, x, level):
        return (
            self.repr1(x.pattern, level)
            if isinstance(x, re.Pattern)
            else self.repr_instance(x, level)
        )

    def repr_PurePath(self, x, level):
        return str(x) if isinstance(x, PurePath) else self.repr_instance(x, level)

    repr_PosixPath = repr_WindowsPath = repr_Path = repr_PurePosixPath = (
        repr_PureWindowsPath
    ) = repr_PurePath


class FullRepr(Repr):
    def repr_StringIO(self, x, level):
        return x.getvalue()

    def repr_BytesIO(self, x, level):
        return x.getvalue().decode(errors="replace")


class TruncatedRepr:
    def __init__(self, _repr: Repr):
        _repr = copy.copy(_repr)
        _repr.maxlevel = 3
        self._repr = _repr.repr

    def repr(self, obj: object):
        s = self._repr(obj)
        if len(s) > 103:
            s = s[:50] + "..." + s[-50:]
        return s


base_repr = Repr()
obj_repr = TruncatedRepr(base_repr)


def initialize(config: Mapping):
    """
    Initializes the module with common configuration settings.
    """
    global EVENT_FIELD_REPR, STACK_FILTER
    EVENT_FIELD_REPR = event_field_repr(config["assess.event_detail"])
    STACK_FILTER = stack_filter(config["assess.stacktraces"])


def event_field_repr(detail: str):
    """
    Returns a function to capture field details in events.
    """
    if detail == "minimal":
        return TruncatedRepr(base_repr)
    elif detail == "full":
        return TruncatedRepr(FullRepr())
    else:
        raise ValueError(f"Unknown event detail: {detail}")


def stack_filter(keep_level: str):
    """
    Returns a function to filter stack frames.
    """
    if keep_level == "ALL":
        return lambda action: False
    elif keep_level == "NONE":
        return lambda action: True
    elif keep_level == "SOME":
        return lambda action: action not in (
            AssessEventAction.CREATION,
            AssessEventAction.TRIGGER,
        )
    elif keep_level == "SINK":
        return lambda action: action != AssessEventAction.TRIGGER
    else:
        raise ValueError(f"Unknown stack level: {keep_level}")


EVENT_FIELD_REPR = event_field_repr("minimal")
STACK_FILTER = stack_filter("ALL")


@dataclass
class Field:
    type: type
    value: str

    def __init__(
        self, obj, typ=None, repr_func: Callable[[object], str] = EVENT_FIELD_REPR.repr
    ):
        self.type = typ or type(obj)
        self.value = repr_func(obj)


Location = Union[
    Literal["OBJ"],
    int,  # args index
    str,  # kwargs key
    Literal["RETURN"],
]
# variables can't be used within Literal, or the Union becomes
# a (variable) not a (type). So we have to duplicate the strings.
# This is an extra check to ensure that the strings are the same.
assert OBJECT == "OBJ"
assert RETURN == "RETURN"


class ContrastEvent:
    """
    This class holds the data about an event in the application
    We'll use it to build an event that TeamServer can consume if
    the object to which this event belongs ends in a trigger.
    """

    ATOMIC_ID = 0

    def __init__(
        self,
        node: PolicyNode,
        tagged: Any,
        self_obj: Any | None,
        ret: Any | None,
        args: Sequence[Any],
        kwargs: dict[str, Any],
        parents: list[ContrastEvent],
        possible_key=None,
        source_type: SourceType | None = None,
        source_name=None,
    ):
        self.node = node
        self._init_tagged(tagged, possible_key, args, kwargs)
        self.source_type = source_type
        self.source_name = source_name
        self.parents = parents or []
        ret = self._update_init_return(node, self_obj, ret)
        self.obj = Field(self_obj) if self_obj is not None else None
        self.ret = Field(ret) if ret is not None else None
        self.args = [Field(arg) for arg in args] if args is not None else []
        self.kwargs = (
            {
                k: Field(f"{k}={obj_repr.repr(v)}", typ=type(v))
                for k, v in kwargs.items()
            }
            if kwargs is not None
            else {}
        )

        # These are needed only at trigger-time but values must be set at init.
        self.time_ns = time.time_ns()
        self.thread = threading.current_thread().ident
        self.event_id = ContrastEvent._atomic_id()

        self.event_action = self.node.build_action()

        self._raw_stack = (
            build_stack()
            if not node.skip_stacktrace and not STACK_FILTER(self.event_action)
            else StackSummary()
        )

        # This must happen at init for stream events to work.
        self._update_method_information()

    def _init_tagged(self, tagged: Any, possible_key=None, args=None, kwargs=None):
        """
        Initialize properties related to tagging.
        - self.tagged
        - self.taint_location
        - self.span_override
        """
        self.taint_location: Location | None = (
            possible_key or self._find_taint_location(args, kwargs)
        )
        if self.taint_location and isinstance(tagged, dict):
            tagged = tagged.get(self.taint_location, None)
        tags = None
        self.tagged_props = get_properties(tagged)
        if self.tagged_props and isinstance(tagged, str):
            self.tagged_props.cleanup_tags()
            tags = [tag for tag in chain.from_iterable(self.tagged_props.tags.values())]
            tagged_repr, truncate_tags = truncate_tainted_string(tagged, tags)
            self.tagged = Field(tagged_repr, repr_func=base_repr.repr)
            self.tags_override = truncate_tags
        else:
            self.tagged = Field(tagged, repr_func=TruncatedRepr(FullRepr()).repr)
            self.tags_override = (
                None
                if len(self.tagged.value) == len_or_zero(tagged)
                else (Tag(len(self.tagged.value), 0),)
            )

    def _update_init_return(self, node, obj, ret):
        """
        For purposes of pretty reporting in Teamserver, we will say the
        `__init__` instance method return the `self` object (the object getting
        instantiated) instead of `None`, even though `None` is the return value of
        `__init__` methods.

        This will not apply if the node is not a class (it's possible someone
        creates a module level function called `__init__` or if the return
        value is already populated (for safety).
        """
        if node.method_name == INIT and node.class_name is not None:
            ret = ret or obj
        return ret

    @property
    def parent_ids(self):
        return [parent.event_id for parent in self.parents]

    @classmethod
    def _atomic_id(cls):
        ret = cls.ATOMIC_ID
        cls.ATOMIC_ID += 1
        return ret

    def _find_taint_location(self, args, kwargs) -> Location | None:
        """
        Find the location of the tagged value in the event. This is used to determine
        where the tagged value is in the event, so that we can mark it up in TeamServer.
        """
        if len(self.node.targets) == 1:
            return self.node.targets[0]
        for loc in chain(self.node.targets, self.node.sources):
            if loc in (OBJECT, RETURN):
                return loc
            if isinstance(loc, int) and loc < len(args):
                return loc
            if isinstance(loc, str) and loc in kwargs:
                return loc

        return None

    def _update_method_information(self):
        """
        For nicer reporting, we lie about the tagged value. For example, a call to
        split() returns a list of strings: ["foo", "bar"]. In the properties for "foo",
        the split event shows a return value of only "foo" instead of the whole list.
        """
        if self.taint_location is None:
            # This would be for trigger nodes without source or target. Trigger rule was
            # violated simply by a method being called. We'll save all the information,
            # but nothing will be marked up, as nothing need be tracked.
            return

        if self.taint_location == OBJECT:
            self.obj = self.tagged
            return

        if self.taint_location == RETURN:
            self.ret = self.tagged

    def to_reportable_event(self):
        """
        Convert a ContrastEvent to a AssessEvent.
        """
        event = AssessEvent(
            action=self.event_action,
            args=(
                [self._build_assess_object(arg, i) for i, arg in enumerate(self.args)]
                + [
                    self._build_assess_object(field, key)
                    for key, field in self.kwargs.items()
                ]
            ),
            event_sources=self._build_assess_event_sources(),
            field_name=self.source_name or "",
            object=self._build_assess_object(self.obj, OBJECT),
            object_id=self.event_id,
            parent_object_ids=[AssessParentObject(id=id) for id in self.parent_ids],
            ret=self._build_assess_object(self.ret, RETURN),
            signature=self._build_assess_signature(),
            source=self.node.ts_valid_source,
            target=self.node.ts_valid_target,
            stack=to_assess_stack(self._raw_stack),
            tags=",".join(self.node.tags),
            taint_ranges=[
                AssessTaintRange(tag=tr.tag, range=tr.range)
                for tr in (
                    self.tagged_props.tags_to_ts_obj() if self.tagged_props else []
                )
            ],
            thread=str(self.thread),
            time=self.time_ns // 1_000_000,
            type=self.node.node_type,
        )

        return event

    def build_route_source(self, safe_source_name: str) -> RouteSource:
        """
        Create a new RouteSource
        """
        assert self.source_type is not None
        return RouteSource(self.source_type, safe_source_name)

    def _build_assess_event_sources(self) -> list[AssessEventSource]:
        return (
            [
                AssessEventSource(
                    source_name=self.source_name or "", source_type=self.source_type
                )
            ]
            if self.source_type
            else []
        )

    def _build_assess_object(
        self, field: Field | None, location: Location
    ) -> AssessObject:
        # For now, only the taint_target needs to be officially marked as tracked.
        # This means that agent-tagged strings may not be marked as "tracked" for TS.
        return AssessObject(
            tracked=location == self.taint_location,
            value=base64_encode(field.value) if field else B64_NONE_STRING,
        )

    def _build_assess_signature(self) -> AssessSignature:
        return AssessSignature(
            arg_types=[
                self._type_string(arg) for arg in chain(self.args, self.kwargs.values())
            ],
            class_name=self.node.location.removeprefix("builtins."),
            constructor=self.node.method_name in INITIALIZERS,
            method_name=self.node.method_name,
            return_type=self._type_string(self.ret),
            void_method=False,
            expression_type=None,  # unused by us so far
            operator=None,  # unused by us so far
            signature=None,  # deprecated
            flags=0,  # only for the Java agent
        )

    def _type_string(self, field: Field | None) -> str:
        return field.type.__name__ if field else NONE_STRING

    def history(self: ContrastEvent):
        """
        Return a generator that yields all the events in the history of this event,
        starting with the event itself and then its parents, and so on.

        Events are yielded in depth-first order, so the event itself is yielded first,
        then its last parent, then the last parent of that parent, and so on.

        Events are deduplicated, so if an event is seen more than once, it will not be
        yielded again.
        """
        seen = set()
        queue = [self]
        while queue:
            event = queue.pop()
            seen.add(event)
            yield event
            queue.extend(event for event in event.parents if event not in seen)

    def dot_repr(self: ContrastEvent) -> str:
        """
        Returns a DOT graph representation of self's history.
        """
        return str(DotGraph(self))


@dataclass
class DotGraph:
    event: ContrastEvent
    normalize: bool = False
    _seen_events: dict[ContrastEvent, int] = field(default_factory=dict, init=False)

    def __str__(self):
        dot_lines = [
            "digraph {",
            "   node [shape=plain];",
        ]
        for event in self.event.history():
            dot_lines.append(self._node(event))
            dot_lines.extend(self._edge(parent, event) for parent in event.parents)
        dot_lines.append("}")
        return "\n".join(dot_lines)

    def _node(self, event: ContrastEvent) -> str:
        return f"""{self._event_id(event)} [label=<
        <table cellborder="0" cellspacing="10" style="rounded" {self._tooltip(event)}>
        <tr><td align="text" cellpadding="1"><b>{event.node}</b></td></tr>
        <tr><td><table cellborder="1" cellspacing="0" cellpadding="15">
            <tr><td align="text">data</td><td align="text"><font face="Monospace">{html_escape(event.tagged.value)}</font></td></tr>
            {"".join(f"<tr><td align='text'>{tag}</td><td align='text'><font face='Monospace'>{self._tagrng_markup(rngs, len(event.tagged.value), untagged_marker='&nbsp;')}</font></td></tr>" for tag, rngs in (event.tagged_props.tags.items() if event.tagged_props else []))}
        </table></td></tr>
        </table>>];"""

    def _edge(self, parent: ContrastEvent, child: ContrastEvent) -> str:
        return f"{self._event_id(parent)} -> {self._event_id(child)};"

    def _event_id(self, event: ContrastEvent) -> int:
        if self.normalize:
            if event not in self._seen_events:
                self._seen_events[event] = len(self._seen_events) + 1
            return self._seen_events[event]

        return event.event_id

    def _tooltip(self, event: ContrastEvent) -> str:
        if self.normalize:
            return ""

        # intentionally avoid using clean_stack because it formats filenames
        # replacing / with ., which makes them unusable as links.
        frame = next(
            (frame for frame in reversed(event._raw_stack) if acceptable_frame(frame)),
            None,
        )

        return (
            f'tooltip="{html_escape(frame.line)}" href="file://{frame.filename}"'
            if frame
            else ""
        )

    def _tagrng_markup(self, rngs, length, tag_marker="*", untagged_marker=" ") -> str:
        return "".join(
            tag_marker if any(rng.covers(i) for rng in rngs) else untagged_marker
            for i in range(length)
        )
