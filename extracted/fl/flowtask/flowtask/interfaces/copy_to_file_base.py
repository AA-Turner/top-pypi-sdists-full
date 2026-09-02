"""
CopyToFileBase — abstract component for writing a DataFrame to a remote file.

Subclasses must override at least one of:
  - ``async _put_from_bytes(self, buf: BytesIO) -> None``   — preferred in-memory path.
  - ``async _put_from_tempfile(self, path: Path) -> None``  — fallback when the SDK
    cannot accept a stream.

This class is independent of ``flowtask/components/CopyTo.py`` (the DB-targeted
DataFrame → database abstract). Same name family, separate hierarchies.
"""
from __future__ import annotations

import os
import tempfile
from collections.abc import Callable
from io import BytesIO
from pathlib import Path
from typing import Optional

import pandas

from ..exceptions import ComponentError, DataNotFound
from .flow import FlowComponent
from ..components.pandas_io import write_from_dataframe

_SUPPORTED_FORMATS = {"csv", "xlsx", "parquet", "json"}

_FORMAT_EXT: dict[str, str] = {
    "csv": ".csv",
    "xlsx": ".xlsx",
    "parquet": ".parquet",
    "json": ".json",
}


class CopyToFileBase(FlowComponent):
    """Abstract: serialize the current DataFrame and push it to a remote file target.

    :interface: true

    Subclasses MUST override at least one of:
      - ``async _put_from_bytes(self, buf: BytesIO) -> None``   (preferred)
      - ``async _put_from_tempfile(self, path: Path) -> None``  (fallback)

    The DataFrame returned by ``run()`` is the **same object** that was passed
    in via ``self.data`` — downstream components can chain without re-reading.

    Note: this class is unrelated to ``flowtask/components/CopyTo.py``
    (the DB-targeted abstract). Same prefix, separate hierarchies.
    """

    _version = "1.0.0"

    def __init__(
        self,
        loop=None,
        job: Optional[Callable] = None,
        stat: Optional[Callable] = None,
        **kwargs,
    ) -> None:
        """Initialise the base, consuming all write options from kwargs.

        Args:
            loop: Unused; accepted for API parity.
            job: Optional job callable forwarded to FlowComponent.
            stat: Optional stat callable forwarded as a kwarg.
            **kwargs: All remaining keyword arguments. Write options are popped
                      here; the remainder is forwarded to FlowComponent.__init__.

        Raises:
            ComponentError: If ``format`` is not a supported token.
        """
        self.format: str = kwargs.pop("format", "csv")
        if self.format not in _SUPPORTED_FORMATS:
            raise ComponentError(
                f"CopyToFileBase: unsupported format {self.format!r}. "
                f"Expected one of {sorted(_SUPPORTED_FORMATS)}."
            )
        self.separator: str = kwargs.pop("separator", ",")
        self.sheet_name: str = kwargs.pop("sheet_name", "Sheet1")
        self.index: bool = kwargs.pop("index", False)
        self.encoding: str = kwargs.pop("encoding", "utf-8")
        self.compression = kwargs.pop("compression", None)
        self.json_orient: str = kwargs.pop("json_orient", "records")
        self.json_lines: bool = kwargs.pop("json_lines", False)
        if stat is not None:
            kwargs.setdefault("stat", stat)
        # `loop` is intentionally not forwarded: FlowComponent.__init__ does not
        # accept it.  It is accepted here for API parity with other components.
        super().__init__(job=job, **kwargs)

    # ------------------------------------------------------------------
    # Abstract put interface — subclasses override exactly one
    # ------------------------------------------------------------------

    async def _put_from_bytes(self, buf: BytesIO) -> None:
        """Upload the serialised DataFrame from a BytesIO buffer.

        Subclasses that can stream bytes directly to the target MUST override
        this method.  The base raises ``NotImplementedError`` to signal fallback.

        Args:
            buf: A ``BytesIO`` whose position is at 0, ready for reading.
        """
        raise NotImplementedError

    async def _put_from_tempfile(self, path: Path) -> None:
        """Upload the serialised DataFrame from a temporary file path.

        Subclasses override this when the underlying SDK requires a file path
        rather than a stream.  The base raises ``NotImplementedError``.

        Args:
            path: Path to the temporary file.  The base will delete this file
                  unconditionally after this method returns (success or failure).
        """
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    async def start(self, **kwargs) -> bool:
        """Prepare the component for execution.

        Args:
            **kwargs: Forwarded to FlowComponent.start.

        Returns:
            ``True`` on success.
        """
        await super().start(**kwargs)
        return True

    async def run(self) -> pandas.DataFrame:
        """Orchestrate the serialise-then-upload pipeline.

        Execution order:
        1. Resolve ``self.data``; raise ``DataNotFound`` if ``None`` or empty.
        2. Serialise the DataFrame to a ``BytesIO`` via ``pandas_io.write_from_dataframe``.
        3. Try ``_put_from_bytes(buf)`` (preferred in-memory path).
        4. On ``NotImplementedError``, write to a ``NamedTemporaryFile`` and call
           ``_put_from_tempfile(path)``.  The tempfile is deleted unconditionally
           in a ``finally`` block.
        5. Store the input DataFrame on ``self._result`` and return it.

        Returns:
            The input ``pandas.DataFrame`` unchanged.

        Raises:
            DataNotFound: When ``self.data`` is ``None`` or empty.
            ComponentError: On serialisation or upload failure.
        """
        df = getattr(self, "data", None)
        if df is None or (hasattr(df, "empty") and df.empty):
            raise DataNotFound(f"{self.__class__.__name__}: no input DataFrame")

        buf = BytesIO()
        write_from_dataframe(
            df,
            self.format,
            buf,
            separator=self.separator,
            sheet_name=self.sheet_name,
            index=self.index,
            encoding=self.encoding,
            compression=self.compression,
            json_orient=self.json_orient,
            json_lines=self.json_lines,
        )
        buf.seek(0)

        try:
            await self._put_from_bytes(buf)
            self._logger.debug(
                "%s: used in-memory BytesIO path", self.__class__.__name__
            )
        except NotImplementedError:
            self._logger.info(
                "%s: subclass does not support stream-write, falling back to tempfile",
                self.__class__.__name__,
            )
            ext = _FORMAT_EXT[self.format]
            # Use delete=False: delete=True is unreliable on Windows and
            # prevents the subclass from reopening the file on some platforms.
            tmp = tempfile.NamedTemporaryFile(suffix=ext, delete=False)
            try:
                buf.seek(0)
                tmp.write(buf.read())
                tmp.flush()
                tmp.close()
                await self._put_from_tempfile(Path(tmp.name))
            finally:
                try:
                    os.unlink(tmp.name)
                except OSError as cleanup_err:
                    self._logger.warning(
                        "%s: failed to delete tempfile %s: %s",
                        self.__class__.__name__,
                        tmp.name,
                        cleanup_err,
                    )

        self._result = df
        return df

    async def close(self) -> None:
        """No-op by default.

        Subclasses that hold open connections should override this method.
        """
        return None
