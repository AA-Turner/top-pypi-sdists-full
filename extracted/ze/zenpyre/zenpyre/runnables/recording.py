r"""Provide a Runnable wrapper that records the input and output of each
invocation to a record store."""

from __future__ import annotations

__all__ = ["RecordingRunnable", "default_serialize"]

import logging
import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any, Generic, TypeVar

from coola.display import MultilineDisplayMixin
from langchain_core.runnables import Runnable

from zenpyre.records import Record
from zenpyre.utils.run import extract_run_id, extract_run_ids
from zenpyre.utils.serialization import default_serialize

if TYPE_CHECKING:
    from collections.abc import AsyncIterator, Callable, Iterator, Sequence

    from langchain_core.runnables import RunnableConfig

    from zenpyre.record_stores import BaseRecordStore

logger: logging.Logger = logging.getLogger(__name__)

Input = TypeVar("Input")
Output = TypeVar("Output")


class RecordingRunnable(Runnable[Input, Output], MultilineDisplayMixin, Generic[Input, Output]):
    r"""Wrap a Runnable to record the input and output of each invocation
    to a record store.

    This is a transparent passthrough wrapper: calling ``invoke``,
    ``ainvoke``, ``batch``, or ``abatch`` behaves exactly like calling
    the wrapped ``runnable`` directly (same return value, same
    exceptions), with the side effect of writing one
    :class:`~zenpyre.records.Record` per invocation to ``record_store``
    via :meth:`~zenpyre.record_stores.base.BaseRecordStore.add_records`.
    Each record gets a fresh, randomly generated ID (not derived from
    its content), so that two calls with identical input/output/extra
    are still both recorded rather than one silently overwriting the
    other via the store's upsert semantics.

    Note:
        If the wrapped ``runnable`` raises during ``invoke``/
        ``ainvoke``, the exception propagates immediately and *no*
        record is written for that call -- unlike ``batch``/``abatch``
        with ``return_exceptions=True``, which does record failed
        items (see ``"error"`` below). If you want failed single calls
        recorded too for a fully consistent audit trail, wrap the
        ``self._runnable.invoke(...)``/``ainvoke(...)`` calls in
        ``invoke``/``ainvoke`` in a try/except that builds an
        error record before re-raising, mirroring
        :meth:`_record_batch`'s handling.

    Each record's metadata is assembled as a plain dict with the
    following keys, then passed through ``serializer`` (see below) as
    a whole before being stored:

    * ``"input"`` / ``"output"``: the invocation's raw input and
      output.
    * ``"timestamp"``: an ISO 8601 UTC timestamp of when the call
      completed.
    * ``"run_id"``: the ``run_id`` from the call's ``RunnableConfig``,
      if the caller supplied one explicitly; otherwise ``None``. This
      is *not* LangChain's internally auto-generated run ID (that
      isn't accessible from a plain wrapper like this one), only one
      explicitly passed in by the caller.
    * ``"error"``: ``None`` on success. On a batch item that failed
      with ``return_exceptions=True``, this holds ``str(exception)``
      and ``"output"`` is ``None``.
    * Any additional keys from ``extra`` (fixed for this wrapper's
      lifetime, e.g. an experiment ID) and/or from the call's
      ``config["metadata"]`` (varies per invocation, e.g. a session or
      user ID). If the same key appears in both, the per-call
      ``config["metadata"]`` value wins. Neither may use one of the
      reserved keys above; doing so raises :exc:`ValueError`.

    ``stream``/``astream`` are supported on a best-effort basis: each
    chunk is yielded to the caller immediately (true streaming isn't
    delayed), while chunks are accumulated internally (via ``+``, as
    LangChain message chunks support) to reconstruct a final output
    for recording once the stream is exhausted. If chunks don't
    support ``+``, or the stream raises before completing, no record
    is written for that call (a warning is logged) rather than raising
    an error into the caller's stream.

    Args:
        runnable: The inner Runnable to wrap.
        record_store: The store to write input/output records to.
        extra: Additional metadata merged into every record written by
            this wrapper, fixed for its lifetime (e.g. an experiment
            ID). For metadata that varies per call, pass it via
            ``config={"metadata": {...}}`` on the individual
            ``invoke``/``batch``/... call instead; it takes precedence
            over ``extra`` on key collision. Must not use a reserved
            key (see above).
        serializer: A function applied to the whole assembled metadata
            dict before it's stored, to make it JSON-friendly (or to
            apply any other custom transform). Defaults to
            :func:`default_serialize`, applied to the whole dict (so
            it naturally recurses into ``"input"``, ``"output"``, and
            any ``extra``/``config["metadata"]`` values in one pass).

    Example:
        ```pycon
        >>> from zenpyre.record_stores import DuckDBRecordStore
        >>> from zenpyre.runnables import RecordingRunnable
        >>> store = DuckDBRecordStore(":memory:")
        >>> recorded = RecordingRunnable(
        ...     chat_model, store, extra={"experiment_id": "exp-42"}
        ... )  # doctest: +SKIP
        >>> recorded.invoke("Hello!", config={"metadata": {"session_id": "s-1"}})  # doctest: +SKIP
        AIMessage(content='Hi there!')
        >>> store.all()[0].metadata["experiment_id"], store.all()[0].metadata[
        ...     "session_id"
        ... ]  # doctest: +SKIP
        ('exp-42', 's-1')

        ```
    """

    @property
    def reserved_metadata_keys(self) -> frozenset[str]:
        """The metadata keys reserved for this class's own use.

        Neither ``extra`` nor a call's ``config["metadata"]`` may use
        one of these; doing so raises :exc:`ValueError`. A subclass may
        override this property to change the reserved set.
        """
        return frozenset({"input", "output", "timestamp", "run_id", "error"})

    def __init__(
        self,
        runnable: Runnable[Input, Output],
        record_store: BaseRecordStore,
        *,
        extra: dict[str, Any] | None = None,
        serializer: Callable[[dict[str, Any]], dict[str, Any]] | None = None,
    ) -> None:
        """Initialize the wrapper.

        Args:
            runnable: The inner Runnable to wrap and record calls of.
            record_store: The store to write input/output records to.
            extra: Additional metadata merged into every record
                written by this wrapper, fixed for its lifetime (e.g.
                an experiment ID). Must not contain a key from
                :attr:`reserved_metadata_keys`.
            serializer: A function applied to the whole assembled
                metadata dict before it's stored. Defaults to
                :func:`default_serialize` when ``None``.

        Raises:
            ValueError: If ``extra`` contains a key from
                :attr:`reserved_metadata_keys`.
        """
        reserved = self.reserved_metadata_keys & (extra or {}).keys()
        if reserved:
            msg = (
                f"'extra' must not contain a reserved key {sorted(self.reserved_metadata_keys)}; "
                f"got overlapping key(s) {sorted(reserved)} in extra={extra!r}."
            )
            raise ValueError(msg)
        self._runnable = runnable
        self._record_store = record_store
        # Copy, so mutating the caller's original dict after construction
        # doesn't silently leak into every subsequently written record.
        self._extra = dict(extra) if extra else {}
        self._serializer = serializer or default_serialize

    def invoke(
        self,
        input: Input,  # noqa: A002
        config: RunnableConfig | None = None,
        **kwargs: Any,
    ) -> Output:
        """Invoke the wrapped runnable and record the call.

        Calls ``self.runnable.invoke(input, config, **kwargs)``,
        writes one :class:`~zenpyre.records.Record` to the record
        store capturing ``input``, the returned output, a timestamp,
        and any ``run_id``/``extra`` metadata, then returns that
        output unchanged.

        Args:
            input: The input to pass to the wrapped runnable.
            config: Optional run configuration. If it has a
                ``"metadata"`` key, those entries are merged into the
                stored record (see the class docstring).
            **kwargs: Additional keyword arguments forwarded to the
                wrapped runnable's ``invoke``.

        Returns:
            The wrapped runnable's output, unchanged.

        Raises:
            Exception: Whatever the wrapped runnable itself raises. In
                that case, this method does not catch it, so no record
                is written for the failed call (see the class
                docstring's Note).
        """
        output = self._runnable.invoke(input, config=config, **kwargs)
        self._record(input, output, config=config)
        return output

    async def ainvoke(
        self,
        input: Input,  # noqa: A002
        config: RunnableConfig | None = None,
        **kwargs: Any,
    ) -> Output:
        """Asynchronously invoke the wrapped runnable and record the
        call.

        The async counterpart of :meth:`invoke`: calls
        ``self.runnable.ainvoke(input, config, **kwargs)``, writes one
        :class:`~zenpyre.records.Record` to the record store capturing
        ``input``, the returned output, a timestamp, and any
        ``run_id``/``extra`` metadata, then returns that output
        unchanged.

        Args:
            input: The input to pass to the wrapped runnable.
            config: Optional run configuration. If it has a
                ``"metadata"`` key, those entries are merged into the
                stored record (see the class docstring).
            **kwargs: Additional keyword arguments forwarded to the
                wrapped runnable's ``ainvoke``.

        Returns:
            The wrapped runnable's output, unchanged.

        Raises:
            Exception: Whatever the wrapped runnable itself raises. In
                that case, this method does not catch it, so no record
                is written for the failed call (see the class
                docstring's Note).
        """
        output = await self._runnable.ainvoke(input, config=config, **kwargs)
        self._record(input, output, config=config)
        return output

    def batch(
        self,
        inputs: list[Input],
        config: RunnableConfig | list[RunnableConfig] | None = None,
        *,
        return_exceptions: bool = False,
        **kwargs: Any,
    ) -> list[Output]:
        """Invoke the wrapped runnable on a list of inputs and record
        each call.

        Calls ``self.runnable.batch(inputs, config, return_exceptions,
        **kwargs)``, then writes one :class:`~zenpyre.records.Record`
        per ``(input, result)`` pair to the record store in a single
        :meth:`~zenpyre.record_stores.base.BaseRecordStore.add_records`
        call, before returning the results unchanged. Unlike
        :meth:`invoke`, a failed item (when ``return_exceptions=True``)
        is still recorded, with ``"error"`` set to ``str(exception)``
        and ``"output"`` set to ``None``.

        Args:
            inputs: The list of inputs to pass to the wrapped
                runnable.
            config: Optional run configuration, either a single config
                shared by every item or a list with one config per
                item (matching ``inputs`` in length and order). If a
                config has a ``"metadata"`` key, those entries are
                merged into that item's stored record.
            return_exceptions: If ``True``, exceptions raised by
                individual items are returned in ``results`` instead
                of propagating, and are still recorded (see above). If
                ``False``, an exception from any item propagates
                immediately from ``self.runnable.batch`` itself, and no
                records are written for this call at all.
            **kwargs: Additional keyword arguments forwarded to the
                wrapped runnable's ``batch``.

        Returns:
            One result per input, in the same order as ``inputs``,
                unchanged from what the wrapped runnable returned
                (which may include exception instances when
                ``return_exceptions=True``).
        """
        results = self._runnable.batch(
            inputs, config=config, return_exceptions=return_exceptions, **kwargs
        )
        self._record_batch(inputs, results, config)
        return results

    async def abatch(
        self,
        inputs: list[Input],
        config: RunnableConfig | list[RunnableConfig] | None = None,
        *,
        return_exceptions: bool = False,
        **kwargs: Any,
    ) -> list[Output]:
        """Asynchronously invoke the wrapped runnable on a list of
        inputs and record each call.

        The async counterpart of :meth:`batch`: calls
        ``self.runnable.abatch(inputs, config, return_exceptions,
        **kwargs)``, then writes one :class:`~zenpyre.records.Record`
        per ``(input, result)`` pair to the record store in a single
        :meth:`~zenpyre.record_stores.base.BaseRecordStore.add_records`
        call, before returning the results unchanged. Unlike
        :meth:`ainvoke`, a failed item (when ``return_exceptions=True``)
        is still recorded, with ``"error"`` set to ``str(exception)``
        and ``"output"`` set to ``None``.

        Args:
            inputs: The list of inputs to pass to the wrapped
                runnable.
            config: Optional run configuration, either a single config
                shared by every item or a list with one config per
                item (matching ``inputs`` in length and order). If a
                config has a ``"metadata"`` key, those entries are
                merged into that item's stored record.
            return_exceptions: If ``True``, exceptions raised by
                individual items are returned in ``results`` instead
                of propagating, and are still recorded (see above). If
                ``False``, an exception from any item propagates
                immediately from ``self.runnable.abatch`` itself, and
                no records are written for this call at all.
            **kwargs: Additional keyword arguments forwarded to the
                wrapped runnable's ``abatch``.

        Returns:
            One result per input, in the same order as ``inputs``,
                unchanged from what the wrapped runnable returned
                (which may include exception instances when
                ``return_exceptions=True``).
        """
        results = await self._runnable.abatch(
            inputs, config=config, return_exceptions=return_exceptions, **kwargs
        )
        self._record_batch(inputs, results, config)
        return results

    def stream(
        self,
        input: Input,  # noqa: A002
        config: RunnableConfig | None = None,
        **kwargs: Any,
    ) -> Iterator[Output]:
        """Stream the wrapped runnable's output chunks, recording an
        accumulated final result once the stream completes.

        Each chunk from ``self.runnable.stream(input, config,
        **kwargs)`` is yielded to the caller immediately, with no
        added latency. In parallel, chunks are accumulated via ``+``
        (see :func:`_try_add`) to reconstruct a final output. Once the
        stream is exhausted (in a ``finally`` block, so this also runs
        if the caller stops iterating early or the stream raises), one
        :class:`~zenpyre.records.Record` is written for the
        accumulated result, unless no chunk could be accumulated at
        all (in which case a warning is logged and nothing is
        recorded for this call).

        Args:
            input: The input to pass to the wrapped runnable.
            config: Optional run configuration. If it has a
                ``"metadata"`` key, those entries are merged into the
                stored record (see the class docstring).
            **kwargs: Additional keyword arguments forwarded to the
                wrapped runnable's ``stream``.

        Yields:
            Each output chunk from the wrapped runnable, unchanged and
                in the same order, as soon as it's produced.
        """
        accumulated: Any = None
        try:
            for chunk in self._runnable.stream(input, config=config, **kwargs):
                accumulated = chunk if accumulated is None else _try_add(accumulated, chunk)
                yield chunk
        finally:
            if accumulated is not None:
                self._record(input, accumulated, config=config)
            else:
                logger.warning(
                    "Could not accumulate a final output from the stream for %r; "
                    "no record was written for this call.",
                    self._runnable,
                )

    async def astream(
        self,
        input: Input,  # noqa: A002
        config: RunnableConfig | None = None,
        **kwargs: Any,
    ) -> AsyncIterator[Output]:
        """Asynchronously stream the wrapped runnable's output chunks,
        recording an accumulated final result once the stream completes.

        The async counterpart of :meth:`stream`: each chunk from
        ``self.runnable.astream(input, config, **kwargs)`` is yielded
        to the caller immediately, with no added latency. In parallel,
        chunks are accumulated via ``+`` (see :func:`_try_add`) to
        reconstruct a final output. Once the stream is exhausted (in a
        ``finally`` block, so this also runs if the caller stops
        iterating early or the stream raises), one
        :class:`~zenpyre.records.Record` is written for the
        accumulated result, unless no chunk could be accumulated at
        all (in which case a warning is logged and nothing is
        recorded for this call).

        Args:
            input: The input to pass to the wrapped runnable.
            config: Optional run configuration. If it has a
                ``"metadata"`` key, those entries are merged into the
                stored record (see the class docstring).
            **kwargs: Additional keyword arguments forwarded to the
                wrapped runnable's ``astream``.

        Yields:
            Each output chunk from the wrapped runnable, unchanged and
                in the same order, as soon as it's produced.
        """
        accumulated: Any = None
        try:
            async for chunk in self._runnable.astream(input, config=config, **kwargs):
                accumulated = chunk if accumulated is None else _try_add(accumulated, chunk)
                yield chunk
        finally:
            if accumulated is not None:
                self._record(input, accumulated, config=config)
            else:
                logger.warning(
                    "Could not accumulate a final output from the stream for %r; "
                    "no record was written for this call.",
                    self._runnable,
                )

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _record(
        self,
        input: Input,  # noqa: A002
        output: Any,
        *,
        config: RunnableConfig | None,
    ) -> None:
        """Build and store a single Record for one successful
        invocation.

        Assembles a metadata dict (``"input"``, ``"output"``,
        ``"timestamp"``, ``"run_id"``, ``"error"`` fixed at ``None``,
        plus whatever :meth:`_merge_extra` returns for ``config``),
        passes it through ``self._serializer``, wraps it in a
        :class:`~zenpyre.records.Record` with a fresh random ID (see
        the class docstring for why the ID isn't content-derived), and
        writes it via a single-item call to
        ``self._record_store.add_records``.

        Not called on ``invoke``/``ainvoke`` failure, since those
        methods don't catch exceptions from the wrapped runnable; see
        the class docstring's Note. Also not called directly for batch
        items, which go through :meth:`_record_batch` instead, since
        the assembly logic there additionally has to handle per-item
        failures.

        Args:
            input: The invocation's input, stored as-is under
                ``"input"`` (subject to ``self._serializer``).
            output: The invocation's output, stored as-is under
                ``"output"`` (subject to ``self._serializer``).
            config: The run configuration passed to the original call,
                if any, used both to extract a ``run_id`` and to merge
                in any ``config["metadata"]`` (via
                :meth:`_merge_extra`).
        """
        metadata = {
            "input": input,
            "output": output,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "run_id": extract_run_id(config),
            "error": None,
            **self._merge_extra(config),
        }
        # A fresh, random ID per call (not content-derived), so two
        # calls with identical metadata are both recorded rather than
        # one overwriting the other via the store's upsert semantics.
        record = Record(id=str(uuid.uuid4()), metadata=self._serializer(metadata))
        self._record_store.add_records([record])

    def _record_batch(
        self,
        inputs: Sequence[Input],
        results: Sequence[Any],
        config: RunnableConfig | list[RunnableConfig] | None,
    ) -> None:
        """Build and store one Record per (input, result) pair from a
        batch call, in a single add_records call.

        For each ``(input, result)`` pair (paired by position, so
        ``inputs`` and ``results`` must be the same length and in
        corresponding order, as ``batch``/``abatch`` guarantee),
        checks whether ``result`` is a ``BaseException`` instance
        (which happens when the wrapped runnable's batch call was
        given ``return_exceptions=True``). If so, the record's
        ``"output"`` is ``None`` and ``"error"`` is ``str(result)``;
        otherwise ``"output"`` is ``result`` and ``"error"`` is
        ``None``. Each item's metadata also gets its own ``run_id``
        (via :func:`~zenpyre.utils.run.extract_run_id`) and merged
        extra metadata (via :meth:`_merge_extra_list`), since a batch
        call's ``config`` may supply a different config per item. All
        resulting records are passed through ``self._serializer``
        individually, then written in a single call to
        ``self._record_store.add_records`` (one round trip for the
        whole batch, rather than one per item).

        Args:
            inputs: The inputs passed to the batch call, in order.
            results: The corresponding results (or, for failed items
                with ``return_exceptions=True``, exception instances),
                in the same order as ``inputs``.
            config: The run configuration passed to the original batch
                call: either a single config shared by every item, a
                list with one config per item, or ``None``.
        """
        run_ids = extract_run_ids(config, len(inputs))
        extras = self._merge_extra_list(config, len(inputs))
        records = []
        for item_input, result, run_id, extra in zip(inputs, results, run_ids, extras):
            is_error = isinstance(result, BaseException)
            metadata = {
                "input": item_input,
                "output": None if is_error else result,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "run_id": run_id,
                "error": str(result) if is_error else None,
                **extra,
            }
            records.append(Record(id=str(uuid.uuid4()), metadata=self._serializer(metadata)))
        self._record_store.add_records(records)

    def _merge_extra(self, config: RunnableConfig | None) -> dict[str, Any]:
        """Merge constructor-level ``extra`` with one call's
        ``config["metadata"]``, validating neither uses a reserved key.

        Reads ``config["metadata"]`` (an empty dict if ``config`` is
        ``None`` or has no ``"metadata"`` key), checks it against
        :attr:`reserved_metadata_keys`, then merges it on top of
        ``self._extra`` using dict unpacking, so a key present in both
        takes its value from ``config["metadata"]`` (the per-call
        value is more specific, so it wins over the wrapper-level
        default).

        Args:
            config: The run configuration for one call, or ``None``.

        Returns:
            A new dict combining ``self._extra`` and
                ``config["metadata"]``, with the latter's values
                overriding on key collision.

        Raises:
            ValueError: If ``config["metadata"]`` contains a key from
                :attr:`reserved_metadata_keys`.
        """
        call_metadata = (config or {}).get("metadata") or {}
        reserved = self.reserved_metadata_keys & call_metadata.keys()
        if reserved:
            msg = (
                f"config['metadata'] must not contain a reserved key "
                f"{sorted(self.reserved_metadata_keys)}; got overlapping key(s) "
                f"{sorted(reserved)} in metadata={call_metadata!r}."
            )
            raise ValueError(msg)
        return {**self._extra, **call_metadata}

    def _merge_extra_list(
        self, config: RunnableConfig | list[RunnableConfig] | None, n: int
    ) -> list[dict[str, Any]]:
        """Compute one merged extra-metadata dict per item for a batch
        call.

        A batch call's ``config`` may be a single ``RunnableConfig``
        shared by every item, a list with one ``RunnableConfig`` per
        item, or ``None``. This normalizes all three cases into a list
        of exactly ``n`` merged metadata dicts, one per item, in
        order:

        * If ``config`` is a list, each item's config is combined with
            the constructor-level ``extra`` independently (so, for
            example, item 0's ``config["metadata"]`` only affects item
            0's record, not the others), with each item's
            ``config["metadata"]`` overriding ``extra`` on key
            collision, and each independently validated to reject
            reserved keys.
        * Otherwise (a single config or ``None``), the same merged
            dict is computed once and repeated ``n`` times, since every
            item shares the same config.

        Args:
            config: The run configuration passed to the original batch
                call: either a single config shared by every item, a
                list with one config per item, or ``None``.
            n: The number of items in the batch (the length of
                ``inputs`` in the calling batch/abatch method). Used
                both to validate/repeat a shared config, and as the
                expected length of the returned list.

        Returns:
            A list of merged extra-metadata dicts, one per item. When
                ``config`` is a list, the returned list's length
                follows ``config``'s length, not ``n`` (this method
                doesn't itself validate that they match; a mismatch
                would surface downstream in :meth:`_record_batch`,
                where ``zip`` silently stops at the shortest of
                ``inputs``, ``results``, and this list). When
                ``config`` is a single config or ``None``, the
                returned list is always exactly length ``n``.

        Raises:
            ValueError: If any per-item ``config["metadata"]`` (or the
                single shared one) contains a key from
                :attr:`reserved_metadata_keys`.
        """
        if isinstance(config, list):
            return [self._merge_extra(c) for c in config]
        merged = self._merge_extra(config)
        return [merged] * n

    def _get_repr_kwargs(self) -> dict[str, Any]:
        """Return the fields shown in this object's repr.

        Used by :class:`~coola.display.MultilineDisplayMixin` to build
        this class's ``__repr__``. Deliberately excludes ``extra`` and
        ``serializer``, keeping the repr focused on the two fields
        that identify what's being wrapped and where records go.

        Returns:
            A dict with ``"runnable"`` and ``"record_store"`` entries.
        """
        return {"runnable": self._runnable, "record_store": self._record_store}


def _try_add(accumulated: Any, chunk: Any) -> Any:
    """Attempt to accumulate a stream chunk into a running total via
    ``+``.

    Used by :meth:`RecordingRunnable.stream` and
    :meth:`RecordingRunnable.astream` to reconstruct a final output
    from individual chunks for recording purposes, without delaying
    the chunks yielded to the caller. Many LangChain streaming output
    types (e.g. ``AIMessageChunk``) implement ``__add__`` for exactly
    this purpose; plain strings also support ``+`` naturally. If the
    chunk type doesn't support addition with the accumulated value, a
    warning is logged and the previous accumulation is returned
    unchanged (dropping this chunk from the eventual recorded output,
    rather than raising into the caller's stream).

    Args:
        accumulated: The running total accumulated from prior chunks.
        chunk: The newly received chunk to add to ``accumulated``.

    Returns:
        ``accumulated + chunk`` if that succeeds; otherwise
            ``accumulated`` unchanged.
    """
    try:
        return accumulated + chunk
    except TypeError:
        logger.warning(
            "Chunk of type %s does not support '+'; stream accumulation for "
            "recording may be incomplete.",
            type(chunk).__name__,
        )
        return accumulated
