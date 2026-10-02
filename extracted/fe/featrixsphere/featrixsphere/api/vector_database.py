#  -*- coding: utf-8 -*-
#
#  Copyright (c) 2023-2026 Featrix, Inc, All Rights Reserved
#
#  Proprietary and Confidential.  Unauthorized use, copying or dissemination
#  of these materials is strictly prohibited.
#

"""
VectorDatabase class for FeatrixSphere API.

Represents a named vector database for cosine similarity search.
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
class VectorDatabase:
    """
    A named vector database for cosine similarity search.

    Each VDB belongs to a foundational model (embedding space) and stores
    records as embedding vectors in LanceDB. Multiple named VDBs can exist
    per foundational model.

    Usage:
        # Create from foundational model (auto-populates with training data)
        vdb = fm.create_vector_database("customers")

        # Create empty, fill manually
        vdb = fm.create_vector_database("vip_only", auto_populate=False)
        vdb.add_records(vip_records)

        # Similarity search with optional SQL WHERE filter
        similar = vdb.similarity_search(
            {"age": 35, "income": 50000},
            k=5,
            where="region = 'west'"
        )

        # Retrieve later
        vdb = fm.get_vector_database("customers")
        all_vdbs = fm.list_vector_databases()
    """

    session_id: str
    name: str
    record_count: int = 0
    auto_populated: bool = True
    created_at: Optional[datetime] = None

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
    ) -> 'VectorDatabase':
        """Create VectorDatabase from server response JSON."""
        return cls(
            session_id=session_id,
            name=data.get("name", "default"),
            record_count=data.get("record_count", 0),
            auto_populated=data.get("auto_populated", True),
            created_at=_parse_datetime(data.get("created_at")),
            _ctx=ctx,
            _foundational_model=foundational_model,
        )

    @property
    def foundational_model(self) -> Optional['FoundationalModel']:
        """Get the parent foundational model."""
        return self._foundational_model

    def similarity_search(
        self,
        query_record: Dict[str, Any],
        k: int = 10,
        where: Optional[str] = None,
        include_field_similarity: bool = True,
    ) -> List[Dict[str, Any]]:
        """
        Find k most similar records using cosine distance.

        Args:
            query_record: Query record dictionary
            k: Number of similar records to return
            where: Optional SQL WHERE clause for pre-filtering
                   (e.g. "region = 'west'" or "age > 30")
            include_field_similarity: Compute per-field similarity scores

        Returns:
            List of result dicts with distance, original_data, field_similarity

        Example:
            similar = vdb.similarity_search(
                {"age": 35, "income": 50000},
                k=5,
                where="region = 'west'"
            )
            for record in similar:
                print(f"Distance: {record['distance']}")
                print(f"Data: {record['original_data']}")
        """
        if not self._ctx:
            raise ValueError("VectorDatabase not connected to client")

        cleaned_query = self._clean_record(query_record)

        payload = {
            "query_record": cleaned_query,
            "k": k,
            "include_field_similarity": include_field_similarity,
        }
        if where is not None:
            payload["where"] = where

        response = self._ctx.post_json(
            f"/session/{self.session_id}/vector_databases/{self.name}/search",
            data=payload,
        )

        return response.get('results', [])

    def add_records(
        self,
        records: Union[List[Dict[str, Any]], 'pd.DataFrame'],
        batch_size: int = 500,
    ) -> 'VectorDatabase':
        """
        Add records to the vector database.

        Args:
            records: List of record dictionaries or DataFrame
            batch_size: Batch size for adding records

        Returns:
            Self (updated record count)
        """
        if not self._ctx:
            raise ValueError("VectorDatabase not connected to client")

        # Convert DataFrame to list if needed
        if hasattr(records, 'to_dict'):
            records = records.to_dict('records')

        cleaned_records = [self._clean_record(r) for r in records]

        total_added = 0
        for i in range(0, len(cleaned_records), batch_size):
            batch = cleaned_records[i:i + batch_size]

            response = self._ctx.post_json(
                f"/session/{self.session_id}/vector_databases/{self.name}/records",
                data={"records": batch},
            )

            added = response.get('records_added', len(batch))
            total_added += added

        self.record_count += total_added
        return self

    def size(self) -> int:
        """Get the current number of records in the database."""
        if not self._ctx:
            raise ValueError("VectorDatabase not connected to client")

        response = self._ctx.get_json(
            f"/session/{self.session_id}/vector_databases/{self.name}/size"
        )
        self.record_count = response.get('size', 0)
        return self.record_count

    def delete(self) -> None:
        """Delete this vector database from the server."""
        if not self._ctx:
            raise ValueError("VectorDatabase not connected to client")

        self._ctx.delete_json(
            f"/session/{self.session_id}/vector_databases/{self.name}"
        )

    def encode(
        self,
        records: Union[Dict[str, Any], List[Dict[str, Any]], 'pd.DataFrame'],
        *,
        intent: Optional[str] = None,
        representation: str = "auto",
        expected_missing: Optional[List[str]] = None,
    ) -> List[List[float]]:
        """
        Encode records to embedding vectors.

        Args:
            records: Single record, list of records, or DataFrame
            intent: Customer-facing intent — one of 'clustering' (default
                   for vector-DB use cases: kNN / similarity), 'visualization',
                   'near_lossless', 'highly_encoded'. When None, the
                   legacy full-length embedding is returned.
            representation: 'auto', 'preserved', or 'compressed'. Ignored
                   unless intent is given.
            expected_missing: Column names you are INTENTIONALLY omitting from
                   these records (e.g. fields you simply don't have). Declaring
                   them tells the server the absence is by design, so it won't
                   warn about a column mismatch. Only columns you didn't declare
                   — and didn't supply — are flagged.

        Returns:
            List of embedding vectors. When intent is given, the vector
            shape matches the intent's resolved port.
        """
        if not self._ctx:
            raise ValueError("VectorDatabase not connected to client")

        if isinstance(records, dict):
            records = [records]
        elif hasattr(records, 'to_dict'):
            records = records.to_dict('records')

        cleaned_records = [self._clean_record(r) for r in records]

        body: Dict[str, Any] = {"records": cleaned_records}
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
        # With intent, server returns 'embedding' in the resolved shape.
        # Without intent (legacy), prefer embedding_long then embedding.
        if intent is not None:
            return [r.get('embedding') for r in results]
        return [r.get('embedding_long', r.get('embedding')) for r in results]

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
            'session_id': self.session_id,
            'name': self.name,
            'record_count': self.record_count,
            'auto_populated': self.auto_populated,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self) -> str:
        return f"VectorDatabase(name='{self.name}', session='{self.session_id}', records={self.record_count})"
