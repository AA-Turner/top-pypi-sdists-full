"""
Zoom Phone Component for FlowTask.

Concrete implementation of ZoomInterface using the standard HTTP layer
provided by the interface.  Supports the following operation types:

- ``call_logs`` fetch call logs with optional recording / transcript
  downloads.
- ``call_detail`` fetch full detail (all legs) for specific call UUIDs.
- ``sms`` fetch SMS sessions and messages for given phone numbers or
  extensions.
- ``recordings`` fetch account-level recordings for a date range with
  optional file downloads.

Usage in a FlowTask YAML::

    ZoomUs:
      type: call_logs
      from_date: "2025-01-01"
      to_date: "2025-01-31"
      download: true
      download_transcripts: true

    ZoomUs:
      type: recordings
      from_date: "2025-01-01"
      to_date: "2025-01-31"
      download: true
      recording_type: automatic

    ZoomUs:
      type: sms
      from_date: "2025-01-01"
      to_date: "2025-01-31"
      phone_numbers: "18001234567,18007654321"
"""
import asyncio
import os
import time
from collections.abc import Callable
from datetime import datetime, timedelta
from io import BytesIO
from pathlib import Path
from typing import Optional, Dict, Any, List
import pandas as pd
from tqdm import tqdm
import boto3
from ..conf import AWS_CREDENTIALS
from ..interfaces.zoom import ZoomInterface
from ..interfaces.cache import CacheSupport
from ..interfaces.Boto3Client import Boto3Client
from ..interfaces.qs import QSSupport
from ..interfaces.flow import FlowComponent
from ..interfaces.zoom import RecordingType
from datetime import datetime as _dt
from ..exceptions import ComponentError, ConfigError, DataNotFound
from ..conf import (
    ZOOM_ACCOUNT_ID,
    ZOOM_CLIENT_ID,
    ZOOM_CLIENT_SECRET,
)


class ZoomUs(ZoomInterface, CacheSupport, Boto3Client, QSSupport, FlowComponent):
    """Zoom Phone Component for FlowTask (interface-based).

    1:1 replacement for the master ``Zoom`` component.  All Zoom API
    interactions go through ``ZoomInterface``; business logic (S3,
    database auto-skip, ``as_bytes`` mode, tqdm) lives here.

    Args:
        type: ``call_logs`` (default) or ``sms``.
        from_date: Start date ``YYYY-MM-DD``.
        to_date: End date ``YYYY-MM-DD``.
        download: Download recordings (default ``True``).
        download_transcripts: Download transcripts (default ``True``).
        as_bytes: Keep files in memory as ``BytesIO`` (default ``False``).
        auto_skip_processed: Query DB to skip existing recordings.
        recordings_table: DB table with existing recordings.
        call_id_column: Column name for call ID in DB.
        s3_filename_column: Column with S3 key in DB.
        s3_config: Named S3 credential set.
        bucket: S3 bucket name.
        directory: S3 prefix / directory.
    """

    _version = "1.0.0"
    BASE_URL = "https://api.zoom.us/v2"
    CACHE_KEY = "_zoom_authentication"

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ):
        # ── Type dispatch ──
        self._fn = kwargs.pop("type", "call_logs").lower().strip()
        if self._fn not in ("call_logs", "sms", "call_detail", "recordings"):
            raise ConfigError(
                f"Invalid type '{self._fn}'. "
                f"Supported: 'call_logs', 'sms', 'call_detail', 'recordings'"
            )

        # ── Credentials ──
        self.client_id = kwargs.pop("client_id", ZOOM_CLIENT_ID)
        self.client_secret = kwargs.pop("client_secret", ZOOM_CLIENT_SECRET)
        self.account_id = kwargs.pop("account_id", ZOOM_ACCOUNT_ID)
        self.access_token: Optional[str] = kwargs.pop("access_token", None)
        self.timeout = kwargs.get("timeout", 30)
        self.session = None

        # ── Date range ──
        self.from_date: str = kwargs.get("from_date")
        self.to_date: str = kwargs.get("to_date")

        # ── Phone numbers / Extensions (SMS) ──
        pn = kwargs.get("phone_numbers")
        self.phone_numbers: List[str] = (
            [str(p).strip() for p in pn if str(p).strip()]
            if isinstance(pn, list)
            else [p.strip() for p in (pn or "").split(",") if p.strip()]
        )
        ext = kwargs.get("extensions")
        self.extensions: List[str] = (
            [str(e).strip() for e in ext if str(e).strip()]
            if isinstance(ext, list)
            else [e.strip() for e in (ext or "").split(",") if e.strip()]
        )

        # ── Session IDs (SMS by session) ──
        # When provided (directly or via an input column), SMS sessions are
        # fetched one-by-one through get_sms_session_details instead of being
        # listed by phone number.
        self.session_id_column: str = kwargs.get("session_id_column", "session_id")
        sid = kwargs.get("session_ids")
        self.session_ids: List[str] = (
            [str(s).strip() for s in sid if str(s).strip()]
            if isinstance(sid, list)
            else [s.strip() for s in (sid or "").split(",") if s.strip()]
        )

        # ── Paths ──
        base_path = Path(kwargs.get("base_path", "/tmp/zoom"))
        self.save_path = Path(kwargs.get("save_path", base_path / "recordings"))
        self.transcripts_path = Path(
            kwargs.get("transcripts_path", base_path / "transcripts")
        )
        self.download_recordings: bool = bool(kwargs.get("download", True))
        self.download_transcripts: bool = bool(kwargs.get("download_transcripts", True))
        self.max_pages: Optional[int] = kwargs.get("max_pages")

        # ── Extension column filtering ──
        self.extension_column: Optional[str] = kwargs.get("extension_column")
        self._extensions_filter: List[str] = []
        # legacy_extension_filter=True mimics the old Zoom.py behaviour:
        # fetch all account-level logs then filter client-side by
        # owner_extension_number instead of resolving extension → userId.
        self.legacy_extension_filter: bool = kwargs.get("legacy_extension_filter", False)

        # ── call_detail mode ──
        # Column in the input DataFrame that contains the call UUID to audit.
        self.call_id_input_column: str = kwargs.get("call_id_input_column", "id")
        # Direct call UUID for single-call debug mode (bypasses input DataFrame).
        self.call_id: Optional[str] = kwargs.get("call_id")

        # ── recordings mode ──
        self.recording_type: Optional[str] = kwargs.get("recording_type")

        # ── as_bytes mode ──
        self.as_bytes: bool = kwargs.get("as_bytes", False)
        self.content_type: str = kwargs.get("content_type", "audio/mpeg")

        # ── Auto-skip / DB ──
        self.auto_skip_processed: bool = kwargs.get("auto_skip_processed", False)
        self.datasource: str = kwargs.get("datasource", "db")
        self.recordings_table: str = kwargs.get("recordings_table", "recordings")
        self.call_id_column: str = kwargs.get("call_id_column", "call_id")
        self.s3_filename_column: str = kwargs.get(
            "s3_filename_column", "recording_mp3_s3_key"
        )
        self.s3_directory: str = kwargs.get("directory", "zoom/recordings/")
        self._driver: str = kwargs.get("driver", "pg")

        # ── S3 ──
        self._s3_config: str = kwargs.get("s3_config", "default")
        if self.auto_skip_processed:
            kwargs["config"] = self._s3_config

        # ── State ──
        self._existing_recordings: Dict[str, str] = {}
        self._s3_client = None
        self._phone_to_extension_map: Dict[str, str] = {}
        self._extension_phone_map: Dict[str, str] = {}

        # ── Ensure folders ──
        if not self.as_bytes:
            self.save_path.mkdir(parents=True, exist_ok=True)
            self.transcripts_path.mkdir(parents=True, exist_ok=True)

        super().__init__(loop=loop, job=job, stat=stat, **kwargs)

    # =================================================================
    # Lifecycle
    # =================================================================

    async def start(self, **kwargs):
        """Authenticate and prepare for execution."""
        # Process masks on dates
        if hasattr(self, "masks"):
            for mask, replace in self._mask.items():
                if self.from_date:
                    self.from_date = self.from_date.replace(mask, str(replace))
                if self.to_date:
                    self.to_date = self.to_date.replace(mask, str(replace))

        # Re-parse phone_numbers in case super().__init__ overwrote it as a raw string,
        # then resolve any env var references (e.g. "ZOOM_SMS_DEFAULT_FROM").
        pn = self.phone_numbers
        if isinstance(pn, str):
            self.phone_numbers = [p.strip() for p in pn.split(",") if p.strip()]
        self.phone_numbers = [
            os.environ.get(p, p) for p in self.phone_numbers
        ]

        self._logger.info("🔐 Starting Zoom authentication...")
        # Use the interface's token method
        token = await self._get_access_token()
        self._logger.info("✅ Successfully authenticated with Zoom API")

        # Process input DataFrame if provided
        if self.previous and hasattr(self, "input") and self.input is not None:
            if hasattr(self.input, "empty") and not self.input.empty:
                self._logger.info(
                    f"📊 Received input DataFrame with {len(self.input)} rows"
                )
                self._process_input_dataframe()

        return True

    # =================================================================
    # Input processing helpers
    # =================================================================

    def _process_input_dataframe(self):
        """Extract extensions for call-log filtering from input DataFrame."""
        if not self.extension_column:
            return

        if self.extension_column not in self.input.columns:
            self._logger.warning(
                f"Extension column '{self.extension_column}' not found. "
                f"Available: {list(self.input.columns)}"
            )
            return

        extensions = (
            self.input[self.extension_column].dropna().astype(str).unique().tolist()
        )
        self._extensions_filter = [ext.strip() for ext in extensions if ext.strip()]
        if self._extensions_filter:
            self._logger.info(
                f"🔍 Extracted {len(self._extensions_filter)} extensions "
                f"from column '{self.extension_column}'"
            )

    def _process_input_dataframe_for_sms(self):
        """Extract phone numbers and extensions from input DataFrame for SMS."""
        extension_column = None
        phone_column = None

        for col_name in ("extension", "extensions", "extension_number"):
            if col_name in self.input.columns:
                extension_column = col_name
                break

        for col_name in ("phone_number", "phone_numbers"):
            if col_name in self.input.columns:
                phone_column = col_name
                break

        # Hybrid: build bidirectional mapping if both columns exist
        if extension_column and phone_column:
            self._logger.info(
                "📋 Found both extension and phone_number columns – "
                "creating local mapping"
            )
            for _, row in self.input.iterrows():
                ext = str(row[extension_column]).strip()
                phone = str(row[phone_column]).strip()
                if ext and phone and phone.lower() not in ("nan", "none", ""):
                    normalized = self.normalize_phone_number(phone)
                    self._extension_phone_map[ext] = normalized
                    self._phone_to_extension_map[normalized] = ext
            self._logger.info(
                f"✅ Created mapping for {len(self._extension_phone_map)} extension(s)"
            )

        # Extract phone numbers
        if phone_column:
            phone_numbers = (
                self.input[phone_column].dropna().astype(str).unique().tolist()
            )
            for num in phone_numbers:
                num = num.strip()
                if num and num.lower() not in ("nan", "none", ""):
                    normalized = self.normalize_phone_number(num)
                    if normalized not in self.phone_numbers:
                        self.phone_numbers.append(normalized)

        # Extract extensions
        if extension_column:
            exts = (
                self.input[extension_column].dropna().astype(str).unique().tolist()
            )
            for ext in exts:
                ext = ext.strip()
                if ext and ext not in self.extensions:
                    self.extensions.append(ext)

    # =================================================================
    # Main entry point
    # =================================================================

    async def run(self):
        """Dispatch to the appropriate method based on ``type``."""
        t0 = time.time()
        self._logger.info(f"🚀 Starting ZoomUs {self._fn.upper()} processing...")

        fn = getattr(self, self._fn, None)
        if fn is None or not callable(fn):
            raise ComponentError(
                f"Unknown operation type: '{self._fn}'. "
                f"Supported: 'call_logs', 'sms'"
            )

        try:
            self._result = await fn()
            self.add_metric("DURATION_SEC", round(time.time() - t0, 3))
            return self._result
        finally:
            await self.close()

    # =================================================================
    # call_logs flow
    # =================================================================

    async def call_logs(self) -> pd.DataFrame:
        """Fetch call logs and optionally download recordings/transcripts.

        Full 1:1 replacement for ``Zoom.py``'s ``call_logs`` method including:
        auto-skip (DB), S3 download with Zoom API fallback, ``as_bytes``
        mode, deduplication, tqdm progress, and detailed metrics.
        """
        t0 = time.time()

        if not self.from_date or not self.to_date:
            raise ComponentError("from_date and to_date are required for call_logs")

        self._logger.info(f"📅 Date range: {self.from_date} → {self.to_date}")
        self._logger.info(f"⬇️ Download recordings: {self.download_recordings}")
        self._logger.info(f"📝 Download transcripts: {self.download_transcripts}")
        self._logger.info(f"💾 as_bytes mode: {self.as_bytes}")
        self._logger.info(f"🔄 auto_skip_processed: {self.auto_skip_processed}")

        # Process input DataFrame for extension filtering
        if self.previous and hasattr(self, "input") and self.input is not None:
            if hasattr(self.input, "empty") and not self.input.empty:
                self._process_input_dataframe()

        # Ensure paths (only when saving to disk)
        if not self.as_bytes:
            self.save_path.mkdir(parents=True, exist_ok=True)
            self.transcripts_path.mkdir(parents=True, exist_ok=True)

        # ── Fetch call logs ──────────────────────────────────────────────────
        # Strategy:
        #   • WITH extension filter  → use /phone/users/{userId}/call_logs
        #     Zoom performs server-side attribution at this endpoint, so calls
        #     answered through a call queue are correctly attributed to the
        #     agent — not to the queue.  Proof: call 664f1ab7-... showed
        #     callee=FLEX ROC (360) at account level, but Emiliano (431) was
        #     the actual answering agent per log_details.
        #   • WITHOUT extension filter → fall back to account-level
        #     /phone/call_logs (original behaviour, returns all account calls).
        # ────────────────────────────────────────────────────────────────────
        self._logger.info("📞 Fetching call logs...")
        all_logs: List[Dict[str, Any]] = []

        if self._extensions_filter and not self.legacy_extension_filter:
            self._logger.info(
                f"🔍 Using per-user endpoint for {len(self._extensions_filter)} extension(s): "
                f"{self._extensions_filter}"
            )
            # Resolve extension → userId once per extension (with a semaphore
            # to avoid hammering the /phone/users directory).
            sem = asyncio.Semaphore(5)

            async def _fetch_for_extension(ext: str):
                async with sem:
                    user_id = await self.get_user_id_by_extension(ext)
                if user_id is None:
                    self._logger.warning(
                        f"⚠️  Extension {ext}: no matching Zoom user found — skipping"
                    )
                    return
                self._logger.info(f"👤 Extension {ext} → userId={user_id}")

                ext_logs: List[Dict[str, Any]] = []
                next_page: Optional[str] = None
                page = 0
                while True:
                    async with sem:
                        data = await self.get_user_call_logs(
                            user_id=user_id,
                            from_date=self.from_date,
                            to_date=self.to_date,
                            next_page_token=next_page,
                        )
                    items = data.get("call_logs", [])
                    ext_logs.extend(items)
                    page += 1
                    self._logger.info(
                        f"  ext={ext} page {page}: {len(items)} logs"
                    )
                    next_page = data.get("next_page_token")
                    if self.max_pages and page >= self.max_pages:
                        self._logger.warning(
                            f"  ext={ext}: reached max_pages={self.max_pages}"
                        )
                        break
                    if not next_page:
                        break

                self._logger.info(
                    f"  ext={ext} total: {len(ext_logs)} call logs"
                )
                all_logs.extend(ext_logs)

            await asyncio.gather(*[_fetch_for_extension(e) for e in self._extensions_filter])

        else:
            # ── Account-level fallback (no extension filter) ──
            next_page: Optional[str] = None
            page = 0
            while True:
                data = await self.get_call_logs(
                    from_date=self.from_date,
                    to_date=self.to_date,
                    next_page_token=next_page,
                )
                items = data.get("call_logs", [])
                all_logs.extend(items)
                self._logger.info(f"📊 Page {page + 1}: {len(items)} logs")
                next_page = data.get("next_page_token")
                page += 1
                if self.max_pages and page >= self.max_pages:
                    self._logger.warning(f"Reached max_pages={self.max_pages}")
                    break
                if not next_page:
                    break

        self._logger.info(f"✅ Total call logs fetched: {len(all_logs)}")

        df = pd.json_normalize(all_logs) if all_logs else pd.DataFrame()
        # Clean column names (dots → underscores)
        if not df.empty:
            col_map = {c: c.replace(".", "_") for c in df.columns if "." in c}
            if col_map:
                df = df.rename(columns=col_map)
            # Deduplicate: the per-user endpoint may return the same call
            # (e.g. a transferred call) from multiple users' perspectives.
            before = len(df)
            df = df.drop_duplicates(subset=["id"]) if "id" in df.columns else df
            if len(df) < before:
                self._logger.info(
                    f"🔁 Deduplication: {before} → {len(df)} rows (removed {before - len(df)} dups)"
                )

        # ── Legacy client-side extension filter ──────────────────────────────
        # Only applied when legacy_extension_filter=True AND extensions were
        # requested.  Mirrors Zoom.py: filter by owner_extension_number after
        # fetching all account-level logs.
        if self.legacy_extension_filter and self._extensions_filter and not df.empty:
            ext_col = "owner_extension_number"
            if ext_col in df.columns:
                def _norm_ext(val):
                    if pd.isna(val):
                        return None
                    try:
                        return str(int(float(val)))
                    except (ValueError, TypeError):
                        return str(val).strip()

                df["_norm_ext"] = df[ext_col].apply(_norm_ext)
                before = len(df)
                df = df[df["_norm_ext"].isin(self._extensions_filter)]
                df = df.drop(columns=["_norm_ext"])
                self._logger.info(
                    f"🔍 Legacy filter by '{ext_col}': {before} → {len(df)} rows"
                )
                if len(df) == 0:
                    self._logger.warning(
                        f"⚠️  No matches — extensions={self._extensions_filter[:5]}"
                    )
            else:
                self._logger.warning(
                    f"⚠️  Legacy filter: '{ext_col}' column not found — skipping. "
                    f"Available: {list(df.columns)}"
                )

        if df.empty:
            self._add_empty_metrics()
            raise DataNotFound("ZoomUs: No call logs found")

        # ── Output columns ──
        if self.as_bytes:
            for col in ("file_data", "content_type", "downloaded_filename",
                         "transcript_data", "transcript_filename"):
                if col not in df.columns:
                    df[col] = None
        else:
            for col in ("local_path", "recording_filename",
                         "transcript_paths", "transcript_filename"):
                if col not in df.columns:
                    df[col] = None

        # ── Identify recorded calls ──
        self._logger.info("🔍 Filtering recorded calls...")

        # recording_status='recorded' takes priority when the column exists
        # (present on some Zoom tenants — same logic as legacy Zoom.py).
        if "recording_status" in df.columns:
            recorded_df = df[
                df["recording_status"].astype(str).str.lower().eq("recorded")
            ]
            self._logger.info(
                f"📹 Found {len(recorded_df)} calls with recording_status='recorded'"
            )
        else:
            has_rec = pd.Series(False, index=df.index)
            if "has_recording" in df.columns:
                has_rec = df["has_recording"].astype(str).str.lower().isin(
                    ["true", "1", "yes"]
                )
            by_rec_id = (
                df["recording_id"].notna() if "recording_id" in df.columns else False
            )
            by_rec_type = (
                df["recording_type"].notna() if "recording_type" in df.columns else False
            )

            count_has_rec = int(has_rec.sum())
            count_rec_id = int(by_rec_id.sum()) if not isinstance(by_rec_id, bool) else 0
            count_rec_type = int(by_rec_type.sum()) if not isinstance(by_rec_type, bool) else 0

            self._logger.info(f"📹 Found {count_has_rec} calls with has_recording=True")
            self._logger.info(f"🆔 Found {count_rec_id} calls with recording_id")
            self._logger.info(f"📋 Found {count_rec_type} calls with recording_type")

            recorded_df = df[has_rec | by_rec_id | by_rec_type]
        recorded_count = len(recorded_df)
        self._logger.info(f"🎯 Processing {recorded_count} recorded calls...")

        if recorded_count == 0 or not (
            self.download_recordings or self.download_transcripts
        ):
            self._add_final_metrics(df, recorded_count, 0, 0, 0, t0)
            self._result = df
            return df

        # ── Auto-skip: separate into new-downloads vs S3-downloads ──
        new_call_ids: List[str] = []
        s3_call_ids: Dict[str, str] = {}  # call_id → s3_filename

        if self.auto_skip_processed:
            all_call_ids = []
            for _, row in recorded_df.iterrows():
                cid = str(row.get("call_id", "") or "").strip()
                if cid:
                    all_call_ids.append(cid)
            if all_call_ids:
                self._existing_recordings = await self._fetch_existing_recordings(
                    all_call_ids
                )
                for cid in all_call_ids:
                    if cid in self._existing_recordings:
                        s3_call_ids[cid] = self._existing_recordings[cid]
                    else:
                        new_call_ids.append(cid)
                self._logger.info(
                    f"📊 Auto-skip status: {len(s3_call_ids)}/{recorded_count} "
                    f"recordings already exist in database"
                )
        else:
            for _, row in recorded_df.iterrows():
                cid = str(row.get("call_id", "") or "").strip()
                if cid:
                    new_call_ids.append(cid)

        # ── Summary before download ──
        total_to_process = len(new_call_ids) + len(s3_call_ids)
        self._logger.info(f"🎥 Total recordings to process: {total_to_process}")
        self._logger.info(f"   📥 New recordings from Zoom API: {len(new_call_ids)}")
        self._logger.info(f"   ♻️ Existing recordings from S3: {len(s3_call_ids)}")

        # ── Download from Zoom API (new recordings) ──
        downloaded = 0
        transcripts_downloaded = 0
        skipped_s3 = 0
        seen_recording_keys: set = set()
        seen_transcript_keys: set = set()

        rows_to_process = recorded_df[
            recorded_df.apply(
                lambda r: str(r.get("call_id", "") or "").strip() in new_call_ids,
                axis=1,
            )
        ] if new_call_ids else pd.DataFrame()

        if not rows_to_process.empty:
            self._logger.info(
                f"🎥 Starting download of {len(rows_to_process)} NEW "
                f"recording files from Zoom API..."
            )
            for _, row in tqdm(
                rows_to_process.iterrows(),
                total=len(rows_to_process),
                desc="Recordings",
                disable=not self._logger.isEnabledFor(20),  # INFO level
            ):
                call_ref = str(row.get("call_id", "") or "").strip()
                call_uuid = str(row.get("id", "") or "").strip()
                call_ref = call_ref or call_uuid
                if not call_ref:
                    continue

                try:
                    meta = await self.get_recording_metadata(call_ref)

                    # ── Recordings ──
                    if self.download_recordings:
                        rec_entries = self._extract_rec_entries(meta)
                        for url, rec_id in rec_entries:
                            dedup_key = f"{call_ref}_{rec_id}"
                            if dedup_key in seen_recording_keys:
                                continue
                            seen_recording_keys.add(dedup_key)

                            result = await self._download_and_store(
                                url, call_ref, rec_id, is_transcript=False
                            )
                            if result is not None:
                                downloaded += 1
                                self._update_df_recording(
                                    df, call_ref, result
                                )

                    # ── Transcripts ──
                    if self.download_transcripts:
                        t_ids = self._extract_transcript_ids(meta)
                        for rid in t_ids:
                            dedup_key = f"{call_ref}_{rid}"
                            if dedup_key in seen_transcript_keys:
                                continue
                            seen_transcript_keys.add(dedup_key)
                            try:
                                content = await self.download_transcript_by_recording_id(rid)
                                if content:
                                    transcripts_downloaded += 1
                                    self._store_transcript(
                                        df, call_ref, rid, content
                                    )
                            except Exception as te:
                                self._logger.warning(
                                    f"  Transcript error {call_ref}/{rid}: {te}"
                                )

                except Exception as e:
                    self._logger.warning(f"Failed metadata for {call_ref}: {e}")

        # ── Download from S3 (existing recordings) ──
        if s3_call_ids and self.download_recordings:
            self._logger.info(
                f"☁️ Downloading {len(s3_call_ids)} recording(s) from S3..."
            )
            for call_id, s3_filename in tqdm(
                s3_call_ids.items(),
                desc="S3 Downloads",
                disable=not self._logger.isEnabledFor(20),
            ):
                result = await self._download_recording_from_s3(
                    s3_filename, call_id
                )
                if result is not None:
                    skipped_s3 += 1
                    self._update_df_recording(df, call_id, result)
                else:
                    # Fallback to Zoom API if S3 fails
                    self._logger.warning(
                        f"  S3 failed for {call_id}, falling back to API"
                    )
                    try:
                        meta = await self.get_recording_metadata(call_id)
                        rec_entries = self._extract_rec_entries(meta)
                        for url, rec_id in rec_entries:
                            result = await self._download_and_store(
                                url, call_id, rec_id, is_transcript=False
                            )
                            if result is not None:
                                downloaded += 1
                                self._update_df_recording(df, call_id, result)
                                break
                    except Exception as e:
                        self._logger.error(
                            f"  API fallback also failed for {call_id}: {e}"
                        )

        # ── Metrics ──
        self._add_final_metrics(
            df, recorded_count, downloaded, transcripts_downloaded, skipped_s3, t0
        )
        self._logger.info(
            f"🎉 Done: {len(df)} logs, {downloaded} new downloads, "
            f"{skipped_s3} from S3, {transcripts_downloaded} transcripts"
        )
        self._log_sample(df)
        self._result = df
        return self._result

    # =================================================================
    # call_detail flow
    # =================================================================

    async def call_detail(self) -> pd.DataFrame:
        """Fetch full detail (all legs) for a list of call UUIDs.

        Reads call UUIDs from the input DataFrame column defined by
        ``call_id_input_column`` (default: ``"id"``).  For each UUID it
        calls ``GET /phone/call_logs/{callLogId}`` which returns the root
        call fields **and** the ``log_details`` array with every agent leg.

        The result is a flat DataFrame where:

        * Each row is one leg (one agent interaction) of a call.
        * Root call fields (``caller_name``, ``callee_name``, ``result``,
          ``duration``, ``path``, ``date_time``, …) are prefixed with
          ``call_`` and added to every leg row so you can always trace back
          to the parent call.
        * Leg-specific fields (``id``, ``result``, ``duration``,
          ``forward_to``, …) come directly from ``log_details``.

        YAML usage::

            - QueryToPandas:
                query: "SELECT id FROM assurant.calls WHERE ..."
            - ZoomUs:
                type: call_detail
                call_id_input_column: id   # column with the call UUID

        Args:
            (none – configuration via __init__ kwargs)

        Returns:
            DataFrame with one row per agent leg, enriched with parent
            call fields.
        """
        # ── Single-call debug mode ───────────────────────────────────────────
        # If call_id is set directly in YAML, bypass the input DataFrame and
        # return the raw Zoom JSON for that one call as a flat DataFrame.
        # Nothing is added, prefixed, or removed — exactly what Zoom returns.
        #
        # YAML:
        #   - ZoomUs:
        #       type: call_detail
        #       call_id: "664f1ab7-c435-4fc4-a6be-44e16c609270"
        # ────────────────────────────────────────────────────────────────────
        if self.call_id:
            self._logger.info(f"🔬 Debug mode: fetching single call {self.call_id!r}")
            detail = await self.get_call_log_detail(str(self.call_id))

            if "code" in detail:
                self._logger.warning(
                    f"⚠️  Zoom error {detail.get('code')}: {detail.get('message', '')}"
                )
                self._result = pd.DataFrame([detail])
                return self._result

            # Flatten nested fields (log_details, forwarded_by, etc.)
            # but keep them all — this is Postman mode, raw output only.
            df = pd.json_normalize(detail)
            col_map = {c: c.replace(".", "_") for c in df.columns if "." in c}
            if col_map:
                df = df.rename(columns=col_map)

            self._logger.info(
                f"✅ call_detail (debug): {len(df.columns)} columns, "
                f"{detail.get('log_details') and len(detail['log_details'])} leg(s) in log_details"
            )
            self._log_sample(df)

            # ── Recording detection & download (debug mode) ──────────────────
            # Strategy: Use GET /phone/recordings for the call's date to find
            # any recording matching this call.  This endpoint returns:
            #   - call_id (numeric)  → matches detail["call_id"]
            #   - call_log_id (UUID) → matches detail["id"]
            #   - download_url       → direct, no secondary API call needed
            #
            # This is more reliable than GET /phone/call_logs/{uuid}/recordings
            # which returns 404 when no recording exists (ambiguous error), and
            # also avoids the deprecated has_recording field entirely.
            # ─────────────────────────────────────────────────────────────────
            call_ref     = str(self.call_id).strip()         # numeric from YAML
            call_uuid    = detail.get("id", "")              # UUID from response
            call_numeric = str(detail.get("call_id", call_ref))  # numeric from response

            if self.download_recordings or self.download_transcripts:
                # Extract the date from the call's date_time (YYYY-MM-DD)
                raw_dt = detail.get("date_time", "")
                call_date = raw_dt[:10] if raw_dt else None  # "2026-01-05"

                if not call_date:
                    self._logger.warning(
                        "⚠️  Cannot probe recordings: no date_time in call detail"
                    )
                else:
                    self._logger.info(
                        f"🔍 Probing GET /phone/recordings for date={call_date!r} "
                        f"(call_id={call_numeric!r}, uuid={call_uuid!r})"
                    )

                    rec_found = None
                    next_page = None

                    try:
                        while True:
                            page = await self.list_recordings(
                                from_date=_dt.strptime(call_date, "%Y-%m-%d"),
                                to_date=_dt.strptime(call_date, "%Y-%m-%d"),
                                page_size=100,
                                next_page_token=next_page,
                            )
                            for rec in page.get("recordings", []):
                                if (
                                    str(rec.get("call_id", "")) == call_numeric
                                    or rec.get("call_log_id", "") == call_uuid
                                ):
                                    rec_found = rec
                                    break
                            if rec_found:
                                break
                            next_page = page.get("next_page_token")
                            if not next_page:
                                break

                    except Exception as e:
                        self._logger.warning(f"⚠️  Could not query recordings: {e}")

                    if rec_found:
                        self._logger.info(
                            f"📋 Recording found!\n"
                            f"   id           = {rec_found.get('id')!r}\n"
                            f"   recording_type = {rec_found.get('recording_type')!r}\n"
                            f"   duration     = {rec_found.get('duration')}s\n"
                            f"   accepted_by  = {rec_found.get('accepted_by')}\n"
                            f"   download_url = {rec_found.get('download_url')!r}\n"
                            f"   transcript   = {rec_found.get('transcript_download_url')!r}"
                        )

                        if self.download_recordings:
                            url = rec_found.get("download_url")
                            rec_id = rec_found.get("id", call_ref)
                            if url:
                                self._logger.info(f"  ⬇️  Downloading recording {rec_id!r}…")
                                result = await self._download_and_store(
                                    url, call_ref, rec_id, is_transcript=False
                                )
                                if result is not None:
                                    self._logger.info("  ✅ Recording downloaded")
                                    if self.as_bytes and isinstance(result, tuple):
                                        fd, ct, fname = result
                                        df.loc[0, "file_data"] = fd
                                        df.loc[0, "content_type"] = ct
                                        df.loc[0, "downloaded_filename"] = fname
                                    else:
                                        df.loc[0, "local_path"] = str(result)
                                        df.loc[0, "recording_filename"] = getattr(result, "name", str(result))

                        if self.download_transcripts:
                            t_url = rec_found.get("transcript_download_url")
                            rec_id = rec_found.get("id", call_ref)
                            if t_url:
                                self._logger.info(f"  📝 Downloading transcript {rec_id!r}…")
                                try:
                                    content = await self.download_transcript_by_recording_id(rec_id)
                                    if content:
                                        self._logger.info("  ✅ Transcript downloaded")
                                except Exception as te:
                                    self._logger.warning(f"  Transcript error: {te}")
                    else:
                        self._logger.info(
                            f"ℹ️  No recording found for call {call_ref!r} on {call_date}. "
                            "Call was not recorded (auto-record likely not enabled)."
                        )

            else:
                has_rec_hint = (
                    bool(detail.get("has_recording", False))
                    or bool(detail.get("recording_id"))
                    or bool(detail.get("recording_type"))
                    or str(detail.get("result", "")).lower() in ("auto recorded", "recorded")
                )
                if has_rec_hint:
                    self._logger.info(
                        "📹 Call signals a recording — set download: true to probe it"
                    )
                else:
                    self._logger.info(
                        "ℹ️  No recording signals (use download: true to probe via API)"
                    )

            self._result = df
            return df

        # ── Batch mode from input DataFrame ─────────────────────────────────
        if not self.previous or not hasattr(self, "input") or self.input is None:
            raise ComponentError(
                "call_detail requires either a 'call_id' param or an input "
                f"DataFrame with call UUIDs in column '{self.call_id_input_column}'"
            )

        if self.call_id_input_column not in self.input.columns:
            raise ComponentError(
                f"Column '{self.call_id_input_column}' not found in input DataFrame. "
                f"Available: {list(self.input.columns)}"
            )

        call_ids: List[str] = (
            self.input[self.call_id_input_column]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )
        self._logger.info(
            f"🔍 call_detail: fetching {len(call_ids)} call(s) from "
            f"column '{self.call_id_input_column}'"
        )

        rows: List[Dict[str, Any]] = []
        sem = asyncio.Semaphore(10)

        # Root-level fields we want to surface on every leg row
        ROOT_FIELDS = (
            "caller_name", "caller_number", "caller_number_type",
            "callee_name", "callee_number", "callee_number_type",
            "direction", "duration", "result", "date_time",
            "waiting_time", "path", "has_recording", "has_voicemail",
            "call_id",
        )

        async def _fetch_one(call_uuid: str):
            async with sem:
                detail = await self.get_call_log_detail(call_uuid)

            if "code" in detail:
                # Zoom returned an error (404, 400, etc)
                self._logger.warning(
                    f"  ⚠️  {call_uuid}: Zoom error {detail.get('code')} – "
                    f"{detail.get('message', '')}"
                )
                return

            log_details: List[Dict[str, Any]] = detail.get("log_details", [])
            root_prefix = {f"call_{k}": detail.get(k) for k in ROOT_FIELDS}
            root_prefix["call_uuid"] = call_uuid   # always keep the parent UUID

            if log_details:
                for leg in log_details:
                    row = {**root_prefix, **leg}
                    rows.append(row)
            else:
                # No legs: store the root record alone so the call isn't lost
                rows.append({**root_prefix, "id": call_uuid})

            self._logger.info(
                f"  ✅ {call_uuid}: {len(log_details)} leg(s)"
            )

        await asyncio.gather(*[_fetch_one(uid) for uid in call_ids])

        df = pd.json_normalize(rows) if rows else pd.DataFrame()
        if not df.empty:
            col_map = {c: c.replace(".", "_") for c in df.columns if "." in c}
            if col_map:
                df = df.rename(columns=col_map)

        self._logger.info(
            f"✅ call_detail complete: {len(call_ids)} call(s) → {len(df)} leg rows"
        )
        if df.empty:
            raise DataNotFound("ZoomUs: No call detail found for the provided call IDs")
        self._log_sample(df)
        self._result = df
        return df

    # =================================================================
    # sms flow
    # =================================================================

    async def sms(self) -> pd.DataFrame:
        """Fetch SMS sessions and messages by session_id (preferred) or phone number."""
        # Collect session_ids from the input DataFrame, if a session_id column exists.
        if self.previous and hasattr(self, "input") and self.input is not None:
            if hasattr(self.input, "empty") and not self.input.empty:
                if self.session_id_column in self.input.columns:
                    ids = (
                        self.input[self.session_id_column]
                        .dropna().astype(str).unique().tolist()
                    )
                    for sid in ids:
                        sid = sid.strip()
                        if sid and sid not in self.session_ids:
                            self.session_ids.append(sid)

        # Mode 1: fetch specific sessions directly by session_id.
        if self.session_ids:
            return await self._sms_by_session_ids()

        # Mode 2: fetch by phone number / extension (original behaviour).
        # Process input DataFrame
        if self.previous and hasattr(self, "input") and self.input is not None:
            if hasattr(self.input, "empty") and not self.input.empty:
                self._logger.info(
                    f"📊 Input DataFrame: {len(self.input)} rows"
                )
                self._process_input_dataframe_for_sms()

        # Extension → phone lookup
        if self.extensions:
            self._logger.info(
                f"🔍 Looking up {len(self.extensions)} extension(s)..."
            )
            for ext in self.extensions:
                # Use local mapping first, then API
                if ext in self._extension_phone_map:
                    normalized = self._extension_phone_map[ext]
                    if normalized not in self.phone_numbers:
                        self.phone_numbers.append(normalized)
                    self._logger.info(f"  ✅ Ext {ext} → {normalized} (local)")
                else:
                    numbers = await self.get_phone_numbers_by_extension(ext)
                    for num in numbers:
                        normalized = self.normalize_phone_number(num)
                        if normalized not in self.phone_numbers:
                            self.phone_numbers.append(normalized)
                        self._phone_to_extension_map[normalized] = ext
                    if numbers:
                        self._logger.info(
                            f"  ✅ Ext {ext} → {len(numbers)} number(s) (API)"
                        )
                    else:
                        self._logger.warning(f"  ⚠️ Ext {ext}: not found")

        if not self.phone_numbers:
            raise ConfigError(
                "No phone numbers found. Provide 'phone_numbers', 'extensions', "
                "or an input DataFrame with appropriate columns."
            )

        self._logger.info(f"📱 Phone numbers: {', '.join(self.phone_numbers)}")

        # ── Step 1: Fetch sessions ──
        all_sessions: List[Dict[str, Any]] = []
        for phone_number in self.phone_numbers:
            self._logger.info(f"  Querying sessions for {phone_number}...")
            next_page = None
            page = 0

            # Calculate to_date if not provided (SMS API requires both)
            effective_to = self.to_date
            if self.from_date and not effective_to:
                from_dt = datetime.strptime(self.from_date, "%Y-%m-%d")
                max_to = from_dt + timedelta(days=31)
                effective_to = min(max_to, datetime.now()).strftime("%Y-%m-%d")

            while True:
                try:
                    data = await self.list_sms_sessions(
                        phone_number=phone_number,
                        from_date=self.from_date,
                        to_date=effective_to,
                        next_page_token=next_page,
                    )
                    sessions = data.get("sms_sessions", [])
                    for s in sessions:
                        s["queried_phone_number"] = phone_number
                        s["fetched_at"] = datetime.utcnow().isoformat() + "Z"
                    all_sessions.extend(sessions)
                    self._logger.info(
                        f"    Page {page + 1}: {len(sessions)} session(s)"
                    )

                    next_page = data.get("next_page_token")
                    page += 1
                    if self.max_pages and page >= self.max_pages:
                        break
                    if not next_page:
                        break
                except Exception as e:
                    self._logger.error(
                        f"    Error fetching sessions for {phone_number}: {e}"
                    )
                    break

        self._logger.info(f"✅ Total sessions: {len(all_sessions)}")
        self.add_metric("SMS_SESSIONS_COUNT", len(all_sessions))

        if not all_sessions:
            self.add_metric("NUMROWS", 0)
            self.add_metric("SMS_MESSAGES_COUNT", 0)
            raise DataNotFound("ZoomUs: No SMS sessions found")

        # ── Step 2: Fetch messages per session ──
        session_records: List[Dict[str, Any]] = []
        total_messages = 0
        sem = asyncio.Semaphore(3)

        async def _process_session(idx: int, session: Dict[str, Any]):
            nonlocal total_messages
            session_id = session.get("session_id") or session.get("id")
            if not session_id:
                return

            session_messages = session.get("sms_histories") or session.get(
                "messages", []
            )

            if not session_messages:
                try:
                    next_page = None
                    while True:
                        async with sem:
                            details = await self.get_sms_session_details(
                                session_id, next_page_token=next_page
                            )
                        msgs = details.get("sms_histories", [])
                        session_messages.extend(msgs)

                        next_page = details.get("next_page_token")
                        if not next_page:
                            break
                except Exception as e:
                    self._logger.error(
                        f"  Session {idx}: Error fetching messages – {e}"
                    )
                    return

            # Build session record
            queried_phone = session.get("queried_phone_number", "")
            bound = self.determine_bound(session)
            extension = self._phone_to_extension_map.get(
                self.normalize_phone_number(queried_phone), ""
            )

            # Participant details
            participants = session.get("participants", [])
            owner_number = owner_name = other_number = None
            for p in participants:
                if p.get("is_session_owner", False):
                    owner_number = p.get("phone_number", "")
                    owner_name = p.get("display_name", "")
                else:
                    other_number = p.get("phone_number", "")

            # Last message time
            last_message_time = session.get("last_message_time")
            if not last_message_time and session_messages:
                times = [m.get("date_time") for m in session_messages if m.get("date_time")]
                if times:
                    last_message_time = max(times)

            session_records.append(
                {
                    "session_id": session_id,
                    "extension": extension,
                    "phone_number": queried_phone,
                    "bound": bound,
                    "owner_number": owner_number,
                    "owner_name": owner_name,
                    "other_number": other_number,
                    "session_type": session.get("session_type"),
                    "last_message_time": last_message_time,
                    "last_access_time": session.get("last_access_time"),
                    "message_count": len(session_messages),
                    "messages": session_messages,
                    "participants": participants,
                    "fetched_at": session.get("fetched_at"),
                }
            )
            total_messages += len(session_messages)

            if idx % 50 == 0:
                self._logger.info(f"  ... processed {idx}/{len(all_sessions)} sessions ({total_messages} messages so far)")

        await asyncio.gather(*[_process_session(idx, session) for idx, session in enumerate(all_sessions, 1)])

        self._logger.info(
            f"✅ Processed {len(session_records)} session(s) "
            f"with {total_messages} message(s)"
        )

        if not session_records:
            self.add_metric("NUMROWS", 0)
            self.add_metric("SMS_MESSAGES_COUNT", 0)
            raise DataNotFound("ZoomUs: No SMS messages found in sessions")

        df = pd.DataFrame(session_records)
        self.add_metric("NUMROWS", len(df))
        self.add_metric("NUMCOLS", len(df.columns))
        self.add_metric("SMS_SESSIONS_COUNT", len(session_records))
        self.add_metric("SMS_MESSAGES_COUNT", total_messages)

        return df

    async def _sms_by_session_ids(self) -> pd.DataFrame:
        """Fetch SMS messages for explicit session IDs.

        Used when session_ids are provided directly or via an input column
        (e.g. navigator.zoom_log.session_id). Each session is retrieved with
        get_sms_session_details, bypassing the phone-number session listing.

        Returns:
            DataFrame with one row per session, same shape as ``sms()`` output.
        """
        self._logger.info(
            f"📱 Fetching {len(self.session_ids)} SMS session(s) by session_id..."
        )
        session_records: List[Dict[str, Any]] = []
        total_messages = 0
        sem = asyncio.Semaphore(3)

        async def _fetch(session_id: str):
            nonlocal total_messages
            messages: List[Dict[str, Any]] = []
            detail: Dict[str, Any] = {}
            next_page = None
            try:
                while True:
                    async with sem:
                        detail = await self.get_sms_session_details(
                            session_id, next_page_token=next_page
                        )
                    messages.extend(detail.get("sms_histories", []))
                    next_page = detail.get("next_page_token")
                    if not next_page:
                        break
            except Exception as e:
                self._logger.error(
                    f"  Session {session_id}: error fetching messages – {e}"
                )
                return

            # The session-detail endpoint returns sms_histories but usually NOT
            # participants, so resolve owner/other/session_type from participants
            # when present and fall back to the messages themselves.
            participants = detail.get("participants", [])
            owner_number = owner_name = other_number = None
            for p in participants:
                if p.get("is_session_owner", False):
                    owner_number = p.get("phone_number") or owner_number
                    owner_name = p.get("display_name") or owner_name
                else:
                    other_number = p.get("phone_number") or other_number

            session_type = detail.get("session_type")
            for m in messages:
                if not session_type:
                    session_type = (m.get("owner") or {}).get("type")
                direction = str(m.get("direction", "")).lower()
                sender = (m.get("sender") or {}).get("phone_number")
                if direction == "out":
                    # T-ROC side sends; recipients are the candidate(s).
                    owner_number = owner_number or sender
                    if not other_number:
                        for tm in (m.get("to_members") or []):
                            if not tm.get("is_message_owner"):
                                other_number = tm.get("phone_number") or other_number
                                if other_number:
                                    break
                elif direction == "in":
                    # Candidate replies; sender is the candidate.
                    other_number = other_number or sender

            # bound: 'In' = a reply from the other party.
            dirs = {str(m.get("direction", "")).lower() for m in messages}
            has_in, has_out = "in" in dirs, "out" in dirs
            if has_in and has_out:
                bound = "both"
            elif has_in:
                bound = "inbound"
            elif has_out:
                bound = "outbound"
            else:
                bound = "unknown"

            last_message_time = detail.get("last_message_time")
            if not last_message_time and messages:
                times = [m.get("date_time") for m in messages if m.get("date_time")]
                if times:
                    last_message_time = max(times)

            session_records.append(
                {
                    "session_id": session_id,
                    "extension": None,
                    "phone_number": owner_number,
                    "bound": bound,
                    "session_type": session_type,
                    "owner_number": owner_number,
                    "owner_name": owner_name,
                    "other_number": other_number,
                    "last_message_time": last_message_time,
                    "last_access_time": detail.get("last_access_time"),
                    "message_count": len(messages),
                    "messages": messages,
                    "participants": participants,
                    "fetched_at": datetime.utcnow().isoformat() + "Z",
                }
            )
            total_messages += len(messages)

        await asyncio.gather(*[_fetch(sid) for sid in self.session_ids])

        self._logger.info(
            f"✅ Fetched {len(session_records)} session(s) "
            f"with {total_messages} message(s)"
        )

        if not session_records:
            self.add_metric("NUMROWS", 0)
            self.add_metric("SMS_MESSAGES_COUNT", 0)
            raise DataNotFound(
                "ZoomUs: No SMS sessions found for the provided session_ids"
            )

        df = pd.DataFrame(session_records)
        self.add_metric("NUMROWS", len(df))
        self.add_metric("NUMCOLS", len(df.columns))
        self.add_metric("SMS_SESSIONS_COUNT", len(session_records))
        self.add_metric("SMS_MESSAGES_COUNT", total_messages)
        return df

    # =================================================================
    # recordings flow
    # =================================================================

    async def recordings(self) -> pd.DataFrame:
        """Fetch account-level recordings for a date range.

        Uses ``GET /phone/recordings`` (account-wide) or
        ``GET /phone/users/{userId}/recordings`` (per-extension) to
        retrieve all recording metadata.  Optionally downloads the
        recording files.

        YAML usage::

            - ZoomUs:
                type: recordings
                from_date: "2025-01-01"
                to_date: "2025-01-31"
                download: true
                recording_type: automatic   # optional: automatic | on_demand | all

        Returns:
            DataFrame with one row per recording.
        """
        t0 = time.time()

        if not self.from_date or not self.to_date:
            raise ComponentError(
                "from_date and to_date are required for recordings"
            )

        self._logger.info(f"📅 Date range: {self.from_date} → {self.to_date}")
        self._logger.info(f"⬇️ Download recordings: {self.download_recordings}")
        if self.recording_type:
            self._logger.info(f"🎚️ Recording type filter: {self.recording_type}")

        

        rec_type = None
        if self.recording_type:
            try:
                rec_type = RecordingType(self.recording_type.lower())
            except ValueError:
                self._logger.warning(
                    f"⚠️  Unknown recording_type '{self.recording_type}', "
                    f"ignoring filter. Valid: automatic, on_demand, all"
                )

        from_dt = datetime.strptime(self.from_date, "%Y-%m-%d")
        to_dt = datetime.strptime(self.to_date, "%Y-%m-%d")

        # ── Fetch recordings ─────────────────────────────────────────────
        all_recordings: List[Dict[str, Any]] = []

        # Process input DataFrame for extension filtering
        if self.previous and hasattr(self, "input") and self.input is not None:
            if hasattr(self.input, "empty") and not self.input.empty:
                self._process_input_dataframe()

        if self._extensions_filter:
            # Per-user recordings
            self._logger.info(
                f"🔍 Fetching recordings for {len(self._extensions_filter)} "
                f"extension(s): {self._extensions_filter}"
            )
            sem = asyncio.Semaphore(5)

            async def _fetch_user_recordings(ext: str):
                async with sem:
                    user_id = await self.get_user_id_by_extension(ext)
                if user_id is None:
                    self._logger.warning(
                        f"⚠️  Extension {ext}: no matching Zoom user — skipping"
                    )
                    return
                self._logger.info(f"👤 Extension {ext} → userId={user_id}")

                ext_recs: List[Dict[str, Any]] = []
                next_page: Optional[str] = None
                page = 0
                while True:
                    async with sem:
                        data = await self.list_recordings(
                            from_date=from_dt,
                            to_date=to_dt,
                            page_size=100,
                            next_page_token=next_page,
                            recording_type=rec_type,
                        )
                    items = data.get("recordings", [])
                    # Filter recordings belonging to this user
                    for rec in items:
                        owner = rec.get("owner", {})
                        if isinstance(owner, dict):
                            if owner.get("extension_number") == int(ext):
                                ext_recs.append(rec)
                        else:
                            ext_recs.append(rec)
                    page += 1
                    self._logger.info(
                        f"  ext={ext} page {page}: {len(items)} recordings, "
                        f"{len(ext_recs)} matched"
                    )
                    next_page = data.get("next_page_token")
                    if self.max_pages and page >= self.max_pages:
                        break
                    if not next_page:
                        break

                self._logger.info(
                    f"  ext={ext} total: {len(ext_recs)} recordings"
                )
                all_recordings.extend(ext_recs)

            await asyncio.gather(
                *[_fetch_user_recordings(e) for e in self._extensions_filter]
            )
        else:
            # Account-level recordings
            self._logger.info("📡 Fetching account-level recordings...")
            next_page: Optional[str] = None
            page = 0
            while True:
                data = await self.list_recordings(
                    from_date=from_dt,
                    to_date=to_dt,
                    page_size=100,
                    next_page_token=next_page,
                    recording_type=rec_type,
                )
                items = data.get("recordings", [])
                all_recordings.extend(items)
                page += 1
                self._logger.info(f"📊 Page {page}: {len(items)} recordings")
                next_page = data.get("next_page_token")
                if self.max_pages and page >= self.max_pages:
                    self._logger.warning(
                        f"Reached max_pages={self.max_pages}"
                    )
                    break
                if not next_page:
                    break

        self._logger.info(
            f"✅ Total recordings fetched: {len(all_recordings)}"
        )

        # ── Build DataFrame ──────────────────────────────────────────────
        df = (
            pd.json_normalize(all_recordings)
            if all_recordings
            else pd.DataFrame()
        )

        if not df.empty:
            col_map = {
                c: c.replace(".", "_") for c in df.columns if "." in c
            }
            if col_map:
                df = df.rename(columns=col_map)

        if df.empty:
            self._add_empty_metrics()
            raise DataNotFound("ZoomUs: No recordings found")

        # ── Optional download ────────────────────────────────────────────
        downloaded = 0
        if self.download_recordings:
            # Prepare output columns
            if self.as_bytes:
                for col in ("file_data", "content_type", "downloaded_filename"):
                    if col not in df.columns:
                        df[col] = None
            else:
                for col in ("local_path", "recording_filename"):
                    if col not in df.columns:
                        df[col] = None

            self._logger.info(
                f"🎥 Downloading {len(df)} recording file(s)..."
            )
            seen: set = set()
            for idx, row in tqdm(
                df.iterrows(),
                total=len(df),
                desc="Recordings",
                disable=not self._logger.isEnabledFor(20),
            ):
                rec_id = str(row.get("id", "") or "").strip()
                url = str(row.get("download_url", "") or "").strip()
                call_ref = str(
                    row.get("call_id", "") or row.get("call_log_id", rec_id) or ""
                ).strip()

                if not url or not rec_id:
                    continue
                if rec_id in seen:
                    continue
                seen.add(rec_id)

                try:
                    result = await self._download_and_store(
                        url, call_ref, rec_id, is_transcript=False
                    )
                    if result is not None:
                        downloaded += 1
                        self._update_df_recording(df, call_ref, result)
                except Exception as e:
                    self._logger.warning(
                        f"Failed to download recording {rec_id}: {e}"
                    )

        # ── Metrics ──────────────────────────────────────────────────────
        self.add_metric("NUMROWS", len(df))
        self.add_metric("NUMCOLS", len(df.columns))
        self.add_metric("RECORDINGS_TOTAL", len(all_recordings))
        self.add_metric("RECORDINGS_DOWNLOADED", downloaded)
        self.add_metric("DURATION_SEC", round(time.time() - t0, 3))

        self._logger.info(
            f"🎉 Done: {len(df)} recordings, {downloaded} downloaded"
        )
        self._log_sample(df)
        self._result = df
        return df

    # =================================================================
    # S3 / Database helpers
    # =================================================================

    async def _get_s3_client(self):
        """Get or initialize S3 client (lazy, avoids QSSupport conflicts)."""
        if self._s3_client is None:


            s3_credentials = AWS_CREDENTIALS.get(self._s3_config)
            if s3_credentials:
                cred = {
                    "aws_access_key_id": s3_credentials.get("aws_key"),
                    "aws_secret_access_key": s3_credentials.get("aws_secret"),
                    "region_name": s3_credentials.get("region_name", "us-east-1"),
                }
                self._s3_client = boto3.client("s3", **cred)
                if not getattr(self, "bucket", None) and "bucket" in s3_credentials:
                    self.bucket = s3_credentials["bucket"]
            else:
                self._s3_client = boto3.client("s3", region_name="us-east-1")
        return self._s3_client

    async def _fetch_existing_recordings(
        self, call_ids: List[str]
    ) -> Dict[str, str]:
        """Query DB for existing recordings.

        Returns:
            Dict mapping ``call_id`` → ``s3_filename``.
        """
        if not call_ids:
            return {}
        try:
            connection = await self.create_connection()
            placeholders = ",".join(f"${i+1}" for i in range(len(call_ids)))
            query = (
                f"SELECT {self.call_id_column}, {self.s3_filename_column} "
                f"FROM {self.recordings_table} "
                f"WHERE {self.call_id_column} IN ({placeholders}) "
                f"AND {self.s3_filename_column} IS NOT NULL"
            )
            self._logger.info(f"🔍 Querying DB for {len(call_ids)} call_ids...")
            async with await connection.connection() as conn:
                res, error = await conn.query(query, *call_ids)
                if error:
                    self._logger.error(f"DB query error: {error}")
                    return {}
                result = {}
                for row in res:
                    cid = row[self.call_id_column]
                    s3fn = row[self.s3_filename_column]
                    if s3fn:
                        result[cid] = s3fn
                self._logger.info(f"✅ Found {len(result)} existing recordings")
                return result
        except Exception as e:
            self._logger.error(f"Error querying existing recordings: {e}")
            return {}

    async def _download_recording_from_s3(
        self, s3_filename: str, call_id: str
    ):
        """Download recording from S3.

        Returns:
            ``(BytesIO, content_type, filename)`` if ``as_bytes``,
            ``Path`` if disk mode, or ``None`` on error.
        """
        bucket = getattr(self, "bucket", None)
        if not bucket:
            self._logger.error("S3 bucket not set, cannot download")
            return None
        try:
            s3_key = (
                self.s3_directory + s3_filename
                if self.s3_directory
                else s3_filename
            )
            s3_client = await self._get_s3_client()
            response = s3_client.get_object(Bucket=bucket, Key=s3_key)
            content = response["Body"].read()
            ct = response.get("ContentType", self.content_type)

            if self.as_bytes:
                fd = BytesIO(content)
                fd.seek(0)
                return (fd, ct, s3_filename)

            final_path = self.save_path / s3_filename
            final_path.parent.mkdir(parents=True, exist_ok=True)
            with open(final_path, "wb") as f:
                f.write(content)
            return final_path
        except Exception as e:
            self._logger.error(f"S3 download error for {s3_filename}: {e}")
            return None

    # =================================================================
    # Download helpers
    # =================================================================

    async def _download_and_store(
        self,
        url: str,
        call_ref: str,
        rec_id: str,
        is_transcript: bool = False,
    ):
        """Download binary from Zoom API via interface and store.

        Returns:
            ``(BytesIO, content_type, filename)`` in as_bytes mode,
            ``Path`` in disk mode, or ``None`` on failure.
        """
        try:
            content_bytes, ct, filename = await self.download_binary(url)
            if not content_bytes:
                self._logger.warning(f"  ⚠️ Empty content for {call_ref}")
                return None

            # Fallback filename
            if not filename or filename == "download":
                ext = ".txt" if is_transcript else ".mp4"
                filename = f"{call_ref}_{rec_id}{ext}"

            if self.as_bytes:
                fd = BytesIO(content_bytes)
                fd.seek(0)
                return (fd, ct, filename)

            dest = (
                self.transcripts_path if is_transcript else self.save_path
            )
            final_path = dest / filename
            final_path.parent.mkdir(parents=True, exist_ok=True)
            with open(final_path, "wb") as f:
                f.write(content_bytes)

            self._logger.info(
                f"  ✅ Saved: {final_path.name} "
                f"({len(content_bytes) / 1024:.1f} KB)"
            )
            return final_path

        except asyncio.TimeoutError:
            self._logger.error(f"  ❌ Timeout downloading {call_ref}_{rec_id}")
        except Exception as e:
            self._logger.error(f"  ❌ Download failed for {call_ref}: {e}")
        return None

    @staticmethod
    def _extract_rec_entries(meta: Dict) -> List[tuple]:
        """Extract ``(download_url, recording_id)`` pairs from metadata."""
        entries = []
        recs = meta.get("recordings")
        if isinstance(recs, list) and recs:
            for rec in recs:
                url = rec.get("download_url") or rec.get("file_url")
                if not url:
                    continue
                rid = str(
                    rec.get("id") or rec.get("recording_id") or ""
                ).strip()
                entries.append((url, rid or "rec"))
        else:
            url = meta.get("download_url") or meta.get("file_url")
            if url:
                rid = str(
                    meta.get("id") or meta.get("recording_id") or ""
                ).strip()
                entries.append((url, rid or "rec"))
        return entries

    @staticmethod
    def _extract_transcript_ids(meta: Dict) -> List[str]:
        """Extract recording IDs that may have transcripts."""
        ids = []
        recs = meta.get("recordings")
        if isinstance(recs, list) and recs:
            for rec in recs:
                rid = str(
                    rec.get("id") or rec.get("recording_id") or ""
                ).strip()
                if rid:
                    ids.append(rid)
        else:
            rid = str(
                meta.get("id") or meta.get("recording_id") or ""
            ).strip()
            if rid:
                ids.append(rid)
        return ids

    def _update_df_recording(self, df: pd.DataFrame, call_ref: str, result):
        """Update the DataFrame row with the download result."""
        mask = df["call_id"].astype(str).str.strip().eq(call_ref)
        if not mask.any() and "id" in df.columns:
            mask = mask | df["id"].astype(str).str.strip().eq(call_ref)

        if not mask.any():
            return

        if self.as_bytes and isinstance(result, tuple):
            fd, ct, fname = result
            for idx in df.index[mask]:
                df.at[idx, "file_data"] = fd
                df.at[idx, "content_type"] = ct
                df.at[idx, "downloaded_filename"] = fname
        elif isinstance(result, Path):
            df.loc[mask, "local_path"] = str(result)
            df.loc[mask, "recording_filename"] = result.name

    def _store_transcript(
        self, df: pd.DataFrame, call_ref: str, rid: str, content: bytes
    ):
        """Store a transcript (BytesIO or disk) and update the DataFrame."""
        mask = df["call_id"].astype(str).str.strip().eq(call_ref)
        if not mask.any() and "id" in df.columns:
            mask = mask | df["id"].astype(str).str.strip().eq(call_ref)

        fname = f"{call_ref}_{rid}.txt"
        if self.as_bytes:
            fd = BytesIO(content)
            fd.seek(0)
            for idx in df.index[mask]:
                df.at[idx, "transcript_data"] = fd
                df.at[idx, "transcript_filename"] = fname
        else:
            path = self.transcripts_path / fname
            path.write_bytes(content)
            self._logger.debug(f"  📝 Transcript saved: {path.name}")
            if mask.any():
                df.loc[mask, "transcript_paths"] = str(path)
                df.loc[mask, "transcript_filename"] = fname

    # =================================================================
    # Metrics helpers
    # =================================================================

    def _log_sample(self, df: "pd.DataFrame") -> None:
        """Print a one-row sample of the DataFrame — dtype and first value per column.

        Output format (identical to FilterRows / TransformRows)::

            column_name -> dtype -> first_value

        Args:
            df: DataFrame to sample.  Does nothing if empty.
        """
        if df is None or df.empty or len(df) == 0:
            return
        print("::: ZoomUs DataFrame sample (first row) :::")
        for column, t in df.dtypes.items():
            try:
                val = df[column].iloc[0]
            except Exception:
                val = "—"
            print(f"{column} -> {t} -> {val}")

    def _add_empty_metrics(self):
        """Add zero metrics when no data is found."""
        for key in (
            "NUMROWS", "NUMCOLS", "RECORDED_COUNT",
            "DOWNLOADED_COUNT", "TRANSCRIPTS_DOWNLOADED",
        ):
            self.add_metric(key, 0)

    def _add_final_metrics(
        self, df, recorded, downloaded, transcripts, s3_count, t0
    ):
        """Add summary metrics at the end of call_logs."""
        self.add_metric("NUMROWS", len(df))
        self.add_metric("NUMCOLS", len(df.columns))
        self.add_metric("RECORDED_COUNT", recorded)
        self.add_metric("DOWNLOADED_COUNT", downloaded)
        self.add_metric("S3_DOWNLOADED_COUNT", s3_count)
        self.add_metric("TRANSCRIPTS_DOWNLOADED", transcripts)
        self.add_metric("SAVE_PATH", str(self.save_path))
        self.add_metric("TRANSCRIPTS_PATH", str(self.transcripts_path))
        self.add_metric("DURATION_SEC", round(time.time() - t0, 3))

    # =================================================================
    # Lifecycle
    # =================================================================

    async def close(self):
        """Cleanup session and S3 client."""
        if self.session and not self.session.closed:
            await self.session.close()
        # S3 client doesn't need explicit close
        return True

