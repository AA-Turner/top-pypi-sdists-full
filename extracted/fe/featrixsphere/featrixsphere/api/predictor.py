#  -*- coding: utf-8 -*-
#
#  Copyright (c) 2023-2026 Featrix, Inc, All Rights Reserved
#
#  Proprietary and Confidential.  Unauthorized use, copying or dissemination
#  of these materials is strictly prohibited.
#

"""
Predictor class for FeatrixSphere API.

Represents a trained predictor (classifier or regressor).
"""

import gc
import time
import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, Optional, List, Union, TYPE_CHECKING

if TYPE_CHECKING:
    from .http_client import ClientContext
    from .foundational_model import FoundationalModel
    from .prediction_grid import PredictionGrid
    import pandas as pd

from .http_client import TRAINING_IN_PROGRESS_STATUSES, customer_metadata_headers
from .prediction_result import PredictionResult
from .api_endpoint import APIEndpoint
from .exceptions import TrainingStatusUnavailableError, SessionNotFoundError
from .poll_utils import adaptive_poll_interval, job_awaiting_start

# A single poll reading status='failed' can be a transient/racy read — require
# this many consecutive confirming reads before treating it as a real terminal
# failure. A non-failed read in between resets the counter. See the matching
# constant/comment in foundational_model.py for the full rationale.
_FAILED_STATUS_CONFIRM_READS = 3

# A single 404 from /compute/session/{id} can also be a transient/racy read —
# require this many consecutive 404s before treating "not found" as
# confirmed-permanent. A non-404 read in between resets the counter. See the
# matching constant/comment in foundational_model.py for the full rationale
# (SP jobs are, if anything, more exposed to this race than ES jobs: an SP
# job is pinned to the specific node holding the session's embedding_space
# file, so it can't be "found" anywhere else while it sits in the gap between
# leaving Supabase's pending queue and that node registering it locally).
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
# matching constant/comment in foundational_model.py.
_POLL_FAILURE_MAX_SECONDS = 2 * 60 * 60


def _extract_training_status_from_body(response: Any) -> Optional[Dict[str, Any]]:
    """If the API body is a soft-503 training-in-progress payload, return a normalized detail dict.

    Server payload shape (from `model_card_repair.get_predictor_status`):
        {
          "status": "training_in_progress_no_checkpoint",
          "message": "...",
          "training_info": {"epoch": 5, "total_epochs": 50, "progress_percent": 10,
                            "is_training": True, "checkpoint_path": "..."},
          ...
        }

    We flatten `training_info` to top-level so callers can read fields like
    `is_training`, `current_epoch`, `total_epochs`, `progress_percent`,
    `checkpoint_epoch` directly.
    """
    if not isinstance(response, dict):
        return None
    # Documented shape has the status fields at the top level (see docstring
    # example above). Also check the legacy `detail`-nested shape for compute
    # nodes mid-rollout of the api.py fix.
    if response.get('status') in TRAINING_IN_PROGRESS_STATUSES:
        detail = response
    else:
        detail = response.get('detail')
        if not (isinstance(detail, dict) and detail.get('status') in TRAINING_IN_PROGRESS_STATUSES):
            return None

    info = detail.get('training_info') or {}
    checkpoint_path = info.get('checkpoint_path')
    checkpoint_epoch = None
    if checkpoint_path:
        # Filename format: ..._epoch_{N}.featrix-model
        import re
        m = re.search(r'_epoch_(\d+)\.', str(checkpoint_path))
        if m:
            checkpoint_epoch = int(m.group(1))

    return {
        "status": detail.get('status'),
        "message": detail.get('message'),
        "is_training": bool(info.get('is_training', True)),
        "current_epoch": info.get('epoch', 0),
        "total_epochs": info.get('total_epochs'),
        "progress_percent": info.get('progress_percent', 0),
        "checkpoint_path": checkpoint_path,
        "checkpoint_epoch": checkpoint_epoch,
        "raw": detail,
    }

def _parse_datetime(value) -> Optional[datetime]:
    """Parse a datetime from ISO string or return as-is if already datetime."""
    if value is None:
        return None
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        try:
            return datetime.fromisoformat(value.replace('Z', '+00:00'))
        except (ValueError, AttributeError):
            return None
    return None


logger = logging.getLogger(__name__)


@dataclass
class Predictor:
    """
    Represents a trained predictor (classifier or regressor).

    Attributes:
        id: Predictor ID
        name: Predictor name
        target_column: Target column name
        target_type: Target type ("set", "numeric", "binary")
        status: Training status ("training", "done", "error")
        session_id: Parent session ID
        accuracy: Training accuracy (if available)
        created_at: Creation timestamp

    Usage:
        # Create from foundational model
        predictor = fm.create_binary_classifier(
            name="churn_predictor",
            target_column="churned"
        )

        # Wait for training
        predictor.wait_for_training()

        # Make prediction
        result = predictor.predict({"age": 35, "income": 50000})
        print(result.predicted_class)
        print(result.confidence)

        # Batch predictions
        results = predictor.batch_predict([
            {"age": 35, "income": 50000},
            {"age": 42, "income": 75000}
        ])
    """

    id: str
    session_id: str
    target_column: str
    target_type: str = "set"
    name: Optional[str] = None
    status: Optional[str] = None
    accuracy: Optional[float] = None
    auc: Optional[float] = None
    f1: Optional[float] = None
    created_at: Optional[datetime] = None
    deletion_protection: bool = False

    # Internal
    _ctx: Optional['ClientContext'] = field(default=None, repr=False)
    _foundational_model: Optional['FoundationalModel'] = field(default=None, repr=False)

    @classmethod
    def from_response(
        cls,
        response: Dict[str, Any],
        session_id: str,
        ctx: Optional['ClientContext'] = None,
        foundational_model: Optional['FoundationalModel'] = None
    ) -> 'Predictor':
        """Create Predictor from API response."""
        return cls(
            id=response.get('predictor_id') or response.get('id', ''),
            session_id=session_id,
            target_column=response.get('target_column', ''),
            target_type=response.get('target_type') or response.get('target_column_type', 'set'),
            name=response.get('name'),
            status=response.get('status'),
            accuracy=response.get('accuracy'),
            auc=response.get('auc') or response.get('roc_auc'),
            f1=response.get('f1') or response.get('f1_score'),
            created_at=_parse_datetime(response.get('created_at')),
            deletion_protection=bool(response.get('deletion_protection', False)),
            _ctx=ctx,
            _foundational_model=foundational_model,
        )

    @property
    def foundational_model(self) -> Optional['FoundationalModel']:
        """Get the parent foundational model."""
        return self._foundational_model

    def predict(
        self,
        record: Dict[str, Any],
        best_metric_preference: Optional[str] = None,
        feature_importance: bool = False,
        generate: bool = False,
        customer_metadata: Optional[Dict[str, Any]] = None,
    ) -> PredictionResult:
        """
        Make a single prediction.

        Args:
            record: Input record dictionary
            best_metric_preference: Metric checkpoint to use ("roc_auc", "pr_auc", or None)
            feature_importance: If True, compute feature importance via leave-one-out ablation
            generate: Generative-string predictors only (see
                create_generative_string_model). False (default): return the
                nearest training row's value — fast, free, deterministic.
                True: few-shot an LLM with the nearest training rows for a
                non-verbatim answer — slower, costs an LLM call,
                non-deterministic. Ignored for every other predictor type.
            customer_metadata: Optional dict of your own ids/labels stored
                with the prediction for tracing it back later -- never sent
                to the model.

        Returns:
            PredictionResult with prediction, confidence, and prediction_uuid.
            If feature_importance=True, also includes feature_importance dict.

        Example:
            result = predictor.predict({"age": 35, "income": 50000})
            print(result.predicted_class)  # "churned"
            print(result.confidence)       # 0.87
            print(result.prediction_uuid)  # UUID for feedback

            # With feature importance
            result = predictor.predict(record, feature_importance=True)
            print(result.feature_importance)  # {"income": 0.15, "age": 0.08, ...}
        """
        if not self._ctx:
            raise ValueError("Predictor not connected to client")

        # Clean the record
        cleaned_record = self._clean_record(record)

        if feature_importance:
            # Build N+1 records: original + each feature nulled out
            columns = list(cleaned_record.keys())
            batch = [cleaned_record]  # Original first

            for col in columns:
                ablated = cleaned_record.copy()
                ablated[col] = None
                batch.append(ablated)

            # Single batch call
            results = self.batch_predict(
                batch,
                show_progress=False,
                best_metric_preference=best_metric_preference
            )

            # Compare: importance = |original_confidence - ablated_confidence|
            original = results[0]
            importance = {}
            original_conf = original.confidence or 0.0

            for i, col in enumerate(columns):
                ablated_result = results[i + 1]
                ablated_conf = ablated_result.confidence or 0.0
                # Higher delta = more important
                delta = abs(original_conf - ablated_conf)
                importance[col] = round(delta, 4)

            # Sort by importance (highest first)
            original.feature_importance = dict(sorted(
                importance.items(),
                key=lambda x: x[1],
                reverse=True
            ))
            return original

        # Standard single prediction
        request_payload = {
            "query_record": cleaned_record,
            "predictor_id": self.id,
        }
        if best_metric_preference:
            request_payload["best_metric_preference"] = best_metric_preference
        if generate:
            request_payload["generate"] = True

        # Make request
        response = self._ctx.post_json(
            f"/session/{self.session_id}/predict",
            data=request_payload,
            headers=customer_metadata_headers(customer_metadata),
        )

        training_status = _extract_training_status_from_body(response)
        if training_status is not None:
            return PredictionResult(
                query_record=cleaned_record,
                predictor_id=self.id,
                session_id=self.session_id,
                target_column=self.target_column,
                timestamp=datetime.now(),
                training_status=training_status,
                _ctx=self._ctx,
            )

        return PredictionResult.from_response(
            response, cleaned_record, self._ctx,
            predictor_id=self.id, session_id=self.session_id,
        )

    def batch_predict(
        self,
        records: Union[List[Dict[str, Any]], 'pd.DataFrame'],
        show_progress: bool = True,
        best_metric_preference: Optional[str] = None,
        generate: bool = False,
    ) -> List[PredictionResult]:
        """
        Make batch predictions.

        Args:
            records: List of record dictionaries or DataFrame
            show_progress: Show progress bar
            best_metric_preference: Metric checkpoint to use
            generate: Generative-string predictors only — see
                Predictor.predict()'s ``generate`` parameter. Ignored for
                every other predictor type.

        Returns:
            List of PredictionResult objects
        """
        if not self._ctx:
            raise ValueError("Predictor not connected to client")

        # Convert DataFrame to list of dicts if needed
        if hasattr(records, 'to_dict'):
            records = records.to_dict('records')

        # Clean records
        cleaned_records = [self._clean_record(r) for r in records]

        # Build request
        request_payload = {
            "records": cleaned_records,
            "predictor_id": self.id,
        }
        if best_metric_preference:
            request_payload["best_metric_preference"] = best_metric_preference
        if generate:
            request_payload["generate"] = True

        # Make request using predict_table endpoint
        response = self._ctx.post_json(
            f"/session/{self.session_id}/predict_table",
            data=request_payload
        )

        training_status = _extract_training_status_from_body(response)
        if training_status is not None:
            now = datetime.now()
            return [
                PredictionResult(
                    query_record=record,
                    predictor_id=self.id,
                    session_id=self.session_id,
                    target_column=self.target_column,
                    timestamp=now,
                    training_status=training_status,
                    _ctx=self._ctx,
                )
                for record in cleaned_records
            ]

        # Parse results
        results = []
        predictions = response.get('predictions', [])

        for i, pred in enumerate(predictions):
            record = cleaned_records[i] if i < len(cleaned_records) else {}
            results.append(PredictionResult.from_response(
                pred, record, self._ctx,
                predictor_id=self.id, session_id=self.session_id,
            ))

        return results

    def evaluate(
        self,
        records: Union[List[Dict[str, Any]], 'pd.DataFrame'],
        labels: Union[List[Any], str],
    ) -> Dict[str, Any]:
        """Score this predictor on labeled holdout data.

        Runs predictions on the server and scores them against your true
        labels, returning a metrics dict. Scoring happens where the model
        lives (the prediction server calls the SP's own metric code), so the
        positive class and all conventions match what the model reports —
        you don't reimplement metrics client-side.

        Args:
            records: list of feature dicts, or a pandas DataFrame. If a
                DataFrame is given and ``labels`` is a column name (str), that
                column is used as the ground truth and dropped from features.
            labels: list of ground-truth labels (one per record), OR — when
                ``records`` is a DataFrame — the name of the truth column.

        Returns:
            Metrics dict. Classification: ``accuracy``, ``f1``, ``auc``
            (plus ``f1_error``/``auc_error`` if the positive class can't be
            resolved). Regression: ``r2``, ``rmse``, ``mae``.

        Example:
            metrics = predictor.evaluate(holdout_df, labels="churned")
            print(metrics["auc"], metrics["f1"])

            # Or explicit records + labels
            metrics = predictor.evaluate(
                records=[{"age": 35, ...}, {"age": 22, ...}],
                labels=["yes", "no"],
            )
        """
        if not self._ctx:
            raise ValueError("Predictor not connected to client")

        # DataFrame ergonomics: allow labels to name a column in the frame.
        if hasattr(records, "to_dict"):
            if isinstance(labels, str):
                if labels not in records.columns:
                    raise ValueError(
                        f"labels column '{labels}' not found in DataFrame columns"
                    )
                label_list = records[labels].tolist()
                record_list = records.drop(columns=[labels]).to_dict("records")
            else:
                label_list = list(labels)
                record_list = records.to_dict("records")
        else:
            if isinstance(labels, str):
                raise ValueError(
                    "labels was given as a column name (str) but records is not "
                    "a DataFrame — pass labels as a list of ground-truth values"
                )
            record_list = list(records)
            label_list = list(labels)

        if len(record_list) != len(label_list):
            raise ValueError(
                f"records ({len(record_list)}) and labels ({len(label_list)}) "
                f"must be the same length"
            )
        if not record_list:
            raise ValueError("evaluate() called with no records")

        cleaned_records = [self._clean_record(r) for r in record_list]

        request_payload = {
            "records": cleaned_records,
            "labels": label_list,
            "predictor_id": self.id,
        }
        response = self._ctx.post_json(
            f"/session/{self.session_id}/evaluate",
            data=request_payload,
        )
        return response.get("metrics", {})

    def predict_grid(
        self,
        degrees_of_freedom: int,
        grid_shape: tuple = None,
    ) -> 'PredictionGrid':
        """
        Create a prediction grid for exploring parameter surfaces with visualization.

        Supports 1D curves, 2D heatmaps, and 3D surfaces with built-in plotting.

        Args:
            degrees_of_freedom: Number of dimensions (1, 2, or 3)
            grid_shape: Custom grid shape tuple (default: auto-sized)

        Returns:
            PredictionGrid object with predict() and plotting methods

        Example:
            grid = predictor.predict_grid(degrees_of_freedom=2, grid_shape=(10, 8))
            grid.set_axis_labels(["Spend", "Campaign Type"])
            grid.set_axis_values(0, [100, 250, 500])
            grid.set_axis_values(1, ["search", "display", "social"])

            for i, spend in enumerate([100, 250, 500]):
                for j, campaign in enumerate(["search", "display", "social"]):
                    grid.predict({"spend": spend, "campaign_type": campaign}, grid_position=(i, j))

            grid.process_batch()
            grid.plot_heatmap()
        """
        from .prediction_grid import PredictionGrid
        return PredictionGrid(predictor=self, degrees_of_freedom=degrees_of_freedom, grid_shape=grid_shape)

    def predict_csv_file(
        self,
        csv_path: str,
        show_progress: bool = True,
        best_metric_preference: Optional[str] = None
    ) -> List[PredictionResult]:
        """
        Load a CSV file and run batch predictions on all rows.

        Args:
            csv_path: Path to the CSV file
            show_progress: Show progress bar
            best_metric_preference: Metric checkpoint to use

        Returns:
            List of PredictionResult objects

        Example:
            results = predictor.predict_csv_file("test_data.csv")
            for r in results:
                print(r.predicted_class, r.confidence)
        """
        import pandas as pd
        df = pd.read_csv(csv_path)
        return self.batch_predict(
            df,
            show_progress=show_progress,
            best_metric_preference=best_metric_preference
        )

    def explain(
        self,
        record: Dict[str, Any],
        class_idx: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Explain a prediction using gradient attribution.

        Args:
            record: Input record to explain
            class_idx: Class index to explain (for multi-class)

        Returns:
            Explanation dictionary with feature attributions
        """
        if not self._ctx:
            raise ValueError("Predictor not connected to client")

        cleaned_record = self._clean_record(record)

        request_payload = {
            "query_record": cleaned_record,
            "predictor_id": self.id,
        }
        if class_idx is not None:
            request_payload["class_idx"] = class_idx

        return self._ctx.post_json(
            f"/session/{self.session_id}/explain",
            data=request_payload
        )

    def get_columns(self) -> List[str]:
        """
        Get column names for this predictor's embedding space.

        Reads from Supabase when available (no compute node needed).
        Falls back to the compute node if Supabase metadata isn't populated.

        Returns:
            List of column names the model was trained on.

        Example:
            columns = predictor.get_columns()
            print(f"Model uses {len(columns)} features: {columns[:5]}...")
        """
        if not self._ctx:
            raise ValueError("Predictor not connected to client")

        # Try Supabase first (no compute node needed)
        try:
            data = self._ctx.get_json(f"/compute/predictor/{self.id}/columns")
            columns = data.get('columns', [])
            if columns:
                if isinstance(columns[0], dict):
                    return [c['name'] for c in columns]
                return columns
        except Exception:
            pass  # Fall through to compute node

        # Fall back to compute node
        data = self._ctx.get_json(f"/compute/session/{self.session_id}/columns")
        return data.get('columns', [])

    def wait_for_training(
        self,
        max_wait_time: int = 3600,
        poll_interval: int = 10,
        show_progress: bool = True
    ) -> 'Predictor':
        """
        Wait for predictor training to complete.

        The timeout is a *stall detector*, not a wall-clock limit. Training
        can run as long as progress is being made (status change, epoch tick,
        or progress fraction advancing). The timer resets on every sign of
        progress and only fires when the job appears genuinely stuck.

        Args:
            max_wait_time: Maximum time in seconds to wait *without progress*
                before raising TimeoutError (default 3600 = 1 hour)
            poll_interval: Polling interval in seconds
            show_progress: Print progress updates

        Returns:
            Self (updated with final status)

        Raises:
            TimeoutError: If no progress is detected for max_wait_time seconds
            RuntimeError: If training fails
        """
        if not self._ctx:
            raise ValueError("Predictor not connected to client")

        start_time = time.time()
        last_progress_time = time.time()
        last_gc_time = time.time()
        last_heartbeat_time = time.time()
        last_status = None
        last_epoch = None
        last_progress_fraction = None
        consecutive_errors = 0
        first_error_time: Optional[float] = None
        consecutive_failed_reads = 0
        consecutive_not_found = 0
        heartbeat_interval = 60  # emit a liveness line at least this often

        while True:
            # Stall detection: timeout only when no progress is made
            stall_seconds = time.time() - last_progress_time
            if stall_seconds > max_wait_time:
                elapsed = int(time.time() - start_time)
                raise TimeoutError(
                    f"Predictor training stalled: no progress for {int(stall_seconds)}s "
                    f"(total elapsed: {elapsed}s). The job may still be running "
                    f"on the server — check session {self.session_id}"
                )

            # Get session status — tolerate transient failures
            try:
                response_data = self._ctx.get_json(f"/compute/session/{self.session_id}")
                consecutive_errors = 0
                first_error_time = None
                consecutive_not_found = 0
            except Exception as e:
                # A 404 can be a transient registration-gap race, not just a
                # confirmed-gone session — see _NOT_FOUND_CONFIRM_READS and the
                # matching comment in foundational_model.py's _wait_with_tqdm
                # for the full rationale.
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
                    raise SessionNotFoundError(session_id=self.session_id)

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
                        session_id=self.session_id,
                        message=(
                            f"Predictor training: lost contact with server after "
                            f"{consecutive_errors} consecutive poll failures over "
                            f"{elapsed}s. Last error: {e}. The job may still be "
                            f"running server-side — check status independently "
                            f"before relaunching."
                        ),
                    )
                time.sleep(adaptive_poll_interval(poll_interval, start_time))
                continue

            # Extract only scalar values we need, then free the response
            status = None
            error_msg = None
            current_epoch = None
            progress_fraction = None
            awaiting_start = False
            for job_id, job in response_data.get('jobs', {}).items():
                if job.get('job_type') == 'train_single_predictor':
                    # The live job registry entry (this dict) does NOT carry
                    # target_column/job_spec once a train_single_predictor job
                    # is actually dispatched -- only the pre-dispatch
                    # session.job_plan entries do (see
                    # FoundationalModel._wait_for_predictor_id's job_plan
                    # merge for the same gap). Requiring an exact match here
                    # unconditionally meant this loop could NEVER find the
                    # real, running job once it replaced any earlier
                    # placeholder entry: status silently froze at whatever it
                    # last was (often "ready"), the stall timer kept ticking
                    # with no progress ever seen again, and the job would
                    # then finish successfully server-side ~15 min later
                    # while wait_for_training kept "waiting" for another 75+
                    # minutes before finally raising TimeoutError (2026-09-14
                    # incident, session e2e-pipeline-smoke-35ed737d...).
                    # Treat a missing target_column as "can't disambiguate,
                    # match on job_type alone" instead of "never matches" --
                    # still disambiguates correctly on the rare job dict that
                    # DOES carry target_column (e.g. multiple concurrent
                    # targets on one session).
                    job_target = job.get('target_column') or job.get('job_spec', {}).get('target_column')
                    if not job_target or job_target == self.target_column:
                        status = job.get('status', 'unknown')
                        current_epoch = job.get('current_epoch') or job.get('epoch')
                        progress_fraction = job.get('progress')
                        awaiting_start = job_awaiting_start(job)
                        if status in ('failed', 'error'):
                            error_msg = job.get('error', 'Unknown error')
                        break

            # Free the response dict immediately — don't hold across sleep()
            del response_data

            # A non-failed read means an earlier 'failed' reading (if any) was
            # transient/unconfirmed — reset the confirmation counter.
            if status != 'failed':
                consecutive_failed_reads = 0

            if awaiting_start:
                # Held for a GPU training slot / not picked up yet (see
                # poll_utils.job_awaiting_start): queue wait, not a stall.
                last_progress_time = time.time()

            if status is not None:
                # Reset stall timer on any sign of progress: status change,
                # epoch tick, or the smooth 0..1 progress fraction advancing
                # (it ticks per-batch server-side). A long-running SP job can
                # sit in a single 'training' status for its entire runtime —
                # keying the stall timer off status alone (as before) meant a
                # perfectly healthy multi-hour fine-tune run got killed as
                # "stalled" the moment it exceeded max_wait_time, even though
                # epochs were visibly completing. Mirrors the epoch-aware
                # reset logic in FoundationalModel's waiter.
                fraction_advanced = (
                    isinstance(progress_fraction, (int, float))
                    and (last_progress_fraction is None or progress_fraction > last_progress_fraction + 1e-6)
                )
                status_changed = status != last_status
                epoch_changed = current_epoch != last_epoch
                if status_changed or epoch_changed or fraction_advanced:
                    last_progress_time = time.time()
                    if isinstance(progress_fraction, (int, float)):
                        last_progress_fraction = progress_fraction
                    last_epoch = current_epoch
                    if show_progress and status_changed:
                        elapsed = int(time.time() - start_time)
                        print(f"[{elapsed}s] Predictor training: {status}")
                        last_heartbeat_time = time.time()
                    elif show_progress and (epoch_changed or fraction_advanced) and (time.time() - last_heartbeat_time) >= heartbeat_interval:
                        elapsed = int(time.time() - start_time)
                        epoch_str = f", epoch {current_epoch}" if current_epoch is not None else ""
                        print(f"[{elapsed}s] Predictor training: {status}{epoch_str} (still running)")
                        last_heartbeat_time = time.time()
                    # Track outside the show_progress guard so stall detection
                    # (which keys off last_status) works even when progress is
                    # not being printed.
                    last_status = status
                elif show_progress and (time.time() - last_heartbeat_time) >= heartbeat_interval:
                    # A long unchanged 'training' status must not leave stdout
                    # silent for minutes — that trips the QA runner's idle
                    # timeout (killed as a false "timeout") and hides liveness
                    # from the user. Emit a periodic heartbeat.
                    elapsed = int(time.time() - start_time)
                    print(f"[{elapsed}s] Predictor training: {status} (still running)")
                    last_heartbeat_time = time.time()

                if status == 'done':
                    self.status = 'done'
                    self._update_metrics()
                    if show_progress:
                        print(f"Predictor training complete!")
                        if self.accuracy:
                            print(f"  Accuracy: {self.accuracy:.4f}")
                        if self.auc:
                            print(f"  AUC: {self.auc:.4f}")
                    return self

                elif status == 'cancelled':
                    # A caller cancelling their own job mid-wait shouldn't see
                    # that reported as a training failure. CANCELLED is a
                    # terminal status in job_manager, so unlike 'failed' this
                    # needs no re-poll confirmation.
                    self.status = 'cancelled'
                    if show_progress:
                        elapsed = int(time.time() - start_time)
                        print(f"[{elapsed}s] 🚫 Predictor training cancelled")
                    return self

                elif status == 'failed':
                    consecutive_failed_reads += 1
                    if consecutive_failed_reads < _FAILED_STATUS_CONFIRM_READS:
                        # Don't trust a single 'failed' read — re-poll to confirm
                        # before raising, in case it's a transient/racy status.
                        if show_progress:
                            elapsed = int(time.time() - start_time)
                            print(
                                f"[{elapsed}s] Predictor training: status read as 'failed' "
                                f"(unconfirmed {consecutive_failed_reads}/{_FAILED_STATUS_CONFIRM_READS}) — re-checking..."
                            )
                        time.sleep(adaptive_poll_interval(poll_interval, start_time))
                        continue

                    self.status = 'error'
                    raise RuntimeError(f"Predictor training failed: {error_msg}")

            # Periodic gc to combat pymalloc arena fragmentation
            now = time.time()
            if now - last_gc_time > 60:
                gc.collect()
                last_gc_time = now

            time.sleep(adaptive_poll_interval(poll_interval, start_time))

    def train_more(
        self,
        epochs: int = 50,
        **kwargs
    ) -> 'Predictor':
        """
        Continue training the predictor.

        Args:
            epochs: Additional epochs to train
            **kwargs: Additional training parameters

        Returns:
            Self (training started)
        """
        if not self._ctx:
            raise ValueError("Predictor not connected to client")

        data = {
            "epochs": epochs,
            "target_column": self.target_column,
            **kwargs
        }

        self._ctx.post_json(
            f"/compute/session/{self.session_id}/train_predictor_more",
            data=data
        )

        self.status = "training"
        return self

    def cancel(self, reason: Optional[str] = None) -> Dict[str, Any]:
        """
        Cancel training for this predictor.

        If the job hasn't been dispatched to a compute node yet, it's
        cancelled immediately. If it's already training, cancellation is
        cooperative — the training loop notices at its next checkpoint
        (roughly every 10 batches or at the start of the next epoch), not
        instantly. A subsequent wait_for_training() call returns normally
        with status='cancelled' rather than raising.

        Note: this cancels the most recent job on the predictor's parent
        session — if that session has a newer job in flight (e.g. another
        train_more() call), that's what gets cancelled.

        Args:
            reason: Optional human-readable reason, stored for audit purposes

        Returns:
            dict with cancellation status — includes 'cancelled' (bool) and
            'status' (the job's status after the call)

        Example:
            predictor.cancel(reason="wrong target column")
        """
        if not self._ctx:
            raise ValueError("Predictor not connected to client")

        data: Dict[str, Any] = {}
        if reason:
            data["reason"] = reason

        return self._ctx.post_json(f"/compute/session/{self.session_id}/cancel", data=data)

    def set_deletion_protection(self, protected: bool) -> Dict[str, Any]:
        """
        Turn deletion protection on or off for this predictor.

        SPs have no independent delete path — they're reaped only when their
        parent foundational model is deleted — so this only blocks the
        *parent* model's delete() while set True. Unprotect it (or protect
        no predictors on the session) to allow the parent to be deleted.

        Args:
            protected: True to protect against deletion/GC, False to allow it

        Returns:
            dict with the updated deletion_protection status

        Example:
            predictor.set_deletion_protection(True)
        """
        if not self._ctx:
            raise ValueError("Predictor not connected to client")

        result = self._ctx.post_json(
            f"/compute/session/{self.session_id}/predictor/{self.id}/deletion_protection",
            data={"protected": protected},
        )
        self.deletion_protection = protected
        return result

    def create_api_endpoint(
        self,
        name: str,
        api_key: Optional[str] = None,
        description: Optional[str] = None
    ) -> APIEndpoint:
        """
        Create a named API endpoint served by this predictor.

        Args:
            name: Endpoint name
            api_key: API key (if None, auto-generate)
            description: Endpoint description

        Returns:
            APIEndpoint -- its `api_key` is shown only here.

        Example:
            endpoint = predictor.create_api_endpoint(
                name="production_api",
                description="Production endpoint"
            )
            print(f"API Key: {endpoint.api_key}")
        """
        if not self._ctx:
            raise ValueError("Predictor not connected to client")

        # session_id lets the server publish this predictor if it isn't yet
        # -- the endpoint then answers once that publish lands.
        data = {
            "name": name,
            "predictor_id": self.id,
            "session_id": self.session_id,
        }
        if api_key:
            data["api_key"] = api_key
        if description:
            data["description"] = description

        # Sent once: a retry after a lost response would create a second endpoint.
        response = self._ctx.post_json("/endpoints", data=data, max_retries=1)
        return APIEndpoint.from_response(response, ctx=self._ctx)

    def configure_webhooks(
        self,
        training_finished: Optional[str] = None,
        training_started: Optional[str] = None,
        alert_drift: Optional[str] = None,
        alert_performance_degradation: Optional[str] = None,
        alert_error_rate: Optional[str] = None,
        alert_quota_threshold: Optional[str] = None,
        prediction_error: Optional[str] = None,
        usage: Optional[str] = None,
        batch_job_completed: Optional[str] = None,
        webhook_secret: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Configure webhooks for various predictor events.

        Args:
            training_finished: URL for training completion webhook
            training_started: URL for training start webhook
            alert_drift: URL for data drift alerts
            alert_performance_degradation: URL for performance alerts
            alert_error_rate: URL for error rate alerts
            alert_quota_threshold: URL for quota threshold alerts
            prediction_error: URL for prediction error webhook
            usage: URL for usage statistics (can be spammy!)
            batch_job_completed: URL for batch job completion
            webhook_secret: Secret for webhook verification

        Returns:
            Current webhook configuration

        Example:
            predictor.configure_webhooks(
                training_finished="https://api.example.com/webhooks/training",
                alert_drift="https://api.example.com/webhooks/drift",
                webhook_secret="my_secret_key"
            )
        """
        if not self._ctx:
            raise ValueError("Predictor not connected to client")

        webhooks = {}
        if training_finished:
            webhooks["training_finished"] = training_finished
        if training_started:
            webhooks["training_started"] = training_started
        if alert_drift:
            webhooks["alert_drift"] = alert_drift
        if alert_performance_degradation:
            webhooks["alert_performance_degradation"] = alert_performance_degradation
        if alert_error_rate:
            webhooks["alert_error_rate"] = alert_error_rate
        if alert_quota_threshold:
            webhooks["alert_quota_threshold"] = alert_quota_threshold
        if prediction_error:
            webhooks["prediction_error"] = prediction_error
        if usage:
            webhooks["usage"] = usage
        if batch_job_completed:
            webhooks["batch_job_completed"] = batch_job_completed
        if webhook_secret:
            webhooks["webhook_secret"] = webhook_secret

        response = self._ctx.post_json(
            f"/session/{self.session_id}/configure_webhooks",
            data={"webhooks": webhooks, "predictor_id": self.id}
        )

        return response.get('webhooks', webhooks)

    def get_webhooks(self) -> Dict[str, str]:
        """
        Get current webhook configuration.

        Returns:
            Dictionary of webhook event types to URLs
        """
        if not self._ctx:
            raise ValueError("Predictor not connected to client")

        response = self._ctx.get_json(
            f"/session/{self.session_id}/webhooks"
        )

        return response.get('webhooks', {})

    def disable_webhook(self, event_type: str) -> None:
        """
        Disable a specific webhook event.

        Args:
            event_type: Webhook event type to disable
        """
        if not self._ctx:
            raise ValueError("Predictor not connected to client")

        self._ctx.post_json(
            f"/session/{self.session_id}/disable_webhook",
            data={"event_type": event_type, "predictor_id": self.id}
        )

    def set_value_meaning(self, meanings: Dict[str, str]) -> Dict[str, str]:
        """
        Set customer-facing text for one or more predicted-class labels.

        Overrides the auto-computed default (derived from this predictor's
        PPV/NPV) for the given labels. Labels not included here keep their
        auto default. Every ``predict()`` response includes ``value_meaning``
        for the predicted class going forward.

        Args:
            meanings: Dict mapping label -> customer-facing text, e.g.
                {"0": "It's not junk", "1": "50/50 — needs human review"}

        Returns:
            Dict mapping every known label to its current text (customer
            overrides merged with auto defaults for the rest).

        Example:
            predictor.set_value_meaning({
                "0": "Safe to auto-approve",
                "1": "Flag for manual review",
            })
        """
        if not self._ctx:
            raise ValueError("Predictor not connected to client")
        if not meanings:
            raise ValueError("meanings must be a non-empty {label: text} dict")

        response = self._ctx.put_json(
            f"/session/{self.session_id}/predictor/{self.id}/value_meaning",
            data=meanings,
        )
        return response.get('value_meaning', {})

    def get_value_meaning(self) -> Dict[str, str]:
        """
        Get the current customer-facing text for every predicted-class label.

        Customer overrides (from set_value_meaning()) are merged with
        auto-computed defaults for any label that has no override.

        Returns:
            Dict mapping label -> text.
        """
        if not self._ctx:
            raise ValueError("Predictor not connected to client")

        response = self._ctx.get_json(
            f"/session/{self.session_id}/predictor/{self.id}/value_meaning"
        )
        return response.get('value_meaning', {})

    def clear_value_meaning(self, label: str) -> Dict[str, str]:
        """
        Clear a customer override for one label, reverting it to the
        auto-computed default.

        Args:
            label: The label whose override should be cleared.

        Returns:
            Dict mapping every known label to its current text after the
            clear.
        """
        if not self._ctx:
            raise ValueError("Predictor not connected to client")

        response = self._ctx.delete_json(
            f"/session/{self.session_id}/predictor/{self.id}/value_meaning/{label}"
        )
        return response.get('value_meaning', {})

    def get_metrics(self) -> Dict[str, Any]:
        """Get training metrics for this predictor."""
        if not self._ctx:
            raise ValueError("Predictor not connected to client")

        return self._ctx.get_json(f"/session/{self.session_id}/training_metrics")

    def get_classification_metrics(self) -> Dict[str, Any]:
        """Confusion matrix, per-class precision/recall/f1, and headline
        classification metrics for this predictor (or ``regression_metrics``
        for a regression target).

        Unlike ``accuracy``/``auc``/``f1`` on this object (or in
        ``to_dict()``), this is a separate, on-demand call — it reads this
        predictor's own model card file, never a session-level card that
        could belong to a different predictor in a multi-predictor session.

        Returns a dict shaped like:
            {"job_id": ..., "target_column": ...,
             "classification_metrics": {"accuracy":..., "precision":...,
                 "recall":..., "f1":..., "macro_f1":..., "auc":..., ...},
             "confusion_matrix": {...}}
        or, for regression targets:
            {"job_id": ..., "target_column": ..., "regression_metrics": {...}}
        """
        if not self._ctx:
            raise ValueError("Predictor not connected to client")

        return self._ctx.get_json(f"/session/{self.session_id}/predictor/{self.id}/classification_metrics")

    def get_model_card(self) -> Dict[str, Any]:
        """Get the model card for this predictor.

        The model card includes a ``model_fit`` block that catalogs the model's
        precision/recall/coverage shape (e.g. "Picky / conservative — only fires
        when sure" vs "Wide net — flags anything plausible") with per-intent
        scores and good-fit/poor-fit use cases.
        """
        if not self._ctx:
            raise ValueError("Predictor not connected to client")

        return self._ctx.get_json(f"/session/{self.session_id}/model_card")

    def what_is_this_model_good_for(self) -> Dict[str, Any]:
        """Concrete, label-aware use-case summary for this predictor.

        Common phrasings that all mean *this method*. If you (human or agent)
        are looking for any of these, you are in the right place:

          - "what is this model good for?"
          - "recommend(ed) uses" / "what do you recommend I use this for?"
          - "use cases" / "use case for this predictor"
          - "intended uses" / "intended use" (Mitchell et al. model-card spec)
          - "best uses" / "best use of this predictor"
          - "suggested applications" / "where should I deploy this?"
          - "suitability" / "deployment guide" / "applicability"

        Returns a structured dict with:

        - ``headline``: capability one-liner (AUC, PR-AUC, selective lift)
          with both ``text`` and structured ``metrics`` fields.
        - ``uses``: list of concrete use cases (e.g. FRAUD DETECTION, ANOMALY
          TRIAGE, HUMAN-IN-THE-LOOP TRIAGE, GENERAL CLASSIFICATION, REVIEW
          QUEUE) with this predictor's own target column and positive /
          negative labels substituted in. Each carries ``domain``,
          ``condition`` (structured IF clause), ``action`` (recommended
          decision pattern), and a flat ``text`` rendering for terse contexts
          (console, log).
        - ``anti``: list of "do not use for X" warnings keyed to specific
          metric weaknesses, each with ``title``, ``reason``, optional
          ``evidence`` (metric, value, threshold), and ``text``.

        Computed at training time and travels with the model card. Returns an
        empty dict if the model card doesn't carry a
        ``what_is_this_model_good_for`` block (older models, pre-rollout).
        """
        card = self.get_model_card() or {}
        return card.get("what_is_this_model_good_for") or {}

    def ground_truth_stats(self) -> Dict[str, Any]:
        """Get ground truth feedback statistics for this predictor's session.

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
            raise ValueError("Predictor not connected to client")

        return self._ctx.get_json(
            f"/compute/session/{self.session_id}/ground_truth_stats"
        )

    def get_manifold_viz(
        self,
        epoch: str | int | None = None,
        start_epoch: int | None = None,
        limit: int | None = None,
        format: str = "native",
        representatives_only: bool = True,
    ) -> Dict[str, Any]:
        """Get manifold visualization data showing decision boundary evolution.

        Returns 3D coordinates of sample points on the ES manifold with per-epoch
        SP predictions showing how the decision boundary evolves during training.

        Args:
            epoch: Specific epoch number, or "last" for the final epoch.
            start_epoch: First epoch to return (0-indexed).
            limit: Maximum number of epochs to return.
            format: "native" for raw manifold data, or "projections" for
                    sphere-viewer compatible epoch_projections format.
            representatives_only: If True (default), only return lattice
                representative points for spatial coverage.

        Returns:
            Dictionary with manifold viz data. Use format="projections" for
            sphere-viewer compatible output with coords, set_columns, and
            scalar_columns per point per epoch.
        """
        if not self._ctx:
            raise ValueError("Predictor not connected to client")

        params = {}
        if epoch is not None:
            params["epoch"] = str(epoch)
        if start_epoch is not None:
            params["start_epoch"] = str(start_epoch)
        if limit is not None:
            params["limit"] = str(limit)
        if format != "native":
            params["format"] = format
        if not representatives_only:
            params["representatives_only"] = "false"

        return self._ctx.get_json(
            f"/session/{self.session_id}/manifold_viz",
            params=params,
        )

    def training_suggestions(self, as_text: bool = False) -> Union[Dict[str, Any], str]:
        """
        Get suggestions for improving predictor performance.

        Analyzes training results to identify:
        - Hard-to-predict samples (consistently misclassified)
        - Feature weaknesses (sparse regions, rare categories)
        - Class imbalance in difficult cases
        - Low-signal features

        Args:
            as_text: If True, return human-readable text report.
                    If False (default), return structured dictionary.

        Returns:
            If as_text=False (default): Dictionary with:
                - summary: Quick stats (hard_rows, weaknesses, suggestions_count)
                - top_features: List of (column, mi_score) by predictive power
                - suggestions: List of prioritized improvement suggestions
                - hard_samples: Sample indices that are consistently wrong

            If as_text=True: Human-readable text report string

        Example:
            >>> predictor.wait_for_training()

            >>> # Get structured data (default)
            >>> suggestions = predictor.training_suggestions()
            >>> print(suggestions['summary'])
            {'hard_rows': 15, 'feature_weaknesses': 3, 'suggestions_count': 5}

            >>> for s in suggestions['suggestions']:
            ...     print(f"[{s['priority']}] {s['title']}")
            ...     print(f"    {s['description']}")
            [1] Address 5 consistently misclassified samples
                These samples were NEVER correctly classified...

            >>> # Get text report
            >>> print(predictor.training_suggestions(as_text=True))
            ================================================================================
            TRAINING SUGGESTIONS REPORT
            ...
        """
        if not self._ctx:
            raise ValueError("Predictor not connected to client")

        format_param = "text" if as_text else "json"
        response = self._ctx.get_json(
            f"/session/{self.session_id}/training_suggestions",
            params={"predictor_id": self.id, "format": format_param}
        )

        if as_text:
            return response.get("report", "")

        return response

    def coverage(
        self,
        strategy: str | None = None,
    ) -> Dict[str, Any]:
        """
        Get coverage metrics — "answer only when you know."

        Each strategy is a different operating point on the same trained model.
        You pick what fraction of queries the model acts on, in exchange for
        higher quality on the rows it does answer.

        Args:
            strategy: Return metrics for a specific strategy. If None, returns
                     the full result including all four strategy views. Options:
                     - "everything": act on every row, no abstention
                     - "only_when_sure": max AUC on the answered set; demurred
                       rows feed your human-in-the-loop label pipeline
                     - "only_on_strong_positives": max precision when predicting +
                     - "only_on_strong_negatives": max NPV when predicting −

        Returns:
            Without strategy: full result with 'strategies' dict containing all
            four views, each with coverage / covered_auc / full_auc / auc_lift /
            confidence_threshold / n_covered / n_total / label.

            With strategy: just that strategy's view (same fields, plus capture
            counts on the strong_positives / strong_negatives strategies).

            Both responses include intent_feasible and intent_feasibility_reason
            for the headline operating point. CHECK THESE BEFORE DEPLOYING:

              intent_feasible=False means the framework could not honor the
              intent contract you trained with (e.g. precision_floor=0.80 but
              no operating point reached that floor). The returned operating
              point is a max-AUC fallback — the model will NOT deliver the
              floor you asked for. intent_feasibility_reason gives a human
              string explaining what couldn't be met and the maximum achievable
              value. Surface this prominently in any automation that consumes
              this response.

        Example:
            >>> predictor.wait_for_training()

            >>> # All strategies at once
            >>> cov = predictor.coverage()
            >>> if not cov.get('intent_feasible', True):
            ...     print(f"⚠ {cov['intent_feasibility_reason']}")
            ...     # don't auto-deploy without explicit acknowledgement
            >>> for key, view in cov['strategies'].items():
            ...     print(f"{view['label']}: coverage={view['coverage']:.0%}")

            >>> # A specific strategy
            >>> pos = predictor.coverage(strategy="only_on_strong_positives")
            >>> print(f"Caught {pos['true_positives_caught']}/{pos['true_positives_total']} positives")
        """
        if not self._ctx:
            raise ValueError("Predictor not connected to client")

        params = {}
        if strategy is not None:
            params["strategy"] = strategy

        return self._ctx.get_json(
            f"/session/{self.session_id}/coverage",
            params=params,
        )

    def coverage_grid(
        self,
        features: list[str],
        steps: int = 20,
        accuracy_threshold: float | None = None,
    ) -> Dict[str, Any]:
        """
        Map the model's "know" vs "don't know" zones across 1 or 2 features.

        Sweeps feature values across their range (mean +/- 2 std for scalars,
        all members for categoricals) while holding other features at their
        median/mode. For each cell, returns the prediction, calibrated
        confidence, and whether the model is in its confident zone.

        Designed for 2D heatmap visualization:
          - Color: red = predict negative, green = predict positive
          - Alpha/saturation: calibrated confidence (vivid = confident)
          - Gray cells: "don't know" — outside qualified bands

        Args:
            features: 1 or 2 feature column names to sweep.
            steps: Number of steps per axis for scalar features (default 20).
                  Categorical features use all unique values regardless.
            accuracy_threshold: Minimum band accuracy for "know" zone (0-1).
                               Default: 0.80.

        Returns:
            Dictionary with:
                - features: list of swept feature names
                - axes: list of value arrays (one per feature)
                - grid: list of cell dicts, each with:
                    - prediction: predicted class
                    - probability: P(positive class)
                    - confidence: margin-based confidence (0-1)
                    - in_qualified_band: bool (True = "know", False = "don't know")
                    - values: dict of swept feature values for this cell
                - baseline_record: median/mode values used for non-swept features
                - n_qualified: cells in the "know" zone
                - n_total: total cells
                - grid_coverage: fraction of grid in "know" zone
                - pos_label: positive class name
                - qualified_bands: probability ranges where model answers

        Example:
            >>> grid = predictor.coverage_grid(
            ...     features=["age", "income"],
            ...     steps=25,
            ... )
            >>> print(f"Grid coverage: {grid['grid_coverage']:.0%}")
            Grid coverage: 62%

            >>> # Find the "know" zone boundaries
            >>> for cell in grid['grid']:
            ...     if cell['in_qualified_band']:
            ...         print(f"  age={cell['values']['age']:.0f}, "
            ...               f"income={cell['values']['income']:.0f}: "
            ...               f"{cell['prediction']} ({cell['confidence']:.0%})")
        """
        if not self._ctx:
            raise ValueError("Predictor not connected to client")

        params = {
            "features": ",".join(features),
            "steps": str(steps),
        }
        if accuracy_threshold is not None:
            params["accuracy_threshold"] = str(accuracy_threshold)

        return self._ctx.get_json(
            f"/session/{self.session_id}/coverage_grid",
            params=params,
        )

    def encode(
        self,
        record: Union[Dict[str, Any], List[Dict[str, Any]], 'pd.DataFrame', None] = None,
        records: Union[Dict[str, Any], List[Dict[str, Any]], 'pd.DataFrame', None] = None,
        short: bool = False,
        *,
        intent: Optional[str] = None,
        representation: str = "auto",
        expected_missing: Optional[List[str]] = None,
    ) -> Union[List[Dict[str, Any]], List[List[float]]]:
        """
        Encode records to embedding vectors using the underlying embedding space.

        Accepts either record= or records= (singular or plural). Each can be
        a single dict, a list of dicts, or a DataFrame.

        Args:
            record: Single record or list of records (alias for records)
            records: Single record or list of records
            short: If True, return only the 3D embedding vectors (for visualization).
                   Deprecated; pass intent='visualization' instead.
            expected_missing: Column names you are INTENTIONALLY omitting from
                   these records (e.g. imputation hold-outs, or fields you simply
                   don't have). Declaring them tells the server the absence is by
                   design, so it won't warn about a column mismatch. Only columns
                   you didn't declare — and didn't supply — are flagged.
            intent: Customer-facing intent describing what you'll do with the
                   embedding. One of: 'clustering' (kNN / similarity), 'visualization'
                   (2D/3D plots), 'near_lossless' (per-column fidelity),
                   'highly_encoded' (dense pooled). Task intents ('regression',
                   'binary_class', 'multiclass', 'multilabel') require a trained
                   predictor — use Predictor.encode(intent=...) on this object.
                   When intent is given, returns a single 'embedding' field in
                   the resolved port's shape (not the short+full pair).
            representation: 'auto' (default), 'preserved' (per-column fidelity),
                   or 'compressed' (dense pooled). Ignored unless intent is given.

        Returns:
            If intent=None, short=False (legacy): List of dicts, each containing
                "embedding" (3D), "embedding_long" (full), "query_record".
            If intent=None, short=True (legacy): List of 3D vectors.
            If intent is given: List of dicts, each containing "embedding"
                (in the intent's resolved shape), "intent", "representation",
                "query_record", and "port_spec".  ``port_spec`` describes the
                embedding the server actually produced — ``{name, width,
                encoding_depth, representation, available}`` — so the caller
                can introspect what they got.

        Example:
            results = predictor.encode(record={"age": 35, "income": 50000})
            vectors_clustering = predictor.encode(records=df, intent='clustering')
            vectors_viz = predictor.encode(records=df, intent='visualization')

            # Inspect what the server returned:
            r = predictor.encode(records=df, intent='near_lossless')[0]
            r['port_spec']['name']             # → 'pre_transformer'
            r['port_spec']['encoding_depth']   # → 'near_lossless'
        """
        if not self._ctx:
            raise ValueError("Predictor not connected to client")

        # Accept either kwarg
        data = record if record is not None else records
        if data is None:
            raise ValueError("Must provide record= or records=")

        # Normalize to list of dicts
        if isinstance(data, dict):
            data = [data]
        elif hasattr(data, 'to_dict'):
            data = data.to_dict('records')
        elif not isinstance(data, list):
            data = [data]

        cleaned = [self._clean_record(r) for r in data]

        body: Dict[str, Any] = {"records": cleaned}
        if intent is not None:
            body["intent"] = intent
            body["representation"] = representation
        if expected_missing:
            body["expected_missing"] = list(expected_missing)

        response = self._ctx.post_json(
            f"/session/{self.session_id}/encode_records",
            data=body,
        )

        results = response.get('results', [])

        if short and intent is None:
            return [r["embedding"] for r in results]

        return results

    def impute(
        self,
        record: Union[Dict[str, Any], List[Dict[str, Any]], 'pd.DataFrame', None] = None,
        records: Union[Dict[str, Any], List[Dict[str, Any]], 'pd.DataFrame', None] = None,
        columns: Optional[List[str]] = None,
        strategy: str = "greedy",
        report: bool = False,
    ) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """Impute missing/null fields in partial records using Gibbs-style probe ensemble.

        Accepts either record= or records= (singular or plural). Each can be
        a single dict, a list of dicts, or a DataFrame.

        Args:
            record: Single record or list of records (alias for records)
            records: Single record or list of records
            columns: Specific columns to impute. Default: all missing probeable columns.
            strategy: "greedy" (sequential, higher quality) or "parallel" (all-at-once).
            report: If True, include a "report" key with per-column aggregate stats.
                    When report=True, always returns a dict with "results" and "report".

        Returns:
            Without report: single result dict or list of result dicts, each containing:
            - "record": The complete record with all fields filled
            - "imputed_fields": Dict mapping column -> {value, confidence, cascade_factor,
              effective_confidence, iteration, target_type, probabilities}
            - "skipped_columns": Columns that couldn't be imputed and why
            - "strategy": Which strategy was used
            - "n_iterations": How many Gibbs iterations were run

            With report=True: dict with "results" (list) and "report" (per-column
            aggregate stats: target_type, n_imputed, prediction_dist, confidence_dist).

        Example:
            result = predictor.impute(record={"age": 35, "income": None})
            print(result["record"])  # {"age": 35, "income": 52000, ...}

            out = predictor.impute(records=batch, report=True)
            print(out["report"]["education"])
        """
        if not self._ctx:
            raise ValueError("Predictor not connected to client")

        data = record if record is not None else records
        if data is None:
            raise ValueError("Must provide record= or records=")

        single = isinstance(data, dict)
        if single:
            data = [data]
        elif hasattr(data, 'to_dict'):
            data = data.to_dict('records')
        elif not isinstance(data, list):
            data = [data]

        cleaned = [self._clean_record(r) for r in data]

        payload = {"records": cleaned, "strategy": strategy}
        if columns is not None:
            payload["columns"] = columns
        if report:
            payload["report"] = True

        response = self._ctx.post_json(
            f"/session/{self.session_id}/impute",
            data=payload,
        )

        if report:
            return {
                "results": response.get("results", []),
                "report": response.get("report", {}),
            }
        results = response.get("results", [])
        return results[0] if single else results

    def _update_metrics(self) -> None:
        """Update metrics from server."""
        try:
            metrics = self.get_metrics()
            # get_metrics() returns {"training_metrics": {..., "final_metrics": {...}}}
            # — this predictor's own accuracy/auc/f1 live under final_metrics.
            # ('single_predictor' was never a real key in this response; that
            # lookup silently returned {} on every call.)
            sp_metrics = metrics.get('training_metrics', {}).get('final_metrics', {})
            if sp_metrics:
                self.accuracy = sp_metrics.get('accuracy')
                self.auc = sp_metrics.get('roc_auc') or sp_metrics.get('auc')
                self.f1 = sp_metrics.get('f1') or sp_metrics.get('f1_score')
        except Exception as e:
            logger.debug(f"_update_metrics() failed for predictor {self.id}: {e}")

    def _clean_record(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """Clean a record for API submission."""
        import math

        cleaned = {}
        for key, value in record.items():
            # Handle NaN/Inf
            if isinstance(value, float):
                if math.isnan(value) or math.isinf(value):
                    value = None
            # Handle numpy types
            if hasattr(value, 'item'):
                value = value.item()
            cleaned[key] = value
        return cleaned

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            'id': self.id,
            'session_id': self.session_id,
            'target_column': self.target_column,
            'target_type': self.target_type,
            'name': self.name,
            'status': self.status,
            'accuracy': self.accuracy,
            'auc': self.auc,
            'f1': self.f1,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'deletion_protection': self.deletion_protection,
        }

    def __repr__(self) -> str:
        status_str = f", status='{self.status}'" if self.status else ""
        acc_str = f", accuracy={self.accuracy:.4f}" if self.accuracy else ""
        return f"Predictor(id='{self.id}', target='{self.target_column}'{status_str}{acc_str})"
