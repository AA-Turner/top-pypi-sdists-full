"""
CopyFromBase — abstract component for reading a remote file into a DataFrame.

Subclasses must override at least one of:
  - ``async _fetch_to_bytes(self) -> BytesIO``   — preferred in-memory path.
  - ``async _fetch_to_tempfile(self) -> Path``   — fallback when the SDK cannot stream.

Concrete subclasses (CopyFromS3, CopyFromSharepoint, etc.) implement the
network-IO half; this base owns the orchestration and parsing.
"""
from __future__ import annotations

import os
import tempfile
from collections.abc import Callable
from io import BytesIO
from pathlib import Path
from typing import Optional

import pandas

from ..exceptions import ComponentError, DataNotFound, EmptyFile  # noqa: F401
from .flow import FlowComponent
from ..components.pandas_io import read_to_dataframe


class CopyFromBase(FlowComponent):
    """Abstract: read a single remote file into a Pandas DataFrame.

    :interface: true

    Subclasses MUST override at least one of:
      - ``async _fetch_to_bytes(self) -> BytesIO``  (preferred, in-memory path)
      - ``async _fetch_to_tempfile(self) -> Path``  (fallback, when the SDK
        cannot accept a stream)

    Note: this class is unrelated to the existing ``flowtask/components/CopyTo.py``
    despite the shared prefix — ``CopyTo`` is DataFrame → database,
    ``CopyFromBase`` is remote-file → DataFrame.
    """

    _version = "1.0.0"

    def __init__(
        self,
        loop=None,
        job: Optional[Callable] = None,
        stat: Optional[Callable] = None,
        **kwargs,
    ) -> None:
        """Initialise the base, consuming all pandas_io read options from kwargs.

        Args:
            loop: Unused; accepted for API parity with other FlowComponent
                  subclasses that accept an event-loop reference.
            job: Optional job callable forwarded to FlowComponent.
            stat: Optional stat callable forwarded as a kwarg.
            **kwargs: All remaining keyword arguments.  pandas_io read options
                      are popped here; the remainder is forwarded to
                      FlowComponent.__init__.
        """
        # Consume pandas_io read options before forwarding to super.
        self.mime: str | None = kwargs.pop("mime", None)
        self.separator: str = kwargs.pop("separator", ",")
        self.decimal: str = kwargs.pop("decimal", ",")
        self.file_engine: str | None = kwargs.pop("file_engine", None)
        self.sheet_name = kwargs.pop("sheet_name", None)
        self.encoding: str | None = kwargs.pop("encoding", None)
        self.dtypes = kwargs.pop("dtypes", None)
        self.parse_dates = kwargs.pop("parse_dates", None)
        self.na_values = kwargs.pop("na_values", None)
        self.filter_nan: bool = kwargs.pop("filter_nan", True)
        self.remove_empty_strings: bool = kwargs.pop("remove_empty_strings", True)
        if stat is not None:
            kwargs.setdefault("stat", stat)
        # `loop` is intentionally not forwarded: FlowComponent.__init__ does not
        # accept it.  It is accepted here for API parity with other components.
        super().__init__(job=job, **kwargs)

    # ------------------------------------------------------------------
    # Abstract fetch interface — subclasses override exactly one
    # ------------------------------------------------------------------

    async def _fetch_to_bytes(self) -> BytesIO:
        """Fetch the remote resource and return it as a BytesIO buffer.

        Subclasses that can stream the resource entirely in memory MUST override
        this method.  The base raises ``NotImplementedError`` to signal the
        fallback path.

        Returns:
            A ``BytesIO`` buffer whose position is at 0, ready for reading.
        """
        raise NotImplementedError

    async def _fetch_to_tempfile(self) -> Path:
        """Fetch the remote resource and write it to a temporary file.

        Subclasses override this when the underlying SDK cannot stream to a
        BytesIO (e.g. SDKs that require a file path).  The base raises
        ``NotImplementedError``.

        Returns:
            A ``Path`` pointing to the temporary file.  The base will delete
            this file unconditionally after parsing (success or failure).
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
        """Orchestrate the fetch-then-parse pipeline.

        Execution order:
        1. Try ``_fetch_to_bytes()`` (preferred in-memory path).
        2. On ``NotImplementedError``, fall back to ``_fetch_to_tempfile()``.
           The temporary file is deleted unconditionally in a ``finally`` block
           (on both success and failure).
        3. Pass the buffer / path to ``pandas_io.read_to_dataframe``.
        4. Store result on ``self._result`` and return it.

        Returns:
            A ``pandas.DataFrame``.

        Raises:
            ComponentError: On parse failure or unexpected errors.
            EmptyFile: When the fetched resource is empty.
            DataNotFound: When the result DataFrame is None.
        """
        try:
            buf = await self._fetch_to_bytes()
            self._logger.debug(
                "%s: using in-memory BytesIO path", self.__class__.__name__
            )
            df = self._parse(buf)
        except NotImplementedError:
            self._logger.info(
                "%s: subclass does not support stream-read, falling back to tempfile",
                self.__class__.__name__,
            )
            path = await self._fetch_to_tempfile()
            if not isinstance(path, Path):
                path = Path(path)
            try:
                df = self._parse(path)
            finally:
                try:
                    os.unlink(path)
                except OSError as cleanup_err:
                    self._logger.warning(
                        "%s: failed to delete tempfile %s: %s",
                        self.__class__.__name__,
                        path,
                        cleanup_err,
                    )
                # Remove the parent tmpdir if it is a dedicated temp dir and now empty
                parent = path.parent
                if parent != Path(tempfile.gettempdir()) and parent.is_dir():
                    try:
                        parent.rmdir()  # only removes if empty
                    except OSError:
                        pass
        self._result = df
        return df

    def _parse(self, buf: BytesIO | str | Path) -> pandas.DataFrame:
        """Delegate to pandas_io.read_to_dataframe with stored options.

        Args:
            buf: A ``BytesIO``, file path string, or ``Path`` to parse.

        Returns:
            A ``pandas.DataFrame``.

        Raises:
            ComponentError: On parse failure.
            EmptyFile: When the source is empty.
        """
        try:
            return read_to_dataframe(
                buf,
                mime=self.mime,
                separator=self.separator,
                decimal=self.decimal,
                file_engine=self.file_engine,
                sheet_name=self.sheet_name,
                dtypes=self.dtypes,
                parse_dates=self.parse_dates,
                na_values=self.na_values,
                encoding=self.encoding,
                filter_nan=self.filter_nan,
                remove_empty_strings=self.remove_empty_strings,
            )
        except (ComponentError, EmptyFile, DataNotFound):
            raise
        except Exception as err:
            raise ComponentError(
                f"{self.__class__.__name__}: parse error: {err}"
            ) from err

    async def close(self) -> None:
        """No-op by default.

        Subclasses that hold open connections (e.g. S3 clients) should override
        this method to close them.
        """
        return None
