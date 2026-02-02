"""
Spatial utilities for working with bounding boxes and document layout.
"""
from .bbox_common import (
    overlaps_with,
    width_of_overlap,
    percent_nodes_overlap,
)

from .azure_models import (
    create_kddb_from_azure,
    create_page_node_keep_azure_lines,
    create_page_node_line_up_kodexa,
    get_azure_next_line,
    convert_azure_bbox,
)

from .table_form_common import (
    transform_line_to_columns,
    to_table,
    transform_lines_to_table,
    DataMarker,
    get_data_marker_column_and_index,
    get_column_below_or_above_data,
)
