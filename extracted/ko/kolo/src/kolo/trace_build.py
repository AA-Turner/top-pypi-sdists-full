"""Compatibility names for Kolo's v3 trace writer.

New code should import these helpers from :mod:`kolo.trace_container`.
"""

from .trace_container import build_v3_trace, iter_v3_trace_chunks


def iter_serialized_trace_chunks(**kwargs):
    return iter_v3_trace_chunks(**kwargs)


def build_serialized_trace(**kwargs):
    return build_v3_trace(**kwargs)
