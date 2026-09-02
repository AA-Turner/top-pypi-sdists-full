"""
DownloadFromGamma
Download a Gamma.app document (or a batch of documents) and save as Markdown.

Single-document example:

```yaml
DownloadFromGamma:
  source:
    url: https://gamma.app/docs/ATandT-Prepaid-WSP-Field-Reference-Guide-0aituhbc1mupp5b
  destination:
    directory: /home/ubuntu/symbits/gamma/
  create_destination: true
```

Batch-mode example (DataFrame piped from previous step — smart column detection):

```yaml
DownloadFromGamma:
  source:
    url: gamma_url          # "gamma_url" is a column in the piped DataFrame
  destination:
    directory: /home/ubuntu/symbits/gamma/{category}/
    filename: doc_name       # "doc_name" is a column -> per-row filename
  create_destination: true
```
"""
import re
import asyncio
from pathlib import Path
from typing import Optional, Union
from collections.abc import Callable

import aiofiles

from ..exceptions import ComponentError, ConfigError
from ..interfaces.download_from import DownloadFromBase
from ..interfaces.gamma import GammaClient, extract_doc_id, snapshot_to_markdown


class DownloadFromGamma(GammaClient, DownloadFromBase):
    """
    DownloadFromGamma

    **Overview**

        Download one or more public Gamma.app documents and save them as
        Markdown files. Fetches documents via Gamma's GraphQL API (no
        credentials required for public documents), converts ProseMirror
        snapshots to Markdown, and writes results to the configured
        destination.

        **Single mode**: ``source.url`` or ``source.document`` selects one
        document; behaves like any other ``DownloadFrom*`` component.

        **Batch mode**: when a DataFrame is piped from a previous component,
        if ``source.url`` (or ``source.document``) exactly matches a column
        name in the DataFrame the component enters batch mode automatically.
        ``destination.filename`` and ``destination.directory`` are also treated
        as column references when they exactly match a column name; otherwise
        they are treated as mask/template strings (``{col}`` tokens supported).

    **Properties**

        | source.url            | Yes*  | Full Gamma URL (single mode) or column name (batch). |
        | source.document       | Yes*  | Document slug / ID (single mode) or column name (batch). |
        | destination.directory |  Yes  | Target directory; column name -> per-row dir;       |
        |                       |       | otherwise supports masks and ``{col}`` tokens.     |
        | destination.filename  |  No   | Column name -> per-row filename; otherwise a mask / |
        |                       |       | ``{col}`` template. Default: sanitized title + .md. |
        | create_destination    |  No   | Create ``directory`` if missing (default: False).  |
        | overwrite             |  No   | Overwrite existing file (default: True).           |
        | timeout               |  No   | HTTP timeout in seconds (default: 30).             |

        *  Exactly one of ``source.url`` / ``source.document`` required.

    **Return — single mode**

        Dict with ``filename``, ``title``, ``doc_id``, ``snapshot_id`` keys.
        Metrics: ``GAMMA_DOC_ID``, ``GAMMA_TITLE``, ``GAMMA_FILENAME``,
        ``GAMMA_MD_BYTES``.

    **Return — batch mode**

        Input DataFrame augmented with ``gamma_filename``, ``gamma_title``,
        and ``gamma_status`` columns.
        Metrics: ``GAMMA_BATCH_TOTAL``, ``GAMMA_BATCH_OK``,
        ``GAMMA_BATCH_SKIPPED``, ``GAMMA_BATCH_ERROR``.

    **Example: explicit filename with date masks**

    ```yaml
      DownloadFromGamma:
        source:
          document: ATandT-Prepaid-WSP-Field-Reference-Guide-0aituhbc1mupp5b
        destination:
          directory: /home/ubuntu/symbits/gamma/{Y}/{m}/
          filename: att_prepaid_wsp_{Y}{m}{d}.md
        create_destination: true
        overwrite: true
        timeout: 30
    ```

    **Example: batch with per-row directory and filename from columns**

    ```yaml
      DownloadFromGamma:
        source:
          url: gamma_url          # column name -> batch mode
        destination:
          directory: /home/ubuntu/gamma/{category}/   # {col} template
          filename: doc_name      # column name -> per-row filename
        create_destination: true
    ```
    """
    _version = "1.2.0"

    def __init__(
        self,
        loop: Optional[asyncio.AbstractEventLoop] = None,
        job: Optional[Union[Callable, list]] = None,
        stat: Optional[Callable] = None,
        **kwargs,
    ) -> None:
        # GammaClient.__init__ called first (MRO); sets _gamma_jar / _gamma_session.
        # DownloadFromBase.__init__ handles timeout, overwrite, create_destination.
        super().__init__(loop=loop, job=job, stat=stat, **kwargs)
        # Single-mode state (resolved in start())
        self._doc_id: str = ""
        self._public_url: str = ""
        # Batch-mode state (resolved in start() via smart column detection)
        self._batch_mode: bool = False
        self._url_column: Optional[str] = None
        self._document_column: Optional[str] = None
        self._filename_column: Optional[str] = None

    def _is_column(self, value: str) -> bool:
        """Return True when value exactly matches a column name in self.data."""
        if self.data is None:
            return False
        return str(value).strip() in self.data.columns

    async def start(self, **kwargs) -> bool:
        """Validate configuration, detect mode, and resolve source + destination.

        Smart column detection: if ``source.url`` or ``source.document`` exactly
        matches a column in the piped DataFrame, batch mode is activated
        automatically.  No explicit ``url_column`` / ``document_column`` keys are
        needed (and using them raises ``ConfigError``).

        Args:
            **kwargs: Forwarded to parent ``start()``.

        Returns:
            True on success.

        Raises:
            ConfigError: If ``source`` is missing, deprecated ``*_column`` keys
                are present, or no ``url``/``document`` is provided.
        """
        source = getattr(self, "source", None)
        if not source:
            raise ConfigError(
                "DownloadFromGamma: 'source' is required (provide source.url or "
                "source.document)"
            )

        # Guard against deprecated keys
        for deprecated in ("url_column", "document_column"):
            if isinstance(source, dict) and deprecated in source:
                raise ConfigError(
                    f"DownloadFromGamma: 'source.{deprecated}' is no longer supported. "
                    f"Use 'source.url' or 'source.document' with the column name directly."
                )
        dest = getattr(self, "destination", {}) or {}
        if isinstance(dest, dict) and "filename_column" in dest:
            raise ConfigError(
                "DownloadFromGamma: 'destination.filename_column' is no longer supported. "
                "Use 'destination.filename: <column_name>' directly."
            )

        gamma_url = source.get("url") if isinstance(source, dict) else None
        gamma_doc = source.get("document") if isinstance(source, dict) else None

        if self.previous:
            # Load DataFrame so _is_column() can inspect its columns
            self.data = self.input

            if self.data is not None:
                url_col = gamma_url if gamma_url and self._is_column(gamma_url) else None
                doc_col = gamma_doc if gamma_doc and self._is_column(gamma_doc) else None

                if url_col or doc_col:
                    # -- Batch mode -------------------------------------------
                    # Disable create_destination during super().start() so the
                    # base class does not mkdir a path with unresolved {col} tokens.
                    _orig_create = self.create_destination
                    self.create_destination = False
                    try:
                        await super(DownloadFromGamma, self).start(**kwargs)
                    finally:
                        self.create_destination = _orig_create

                    self._batch_mode = True
                    self._url_column = url_col
                    self._document_column = doc_col

                    # destination.filename may itself be a column reference
                    dest_fn = dest.get("filename")
                    self._filename_column = (
                        dest_fn if dest_fn and self._is_column(dest_fn) else None
                    )

                    if hasattr(self.data, "empty") and self.data.empty:
                        raise ConfigError(
                            "DownloadFromGamma: batch mode requires a non-empty DataFrame "
                            "from the previous component"
                        )
                    self._logger.info(
                        f"DownloadFromGamma: batch mode — {len(self.data)} rows, "
                        f"source column: '{url_col or doc_col}'"
                    )
                    return True

                # source value is not a column name -> fall through to single mode
                self.data = None

        # -- Single mode -------------------------------------------------------
        if not gamma_url and not gamma_doc:
            raise ConfigError(
                "DownloadFromGamma: source must contain 'url' or 'document'"
            )

        await super(DownloadFromGamma, self).start(**kwargs)

        if gamma_url:
            self._doc_id = extract_doc_id(str(gamma_url))
            self._public_url = str(gamma_url)
        else:
            self._doc_id = extract_doc_id(str(gamma_doc))
            self._public_url = f"https://gamma.app/docs/{gamma_doc}"

        self._logger.debug(
            f"DownloadFromGamma: doc_id={self._doc_id!r}, "
            f"public_url={self._public_url!r}"
        )
        return True

    async def run(self):
        """Download document(s) and write Markdown file(s).

        Returns:
            dict: Single-mode result with ``filename``, ``title``, ``doc_id``,
                ``snapshot_id`` (plus ``skipped: True`` when overwrite=False and
                file already exists).
            pandas.DataFrame: Batch-mode result — input DataFrame with
                ``gamma_filename``, ``gamma_title``, ``gamma_status`` appended.

        Raises:
            ComponentError: On GraphQL errors, HTTP 403, or write failures
                (single mode only; batch mode captures errors per row).
        """
        if self._batch_mode:
            return await self._run_batch()

        # -- Single mode -------------------------------------------------------
        # 1. Warm-up (tolerates failures)
        await self.warm_up(self._public_url)

        # 2. Fetch metadata
        doc = await self.get_document(self._doc_id)
        self._logger.info(
            f"Gamma document: {doc['title']!r} (snapshot {doc['snapshot_id']})"
        )

        # 3. Fetch snapshot content
        content = await self.get_snapshot(doc["snapshot_id"])

        # 4. Convert to Markdown
        markdown = snapshot_to_markdown(doc["title"], content)

        # 5. Resolve output path
        if self.filename:
            output_path = Path(self.filename)
        else:
            safe = re.sub(r"\s+", "_", re.sub(r"[^\w\s-]", "", doc["title"]).strip())
            output_path = Path(self.directory) / f"{safe}.md"

        # 6. Honour overwrite flag
        if output_path.exists() and not self.overwrite:
            self._logger.warning(
                f"DownloadFromGamma: {output_path} already exists and "
                "overwrite=False, skipping"
            )
            self._result = {"filename": str(output_path), "skipped": True}
            return self._result

        # 7. Write file
        try:
            async with aiofiles.open(output_path, "w", encoding="utf-8") as fh:
                await fh.write(markdown)
        except OSError as exc:
            raise ComponentError(
                f"DownloadFromGamma: could not write {output_path}: {exc}"
            ) from exc

        # 8. Store result and metrics
        self._result = {
            "filename": str(output_path),
            "title": doc["title"],
            "doc_id": self._doc_id,
            "snapshot_id": doc["snapshot_id"],
        }
        self.add_metric("GAMMA_DOC_ID", self._doc_id)
        self.add_metric("GAMMA_TITLE", doc["title"])
        self.add_metric("GAMMA_FILENAME", str(output_path))
        self.add_metric("GAMMA_MD_BYTES", len(markdown.encode()))

        self._logger.notice(f"Gamma document saved: {output_path}")
        return self._result

    async def _run_batch(self):
        """Download one Gamma document per DataFrame row.

        Iterates ``self.data`` sequentially; per-row errors are captured
        without aborting the rest of the batch.

        Returns:
            pandas.DataFrame: Input DataFrame with ``gamma_filename``,
                ``gamma_title``, and ``gamma_status`` columns appended.
        """
        assert self.data is not None, "_run_batch called without DataFrame"
        filenames, titles, statuses = [], [], []
        src_col = self._url_column or self._document_column
        total = len(self.data)

        for idx, row in self.data.iterrows():
            raw = str(row[src_col])
            try:
                doc_id = extract_doc_id(raw)
                public_url = (
                    raw if self._url_column else f"https://gamma.app/docs/{raw}"
                )

                output_path = self._resolve_batch_path(row)

                if Path(output_path).exists() and not self.overwrite:
                    self._logger.warning(
                        f"DownloadFromGamma: row {idx} — {output_path} exists, skipping"
                    )
                    filenames.append(str(output_path))
                    titles.append(None)
                    statuses.append("skipped")
                    continue

                await self.warm_up(public_url)
                doc = await self.get_document(doc_id)
                content = await self.get_snapshot(doc["snapshot_id"])
                markdown = snapshot_to_markdown(doc["title"], content)

                out = Path(output_path)
                if self.create_destination:
                    out.parent.mkdir(parents=True, exist_ok=True)

                async with aiofiles.open(out, "w", encoding="utf-8") as fh:
                    await fh.write(markdown)

                self._logger.debug(f"DownloadFromGamma: row {idx} -> {out}")
                filenames.append(str(out))
                titles.append(doc["title"])
                statuses.append("ok")

            except Exception as exc:
                self._logger.warning(
                    f"DownloadFromGamma: row {idx} error — {exc}"
                )
                filenames.append(None)
                titles.append(None)
                statuses.append(f"error:{exc}")

        self.data = self.data.assign(
            gamma_filename=filenames,
            gamma_title=titles,
            gamma_status=statuses,
        )

        ok = statuses.count("ok")
        skipped = statuses.count("skipped")
        errors = sum(1 for s in statuses if s.startswith("error:"))
        self._logger.notice(
            f"DownloadFromGamma batch: {ok} ok, {skipped} skipped, "
            f"{errors} errors out of {total} rows"
        )
        self.add_metric("GAMMA_BATCH_TOTAL", total)
        self.add_metric("GAMMA_BATCH_OK", ok)
        self.add_metric("GAMMA_BATCH_SKIPPED", skipped)
        self.add_metric("GAMMA_BATCH_ERROR", errors)
        self._result = self.data
        return self.data

    def _resolve_batch_path(self, row) -> str:
        """Resolve the output file path for a single DataFrame row.

        If ``destination.directory`` or ``destination.filename`` exactly matches
        a column name, the per-row column value is used directly.  Otherwise
        mask replacement and ``{col}`` token substitution are applied.

        Args:
            row: A pandas Series representing one DataFrame row.

        Returns:
            Absolute output path string.
        """
        assert self.data is not None, "_resolve_batch_path called without DataFrame"
        dest = getattr(self, "destination", {}) or {}

        # 1. Resolve directory
        dir_val = str(dest.get("directory") or self.directory or ".")
        if self._is_column(dir_val):
            directory = str(row[dir_val])
        else:
            if hasattr(self, "masks"):
                dir_val = self.mask_replacement(dir_val)
            for col in self.data.columns:
                dir_val = dir_val.replace(f"{{{col}}}", str(row[col]))
            directory = dir_val

        # 2. Resolve filename
        if self._filename_column:
            # Set in start() when dest.filename matched a column name
            fname = str(row[self._filename_column])
            if not fname.endswith(".md"):
                fname += ".md"
        else:
            fn_val = dest.get("filename")
            if fn_val:
                fn_str = str(fn_val)
                if hasattr(self, "masks"):
                    fn_str = self.mask_replacement(fn_str)
                for col in self.data.columns:
                    fn_str = fn_str.replace(f"{{{col}}}", str(row[col]))
                fname = fn_str
            else:
                # Default: sanitize the raw source value as filename placeholder
                src_col = self._url_column or self._document_column
                raw = str(row[src_col])
                safe = re.sub(r"\s+", "_", re.sub(r"[^\w\s-]", "", raw).strip())
                fname = f"{safe}.md"

        return str(Path(directory) / fname)

    async def close(self) -> None:
        """Close the underlying aiohttp session."""
        await GammaClient.close(self)
