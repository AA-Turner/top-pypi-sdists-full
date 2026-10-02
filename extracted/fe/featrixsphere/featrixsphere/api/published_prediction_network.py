#  -*- coding: utf-8 -*-
#
#  Copyright (c) 2023-2026 Featrix, Inc, All Rights Reserved
#
#  Proprietary and Confidential.  Unauthorized use, copying or dissemination
#  of these materials is strictly prohibited.
#

"""
PublishedPredictionNetwork class for FeatrixSphere API.

A PredictionNetwork is a customer-registered chain of their own published
models: output of one node (label / confidence / value) gates whether
downstream nodes run. See
docs/internal/plans/2026-07-prediction-networks.md in the main repo for
the full design.

This mirrors PublishedPredictor's shape deliberately — same dataclass
fields, same _clean_record handling, same base_url default — but takes
its own base_url separately (not shared with PublishedPredictor's) so
that pointing PredictionNetwork calls at a different host later (e.g.
if this feature moves off sphere-api to its own service) is a config
change, not an API-shape change.
"""

import math
import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .http_client import ClientContext

logger = logging.getLogger(__name__)


@dataclass
class PredictionNetworkTraceEntry:
    """One node's execution record from a PredictionNetwork run."""
    node_id: str
    model: Optional[str] = None
    label: Optional[Any] = None
    confidence: Optional[float] = None
    latency_ms: Optional[float] = None
    skipped: bool = False
    skip_reason: Optional[str] = None
    error: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PredictionNetworkTraceEntry":
        return cls(
            node_id=data.get("node_id"),
            model=data.get("model"),
            label=data.get("label"),
            confidence=data.get("confidence"),
            latency_ms=data.get("latency_ms"),
            skipped=bool(data.get("skipped", False)),
            skip_reason=data.get("skip_reason"),
            error=data.get("error"),
        )


@dataclass
class PredictionNetworkResult:
    """Result of executing a PredictionNetwork against one record.

    ``final`` maps each terminal node's id to its output (label,
    confidence, probabilities); ``trace`` is every node the chain
    touched, in execution order, including skipped branches with their
    ``skip_reason`` — this is what makes the chain inspectable instead
    of a black box.
    """
    final: Dict[str, Any]
    trace: List[PredictionNetworkTraceEntry]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PredictionNetworkResult":
        return cls(
            final=data.get("final", {}),
            trace=[PredictionNetworkTraceEntry.from_dict(t) for t in data.get("trace", [])],
        )


@dataclass
class PublishedPredictionNetwork:
    """
    Represents a PredictionNetwork deployed to production for serving
    composed, chained predictions across several of your own published
    models.

    Attributes:
        org: Organization ID
        name: PredictionNetwork name
        api_key: API key for authentication
        base_url: Sphere API URL (default: https://sphere-api.featrix.com)

    Usage:
        network = client.published_prediction_network(
            org="alph",
            name="carrier-qualification",
            api_key="sk_alph_xxx",
        )

        # Register/update the chain (nodes reference your own published models)
        network.register({
            "nodes": [
                {"id": "is_company", "model": "is-company"},
                {"id": "company_type", "model": "company-type"},
            ],
            "edges": [
                {"from": "is_company", "to": "company_type", "when": {"op": "always"}},
            ],
        })

        result = network.predict({"company_name": "Acme Trucking Co"})
        print(result.final)
        for entry in result.trace:
            print(entry.node_id, entry.label, entry.skipped, entry.skip_reason)
    """

    org: str
    name: str
    api_key: str
    base_url: str = "https://sphere-api.featrix.com"

    # Internal
    _ctx: Optional['ClientContext'] = field(default=None, repr=False)

    @property
    def endpoint_url(self) -> str:
        """Registration (PUT/GET) and execution (POST) share this URL."""
        return f"{self.base_url}/prediction-network/{self.org}/{self.name}"

    def register(self, spec: Dict[str, Any]) -> Dict[str, Any]:
        """
        Register or update this PredictionNetwork's spec.

        Args:
            spec: {"nodes": [{"id", "model"}, ...],
                   "edges": [{"from", "to", "when": {"op", "field"?, "value"?}}, ...]}

        Returns:
            {"org", "name", "version", "nodes"} on success.
        """
        import requests
        headers = {"X-API-Key": self.api_key, "Content-Type": "application/json"}
        response = requests.put(self.endpoint_url, json=spec, headers=headers, timeout=30)
        if response.status_code != 200:
            raise RuntimeError(self._error_message(response))
        return response.json()

    def get_spec(self) -> Dict[str, Any]:
        """Fetch this PredictionNetwork's currently registered spec."""
        import requests
        headers = {"X-API-Key": self.api_key}
        response = requests.get(self.endpoint_url, headers=headers, timeout=30)
        if response.status_code != 200:
            raise RuntimeError(self._error_message(response))
        return response.json()

    def delete(self) -> Dict[str, Any]:
        """Delete this PredictionNetwork's registered spec."""
        import requests
        headers = {"X-API-Key": self.api_key}
        response = requests.delete(self.endpoint_url, headers=headers, timeout=30)
        if response.status_code != 200:
            raise RuntimeError(self._error_message(response))
        return response.json()

    def predict(self, record: Dict[str, Any]) -> PredictionNetworkResult:
        """
        Execute the chain against one record.

        v1 executes exactly one record per call — batch semantics are not
        yet implemented (see the plan doc's open questions).

        Example:
            result = network.predict({"company_name": "Acme Trucking Co"})
            print(result.final)       # terminal node outputs
            print(result.trace)       # every node touched, including skipped ones
        """
        import requests

        cleaned_record = self._clean_record(record)
        headers = {"X-API-Key": self.api_key, "Content-Type": "application/json"}
        response = requests.post(
            self.endpoint_url,
            json={"records": [cleaned_record]},
            headers=headers,
            timeout=300,
        )
        if response.status_code != 200:
            raise RuntimeError(self._error_message(response))
        return PredictionNetworkResult.from_dict(response.json())

    def _clean_record(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """Clean a record for API submission — mirrors PublishedPredictor._clean_record."""
        cleaned = {}
        for key, value in record.items():
            if isinstance(value, float):
                if math.isnan(value) or math.isinf(value):
                    value = None
            if hasattr(value, 'item'):
                value = value.item()
            cleaned[key] = value
        return cleaned

    def _error_message(self, response) -> str:
        try:
            data = response.json()
            return data.get('error', f'HTTP {response.status_code}')
        except Exception:
            return response.text or f'HTTP {response.status_code}'

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            'org': self.org,
            'name': self.name,
            'base_url': self.base_url,
            'endpoint_url': self.endpoint_url,
        }

    def __repr__(self) -> str:
        return f"PublishedPredictionNetwork(org='{self.org}', name='{self.name}')"
