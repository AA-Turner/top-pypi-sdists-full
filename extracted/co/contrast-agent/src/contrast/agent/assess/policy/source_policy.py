# Copyright © 2025 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from collections.abc import Mapping
import functools

import contrast
from contrast.agent.assess.adjusted_span import AdjustedSpan
from contrast.agent.assess.policy.source_node import SourceNode
from contrast.agent.assess.properties import Properties
from contrast.agent.assess.utils import (
    get_properties,
    get_last_event_from_sources,
    is_trackable,
    set_properties,
    track_string,
)
from contrast.agent.policy.constants import OBJECT, RETURN
from contrast.utils.assess.duck_utils import is_iterable, safe_getattr, safe_iterator
from contrast.utils.decorators import fail_loudly, fail_quietly
from contrast.utils.safe_import import safe_import, safe_import_list
from contrast.utils.string_utils import truncated_signature

from tempfile import SpooledTemporaryFile

from contrast_vendor import structlog as logging

logger = logging.getLogger("contrast")


class Sentinel: ...


cgi_FieldStorage = safe_import("cgi.FieldStorage") or Sentinel


@functools.lru_cache(maxsize=1)
def _get_file_storage_types():
    return tuple(
        safe_import_list(
            "werkzeug.datastructures.FileStorage", "starlette.datastructures.UploadFile"
        )
    )


@functools.lru_cache(maxsize=1)
def _get_environ_headers_types():
    return tuple(safe_import_list("werkzeug.datastructures.EnvironHeaders"))


@functools.lru_cache(maxsize=1)
def _get_in_memory_uploaded_file_types():
    return tuple(
        safe_import_list("django.core.files.uploadedfile.InMemoryUploadedFile")
    )


@functools.lru_cache(maxsize=1)
def _get_file_field_types():
    return tuple(safe_import_list("aiohttp.web_request.FileField"))


def apply(nodes, self_obj, ret, orig_args, orig_kwargs=None, **kwargs):  # pylint: disable=redefined-builtin
    """
    Apply node into all sources to track all new strings coming in from a request
    """
    context = contrast.REQUEST_CONTEXT.get()
    if context is None or not context.assess_enabled:
        return

    file_storage_types = _get_file_storage_types()
    in_memory_uploaded_file_types = _get_in_memory_uploaded_file_types()
    for node in nodes:
        # args[0] is `self` for instance methods
        args = orig_args[1:] if node.instance_method else orig_args

        target = node.get_matching_first_target(self_obj, ret, args, orig_kwargs)

        source_type = node.type
        if isinstance(target, file_storage_types):
            # first, track the filename, if present
            filename = getattr(target, "filename", None)
            cs__apply_source(
                context,
                node,
                filename,
                target,
                filename,
                (),
                {},
                source_type="PARAMETER",
                source_name="filename",
            )
            # We don't try to propagate through werkzeug's file parsing logic, because
            # it causes massive slowdown. Instead, if we see a FileStorage object
            # come out of a multidict, we track it. We need to track the underlying
            # stream, not the FileStorage object itself.
            if hasattr(target, "stream"):
                # werkzeug case
                target = target.stream
            elif hasattr(target, "file"):
                # starlette case
                target = target.file
            source_type = "MULTIPART_CONTENT_DATA"
        elif isinstance(target, in_memory_uploaded_file_types):
            # same as above but for django
            source_type = "MULTIPART_CONTENT_DATA"
            if hasattr(target, "_name"):
                cs__apply_source(
                    context,
                    node,
                    target._name,
                    self_obj,
                    ret,
                    args,
                    orig_kwargs,
                    source_type=source_type,
                )
            target = target.file

        if hasattr(target, "cs__source"):
            # Target is already a source, nothing to do
            if target.cs__source:
                return

            target.cs__source = True
            target.cs__source_type = source_type
            target.cs__source_tags = node.tags
            set_properties(target, Properties(target))

        cs__apply_source(
            context,
            node,
            target,
            self_obj,
            ret,
            args,
            orig_kwargs,
            source_type=source_type,
        )


def adjust_source_tags(tags, source_type, source_name):
    """
    Update source tags to account for Referer header

    The XSS spec dictates that, with a single exception, no HTTP headers (or keys)
    should trigger XSS due to a high rate of false positives. The one exception is the
    'Referer' header. In order to account for this, we add the CROSS_SITE tag if the
    given source appears to correspond to this header value.
    """
    is_header = source_type == "HEADER"
    # This accounts for various representations of referer header keys, including
    # 'Referer' and 'HTTP_REFERER'
    is_referer = is_header and source_name and source_name.lower().endswith("referer")

    # According to XSS spec, the only header that should have CROSS_SITE is Referer.
    return (
        list(tags) + ["CROSS_SITE"]
        if (is_referer and "CROSS_SITE" not in tags)
        else list(tags)
    )


@fail_quietly("Error in apply_stream_source")
def apply_stream_source(method_name, target, self_obj, ret, args, kwargs):
    source_name = None
    context = contrast.REQUEST_CONTEXT.get()
    if context is None or not context.assess_enabled:
        return

    module = self_obj.__class__.__module__
    class_name = self_obj.__class__.__name__

    source_type = safe_getattr(self_obj, "cs__source_type", None) or "BODY"
    source_tags = safe_getattr(self_obj, "cs__source_tags", None) or ["UNTRUSTED"]

    if context.stop_source_creation(source_type, source_name):
        return

    node = SourceNode(
        module,
        class_name,
        True,
        method_name,
        "RETURN",
        source_type,
        tags=source_tags,
    )

    cs__apply_source(context, node, target, self_obj, ret, args, kwargs)


NAMED_SOURCE_TYPES = [
    "PARAMETER",
    "PARAMETER_KEY",
    "HEADER",
    "HEADER_KEY",
    "COOKIE",
    "COOKIE_KEY",
    "MULTIPART_HEADER",
    "MULTIPART_HEADER_KEY",
    "MULTIPART_PARAMETER",
    "MULTIPART_PARAMETER_KEY",
]


def _get_source_name(node, self_obj, args):
    """
    Determine name for source

    Some sources require a source name since there can potentially be multiple values
    for that given source type (e.g. multiple headers, cookies, etc.).

    If no source name is explicitly given, but we have a dict/mapping object, then we
    try to use the dict/mapping key as the source name. This assumes that the
    instrumented dict/mapping method is something like __getitem__.

    Otherwise, use the method name (e.g. for `flask.wrappers.Request.full_path`, the
    source name will be "full_path").
    """
    if args and isinstance(self_obj, (dict, Mapping) + _get_environ_headers_types()):
        return args[0]

    return node.method_name


def cs__apply_source(
    context,
    node,
    target,
    self_obj,
    ret,
    args,
    kwargs,
    source_name=None,
    source_type=None,
):
    logger.debug("In cs__apply_source for %r", node)

    if source_type is None:
        source_type = node.type

    if source_type in NAMED_SOURCE_TYPES and not source_name:
        source_name = _get_source_name(node, self_obj, args)

    if context.stop_source_creation(source_type, source_name):
        return

    _cs__apply_source(
        context,
        node,
        target,
        self_obj,
        ret,
        source_type,
        source_name,
        True,
        args,
        kwargs,
    )


@fail_loudly("Unable to apply source for node")
def _cs__apply_source(
    context,
    node,
    target,
    self_obj,
    ret,
    source_type,
    source_name,
    use_source_key,
    args,
    kwargs,
):
    if not context or not node or target is None:
        return

    if context.stop_source_creation(source_type, source_name):
        return

    target_properties = get_properties(target)
    if target_properties is not None and all(
        e.source_type == "COOKIE" for e in target_properties.events if e.source_type
    ):
        source_type = "COOKIE"
        # Discard any preexisting tags or events for this string. This greatly
        # simplifies reporting by retaining only the most recent source event for each
        # string
        target_properties.reset()
    if target_properties is None and is_trackable(target):
        target_properties = track_string(target)
    if target_properties is not None:
        if not safe_getattr(target, "cs__source", False):
            for tag in adjust_source_tags(node.tags, source_type, source_name):
                if source_type == "COOKIE" and tag == "CROSS_SITE":
                    continue

                target_properties.add_tag(tag, AdjustedSpan(0, len(target)))
                target_properties.add_properties(node.properties)

                logger.debug(
                    "Source %s detected: %s tagged with %s",
                    node.name,
                    truncated_signature(target),
                    str(tag),
                )

        parents = get_parents(node, self_obj, ret, args, kwargs)
        target_properties.build_event(
            node,
            target,
            self_obj,
            ret,
            args,
            kwargs,
            parents,
            possible_key=None,
            source_type=source_type,
            source_name=source_name,
        )

        # Only report the source if we have written policy for it.
        # If we were to report all sources, then events such as pre-tracking
        # the WSGI environ would result in a lot of noise. (PYT-825)
        if node.policy_patch:
            target_properties.report_source(target_properties.event)

        context.source_created()

        if is_trackable(target):
            set_properties(target, target_properties)

    elif isinstance(target, (dict, Mapping)):
        # This logic is intended to handle the case where the source is a dict
        # that happens to represent request parameters, headers, or cookies.
        # In these cases we want the top-level keys of this dictionary to be
        # labeled with the appropriate data type (e.g. PARAMETER_KEY). This
        # behavior should not apply to recursive calls, however.
        source_key_type = key_type(source_type) if use_source_key else source_type
        for key, value in target.items():
            _cs__apply_source(
                context,
                node,
                key,
                self_obj,
                ret,
                source_key_type,
                key,
                False,
                args,
                kwargs,
            )
            _cs__apply_source(
                context,
                node,
                value,
                self_obj,
                ret,
                source_type,
                key,
                False,
                args,
                kwargs,
            )

    elif isinstance(target, cgi_FieldStorage):
        # we have patches for this already and we don't want to fall into the
        # is_iterable case
        return

    elif isinstance(target, SpooledTemporaryFile):
        # circular import
        from contrast.utils.assess.stream_utils import ContrastFileProxy  # noqa

        target._file = ContrastFileProxy(target._file)
        target._file.cs__source_type = "MULTIPART_CONTENT_DATA"
        target._file.cs__source_tags = node.tags

    elif isinstance(target, _get_file_field_types()):
        # circular import
        from contrast.utils.assess.stream_utils import (
            ContrastBufferedReaderProxy,
        )  # noqa

        # these instances are frozen using a library called `attr`. The library
        # overrides __setattr__ for instances. The documented workaround is to use
        # `object`'s __setattr__ instead
        object.__setattr__(target, "file", ContrastBufferedReaderProxy(target.file))
        target.file.cs__source_type = "MULTIPART_CONTENT_DATA"
        target.file.cs__source_tags = node.tags

    elif is_iterable(target):
        for value in safe_iterator(target):
            _cs__apply_source(
                context,
                node,
                value,
                self_obj,
                ret,
                source_type,
                source_name,
                False,
                args,
                kwargs,
            )


def value_of_source(source, self_obj, ret, args, kwargs):
    if source == OBJECT:
        return self_obj

    if source == RETURN:
        return ret

    if not args:
        return self_obj

    if args and isinstance(source, int) and source < len(args):
        return args[source]

    if kwargs and source in kwargs:
        return kwargs[source]

    return None


def get_parents(node, self_obj, ret, args, kwargs):
    if isinstance(node, SourceNode):
        return []

    sources = [
        value_of_source(source, self_obj, ret, args, kwargs) for source in node.sources
    ]
    return get_last_event_from_sources(sources)


def build_source_node(source_dict, method_name, source_type):
    """
    Useful for explicit source tracking, ie scope tracking / aiohttp request tracking.

    Note that headers (including cookies) should not trigger XSS, per labs
    """
    tags = (
        ["CROSS_SITE"] if source_type not in ["HEADER", "COOKIE"] else ["NO_NEWLINES"]
    )

    node = SourceNode(
        method_name=method_name,
        node_type=source_type,
        tags=tags,
        **source_dict,
    )
    node.skip_stacktrace = True

    return node


KEY_MAPPING = {
    "PARAMETER": "PARAMETER_KEY",
    "HEADER": "HEADER_KEY",
    "COOKIE": "COOKIE_KEY",
}

PARAMETER_TYPE = "PARAMETER"
PARAMETER_KEY_TYPE = "PARAMETER_KEY"
HEADER_TYPE = "HEADER"
HEADER_KEY_TYPE = "HEADER_KEY"
COOKIE_TYPE = "COOKIE"
COOKIE_KEY_TYPE = "COOKIE_KEY"
QUERYSTRING_TYPE = "QUERYSTRING"


def key_type(source_type):
    return KEY_MAPPING.get(source_type, source_type)
