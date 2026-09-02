"""Compute content-addressable identifiers for skills using a Merkle tree."""

from runlayer_cli.skill_identifier.hashing import hash_fields, normalize_text
from runlayer_cli.skill_identifier.merkle import build_merkle_tree
from runlayer_cli.skill_identifier.types import SkillFileInput, SkillIdentifier


def compute_skill_identifier(files: list[SkillFileInput]) -> SkillIdentifier:
    """Compute a deterministic identifier for a skill from its files.

    Each file produces a leaf hash from its normalized name and content.
    Files are sorted by name for deterministic ordering, then assembled
    into a binary Merkle tree. The root hash is the skill identifier.
    """
    if not files:
        raise ValueError("Cannot compute identifier for skill with no files")

    sorted_files = sorted(files, key=lambda f: normalize_text(f.name))

    names = [normalize_text(f.name) for f in sorted_files]
    if len(names) != len(set(names)):
        raise ValueError("Duplicate file names are not allowed")

    file_hashes: dict[str, str] = {}
    leaf_hashes: list[str] = []
    for f in sorted_files:
        h = hash_fields(f.name, f.content)
        file_hashes[f.name] = h
        leaf_hashes.append(h)

    tree = build_merkle_tree(leaf_hashes)
    return SkillIdentifier(root=tree.root, file_hashes=file_hashes)
