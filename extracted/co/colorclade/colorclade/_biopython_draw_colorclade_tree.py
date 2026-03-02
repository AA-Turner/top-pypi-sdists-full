from collections import abc
import copy
import typing

from Bio import Phylo as BioPhylo
from Bio.Phylo.BaseTree import Clade as BioClade
from matplotlib import pyplot as plt
from matplotlib.axes import Axes as mpl_Axes

from ._biopython_color_tree import biopython_color_tree as color_tree
from ._biopython_pare_tree import biopython_pare_tree as pare_tree
from ._biopython_sort_tree import biopython_sort_tree as sort_tree
from ._matplotlib_drop_overlapping_labels import (
    matplotlib_drop_overlapping_labels,
)


def biopython_draw_colorclade_tree(
    tree: BioPhylo.BaseTree,
    ax: typing.Union[plt.Axes, tuple, None] = None,
    *,
    drop_overlapping_labels: bool = False,
    label_tips: typing.Union[typing.Callable[[BioClade], str], bool] = True,
    color_labels: typing.Union[typing.Callable[[str], str], str] = "black",
    line_width: float = 4.0,
    max_leaves: typing.Optional[int] = None,
    salt_color: typing.Optional[int] = None,
    use_branch_lengths: bool = True,
    val_to_color: typing.Optional[typing.Callable] = None,
) -> mpl_Axes:
    """Draw a phylogenetic tree from Biopython Tree, color-coding clades based
    on descendant labels.

    Labels are mapped to colors using a hash function. Color-coding uses an
    arbitrarily dominant color among the labels of the clade's descendants. The
    criteria used to determine dominance is deterministic, but arbitrary.

    Parameters
    ----------
    tree : BioPhylo.BaseTree
        The phylogenetic tree object to be visualized.
    ax : plt.Axes, tuple, or None, optional
        The matplotlib Axes object to draw on.

        If a tuple, it is interpreted as the size of the figure to create
        (width, height) in inches. If None, `plt.gca()` is used.
    drop_overlapping_labels : bool, default False
        If True, overlapping labels will be removed to improve clarity.
    label_tips : callable or bool, default True
        If a callable, then `label_tips` will be called on each tip node
        to determine if it should be labeled. If True, all tips of the tree
        will be labeled with their respective names.
    color_labels : callable or str, default "black"
        If a callable, then `color_labels` will be called on each tip name
        to determine what color it will be labeled with. If a string, it is
        interpreted directly as a color.
    line_width : float, default 4.0
        The width of the lines used to draw the tree.
    max_leaves : int or None, optional
        The maximum number of leaves to display.

        If the tree has more leaves, an arbitrary subset of the leaves will be
        displayed.
    salt_color : int or None, optional
        An optional integer to seed the random color generator for clade
        coloring.

        Useful to generate alternate colorings to find one that is visually
        appealing.
    use_branch_lengths : bool, default True
        If True, branch lengths are used to layout the tree. If False, tree is
        displayed as a cladogram.
    val_to_color : Callable or None, optional
        A function mapping each node's value to a color.

        If None, default coloring is applied.

    Returns
    -------
    mpl_Axes
        The matplotlib Axes object with the tree drawn.
    """
    if isinstance(label_tips, bool):
        # kwarg prevents unexpected late-binding behavior
        def label_tips(node: BioClade, label_tips=label_tips) -> str:
            return node.name or "" if label_tips else ""

    if isinstance(color_labels, str):
        # kwarg prevents unexpected late-binding behavior
        def color_labels(_: BioClade, color_labels=color_labels) -> str:
            return color_labels

    biopy_tree = copy.deepcopy(tree)
    if not use_branch_lengths:
        for clade in biopy_tree.find_clades(order="postorder"):
            clade.branch_length = 1.0

    if max_leaves is not None:
        biopy_tree = pare_tree(biopy_tree, max_leaves)

    sort_tree(biopy_tree.root)
    color_tree(biopy_tree.root, salt=salt_color, val_to_color=val_to_color)

    if isinstance(ax, abc.Sequence):
        _fig, ax = plt.subplots(figsize=ax, squeeze=True)
    elif ax is None:
        ax = plt.gca()
    elif not isinstance(ax, plt.Axes):
        raise TypeError(f"ax must be a Axes instance or tuple, not {type(ax)}")
    ax: plt.Axes  # ax has now been converted to a plt.Axes object

    with plt.rc_context({"lines.linewidth": line_width}):
        BioPhylo.draw(
            biopy_tree,
            axes=ax,
            label_func=lambda node: (
                label_tips(node) if node.is_terminal() else ""
            ),
            label_colors=color_labels,
            do_show=False,
        )

    if drop_overlapping_labels:
        matplotlib_drop_overlapping_labels(ax)

    # Remove axes borders except for bottom, and remove y-axis tick/labels
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.set_yticklabels([])
    ax.set_yticks([])
    ax.axes.get_yaxis().set_visible(False)

    return ax
