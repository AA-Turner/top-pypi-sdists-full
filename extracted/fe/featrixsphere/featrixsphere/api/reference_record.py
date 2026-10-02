#  -*- coding: utf-8 -*-
#
#  Copyright (c) 2023-2026 Featrix, Inc, All Rights Reserved
#
#  Proprietary and Confidential.  Unauthorized use, copying or dissemination
#  of these materials is strictly prohibited.
#

"""
ReferenceRecord class for FeatrixSphere API.

Represents a reference point in the embedding space for similarity search.
Useful when you only have positive examples and want to find similar records.
"""

import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from .http_client import ClientContext
    from .foundational_model import FoundationalModel
    from .vector_database import VectorDatabase
    import numpy as np

logger = logging.getLogger(__name__)


@dataclass
class ReferenceRecord:
    """
    Represents a reference record in the embedding space.

    A ReferenceRecord is useful when you only have positive examples but no
    negative examples. Instead of training a classifier, you can create a
    reference from a positive example and find similar records.

    Attributes:
        id: ReferenceRecord ID
        name: Optional name
        session_id: Parent session ID
        record: The record this reference represents
        embedding: Cached embedding vector
        created_at: Creation timestamp

    Usage:
        # Create from foundational model
        ref = fm.create_reference_record(
            record={"age": 35, "income": 50000},
            name="target_profile"
        )

        # Find similar records
        similar = ref.find_similar(k=10, vector_database=vdb)

        # Get embedding
        embedding = ref.get_embedding()
    """

    id: str
    session_id: str
    record: Dict[str, Any]
    name: Optional[str] = None
    embedding: Optional[List[float]] = None
    created_at: Optional[datetime] = None

    # Internal
    _ctx: Optional['ClientContext'] = field(default=None, repr=False)
    _foundational_model: Optional['FoundationalModel'] = field(default=None, repr=False)

    @classmethod
    def from_record(
        cls,
        record: Dict[str, Any],
        session_id: str,
        name: Optional[str] = None,
        ctx: Optional['ClientContext'] = None,
        foundational_model: Optional['FoundationalModel'] = None
    ) -> 'ReferenceRecord':
        """
        Create a ReferenceRecord from a record.

        Args:
            record: The record to create reference from
            session_id: Parent session ID
            name: Optional name
            ctx: Client context for API calls
            foundational_model: Parent FM

        Returns:
            ReferenceRecord instance
        """
        import uuid

        ref = cls(
            id=str(uuid.uuid4()),
            session_id=session_id,
            record=record,
            name=name,
            created_at=datetime.now(),
            _ctx=ctx,
            _foundational_model=foundational_model,
        )

        # Pre-compute embedding if we have context
        if ctx:
            try:
                ref._compute_embedding()
            except Exception as e:
                logger.warning(f"Failed to compute embedding for reference record: {e}")

        return ref

    @property
    def foundational_model(self) -> Optional['FoundationalModel']:
        """Get the parent foundational model."""
        return self._foundational_model

    def find_similar(
        self,
        k: int = 10,
        vector_database: Optional['VectorDatabase'] = None
    ) -> List[Dict[str, Any]]:
        """
        Find k records similar to this reference.

        Args:
            k: Number of similar records to return
            vector_database: VectorDatabase to search in. If None, falls back
                           to the foundational model's "default" named vector
                           database (see FoundationalModel.create_vector_database).

        Returns:
            List of similar records with similarity scores

        Example:
            vdb = fm.create_vector_database()  # name="default"
            similar = ref.find_similar(k=10)
            for record in similar:
                print(f"Score: {record['similarity']}")
                print(f"Data: {record['record']}")
        """
        if not self._ctx:
            raise ValueError("ReferenceRecord not connected to client")

        if vector_database is None:
            if not self._foundational_model:
                raise ValueError(
                    "find_similar() with no vector_database requires a ReferenceRecord "
                    "created via FoundationalModel.create_reference_record(); pass "
                    "vector_database= explicitly otherwise."
                )
            vector_database = self._foundational_model.get_vector_database("default")

        return vector_database.similarity_search(self.record, k=k)

    def get_embedding(self) -> List[float]:
        """
        Get the embedding vector for this reference record.

        Returns:
            List of floats representing the embedding vector

        Example:
            embedding = ref.get_embedding()
            print(f"Embedding dimension: {len(embedding)}")
        """
        if self.embedding is not None:
            return self.embedding

        self._compute_embedding()
        return self.embedding or []

    def _compute_embedding(self) -> None:
        """Compute and cache the embedding for this reference's record."""
        if not self._ctx:
            raise ValueError("ReferenceRecord not connected to client")

        cleaned_record = self._clean_record(self.record)

        response = self._ctx.post_json(
            f"/session/{self.session_id}/encode_records",
            data={"records": [cleaned_record]}
        )

        results = response.get('results', [])
        if results:
            self.embedding = results[0].get('embedding_long', results[0].get('embedding'))

    def delete(self) -> None:
        """
        Delete this reference record.

        Note: ReferenceRecords are lightweight and exist only in memory on the client.
        This method clears the reference's data.
        """
        self.record = {}
        self.embedding = None
        self._ctx = None
        self._foundational_model = None

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
            'session_id': self.session_id,
            'name': self.name,
            'record': self.record,
            'embedding_dimension': len(self.embedding) if self.embedding else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self) -> str:
        name_str = f", name='{self.name}'" if self.name else ""
        emb_str = f", dim={len(self.embedding)}" if self.embedding else ""
        return f"ReferenceRecord(id='{self.id}'{name_str}{emb_str})"
