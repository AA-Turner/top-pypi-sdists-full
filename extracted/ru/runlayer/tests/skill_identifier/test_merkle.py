import pytest

from runlayer_cli.skill_identifier.merkle import MerkleTree, build_merkle_tree


class TestBuildMerkleTree:
    def test_single_leaf(self):
        tree = build_merkle_tree(["aaa"])
        assert tree.root == "aaa"
        assert tree.leaves == ["aaa"]
        assert tree.layers == [["aaa"]]

    def test_two_leaves(self):
        tree = build_merkle_tree(["aaa", "bbb"])
        assert tree.root != "aaa"
        assert tree.root != "bbb"
        assert len(tree.layers) == 2
        assert tree.layers[0] == ["aaa", "bbb"]
        assert len(tree.layers[1]) == 1

    def test_even_count(self):
        tree = build_merkle_tree(["a", "b", "c", "d"])
        assert len(tree.layers) == 3
        assert len(tree.layers[0]) == 4
        assert len(tree.layers[1]) == 2
        assert len(tree.layers[2]) == 1

    def test_odd_count_duplicates_last(self):
        tree = build_merkle_tree(["a", "b", "c"])
        assert len(tree.layers) == 3
        assert len(tree.layers[0]) == 3
        assert len(tree.layers[1]) == 2
        assert len(tree.layers[2]) == 1

        tree_different = build_merkle_tree(["a", "b", "d"])
        assert tree.root != tree_different.root

    def test_empty_list_raises(self):
        with pytest.raises(ValueError, match="empty"):
            build_merkle_tree([])

    def test_determinism(self):
        leaves = ["hash1", "hash2", "hash3"]
        t1 = build_merkle_tree(leaves)
        t2 = build_merkle_tree(leaves)
        assert t1.root == t2.root
        assert t1.layers == t2.layers

    def test_order_matters(self):
        t1 = build_merkle_tree(["a", "b"])
        t2 = build_merkle_tree(["b", "a"])
        assert t1.root != t2.root

    def test_returns_merkle_tree_dataclass(self):
        tree = build_merkle_tree(["x"])
        assert isinstance(tree, MerkleTree)
