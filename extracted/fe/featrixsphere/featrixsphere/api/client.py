#  -*- coding: utf-8 -*-
#
#  Copyright (c) 2023-2026 Featrix, Inc, All Rights Reserved
#
#  Proprietary and Confidential.  Unauthorized use, copying or dissemination
#  of these materials is strictly prohibited.
#

"""
FeatrixSphere main client class.

This is the entry point for the new FeatrixSphere API.
"""

import io
import gzip
import json
import logging
import os
import uuid
import requests
from pathlib import Path
from typing import Dict, Any, Optional, List, Union, TYPE_CHECKING

if TYPE_CHECKING:
    import pandas as pd
    from .prediction_grid import PredictionGrid

from .http_client import HTTPClientMixin, ClientContext
from .foundational_model import FoundationalModel, PRIORITY_HEADER, _parse_datetime, _validate_priority
from .predictor import Predictor
from .published_predictor import PublishedPredictor
from .published_prediction_network import PublishedPredictionNetwork
from .vector_database import VectorDatabase
from .prediction_result import PredictionFeedback
from .api_endpoint import APIEndpoint
from .event_group import EventGroup
from .notebook_helper import FeatrixNotebookHelper
from ._key_resolution import load_config as _load_config
from ._key_resolution import get_internal_api_key as _get_internal_api_key
from ._key_resolution import internal_key_location as _internal_key_location

logger = logging.getLogger(__name__)


class FeatrixSphere(HTTPClientMixin):
    """
    Main client for interacting with FeatrixSphere.

    This is the entry point for the new object-oriented API.

    Usage:
        from featrixsphere.api import FeatrixSphere

        # Option 1: API key from ~/.featrix or FEATRIX_API_KEY env var
        featrix = FeatrixSphere()

        # Option 2: Explicit API key
        featrix = FeatrixSphere(api_key="sk_live_your_api_key")

        # Create foundational model
        fm = featrix.create_foundational_model(
            name="my_model",
            data_file="data.csv"
        )
        fm.wait_for_training()

        # Create predictor
        predictor = fm.create_binary_classifier(
            name="my_classifier",
            target_column="target"
        )
        predictor.wait_for_training()

        # Make predictions
        result = predictor.predict({"feature1": "value1"})
        print(result.predicted_class)
        print(result.confidence)

    Configuration:
        Create ~/.featrix with your API key:

            echo 'api_key=sk_live_your_api_key' > ~/.featrix

        Or use JSON format:

            {"api_key": "sk_live_...", "base_url": "https://..."}

        Or set environment variable:

            export FEATRIX_API_KEY=sk_live_your_api_key

    On-Premises Deployment:
        Featrix offers on-premises data processing with qualified NVIDIA
        hardware configurations. The API works exactly the same - just
        point your client to your on-premises endpoint:

        featrix = FeatrixSphere(base_url="https://your-on-premises-server.com")
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://sphere-api.featrix.com",
        compute_cluster: Optional[str] = None,
        project: Optional[str] = None,
        default_max_retries: int = 5,
        default_timeout: int = 30,
        retry_base_delay: float = 2.0,
        retry_max_delay: float = 60.0,
        internal: bool = False,
        priority: Optional[str] = None,
    ):
        """
        Initialize the FeatrixSphere client.

        Args:
            api_key: Your Featrix API key. If not provided, looks for:
                1. FEATRIX_API_KEY environment variable
                2. ~/.featrix (file), ~/.featrix/identity.env, ~/.featrix/config,
                   or ~/.featrix_default_key
            base_url: API server URL. Can also be set via FEATRIX_BASE_URL env var
                or in a config file.
            compute_cluster: Compute cluster name (e.g., "burrito", "churro")
            priority: Queue priority for every job this client starts
                (JOB_PRIORITIES; sent as the X-Featrix-Priority header). A
                per-call ``priority=`` argument still wins. None = your
                organization's default tier.
            project: Project name or ID. If provided, verifies the project exists
                and sets it as the current project for all subsequent operations.
            default_max_retries: Default retry count for failed requests
            default_timeout: Default request timeout in seconds
            retry_base_delay: Base delay for exponential backoff
            retry_max_delay: Maximum delay for exponential backoff
            internal: This client call is Featrix's own internal work, not on
                behalf of a customer -- authenticate with the Featrix Internal
                org's key (/etc/.featrix_key, provisioned on every node) instead
                of api_key/FEATRIX_API_KEY/~/.featrix. Every session, job, ES,
                and SP created through this client ends up owned by Featrix
                Internal, not whatever org the ambient key belongs to. Mutually
                exclusive with passing api_key explicitly.

        Raises:
            ValueError: If api_key is not found in arguments, env vars, or config
                file; or if internal=True but no internal key is provisioned on
                this machine; or if both api_key and internal=True are given.

        Config file format (~/.featrix, ~/.featrix/identity.env, ~/.featrix/config,
        or ~/.featrix_default_key):
            JSON:  {"api_key": "fx_...", "base_url": "https://..."}
            or
            Env:   api_key=fx_...
                   base_url=https://...
        """
        if internal:
            if api_key:
                raise ValueError("Pass either api_key or internal=True, not both.")
            api_key = _get_internal_api_key()
            if not api_key:
                raise ValueError(
                    "internal=True but no Featrix Internal key is provisioned on "
                    f"this machine (checked {_internal_key_location()}). "
                    "This only works on nodes that have the internal key installed."
                )

        # Load config from env vars and ~/.featrix
        config = _load_config()

        # Use provided api_key, or fall back to config
        if not api_key:
            api_key = config.get("api_key")

        if not api_key:
            raise ValueError(
                "api_key is required. Provide it as an argument, set FEATRIX_API_KEY "
                "environment variable, or add it to ~/.featrix, ~/.featrix/identity.env, "
                "~/.featrix/config, or ~/.featrix_default_key."
            )

        if not api_key.startswith("fx_"):
            raise ValueError(
                f"Invalid API key (must start with 'fx_'). Got: {api_key[:20]}... "
                "Check ~/.featrix or FEATRIX_API_KEY environment variable."
            )

        # Use provided base_url, or fall back to config (only if not the default)
        if base_url == "https://sphere-api.featrix.com" and "base_url" in config:
            base_url = config["base_url"]

        self._base_url = base_url.rstrip('/')
        self._default_timeout = default_timeout
        self._session = requests.Session()

        # Public — lets callers that already hold an authenticated FeatrixSphere
        # instance (e.g. the ffs CLI) construct a PublishedPredictor /
        # PublishedPredictionNetwork without re-resolving the key/config
        # themselves. Those classes take api_key/base_url explicitly so they
        # stay usable standalone, without a full FeatrixSphere session.
        self.api_key = api_key
        self.base_url = self._base_url

        # Set API key header
        self._session.headers.update({'X-Api-Key': api_key})

        # Set User-Agent
        try:
            from featrixsphere import __version__
            self._session.headers.update({'User-Agent': f'FeatrixSphere {__version__}'})
        except ImportError:
            self._session.headers.update({'User-Agent': 'FeatrixSphere'})

        # Compute cluster
        self._compute_cluster = compute_cluster
        if compute_cluster:
            self._session.headers.update({'X-Featrix-Node': compute_cluster})
        self.set_priority(priority)

        # Retry config
        self._default_max_retries = default_max_retries
        self._retry_base_delay = retry_base_delay
        self._retry_max_delay = retry_max_delay

        # Client context for resource classes
        self._ctx = ClientContext(self)

        # Current project (set via constructor or set_current_project())
        self._current_project_id: Optional[str] = None
        self._current_project: Optional[Dict[str, Any]] = None
        if project:
            self.set_current_project(project)

    def set_compute_cluster(self, cluster: Optional[str]) -> None:
        """
        Set the compute cluster for all subsequent requests.

        Args:
            cluster: Cluster name or None for default
        """
        self._compute_cluster = cluster
        if cluster:
            self._session.headers.update({'X-Featrix-Node': cluster})
        else:
            self._session.headers.pop('X-Featrix-Node', None)

    def set_priority(self, priority: Optional[str]) -> None:
        """
        Set the queue priority for every job this client starts from now on.

        Args:
            priority: One of JOB_PRIORITIES, or None for your organization's default
        """
        self._priority = _validate_priority(priority)
        if priority:
            self._session.headers.update({PRIORITY_HEADER: priority})
        else:
            self._session.headers.pop(PRIORITY_HEADER, None)

    def set_current_project(self, project: str) -> Dict[str, Any]:
        """
        Set the current project for all subsequent operations.

        Verifies the project exists and belongs to your organization by
        calling the API immediately. If the project is not found, raises
        an error.

        Projects are organizational tags, not access boundaries. A predictor
        created under one project can reference a Foundational Model from a
        different project. This lets you maintain shared FMs in one project
        while different teams create predictors in their own projects.

        Args:
            project: Project name, project_id, or UUID

        Returns:
            Project info dict from the API

        Raises:
            requests.HTTPError: If project not found (404) or auth fails (401)

        Example:
            featrix = FeatrixSphere(api_key="fx_...")
            featrix.set_current_project("my-project")

            # All subsequent creates are scoped to this project
            fm = featrix.create_foundational_model(...)
        """
        response = self._get_json(f"/projects/{project}")
        self._current_project_id = response.get('id')
        self._current_project = response
        self._session.headers.update({'X-Featrix-Project': self._current_project_id})
        logger.info(f"Current project set to: {response.get('name')} ({self._current_project_id})")
        return response

    def clear_current_project(self) -> None:
        """
        Clear the current project.

        Subsequent creation operations will not be associated with any project.
        """
        self._current_project_id = None
        self._current_project = None
        self._session.headers.pop('X-Featrix-Project', None)

    @property
    def current_project(self) -> Optional[Dict[str, Any]]:
        """The currently set project, or None."""
        return self._current_project

    def create_foundational_model(
        self,
        name: Optional[str] = None,
        data_file: Optional[str] = None,
        df: Optional['pd.DataFrame'] = None,
        ignore_columns: Optional[List[str]] = None,
        column_overrides: Optional[Dict[str, str]] = None,
        epochs: Optional[int] = None,
        webhooks: Optional[Dict[str, str]] = None,
        user_metadata: Optional[Dict[str, Any]] = None,
        foundation_mode: Optional[bool] = None,
        session_name_prefix: Optional[str] = None,
        sequential_timestamp_col: Optional[str] = None,
        sequential_entity_id_col: Optional[str] = None,
        sequential_window_units: str = "days",
        sequential_window_interval: int = 3,
        sequential_rolling_windows: Optional[List[int]] = None,
        time_column: Optional[str] = None,
        priority: Optional[str] = None,
        **kwargs
    ) -> FoundationalModel:
        """
        Create a foundational model (embedding space).

        Args:
            name: Model name - also used as session directory prefix unless
                session_name_prefix is explicitly provided. Session directory
                will be named {name}-{uuid} instead of {uuid}-{timestamp}.
            data_file: Data source — one of:
                - https:// link, public or presigned (S3, GCS, Azure SAS, ...)
                - Public S3 URL (s3://bucket/path/to/file.csv); for a private
                  bucket pass a presigned https:// link instead
                - Local CSV file path (/path/to/data.csv)
                - Local Parquet file path (/path/to/data.parquet)
                - Local JSON file path (/path/to/data.json)
            df: DataFrame with training data (alternative to data_file)
            ignore_columns: Columns to ignore during training
            column_overrides: Override auto-detected column types. Dict mapping
                column name to type string. Example:
                {"activities": "sparse_multihot", "codes": "sparse_multihot<fips>"}
            epochs: Number of training epochs (None = auto)
            webhooks: Webhook URLs for events
            user_metadata: Custom metadata (max 32KB)
            foundation_mode: Force foundation training mode for large datasets.
                If True, uses foundation training (chunked iteration, SQLite-backed
                splits). If False, uses standard training. If None (default),
                auto-detects based on dataset size (>=100k rows).
            session_name_prefix: Optional explicit prefix for session directory name.
                If provided, overrides the name parameter for directory naming.
                Session directory will be named {prefix}-{uuid}.
            sequential_timestamp_col: For time-ordered data, the column to sort by
                within entity groups (e.g. "purchase_date"). Setting this enables
                derived lag/delta and rolling-window features for every other
                numeric/categorical column. None (default) = feature disabled.
            sequential_entity_id_col: Column to group by (e.g. "customer_id") when
                deriving sequential features. Optional — omit to treat the whole
                dataset as a single entity (e.g. a single time series).
            sequential_window_units: Units for the derived time_since_prev feature —
                "days" or "hours". Only used when sequential_timestamp_col is set.
            sequential_window_interval: Number of lag slots to derive (1-10), e.g.
                3 creates lag_1/lag_2/lag_3 + matching deltas for numeric columns.
            sequential_rolling_windows: Trailing window sizes (in rows) for rolling
                mean/std/min/max over numeric columns, e.g. [7, 30]. Windows are
                causal (never include the current or future rows). None (default)
                = no rolling-window features.
            time_column: For time-ordered data (FOREX bars, sensor streams,
                anything autocorrelated across rows), the column to sort by
                for the train/val split itself. When set, the split is
                chronological — val is strictly LATER in time than train, no
                shuffling, no stratification — instead of the default
                stratified/KL-matched random split. A random split on
                time-ordered data leaks adjacent-in-time rows across
                train/val and inflates every downstream metric. None
                (default) = existing stratified/KL-matched split, unchanged.
                Distinct from sequential_timestamp_col, which derives
                lag/rolling-window features but does not change the split
                method.
            priority: Queue priority for this job — "urgent", "regular", or
                "low" (default: your organization's tier). "urgent" jumps
                ahead of lower-tier work when the fleet is busy.
            **kwargs: Additional parameters

        Returns:
            FoundationalModel object (training started)

        Example:
            # Name controls both metadata AND directory name
            fm = featrix.create_foundational_model(
                name="xx13-xxlarge",  # Directory: xx13-xxlarge-{uuid}
                data_file="customers.csv",
                ignore_columns=["id", "timestamp"]
            )

            # Override directory name separately
            fm = featrix.create_foundational_model(
                name="Customer Model v2",           # Metadata name
                data_file="s3://my-bucket/customers.parquet",
                session_name_prefix="customer-prod"  # Directory: customer-prod-{uuid}
            )

            fm.wait_for_training()
        """
        if df is None and not data_file:
            raise ValueError("Either data_file or df must be provided")
        _validate_priority(priority)

        # If session_name_prefix not provided, use name for directory naming
        if session_name_prefix is None and name:
            session_name_prefix = name

        # URL (https:// or s3://) — the server fetches it; nothing is uploaded.
        # http:// is routed here too so the server can say why it's refused,
        # instead of it failing as a missing local file.
        if data_file and str(data_file).lower().startswith(('s3://', 'https://', 'http://')):
            return self._create_foundational_model_s3(
                name=name,
                s3_url=data_file,
                ignore_columns=ignore_columns,
                column_overrides=column_overrides,
                epochs=epochs,
                webhooks=webhooks,
                user_metadata=user_metadata,
                foundation_mode=foundation_mode,
                session_name_prefix=session_name_prefix,
                priority=priority,
                **kwargs
            )

        # Local file / DataFrame path — upload via multipart
        known_n_rows = None
        known_n_cols = None
        if df is not None:
            if len(df.columns) < 2:
                raise ValueError(
                    f"df has only {len(df.columns)} column(s) ({list(df.columns)}) — "
                    f"Embedding Space training requires at least 2 columns."
                )
            # Exact shape, known for free — no need for the server to guess
            # it from a byte-sample peek. See NODE_SHAPE_CAP routing in
            # sphere-api-router/route_proxy.py.
            known_n_rows = len(df)
            known_n_cols = len(df.columns)
            file_content, filename = self._dataframe_to_file(df)
        else:
            ncols = self._peek_column_count(data_file)
            if ncols is not None and ncols < 2:
                raise ValueError(
                    f"{data_file} has only {ncols} column(s) — "
                    f"Embedding Space training requires at least 2 columns."
                )
            file_content, filename = self._read_file(data_file)

        # Build form data
        form_data = {}
        if name:
            form_data['name'] = name
        if session_name_prefix:
            form_data['session_name_prefix'] = session_name_prefix
        if ignore_columns:
            form_data['ignore_columns'] = json.dumps(ignore_columns)
        if column_overrides:
            form_data['column_overrides'] = json.dumps(column_overrides)
        if epochs is not None:
            form_data['epochs'] = str(epochs)
        if webhooks:
            form_data['webhooks'] = json.dumps(webhooks)
        if user_metadata:
            form_data['user_metadata'] = json.dumps(user_metadata)
        if foundation_mode is not None:
            form_data['foundation_mode'] = str(foundation_mode).lower()
        if known_n_rows is not None:
            form_data['n_rows'] = str(known_n_rows)
            form_data['n_cols'] = str(known_n_cols)
        if self._current_project_id:
            form_data['project_id'] = self._current_project_id
        if sequential_timestamp_col:
            form_data['sequential_timestamp_col'] = sequential_timestamp_col
            if sequential_entity_id_col:
                form_data['sequential_entity_id_col'] = sequential_entity_id_col
            form_data['sequential_window_units'] = sequential_window_units
            form_data['sequential_window_interval'] = str(sequential_window_interval)
            if sequential_rolling_windows:
                form_data['sequential_rolling_windows'] = json.dumps(sequential_rolling_windows)
        if time_column:
            form_data['time_column'] = time_column
        if priority:
            form_data['priority'] = priority

        # Add any extra kwargs
        for key, value in kwargs.items():
            if value is not None:
                if isinstance(value, (dict, list)):
                    form_data[key] = json.dumps(value)
                else:
                    form_data[key] = str(value)

        # Upload file and create session
        files = {'file': (filename, file_content)}

        # One idempotency key per logical call, sent on every retry
        # _make_request performs internally — lets the router collapse a
        # retried upload into the original session instead of fanning out
        # into a duplicate (see docs/internal/plans/2026-07-upload-session-idempotency-key.md).
        idempotency_key = str(uuid.uuid4())

        response = self._post_multipart(
            "/compute/upload_with_new_session/",
            data=form_data,
            files=files,
            headers={'X-Featrix-Idempotency-Key': idempotency_key},
        )

        session_id = response.get('session_id', '')

        # Handle warnings
        warnings = response.get('warnings', [])
        if warnings:
            for warning in warnings:
                logger.warning(f"Upload warning: {warning}")

        # If the router queued the job (all ES nodes busy), surface that to the
        # caller instead of pretending a session is live on a compute node.
        is_queued = bool(response.get('queued'))
        if is_queued:
            queue_position = response.get('queue_position')
            pos_str = f" (position {queue_position})" if queue_position else ""
            logger.info(
                f"📥 Job queued{pos_str} — all compute nodes are busy. "
                f"Session will start when one becomes available. "
                f"session_id={session_id}"
            )

        return FoundationalModel(
            id=session_id,
            name=name,
            status="queued" if is_queued else "training",
            created_at=None,
            compute_cluster=response.get('compute_cluster'),
            _ctx=self._ctx,
        )

    def _create_foundational_model_and_wait(
        self,
        data_file: Optional[str],
        df: Optional['pd.DataFrame'],
        name: Optional[str],
        fm_name: Optional[str],
        ignore_columns: Optional[List[str]],
        column_overrides: Optional[Dict[str, str]],
        fm_epochs: Optional[int],
        webhooks: Optional[Dict[str, str]],
        user_metadata: Optional[Dict[str, Any]],
        foundation_mode: Optional[bool],
        max_wait_time: int,
        poll_interval: int,
        show_progress: bool,
    ) -> FoundationalModel:
        """
        Shared ES-creation step for the one-shot create_* convenience methods.

        Always waits for the ES to finish — a predictor cannot be trained on
        an ES that's still training, so this wait is not optional the way the
        final predictor wait is (see `block` on the public methods).
        """
        fm = self.create_foundational_model(
            name=fm_name or name,
            data_file=data_file,
            df=df,
            ignore_columns=ignore_columns,
            column_overrides=column_overrides,
            epochs=fm_epochs,
            webhooks=webhooks,
            user_metadata=user_metadata,
            foundation_mode=foundation_mode,
        )
        fm.wait_for_training(
            max_wait_time=max_wait_time,
            poll_interval=poll_interval,
            show_progress=show_progress,
        )
        return fm

    def create_binary_classifier(
        self,
        target_column: str,
        data_file: Optional[str] = None,
        df: Optional['pd.DataFrame'] = None,
        name: Optional[str] = None,
        fm_name: Optional[str] = None,
        ignore_columns: Optional[List[str]] = None,
        column_overrides: Optional[Dict[str, str]] = None,
        fm_epochs: Optional[int] = None,
        predictor_epochs: int = 0,
        rare_label_value: Optional[str] = None,
        class_imbalance: Optional[Dict[str, float]] = None,
        cost_false_positive: Optional[float] = None,
        cost_false_negative: Optional[float] = None,
        intent: Optional[str] = None,
        auto_collapse_synonyms: Optional[bool] = None,
        synonym_collapse_threshold: Optional[float] = None,
        label_mapping: Optional[Dict[str, str]] = None,
        group_column: Optional[str] = None,
        webhooks: Optional[Dict[str, str]] = None,
        user_metadata: Optional[Dict[str, Any]] = None,
        foundation_mode: Optional[bool] = None,
        block: bool = True,
        max_wait_time: int = 3600,
        poll_interval: int = 10,
        show_progress: bool = True,
        **kwargs,
    ) -> Predictor:
        """
        Train an embedding space AND a binary classifier on it in one call.

        For callers who just want a model for `target_column` and don't want
        to think about the embedding space as a separate object. Internally
        this is exactly the two-step flow —
            fm = self.create_foundational_model(...); fm.wait_for_training()
            predictor = fm.create_binary_classifier(...); predictor.wait_for_training()
        — with the intermediate FoundationalModel still reachable via
        `predictor.foundational_model` for anyone who wants it (encode(),
        create_vector_database(), a second predictor on the same ES, etc.).

        Args:
            target_column: Column to predict (exactly 2 unique values).
            data_file: Data source (S3 URL / local CSV / Parquet / JSON path).
                One of data_file or df is required.
            df: DataFrame with training data (alternative to data_file).
            name: Predictor name (optional). Also used as the ES name unless
                fm_name is given.
            fm_name: Explicit ES name, if different from the predictor name.
            ignore_columns: Columns to ignore during ES training.
            column_overrides: Override auto-detected column types (ES-level).
            fm_epochs: Embedding space training epochs (None = auto).
            predictor_epochs: Predictor training epochs (0 = auto).
            rare_label_value: Which class is the minority/positive class for metrics.
            class_imbalance: Expected real-world class distribution, e.g.
                {"approved": 0.97, "rejected": 0.03}.
            cost_false_positive: Cost of a false positive. Implies
                intent="minimize_cost" when intent is not explicitly provided.
            cost_false_negative: Cost of a false negative.
            intent: Plain-language objective — see
                FoundationalModel.create_binary_classifier for the full list
                ("balanced", "only_alert_when_confident", "catch_everything",
                "catch_everything_aggressive", "minimize_cost", "rank",
                "predict_probabilities").
            auto_collapse_synonyms: Auto-detect and merge near-duplicate class
                labels (default: True via config).
            synonym_collapse_threshold: Cosine similarity threshold for
                synonym detection (default: 0.90 via config).
            label_mapping: Explicit old→new class name mapping.
            group_column: Optional column for group-aware train/val splitting.
            webhooks: Forwarded to BOTH the ES and predictor training calls.
            user_metadata, foundation_mode: Forwarded to create_foundational_model.
            block: If True (default), block until the predictor finishes
                training and return it ready for .predict(). The ES wait
                always happens regardless of this flag — a predictor cannot
                be created on an ES that's still training. If False, skip
                only the final predictor wait; caller must call
                predictor.wait_for_training() themselves before predicting.
            max_wait_time, poll_interval, show_progress: Forwarded to both
                wait_for_training() calls.
            **kwargs: Additional params forwarded to create_binary_classifier
                (e.g. server-side knobs not yet promoted to named args).

        Returns:
            Predictor object. If block=True, training is complete and
            predictor.predict(...) is ready to call immediately.
            predictor.foundational_model gives access to the underlying ES.

        Example:
            predictor = featrix.create_binary_classifier(
                target_column="churned",
                data_file="customers.csv",
                rare_label_value="yes",
                intent="catch_everything",
            )
            result = predictor.predict({"age": 35, "plan": "premium"})
        """
        if df is None and not data_file:
            raise ValueError("Either data_file or df must be provided")

        fm = self._create_foundational_model_and_wait(
            data_file=data_file,
            df=df,
            name=name,
            fm_name=fm_name,
            ignore_columns=ignore_columns,
            column_overrides=column_overrides,
            fm_epochs=fm_epochs,
            webhooks=webhooks,
            user_metadata=user_metadata,
            foundation_mode=foundation_mode,
            max_wait_time=max_wait_time,
            poll_interval=poll_interval,
            show_progress=show_progress,
        )
        predictor = fm.create_binary_classifier(
            target_column=target_column,
            name=name,
            epochs=predictor_epochs,
            rare_label_value=rare_label_value,
            class_imbalance=class_imbalance,
            cost_false_positive=cost_false_positive,
            cost_false_negative=cost_false_negative,
            intent=intent,
            auto_collapse_synonyms=auto_collapse_synonyms,
            synonym_collapse_threshold=synonym_collapse_threshold,
            label_mapping=label_mapping,
            group_column=group_column,
            webhooks=webhooks,
            **kwargs,
        )
        if block:
            predictor.wait_for_training(
                max_wait_time=max_wait_time,
                poll_interval=poll_interval,
                show_progress=show_progress,
            )
        return predictor

    def create_multi_classifier(
        self,
        target_column: str,
        data_file: Optional[str] = None,
        df: Optional['pd.DataFrame'] = None,
        name: Optional[str] = None,
        fm_name: Optional[str] = None,
        ignore_columns: Optional[List[str]] = None,
        column_overrides: Optional[Dict[str, str]] = None,
        fm_epochs: Optional[int] = None,
        predictor_epochs: int = 0,
        class_imbalance: Optional[Dict[str, float]] = None,
        intent: Optional[str] = None,
        k: Optional[int] = None,
        auto_collapse_synonyms: Optional[bool] = None,
        synonym_collapse_threshold: Optional[float] = None,
        label_mapping: Optional[Dict[str, str]] = None,
        webhooks: Optional[Dict[str, str]] = None,
        user_metadata: Optional[Dict[str, Any]] = None,
        foundation_mode: Optional[bool] = None,
        block: bool = True,
        max_wait_time: int = 3600,
        poll_interval: int = 10,
        show_progress: bool = True,
        **kwargs,
    ) -> Predictor:
        """
        Train an embedding space AND a multiclass classifier on it in one call.

        Task-specific args (target_column, class_imbalance, intent, k,
        auto_collapse_synonyms, synonym_collapse_threshold, label_mapping) are
        identical to FoundationalModel.create_multi_classifier. Data/ES-level
        args (data_file, df, name, fm_name, ignore_columns, column_overrides,
        fm_epochs, predictor_epochs, webhooks, user_metadata, foundation_mode,
        block, max_wait_time, poll_interval, show_progress) are identical to
        create_binary_classifier above — see that docstring for full semantics.

        Returns:
            Predictor object (trained and ready if block=True).

        Example:
            predictor = featrix.create_multi_classifier(
                target_column="product_category",
                data_file="orders.csv",
                intent="top_k_hit",
                k=3,
            )
        """
        if df is None and not data_file:
            raise ValueError("Either data_file or df must be provided")

        fm = self._create_foundational_model_and_wait(
            data_file=data_file,
            df=df,
            name=name,
            fm_name=fm_name,
            ignore_columns=ignore_columns,
            column_overrides=column_overrides,
            fm_epochs=fm_epochs,
            webhooks=webhooks,
            user_metadata=user_metadata,
            foundation_mode=foundation_mode,
            max_wait_time=max_wait_time,
            poll_interval=poll_interval,
            show_progress=show_progress,
        )
        predictor = fm.create_multi_classifier(
            target_column=target_column,
            name=name,
            epochs=predictor_epochs,
            class_imbalance=class_imbalance,
            intent=intent,
            k=k,
            auto_collapse_synonyms=auto_collapse_synonyms,
            synonym_collapse_threshold=synonym_collapse_threshold,
            label_mapping=label_mapping,
            webhooks=webhooks,
            **kwargs,
        )
        if block:
            predictor.wait_for_training(
                max_wait_time=max_wait_time,
                poll_interval=poll_interval,
                show_progress=show_progress,
            )
        return predictor

    def create_multi_label_classifier(
        self,
        target_column: str,
        data_file: Optional[str] = None,
        df: Optional['pd.DataFrame'] = None,
        name: Optional[str] = None,
        fm_name: Optional[str] = None,
        ignore_columns: Optional[List[str]] = None,
        column_overrides: Optional[Dict[str, str]] = None,
        fm_epochs: Optional[int] = None,
        predictor_epochs: int = 0,
        class_imbalance: Optional[Dict[str, float]] = None,
        webhooks: Optional[Dict[str, str]] = None,
        user_metadata: Optional[Dict[str, Any]] = None,
        foundation_mode: Optional[bool] = None,
        block: bool = True,
        max_wait_time: int = 3600,
        poll_interval: int = 10,
        show_progress: bool = True,
        **kwargs,
    ) -> Predictor:
        """
        Train an embedding space AND a multi-label classifier on it in one call.

        Task-specific args (target_column, class_imbalance, plus **kwargs
        knobs sp_multilabel_threshold / sp_multilabel_loss_type /
        sp_multilabel_use_pos_weight) are identical to
        FoundationalModel.create_multi_label_classifier. Data/ES-level args
        are identical to create_binary_classifier above.

        Returns:
            Predictor object (trained and ready if block=True).

        Example:
            predictor = featrix.create_multi_label_classifier(
                target_column="genres",
                data_file="movies.csv",
            )
        """
        if df is None and not data_file:
            raise ValueError("Either data_file or df must be provided")

        fm = self._create_foundational_model_and_wait(
            data_file=data_file,
            df=df,
            name=name,
            fm_name=fm_name,
            ignore_columns=ignore_columns,
            column_overrides=column_overrides,
            fm_epochs=fm_epochs,
            webhooks=webhooks,
            user_metadata=user_metadata,
            foundation_mode=foundation_mode,
            max_wait_time=max_wait_time,
            poll_interval=poll_interval,
            show_progress=show_progress,
        )
        predictor = fm.create_multi_label_classifier(
            target_column=target_column,
            name=name,
            epochs=predictor_epochs,
            class_imbalance=class_imbalance,
            webhooks=webhooks,
            **kwargs,
        )
        if block:
            predictor.wait_for_training(
                max_wait_time=max_wait_time,
                poll_interval=poll_interval,
                show_progress=show_progress,
            )
        return predictor

    def create_regressor(
        self,
        target_column: str,
        data_file: Optional[str] = None,
        df: Optional['pd.DataFrame'] = None,
        allow_null: bool = False,
        name: Optional[str] = None,
        fm_name: Optional[str] = None,
        ignore_columns: Optional[List[str]] = None,
        column_overrides: Optional[Dict[str, str]] = None,
        fm_epochs: Optional[int] = None,
        predictor_epochs: int = 0,
        intent: Optional[str] = None,
        group_column: Optional[str] = None,
        webhooks: Optional[Dict[str, str]] = None,
        user_metadata: Optional[Dict[str, Any]] = None,
        foundation_mode: Optional[bool] = None,
        block: bool = True,
        max_wait_time: int = 3600,
        poll_interval: int = 10,
        show_progress: bool = True,
        **kwargs,
    ) -> Predictor:
        """
        Train an embedding space AND a regressor on it in one call.

        Task-specific args (target_column, allow_null, intent, group_column)
        are identical to FoundationalModel.create_regressor. Data/ES-level
        args are identical to create_binary_classifier above.

        Returns:
            Predictor object (trained and ready if block=True).

        Example:
            predictor = featrix.create_regressor(
                target_column="price",
                data_file="listings.csv",
                intent="minimize_relative_error",
            )
        """
        if df is None and not data_file:
            raise ValueError("Either data_file or df must be provided")

        fm = self._create_foundational_model_and_wait(
            data_file=data_file,
            df=df,
            name=name,
            fm_name=fm_name,
            ignore_columns=ignore_columns,
            column_overrides=column_overrides,
            fm_epochs=fm_epochs,
            webhooks=webhooks,
            user_metadata=user_metadata,
            foundation_mode=foundation_mode,
            max_wait_time=max_wait_time,
            poll_interval=poll_interval,
            show_progress=show_progress,
        )
        predictor = fm.create_regressor(
            target_column=target_column,
            allow_null=allow_null,
            name=name,
            epochs=predictor_epochs,
            intent=intent,
            group_column=group_column,
            webhooks=webhooks,
            **kwargs,
        )
        if block:
            predictor.wait_for_training(
                max_wait_time=max_wait_time,
                poll_interval=poll_interval,
                show_progress=show_progress,
            )
        return predictor

    def create_generative_string_model(
        self,
        target_column: str,
        data_file: Optional[str] = None,
        df: Optional['pd.DataFrame'] = None,
        name: Optional[str] = None,
        fm_name: Optional[str] = None,
        ignore_columns: Optional[List[str]] = None,
        column_overrides: Optional[Dict[str, str]] = None,
        fm_epochs: Optional[int] = None,
        webhooks: Optional[Dict[str, str]] = None,
        user_metadata: Optional[Dict[str, Any]] = None,
        foundation_mode: Optional[bool] = None,
        block: bool = True,
        max_wait_time: int = 3600,
        poll_interval: int = 10,
        show_progress: bool = True,
        **kwargs,
    ) -> Predictor:
        """
        Train an embedding space AND a generative-string predictor on it in
        one call: generate the right value of ``target_column`` (e.g. a
        company description) from the row's other columns.

        Task-specific args (target_column) are identical to
        FoundationalModel.create_generative_string_model. Data/ES-level args
        are identical to create_binary_classifier above.

        Unlike every other predictor type there's no gradient-trained head
        — index build is much faster than a normal training run.

        Returns:
            Predictor object (index built and ready if block=True).

        Example:
            predictor = featrix.create_generative_string_model(
                target_column="company_description",
                data_file="companies.csv",
            )
            result = predictor.predict({"industry": "logistics", "state": "CA"})
            print(result.predicted_class)  # nearest training row's description

            result = predictor.predict(
                {"industry": "logistics", "state": "CA"}, generate=True,
            )
            print(result.predicted_class)  # LLM-generated, not verbatim
        """
        if df is None and not data_file:
            raise ValueError("Either data_file or df must be provided")

        fm = self._create_foundational_model_and_wait(
            data_file=data_file,
            df=df,
            name=name,
            fm_name=fm_name,
            ignore_columns=ignore_columns,
            column_overrides=column_overrides,
            fm_epochs=fm_epochs,
            webhooks=webhooks,
            user_metadata=user_metadata,
            foundation_mode=foundation_mode,
            max_wait_time=max_wait_time,
            poll_interval=poll_interval,
            show_progress=show_progress,
        )
        predictor = fm.create_generative_string_model(
            target_column=target_column,
            name=name,
            webhooks=webhooks,
            **kwargs,
        )
        if block:
            predictor.wait_for_training(
                max_wait_time=max_wait_time,
                poll_interval=poll_interval,
                show_progress=show_progress,
            )
        return predictor

    def create_ranking_predictor(
        self,
        target_column: Optional[str] = None,
        *,
        group_column: str,
        data_file: Optional[str] = None,
        df: Optional['pd.DataFrame'] = None,
        use_row_order: bool = False,
        name: Optional[str] = None,
        fm_name: Optional[str] = None,
        ignore_columns: Optional[List[str]] = None,
        column_overrides: Optional[Dict[str, str]] = None,
        fm_epochs: Optional[int] = None,
        predictor_epochs: int = 0,
        webhooks: Optional[Dict[str, str]] = None,
        user_metadata: Optional[Dict[str, Any]] = None,
        foundation_mode: Optional[bool] = None,
        block: bool = True,
        max_wait_time: int = 3600,
        poll_interval: int = 10,
        show_progress: bool = True,
        **kwargs,
    ) -> Predictor:
        """
        Train an embedding space AND a learning-to-rank predictor on it in one call.

        Task-specific args (target_column, group_column, use_row_order) are
        identical to FoundationalModel.create_ranking_predictor. Data/ES-level
        args are identical to create_binary_classifier above.

        Returns:
            Predictor object (trained and ready if block=True). Scored as
            mean per-group NDCG.

        Example:
            predictor = featrix.create_ranking_predictor(
                data_file="search_logs.csv",
                group_column="query_id",
                use_row_order=True,
            )
        """
        if df is None and not data_file:
            raise ValueError("Either data_file or df must be provided")

        fm = self._create_foundational_model_and_wait(
            data_file=data_file,
            df=df,
            name=name,
            fm_name=fm_name,
            ignore_columns=ignore_columns,
            column_overrides=column_overrides,
            fm_epochs=fm_epochs,
            webhooks=webhooks,
            user_metadata=user_metadata,
            foundation_mode=foundation_mode,
            max_wait_time=max_wait_time,
            poll_interval=poll_interval,
            show_progress=show_progress,
        )
        predictor = fm.create_ranking_predictor(
            target_column=target_column,
            group_column=group_column,
            use_row_order=use_row_order,
            name=name,
            epochs=predictor_epochs,
            webhooks=webhooks,
            **kwargs,
        )
        if block:
            predictor.wait_for_training(
                max_wait_time=max_wait_time,
                poll_interval=poll_interval,
                show_progress=show_progress,
            )
        return predictor

    def _create_foundational_model_s3(
        self,
        name: Optional[str],
        s3_url: str,
        ignore_columns: Optional[List[str]] = None,
        column_overrides: Optional[Dict[str, str]] = None,
        epochs: Optional[int] = None,
        webhooks: Optional[Dict[str, str]] = None,
        user_metadata: Optional[Dict[str, Any]] = None,
        foundation_mode: Optional[bool] = None,
        session_name_prefix: Optional[str] = None,
        priority: Optional[str] = None,
        **kwargs
    ) -> FoundationalModel:
        """Create foundational model from S3 URL via the create-embedding-space endpoint."""

        data = {
            "name": name or "",
            "s3_file_data_set_training": s3_url,
        }
        if session_name_prefix:
            data['session_name_prefix'] = session_name_prefix
        if ignore_columns:
            data['ignore_columns'] = ignore_columns
        if column_overrides:
            data['column_overrides'] = column_overrides
        if epochs is not None:
            data['epochs'] = epochs
        if webhooks:
            data['webhooks'] = webhooks
        if user_metadata:
            data['user_metadata'] = json.dumps(user_metadata)
        if foundation_mode is not None:
            data['foundation_mode'] = foundation_mode
        if priority:
            data['priority'] = priority
        if self._current_project_id:
            data['project_id'] = self._current_project_id

        for key, value in kwargs.items():
            if value is not None:
                data[key] = value

        response = self._post_json(
            "/compute/create-embedding-space",
            data=data
        )

        session_id = response.get('session_id', '')

        is_queued = bool(response.get('queued'))
        if is_queued:
            queue_position = response.get('queue_position')
            pos_str = f" (position {queue_position})" if queue_position else ""
            logger.info(
                f"📥 Job queued{pos_str} — all compute nodes are busy. "
                f"Session will start when one becomes available. "
                f"session_id={session_id}"
            )

        return FoundationalModel(
            id=session_id,
            name=name,
            status="queued" if is_queued else "training",
            created_at=None,
            compute_cluster=response.get('compute_cluster'),
            _ctx=self._ctx,
        )

    def foundational_model(self, fm_id: str) -> FoundationalModel:
        """
        Get an existing foundational model by ID.

        Args:
            fm_id: Foundational model (session) ID

        Returns:
            FoundationalModel object

        Example:
            fm = featrix.foundational_model("abc123")
            print(fm.status)
        """
        return FoundationalModel.from_session_id(fm_id, self._ctx)

    def predictor(self, session_id: str, predictor_id: Optional[str] = None) -> Predictor:
        """
        Get a predictor for a session.

        Most sessions have exactly one predictor, in which case predictor_id
        can be omitted. Sessions with more than one trained predictor (e.g.
        multiple target columns on the same embedding space) MUST pass the
        specific predictor_id — omitting it is only safe for the single-
        predictor case. Use list_predictors() to enumerate the available ids.

        Args:
            session_id: Session ID
            predictor_id: Which predictor to fetch. Required when the session
                has more than one; if omitted, the session's only predictor
                is returned (or an error if there's more than one).

        Returns:
            Predictor object

        Raises:
            ValueError: no predictor found, or predictor_id doesn't match any
                trained predictor in this session (never silently falls back
                to a different one).
        """
        # Get session info
        response = self._get_json(f"/compute/session/{session_id}")
        session = response.get('session', {})
        jobs = response.get('jobs') or {}

        # Find the train_single_predictor entry in job_plan matching
        # predictor_id (same id derivation as FoundationalModel.list_predictors:
        # job_plan's own predictor_id, falling back to "predictor-{target_column}").
        # NEVER just take the first entry when predictor_id is given — a
        # session can have multiple predictors, and silently returning the
        # wrong one's target_column/metrics is the exact bug class this
        # guards against.
        matches = []
        for job_entry in session.get('job_plan', []):
            if job_entry.get('job_type') != 'train_single_predictor':
                continue
            spec = job_entry.get('spec', {})
            entry_target_column = spec.get('target_column', job_entry.get('target_column', ''))
            entry_pred_id = job_entry.get('predictor_id') or f"predictor-{entry_target_column}"
            matches.append((entry_pred_id, job_entry, spec, entry_target_column))

        if predictor_id is not None:
            selected = [m for m in matches if m[0] == predictor_id]
            if not selected:
                available = [m[0] for m in matches]
                raise ValueError(
                    f"predictor_id={predictor_id!r} not found in session {session_id} "
                    f"(available: {available})"
                )
            _, job_entry, spec, target_column = selected[0]
        elif matches:
            if len(matches) > 1:
                available = [m[0] for m in matches]
                raise ValueError(
                    f"Session {session_id} has {len(matches)} predictors — "
                    f"predictor_id is required (available: {available})"
                )
            _, job_entry, spec, target_column = matches[0]
        else:
            job_entry, spec, target_column = {}, {}, None

        target_type = spec.get('target_column_type', job_entry.get('target_column_type', 'set'))
        job_id = job_entry.get('job_id')

        if target_column is None:
            raise ValueError(f"No predictor found in session {session_id}")

        # The live Redis job record (if not yet TTL'd out) carries the real
        # created_at/accuracy/auc/f1 for this predictor — job_plan itself
        # doesn't persist them.
        live_job = jobs.get(job_id) if job_id else None
        accuracy = auc = f1 = created_at = None
        if live_job:
            accuracy = live_job.get('accuracy')
            auc = live_job.get('auc') or live_job.get('roc_auc')
            f1 = live_job.get('f1') or live_job.get('f1_score')
            created_at = _parse_datetime(live_job.get('created_at'))

        return Predictor(
            id=predictor_id or session_id,
            session_id=session_id,
            target_column=target_column,
            target_type=target_type,
            name=session.get('name'),
            status=session.get('status'),
            accuracy=accuracy,
            auc=auc,
            f1=f1,
            created_at=created_at,
            _ctx=self._ctx,
        )

    def vector_database(self, session_id: str, name: str = "default") -> VectorDatabase:
        """
        Get a named vector database from a foundational model session.

        Args:
            session_id: Foundational model (session) ID
            name: Vector database name (default: "default")

        Returns:
            VectorDatabase object

        Example:
            vdb = featrix.vector_database("abc123", "customers")
            results = vdb.similarity_search({"age": 35}, k=5)
        """
        response = self._get_json(
            f"/session/{session_id}/vector_databases/{name}"
        )
        return VectorDatabase.from_api_response(
            data=response,
            session_id=session_id,
            ctx=self._ctx,
        )

    def list_api_endpoints(self) -> List[APIEndpoint]:
        """Every API endpoint in your organization."""
        response = self._get_json("/endpoints")
        return [APIEndpoint.from_response(e, ctx=self._ctx) for e in response.get('endpoints', [])]

    def api_endpoint(self, endpoint_id: str) -> APIEndpoint:
        """
        Get an API endpoint: its serving model, shadows, and how each shadow
        does against the serving model on the same labelled requests.
        """
        return APIEndpoint.from_response(self._get_json(f"/endpoints/{endpoint_id}"), ctx=self._ctx)

    def bind_api_endpoint(self, model_name: str) -> APIEndpoint:
        """
        Serve one of your published models through an endpoint. Callers keep
        using the same name; the version published now keeps serving, and a
        retrain of it shadows (same traffic, graded, never answering) until
        you promote it. Returns the endpoint with its API key (shown once).
        """
        response = self._post_json("/endpoints/bind", {"model_name": model_name}, max_retries=1)
        return APIEndpoint.from_response(response, ctx=self._ctx)

    def list_event_groups(self, limit: int = 50, offset: int = 0) -> List[EventGroup]:
        """
        List event groups registered for the authenticated org -- i.e.
        groups that have received at least one event via featrixevents'
        featrix_post_event(). A group that's never received an event never
        appears here.

        Note: event_count is None on list results (only the cheaper,
        possibly-stale event_count_at_last_train is included) -- call
        event_group(id) or .refresh() on a result for a live count.

        Args:
            limit: Max groups to return (server clamps to 200).
            offset: Pagination offset.

        Returns:
            List of EventGroup objects.
        """
        response = self._get_json("/events/groups", params={'limit': limit, 'offset': offset})
        return [
            EventGroup.from_response(item, ctx=self._ctx)
            for item in response.get('event_groups', [])
        ]

    def event_group(self, event_group_id: str) -> EventGroup:
        """
        Get one event group's detail, including a live event count.

        Args:
            event_group_id: UUID grouping related events.

        Returns:
            EventGroup object.
        """
        response = self._get_json(f"/events/groups/{event_group_id}")
        return EventGroup.from_response(response, ctx=self._ctx)

    def published_predictor(
        self,
        org: str,
        name: str,
        api_key: str,
        base_url: str = "https://sphere-api.featrix.com"
    ) -> PublishedPredictor:
        """
        Load a published predictor for making predictions.

        Published predictors are served via the Sphere API, which routes
        predictions to production-ai and handles UUID tracking, logging,
        and feedback.

        Args:
            org: Organization ID
            name: Model name
            api_key: API key for authentication
            base_url: Sphere API URL (default: https://sphere-api.featrix.com)

        Returns:
            PublishedPredictor instance

        Example:
            # Load a published predictor
            predictor = client.published_predictor(
                org="alph",
                name="my-model",
                api_key="sk_alph_xxx"
            )

            # Make single prediction
            result = predictor.predict({"age": 35, "income": 50000})
            print(result.predicted_class)
            print(result.confidence)

            # Batch predictions
            results = predictor.batch_predict([
                {"age": 35, "income": 50000},
                {"age": 42, "income": 75000}
            ])
        """
        return PublishedPredictor(
            org=org,
            name=name,
            api_key=api_key,
            base_url=base_url,
            _ctx=self._ctx,
        )

    def published_prediction_network(
        self,
        org: str,
        name: str,
        api_key: str,
        base_url: str = "https://sphere-api.featrix.com"
    ) -> PublishedPredictionNetwork:
        """
        Load a PredictionNetwork for making chained predictions across
        several of your own published models.

        Args:
            org: Organization ID
            name: PredictionNetwork name
            api_key: API key for authentication
            base_url: Sphere API URL (default: https://sphere-api.featrix.com)
                Deliberately a separate parameter from published_predictor's
                base_url — if PredictionNetworks moves to its own host later,
                only this default needs to change.

        Returns:
            PublishedPredictionNetwork instance

        Example:
            network = client.published_prediction_network(
                org="alph",
                name="carrier-qualification",
                api_key="sk_alph_xxx",
            )
            network.register({
                "nodes": [{"id": "is_company", "model": "is-company"}],
                "edges": [],
            })
            result = network.predict({"company_name": "Acme Trucking Co"})
            print(result.final)
        """
        return PublishedPredictionNetwork(
            org=org,
            name=name,
            api_key=api_key,
            base_url=base_url,
            _ctx=self._ctx,
        )

    def list_prediction_networks(self, org: str) -> List[Dict[str, Any]]:
        """
        List PredictionNetworks registered for an org.

        Args:
            org: Organization ID

        Returns:
            List of {"name", "version", "created_at", "updated_at"} dicts.

        Example:
            for net in client.list_prediction_networks("alph"):
                print(net["name"], "v" + str(net["version"]))
        """
        response = self._get_json(f"/prediction-network/{org}")
        return response.get("networks", [])

    def get_notebook(self) -> FeatrixNotebookHelper:
        """
        Get the Jupyter notebook visualization helper.

        Returns a helper object with methods for visualizing training,
        embedding spaces, and model analysis in Jupyter notebooks.

        Returns:
            FeatrixNotebookHelper instance

        Example:
            notebook = featrix.get_notebook()
            fig = notebook.training_loss(fm)
            fig.show()
        """
        return FeatrixNotebookHelper(ctx=self._ctx)

    def prediction_feedback(
        self,
        prediction_uuid: str,
        ground_truth: Union[str, float],
        session_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Send feedback for a prediction.

        Convenience method that creates and sends feedback in one call.

        Args:
            prediction_uuid: UUID from PredictionResult.prediction_uuid
            ground_truth: The correct label/value
            session_id: Session that served the prediction
                (PredictionResult.session_id). Pass it for session-served
                predictions — their prediction_uuid lives on sphere-api's audit
                row, not in the compute node's label store. For a published
                model's prediction use PublishedPredictor.send_feedback().

        Returns:
            Server response
        """
        return PredictionFeedback.create_and_send(
            ctx=self._ctx,
            prediction_uuid=prediction_uuid,
            ground_truth=ground_truth,
            session_id=session_id,
        )

    def predict_grid(
        self,
        fm_id: str,
        degrees_of_freedom: int,
        grid_shape: tuple = None,
        target_column: str = None,
        predictor_id: str = None,
    ) -> 'PredictionGrid':
        """
        Create a prediction grid for exploring parameter surfaces with visualization.

        Resolves the predictor from the foundational model, then creates a grid.

        Args:
            fm_id: Foundational model (session) ID
            degrees_of_freedom: Number of dimensions (1, 2, or 3)
            grid_shape: Custom grid shape tuple (default: auto-sized)
            target_column: Target column to find predictor for (if multiple predictors)
            predictor_id: Specific predictor ID to use

        Returns:
            PredictionGrid object with predict() and plotting methods

        Example:
            grid = featrix.predict_grid(fm_id, degrees_of_freedom=2, grid_shape=(19, 8))
            grid.set_axis_labels(["Spend ($)", "Ad Set Campaign"])

            for i, spend in enumerate(spend_levels):
                for j, ad_set in enumerate(ad_sets):
                    grid.predict({"spend": spend, "ad_set_name": ad_set}, grid_position=(i, j))

            grid.process_batch()
            grid.plot_heatmap()
        """
        from .prediction_grid import PredictionGrid

        # Resolve predictor
        if predictor_id:
            pred = self.predictor(fm_id, predictor_id=predictor_id)
        else:
            fm = self.foundational_model(fm_id)
            predictors = fm.list_predictors()
            if not predictors:
                raise ValueError(f"No predictors found for foundational model {fm_id}")
            if target_column:
                matches = [p for p in predictors if p.target_column == target_column]
                if not matches:
                    available = [p.target_column for p in predictors]
                    raise ValueError(
                        f"No predictor found for target_column='{target_column}'. "
                        f"Available: {available}"
                    )
                pred = matches[0]
            elif len(predictors) == 1:
                pred = predictors[0]
            else:
                available = [f"{p.id} (target={p.target_column})" for p in predictors]
                raise ValueError(
                    f"Multiple predictors found. Specify target_column or predictor_id. "
                    f"Available: {available}"
                )

        return PredictionGrid(predictor=pred, degrees_of_freedom=degrees_of_freedom, grid_shape=grid_shape)

    def list_sessions(
        self,
        name_prefix: str = "",
    ) -> List[FoundationalModel]:
        """
        List foundational models (embedding spaces) for the authenticated org.

        Args:
            name_prefix: Optional search term to filter by name or session ID

        Returns:
            List of FoundationalModel summary objects

        Example:
            models = featrix.list_sessions()
            for fm in models:
                print(f"{fm.id}: {fm.name} ({fm.status})")
        """
        params = {}
        if name_prefix:
            params['name_prefix'] = name_prefix
        response = self._get_json("/compute/sessions-for-org", params=params)

        sessions = response.get('sessions', [])

        # Handle both rich (dict) and legacy (string) response formats
        results = []
        for item in sessions:
            if isinstance(item, dict):
                results.append(FoundationalModel.from_response(item, ctx=self._ctx))
            else:
                # Legacy: plain session ID string
                results.append(FoundationalModel(id=str(item), _ctx=self._ctx))

        return results

    def list_pending_jobs(
        self,
        name_prefix: str = "",
    ) -> List[FoundationalModel]:
        """
        List sessions that haven't finished yet — queued or actively training.

        Excludes sessions whose jobs are all done/failed/cancelled. Use the
        returned FoundationalModel.id (session_id) to identify a job for a
        subsequent cancel call.

        Args:
            name_prefix: Optional search term to filter by name or session ID

        Returns:
            List of FoundationalModel objects with status "ready" or "running"

        Example:
            for fm in featrix.list_pending_jobs():
                print(f"{fm.id}: {fm.name} ({fm.status})")
        """
        all_sessions = self.list_sessions(name_prefix=name_prefix)
        return [fm for fm in all_sessions if fm.status in ("ready", "running")]

    def get_job_predictabar(self, job_id: str) -> Dict[str, Any]:
        """
        Get live progress + ETA for a job, in the same shape the PredictaBar
        widget renders (see GET /predictabar/status/<job_id> on sphere-api).

        The job must have reported at least one PredictaBar event already
        (training/upload/processing jobs do this automatically); a job_id
        that's never reported anything raises HTTPError(404).

        Args:
            job_id: The job/session id to look up.

        Returns:
            Dict with at least: job_id, status, job_type, subsection,
            percent (0-100 or None), started_at (ISO 8601), elapsed_seconds,
            elapsed_in_stage_seconds, eta_seconds, eta_confidence, source,
            stage_plan (list, empty if this job_type has no declared stage
            taxonomy — render a flat bar in that case), metadata,
            subsection_history.

        Example:
            status = featrix.get_job_predictabar(job_id)
            print(f"{status['status']}: {status['percent']}% (ETA {status['eta_seconds']}s)")
        """
        return self._get_json(f"/predictabar/status/{job_id}")

    def list_foundational_models(
        self,
        name_prefix: str = "",
    ) -> List[FoundationalModel]:
        """
        List successfully trained foundational models (embedding spaces only).

        Unlike list_sessions() which returns all sessions (ES + SP), this
        returns only embedding space sessions that completed training.

        Args:
            name_prefix: Optional filter — matches anywhere in session name/ID

        Returns:
            List of FoundationalModel objects for completed embedding spaces
        """
        params = {}
        if name_prefix:
            params['name_prefix'] = name_prefix

        response = self._get_json("/compute/foundational-models", params=params)
        items = response.get('models', [])

        return [
            FoundationalModel.from_response(item, ctx=self._ctx)
            for item in items
        ]

    def health_check(self) -> Dict[str, Any]:
        """
        Check if the API server is healthy.

        Returns:
            Health status dictionary
        """
        return self._get_json("/health")

    def whoami(self) -> Dict[str, Any]:
        """
        Return identity info for the authenticated API key.

        Returns:
            Dictionary with user_id, org_id, org_name, org_slug,
            api_key_id, scopes, authenticated_at, and queue_limit (this
            org's effective max concurrently-pending jobs -- an admin-set
            override if the org has one, else the service-wide default).
        """
        return self._get_json("/auth/whoami")

    def _dataframe_to_file(self, df: 'pd.DataFrame') -> tuple:
        """Convert DataFrame to file content and filename."""
        # Try parquet first (more efficient)
        try:
            import pyarrow
            buffer = io.BytesIO()
            df.to_parquet(buffer, index=False)
            return buffer.getvalue(), "data.parquet"
        except ImportError:
            pass

        # Fall back to CSV
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        content = csv_buffer.getvalue().encode('utf-8')

        # Compress if large
        if len(content) > 100_000:
            compressed = gzip.compress(content)
            if len(compressed) < len(content):
                return compressed, "data.csv.gz"

        return content, "data.csv"

    def _peek_column_count(self, file_path: str) -> Optional[int]:
        """Best-effort column count from just the file header — no full read.

        Returns None (not 0) when the format can't be cheaply inspected client-side
        (e.g. JSON/JSONL) — the caller must treat None as "unknown" and skip the
        pre-upload check rather than block on it; the server-side ingest check is
        the authoritative one for those formats.
        """
        name = Path(file_path).name.lower()
        try:
            if name.endswith('.parquet'):
                import pyarrow.parquet as pq
                return len(pq.ParquetFile(file_path).schema.names)

            if name.endswith('.csv') or name.endswith('.csv.gz'):
                import csv
                opener = gzip.open if name.endswith('.gz') else open
                with opener(file_path, 'rt', newline='', encoding='utf-8', errors='replace') as f:
                    header = next(csv.reader(f), None)
                return len(header) if header else None
        except Exception as e:
            logger.debug(f"Could not peek column count for {file_path}: {e}")
        return None

    def _read_file(self, file_path: str) -> tuple:
        """Read file content and return with filename."""
        path = Path(file_path)
        filename = path.name

        with open(path, 'rb') as f:
            content = f.read()

        # Compress if large and not already compressed
        if len(content) > 100_000 and not filename.endswith('.gz'):
            compressed = gzip.compress(content)
            if len(compressed) < len(content):
                return compressed, filename + '.gz'

        return content, filename

    def __repr__(self) -> str:
        cluster_str = f", cluster='{self._compute_cluster}'" if self._compute_cluster else ""
        return f"FeatrixSphere(url='{self._base_url}'{cluster_str})"
