#  -*- coding: utf-8 -*-
#
#  Copyright (c) 2023-2026 Featrix, Inc, All Rights Reserved
#
#  Proprietary and Confidential.  Unauthorized use, copying or dissemination
#  of these materials is strictly prohibited.
#

"""
PublishedPredictor class for FeatrixSphere API.

Represents a predictor deployed to production, accessed via the Sphere API.
"""

import json
import logging
import time
from dataclasses import dataclass, field
from typing import Callable, Dict, Any, Iterator, Optional, List, Union, TYPE_CHECKING

if TYPE_CHECKING:
    from .http_client import ClientContext
    import pandas as pd

from .http_client import customer_metadata_headers
from .prediction_result import PredictionResult
from .exceptions import (
    LoadFailedError,
    LoadTimeoutError,
    ModelNotLoadingError,
)

logger = logging.getLogger(__name__)


@dataclass
class LoadStatus:
    """One progress sample from the prediction server's model-load tracker.

    Shape mirrors the on-the-wire JSON contract from the load-progress plan
    (``docs/internal/plans/2026-05-model-load-progress-reporting.md``):
    ``phase`` is stable, fields are additive-only.
    """
    phase: str                         # reading_header | loading_training_db | unpickling | verifying_fixture | done | failed
    pct_within_phase: float            # 0–100 within the current phase
    overall_pct: float                 # 0–100, server-computed weight across phases
    elapsed_s: float
    estimated_remaining_s: Optional[float] = None
    error: Optional[str] = None
    model_id: Optional[str] = None

    @property
    def is_terminal(self) -> bool:
        return self.phase in ("done", "failed")

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LoadStatus":
        return cls(
            phase=data.get("phase", "unknown"),
            pct_within_phase=float(data.get("pct_within_phase", 0.0)),
            overall_pct=float(data.get("overall_pct", 0.0)),
            elapsed_s=float(data.get("elapsed_s", 0.0)),
            estimated_remaining_s=data.get("estimated_remaining_s"),
            error=data.get("error"),
            model_id=data.get("model_id"),
        )


@dataclass
class PublishedPredictor:
    """
    Represents a predictor deployed to production for serving predictions.

    Attributes:
        org: Organization ID
        name: Model name
        api_key: API key for authentication
        base_url: Sphere API URL (default: https://sphere-api.featrix.com)

    Usage:
        # Load a published predictor
        predictor = client.published_predictor(
            org="alph",
            name="my-model",
            api_key="sk_alph_xxx"
        )

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

    org: str
    name: str
    api_key: str
    base_url: str = "https://sphere-api.featrix.com"

    # Internal
    _ctx: Optional['ClientContext'] = field(default=None, repr=False)

    @property
    def endpoint_url(self) -> str:
        """Get the full prediction endpoint URL."""
        return f"{self.base_url}/predict/{self.org}/{self.name}"

    @property
    def load_status_url(self) -> str:
        """URL for the model-load status endpoint on the prediction server."""
        return f"{self.base_url}/v1/models/{self.org}/{self.name}/load_status"

    def get_load_status(self) -> LoadStatus:
        """One-shot poll of the prediction server's load tracker.

        Raises:
            ModelNotLoadingError: server returned 404 — the model is not in
                the load tracker (either never started, or evicted).
            RuntimeError: any other non-200 response.

        Returns:
            LoadStatus. If ``phase=='failed'`` the caller should treat this
            as a terminal error; ``wait_until_loaded`` does this conversion
            for you by raising ``LoadFailedError``.
        """
        import requests
        response = requests.get(
            self.load_status_url,
            headers={"X-API-Key": self.api_key},
            timeout=10,
        )
        if response.status_code == 404:
            raise ModelNotLoadingError(model_id=f"{self.org}/{self.name}")
        if response.status_code != 200:
            raise RuntimeError(
                f"load_status failed with status {response.status_code}: "
                f"{response.text[:200]}"
            )
        return LoadStatus.from_dict(response.json())

    def wait_until_loaded(
        self,
        timeout_s: float = 300.0,
        poll_interval_s: float = 1.0,
        on_progress: Optional[Callable[[LoadStatus], None]] = None,
    ) -> LoadStatus:
        """Block until the server reports ``phase='done'`` for this model.

        Args:
            timeout_s: Maximum wall time before giving up.
            poll_interval_s: Sleep between status polls.
            on_progress: Optional callback fired on every poll that returns
                fresh data. Use this to drive a progress bar / log line.

        Raises:
            LoadTimeoutError: ``timeout_s`` elapsed and load is still
                in-flight.
            LoadFailedError: server reports ``phase='failed'``.

        Returns:
            The final ``LoadStatus`` (phase='done').
        """
        deadline = time.monotonic() + timeout_s
        last_status: Optional[LoadStatus] = None
        last_emitted_phase: Optional[str] = None
        last_emitted_pct: float = -1.0

        while True:
            try:
                status = self.get_load_status()
            except ModelNotLoadingError:
                # Server may legitimately race with the load request — give it
                # one poll interval before treating as fatal.
                if last_status is None and time.monotonic() < deadline:
                    time.sleep(poll_interval_s)
                    continue
                raise

            last_status = status
            if on_progress is not None and (
                status.phase != last_emitted_phase
                or (status.overall_pct - last_emitted_pct) >= 1.0
                or status.is_terminal
            ):
                last_emitted_phase = status.phase
                last_emitted_pct = status.overall_pct
                try:
                    on_progress(status)
                except Exception:
                    logger.debug("on_progress callback raised", exc_info=True)

            if status.phase == "done":
                return status
            if status.phase == "failed":
                raise LoadFailedError(
                    model_id=f"{self.org}/{self.name}", status=status
                )

            if time.monotonic() >= deadline:
                raise LoadTimeoutError(
                    model_id=f"{self.org}/{self.name}",
                    last_status=status,
                    timeout_s=timeout_s,
                )
            time.sleep(poll_interval_s)

    def predict(
        self,
        record: Dict[str, Any],
        *,
        feature_importance: bool = False,
        wait_for_load: bool = False,
        on_progress: Optional[Callable[[LoadStatus], None]] = None,
        load_timeout_s: float = 300.0,
        customer_metadata: Optional[Dict[str, Any]] = None,
    ) -> PredictionResult:
        """
        Make a single prediction.

        Args:
            record: Input record dictionary
            feature_importance: If True, compute feature importance via
                leave-one-out ablation (mask each column, batch-predict
                the original + N ablated variants, importance = the
                confidence delta). Same mechanism as the session-based
                ``Predictor.predict(feature_importance=True)`` — see
                docs/internal/plans/2026-08-02-real-explain-attribution.md
                for why this ablation path is used instead of the
                gradient-based ``/explain`` endpoint.
            wait_for_load: If True, poll the server's load_status endpoint
                until the model is ``done`` before issuing the prediction.
                Off by default — preserves the legacy fail-fast behavior.
            on_progress: Optional callback for load progress (only used when
                ``wait_for_load=True``).
            load_timeout_s: Maximum seconds to wait for load.
            customer_metadata: Optional dict of your own ids/labels (e.g.
                {"order_id": ..., "caller": ...}) stored with the prediction
                for tracing it back later -- never sent to the model.

        Returns:
            PredictionResult with prediction, confidence, and probabilities.
            If feature_importance=True, also includes feature_importance dict.

        Example:
            result = predictor.predict({"age": 35, "income": 50000})
            print(result.predicted_class)  # "churned"
            print(result.confidence)       # 0.87

            # With feature importance
            result = predictor.predict(record, feature_importance=True)
            print(result.feature_importance)  # {"income": 0.15, "age": 0.08, ...}
        """
        if wait_for_load:
            self.wait_until_loaded(
                timeout_s=load_timeout_s, on_progress=on_progress
            )

        # Clean the record
        cleaned_record = self._clean_record(record)

        if feature_importance:
            # Build N+1 records: original + each feature nulled out
            columns = list(cleaned_record.keys())
            batch = [cleaned_record]

            for col in columns:
                ablated = cleaned_record.copy()
                ablated[col] = None
                batch.append(ablated)

            # Single batch call
            results = self.batch_predict(batch, customer_metadata=customer_metadata)

            # Compare: importance = |original_confidence - ablated_confidence|
            original = results[0]
            importance = {}
            original_conf = original.confidence or 0.0

            for i, col in enumerate(columns):
                ablated_result = results[i + 1]
                ablated_conf = ablated_result.confidence or 0.0
                delta = abs(original_conf - ablated_conf)
                importance[col] = round(delta, 4)

            original.feature_importance = dict(sorted(
                importance.items(),
                key=lambda x: x[1],
                reverse=True,
            ))
            return original

        # Make batch request with single record
        results = self.batch_predict([cleaned_record], customer_metadata=customer_metadata)

        return results[0] if results else None

    def batch_predict(
        self,
        records: Union[List[Dict[str, Any]], 'pd.DataFrame'],
        batch_size: int = 256,
        *,
        wait_for_load: bool = False,
        on_progress: Optional[Callable[[LoadStatus], None]] = None,
        load_timeout_s: float = 300.0,
        customer_metadata: Optional[Dict[str, Any]] = None,
    ) -> List[PredictionResult]:
        """
        Make batch predictions.

        Args:
            records: List of record dictionaries or DataFrame
            batch_size: Number of records to process per batch
            wait_for_load: If True, poll the server's load_status endpoint
                until the model is ``done`` before issuing predictions.
            on_progress: Optional callback for load progress (only used when
                ``wait_for_load=True``).
            load_timeout_s: Maximum seconds to wait for load.
            customer_metadata: Optional dict stored with the prediction for
                tracing -- never sent to the model (see predict()).

        Returns:
            List of PredictionResult objects

        Example:
            results = predictor.batch_predict([
                {"age": 35, "income": 50000},
                {"age": 42, "income": 75000}
            ])
            for result in results:
                print(result.predicted_class, result.confidence)
        """
        if wait_for_load:
            self.wait_until_loaded(
                timeout_s=load_timeout_s, on_progress=on_progress
            )

        # Convert DataFrame to list of dicts if needed
        if hasattr(records, 'to_dict'):
            records = records.to_dict('records')

        # Clean records
        cleaned_records = [self._clean_record(r) for r in records]

        # Build request
        request_payload = {
            "records": cleaned_records,
            "batch_size": batch_size,
        }

        # Make request to production API with authentication
        import requests

        headers = {
            "X-API-Key": self.api_key,
            "Content-Type": "application/json",
            **customer_metadata_headers(customer_metadata),
        }

        response = requests.post(
            self.endpoint_url,
            json=request_payload,
            headers=headers,
            timeout=300,  # 5 minute timeout for large batches
        )

        # Check for errors
        if response.status_code != 200:
            error_msg = f"Prediction failed with status {response.status_code}"
            try:
                error_data = response.json()
                error_msg = error_data.get('error', error_msg)
            except:
                error_msg = response.text or error_msg
            raise RuntimeError(error_msg)

        # Parse response
        response_data = response.json()

        if not response_data.get('success'):
            error = response_data.get('error', 'Unknown error')
            raise RuntimeError(f"Prediction failed: {error}")

        # Parse results
        results = []
        predictions = response_data.get('predictions', [])

        # Extract prediction_uuid and deep links injected by sphere-api
        top_level_uuid = response_data.get('prediction_uuid')
        links = response_data.get('_links')

        for i, pred in enumerate(predictions):
            record = cleaned_records[i] if i < len(cleaned_records) else {}

            # Production API nests prediction data under 'results' key
            pred_results = pred.get('results', pred)

            # Create PredictionResult from production API response
            result = PredictionResult(
                predicted_class=pred_results.get('prediction', pred_results.get('predicted_class')),
                confidence=pred_results.get('confidence'),
                probabilities=pred_results.get('probabilities', {}),
                threshold=pred_results.get('threshold'),
                query_record=record,
                guardrails=pred.get('guardrails'),
                ignored_query_columns=pred.get('ignored_query_columns'),
                available_query_columns=pred.get('available_query_columns'),
                prediction_uuid=top_level_uuid,
                links=links,
                # Which model actually answered: the serving worker echoes its
                # loaded default predictor_id as neural_function_id. After a
                # retrain + republish under the same name, this is how a caller
                # tells the new model is live.
                predictor_id=response_data.get('neural_function_id'),
                _ctx=self._ctx,
                _published_predictor=self,
            )
            results.append(result)

        return results

    def predict_csv_file(
        self,
        csv_path: str,
        batch_size: int = 256,
        customer_metadata: Optional[Dict[str, Any]] = None,
    ) -> List[PredictionResult]:
        """
        Load a CSV file and run batch predictions on all rows.

        Args:
            csv_path: Path to the CSV file
            batch_size: Number of records to process per batch

        Returns:
            List of PredictionResult objects

        Example:
            results = predictor.predict_csv_file("test_data.csv")
            for r in results:
                print(r.predicted_class, r.confidence)
        """
        import pandas as pd
        df = pd.read_csv(csv_path)
        return self.batch_predict(df, batch_size=batch_size, customer_metadata=customer_metadata)

    def batch_predict_streaming(
        self,
        records: Union[List[Dict[str, Any]], 'pd.DataFrame'],
        batch_size: int = 256,
        customer_metadata: Optional[Dict[str, Any]] = None,
    ) -> Iterator[PredictionResult]:
        """
        Stream predictions one at a time as they come off the GPU.

        Yields individual PredictionResult objects as they arrive from the
        production server, rather than waiting for all predictions to complete.

        Args:
            records: List of record dictionaries or DataFrame
            batch_size: Number of records per GPU batch on the server

        Yields:
            PredictionResult objects, one per input record

        Example:
            for result in predictor.batch_predict_streaming(records):
                print(result.predicted_class, result.confidence)
        """
        import requests as req_lib

        # Convert DataFrame to list of dicts if needed
        if hasattr(records, 'to_dict'):
            records = records.to_dict('records')

        # Clean records
        cleaned_records = [self._clean_record(r) for r in records]

        # Build request with NDJSON format
        request_payload = {
            "records": cleaned_records,
            "batch_size": batch_size,
            "result_format": "ndjson",
        }

        headers = {
            "X-API-Key": self.api_key,
            "Content-Type": "application/json",
            **customer_metadata_headers(customer_metadata),
        }

        response = req_lib.post(
            self.endpoint_url,
            json=request_payload,
            headers=headers,
            timeout=600,  # 10 minute timeout for large streaming batches
            stream=True,
        )

        if response.status_code != 200:
            error_msg = f"Prediction failed with status {response.status_code}"
            try:
                error_data = response.json()
                error_msg = error_data.get('error', error_msg)
            except Exception:
                error_msg = response.text or error_msg
            raise RuntimeError(error_msg)

        header_info = {}

        for line in response.iter_lines():
            if not line:
                continue
            msg = json.loads(line)

            if msg['type'] == 'header':
                header_info = msg
            elif msg['type'] == 'prediction':
                idx = msg['index']
                pred = msg['result']
                record = cleaned_records[idx] if idx < len(cleaned_records) else {}

                # Production API nests prediction data under 'results' key
                pred_results = pred.get('results', pred)

                yield PredictionResult(
                    predicted_class=pred_results.get('prediction', pred_results.get('predicted_class')),
                    confidence=pred_results.get('confidence'),
                    probabilities=pred_results.get('probabilities', {}),
                    threshold=pred_results.get('threshold'),
                    query_record=record,
                    guardrails=pred.get('guardrails'),
                    ignored_query_columns=pred.get('ignored_query_columns'),
                    available_query_columns=pred.get('available_query_columns'),
                    prediction_uuid=header_info.get('prediction_uuid'),
                    links=header_info.get('_links'),
                    predictor_id=header_info.get('neural_function_id'),
                    _ctx=self._ctx,
                    _published_predictor=self,
                )
            elif msg['type'] == 'done':
                pass  # streaming complete

    def send_feedback(
        self,
        prediction_uuid: str,
        ground_truth: Union[str, float],
        meta: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        """
        Send ground truth feedback for a prediction.

        Args:
            prediction_uuid: UUID from PredictionResult.prediction_uuid
            ground_truth: The correct label/value
            meta: Optional metadata dict (source, annotator, notes, batch_id, etc.)

        Returns:
            Server response dict

        Example:
            result = predictor.predict({"age": 35})
            predictor.send_feedback(
                prediction_uuid=result.prediction_uuid,
                ground_truth="correct_label",
                meta={"source": "manual_review", "annotator": "jdoe"},
            )
        """
        import requests as req_lib

        headers = {
            "X-API-Key": self.api_key,
            "Content-Type": "application/json",
        }

        feedback_url = f"{self.base_url}/predict/{self.org}/{self.name}/feedback"

        body = {
            "prediction_uuid": prediction_uuid,
            "ground_truth": str(ground_truth),
        }
        if meta is not None:
            body["meta"] = meta

        response = req_lib.post(
            feedback_url,
            json=body,
            headers=headers,
            timeout=30,
        )

        if response.status_code != 200:
            error_msg = f"Feedback failed with status {response.status_code}"
            try:
                error_data = response.json()
                error_msg = error_data.get('error', error_msg)
            except Exception:
                error_msg = response.text or error_msg
            raise RuntimeError(error_msg)

        return response.json()

    def status(self) -> Dict[str, Any]:
        """
        Get deployment status of this published model on the production network.

        Returns:
            Dictionary with:
                - on_disk: Whether the model files exist on the production server
                - published_at: When the model was published (ISO 8601)
                - in_memory: Whether the model is loaded in a running container
                - loaded_at: When the container was started (ISO 8601)
                - last_used: Last prediction request time (ISO 8601)
                - request_count: Total predictions served since container start
                - uptime_seconds: How long the container has been running
                - verification: Self-test status (PASSED, FAILED, SKIPPED, PENDING)

        Example:
            status = predictor.status()
            if status['in_memory']:
                print(f"Model hot, {status['request_count']} predictions served")
            else:
                print(f"Model on disk, will cold-start on next prediction")
        """
        import requests as req_lib

        headers = {
            "X-API-Key": self.api_key,
        }

        status_url = f"{self.base_url}/predict/{self.org}/{self.name}/status"

        response = req_lib.get(
            status_url,
            headers=headers,
            timeout=15,
        )

        if response.status_code != 200:
            error_msg = f"Status request failed with status {response.status_code}"
            try:
                error_data = response.json()
                error_msg = error_data.get('error', error_msg)
            except Exception:
                error_msg = response.text or error_msg
            raise RuntimeError(error_msg)

        return response.json()

    def metrics(self) -> Dict[str, Any]:
        """
        Get training-time metrics for this published model.

        Returns:
            Dictionary with:
                - org, name
                - metrics: the model's training-time metrics (classification
                  fields like accuracy/auc/macro_f1, or regression fields
                  like r2/rmse/mae, whichever applies to this model)
                - primary_metric: {key, value} for the single headline metric
                  MetricPolicy selected for this model's problem type, or
                  None for a model published before this field existed

        Example:
            m = predictor.metrics()
            if m['primary_metric']:
                print(f"{m['primary_metric']['key']}: {m['primary_metric']['value']:.3f}")
        """
        import requests as req_lib

        headers = {
            "X-API-Key": self.api_key,
        }

        metrics_url = f"{self.base_url}/predict/{self.org}/{self.name}/metrics"

        response = req_lib.get(
            metrics_url,
            headers=headers,
            timeout=15,
        )

        if response.status_code != 200:
            error_msg = f"Metrics request failed with status {response.status_code}"
            try:
                error_data = response.json()
                error_msg = error_data.get('error', error_msg)
            except Exception:
                error_msg = response.text or error_msg
            raise RuntimeError(error_msg)

        return response.json()

    def ground_truth_stats(self) -> Dict[str, Any]:
        """
        Get ground truth feedback statistics for this published model.

        Returns:
            Dictionary with:
                - org: Organization slug
                - model_name: Model name
                - total_predictions: Total successful predictions
                - total_corrections: Predictions with ground truth feedback
                - correction_rate: Fraction with ground truth

        Example:
            stats = predictor.ground_truth_stats()
            print(f"{stats['total_corrections']}/{stats['total_predictions']} have ground truth")
        """
        import requests as req_lib

        headers = {
            "X-API-Key": self.api_key,
        }

        stats_url = f"{self.base_url}/predict/{self.org}/{self.name}/ground_truth_stats"

        response = req_lib.get(
            stats_url,
            headers=headers,
            timeout=30,
        )

        if response.status_code != 200:
            error_msg = f"Stats request failed with status {response.status_code}"
            try:
                error_data = response.json()
                error_msg = error_data.get('error', error_msg)
            except Exception:
                error_msg = response.text or error_msg
            raise RuntimeError(error_msg)

        return response.json()

    def get_columns(self) -> List[str]:
        """
        Get column names for this published model.

        Returns column metadata from Supabase — no compute node or production-ai
        worker is involved. Available as soon as the model is published.

        Returns:
            List of column names (excludes internal __featrix columns).

        Example:
            columns = predictor.get_columns()
            print(f"Model expects {len(columns)} columns: {columns[:5]}...")
        """
        import requests as req_lib

        response = req_lib.get(
            f"{self.base_url}/predict/{self.org}/{self.name}/columns",
            headers={"X-API-Key": self.api_key},
            timeout=15,
        )

        if response.status_code != 200:
            error_msg = f"get_columns failed with status {response.status_code}"
            try:
                error_data = response.json()
                error_msg = error_data.get('error', error_msg)
            except Exception:
                error_msg = response.text or error_msg
            raise RuntimeError(error_msg)

        data = response.json()
        columns = data.get('columns', [])
        # Extract just the name strings if columns are dicts (full metadata format)
        if columns and isinstance(columns[0], dict):
            return [c['name'] for c in columns]
        return columns

    def get_session(self) -> Dict[str, Any]:
        """
        Get session metadata for this published model.

        Returns session data from production-ai — no compute node is involved.

        Returns:
            Dictionary with session metadata (session_id, status, job_plan, etc.).

        Example:
            session = predictor.get_session()
            print(f"Session: {session.get('session', {}).get('session_id')}")
        """
        import requests as req_lib

        response = req_lib.get(
            f"{self.base_url}/predict/{self.org}/{self.name}/session",
            headers={"X-API-Key": self.api_key},
            timeout=15,
        )

        if response.status_code != 200:
            error_msg = f"get_session failed with status {response.status_code}"
            try:
                error_data = response.json()
                error_msg = error_data.get('error', error_msg)
            except Exception:
                error_msg = response.text or error_msg
            raise RuntimeError(error_msg)

        return response.json()

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
            'org': self.org,
            'name': self.name,
            'base_url': self.base_url,
            'endpoint_url': self.endpoint_url,
        }

    def __repr__(self) -> str:
        return f"PublishedPredictor(org='{self.org}', name='{self.name}')"
