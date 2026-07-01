from __future__ import annotations

import logging
from typing import Any

from cvc.core.database import ContextDatabase
from cvc.core.snapshot import CVCSnapshot

logger = logging.getLogger("cvc.persistence")

def persist_snapshot(db: ContextDatabase, snapshot: CVCSnapshot) -> str:
    """
    Persist a CVCSnapshot to storage following the strict three-tier order:
    1. blob (Tier 2)
    2. escalate (Tier 1 - Index)
    3. Chroma DB (Tier 3 - Semantic)

    This function ensures data integrity across the context database tiers.
    """
    
    # --- 1. BLOB (Tier 2: Content-Addressable Storage) ---
    # We store the full snapshot as a JSON blob in the CAS.
    blob_key = db.blobs.put_json(snapshot.to_dict())
    logger.debug(f"Snapshot blob stored with key: {blob_key}")

    # --- 2. ESCALATE (Tier 1: SQLite Index) ---
    # 'Escalating' the metadata from the raw blob to the searchable SQLite index.
    db.index._conn.execute(
        """INSERT OR REPLACE INTO commits
           (commit_hash, parent_hashes, commit_type, message,
            is_delta, anchor_hash, blob_key, metadata_json, created_at)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            snapshot.commit_hash,
            "[]",
            "checkpoint",
            snapshot.message,
            int(not snapshot.is_anchor),
            None,
            blob_key,
            snapshot.to_json(),
            snapshot.timestamp,
        ),
    )
    db.index._conn.commit()
    logger.debug(f"Snapshot {snapshot.short_hash} escalated to SQLite index.")

    # --- 3. CHROMA DB (Tier 3: Semantic Vector Store) ---
    # Finally, index the snapshot in Chroma for similarity search.
    if db.vectors.available:
        doc_parts = [snapshot.message]
        if snapshot.metadata.get("distilled_summary"):
            doc_parts.append(f"Distilled: {snapshot.metadata['distilled_summary']}")
        
        document_text = "\\n".join(doc_parts)
        
        db.vectors.add(
            snapshot.commit_hash,
            document_text,
            {
                "author": snapshot.author,
                "branch": snapshot.branch,
                "ts": snapshot.timestamp,
                "tags": ",".join(snapshot.tags) if snapshot.tags else "",
                "is_anchor": int(snapshot.is_anchor),
                "summary_tokens": snapshot.summary_tokens,
                "type": "snapshot",
            }
        )
        logger.debug(f"Snapshot {snapshot.short_hash} indexed in Chroma DB.")

    logger.info(f"Successfully persisted snapshot {snapshot.short_hash} across all tiers.")
    return snapshot.commit_hash
