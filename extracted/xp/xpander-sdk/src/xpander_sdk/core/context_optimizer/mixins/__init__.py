"""Behavior mixins for ``XPanderContextOptimizer``.

Each mixin owns one orthogonal concern (chunked map-reduce summarization,
activity event publishing, etc.) so the optimizer's main file stays small
enough to read end-to-end. Mixins declare no fields — those live on the
final dataclass — and reference shared state via ``self.<field>``; the MRO
resolves the lookup at runtime.

Adding a new mixin:

1. Drop a class in this package (``class FooMixin:``) with no
   ``__init__`` / ``__post_init__``.
2. Add it to the inheritance list of ``XPanderContextOptimizer`` (mixins
   first, then ``CompressionManager``).
3. Move methods over without changing their bodies — they can keep using
   ``self.<field>`` without re-declaration.
"""

from xpander_sdk.core.context_optimizer.mixins.map_reduce import MapReduceMixin

__all__ = ["MapReduceMixin"]
