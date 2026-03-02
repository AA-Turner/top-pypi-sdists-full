from Bio import Phylo as BioPhylo
import opytional as opyt


def biopython_sort_tree(tree: BioPhylo.BaseTree) -> None:
    """Recursively sort clades in-place in the tree based on their terminal
    elements' names."""
    tree.clades.sort(
        key=lambda x: min(
            (opyt.or_value(y.name, "") for y in x.get_terminals()),
            default=opyt.or_value(x.name, ""),
        )
    )

    for clade in tree.clades:
        biopython_sort_tree(clade)
