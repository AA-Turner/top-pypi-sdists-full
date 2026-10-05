#  -*- coding: utf-8 -*-
#
#  Copyright (c) 2023-2026 Featrix, Inc, All Rights Reserved
#
#  Proprietary and Confidential.  Unauthorized use, copying or dissemination
#  of these materials is strictly prohibited.
#

"""
FoundationalModel class for FeatrixSphere API.

Represents a trained embedding space (foundational model).
"""

import gc
import gzip
import io
import sys
import time
import logging
import requests
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List, Union, TYPE_CHECKING

if TYPE_CHECKING:
    from .http_client import ClientContext
    import pandas as pd
    import numpy as np

from .predictor import Predictor
from .prediction_result import PredictionResult
from .vector_database import VectorDatabase
from .vector_view import VectorView
from .reference_record import ReferenceRecord
from .exceptions import TrainingStatusUnavailableError, SessionNotFoundError, FeatrixPredictionError
from .poll_utils import adaptive_poll_interval, job_awaiting_start, server_liveness_time

logger = logging.getLogger(__name__)

# A single poll reading status='failed' can be a transient/racy read (e.g. the
# jobs dict momentarily missing the matched job entry while the session-level
# status field still says 'failed' from a stale write). Require this many
# consecutive confirming reads before treating it as a real terminal failure —
# a non-failed read in between resets the counter. Prevents false "Training
# failed" raises on jobs that are actually still running server-side.
_FAILED_STATUS_CONFIRM_READS = 3

# A single 404 from /compute/session/{id} can also be a transient/racy read:
# there is a real gap on the server between a job leaving Supabase's 'pending'
# queue (claimed by a node) and that node registering the session locally —
# during that gap the session is in neither the pending-queue fallback nor
# any node's local session store, so the router legitimately has nothing to
# return but 404, even though the job is healthy and about to start reporting
# progress. Require this many consecutive 404s before treating "not found" as
# confirmed-permanent — any non-404 read in between (queued/running/done/even
# a different error) resets the counter. Keeps the 2026-07 zombie-polling fix
# (see docs/internal/plans/2026-07-job-system-reliability-consolidated-plan.md)
# intact — retries are still bounded, just not zero — while no longer treating
# a brand-new job's very first unlucky poll as a permanent, unretriable loss.
_NOT_FOUND_CONFIRM_READS = 5

# How long to keep polling through *consecutive* failures (connection errors,
# 5xx, transient 401s from a Supabase/auth hiccup, etc.) before giving up on
# an otherwise-healthy-looking job. A count-based budget doesn't track wall
# clock time well here since a single failed poll can itself burn up to 120s
# retrying inside _make_request — a fixed count of "attempts" translates to
# wildly different real time depending on the failure mode. Sized like
# _NODE_UPGRADE_MAX_WAIT_SECONDS / _ORG_QUEUE_MAX_WAIT_SECONDS in
# http_client.py: long enough to ride out a sphere-api restart or a Supabase
# outage without abandoning a job that can run for many hours (observed
# 2026-09-10: a ~30-90 min sphere-api/Supabase outage 401'd every in-flight
# poll fleet-wide and the old 30-consecutive-failures budget gave up on
# several 8-12h trainings that were still running server-side). See the
# matching constant/comment in predictor.py.
_POLL_FAILURE_MAX_SECONDS = 2 * 60 * 60

# Queue priority a caller can ask for on any training job (foundational model
# or predictor). sphere-api's backing_db.resolve_priority_tier owns what each
# tier means for dispatch; any account may request any tier, including
# "urgent". The server ignores an unrecognized value (falls back to the org's
# default tier), so the client rejects it loudly instead. "qa" is the lowest
# tier (QA runs; yields to all other work) and the only one the shared Mac
# nodes accept.
JOB_PRIORITIES = ("urgent", "regular", "low", "qa")
PRIORITY_HEADER = "X-Featrix-Priority"


def _validate_priority(priority: Optional[str]) -> Optional[str]:
    if priority is not None and priority not in JOB_PRIORITIES:
        raise ValueError(f"priority must be one of {JOB_PRIORITIES}, got {priority!r}")
    return priority


def _parse_datetime(value) -> Optional[datetime]:
    """Parse a datetime from ISO string or return as-is if already datetime."""
    if value is None:
        return None
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        try:
            # Handle ISO format with or without timezone
            return datetime.fromisoformat(value.replace('Z', '+00:00'))
        except (ValueError, AttributeError):
            return None
    return None


# ── Client-side intent validation ────────────────────────────────────────────
# Vocabularies copied here so the SDK package stays standalone. Keep these in
# sync with ``src/lib/featrix/neural/user_intent.{BINARY,MULTICLASS,REGRESSION}_OBJECTIVES``.
_BINARY_INTENT_VOCAB = frozenset({
    "balanced",
    "only_alert_when_confident",
    "catch_everything",
    "catch_everything_aggressive",
    "minimize_cost",
    "rank",
    "predict_probabilities",
})

_MULTICLASS_INTENT_VOCAB = frozenset({
    "balanced",
    "accuracy",
    "rank_classes",
    "top_k_hit",
})

_REGRESSION_INTENT_VOCAB = frozenset({
    "balanced",
    "minimize_typical_error",
    "minimize_worst_case",
    "minimize_relative_error",
})


def _validate_binary_intent(
    *,
    intent: str,
    cost_false_positive: Optional[float],
    cost_false_negative: Optional[float],
) -> None:
    """Client-side early-fail. Server revalidates.

    Rules (same as ``user_intent.from_binary_kwargs``):
      * intent must be in the binary vocabulary.
      * ``intent="minimize_cost"`` requires both costs.
      * A non-cost intent combined with ``cost_false_*`` kwargs is incoherent —
        the customer must pick one.
    """
    if intent not in _BINARY_INTENT_VOCAB:
        raise ValueError(
            f"Unknown intent={intent!r}. "
            f"Must be one of: {sorted(_BINARY_INTENT_VOCAB)}."
        )
    if intent == "minimize_cost":
        if cost_false_positive is None or cost_false_negative is None:
            raise ValueError(
                "intent='minimize_cost' requires BOTH cost_false_positive and "
                "cost_false_negative."
            )
    else:
        if cost_false_positive is not None or cost_false_negative is not None:
            raise ValueError(
                f"intent={intent!r} is incompatible with cost_false_positive / "
                f"cost_false_negative. Either drop the costs, or use "
                f"intent='minimize_cost'."
            )


def _validate_multiclass_intent(*, intent: str, k: Optional[int]) -> None:
    """Client-side early-fail for multiclass intent + k= kwarg."""
    if intent not in _MULTICLASS_INTENT_VOCAB:
        raise ValueError(
            f"Unknown intent={intent!r}. "
            f"Must be one of: {sorted(_MULTICLASS_INTENT_VOCAB)}."
        )
    if intent == "top_k_hit":
        if k is None:
            raise ValueError(
                "intent='top_k_hit' requires k= (positive integer, e.g. k=3)."
            )
        if not isinstance(k, int) or k <= 0:
            raise ValueError(
                f"k= must be a positive integer, got {k!r}."
            )
    else:
        if k is not None:
            raise ValueError(
                f"intent={intent!r} is incompatible with k=. The k= kwarg "
                f"only applies to intent='top_k_hit'."
            )


def _validate_regression_intent(*, intent: str) -> None:
    """Client-side early-fail for regression intent (Tier-1 vocab is balanced only)."""
    if intent not in _REGRESSION_INTENT_VOCAB:
        raise ValueError(
            f"Unknown intent={intent!r}. "
            f"Must be one of: {sorted(_REGRESSION_INTENT_VOCAB)}."
        )


@dataclass
class FoundationalModel:
    """
    Represents a foundational model (embedding space).

    Attributes:
        id: Session ID / FM ID
        name: Model name
        status: Training status ("training", "done", "error")
        dimensions: Embedding dimensions (d_model)
        epochs: Training epochs completed
        created_at: Creation timestamp

    Usage:
        # Create from client
        fm = featrix.create_foundational_model(
            name="customer_embeddings",
            data_file="customers.csv"
        )

        # Wait for training
        fm.wait_for_training()

        # Create classifier
        predictor = fm.create_binary_classifier(
            name="churn_predictor",
            target_column="churned"
        )

        # Create vector database
        vdb = fm.create_vector_database(
            name="customer_search",
            records=customer_records
        )

        # Encode records
        vectors = fm.encode([{"age": 35}, {"age": 42}])
    """

    id: str
    name: Optional[str] = None
    status: Optional[str] = None
    # Per-stage status, additive alongside `status` (which stays the pooled
    # "is the whole pipeline done" view and can legitimately flip back to
    # "running" when an SP starts training on top of a finished ES). Use
    # these when you need to know ES readiness independent of SP progress.
    # None means no job of that type exists yet for this session.
    es_status: Optional[str] = None
    sp_status: Optional[str] = None
    dimensions: Optional[int] = None
    epochs: Optional[int] = None
    final_loss: Optional[float] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    session_type: Optional[str] = None
    compute_cluster: Optional[str] = None
    error_message: Optional[str] = None
    training_progress: Optional[Dict[str, Any]] = None
    user_metadata: Optional[Dict[str, Any]] = None
    deletion_protection: bool = False
    jobs: Optional[Dict[str, Any]] = field(default_factory=dict, repr=False)

    # Internal
    _ctx: Optional['ClientContext'] = field(default=None, repr=False)

    @classmethod
    def from_response(
        cls,
        response: Dict[str, Any],
        ctx: Optional['ClientContext'] = None
    ) -> 'FoundationalModel':
        """Create FoundationalModel from API response."""
        session_id = response.get('session_id', '')

        return cls(
            id=session_id,
            name=response.get('name') or response.get('label'),
            status=response.get('status'),
            es_status=response.get('es_status'),
            sp_status=response.get('sp_status'),
            dimensions=response.get('d_model') or response.get('dimensions'),
            epochs=response.get('epochs') or response.get('final_epoch'),
            final_loss=response.get('final_loss'),
            created_at=_parse_datetime(response.get('created_at')),
            session_type=response.get('session_type'),
            compute_cluster=response.get('compute_cluster'),
            user_metadata=response.get('user_metadata'),
            deletion_protection=bool(response.get('deletion_protection', False)),
            _ctx=ctx,
        )

    @classmethod
    def from_session_id(
        cls,
        session_id: str,
        ctx: 'ClientContext'
    ) -> 'FoundationalModel':
        """Load FoundationalModel from session ID."""
        # Get session info - response has {"session": {...}, "jobs": {...}}
        response_data = ctx.get_json(f"/compute/session/{session_id}")
        session = response_data.get('session', response_data)

        fm = cls(
            id=session_id,
            name=session.get('name'),
            status=session.get('status'),
            created_at=_parse_datetime(session.get('created_at')),
            session_type=session.get('session_type'),
            compute_cluster=session.get('compute_cluster'),
            _ctx=ctx,
        )

        # Extract model info, training stats, jobs, error_message
        fm._update_from_session(response_data)

        return fm

    def create_binary_classifier(
        self,
        target_column: str,
        name: Optional[str] = None,
        labels_file: Optional[str] = None,
        labels_df: Optional['pd.DataFrame'] = None,
        epochs: int = 0,
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
        keep_duplicates: Optional[bool] = None,
        **kwargs
    ) -> Predictor:
        """
        Create a binary classifier on this foundational model.

        group_column: Optional column for group-aware (leave-one-group-out)
            train/val splitting. When set, whole groups (rows sharing this
            column's value) go entirely to train OR val — never straddling — so
            correlated/clustered rows can't leak across the split. The column is
            carried for splitting only, never used as a feature. Use for grouped
            data (repeated measures, multiple rows per entity/dataset). None =
            ordinary stratified split.

        For target columns with exactly 2 classes. Supports cost-sensitive
        optimization for asymmetric error costs (e.g., fraud detection where
        missing fraud is much worse than a false alarm).

        Args:
            target_column: Column name to predict (must have exactly 2 unique values)
            name: Predictor name (optional)
            labels_file: Path to CSV with labels (optional - uses existing data if not provided)
            labels_df: DataFrame with labels (optional - alternative to labels_file)
            epochs: Training epochs (0 = automatic based on dataset complexity)
            rare_label_value: Which class is the minority/positive class for metrics
            class_imbalance: Expected real-world class distribution, e.g.
                {"approved": 0.97, "rejected": 0.03}. Use when training data
                is resampled but production distribution differs.
            cost_false_positive: Cost of a false positive (e.g., 100 = $100 per false alarm).
                Used for Bayes-optimal threshold selection. Implies intent="minimize_cost"
                when intent is not explicitly provided.
            cost_false_negative: Cost of a false negative (e.g., 5000 = $5000 per missed case).
                Used for Bayes-optimal threshold selection.
            intent: Plain-language objective. One of:
                "balanced" (default), "only_alert_when_confident" (high precision),
                "catch_everything" (catch ≥85% of positives), "catch_everything_aggressive"
                (catch ≥95% of positives — pick this on heavily skewed data or when
                missing positives is much worse than false alarms),
                "minimize_cost" (requires cost_false_positive + cost_false_negative),
                "rank" (AUC only, no threshold), or "predict_probabilities" (calibrated
                probabilities, fixed 0.5 threshold). When None, resolves from cost_*
                kwargs or defaults to "balanced".
            auto_collapse_synonyms: Auto-detect and merge near-duplicate class labels
                using BERT embedding similarity (default: True via config). Set False to disable.
            synonym_collapse_threshold: Cosine similarity threshold for synonym detection
                (default: 0.90 via config). Pairs above this are merged.
            label_mapping: Explicit old→new class name mapping, e.g.
                {"Unsafe & Dangerous": "Unsafe and Dangerous"}. Overrides auto-detection.
            keep_duplicates: When the uploaded data had exact duplicate rows, train
                and score on the true row distribution (each distinct row counted as
                many times as it appeared). Default None = server default (on). Set
                False to train on distinct rows only — e.g. when the duplicates are an
                export artifact rather than real repeated observations.
            webhooks: Webhook URLs for training events
            priority: Queue priority for this job — "urgent", "regular", or
                "low" (default: your organization's tier). "urgent" jumps
                ahead of lower-tier work when the fleet is busy. Accepted by
                every create_* predictor method.
            **kwargs: Additional training parameters

        Returns:
            Predictor object (training started). Call predictor.wait_for_training() to block.

        Example:
            # Basic binary classifier
            predictor = fm.create_binary_classifier(
                target_column="churned",
                rare_label_value="yes"
            )
            predictor.wait_for_training()

            # Cost-sensitive fraud detection
            predictor = fm.create_binary_classifier(
                target_column="is_fraud",
                rare_label_value="fraud",
                cost_false_positive=100,
                cost_false_negative=5000
            )
        """
        if cost_false_positive is not None:
            kwargs['cost_false_positive'] = cost_false_positive
        if cost_false_negative is not None:
            kwargs['cost_false_negative'] = cost_false_negative
        if intent is not None:
            _validate_binary_intent(
                intent=intent,
                cost_false_positive=cost_false_positive,
                cost_false_negative=cost_false_negative,
            )
            kwargs['intent'] = intent
        if auto_collapse_synonyms is not None:
            kwargs['auto_collapse_synonyms'] = auto_collapse_synonyms
        if synonym_collapse_threshold is not None:
            kwargs['synonym_collapse_threshold'] = synonym_collapse_threshold
        if label_mapping is not None:
            kwargs['label_mapping'] = label_mapping
        if group_column is not None:
            kwargs['group_column'] = group_column

        return self._create_predictor(
            target_column=target_column,
            target_type="set",
            name=name,
            labels_file=labels_file,
            labels_df=labels_df,
            epochs=epochs,
            rare_label_value=rare_label_value,
            class_imbalance=class_imbalance,
            webhooks=webhooks,
            keep_duplicates=keep_duplicates,
            **kwargs
        )

    def create_multi_classifier(
        self,
        target_column: str,
        name: Optional[str] = None,
        labels_file: Optional[str] = None,
        labels_df: Optional['pd.DataFrame'] = None,
        epochs: int = 0,
        class_imbalance: Optional[Dict[str, float]] = None,
        intent: Optional[str] = None,
        k: Optional[int] = None,
        auto_collapse_synonyms: Optional[bool] = None,
        synonym_collapse_threshold: Optional[float] = None,
        label_mapping: Optional[Dict[str, str]] = None,
        webhooks: Optional[Dict[str, str]] = None,
        keep_duplicates: Optional[bool] = None,
        **kwargs
    ) -> Predictor:
        """
        Create a multiclass classifier on this foundational model.

        For target columns with 3 or more classes. Architecture is auto-sized
        based on dataset complexity.

        Args:
            target_column: Column name to predict (3+ unique values)
            name: Predictor name (optional)
            labels_file: Path to CSV with labels (optional - uses existing data if not provided)
            labels_df: DataFrame with labels (optional - alternative to labels_file)
            epochs: Training epochs (0 = automatic based on dataset complexity)
            class_imbalance: Expected real-world class distribution, e.g.
                {"cat": 0.7, "dog": 0.2, "bird": 0.1}. Use when training data
                is resampled but production distribution differs.
            intent: Plain-language objective. One of:
                "balanced" (default, macro-F1 across classes),
                "accuracy" (plain accuracy — good for class-balanced data),
                "rank_classes" (per-class ranking, no argmax — call
                predict() and read result.probabilities instead of
                result.prediction; the model declines to pick a single
                class and returns the per-class scores for you to rank),
                "top_k_hit" (correct class in top-K — requires k=).
            k: Required when intent="top_k_hit". Number of top predictions to
                count as a hit (e.g. k=3).
            auto_collapse_synonyms: Auto-detect and merge near-duplicate class labels
                using BERT embedding similarity (default: True via config). Set False to disable.
            synonym_collapse_threshold: Cosine similarity threshold for synonym detection
                (default: 0.90 via config). Pairs above this are merged.
            label_mapping: Explicit old→new class name mapping, e.g.
                {"Unsafe & Dangerous": "Unsafe and Dangerous"}. Overrides auto-detection.
            keep_duplicates: When the uploaded data had exact duplicate rows, train
                and score on the true row distribution (each distinct row counted as
                many times as it appeared). Default None = server default (on). Set
                False to train on distinct rows only — e.g. when the duplicates are an
                export artifact rather than real repeated observations.
            webhooks: Webhook URLs for training events
            **kwargs: Additional training parameters

        Returns:
            Predictor object (training started). Call predictor.wait_for_training() to block.

        Example:
            predictor = fm.create_multi_classifier(
                target_column="product_category",
                intent="top_k_hit",
                k=3,
            )
            predictor.wait_for_training()
        """
        if intent is not None:
            _validate_multiclass_intent(intent=intent, k=k)
            kwargs['intent'] = intent
            if k is not None:
                kwargs['k'] = k
        if auto_collapse_synonyms is not None:
            kwargs['auto_collapse_synonyms'] = auto_collapse_synonyms
        if synonym_collapse_threshold is not None:
            kwargs['synonym_collapse_threshold'] = synonym_collapse_threshold
        if label_mapping is not None:
            kwargs['label_mapping'] = label_mapping

        return self._create_predictor(
            target_column=target_column,
            target_type="set",
            name=name,
            labels_file=labels_file,
            labels_df=labels_df,
            epochs=epochs,
            class_imbalance=class_imbalance,
            webhooks=webhooks,
            keep_duplicates=keep_duplicates,
            **kwargs
        )

    def create_multi_label_classifier(
        self,
        target_column: str,
        name: Optional[str] = None,
        labels_file: Optional[str] = None,
        labels_df: Optional['pd.DataFrame'] = None,
        epochs: int = 0,
        class_imbalance: Optional[Dict[str, float]] = None,
        webhooks: Optional[Dict[str, str]] = None,
        keep_duplicates: Optional[bool] = None,
        **kwargs
    ) -> Predictor:
        """
        Create a multi-label classifier on this foundational model.

        For target columns where each row can carry MULTIPLE labels at once
        (e.g. movie genres, product tags, document topics). Distinct from
        ``create_multi_classifier``, which picks exactly one of N classes
        per row.

        The target column may be supplied in any of these shapes — the
        server's column-type detector picks the right delimiter / parser:

        * Delimited string: ``"comedy,drama"`` / ``"a; b; c"`` / ``"x|y"``
        * JSON list string: ``'["comedy","drama"]'``
        * Python-repr list string: ``"['comedy', 'drama']"``
        * In-memory ``list`` / ``tuple`` / ``set`` / ``np.ndarray`` per cell

        Args:
            target_column: Column name to predict.
            name: Predictor name (optional).
            labels_file: Path to CSV with labels (optional — uses existing
                data if not provided).
            labels_df: DataFrame with labels (optional alternative to
                ``labels_file``).
            epochs: Training epochs (0 = automatic based on dataset
                complexity and label cardinality).
            class_imbalance: Per-label expected real-world prevalence, e.g.
                ``{"fraud": 0.02, "review": 0.15}``. Use when training data
                is resampled but production distribution differs.
            keep_duplicates: When the uploaded data had exact duplicate rows, train
                and score on the true row distribution (each distinct row counted as
                many times as it appeared). Default None = server default (on). Set
                False to train on distinct rows only — e.g. when the duplicates are an
                export artifact rather than real repeated observations.
            webhooks: Webhook URLs for training events.
            **kwargs: Additional training parameters passed through to the
                server. Notable knobs the server understands for this task
                type (defaults applied per-deployment, not per-request):
                ``sp_multilabel_threshold`` (sigmoid cutoff, default 0.5),
                ``sp_multilabel_loss_type`` ("bce" or "focal_bce"),
                ``sp_multilabel_use_pos_weight`` (per-label weighting from
                label frequency).

        Returns:
            Predictor object (training started). Call
            ``predictor.wait_for_training()`` to block.

        Notes:
            ``intent=`` and ``cost_false_positive/negative=`` are not
            currently meaningful for multi-label and are silently ignored
            server-side. If you need cost-sensitive behavior, tune
            ``sp_multilabel_threshold`` instead.

        Example:
            predictor = fm.create_multi_label_classifier(
                target_column="genres",
            )
            predictor.wait_for_training()

            result = predictor.predict({"title": "...", "year": 1999})
            # result.probabilities is a {label: prob} dict;
            # result.prediction is the list of labels above the threshold.
        """
        return self._create_predictor(
            target_column=target_column,
            target_type="multi_label",
            name=name,
            labels_file=labels_file,
            labels_df=labels_df,
            epochs=epochs,
            class_imbalance=class_imbalance,
            webhooks=webhooks,
            keep_duplicates=keep_duplicates,
            **kwargs
        )

    def create_regressor(
        self,
        target_column: str,
        allow_null: bool = False,
        name: Optional[str] = None,
        labels_file: Optional[str] = None,
        labels_df: Optional['pd.DataFrame'] = None,
        epochs: int = 0,
        intent: Optional[str] = None,
        group_column: Optional[str] = None,
        webhooks: Optional[Dict[str, str]] = None,
        keep_duplicates: Optional[bool] = None,
        **kwargs
    ) -> Predictor:
        """
        Create a regressor predictor from this foundational model.

        group_column: Optional column for group-aware (leave-one-group-out)
            train/val splitting — whole groups go entirely to train OR val so
            correlated rows can't leak. Carried for splitting only, not a
            feature. None = ordinary random split.

        Args:
            target_column: Column name to predict
            allow_null: If True, return null when model uncertainty is too high
            name: Predictor name (optional)
            labels_file: Path to labels file (optional)
            labels_df: DataFrame with labels (optional)
            epochs: Training epochs (0 = auto)
            intent: Plain-language objective. One of:
                "balanced" (default — MSE loss, best-epoch by R²),
                "minimize_typical_error" (Huber loss, best-epoch by MAE — outliers
                exist but you care about the typical case),
                "minimize_worst_case" (tail-weighted MSE, best-epoch by RMSE —
                big misses are catastrophic, no tolerance for outliers),
                "minimize_relative_error" (log-target MSE, best-epoch by sMAPE —
                "off by 10%" matters more than "off by $10"; targets must be ≥0).
                When None, defaults to "balanced".
            keep_duplicates: When the uploaded data had exact duplicate rows, train
                and score on the true row distribution (each distinct row counted as
                many times as it appeared). Default None = server default (on). Set
                False to train on distinct rows only — e.g. when the duplicates are an
                export artifact rather than real repeated observations.
            webhooks: Webhook URLs for events
            **kwargs: Additional training parameters

        Returns:
            Predictor object (training started)
        """
        if intent is not None:
            _validate_regression_intent(intent=intent)
            kwargs['intent'] = intent
        # Wire value is "scalar". The server's train_predictor validator
        # accepts {set, scalar, multi_label, ordinal, ranking} (see
        # featrix.neural.single_predictor.targets.registry) — "numeric" is
        # rejected with 400.
        if group_column is not None:
            kwargs['group_column'] = group_column
        return self._create_predictor(
            target_column=target_column,
            target_type="scalar",
            name=name,
            labels_file=labels_file,
            labels_df=labels_df,
            epochs=epochs,
            webhooks=webhooks,
            allow_null=allow_null,
            keep_duplicates=keep_duplicates,
            **kwargs
        )

    def create_generative_string_model(
        self,
        target_column: str,
        name: Optional[str] = None,
        labels_file: Optional[str] = None,
        labels_df: Optional['pd.DataFrame'] = None,
        webhooks: Optional[Dict[str, str]] = None,
        **kwargs
    ) -> Predictor:
        """
        Create a generative-string predictor from this foundational model:
        generate the right value of ``target_column`` (e.g. a company
        description) from the row's other columns.

        Unlike every other predictor type, there's no gradient-trained head
        — "training" builds a nearest-neighbor index over row embeddings.
        predict() defaults to the fast path (the nearest training row's real
        value); pass ``generate=True`` to predict() to instead few-shot an
        LLM with the nearest training rows for a non-verbatim answer. See
        Predictor.predict()'s ``generate`` parameter.

        Args:
            target_column: Column name to generate
            name: Predictor name (optional)
            labels_file: Path to labels file (optional)
            labels_df: DataFrame with labels (optional)
            webhooks: Webhook URLs for events
            **kwargs: Additional training parameters

        Returns:
            Predictor object (index build started — much faster than a
            gradient-trained predictor, no epochs involved)

        Example:
            predictor = fm.create_generative_string_model(
                target_column="company_description",
            )
            result = predictor.predict({"industry": "logistics", "state": "CA"})
            print(result.predicted_class)  # nearest training row's description

            result = predictor.predict(
                {"industry": "logistics", "state": "CA"}, generate=True,
            )
            print(result.predicted_class)  # LLM-generated, not verbatim
        """
        return self._create_predictor(
            target_column=target_column,
            target_type="free_string",
            name=name,
            labels_file=labels_file,
            labels_df=labels_df,
            epochs=0,
            webhooks=webhooks,
            **kwargs
        )

    def create_ranking_predictor(
        self,
        target_column: Optional[str] = None,
        *,
        group_column: str,
        use_row_order: bool = False,
        name: Optional[str] = None,
        labels_file: Optional[str] = None,
        labels_df: Optional['pd.DataFrame'] = None,
        epochs: int = 0,
        webhooks: Optional[Dict[str, str]] = None,
        **kwargs
    ) -> Predictor:
        """Create a learning-to-rank predictor from this foundational model.

        Ranks candidate rows *within* a query group. Training data is many query
        sets stacked: each row carries a query id (``group_column``) and a
        relevance label; the model learns the order within each query, never
        across queries. At serve time you send a query set (the candidate rows
        for one query) and get them scored — sort by the score to rank.

        The relevance label comes from ONE of:
          * ``target_column`` — a continuous relevance/score column (higher =
            more relevant), or
          * ``use_row_order=True`` — the file's row order *within each group* is
            the ranking (top row = most relevant). The server synthesizes the
            relevance from row position; no relevance column needed.

        Args:
            target_column: The continuous relevance column. Omit when
                ``use_row_order=True``.
            group_column: The query-id column. Rows sharing a value are one query
                group. Required. Split is by group (a query never straddles
                train/val) and the ranking loss only compares rows in the same
                group.
            use_row_order: Use within-group file row order as the relevance label
                instead of a relevance column. Mutually exclusive with
                ``target_column``.
            name: Predictor name (optional).
            labels_file / labels_df: Optional separate labels source.
            epochs: Training epochs (0 = auto).
            webhooks: Webhook URLs for events.
            **kwargs: Additional training parameters.

        Returns:
            Predictor object (training started). Scored as mean per-group NDCG.

        Example:
            # relevance column
            r = fm.create_ranking_predictor(
                target_column="relevance", group_column="query_id")

            # or: the file is already ordered best-first within each query
            r = fm.create_ranking_predictor(
                group_column="query_id", use_row_order=True)
        """
        if not group_column:
            raise ValueError("create_ranking_predictor requires group_column (the query-id column).")
        if use_row_order and target_column:
            raise ValueError(
                "Pass either target_column (a relevance column) or use_row_order=True, not both."
            )
        if not use_row_order and not target_column:
            raise ValueError(
                "create_ranking_predictor needs a relevance signal: pass target_column "
                "(a relevance column) or use_row_order=True (rank by file order within group)."
            )
        # When ranking by row order there is no relevance column; the server
        # synthesizes the internal __featrix_row_input_is_rank__ label.
        effective_target = target_column or "__featrix_row_input_is_rank__"
        kwargs["group_column"] = group_column
        if use_row_order:
            kwargs["use_row_order"] = True
        return self._create_predictor(
            target_column=effective_target,
            target_type="ranking",
            name=name,
            labels_file=labels_file,
            labels_df=labels_df,
            epochs=epochs,
            webhooks=webhooks,
            **kwargs
        )

    def _wait_for_queued_predictor(
        self,
        session_id: str,
        target_column: str,
        max_wait_time: int = 3600,
        poll_interval: int = 10,
    ) -> str:
        """
        Poll a session whose predictor-training job was queued (all SP-capable
        nodes were busy at creation time) until it's dispatched and gets a
        predictor_id.

        A queued create response has no predictor_id yet — the server only
        mints one when a compute node actually picks the job up. Until then,
        the session may not exist on any node at all, so GET .../session/<id>
        legitimately 404s; that's expected while queued, not a failure.
        """
        start_time = time.time()
        last_progress_time = time.time()
        consecutive_errors = 0
        first_error_time: Optional[float] = None  # for REAL errors only, not expected 404s

        while True:
            stall_seconds = time.time() - last_progress_time
            if stall_seconds > max_wait_time:
                raise TimeoutError(
                    f"Predictor for session {session_id} (target_column={target_column}) "
                    f"stayed queued with no progress for {int(stall_seconds)}s. It may "
                    f"still be waiting on the server — check session {session_id}."
                )

            try:
                response_data = self._ctx.get_json(f"/compute/session/{session_id}")
                consecutive_errors = 0
                first_error_time = None
            except requests.HTTPError as e:
                if e.response is not None and e.response.status_code == 404:
                    # Not dispatched to any node yet — expected while queued.
                    time.sleep(adaptive_poll_interval(poll_interval, start_time))
                    continue
                consecutive_errors += 1
            except Exception:
                consecutive_errors += 1

            if consecutive_errors:
                if first_error_time is None:
                    first_error_time = time.time()
                error_streak_seconds = time.time() - first_error_time
                if error_streak_seconds >= _POLL_FAILURE_MAX_SECONDS:
                    elapsed = int(time.time() - start_time)
                    raise RuntimeError(
                        f"Predictor for session {session_id}: lost contact with server "
                        f"while waiting on a queued job after {consecutive_errors} "
                        f"consecutive poll failures over {elapsed}s."
                    )
                time.sleep(adaptive_poll_interval(poll_interval, start_time))
                continue

            jobs = list(response_data.get('jobs', {}).values())
            jobs += response_data.get('session', {}).get('job_plan', []) or []
            for job in jobs:
                if job.get('job_type') != 'train_single_predictor':
                    continue
                job_target = job.get('target_column') or job.get('job_spec', {}).get('target_column')
                if job_target != target_column:
                    continue
                predictor_id = job.get('predictor_id') or job.get('job_spec', {}).get('predictor_id')
                if predictor_id:
                    return predictor_id
                if job.get('status') in ('failed', 'error'):
                    raise RuntimeError(
                        f"Queued predictor training (session {session_id}) failed before "
                        f"dispatch: {job.get('error', 'Unknown error')}"
                    )
                # Job has landed but no predictor_id stamped yet — progress, keep polling.
                last_progress_time = time.time()

            del response_data
            time.sleep(adaptive_poll_interval(poll_interval, start_time))

    def _create_predictor(
        self,
        target_column: str,
        target_type: str,
        name: Optional[str] = None,
        labels_file: Optional[str] = None,
        labels_df: Optional['pd.DataFrame'] = None,
        epochs: int = 0,
        rare_label_value: Optional[str] = None,
        class_imbalance: Optional[Dict[str, float]] = None,
        webhooks: Optional[Dict[str, str]] = None,
        allow_null: bool = False,
        priority: Optional[str] = None,
        keep_duplicates: Optional[bool] = None,
        **kwargs
    ) -> Predictor:
        """Internal method to create predictor."""
        if not self._ctx:
            raise ValueError("FoundationalModel not connected to client")

        # If labels file/df provided, use train_on_foundational_model which
        # creates a NEW session. The proxy handles finding the FM on any node.
        if labels_file or labels_df is not None:
            return self._create_predictor_with_labels(
                target_column=target_column,
                target_type=target_type,
                name=name,
                labels_file=labels_file,
                labels_df=labels_df,
                epochs=epochs,
                rare_label_value=rare_label_value,
                class_imbalance=class_imbalance,
                webhooks=webhooks,
                allow_null=allow_null,
                priority=priority,
                keep_duplicates=keep_duplicates,
                **kwargs
            )

        # No labels file — train on the FM's existing data.
        # Uses the FM's session directly (data lives in its session dir).
        data = {
            "target_column": target_column,
            "target_column_type": target_type,
            "epochs": epochs,
        }
        if name:
            data["name"] = name
        if rare_label_value:
            data["rare_label_value"] = rare_label_value
        if class_imbalance:
            data["class_imbalance"] = class_imbalance
        if webhooks:
            data["webhooks"] = webhooks
        if allow_null:
            data["allow_null"] = True
        if _validate_priority(priority):
            data["priority"] = priority
        if keep_duplicates is not None:
            data["keep_duplicates"] = keep_duplicates
        data.update(kwargs)

        # Include project_id if set on client
        if self._ctx.current_project_id:
            data['project_id'] = self._ctx.current_project_id

        response = self._ctx.post_json(
            f"/compute/session/{self.id}/train_predictor",
            data=data
        )

        predictor_id = response.get('predictor_id', '')
        if not predictor_id:
            if response.get('queued'):
                predictor_id = self._wait_for_queued_predictor(
                    session_id=self.id,
                    target_column=target_column,
                )
            else:
                raise ValueError(
                    f"Server did not return a predictor_id for session {self.id}. "
                    f"The predictor may not have been created. Response: {response}"
                )

        return Predictor(
            id=predictor_id,
            session_id=self.id,
            target_column=target_column,
            target_type=target_type,
            name=name,
            status="training",
            _ctx=self._ctx,
            _foundational_model=self,
        )

    def _create_predictor_with_labels(
        self,
        target_column: str,
        target_type: str,
        name: Optional[str] = None,
        labels_file: Optional[str] = None,
        labels_df: Optional['pd.DataFrame'] = None,
        epochs: int = 0,
        rare_label_value: Optional[str] = None,
        class_imbalance: Optional[Dict[str, float]] = None,
        webhooks: Optional[Dict[str, str]] = None,
        allow_null: bool = False,
        priority: Optional[str] = None,
        keep_duplicates: Optional[bool] = None,
        **kwargs
    ) -> Predictor:
        """Create predictor with separate labels file.

        Uses /compute/train_on_foundational_model which creates a NEW session.
        The proxy handles finding the FM on any node and forwarding its session
        data to the target compute node.
        """
        import io
        import gzip
        import json

        # Prepare the labels data
        if labels_df is not None:
            csv_buffer = io.StringIO()
            labels_df.to_csv(csv_buffer, index=False)
            file_content = csv_buffer.getvalue().encode('utf-8')
            filename = "labels.csv"
        elif labels_file:
            with open(labels_file, 'rb') as f:
                file_content = f.read()
            filename = labels_file.split('/')[-1]
        else:
            raise ValueError("Either labels_file or labels_df must be provided")

        # Compress if large
        if len(file_content) > 100_000:
            compressed = gzip.compress(file_content)
            if len(compressed) < len(file_content):
                file_content = compressed
                filename = filename + '.gz'

        # Build form data for train_on_foundational_model endpoint
        form_data = {
            "foundation_model_id": self.id,
            "target_column": target_column,
            "target_column_type": target_type,
            "epochs": str(epochs),
        }
        if name:
            form_data["name"] = name
        if rare_label_value:
            form_data["rare_label_value"] = rare_label_value
        if class_imbalance:
            form_data["class_imbalance"] = json.dumps(class_imbalance)
        if webhooks:
            form_data["webhooks"] = json.dumps(webhooks)
        if allow_null:
            form_data["allow_null"] = "true"
        if _validate_priority(priority):
            form_data["priority"] = priority
        if keep_duplicates is not None:
            form_data["keep_duplicates"] = "true" if keep_duplicates else "false"
        # Pass through kwargs (session_name_prefix, user_metadata, etc.)
        for key, value in kwargs.items():
            if value is not None:
                if isinstance(value, (dict, list)):
                    form_data[key] = json.dumps(value)
                else:
                    form_data[key] = str(value)

        # Include project_id if set on client
        if self._ctx.current_project_id:
            form_data['project_id'] = self._ctx.current_project_id

        files = {"file": (filename, file_content)}

        response = self._ctx.post_multipart(
            "/compute/train_on_foundational_model",
            data=form_data,
            files=files
        )

        # The server creates a NEW session — use that session_id, not the FM's
        new_session_id = response.get('session_id', self.id)

        predictor_id = response.get('predictor_id', '')
        if not predictor_id:
            if response.get('queued'):
                predictor_id = self._wait_for_queued_predictor(
                    session_id=new_session_id,
                    target_column=target_column,
                )
            else:
                raise ValueError(
                    f"Server did not return a predictor_id for foundation model {self.id}. "
                    f"The predictor may not have been created. Response: {response}"
                )

        return Predictor(
            id=predictor_id,
            session_id=new_session_id,
            target_column=target_column,
            target_type=target_type,
            name=name,
            status="training",
            _ctx=self._ctx,
            _foundational_model=self,
        )

    def create_vector_database(
        self,
        name: str = "default",
        auto_populate: bool = True,
        records: Optional[Union[List[Dict[str, Any]], 'pd.DataFrame']] = None,
    ) -> VectorDatabase:
        """
        Create a named vector database from this foundational model.

        Uses cosine distance (embeddings live on a hypersphere).

        Args:
            name: Database name (default: "default")
            auto_populate: If True, populate with training data (default: True)
            records: Additional records to add after creation (optional)

        Returns:
            VectorDatabase object

        Example:
            # Auto-populated with training data
            vdb = fm.create_vector_database("customers")

            # Empty, fill manually
            vdb = fm.create_vector_database("vip_only", auto_populate=False)
            vdb.add_records(vip_records)

            # Search
            similar = vdb.similarity_search({"age": 35}, k=5)
        """
        response = self._ctx.post_json(
            f"/session/{self.id}/vector_databases",
            data={"name": name, "auto_populate": auto_populate},
        )

        vdb = VectorDatabase.from_api_response(
            data=response,
            session_id=self.id,
            ctx=self._ctx,
            foundational_model=self,
        )

        if records is not None:
            vdb.add_records(records)

        return vdb

    def get_vector_database(self, name: str = "default") -> VectorDatabase:
        """
        Get an existing named vector database.

        Args:
            name: Database name (default: "default")

        Returns:
            VectorDatabase object
        """
        response = self._ctx.get_json(
            f"/session/{self.id}/vector_databases/{name}"
        )
        return VectorDatabase.from_api_response(
            data=response,
            session_id=self.id,
            ctx=self._ctx,
            foundational_model=self,
        )

    def list_vector_databases(self) -> List[VectorDatabase]:
        """
        List all named vector databases for this foundational model.

        Returns:
            List of VectorDatabase objects
        """
        response = self._ctx.get_json(
            f"/session/{self.id}/vector_databases"
        )
        return [
            VectorDatabase.from_api_response(
                data=vdb_data,
                session_id=self.id,
                ctx=self._ctx,
                foundational_model=self,
            )
            for vdb_data in response.get("vector_databases", [])
        ]

    # ------------------------------------------------------------------
    # Vector Views
    # ------------------------------------------------------------------

    def create_vector_view(
        self,
        records: Union[List[Dict[str, Any]], 'pd.DataFrame'],
        target_column: str,
        name: Optional[str] = None,
    ) -> VectorView:
        """
        Create a vector view: encode records through this ES, run linear probe,
        and get an immediate SphereViewer URL.

        This is fast (seconds) — the ES is already trained, encoding is just inference.

        Args:
            records: Records to encode (list of dicts or DataFrame)
            target_column: Column to color by and run probe against
            name: View name (defaults to target_column)

        Returns:
            VectorView with viewer_url, linear_probe results, and metadata

        Example:
            view = fm.create_vector_view(
                records=df.to_dict('records'),
                target_column="credit_risk"
            )
            print(view.viewer_url)          # Open NOW in browser
            print(view.linear_probe_auc)    # Instant baseline
        """
        if hasattr(records, 'to_dict'):
            records = records.to_dict('records')

        payload = {
            "records": records,
            "target_column": target_column,
        }
        if name is not None:
            payload["name"] = name

        response = self._ctx.post_json(
            f"/session/{self.id}/vector_views",
            data=payload,
        )

        return VectorView.from_api_response(
            data=response,
            session_id=self.id,
            ctx=self._ctx,
            foundational_model=self,
        )

    def get_vector_view(self, name: str) -> VectorView:
        """
        Get an existing vector view by name.

        Args:
            name: View name

        Returns:
            VectorView object
        """
        response = self._ctx.get_json(
            f"/session/{self.id}/vector_views/{name}"
        )
        return VectorView.from_api_response(
            data=response,
            session_id=self.id,
            ctx=self._ctx,
            foundational_model=self,
        )

    def list_vector_views(self) -> List[VectorView]:
        """
        List all vector views for this foundational model.

        Returns:
            List of VectorView objects
        """
        response = self._ctx.get_json(
            f"/session/{self.id}/vector_views"
        )
        return [
            VectorView.from_api_response(
                data=vv_data,
                session_id=self.id,
                ctx=self._ctx,
                foundational_model=self,
            )
            for vv_data in response.get("vector_views", [])
        ]

    def ground_truth_stats(self) -> Dict[str, Any]:
        """Get ground truth feedback statistics for this foundational model.

        Returns:
            Dictionary with:
                - total_predictions: Total predictions made
                - total_corrections: Total ground truth labels submitted
                - corrections_since_last_training: Corrections since last SP training
                - last_trained_at: When the predictor was last trained
                - correction_rate: Fraction of predictions that have been corrected
                - ready_for_retraining: Whether enough corrections exist to retrain
        """
        if not self._ctx:
            raise ValueError("FoundationalModel not connected to client")

        return self._ctx.get_json(
            f"/compute/session/{self.id}/ground_truth_stats"
        )

    def create_reference_record(
        self,
        record: Dict[str, Any],
        name: Optional[str] = None
    ) -> ReferenceRecord:
        """
        Create a reference record from a specific record for similarity search.

        A reference record is a reference point in the embedding space that you can use
        to find similar records. Particularly useful when you only have a positive
        class but no negative class - just find more records like the positive example.

        Args:
            record: The record to create a reference from
            name: Optional name for the reference record

        Returns:
            ReferenceRecord object that can be used for similarity search

        Example:
            # Create a reference record from a high-value customer
            ref = fm.create_reference_record(
                record={"age": 35, "income": 100000, "plan": "premium"},
                name="high_value_customer"
            )

            # Find similar customers
            similar = ref.find_similar(k=10, vector_database=vdb)
        """
        if not self._ctx:
            raise ValueError("FoundationalModel not connected to client")

        return ReferenceRecord.from_record(
            record=record,
            session_id=self.id,
            name=name,
            ctx=self._ctx,
            foundational_model=self,
        )

    def wait_for_training(
        self,
        max_wait_time: int = 3600,
        poll_interval: int = 10,
        show_progress: bool = True
    ) -> 'FoundationalModel':
        """
        Wait for foundational model training to complete with tqdm progress bar.

        The timeout is a *stall detector*, not a wall-clock limit. Training
        can run for days as long as progress is being made (epochs advancing,
        status changing). The timer resets on every sign of progress and only
        fires when the job appears stuck.

        Args:
            max_wait_time: Maximum time in seconds to wait *without progress*
                before raising TimeoutError (default 3600 = 1 hour)
            poll_interval: Polling interval in seconds
            show_progress: Show progress bar (tqdm if available, fallback to simple)

        Returns:
            Self (updated with final status)

        Raises:
            TimeoutError: If no progress is detected for max_wait_time seconds
            RuntimeError: If training fails
        """
        if not self._ctx:
            raise ValueError("FoundationalModel not connected to client")

        if not show_progress:
            return self._wait_simple(max_wait_time, poll_interval, show_progress=False)

        # tqdm renders via \r to stderr and effectively goes silent under
        # non-TTY output (e.g. piped through tee). Fall back to _wait_simple
        # so each poll prints a status line that survives logging.
        is_tty = getattr(sys.stdout, 'isatty', lambda: False)() and getattr(sys.stderr, 'isatty', lambda: False)()
        if not is_tty:
            return self._wait_simple(max_wait_time, poll_interval, show_progress=True)

        try:
            from tqdm import tqdm
            return self._wait_with_tqdm(max_wait_time, poll_interval)
        except ImportError:
            return self._wait_simple(max_wait_time, poll_interval, show_progress=True)

    def _wait_with_tqdm(self, max_wait_time: int, poll_interval: int) -> 'FoundationalModel':
        """Wait for training with tqdm progress bar."""
        from tqdm import tqdm

        start_time = time.time()
        last_progress_time = time.time()
        last_gc_time = time.time()
        pbar = None
        last_total = None
        last_epoch = None
        last_job_status = None
        last_queue_position = None
        last_progress_fraction = None

        consecutive_errors = 0
        first_error_time: Optional[float] = None
        consecutive_failed_reads = 0
        consecutive_not_found = 0

        try:
            while True:
                # Stall detection: timeout only when no progress is made
                stall_seconds = time.time() - last_progress_time
                if stall_seconds > max_wait_time:
                    if pbar:
                        pbar.close()
                    elapsed = int(time.time() - start_time)
                    raise TimeoutError(
                        f"Training stalled: no progress for {int(stall_seconds)}s "
                        f"(total elapsed: {elapsed}s). The job may still be running "
                        f"on the server — check status with client.foundational_model('{self.id}')"
                    )

                # Get session status — tolerate transient failures
                try:
                    response_data = self._ctx.get_json(f"/compute/session/{self.id}")
                    consecutive_errors = 0
                    first_error_time = None
                    consecutive_not_found = 0
                except Exception as e:
                    # A 404 usually means the router fanned out to every compute
                    # node, production-ai, and the pending queue and found nothing
                    # — but there's a real gap right after a job leaves Supabase's
                    # 'pending' queue (claimed by a node) and before that node
                    # registers the session locally, where a poll legitimately
                    # gets a 404 for a session that is healthy and about to start
                    # reporting progress (confirmed live 2026-08-15 — california_
                    # housing and 3 other QA datasets lost their SP jobs entirely
                    # to a first-poll 404 raised with zero retry). Require several
                    # consecutive 404s (see _NOT_FOUND_CONFIRM_READS) before
                    # treating "not found" as confirmed-permanent — bounded, so
                    # this still can't reproduce the zombie-polling incident that
                    # motivated failing fast on 404 in the first place: one
                    # customer polled 7 permanently-absent sessions continuously
                    # for 5+ days (~18,000 requests). See
                    # docs/internal/plans/2026-07-job-system-reliability-consolidated-plan.md
                    # Part 1, "zombie client, no circuit breaker either side".
                    status_code = getattr(getattr(e, "response", None), "status_code", None)
                    if status_code == 404:
                        consecutive_not_found += 1
                        elapsed = int(time.time() - start_time)
                        if consecutive_not_found < _NOT_FOUND_CONFIRM_READS:
                            if pbar:
                                pbar.set_postfix_str(
                                    f"not found (unconfirmed {consecutive_not_found}/{_NOT_FOUND_CONFIRM_READS})"
                                )
                            else:
                                print(
                                    f"[{elapsed}s] Session not found "
                                    f"(unconfirmed {consecutive_not_found}/{_NOT_FOUND_CONFIRM_READS}) — re-checking..."
                                )
                            time.sleep(adaptive_poll_interval(poll_interval, start_time))
                            continue
                        if pbar:
                            pbar.close()
                        raise SessionNotFoundError(session_id=self.id)

                    consecutive_errors += 1
                    if first_error_time is None:
                        first_error_time = time.time()
                    error_streak_seconds = time.time() - first_error_time
                    elapsed = int(time.time() - start_time)
                    if pbar:
                        pbar.set_postfix_str(
                            f"poll error {consecutive_errors} consecutive, "
                            f"{int(error_streak_seconds)}/{_POLL_FAILURE_MAX_SECONDS}s"
                        )
                    else:
                        print(
                            f"[{elapsed}s] Poll error ({consecutive_errors} consecutive, "
                            f"{int(error_streak_seconds)}/{_POLL_FAILURE_MAX_SECONDS}s): {e}"
                        )
                    if error_streak_seconds >= _POLL_FAILURE_MAX_SECONDS:
                        if pbar:
                            pbar.close()
                        # We genuinely can't tell if training succeeded, failed, or is
                        # still running — NOT the same as a confirmed server-reported
                        # failure. Automation must not treat this as "failed" and relaunch.
                        raise TrainingStatusUnavailableError(
                            session_id=self.id,
                            message=(
                                f"Training: lost contact with server after "
                                f"{consecutive_errors} consecutive poll failures over "
                                f"{elapsed}s. Last error: {e}. The job may still be "
                                f"running server-side — check status independently "
                                f"before relaunching."
                            ),
                        )
                    time.sleep(adaptive_poll_interval(poll_interval, start_time))
                    continue

                # Extract only the scalar values we need, then free the response
                session_data = response_data.get('session', response_data)
                status = session_data.get('status', 'unknown')

                # Queued: job is in the dispatch queue, no compute node yet.
                # Don't open a tqdm bar; just print queue status and keep polling.
                if status == 'queued':
                    queue_position = session_data.get('queue_position')
                    queue_msg = session_data.get('message', 'Waiting for a compute node to become available...')
                    elapsed = int(time.time() - start_time)
                    pos_str = f" (position {queue_position})" if queue_position else ""
                    if queue_position != last_queue_position or last_job_status != 'queued':
                        print(f"[{elapsed}s] 📥 Queued{pos_str} — {queue_msg}")
                        last_progress_time = time.time()
                        last_queue_position = queue_position
                        last_job_status = 'queued'
                    self.status = 'queued'
                    del response_data, session_data
                    time.sleep(adaptive_poll_interval(poll_interval, start_time))
                    continue

                # Find ES training job and extract scalars
                current_epoch = None
                total_epochs = None
                progress_fraction = None
                job_status = status
                latest_fact = ''
                error_msg = None
                completion_data = None

                # A session can carry more than one train_es job entry when an
                # earlier attempt aborted (e.g. heartbeat_stale_pid_dead) and
                # session_chains retried it under a new job_id — the dict is
                # insertion-ordered, so the dead first attempt sorts before
                # the retry. Picking the first match locks the progress bar
                # onto the dead job's frozen epoch/progress forever (observed
                # 2026-09-01: bar stuck at 0.03/25 for a full 29-minute run
                # that actually completed at 25/25 under a different job_id).
                # Pick the most-recently-created matching job instead.
                candidate_job = None
                candidate_created_at = None
                for job_id, job in response_data.get('jobs', {}).items():
                    if job.get('job_type') not in ('train_embedding_space', 'train_es', 'training'):
                        continue
                    created_at = job.get('created_at') or ''
                    if candidate_job is None or created_at > candidate_created_at:
                        candidate_job = job
                        candidate_created_at = created_at

                if candidate_job is not None:
                    job = candidate_job
                    current_epoch = job.get('current_epoch') or job.get('epoch')
                    total_epochs = job.get('total_epochs') or job.get('epochs')
                    progress_fraction = job.get('progress')
                    job_status = job.get('status', status)
                    fun_facts = job.get('fun_facts', [])
                    if fun_facts:
                        latest_fact = fun_facts[-1].get('message', '') if isinstance(fun_facts[-1], dict) else str(fun_facts[-1])
                    if job_status in ('failed', 'error'):
                        error_msg = (
                            job.get('error')
                            or job.get('error_message')
                            or job.get('failure_reason')
                            or 'Unknown error'
                        )
                    # Node still sees the job working (poll_utils.server_liveness_time).
                    alive_at = server_liveness_time(job)
                    if alive_at is not None:
                        last_progress_time = max(last_progress_time, alive_at)

                    # The session_chain has claimed this job (it exists, with a
                    # job_id) but it hasn't actually started running yet — e.g.
                    # waiting on a compute node for a free GPU/worker slot between
                    # pipeline steps. current_epoch/progress_fraction are
                    # legitimately still None here, and job_status doesn't change
                    # while it waits, so nothing below would reset the stall timer —
                    # dispatch-wait time would silently count against the 3600s
                    # stall budget as if the job were hung. Confirmed live
                    # 2026-09-09: a train_es job was created 17:49:07 but didn't
                    # start until 18:27:15 (38 min) and was NOT actually stuck.
                    # Treat this the same as the pre-dispatch 'queued' branch
                    # above: report it, reset the timer, keep polling.
                    # job_awaiting_start also covers a job the node already
                    # started (started_at set, status 'running') but is holding
                    # for a GPU training slot (gpu_slot_wait_started_at).
                    if job_awaiting_start(job):
                        elapsed = int(time.time() - start_time)
                        if job_status != last_job_status:
                            print(f"[{elapsed}s] 📥 Dispatched, waiting for a free compute slot...")
                        last_progress_time = time.time()
                        last_job_status = job_status
                        self.status = job_status
                        del response_data, session_data
                        time.sleep(adaptive_poll_interval(poll_interval, start_time))
                        continue

                # The training job entry may not exist yet if the pipeline failed
                # in an earlier step (create_structured_data, pre_analysis_architecture,
                # ...) before train_es was ever dispatched — fall back to any failed
                # job's error so we don't report "Unknown error" when the server did.
                if error_msg is None and (job_status in ('failed', 'error') or status == 'failed'):
                    for job_id, job in response_data.get('jobs', {}).items():
                        if job.get('status') in ('failed', 'error'):
                            error_msg = (
                                job.get('error')
                                or job.get('error_message')
                                or job.get('failure_reason')
                            )
                            if error_msg:
                                break

                # Keep response_data only if training is done (for _update_from_session)
                if job_status == 'done' or status == 'done':
                    completion_data = response_data

                # Free the response dict immediately — don't hold across sleep()
                del response_data, session_data

                # A non-failed read means an earlier 'failed' reading (if any) was
                # transient/unconfirmed — reset the confirmation counter.
                is_failed_this_read = (job_status == 'failed' or status == 'failed')
                if not is_failed_this_read:
                    consecutive_failed_reads = 0

                # A caller cancelling their own job mid-wait shouldn't see
                # that reported as a training failure. CANCELLED is a
                # terminal status in job_manager (no legal transition back to
                # running), so unlike 'failed' this needs no re-poll
                # confirmation.
                is_cancelled_this_read = (job_status == 'cancelled' or status == 'cancelled')

                # Reset stall timer on any sign of progress (epoch tick, status change,
                # or smooth fraction advancing — the latter ticks per-batch on the server)
                fraction_advanced = (
                    isinstance(progress_fraction, (int, float))
                    and (last_progress_fraction is None or progress_fraction > last_progress_fraction + 1e-6)
                )
                if current_epoch != last_epoch or job_status != last_job_status or fraction_advanced:
                    last_progress_time = time.time()
                    last_epoch = current_epoch
                    last_job_status = job_status
                    if isinstance(progress_fraction, (int, float)):
                        last_progress_fraction = progress_fraction

                # Initialize or update progress bar
                if current_epoch and total_epochs:
                    if pbar is None or last_total != total_epochs:
                        if pbar is not None:
                            pbar.close()
                        pbar = tqdm(
                            total=total_epochs,
                            desc=f"Training {self.name or self.id[:12]}",
                            unit="epoch",
                            dynamic_ncols=True,
                            bar_format='{desc}: {percentage:6.2f}%|{bar}| {n:.2f}/{total_fmt} epochs [{elapsed}<{remaining}]{postfix}'
                        )
                        last_total = total_epochs

                    # Prefer the smooth 0..1 progress fraction the server writes per-batch;
                    # falls back to integer epoch when the field is missing (older servers).
                    if isinstance(progress_fraction, (int, float)) and 0.0 <= progress_fraction <= 1.0:
                        target_n = float(progress_fraction) * total_epochs
                    else:
                        target_n = float(current_epoch)
                    if target_n > pbar.n:
                        pbar.update(target_n - pbar.n)
                        pbar.set_postfix_str(latest_fact or job_status)
                    elif target_n >= total_epochs and job_status != 'done':
                        # All epochs are in, but the job/session hasn't
                        # reported terminal yet -- baseline fitting, threshold
                        # calibration, and model-card generation all run
                        # after the last epoch tick. Without this the bar
                        # just sits frozen at 100% looking finished while
                        # that work is still going.
                        pbar.set_postfix_str(f"epochs done, finalizing ({job_status})")

                # Check completion
                if completion_data is not None:
                    if pbar:
                        pbar.n = pbar.total
                        pbar.refresh()
                        pbar.close()

                    self._update_from_session(completion_data)
                    # Set AFTER _update_from_session, not before: the session-level
                    # status field it reads can still say "running" for a beat after
                    # the ES job itself reports done (aggregate status lags the
                    # per-job status), which would otherwise silently clobber this
                    # back to "running" right as we return — see the matching fix
                    # in _wait_simple and TS's waitForTraining.
                    self.status = 'done'
                    del completion_data
                    print(f"\n✅ Training complete!")
                    if self.dimensions:
                        print(f"   Dimensions: {self.dimensions}")
                    if self.epochs:
                        print(f"   Epochs: {self.epochs}")
                    return self

                elif is_cancelled_this_read:
                    if pbar:
                        pbar.close()
                    self.status = 'cancelled'
                    print(f"\n🚫 Training cancelled")
                    return self

                elif is_failed_this_read:
                    consecutive_failed_reads += 1
                    if consecutive_failed_reads < _FAILED_STATUS_CONFIRM_READS:
                        # Don't trust a single 'failed' read — the jobs dict can
                        # transiently miss the matched job entry while the job keeps
                        # training server-side. Re-poll to confirm before raising.
                        if pbar:
                            pbar.set_postfix_str(
                                f"unconfirmed failure ({consecutive_failed_reads}/{_FAILED_STATUS_CONFIRM_READS})"
                            )
                        else:
                            elapsed = int(time.time() - start_time)
                            print(
                                f"[{elapsed}s] Training: status read as 'failed' "
                                f"(unconfirmed {consecutive_failed_reads}/{_FAILED_STATUS_CONFIRM_READS}) — re-checking..."
                            )
                        time.sleep(adaptive_poll_interval(poll_interval, start_time))
                        continue

                    if pbar:
                        pbar.close()
                    self.status = 'error'
                    raise RuntimeError(f"Training failed: {error_msg or 'Unknown error (server did not report a reason)'}")

                # Periodic gc to combat pymalloc arena fragmentation
                now = time.time()
                if now - last_gc_time > 60:
                    gc.collect()
                    last_gc_time = now

                time.sleep(adaptive_poll_interval(poll_interval, start_time))

        except KeyboardInterrupt:
            if pbar:
                pbar.close()
            print("\n⚠️  Training interrupted by user")
            raise

    def _wait_simple(self, max_wait_time: int, poll_interval: int, show_progress: bool) -> 'FoundationalModel':
        """Simple progress display without external dependencies."""
        start_time = time.time()
        last_progress_time = time.time()
        last_gc_time = time.time()
        last_epoch = None
        last_status = None
        last_fact = None
        last_queue_position = None
        last_progress_fraction = None
        last_printed_fraction = None
        epochs_done_announced = False
        consecutive_errors = 0
        first_error_time: Optional[float] = None
        consecutive_failed_reads = 0
        consecutive_not_found = 0

        while True:
            # Stall detection: timeout only when no progress is made
            stall_seconds = time.time() - last_progress_time
            if stall_seconds > max_wait_time:
                elapsed = int(time.time() - start_time)
                raise TimeoutError(
                    f"Training stalled: no progress for {int(stall_seconds)}s "
                    f"(total elapsed: {elapsed}s). The job may still be running "
                    f"on the server — check status with client.foundational_model('{self.id}')"
                )

            # Get session status — tolerate transient failures
            try:
                response_data = self._ctx.get_json(f"/compute/session/{self.id}")
                consecutive_errors = 0
                first_error_time = None
                consecutive_not_found = 0
            except Exception as e:
                # A 404 can be a transient registration-gap race, not just a
                # confirmed-gone session — see the matching comment and
                # _NOT_FOUND_CONFIRM_READS in _wait_with_tqdm for the full
                # rationale. Require several consecutive 404s before treating
                # "not found" as permanent.
                status_code = getattr(getattr(e, "response", None), "status_code", None)
                if status_code == 404:
                    consecutive_not_found += 1
                    elapsed = int(time.time() - start_time)
                    if consecutive_not_found < _NOT_FOUND_CONFIRM_READS:
                        if show_progress:
                            print(
                                f"[{elapsed}s] Session not found "
                                f"(unconfirmed {consecutive_not_found}/{_NOT_FOUND_CONFIRM_READS}) — re-checking..."
                            )
                        time.sleep(adaptive_poll_interval(poll_interval, start_time))
                        continue
                    raise SessionNotFoundError(session_id=self.id)

                consecutive_errors += 1
                if first_error_time is None:
                    first_error_time = time.time()
                error_streak_seconds = time.time() - first_error_time
                elapsed = int(time.time() - start_time)
                if show_progress:
                    print(
                        f"[{elapsed}s] Poll error ({consecutive_errors} consecutive, "
                        f"{int(error_streak_seconds)}/{_POLL_FAILURE_MAX_SECONDS}s): {e}"
                    )
                if error_streak_seconds >= _POLL_FAILURE_MAX_SECONDS:
                    # We genuinely can't tell if training succeeded, failed, or is
                    # still running — NOT the same as a confirmed server-reported
                    # failure. Automation must not treat this as "failed" and relaunch.
                    raise TrainingStatusUnavailableError(
                        session_id=self.id,
                        message=(
                            f"Training: lost contact with server after "
                            f"{consecutive_errors} consecutive poll failures over "
                            f"{elapsed}s. Last error: {e}. The job may still be "
                            f"running server-side — check status independently "
                            f"before relaunching."
                        ),
                    )
                time.sleep(adaptive_poll_interval(poll_interval, start_time))
                continue

            # Extract only scalar values we need, then free the response
            session_data = response_data.get('session', response_data)
            status = session_data.get('status', 'unknown')

            # Queued: job is sitting in the dispatch queue. Print queue status
            # and keep polling until a compute node picks it up.
            if status == 'queued':
                queue_position = session_data.get('queue_position')
                queue_msg = session_data.get('message', 'Waiting for a compute node to become available...')
                if queue_position != last_queue_position or last_status != 'queued':
                    last_progress_time = time.time()
                    last_queue_position = queue_position
                    last_status = 'queued'
                    if show_progress:
                        elapsed = int(time.time() - start_time)
                        pos_str = f" (position {queue_position})" if queue_position else ""
                        print(f"[{elapsed}s] 📥 Queued{pos_str} — {queue_msg}")
                self.status = 'queued'
                del response_data, session_data
                time.sleep(adaptive_poll_interval(poll_interval, start_time))
                continue

            current_epoch = None
            total_epochs = None
            progress_fraction = None
            job_status = status
            latest_fact = None
            error_msg = None
            completion_data = None

            # See _wait_with_tqdm's identical fix above: a retried job_type
            # match must win over an earlier aborted attempt, not the first
            # one found in dict-insertion order.
            candidate_job = None
            candidate_created_at = None
            for job_id, job in response_data.get('jobs', {}).items():
                if job.get('job_type') not in ('train_embedding_space', 'train_es', 'training'):
                    continue
                created_at = job.get('created_at') or ''
                if candidate_job is None or created_at > candidate_created_at:
                    candidate_job = job
                    candidate_created_at = created_at

            if candidate_job is not None:
                job = candidate_job
                current_epoch = job.get('current_epoch') or job.get('epoch')
                total_epochs = job.get('total_epochs') or job.get('epochs')
                progress_fraction = job.get('progress')
                job_status = job.get('status', status)
                fun_facts = job.get('fun_facts', [])
                if fun_facts:
                    latest_fact = fun_facts[-1].get('message', '') if isinstance(fun_facts[-1], dict) else str(fun_facts[-1])
                if job_status in ('failed', 'error'):
                    error_msg = (
                        job.get('error')
                        or job.get('error_message')
                        or job.get('failure_reason')
                        or 'Unknown error'
                    )
                # Node still sees the job working (poll_utils.server_liveness_time).
                alive_at = server_liveness_time(job)
                if alive_at is not None:
                    last_progress_time = max(last_progress_time, alive_at)

                # See _wait_with_tqdm's identical fix: the session_chain has
                # claimed this job but it hasn't started running yet (waiting
                # on a compute node for a free GPU/worker slot between
                # pipeline steps) — current_epoch/progress_fraction are
                # legitimately still None, so treat it like the 'queued'
                # branch above rather than letting dispatch-wait time count
                # against the stall budget.
                if job_awaiting_start(job):
                    if job_status != last_status and show_progress:
                        elapsed = int(time.time() - start_time)
                        print(f"[{elapsed}s] 📥 Dispatched, waiting for a free compute slot...")
                    last_progress_time = time.time()
                    last_status = job_status
                    self.status = job_status
                    del response_data, session_data
                    time.sleep(adaptive_poll_interval(poll_interval, start_time))
                    continue

            # The training job entry may not exist yet if the pipeline failed in
            # an earlier step (create_structured_data, pre_analysis_architecture,
            # ...) before train_es was ever dispatched — fall back to any failed
            # job's error so we don't report "Unknown error" when the server did.
            if error_msg is None and (job_status in ('failed', 'error') or status == 'failed'):
                for job_id, job in response_data.get('jobs', {}).items():
                    if job.get('status') in ('failed', 'error'):
                        error_msg = (
                            job.get('error')
                            or job.get('error_message')
                            or job.get('failure_reason')
                        )
                        if error_msg:
                            break

            # Keep response_data only if training is done (for _update_from_session)
            if job_status == 'done' or status == 'done':
                completion_data = response_data

            # Free the response dict immediately — don't hold across sleep()
            del response_data, session_data

            # A non-failed read means an earlier 'failed' reading (if any) was
            # transient/unconfirmed — reset the confirmation counter.
            is_failed_this_read = (job_status == 'failed' or status == 'failed')
            if not is_failed_this_read:
                consecutive_failed_reads = 0

            # A caller cancelling their own job mid-wait shouldn't see that
            # reported as a training failure. CANCELLED is a terminal status
            # in job_manager (no legal transition back to running), so
            # unlike 'failed' this needs no re-poll confirmation.
            is_cancelled_this_read = (job_status == 'cancelled' or status == 'cancelled')

            # Reset stall timer on any sign of progress (epoch tick, status change,
            # or smooth fraction advancing — the latter ticks per-batch on the server)
            fraction_advanced = (
                isinstance(progress_fraction, (int, float))
                and (last_progress_fraction is None or progress_fraction > last_progress_fraction + 1e-6)
            )
            if current_epoch != last_epoch or job_status != last_status or fraction_advanced:
                last_progress_time = time.time()
                if isinstance(progress_fraction, (int, float)):
                    last_progress_fraction = progress_fraction

            # Progress update — print on epoch/status changes OR on ≥1% smooth advance
            if show_progress:
                elapsed = int(time.time() - start_time)
                state_changed = current_epoch != last_epoch or job_status != last_status
                smooth_changed = (
                    isinstance(progress_fraction, (int, float))
                    and (last_printed_fraction is None or progress_fraction - last_printed_fraction >= 0.01)
                )
                if state_changed or smooth_changed:
                    if isinstance(progress_fraction, (int, float)) and 0.0 <= progress_fraction <= 1.0:
                        pct = int(progress_fraction * 100)
                    elif current_epoch and total_epochs:
                        pct = int(current_epoch / total_epochs * 100)
                    else:
                        pct = None
                    if pct is not None and current_epoch and total_epochs:
                        bar = "█" * (pct // 5) + "░" * (20 - pct // 5)
                        print(f"[{elapsed}s] [{bar}] {current_epoch}/{total_epochs} epochs ({pct}%) - {job_status}")
                    else:
                        print(f"[{elapsed}s] Training: {job_status}")
                    if isinstance(progress_fraction, (int, float)):
                        last_printed_fraction = progress_fraction
                if latest_fact and latest_fact != last_fact:
                    print(f"   {latest_fact}")
                    last_fact = latest_fact
                if (not epochs_done_announced and current_epoch and total_epochs
                        and current_epoch >= total_epochs and job_status != 'done'):
                    # All epochs are in, but the job/session hasn't reported
                    # terminal yet -- baseline fitting, threshold
                    # calibration, and model-card generation all run after
                    # the last epoch tick. Without this, output goes silent
                    # right after the 100% line and reads as hung.
                    print(f"   epochs done, finalizing ({job_status})...")
                    epochs_done_announced = True

            # Track progress (always, even when not showing)
            last_epoch = current_epoch
            last_status = job_status

            # Check completion
            if completion_data is not None:
                self._update_from_session(completion_data)
                # Set AFTER _update_from_session — see the comment on the
                # matching assignment in _wait_with_tqdm above.
                self.status = 'done'
                del completion_data
                if show_progress:
                    print(f"✅ Training complete!")
                    if self.dimensions:
                        print(f"   Dimensions: {self.dimensions}")
                    if self.epochs:
                        print(f"   Epochs: {self.epochs}")
                return self

            elif is_cancelled_this_read:
                self.status = 'cancelled'
                if show_progress:
                    elapsed = int(time.time() - start_time)
                    print(f"[{elapsed}s] 🚫 Training cancelled")
                return self

            elif is_failed_this_read:
                consecutive_failed_reads += 1
                if consecutive_failed_reads < _FAILED_STATUS_CONFIRM_READS:
                    # Don't trust a single 'failed' read — the jobs dict can
                    # transiently miss the matched job entry while the job keeps
                    # training server-side. Re-poll to confirm before raising.
                    if show_progress:
                        elapsed = int(time.time() - start_time)
                        print(
                            f"[{elapsed}s] Training: status read as 'failed' "
                            f"(unconfirmed {consecutive_failed_reads}/{_FAILED_STATUS_CONFIRM_READS}) — re-checking..."
                        )
                    time.sleep(adaptive_poll_interval(poll_interval, start_time))
                    continue

                self.status = 'error'
                raise RuntimeError(f"Training failed: {error_msg or 'Unknown error (server did not report a reason)'}")

            # Periodic gc to combat pymalloc arena fragmentation
            now = time.time()
            if now - last_gc_time > 60:
                gc.collect()
                last_gc_time = now

            time.sleep(adaptive_poll_interval(poll_interval, start_time))

    def encode(
        self,
        records: Union[Dict[str, Any], List[Dict[str, Any]], 'pd.DataFrame'],
        short: bool = False,
        *,
        intent: Optional[str] = None,
        representation: str = "auto",
        expected_missing: Optional[List[str]] = None,
    ) -> Union[List[Dict[str, Any]], List[List[float]]]:
        """
        Encode records to embedding vectors.

        Args:
            records: Single record, list of records, or DataFrame
            short: Deprecated. If True, return only 3D vectors. Use
                   intent='visualization' instead.
            expected_missing: Column names you are INTENTIONALLY omitting from
                   these records (e.g. imputation hold-outs, or fields you simply
                   don't have). Declaring them tells the server the absence is by
                   design, so it won't warn about a column mismatch. Only columns
                   you didn't declare — and didn't supply — are flagged.
            intent: Customer-facing intent — one of 'clustering' (kNN /
                   similarity, default for external tools), 'visualization'
                   (2D/3D plots), 'near_lossless' (per-column fidelity,
                   good for downstream tree/linear models), 'highly_encoded'
                   (dense pooled representation). Task intents ('regression',
                   'binary_class', 'multiclass', 'multilabel') require a
                   trained Single Predictor — use Predictor.encode() with
                   intent= instead. When given, returns a single 'embedding'
                   field per record in the resolved port's shape.
            representation: 'auto' (default), 'preserved' (per-column),
                   or 'compressed' (dense pooled). Ignored unless intent
                   is given.

        Returns:
            intent=None (legacy): List of dicts with short+full embeddings,
                OR a list of 3D vectors if short=True.
            intent given: List of dicts with 'embedding' + 'intent' +
                'representation' + 'query_record' + 'port_spec' fields.
                ``port_spec`` describes the embedding the server actually
                produced — ``{name, width, encoding_depth, representation,
                available}`` — so the caller can introspect what they got.

        Example:
            vectors_for_kmeans = fm.encode(records, intent='clustering')
            vectors_for_plot = fm.encode(records, intent='visualization')
            per_col = fm.encode(records, intent='near_lossless')

            # Inspect what the server returned:
            r = fm.encode(records, intent='near_lossless')[0]
            r['port_spec']['name']             # → 'pre_transformer'
            r['port_spec']['width']            # → e.g. 1152
            r['port_spec']['encoding_depth']   # → 'near_lossless'
        """
        if not self._ctx:
            raise ValueError("FoundationalModel not connected to client")

        # Normalize input
        if isinstance(records, dict):
            records = [records]
        elif hasattr(records, 'to_dict'):
            records = records.to_dict('records')

        # Clean records
        cleaned = [self._clean_record(r) for r in records]

        body: Dict[str, Any] = {"records": cleaned}
        if intent is not None:
            body["intent"] = intent
            body["representation"] = representation
        if expected_missing:
            body["expected_missing"] = list(expected_missing)

        response = self._ctx.post_json(
            f"/session/{self.id}/encode_records",
            data=body,
        )

        results = response.get('results', [])

        if short and intent is None:
            return [r["embedding"] for r in results]

        return results

    # ------------------------------------------------------------------
    # Imputation (Gibbs-style fill-in-the-blanks)
    # ------------------------------------------------------------------

    def impute(
        self,
        records: Union[Dict[str, Any], List[Dict[str, Any]], 'pd.DataFrame'],
        columns: Optional[List[str]] = None,
        strategy: str = "greedy",
        report: bool = False,
    ) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """Impute missing/null fields in partial records using Gibbs-style probe ensemble.

        Predicts the most-confident missing column first, feeds that prediction
        back into the ES for better context, then predicts the next column, and so on.

        Args:
            records: Single record, list of records, or DataFrame.
                     Missing fields should be None or absent.
            columns: Specific columns to impute. Default: all missing probeable columns.
            strategy: "greedy" (sequential, higher quality) or "parallel" (all-at-once).
            report: If True, include a "report" key in the return value with per-column
                    aggregate stats (prediction distribution, confidence distribution).
                    When report=True, always returns a dict with "results" and "report".

        Returns:
            Without report: single result dict or list of result dicts, each containing:
            - "record": The complete record with all fields filled
            - "imputed_fields": Dict mapping column -> {value, confidence, cascade_factor,
              effective_confidence, iteration, target_type, probabilities}
            - "skipped_columns": Columns that couldn't be imputed and why
            - "strategy": Which strategy was used
            - "n_iterations": How many Gibbs iterations were run

            With report=True: dict with:
            - "results": list of result dicts (as above)
            - "report": per-column aggregate stats keyed by column name, each containing
              "target_type", "n_imputed", "prediction_dist", "confidence_dist"

        Example:
            result = fm.impute({"age": 35, "income": None, "job": None})
            print(result["record"])           # {"age": 35, "income": 52000, "job": "engineer"}
            print(result["imputed_fields"])   # {"income": {"value": 52000, ...}, ...}

            # With distribution report (useful for batch evaluation):
            out = fm.impute(records, report=True)
            print(out["report"]["education"])
            # {"target_type": "set", "n_imputed": 400,
            #  "prediction_dist": {"Bachelors": 120, ...}, "confidence_dist": [...]}
        """
        if not self._ctx:
            raise ValueError("FoundationalModel not connected to client")

        single = isinstance(records, dict)
        if single:
            records = [records]
        elif hasattr(records, 'to_dict'):
            records = records.to_dict('records')

        cleaned = [self._clean_record(r) for r in records]

        payload = {"records": cleaned, "strategy": strategy}
        if columns is not None:
            payload["columns"] = columns
        if report:
            payload["report"] = True

        response = self._ctx.post_json(
            f"/session/{self.id}/impute",
            data=payload,
        )

        if report:
            return {
                "results": response.get("results", []),
                "report": response.get("report", {}),
            }
        results = response.get("results", [])
        return results[0] if single else results

    def autocomplete_record(
        self,
        records: Union[Dict[str, Any], List[Dict[str, Any]], 'pd.DataFrame'],
        method: str = "beam",
        top_k: int = 1,
        columns: Optional[List[str]] = None,
        beam_width: int = 32,
        top_k_columns: int = 3,
        top_k_values: int = 5,
        score_fn: str = "log_sum",
    ) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """Autocomplete missing fields, returning ranked completions instead of a single guess.

        Unlike `impute()`, which returns a single point estimate, this returns a
        ranked list of plausible completions plus per-column divergence — the
        honest output when a partial record admits multiple plausible fills.

        Args:
            records: Single record dict, list of dicts, or DataFrame. Missing
                fields should be None or absent from the dict.
            method: "parallel", "greedy", or "beam" (default). beam runs a
                batched beam search over (column, value) fill-in orders.
            top_k: Number of ranked completions to return per record (beam only;
                parallel/greedy always return 1).
            columns: Optional filter — only impute these columns.
            beam_width: Max live beams per iteration (beam only).
            top_k_columns: Branch on top-J columns by probe confidence (beam only).
            top_k_values: Branch on top-K values per column (beam only;
                classification only — regression currently uses K=1).
            score_fn: "log_sum" (default), "min", or "length_norm".

        Returns:
            For a single record input: a dict with keys:
              - "completions": list of {record, imputed_fields, score, min_confidence, n_iterations}
              - "divergence": per-column {entropy, modes, n_unique} across completions
              - "method", "top_k", "n_iterations", ...
            For a list/DataFrame input: a list of such dicts (one per record).

        Example:
            result = fm.autocomplete_record(
                {"age": 35, "income": None, "job": None},
                method="beam", top_k=10,
            )
            for c in result["completions"]:
                print(c["score"], c["record"])
            print(result["divergence"])  # which columns the model is uncertain about
        """
        if not self._ctx:
            raise ValueError("FoundationalModel not connected to client")
        if method not in ("parallel", "greedy", "beam"):
            raise ValueError(
                f"Invalid method: {method!r}. Must be 'parallel', 'greedy', or 'beam'."
            )

        single = isinstance(records, dict)
        if single:
            records = [records]
        elif hasattr(records, 'to_dict'):
            records = records.to_dict('records')

        cleaned = [self._clean_record(r) for r in records]

        payload: Dict[str, Any] = {
            "records": cleaned,
            "method": method,
            "top_k": top_k,
            "beam_width": beam_width,
            "top_k_columns": top_k_columns,
            "top_k_values": top_k_values,
            "score_fn": score_fn,
        }
        if columns is not None:
            payload["columns"] = columns

        response = self._ctx.post_json(
            f"/session/{self.id}/autocomplete_record",
            data=payload,
        )

        results = response.get("results", [])
        return results[0] if single else results

    # ------------------------------------------------------------------
    # ES Instant Prediction (probe-based ensemble)
    #
    # Response shape depends on the target column's type:
    #   - classification/regression: {"prediction": <class-or-value>,
    #     "confidence": float, "probabilities": {class: prob, ...}, "model": str}
    #   - multilabel targets (comma/list-delimited tag columns): {"prediction":
    #     [tag, ...], "confidence": float|None, "probabilities": {tag: prob, ...},
    #     "model": str, "target_type": "multilabel"} — "prediction" is the list
    #     of tags above a 0.5 threshold, not a single class.
    # ------------------------------------------------------------------

    def predict_linear(
        self,
        target_column: str,
        records: Union[Dict[str, Any], List[Dict[str, Any]], 'pd.DataFrame'],
    ) -> List[Dict[str, Any]]:
        """Instant prediction using linear probe on frozen embeddings.

        Uses LogisticRegression for classification, Ridge for regression.
        No neural SP training required — fits on first call, cached after.

        Args:
            target_column: Column to predict
            records: Single record, list of records, or DataFrame

        Returns:
            List of prediction dicts with prediction, confidence, probabilities, model.
        """
        return self._light_predict(target_column=target_column, records=records, model="linear")

    def predict_xgboost(
        self,
        target_column: str,
        records: Union[Dict[str, Any], List[Dict[str, Any]], 'pd.DataFrame'],
    ) -> List[Dict[str, Any]]:
        """Instant prediction using XGBoost probe on frozen embeddings.

        Args:
            target_column: Column to predict
            records: Single record, list of records, or DataFrame

        Returns:
            List of prediction dicts with prediction, confidence, probabilities, model.
        """
        return self._light_predict(target_column=target_column, records=records, model="xgboost")

    def predict_knn(
        self,
        target_column: str,
        records: Union[Dict[str, Any], List[Dict[str, Any]], 'pd.DataFrame'],
    ) -> List[Dict[str, Any]]:
        """Instant prediction using k-NN probe on frozen embeddings.

        Args:
            target_column: Column to predict
            records: Single record, list of records, or DataFrame

        Returns:
            List of prediction dicts with prediction, confidence, probabilities, model.
        """
        return self._light_predict(target_column=target_column, records=records, model="knn")

    def predict_random_forest(
        self,
        target_column: str,
        records: Union[Dict[str, Any], List[Dict[str, Any]], 'pd.DataFrame'],
    ) -> List[Dict[str, Any]]:
        """Instant prediction using Random Forest probe on frozen embeddings.

        Args:
            target_column: Column to predict
            records: Single record, list of records, or DataFrame

        Returns:
            List of prediction dicts with prediction, confidence, probabilities, model.
        """
        return self._light_predict(target_column=target_column, records=records, model="random_forest")

    def predict(
        self,
        target_column: str,
        records: Union[Dict[str, Any], List[Dict[str, Any]], 'pd.DataFrame'],
        model: str = "xgboost",
        model_type: Optional[str] = None,
        predictor_id: Optional[str] = None,
    ) -> Union[PredictionResult, List[PredictionResult]]:
        """Predict any column using the foundation model.

        Routing logic:
        - If model_type="sp" or predictor_id is given, forces SP prediction.
        - If model_type="foundation" (or "foundation+xgboost", etc.), forces
          foundation model prediction even if an SP exists.
        - If neither is given (default): uses the SP if one is trained for
          this target column, otherwise falls back to the foundation model.

        Returns full PredictionResult objects with prediction_uuid, model_type,
        confidence, probabilities — the same result shape either way.

        Args:
            target_column: Column to predict
            records: Single record, list of records, or DataFrame
            model: Foundation model to use — "xgboost" (default), "linear",
                   "knn", "random_forest", or "ensemble".
                   Only used for foundation predictions.
            model_type: Force a specific prediction path:
                   "sp" — use trained SinglePredictor (error if none exists)
                   "foundation" — use foundation model (skip SP even if available)
                   None (default) — auto-route: SP if available, else foundation
            predictor_id: Use a specific SP by ID (implies model_type="sp")

        Returns:
            Single PredictionResult if input was a single dict,
            list of PredictionResult if input was a list or DataFrame.

        Example:
            # Auto-route (SP if available, else foundation)
            result = fm.predict("churned", {"age": 35, "income": 50000})

            # Force foundation model
            result = fm.predict("churned", record, model_type="foundation")

            # Force SP
            result = fm.predict("churned", record, model_type="sp")

            # Check what was used
            print(result.model_type)  # "foundation+xgboost" or "sp"
        """
        # Explicit SP request
        use_sp = (
            model_type == "sp"
            or predictor_id is not None
        )
        # Explicit foundation request
        use_foundation = (
            model_type is not None
            and model_type.startswith("foundation")
        )

        if use_sp:
            sp = self._find_predictor(target_column, predictor_id=predictor_id)
            if sp is None:
                raise ValueError(
                    f"No trained SinglePredictor found for target_column='{target_column}'"
                    + (f", predictor_id='{predictor_id}'" if predictor_id else "")
                )
            single_input = isinstance(records, dict)
            if single_input:
                return sp.predict(records)
            return sp.batch_predict(records, show_progress=False)

        if use_foundation:
            # Parse model from model_type if given as "foundation+xgboost"
            if "+" in model_type:
                model = model_type.split("+", 1)[1]
            return self.foundation_predict(
                target_column=target_column, records=records, model=model,
            )

        # Auto-route: SP if available, else foundation
        sp = self._find_predictor(target_column)
        if sp is not None:
            single_input = isinstance(records, dict)
            if single_input:
                return sp.predict(records)
            return sp.batch_predict(records, show_progress=False)

        return self.foundation_predict(
            target_column=target_column, records=records, model=model,
        )

    def _find_predictor(
        self,
        target_column: str,
        predictor_id: Optional[str] = None,
    ) -> Optional[Predictor]:
        """Find a trained SP for the given target column (and optional ID), or None."""
        try:
            predictors = self.list_predictors()
            for p in predictors:
                if predictor_id and p.id != predictor_id:
                    continue
                if p.target_column == target_column and p.status == 'done':
                    return p
        except Exception:
            pass
        return None

    def _light_predict(
        self,
        target_column: str,
        records: Union[Dict[str, Any], List[Dict[str, Any]], 'pd.DataFrame'],
        model: str,
    ) -> List[Dict[str, Any]]:
        """Internal: ES probe-based prediction via compute node API."""
        if not self._ctx:
            raise ValueError("FoundationalModel not connected to client")

        # Normalize input
        if isinstance(records, dict):
            records = [records]
        elif hasattr(records, 'to_dict'):
            records = records.to_dict('records')

        # Clean records
        cleaned = [self._clean_record(r) for r in records]

        response = self._ctx.post_json(
            f"/compute/session/{self.id}/light_predict",
            data={
                "target_column": target_column,
                "records": cleaned,
                "model": model,
            },
        )

        return response.get('predictions', [])

    def foundation_predict(
        self,
        target_column: str,
        records: Union[Dict[str, Any], List[Dict[str, Any]], 'pd.DataFrame'],
        model: str = "xgboost",
    ) -> Union[PredictionResult, List[PredictionResult]]:
        """Predict any column using the foundation model.

        Returns full PredictionResult objects with prediction_uuid for feedback
        loops, model_type identification, and all standard fields.

        If no SinglePredictor has been trained, this is the fastest way to get
        predictions from a foundation model.

        Args:
            target_column: Column to predict
            records: Single record, list of records, or DataFrame
            model: Model to use — "xgboost" (default), "linear",
                   "knn", "random_forest", or "ensemble"

        Returns:
            Single PredictionResult if input was a single dict,
            list of PredictionResult if input was a list or DataFrame.
            For multilabel target columns, read `result.predicted_labels`
            (list of tags) instead of `result.predicted_class` (None —
            there is no single predicted class for a multilabel target).

        Example:
            result = fm.foundation_predict("churned", {"age": 35, "income": 50000})
            print(result.predicted_class)   # "yes"
            print(result.confidence)        # 0.82
            print(result.model_type)        # "foundation+xgboost"
            print(result.prediction_uuid)   # UUID for feedback

            # Batch
            results = fm.foundation_predict("churned", [{"age": 35}, {"age": 42}])
        """
        if not self._ctx:
            raise ValueError("FoundationalModel not connected to client")

        single_input = isinstance(records, dict)

        # Normalize input
        if single_input:
            records = [records]
        elif hasattr(records, 'to_dict'):
            records = records.to_dict('records')

        cleaned = [self._clean_record(r) for r in records]

        response = self._ctx.post_json(
            f"/compute/session/{self.id}/light_predict",
            data={
                "target_column": target_column,
                "records": cleaned,
                "model": model,
            },
        )

        results = []
        for i, pred in enumerate(response.get('predictions', [])):
            query_record = cleaned[i] if i < len(cleaned) else {}
            result = PredictionResult.from_response(pred, query_record, self._ctx)
            # Ensure model_type is set even if backend didn't include it
            if not result.model_type:
                result.model_type = f"foundation+{model}"
            results.append(result)

        if single_input:
            return results[0] if results else PredictionResult(
                model_type=f"foundation+{model}",
                target_column=target_column,
            )
        return results

    def extend(
        self,
        new_data_file: Optional[str] = None,
        new_data_df: Optional['pd.DataFrame'] = None,
        epochs: Optional[int] = None,
        name: Optional[str] = None,
        session_name_prefix: Optional[str] = None,
        **kwargs
    ) -> 'FoundationalModel':
        """
        Continue training this foundational model on MORE ROWS of data.

        This does NOT modify the current model in place -- it creates a NEW
        session that combines this model's original training data with the
        new rows you provide, and resumes training (warm-started from this
        model's weights) on the combined dataset for `epochs` additional
        epochs. The source model/session is untouched.

        To add new feature COLUMNS to an existing embedding space instead
        (not new rows), see the server-side EmbeddingSpace.extend_from_existing()
        workflow -- that is a different feature and not what this method does.

        Args:
            new_data_file: Path to a local CSV (or .csv.gz) file with new rows.
                Must have the same columns as the original training data.
            new_data_df: DataFrame with new rows (alternative to new_data_file).
            epochs: Additional training epochs on the combined dataset (default: 50).
            name: Optional name for the new extended session.
            session_name_prefix: Optional prefix for the new session ID.
            **kwargs: Extra fields passed through as form data (e.g. project_id).

        Returns:
            New FoundationalModel instance for the extended session (training started).
            Call .wait_for_training() to block until it completes.

        Example:
            more_customers = pd.read_csv("new_customers.csv")
            extended_fm = fm.extend(new_data_df=more_customers, epochs=25)
            extended_fm.wait_for_training()
        """
        if not self._ctx:
            raise ValueError("FoundationalModel not connected to client")
        if new_data_file is None and new_data_df is None:
            raise ValueError("Either new_data_file or new_data_df must be provided")

        if new_data_df is not None:
            file_content, filename = self._ctx.dataframe_to_file(new_data_df)
        else:
            with open(new_data_file, 'rb') as f:
                file_content = f.read()
            filename = Path(new_data_file).name

        form_data = {
            'data_passes': str(epochs if epochs is not None else 50),
        }
        if name:
            form_data['name'] = name
        if session_name_prefix:
            form_data['session_name_prefix'] = session_name_prefix
        if self._ctx.current_project_id and 'project_id' not in kwargs:
            form_data['project_id'] = self._ctx.current_project_id
        for key, value in kwargs.items():
            if value is not None:
                form_data[key] = str(value)

        response = self._ctx.post_multipart(
            f"/compute/session/{self.id}/extend_embedding_space_data",
            data=form_data,
            files={'file': (filename, file_content)},
        )

        new_session_id = response.get('session_id', '')
        return FoundationalModel(
            id=new_session_id,
            name=name,
            status='training',
            _ctx=self._ctx,
        )

    def get_projections(self, limit: int = None, offset: int = 0) -> Dict[str, Any]:
        """Get 2D/3D projections for visualization.

        Args:
            limit: Max number of points to return. If None, returns all points.
            offset: Number of points to skip (for pagination).

        Returns:
            Dict with 'projections' key containing coords, total_count, offset, limit.
        """
        if not self._ctx:
            raise ValueError("FoundationalModel not connected to client")

        params = {}
        if limit is not None:
            params["limit"] = limit
        if offset:
            params["offset"] = offset
        return self._ctx.get_json(f"/session/{self.id}/projections", params=params or None)

    def get_epoch_projections(
        self,
        epoch: str = None,
        start_epoch: int = None,
        limit: int = None,
        point_limit: int = None,
        point_offset: int = 0,
        metadata_only: bool = False,
        include_source_data: bool = False,
    ) -> Dict[str, Any]:
        """Get epoch projection data for training movie visualization.

        Args:
            epoch: Single epoch to return ('last' or a number). Most efficient for thumbnails.
            start_epoch: Start epoch (1-indexed). If not specified, returns all epochs.
            limit: Max number of epochs to return.
            point_limit: Max number of points per epoch to return (for incremental loading).
            point_offset: Number of points to skip per epoch (for pagination).
            metadata_only: If True, only return metadata (epoch count, etc).
            include_source_data: If True, enrich coords with original dataset columns.

        Returns:
            Dict with 'epoch_projections' key. Each epoch contains coords with
            total_count, offset, limit when point pagination is used.
        """
        if not self._ctx:
            raise ValueError("FoundationalModel not connected to client")

        params = {}
        if epoch is not None:
            params["epoch"] = epoch
        if start_epoch is not None:
            params["start_epoch"] = start_epoch
        if limit is not None:
            params["limit"] = limit
        if point_limit is not None:
            params["point_limit"] = point_limit
        if point_offset:
            params["point_offset"] = point_offset
        if metadata_only:
            params["metadata_only"] = "true"
        if include_source_data:
            params["include_source_data"] = "true"
        return self._ctx.get_json(f"/session/{self.id}/epoch_projections", params=params or None)

    def get_sphere_preview(self, save_path: str = None) -> bytes:
        """
        Get the 2D sphere projection preview image (PNG).

        Args:
            save_path: Optional path to save the PNG file. If provided, the image
                      will be written to this path.

        Returns:
            Raw PNG image bytes.
        """
        if not self._ctx:
            raise ValueError("FoundationalModel not connected to client")

        png_bytes = self._ctx.get_bytes(f"/session/{self.id}/preview")

        if save_path:
            with open(save_path, 'wb') as f:
                f.write(png_bytes)

        return png_bytes

    def get_training_metrics(self) -> Dict[str, Any]:
        """Get training metrics and history."""
        if not self._ctx:
            raise ValueError("FoundationalModel not connected to client")

        return self._ctx.get_json(f"/session/{self.id}/training_metrics")

    def training_summary(self) -> Dict[str, Any]:
        """How the embedding space trained, from its training timeline.

        Returns ``{"epochs", "final_train_loss", "final_val_loss",
        "best_val_loss", "best_epoch", "d_model", "n_parameters"}`` (a key is
        None when not recorded), or ``{}`` before the first epoch is recorded.
        Also fills ``self.epochs``, ``self.final_loss`` (the final VALIDATION
        loss) and ``self.dimensions``, which a plain refresh() can't: loss is
        not on the session.
        """
        data = (self.get_training_metrics() or {}).get('data') or {}
        epochs = data.get('epochs') or []
        if not epochs:
            return {}

        def _last(values):
            present = [v for v in (values or []) if v is not None]
            return present[-1] if present else None

        summary = {
            'epochs': len(epochs),
            'final_train_loss': _last(data.get('train_loss')),
            'final_val_loss': _last(data.get('val_loss')),
            'best_val_loss': data.get('best_val_loss'),
            'best_epoch': data.get('best_epoch'),
            'd_model': data.get('d_model'),
            'n_parameters': (data.get('metadata') or {}).get('n_parameters'),
        }
        self.epochs = summary['epochs']
        self.final_loss = summary['final_val_loss']
        if summary['d_model']:
            self.dimensions = summary['d_model']
        return summary

    def get_model_card(self) -> Dict[str, Any]:
        """Get the model card for this foundational model."""
        if not self._ctx:
            raise ValueError("FoundationalModel not connected to client")

        return self._ctx.get_json(f"/session/{self.id}/model_card")

    def what_is_this_model_good_for(self) -> Dict[str, Any]:
        """Concrete, label-aware use-case summary for this foundational model.

        Common phrasings that all mean *this method*. If you (human or agent)
        are looking for any of these, you are in the right place:

          - "what is this model good for?"
          - "recommend(ed) uses" / "what do you recommend I use this for?"
          - "use cases" / "use case for this model"
          - "intended uses" / "intended use" (Mitchell et al. model-card spec)
          - "best uses" / "best use of this model"
          - "suggested applications" / "where should I deploy this?"
          - "suitability" / "deployment guide" / "applicability"

        Same structured dict shape as ``Predictor.what_is_this_model_good_for()``.
        See that method for full field documentation. Returns an empty dict
        if the model card doesn't carry a ``what_is_this_model_good_for``
        block.
        """
        card = self.get_model_card() or {}
        return card.get("what_is_this_model_good_for") or {}

    def list_predictors(self) -> List[Predictor]:
        """List all predictors for this foundational model.

        Primary source is ``session.job_plan`` (persisted on the session doc)
        rather than the ``jobs`` block, which is a live view over per-job
        Redis records that carry a TTL and can be gone long before the
        session itself expires — a predictor that finished training would
        silently vanish from this list once its Redis record aged out even
        though the trained model is still on disk and servable. ``job_plan``
        entries are enriched with the live Redis record's status/accuracy
        when one is still present, and otherwise fall back to job_plan's own
        status / whether ``single_predictors`` has a model path for that
        index. Any ``jobs`` entry not already covered by ``job_plan`` (e.g. a
        job dispatched but not yet persisted to the plan) is still surfaced.
        """
        if not self._ctx:
            raise ValueError("FoundationalModel not connected to client")

        response = self._ctx.get_json(f"/compute/session/{self.id}")
        session_doc = response.get('session') or {}
        jobs = response.get('jobs') or {}
        job_plan = session_doc.get('job_plan') or []
        single_predictors = session_doc.get('single_predictors') or []
        predictor_deletion_protection = session_doc.get('predictor_deletion_protection') or {}

        # Best-effort fetch of the session's persisted training_metrics.json
        # (via GET /session/{id}/training_metrics — the same endpoint
        # Predictor.get_metrics() uses). This is a session-level endpoint,
        # not predictor-specific, so we only apply it to a predictor when its
        # target_column matches — a done predictor's accuracy/auc/f1 should
        # never come from a different predictor's metrics file. 404/422
        # (nothing trained yet) is expected and silently skipped; anything
        # else propagates so real errors aren't hidden.
        metrics_by_target_column = {}
        try:
            tm_response = self._ctx.get_json(f"/session/{self.id}/training_metrics")
            tm = tm_response.get('training_metrics') or {}
            final_metrics = tm.get('final_metrics') or tm.get('sp_metrics') or {}
            tm_target_column = tm.get('target_column')
            if tm_target_column and final_metrics:
                metrics_by_target_column[tm_target_column] = final_metrics
        except requests.exceptions.HTTPError:
            pass

        predictors = []
        seen_job_ids = set()

        for job_desc in job_plan:
            if job_desc.get('job_type') != 'train_single_predictor':
                continue

            spec = job_desc.get('spec') or {}
            target_column = spec.get('target_column', '')
            predictor_index = job_desc.get('predictor_index') or 0
            pred_id = job_desc.get('predictor_id') or f"predictor-{target_column}"

            job_id = job_desc.get('job_id')
            live_job = jobs.get(job_id) if job_id else None
            if job_id:
                seen_job_ids.add(job_id)
            has_model = predictor_index < len(single_predictors) and bool(single_predictors[predictor_index])

            # job_plan's own created_at is the durable fallback once the
            # live Redis job record has TTL'd out — Redis is the freshest
            # source when present, job_plan is the one that survives.
            job_plan_created_at = _parse_datetime(job_desc.get('created_at'))

            if live_job:
                status = live_job.get('status')
                accuracy = live_job.get('accuracy')
                auc = live_job.get('auc') or live_job.get('roc_auc')
                f1 = live_job.get('f1') or live_job.get('f1_score')
                created_at = _parse_datetime(live_job.get('created_at')) or job_plan_created_at
            elif has_model or job_desc.get('status') == 'completed':
                status = 'done'
                accuracy = auc = f1 = None
                created_at = job_plan_created_at
            else:
                status = job_desc.get('status')
                accuracy = auc = f1 = None
                created_at = job_plan_created_at

            file_metrics = metrics_by_target_column.get(target_column)
            if file_metrics:
                accuracy = accuracy if accuracy is not None else (
                    file_metrics.get('val_accuracy') or file_metrics.get('accuracy'))
                auc = auc if auc is not None else (
                    file_metrics.get('val_auc') or file_metrics.get('auc')
                    or file_metrics.get('val_roc_auc') or file_metrics.get('roc_auc'))
                f1 = f1 if f1 is not None else (
                    file_metrics.get('val_f1') or file_metrics.get('f1') or file_metrics.get('f1_score'))

            predictors.append(Predictor(
                id=pred_id,
                session_id=self.id,
                target_column=target_column,
                target_type=spec.get('target_column_type', 'set'),
                name=job_desc.get('name'),
                status=status,
                accuracy=accuracy,
                auc=auc,
                f1=f1,
                created_at=created_at,
                deletion_protection=bool(predictor_deletion_protection.get(pred_id, False)),
                _ctx=self._ctx,
                _foundational_model=self,
            ))

        # Defense in depth: surface any live SP job Redis carries that
        # job_plan doesn't know about yet (dispatched but not yet persisted
        # to the plan, or a reconstructed/legacy session document).
        for job_id, job in jobs.items():
            if job_id in seen_job_ids or job.get('job_type') != 'train_single_predictor':
                continue
            target_column = job.get('target_column', '')
            pred_id = job.get('predictor_id') or f"predictor-{target_column}"
            file_metrics = metrics_by_target_column.get(target_column) or {}
            predictors.append(Predictor(
                id=pred_id,
                session_id=self.id,
                target_column=target_column,
                target_type=job.get('target_column_type', 'set'),
                name=job.get('name'),
                status=job.get('status'),
                accuracy=job.get('accuracy') or file_metrics.get('val_accuracy') or file_metrics.get('accuracy'),
                auc=(job.get('auc') or job.get('roc_auc')
                     or file_metrics.get('val_auc') or file_metrics.get('auc')
                     or file_metrics.get('val_roc_auc') or file_metrics.get('roc_auc')),
                f1=(job.get('f1') or job.get('f1_score')
                    or file_metrics.get('val_f1') or file_metrics.get('f1') or file_metrics.get('f1_score')),
                created_at=_parse_datetime(job.get('created_at')),
                deletion_protection=bool(predictor_deletion_protection.get(pred_id, False)),
                _ctx=self._ctx,
                _foundational_model=self,
            ))

        return predictors

    def refresh(self) -> Dict[str, Any]:
        """Re-fetch status from the server and update this object's fields.

        Returns:
            The raw session response dict.
        """
        if not self._ctx:
            raise ValueError("FoundationalModel not connected to client")

        response_data = self._ctx.get_json(f"/compute/session/{self.id}")
        self._update_from_session(response_data)
        return response_data

    def is_ready(self) -> bool:
        """Check if training is complete by refreshing status from the server.

        Returns:
            True if status is "done", False otherwise.
        """
        self.refresh()
        return self.status == "done"

    def _update_from_session(self, response_data: Dict[str, Any]) -> None:
        """Update fields from session API response.

        The response from GET /session/{id} has structure:
            {"session": {...}, "jobs": {...}, ...}
        """
        # Handle both nested and flat response formats
        session = response_data.get('session', response_data)
        jobs = response_data.get('jobs', {})
        self.jobs = jobs

        # Core session fields
        if session.get('name') and not self.name:
            self.name = session['name']
        if session.get('status'):
            self.status = session['status']
        if session.get('es_status'):
            self.es_status = session['es_status']
        if session.get('sp_status'):
            self.sp_status = session['sp_status']
        if session.get('session_type'):
            self.session_type = session['session_type']
        if session.get('compute_cluster'):
            self.compute_cluster = session['compute_cluster']
        if session.get('user_metadata') is not None:
            self.user_metadata = session['user_metadata']
        if 'deletion_protection' in session:
            self.deletion_protection = bool(session['deletion_protection'])
        if session.get('created_at') and not self.created_at:
            self.created_at = _parse_datetime(session['created_at'])
        if session.get('finished_at'):
            self.updated_at = _parse_datetime(session['finished_at'])
        elif session.get('started_at'):
            self.updated_at = _parse_datetime(session['started_at'])

        # The session carries the ES width in optimal_es_config; epochs come
        # from the train_es job below. Loss is not on the session at all --
        # training_summary() reads it from the training timeline. (This used
        # to read session['model_info'] / ['training_stats'], which no server
        # writes, so dimensions/epochs/final_loss were None for every model.)
        es_config = session.get('optimal_es_config') or {}
        if es_config.get('d_model'):
            self.dimensions = es_config['d_model']

        # Extract error_message and training_progress from jobs
        for job_id, job in jobs.items():
            job_type = job.get('job_type', '')
            job_status = job.get('status', '')

            # Training progress from ES training job
            if job_type in ('train_embedding_space', 'train_es', 'training'):
                current_epoch = job.get('current_epoch') or job.get('epoch')
                total_epochs = job.get('total_epochs') or job.get('epochs')
                if current_epoch and job_status in ('done', 'completed'):
                    self.epochs = current_epoch
                if current_epoch or total_epochs:
                    self.training_progress = {
                        'current_epoch': current_epoch,
                        'total_epochs': total_epochs,
                        'job_status': job_status,
                        'fun_facts': job.get('fun_facts', []),
                    }

            # Error message from any failed job
            if job_status in ('failed', 'error'):
                err = job.get('error') or job.get('error_message') or job.get('failure_reason')
                if err:
                    self.error_message = err

    def _clean_record(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """Clean a record for API submission."""
        import math

        cleaned = {}
        for key, value in record.items():
            if isinstance(value, float):
                if math.isnan(value) or math.isinf(value):
                    value = None
            if hasattr(value, 'item'):
                value = value.item()
            cleaned[key] = value
        return cleaned

    def get_columns(self) -> List[str]:
        """
        Get the column names in this foundational model's embedding space.

        Returns:
            List of column name strings

        Example:
            columns = fm.get_columns()
            print(columns)  # ['age', 'income', 'city', ...]
        """
        if not self._ctx:
            raise ValueError("FoundationalModel not connected to client")

        response = self._ctx.get_json(f"/compute/session/{self.id}/columns")
        return response.get('column_names', response.get('columns', []))

    @property
    def columns(self) -> List[str]:
        """Column names in this foundational model's embedding space."""
        return self.get_columns()

    @property
    def schema_metadata(self) -> Dict[str, Any]:
        """Get schema metadata including column names and types.

        Returns:
            Dict with 'column_names', 'column_types', and 'num_columns'
        """
        if not self._ctx:
            raise ValueError("FoundationalModel not connected to client")
        return self._ctx.get_json(f"/compute/session/{self.id}/columns")

    def clone(
        self,
        target_compute_cluster: Optional[str] = None,
        new_name: Optional[str] = None,
        source_compute_cluster: Optional[str] = None,
    ) -> 'FoundationalModel':
        """
        Clone this embedding space, optionally to a different compute node.

        Args:
            target_compute_cluster: Target compute cluster (None = same node)
            new_name: Name for the cloned session
            source_compute_cluster: Source compute cluster (if routing needed)

        Returns:
            New FoundationalModel instance for the cloned embedding space

        Example:
            cloned = fm.clone(
                target_compute_cluster="churro",
                new_name="my-model-clone"
            )
        """
        if not self._ctx:
            raise ValueError("FoundationalModel not connected to client")

        data = {
            "to_compute": target_compute_cluster,
            "new_session_name": new_name,
        }

        response = self._ctx.post_json(
            f"/compute/session/{self.id}/clone_embedding_space",
            data=data
        )

        new_session_id = response.get('new_session_id', '')
        return FoundationalModel(
            id=new_session_id,
            name=new_name,
            status="done",
            created_at=datetime.now(),
            _ctx=self._ctx,
        )

    def refresh(self) -> Dict[str, Any]:
        """
        Refresh this foundational model's state from the server.

        Returns the full server-side info for this model, and updates
        local attributes (status, epochs, dimensions, etc.).

        Returns:
            Full model info dictionary from the server

        Example:
            info = fm.refresh()
            print(fm.status)   # Updated from server
            print(fm.epochs)   # Updated from server
        """
        if not self._ctx:
            raise ValueError("FoundationalModel not connected to client")

        data = self._ctx.get_json(f"/compute/session/{self.id}")
        self._update_from_session(data)
        return data

    def is_ready(self) -> bool:
        """
        Check if this foundational model has finished training and is ready for use.

        Returns:
            True if training is complete, False otherwise

        Example:
            if fm.is_ready():
                predictor = fm.create_binary_classifier(target_column="target")
        """
        if not self._ctx:
            raise ValueError("FoundationalModel not connected to client")

        data = self._ctx.get_json(f"/compute/session/{self.id}")
        self._update_from_session(data)
        return self.status == 'done'

    def publish(
        self,
        name: Optional[str] = None,
        max_wait_time: int = 600,
        poll_interval: int = 5,
    ) -> Dict[str, Any]:
        """
        Publish this foundational model to the production directory and cloud storage.

        Published models are protected from garbage collection and available
        across all compute nodes via the shared backplane. The model is also
        backed up to cloud storage (DO Spaces).

        The model is published under your organization (derived from your API key).
        This dispatches a background job and polls until complete.

        The timeout is a *stall detector*, not a wall-clock limit — same
        contract as wait_for_training(). A publish copies the whole session
        to the backplane, uploads it to cloud storage, and writes the
        production deployment manifest; on the live fleet that routinely
        takes 7-25 minutes of real work (measured 2026-09-16 across
        taco/churro/burrito: 432s-1546s per publish task), and a node upgrade
        mid-publish re-delivers the task and starts it over. A fixed
        wall-clock cap failed healthy publishes that were still copying.
        The timer resets whenever the job reports progress (status, step,
        message, bytes/files copied change) and only fires when the job
        appears stuck.

        Transient poll failures (a sphere-api restart, a compute node
        upgrading, a 404 while the router re-locates the session) are ridden
        out rather than raised — they don't count as progress, so a publish
        that is genuinely unreachable still ends at max_wait_time.

        Args:
            name: Name for the published model (defaults to self.name)
            max_wait_time: Max seconds to wait *without progress* before
                raising TimeoutError (default 600)
            poll_interval: Seconds between status polls (default 5)

        Returns:
            dict with published_path, cloud_upload status, etc.

        Example:
            fm = featrix.create_foundational_model(name="my_model", data_file="data.csv")
            fm.wait_for_training()
            fm.publish(name="my_model_v1")
        """
        if not self._ctx:
            raise ValueError("FoundationalModel not connected to client")

        publish_name = name or self.name
        if not publish_name:
            raise ValueError("name is required (either pass it or set it on the model)")

        data = {
            "name": publish_name,
        }
        response = self._ctx.post_json(f"/compute/session/{self.id}/publish", data=data)

        # If already published, return immediately
        if response.get("status") == "already_published":
            self.deletion_protection = True
            return response

        # If the server returned a job_id, poll for completion
        job_id = response.get("job_id")
        if not job_id:
            # Old-style synchronous response (backwards compat)
            self.deletion_protection = True
            return response

        logger.info(f"Publishing model as '{publish_name}'... (job_id: {job_id})")

        start_time = time.time()
        last_progress_time = time.time()
        last_progress_key = None
        last_message = None
        last_poll_error: Optional[Exception] = None

        while time.time() - last_progress_time < max_wait_time:
            time.sleep(adaptive_poll_interval(poll_interval, start_time))

            try:
                status_response = self._ctx.get_json(
                    f"/compute/session/{self.id}/publish_job/{job_id}"
                )
            except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError,
                    requests.exceptions.Timeout, requests.exceptions.JSONDecodeError,
                    FeatrixPredictionError) as e:
                # A body cut off by a restarting sphere-api worker surfaces as
                # a JSONDecodeError; _make_request raises a server-detailed 500
                # as FeatrixPredictionError. Everything below 500 except 404
                # is a real client-side error and still raises immediately.
                status_code = getattr(e, "status_code", None) or getattr(
                    getattr(e, "response", None), "status_code", None)
                if status_code is not None and status_code != 404 and status_code < 500:
                    raise
                if last_poll_error is None:
                    logger.warning(
                        f"Publish status poll failed ({e}) — the job keeps running "
                        f"server-side; retrying (job_id: {job_id})"
                    )
                last_poll_error = e
                continue
            last_poll_error = None

            status = status_response.get("status")
            message = status_response.get("message", "")

            progress_key = tuple(
                status_response.get(k)
                for k in ("status", "step", "message", "bytes_copied", "files_copied", "progress_pct")
            )
            if progress_key != last_progress_key:
                last_progress_time = time.time()
                last_progress_key = progress_key

            # Show progress with ETA if available
            pct = status_response.get("progress_pct")
            eta = status_response.get("eta_minutes")
            if pct is not None:
                eta_str = f", ~{eta:.0f} min remaining" if eta and eta > 0.1 else ""
                progress_msg = f"  {message}{eta_str}"
            else:
                progress_msg = f"  {message}" if message else None

            if progress_msg and progress_msg != last_message:
                logger.info(progress_msg)
                last_message = progress_msg

            if status == "completed":
                logger.info(f"Published successfully: {status_response.get('published_path')}")
                self.deletion_protection = True
                return status_response

            elif status == "failed":
                error = status_response.get("error", "Unknown error")
                raise RuntimeError(f"Publish failed: {error}")

        last_error_note = f" Last poll error: {last_poll_error}." if last_poll_error is not None else ""
        raise TimeoutError(
            f"Publish stalled: no progress for {max_wait_time}s "
            f"(total elapsed: {int(time.time() - start_time)}s, job_id: {job_id}).{last_error_note} "
            f"The job may still be running — check status at /session/{self.id}/publish_job/{job_id}"
        )

    def deprecate(
        self,
        warning_message: str,
        expiration_date: str,
    ) -> Dict[str, Any]:
        """
        Deprecate this published model with a warning and expiration date.

        The model remains available until the expiration date. Prediction
        responses will include a model_expiration field warning consumers.

        Args:
            warning_message: Warning message to display
            expiration_date: ISO format date string (e.g., "2026-06-01T00:00:00Z")

        Returns:
            dict with deprecation status

        Example:
            from datetime import datetime, timedelta
            expiration = (datetime.now() + timedelta(days=90)).isoformat() + "Z"
            fm.deprecate(
                warning_message="Replaced by v2. Migrate by expiration.",
                expiration_date=expiration
            )
        """
        if not self._ctx:
            raise ValueError("FoundationalModel not connected to client")

        data = {
            "warning_message": warning_message,
            "expiration_date": expiration_date,
        }
        return self._ctx.post_json(f"/compute/session/{self.id}/deprecate", data=data)

    def unpublish(self) -> Dict[str, Any]:
        """
        Unpublish this model, moving it back from the published directory.

        Note: publish() automatically turns on deletion_protection, and
        unpublish() does NOT turn it back off — the model remains immune to
        garbage collection until you explicitly call
        set_deletion_protection(False).

        Returns:
            dict with unpublish status

        Example:
            fm.unpublish()
        """
        if not self._ctx:
            raise ValueError("FoundationalModel not connected to client")

        return self._ctx.post_json(f"/compute/session/{self.id}/unpublish", data={})

    def set_deletion_protection(self, protected: bool) -> Dict[str, Any]:
        """
        Turn deletion protection on or off for this model.

        While protected, delete() is refused (and the GC daemon skips this
        session) until you explicitly call set_deletion_protection(False).
        publish() turns this on automatically; unpublish() does not turn it
        back off.

        Args:
            protected: True to protect against deletion/GC, False to allow it

        Returns:
            dict with the updated deletion_protection status

        Example:
            fm.set_deletion_protection(True)
        """
        if not self._ctx:
            raise ValueError("FoundationalModel not connected to client")

        result = self._ctx.post_json(
            f"/compute/session/{self.id}/deletion_protection",
            data={"protected": protected},
        )
        self.deletion_protection = protected
        return result

    def delete(self) -> Dict[str, Any]:
        """
        Mark this model for deletion.

        The session will be picked up by the garbage collection process
        and deleted from the compute node. Raises if deletion_protection is
        on (for this model or any child predictor) — call
        set_deletion_protection(False) first.

        Returns:
            dict with deletion confirmation

        Example:
            fm.delete()
        """
        if not self._ctx:
            raise ValueError("FoundationalModel not connected to client")

        return self._ctx.post_json(f"/compute/session/{self.id}/mark_for_deletion", data={})

    def cancel(self, reason: Optional[str] = None) -> Dict[str, Any]:
        """
        Cancel training for this foundational model.

        If the job hasn't been dispatched to a compute node yet, it's
        cancelled immediately. If it's already training, cancellation is
        cooperative — the training loop notices at its next checkpoint
        (roughly every 10 batches), not instantly. A subsequent
        wait_for_training() call returns normally with status='cancelled'
        rather than raising.

        Args:
            reason: Optional human-readable reason, stored for audit purposes

        Returns:
            dict with cancellation status — includes 'cancelled' (bool) and
            'status' (the job's status after the call: 'cancelled' if it was
            still queued, or the pre-existing status if the job had already
            reached a terminal state)

        Example:
            fm.cancel(reason="duplicate of an earlier run")
        """
        if not self._ctx:
            raise ValueError("FoundationalModel not connected to client")

        data: Dict[str, Any] = {}
        if reason:
            data["reason"] = reason

        return self._ctx.post_json(f"/compute/session/{self.id}/cancel", data=data)

    def publish_checkpoint(
        self,
        name: str,
        org_id: Optional[str] = None,
        checkpoint_epoch: Optional[int] = None,
        session_name_prefix: Optional[str] = None,
        publish: bool = True,
    ) -> 'FoundationalModel':
        """
        Publish a checkpoint from this model's training as a new foundation model.

        Creates a NEW FoundationalModel from a training checkpoint with full
        provenance tracking. Useful for snapshotting good intermediate models
        while training continues.

        Args:
            name: Name for the new foundation model (required)
            org_id: Organization ID (required if publish=True)
            checkpoint_epoch: Which epoch checkpoint to use (None = best/latest)
            session_name_prefix: Optional prefix for the new session ID
            publish: Move to published directory (default: True)

        Returns:
            New FoundationalModel instance for the published checkpoint

        Example:
            # Snapshot epoch 50 while training continues
            checkpoint_fm = fm.publish_checkpoint(
                name="My Model v0.5",
                org_id="my_org",
                checkpoint_epoch=50
            )
            # Use immediately
            predictor = checkpoint_fm.create_binary_classifier(target_column="target")
        """
        if not self._ctx:
            raise ValueError("FoundationalModel not connected to client")

        if publish and not org_id:
            raise ValueError("org_id is required when publish=True")

        data = {
            "name": name,
            "publish": publish,
        }
        if checkpoint_epoch is not None:
            data["checkpoint_epoch"] = checkpoint_epoch
        if session_name_prefix:
            data["session_name_prefix"] = session_name_prefix
        if org_id:
            data["org_id"] = org_id

        response = self._ctx.post_json(
            f"/compute/session/{self.id}/publish_partial_foundation",
            data=data
        )

        new_fm = FoundationalModel(
            id=response.get("foundation_session_id", ""),
            name=name,
            status="done",
            epochs=response.get("checkpoint_epoch"),
            created_at=datetime.now(),
            _ctx=self._ctx,
        )

        return new_fm

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            'id': self.id,
            'name': self.name,
            'status': self.status,
            'es_status': self.es_status,
            'sp_status': self.sp_status,
            'dimensions': self.dimensions,
            'epochs': self.epochs,
            'final_loss': self.final_loss,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'session_type': self.session_type,
            'compute_cluster': self.compute_cluster,
            'error_message': self.error_message,
            'training_progress': self.training_progress,
            'user_metadata': self.user_metadata,
            'deletion_protection': self.deletion_protection,
        }

    def __repr__(self) -> str:
        name_str = f", name='{self.name}'" if self.name else ""
        status_str = f", status='{self.status}'" if self.status else ""
        dims_str = f", dims={self.dimensions}" if self.dimensions else ""
        return f"FoundationalModel(id='{self.id}'{name_str}{status_str}{dims_str})"
