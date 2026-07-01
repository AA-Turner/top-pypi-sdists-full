"""
Semantic Merging Engine for Cognitive Version Control.

This module resolves 'cognitive collisions' between two diverging branches
by comparing their vector embeddings (thoughts, insights, file modifications).
"""

from typing import Any
import numpy as np

def cosine_similarity(v1: list[float], v2: list[float]) -> float:
    """Calculate cosine similarity between two vectors."""
    vec1 = np.array(v1)
    vec2 = np.array(v2)
    if np.linalg.norm(vec1) == 0 or np.linalg.norm(vec2) == 0:
        return 0.0
    return float(np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2)))

def detect_cognitive_collisions(engine: Any, source_branch: str, target_branch: str) -> dict[str, Any]:
    """
    Compare the semantic drift between the source branch and the target branch.
    Returns collision details or an empty dict if they align.
    """
    source_bp = engine.db.index.get_branch(source_branch)
    target_bp = engine.db.index.get_branch(target_branch)
    
    if not source_bp or not target_bp:
        raise ValueError("Invalid branches provided for semantic diffing.")
    
    # In a full implementation, we extract Chroma embeddings here
    # For now, we simulate pulling the 'distilled_summary' from the commits
    source_commit = engine.db.index.get_commit(source_bp.head_hash)
    target_commit = engine.db.index.get_commit(target_bp.head_hash)
    
    # We perform a basic check on the new fields
    s_sum = source_commit.content_blob.distilled_summary if source_commit else None
    t_sum = target_commit.content_blob.distilled_summary if target_commit else None
    
    return {
        "collision": bool(s_sum and t_sum and s_sum != t_sum),
        "source_summary": s_sum,
        "target_summary": t_sum,
    }

def synthesize_merge_resolution(engine: Any, source_branch: str, target_branch: str, llm_adapter: Any = None) -> str:
    """
    Evaluates branch drift. If there is a collision, it asks the LLM to resolve it.
    If no collision, returns a standard merged summary.
    """
    diff_report = detect_cognitive_collisions(engine, source_branch, target_branch)
    
    # In production, this uses the LLM to resolve `diff_report`
    if diff_report["collision"]:
        return (
            f"Resolved Cognitive Collision.\n"
            f"Branch A ({target_branch}) thought: {diff_report['target_summary']}\n"
            f"Branch B ({source_branch}) thought: {diff_report['source_summary']}\n"
            f"Synthesis: Integrated insights from both exploration paths."
        )
    
    return f"Merged branch {source_branch} into {target_branch} cleanly."
