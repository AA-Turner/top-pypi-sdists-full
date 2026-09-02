"""Skill identifier library — self-contained Merkle-tree skill fingerprinting.

SYNC WARNING: The algorithm here is duplicated from backend/app/domains/skill_identifier/.
Any changes to hashing, normalization, or tree construction must be mirrored there.
"""

from runlayer_cli.skill_identifier.merkle import MerkleTree, build_merkle_tree
from runlayer_cli.skill_identifier.skill_id import compute_skill_identifier
from runlayer_cli.skill_identifier.types import SkillFileInput, SkillIdentifier

__all__ = [
    "MerkleTree",
    "SkillFileInput",
    "SkillIdentifier",
    "build_merkle_tree",
    "compute_skill_identifier",
]
