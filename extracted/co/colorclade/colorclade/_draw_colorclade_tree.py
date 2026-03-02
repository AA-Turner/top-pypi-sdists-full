import typing

import alifedata_phyloinformatics_convert as apc
from matplotlib.axes import Axes as mpl_Axes
import pandas as pd

from ._biopython_draw_colorclade_tree import biopython_draw_colorclade_tree


def draw_colorclade_tree(
    tree: pd.DataFrame,
    backend: typing.Literal["biopython"],
    taxon_name_key: str,
    mutate: bool = False,
    *args,
    **kwargs,
) -> mpl_Axes:
    """Draw a phylogenetic tree given in alife standard as a pandas DataFrame,
    color-coding clades based on descendant labels.

    Labels are mapped to colors using a hash function. Color-coding uses an
    arbitrarily dominant color among the labels of the clade's descendants. The
    criteria used to determine dominance is deterministic, but arbitrary.

    Parameters
    ----------
    tree : pd.DataFrame
        The input phylogenetic tree data in a pandas DataFrame format.
    backend : typing.Literal["biopython"]
        The backend to use for drawing the phylogenetic tree.

        Currently, only 'biopython' is supported.
    taxon_name_key : str
        The column name in the DataFrame that contains the taxon names, which
        will be used as labels for the tree tips.
    mutate : bool, default False
        Can the input DataFrame be mutated?

        If False, a copy of the input DataFrame is made before drawing the tree.
    *args
        Variable length argument list, passed to the backend drawing function.
    **kwargs
        Arbitrary keyword arguments, passed to the backend drawing function.

    Returns
    -------
    mpl_Axes
        The matplotlib Axes object with the tree drawn.
    """
    if not mutate:
        tree = tree.copy()

    tree["name"] = tree[taxon_name_key]  # biopython expects "name" column

    rosetta_tree = apc.RosettaTree(tree)
    tree = {"biopython": lambda x: x.as_biopython}[backend](rosetta_tree)

    plotter = {"biopython": biopython_draw_colorclade_tree}[backend]
    return plotter(
        tree,
        *args,
        **kwargs,
    )
