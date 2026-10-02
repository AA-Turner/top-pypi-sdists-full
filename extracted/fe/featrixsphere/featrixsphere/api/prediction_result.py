#  -*- coding: utf-8 -*-
#
#  Copyright (c) 2023-2026 Featrix, Inc, All Rights Reserved
#
#  Proprietary and Confidential.  Unauthorized use, copying or dissemination
#  of these materials is strictly prohibited.
#

"""
PredictionResult and PredictionFeedback classes.

These classes represent prediction results and the feedback mechanism
for improving model accuracy.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, Optional, Union, TYPE_CHECKING

if TYPE_CHECKING:
    from .http_client import ClientContext


@dataclass
class PredictionResult:
    """
    Represents a prediction result with full metadata.

    Attributes:
        prediction_uuid: Unique identifier for this prediction (use for feedback)
        prediction: Raw prediction result (class probabilities or numeric value)
        predicted_class: Predicted class name (for classification)
        confidence: Confidence score (for classification)
        probabilities: Full probability distribution (for classification)
        threshold: Classification threshold (for binary classification)
        query_record: Original input record
        predictor_id: ID of predictor that made this prediction
        session_id: Session ID (internal)
        timestamp: When prediction was made
        target_column: Target column name
        guardrails: Per-column guardrail warnings (if any)
        ignored_query_columns: Columns in input that were not used (not in training data)
        available_query_columns: All columns the model knows about

    Usage:
        result = predictor.predict({"age": 35, "income": 50000})
        print(result.predicted_class)  # "churned"
        print(result.confidence)       # 0.87
        print(result.prediction_uuid)  # UUID for feedback

        # Check for guardrail warnings
        if result.guardrails:
            print(f"Warnings: {len(result.guardrails)} columns with issues")

        # Check for ignored columns
        if result.ignored_query_columns:
            print(f"Ignored: {result.ignored_query_columns}")

        # Send feedback if prediction was wrong
        if result.predicted_class != actual_label:
            feedback = result.send_feedback(ground_truth=actual_label)
            feedback.send()
    """

    prediction_uuid: Optional[str] = None
    prediction: Optional[Union[Dict[str, float], float]] = None
    predicted_class: Optional[str] = None
    probability: Optional[float] = None
    confidence: Optional[float] = None
    probabilities: Optional[Dict[str, float]] = None
    # Multilabel targets only: the list of predicted tags (probabilities keyed
    # by tag are still in `probabilities` above). `predicted_class` stays None
    # here — there is no single predicted class for a multilabel target.
    predicted_labels: Optional[list] = None
    threshold: Optional[float] = None
    query_record: Optional[Dict[str, Any]] = None

    # Documentation fields - explain what prediction/probability/confidence mean
    readme_prediction: str = field(default="The predicted class label (for classification) or value (for regression).")
    readme_probability: str = field(default="Raw probability of the predicted class from the model's softmax output.")
    readme_confidence: str = field(default=(
        "For binary classification: normalized margin from threshold. "
        "confidence = (prob - threshold) / (1 - threshold) if predicting positive, "
        "or (threshold - prob) / threshold if predicting negative. "
        "Ranges from 0 (at decision boundary) to 1 (maximally certain). "
        "For multi-class: same as probability. "
        "For regression: derived from the conformal interval half-width, "
        "confidence = 1/(1+halfwidth) where halfwidth = q_alpha * sigma. "
        "Higher values mean a tighter prediction interval. "
        "The 'sigma' field is the per-row scale in raw target units, and "
        "'interval_low'/'interval_high' give the prediction interval at "
        "'coverage_level' (e.g. 0.90 for a 90% interval)."
    ))
    readme_threshold: str = field(default=(
        "Decision boundary for binary classification. "
        "If P(positive_class) >= threshold, predict positive; otherwise predict negative. "
        "Calibrated to optimize F1 score on validation data."
    ))
    readme_probabilities: str = field(default=(
        "Full probability distribution across all classes from the model's softmax output. "
        "Dictionary mapping class labels to their probabilities (sum to 1.0)."
    ))
    readme_pos_label: str = field(default=(
        "The class label considered 'positive' for binary classification metrics. "
        "Threshold and confidence calculations are relative to this class."
    ))
    predictor_id: Optional[str] = None
    session_id: Optional[str] = None
    pos_label: Optional[str] = None

    # Customer-facing "what this prediction means" text for the predicted
    # class. Auto-computed from the predictor's confusion matrix (PPV/NPV
    # tiers) unless overridden — see Predictor.set_value_meaning().
    value_meaning: Optional[str] = None
    target_column: Optional[str] = None
    timestamp: Optional[datetime] = None
    model_version: Optional[str] = None

    # Model type: "sp" for single predictor, "foundation_probe+xgboost", "foundation_probe+linear", etc.
    model_type: Optional[str] = None

    # Checkpoint info from the model (epoch, metric_type, metric_value)
    checkpoint_info: Optional[Dict[str, Any]] = None

    # Checkpoint freshness — how stale the checkpoint behind this prediction
    # is, and a rough guess (extrapolated from the interval between the two
    # most recent checkpoints) at when a newer one lands. Populated for
    # every prediction, not just mid-training ones — a "final" checkpoint
    # still has an age. seconds_to_next_checkpoint is None when there's only
    # one checkpoint on disk to extrapolate from.
    seconds_age_of_current_checkpoint: Optional[float] = None
    seconds_to_next_checkpoint: Optional[float] = None

    # Guardrails and warnings
    guardrails: Optional[Dict[str, Any]] = None
    ignored_query_columns: Optional[list] = None
    available_query_columns: Optional[list] = None

    # Regression uncertainty in original target-column units, from the
    # post-hoc conformal scale-head calibrator. ``sigma`` is the per-row
    # scale s(x). ``interval_low``/``interval_high`` are the conformal
    # prediction interval bounds at ``coverage_level`` (e.g. 0.90 for a
    # 90% interval). All four fields are populated together for regression
    # SPs; classification predictions leave them ``None``.
    sigma: Optional[float] = None
    interval_low: Optional[float] = None
    interval_high: Optional[float] = None
    coverage_level: Optional[float] = None

    # Feature importance (from leave-one-out ablation)
    feature_importance: Optional[Dict[str, float]] = None

    # Deep links to Featrix UI (model, foundation, prediction endpoint, etc.)
    links: Optional[Dict[str, str]] = None

    # Populated when the server reports the predictor is mid-training and no
    # checkpoint is available yet. When set, prediction fields (predicted_class,
    # confidence, ...) will be None — caller should retry once training advances.
    # Mirrors the server's `detail` payload from a soft-503 response (status,
    # message, training_info: {epoch, total_epochs, progress_percent, ...}).
    training_status: Optional[Dict[str, Any]] = None

    # Internal: client context for sending feedback
    _ctx: Optional['ClientContext'] = field(default=None, repr=False)
    # Internal: reference to PublishedPredictor for published model feedback routing
    _published_predictor: Optional[Any] = field(default=None, repr=False)

    @classmethod
    def from_response(
        cls,
        response: Dict[str, Any],
        query_record: Dict[str, Any],
        ctx: Optional['ClientContext'] = None,
        predictor_id: Optional[str] = None,
        session_id: Optional[str] = None,
    ) -> 'PredictionResult':
        """
        Create PredictionResult from API response.

        Args:
            response: API response dictionary
            query_record: Original query record
            ctx: Client context for feedback
            predictor_id: Fallback predictor id (the caller's own, used when
                the server response doesn't echo one back)
            session_id: Fallback session id (the caller's own, used when
                the server response doesn't echo one back)

        Returns:
            PredictionResult instance
        """
        # Extract prediction data - handle both formats
        # New format: prediction is the class label, probabilities is separate
        # Old format: prediction is the probabilities dict
        prediction = response.get('prediction')
        probabilities = response.get('probabilities')
        predicted_class = response.get('predicted_class')
        probability = response.get('probability')
        confidence = response.get('confidence')
        predicted_labels = None

        # For old format where prediction is the probabilities dict
        if isinstance(prediction, dict) and not probabilities:
            probabilities = prediction
            if prediction:
                predicted_class = max(prediction.keys(), key=lambda k: prediction[k])
                probability = prediction[predicted_class]
                confidence = probability  # Old format: confidence = probability
        elif isinstance(prediction, str) and not predicted_class:
            # New format: prediction is already the class label
            predicted_class = prediction
        elif isinstance(prediction, list):
            # Multilabel target (light_predict target_type="multilabel"): prediction
            # is the list of tags above threshold, not one class. probabilities
            # is already keyed by tag (not class) from the server.
            predicted_labels = prediction

        return cls(
            prediction_uuid=response.get('prediction_uuid') or response.get('prediction_id'),
            prediction=prediction,
            predicted_class=predicted_class,
            predicted_labels=predicted_labels,
            probability=probability,
            confidence=confidence,
            probabilities=probabilities,
            threshold=response.get('threshold'),
            query_record=query_record,
            predictor_id=response.get('predictor_id') or predictor_id,
            session_id=response.get('session_id') or session_id,
            pos_label=response.get('pos_label'),
            value_meaning=response.get('value_meaning'),
            target_column=response.get('target_column'),
            timestamp=datetime.now(),
            model_version=response.get('model_version'),
            checkpoint_info=response.get('checkpoint_info'),
            seconds_age_of_current_checkpoint=response.get('seconds_age_of_current_checkpoint'),
            seconds_to_next_checkpoint=response.get('seconds_to_next_checkpoint'),
            sigma=response.get('sigma'),
            interval_low=response.get('interval_low'),
            interval_high=response.get('interval_high'),
            coverage_level=response.get('coverage_level'),
            model_type=response.get('model_type'),
            guardrails=response.get('guardrails'),
            ignored_query_columns=response.get('ignored_query_columns'),
            available_query_columns=response.get('available_query_columns'),
            links=response.get('_links'),
            _ctx=ctx,
        )

    def send_feedback(
        self,
        ground_truth: Union[str, float],
        meta: Optional[Dict[str, Any]] = None,
    ) -> Union['PredictionFeedback', Dict[str, Any]]:
        """
        Send or prepare feedback for this prediction.

        For published models: sends feedback immediately and returns server response.
        For compute models: returns a PredictionFeedback object (call .send() to submit).

        Args:
            ground_truth: The correct label/value
            meta: Optional metadata dict (source, annotator, notes, etc.)

        Returns:
            Server response dict (published models) or PredictionFeedback (compute models)

        Raises:
            ValueError: If prediction_uuid is not available
        """
        if not self.prediction_uuid:
            raise ValueError(
                "Cannot send feedback: prediction_uuid not available. "
                "The server may not have returned a prediction_uuid for this prediction."
            )

        if self._published_predictor:
            # Published model: delegate to PublishedPredictor.send_feedback()
            return self._published_predictor.send_feedback(
                prediction_uuid=self.prediction_uuid,
                ground_truth=ground_truth,
                meta=meta,
            )

        # Compute model: create PredictionFeedback (call .send() to submit)
        return PredictionFeedback(
            prediction_uuid=self.prediction_uuid,
            ground_truth=ground_truth,
            session_id=self.session_id,
            meta=meta,
            _ctx=self._ctx,
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        result = {
            'prediction_uuid': self.prediction_uuid,
            'prediction': self.prediction,
            'predicted_class': self.predicted_class,
            'predicted_labels': self.predicted_labels,
            'probability': self.probability,
            'confidence': self.confidence,
            'probabilities': self.probabilities,
            'threshold': self.threshold,
            'query_record': self.query_record,
            'predictor_id': self.predictor_id,
            'session_id': self.session_id,
            'pos_label': self.pos_label,
            'target_column': self.target_column,
            'value_meaning': self.value_meaning,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'model_version': self.model_version,
            # Documentation
            'readme_prediction': self.readme_prediction,
            'readme_probability': self.readme_probability,
            'readme_confidence': self.readme_confidence,
            'readme_threshold': self.readme_threshold,
            'readme_probabilities': self.readme_probabilities,
            'readme_pos_label': self.readme_pos_label,
        }
        # Include model_type if present
        if self.model_type:
            result['model_type'] = self.model_type
        # Include regression uncertainty fields if present (sigma + conformal
        # interval at coverage_level — all four are populated together by the
        # post-hoc calibrator on regression SPs).
        if self.sigma is not None:
            result['sigma'] = self.sigma
        if self.interval_low is not None:
            result['interval_low'] = self.interval_low
        if self.interval_high is not None:
            result['interval_high'] = self.interval_high
        if self.coverage_level is not None:
            result['coverage_level'] = self.coverage_level
        # Include checkpoint_info if present
        if self.checkpoint_info:
            result['checkpoint_info'] = self.checkpoint_info
        if self.seconds_age_of_current_checkpoint is not None:
            result['seconds_age_of_current_checkpoint'] = self.seconds_age_of_current_checkpoint
        if self.seconds_to_next_checkpoint is not None:
            result['seconds_to_next_checkpoint'] = self.seconds_to_next_checkpoint
        # Include guardrails if present
        if self.guardrails:
            result['guardrails'] = self.guardrails
        if self.ignored_query_columns:
            result['ignored_query_columns'] = self.ignored_query_columns
        if self.available_query_columns:
            result['available_query_columns'] = self.available_query_columns
        if self.feature_importance:
            result['feature_importance'] = self.feature_importance
        if self.links:
            result['_links'] = self.links
        return result


@dataclass
class PredictionFeedback:
    """
    Represents feedback (ground truth) for a prediction.

    Usage:
        # Method 1: From PredictionResult
        result = predictor.predict(record)
        feedback = result.send_feedback(ground_truth="correct_label")
        feedback.send()

        # Method 2: Create directly
        feedback = PredictionFeedback(
            prediction_uuid="123e4567-e89b-12d3-a456-426614174000",
            ground_truth="correct_label"
        )
        feedback.send()

        # Method 3: Create and send in one call
        PredictionFeedback.create_and_send(
            ctx=client_context,
            prediction_uuid="123e4567-...",
            ground_truth="correct_label"
        )
    """

    prediction_uuid: str
    ground_truth: Union[str, float]
    feedback_timestamp: Optional[datetime] = None
    # The session that served the prediction. When known, feedback goes to
    # that session's audit-table route — see send().
    session_id: Optional[str] = None
    meta: Optional[Dict[str, Any]] = None

    # Internal: client context for sending
    _ctx: Optional['ClientContext'] = field(default=None, repr=False)

    def send(self) -> Dict[str, Any]:
        """
        Submit feedback to the server.

        Returns:
            Server response

        Raises:
            ValueError: If no client context available
        """
        if not self._ctx:
            raise ValueError(
                "Cannot send feedback: no client context. "
                "Create feedback from a PredictionResult or use create_and_send()."
            )

        self.feedback_timestamp = datetime.now()

        if self.session_id:
            # A session /predict call's prediction_uuid is issued by
            # sphere-api, which writes the durable audit row to the Supabase
            # predictions table (route_proxy.proxy_single_predictor_predict).
            # That uuid never exists in the compute node's own prediction
            # store, so the node-side update_label route below can't find it —
            # feedback on session predictions was silently lost. This route
            # records it on the audit row (same writer as published models).
            body: Dict[str, Any] = {"ground_truth": str(self.ground_truth)}
            if self.meta is not None:
                body["meta"] = self.meta
            return self._ctx.post_json(
                f"/compute/session/{self.session_id}/predict/{self.prediction_uuid}/feedback",
                data=body,
            )

        # No session known (a bare prediction_uuid): the node-side label store
        # is the only route that can resolve it without a session.
        response = self._ctx.post_json(
            f"/compute/prediction/{self.prediction_uuid}/update_label",
            data={"prediction_id": self.prediction_uuid, "user_label": str(self.ground_truth)}
        )
        return response

    @classmethod
    def create_and_send(
        cls,
        ctx: 'ClientContext',
        prediction_uuid: str,
        ground_truth: Union[str, float],
        session_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Create and send feedback in one call.

        Args:
            ctx: Client context
            prediction_uuid: UUID of the prediction
            ground_truth: Correct label/value
            session_id: Session that served the prediction, when known —
                routes feedback onto that prediction's audit row.

        Returns:
            Server response
        """
        feedback = cls(
            prediction_uuid=prediction_uuid,
            ground_truth=ground_truth,
            session_id=session_id,
            _ctx=ctx,
        )
        return feedback.send()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            'prediction_uuid': self.prediction_uuid,
            'ground_truth': self.ground_truth,
            'feedback_timestamp': self.feedback_timestamp.isoformat() if self.feedback_timestamp else None,
        }
