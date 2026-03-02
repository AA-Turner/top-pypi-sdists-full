import typing

from Bio import Phylo as BioPhylo
import opytional as opyt

from ._val_to_color_hls import val_to_color_hls


def biopython_color_tree(
    tree: BioPhylo.BaseTree,
    salt: typing.Optional[int] = None,
    val_to_color: typing.Optional[typing.Callable] = None,
) -> None:
    """Recursively color tree nodes based on dominant color among terminals."""
    if val_to_color is None:
        val_to_color = val_to_color_hls

    name = min(
        (opyt.or_value(y.name, "") for y in tree.get_terminals()),
        default=tree.name,
    )
    tree.color = val_to_color(name, salt=salt)

    for clade in tree.clades:
        biopython_color_tree(clade, salt=salt)
