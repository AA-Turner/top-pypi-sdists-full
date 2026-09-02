"""Merkle tree construction for content-addressable skill identification."""

from __future__ import annotations

from dataclasses import dataclass

from runlayer_cli.skill_identifier.hashing import sha256_hash


@dataclass(frozen=True)
class MerkleTree:
    root: str
    leaves: list[str]
    layers: list[list[str]]


def build_merkle_tree(leaf_hashes: list[str]) -> MerkleTree:
    """Build a binary Merkle tree from leaf hashes and return the full tree.

    Leaves are NOT sorted here — callers are responsible for ordering.
    If the leaf count is odd, the last leaf is duplicated at each level.
    Single leaf: root == leaf hash. Empty list raises ValueError.
    """
    if not leaf_hashes:
        raise ValueError("Cannot build Merkle tree from empty leaf list")

    layers: list[list[str]] = [list(leaf_hashes)]

    current = list(leaf_hashes)
    while len(current) > 1:
        next_layer: list[str] = []
        for i in range(0, len(current), 2):
            left = current[i]
            right = current[i + 1] if i + 1 < len(current) else current[i]
            next_layer.append(sha256_hash(left + right))
        layers.append(next_layer)
        current = next_layer

    return MerkleTree(root=current[0], leaves=list(leaf_hashes), layers=layers)
