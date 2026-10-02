#  -*- coding: utf-8 -*-
#
#  Copyright (c) 2023-2026 Featrix, Inc, All Rights Reserved
#
#  Proprietary and Confidential.  Unauthorized use, copying or dissemination
#  of these materials is strictly prohibited.
#

"""
APIEndpoint class for FeatrixSphere API.

An endpoint is a stable, named, API-keyed place to get predictions. It
answers with ONE serving model; other versions can shadow it -- they receive
the same requests after the answer is sent, are graded against the same
ground truth, and serve only once promoted. An endpoint can also be bound to
a published model name, so a retrain of that name shadows before it serves.
"""

import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, TYPE_CHECKING

from .http_client import customer_metadata_headers

if TYPE_CHECKING:
    from .http_client import ClientContext
    from .prediction_result import PredictionResult

logger = logging.getLogger(__name__)

# Calls that create or rotate something: a retry after a response was lost
# would do it twice (e.g. two endpoints, or a second key that invalidates the
# one the caller just got), so they are sent exactly once.
_ONCE = 1


def _ts(value: Optional[str]) -> Optional[datetime]:
    return datetime.fromisoformat(value) if value else None


@dataclass
class APIEndpoint:
    """
    A named API endpoint.

    Attributes:
        id: Endpoint ID
        name: Endpoint name
        description: Endpoint description
        target_column: The column this endpoint predicts
        bound_model: "org/name" of the published model this endpoint serves,
            or None for an endpoint reachable only at `predict_url`
        serving_predictor_id: The predictor that answers
        shadows: Versions receiving the same traffic, never answering --
            [{neural_function_id, org, name, activated_at}]
        comparisons: Serving vs each shadow on the same labelled requests
            (filled by `refresh()` / `client.api_endpoint()`)
        models: Every model ever attached (retired rows are the history)
        has_api_key: Whether the endpoint has a key (calls need one)
        api_key: The plaintext key -- only right after create / regenerate
        predict_url: URL third parties call with the endpoint's key
        usage_count, last_used_at, created_at
        publishing: Right after create, when the predictor wasn't published
            yet: {publish_name, job_id, status, error} -- the endpoint answers
            once that publish lands

    Usage:
        endpoint = predictor.create_api_endpoint(name="production_api")
        print(endpoint.api_key)            # shown once
        result = endpoint.predict({"age": 35, "income": 50000})

        endpoint = client.bind_api_endpoint("churn")   # serve a published name
        endpoint.shadow(new_predictor_id)               # evaluate a retrain
        endpoint.refresh(); endpoint.comparisons        # how it does live
        endpoint.promote(new_predictor_id)              # make it serve
    """

    id: str
    name: str
    description: Optional[str] = None
    target_column: Optional[str] = None
    bound_model: Optional[str] = None
    serving_predictor_id: Optional[str] = None
    shadows: List[Dict[str, Any]] = field(default_factory=list)
    comparisons: List[Dict[str, Any]] = field(default_factory=list)
    models: List[Dict[str, Any]] = field(default_factory=list)
    plan_error: Optional[str] = None
    has_api_key: bool = False
    api_key: Optional[str] = None
    api_key_created_at: Optional[datetime] = None
    predict_url: Optional[str] = None
    created_at: Optional[datetime] = None
    last_used_at: Optional[datetime] = None
    usage_count: int = 0
    publishing: Optional[Dict[str, Any]] = None

    # Internal
    _ctx: Optional['ClientContext'] = field(default=None, repr=False)

    @classmethod
    def from_response(cls, response: Dict[str, Any], ctx: Optional['ClientContext'] = None) -> 'APIEndpoint':
        """Create an APIEndpoint from a /endpoints response."""
        plan = response.get('plan') or {}
        bound = (
            f"{response['bound_org_slug']}/{response['bound_model_name']}"
            if response.get('bound_org_slug') and response.get('bound_model_name') else None
        )
        return cls(
            id=response.get('id', ''),
            name=response.get('name', ''),
            description=response.get('description'),
            target_column=response.get('target_column'),
            bound_model=bound,
            serving_predictor_id=response.get('serving_predictor_id'),
            shadows=list(plan.get('shadows') or []),
            comparisons=list(response.get('comparisons') or []),
            models=list(response.get('models') or []),
            plan_error=response.get('plan_error'),
            has_api_key=bool(response.get('has_api_key') or response.get('api_key')),
            api_key=response.get('api_key'),
            api_key_created_at=_ts(response.get('api_key_created_at')),
            predict_url=response.get('predict_url'),
            created_at=_ts(response.get('created_at')),
            last_used_at=_ts(response.get('last_used_at')),
            usage_count=response.get('usage_count') or 0,
            publishing=response.get('publishing'),
            _ctx=ctx,
        )

    def _require_ctx(self) -> 'ClientContext':
        if not self._ctx:
            raise ValueError("APIEndpoint not connected to client")
        return self._ctx

    def _update_from(self, response: Dict[str, Any]) -> 'APIEndpoint':
        fresh = APIEndpoint.from_response(response, self._ctx)
        key = self.api_key  # a fresh read never carries the plaintext key
        for name in self.__dataclass_fields__:
            if name != '_ctx':
                setattr(self, name, getattr(fresh, name))
        if self.has_api_key and self.api_key is None:
            self.api_key = key
        return self

    def refresh(self) -> 'APIEndpoint':
        """Re-read the endpoint: serving model, shadows, and the serving-vs-shadow
        comparison on the same labelled requests."""
        return self._update_from(self._require_ctx().get_json(f"/endpoints/{self.id}"))

    def predict(self, record: Dict[str, Any], api_key: Optional[str] = None,
                customer_metadata: Optional[Dict[str, Any]] = None) -> 'PredictionResult':
        """
        Make a prediction via this endpoint (authenticated by the endpoint's
        own key -- `api_key` overrides the one this object holds).
        `customer_metadata`: optional dict of your own ids/labels stored with
        the prediction for tracing -- never sent to the model.

        Example:
            result = endpoint.predict({"age": 35, "income": 50000}, api_key="fx_ep_...")
            print(result.predicted_class)
        """
        ctx = self._require_ctx()
        from .prediction_result import PredictionResult

        cleaned_record = self._clean_record(record)
        headers = customer_metadata_headers(customer_metadata)
        key_to_use = api_key or self.api_key
        if key_to_use:
            headers['X-API-Key'] = key_to_use
        response = ctx.post_json(
            f"/endpoint/{self.id}/predict",
            data={"query_record": cleaned_record},
            headers=headers,
        )
        self.usage_count += 1
        self.last_used_at = datetime.now()
        return PredictionResult.from_response(response, cleaned_record, ctx)

    def regenerate_api_key(self) -> str:
        """Issue a new API key; the old one stops working. Returns the new key
        (shown once)."""
        response = self._require_ctx().post_json(
            f"/endpoints/{self.id}/regenerate_key", data={}, max_retries=_ONCE,
        )
        self.api_key = response.get('api_key')
        self.has_api_key = bool(self.api_key)
        self.api_key_created_at = datetime.now()
        return self.api_key or ""

    def revoke_api_key(self) -> None:
        """Remove the endpoint's API key. Every predict() call is refused until
        a new key is generated -- this disables the endpoint, it does not make
        it public."""
        self._require_ctx().post_json(f"/endpoints/{self.id}/revoke_key", data={})
        self.api_key = None
        self.has_api_key = False
        self.api_key_created_at = None

    def get_usage_stats(self) -> Dict[str, Any]:
        """Calls made directly to this endpoint's predict URL."""
        response = self._require_ctx().get_json(f"/endpoints/{self.id}/stats")
        self.usage_count = response.get('usage_count', self.usage_count)
        self.last_used_at = _ts(response.get('last_used_at')) or self.last_used_at
        return response

    def shadow(self, predictor_id: str, session_id: Optional[str] = None,
               target_column: Optional[str] = None) -> Dict[str, Any]:
        """Publish a trained predictor beside the serving model and mirror this
        endpoint's traffic to it (it never answers). Replaces any current shadow.
        session_id/target_column default to the predictor's training record."""
        data: Dict[str, Any] = {"predictor_id": predictor_id}
        if session_id:
            data["session_id"] = session_id
        if target_column:
            data["target_column"] = target_column
        return self._require_ctx().post_json(f"/endpoints/{self.id}/shadow", data=data, max_retries=_ONCE)

    def promote(self, predictor_id: str) -> 'APIEndpoint':
        """Make an active shadow the serving model (the old one is retired in
        the same step)."""
        return self._update_from(self._require_ctx().post_json(
            f"/endpoints/{self.id}/promote", data={"neural_function_id": predictor_id}, max_retries=_ONCE,
        ))

    def stop_shadowing(self, predictor_id: str) -> 'APIEndpoint':
        """Stop mirroring traffic to a shadow (its history is kept)."""
        return self._update_from(self._require_ctx().post_json(
            f"/endpoints/{self.id}/stop_shadowing", data={"neural_function_id": predictor_id},
        ))

    def delete(self) -> None:
        """Delete this endpoint. A bound published name goes back to being
        served by name."""
        self._require_ctx().delete_json(f"/endpoints/{self.id}")

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

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'target_column': self.target_column,
            'bound_model': self.bound_model,
            'serving_predictor_id': self.serving_predictor_id,
            'shadows': self.shadows,
            'comparisons': self.comparisons,
            'models': self.models,
            'plan_error': self.plan_error,
            'has_api_key': self.has_api_key,
            'api_key': self.api_key,
            'api_key_created_at': self.api_key_created_at.isoformat() if self.api_key_created_at else None,
            'predict_url': self.predict_url,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_used_at': self.last_used_at.isoformat() if self.last_used_at else None,
            'usage_count': self.usage_count,
            'publishing': self.publishing,
        }

    def __repr__(self) -> str:
        key_str = ", has_key=True" if self.has_api_key else ""
        bound = f", bound='{self.bound_model}'" if self.bound_model else ""
        return f"APIEndpoint(id='{self.id}', name='{self.name}'{bound}{key_str})"
