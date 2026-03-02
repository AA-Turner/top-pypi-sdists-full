from matplotlib.axes import Axes as mpl_Axes


def matplotlib_drop_overlapping_labels(ax: mpl_Axes) -> None:
    """Iteratively hide labels from a matplotlib Axes object to resolve
    overlaps."""
    # Code to remove overlapping annotations
    bboxes = []
    for label in ax.texts:
        bbox = label.get_window_extent()
        # Check if current label overlaps with the others
        overlaps = any(bbox.overlaps(bbox_) for bbox_ in bboxes)
        if overlaps:
            label.set_visible(False)
        else:
            bboxes.append(bbox)
