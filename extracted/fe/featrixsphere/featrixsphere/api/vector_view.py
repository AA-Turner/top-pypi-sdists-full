#  -*- coding: utf-8 -*-
#
#  Copyright (c) 2023-2026 Featrix, Inc, All Rights Reserved
#
#  Proprietary and Confidential.  Unauthorized use, copying or dissemination
#  of these materials is strictly prohibited.
#

"""
VectorView class for FeatrixSphere API.

Represents a SphereViewer-ready vector view with target coloring and linear probe results.
"""

import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, Optional, List, Union, TYPE_CHECKING

if TYPE_CHECKING:
    from .http_client import ClientContext
    from .foundational_model import FoundationalModel
    import pandas as pd

logger = logging.getLogger(__name__)


def _parse_datetime(value) -> Optional[datetime]:
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


@dataclass
class VectorView:
    """
    A SphereViewer-ready vector view with target coloring and linear probe.

    Created by encoding records through a trained ES.  Provides an immediate
    viewer URL and linear probe baseline — no SP training required.

    Usage:
        # Create a vector view
        view = fm.create_vector_view(
            records=df.to_dict('records'),
            target_column="credit_risk"
        )

        # Viewer URL is available immediately
        print(view.viewer_url)

        # Linear probe results (instant, from sklearn)
        print(view.linear_probe_score)
        print(view.linear_probe)

        # Get projections with custom K
        projections = view.get_projections(k=4)
    """

    session_id: str
    name: str
    target_column: str
    target_type: Optional[str] = None
    class_labels: Optional[List[str]] = None
    record_count: int = 0
    viewer_url: Optional[str] = None
    linear_probe: Optional[Dict[str, Any]] = None
    created_at: Optional[datetime] = None
    source: Optional[str] = None

    # Internal
    _ctx: Optional['ClientContext'] = field(default=None, repr=False)
    _foundational_model: Optional['FoundationalModel'] = field(default=None, repr=False)

    @classmethod
    def from_api_response(
        cls,
        data: dict,
        session_id: str,
        ctx: Optional['ClientContext'] = None,
        foundational_model: Optional['FoundationalModel'] = None,
    ) -> 'VectorView':
        """Create VectorView from server response JSON."""
        return cls(
            session_id=session_id,
            name=data.get("name", ""),
            target_column=data.get("target_column", ""),
            target_type=data.get("target_type"),
            class_labels=data.get("class_labels"),
            record_count=data.get("record_count", 0),
            viewer_url=data.get("viewer_url"),
            linear_probe=data.get("linear_probe"),
            created_at=_parse_datetime(data.get("created_at")),
            source=data.get("source"),
            _ctx=ctx,
            _foundational_model=foundational_model,
        )

    @property
    def linear_probe_score(self) -> Optional[float]:
        """The headline probe score (AUC for classification, R² for regression)."""
        if self.linear_probe:
            return self.linear_probe.get("score")
        return None

    @property
    def linear_probe_auc(self) -> Optional[float]:
        """AUC from linear probe (classification only)."""
        if self.linear_probe:
            return self.linear_probe.get("auc")
        return None

    @property
    def foundational_model(self) -> Optional['FoundationalModel']:
        """Get the parent foundational model."""
        return self._foundational_model

    def get_projections(self, k: Optional[int] = None) -> Dict[str, Any]:
        """Get SphereViewer-compatible projections.

        Args:
            k: Number of clusters (optional, uses best K if omitted)

        Returns:
            Projections dict with coords, available_k, cluster info, target metadata
        """
        if not self._ctx:
            raise ValueError("VectorView not connected to client")

        params = {}
        if k is not None:
            params["k"] = k

        response = self._ctx.get_json(
            f"/session/{self.session_id}/vector_views/{self.name}/projections",
            params=params,
        )
        return response.get("projections", {})

    def get_linear_probe_details(self) -> Dict[str, Any]:
        """Get detailed linear probe results (per-class precision/recall)."""
        if not self._ctx:
            raise ValueError("VectorView not connected to client")

        return self._ctx.get_json(
            f"/session/{self.session_id}/vector_views/{self.name}/linear_probe",
        )

    def append_records(
        self,
        records: Union[List[Dict[str, Any]], 'pd.DataFrame'],
        batch_size: int = 500,
    ) -> 'VectorView':
        """Add more records to this vector view.

        Args:
            records: List of record dicts or DataFrame
            batch_size: Batch size for uploads

        Returns:
            Self (updated record count)
        """
        if not self._ctx:
            raise ValueError("VectorView not connected to client")

        if hasattr(records, 'to_dict'):
            records = records.to_dict('records')

        total_added = 0
        for i in range(0, len(records), batch_size):
            batch = records[i:i + batch_size]
            response = self._ctx.post_json(
                f"/session/{self.session_id}/vector_views/{self.name}/append",
                data={"records": batch},
            )
            total_added += response.get("records_added", 0)

        self.record_count += total_added
        return self

    def refresh(self) -> 'VectorView':
        """Refresh metadata from server (e.g., after SP training enriches the view)."""
        if not self._ctx:
            raise ValueError("VectorView not connected to client")

        data = self._ctx.get_json(
            f"/session/{self.session_id}/vector_views/{self.name}",
        )
        self.record_count = data.get("record_count", self.record_count)
        self.linear_probe = data.get("linear_probe", self.linear_probe)
        self.viewer_url = data.get("viewer_url", self.viewer_url)
        return self

    def delete(self) -> None:
        """Delete this vector view from the server."""
        if not self._ctx:
            raise ValueError("VectorView not connected to client")

        self._ctx.delete_json(
            f"/session/{self.session_id}/vector_views/{self.name}"
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            'session_id': self.session_id,
            'name': self.name,
            'target_column': self.target_column,
            'target_type': self.target_type,
            'class_labels': self.class_labels,
            'record_count': self.record_count,
            'viewer_url': self.viewer_url,
            'linear_probe': self.linear_probe,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'source': self.source,
        }

    def __repr__(self) -> str:
        score = self.linear_probe_score
        score_str = f", score={score}" if score is not None else ""
        return (f"VectorView(name='{self.name}', target='{self.target_column}', "
                f"records={self.record_count}{score_str})")
