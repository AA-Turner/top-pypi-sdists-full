from Bio import Phylo as BioPhylo

from ._hash_name import hash_name


def biopython_pare_tree(
    tree: BioPhylo.BaseTree, max_leaves: int
) -> BioPhylo.BaseTree:
    """Trim the tree to keep only max_leaves leaves, selected based on the hash
    of their names."""

    # create a dictionary to store leaf names and their hashes
    hashes = {leaf.name: hash_name(leaf.name) for leaf in tree.get_terminals()}

    # sort the dictionary by hash value
    sorted_hashes = sorted(hashes.items(), key=lambda item: item[1])

    # keep only max_leaves leaves
    kept_names = {name for name, _ in sorted_hashes[:max_leaves]}

    # Traverse tree, but avoid modifying list during iteration
    while True:
        for clade in tree.find_clades(terminal=True):
            if clade.name not in kept_names:
                # If clade name isn't in kept_names, prune it
                tree.prune(clade)
                break
        else:
            break

    return tree
