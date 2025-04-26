from typing import Union

from ..extensions import UnknownType
from ..models.table_ui_block_data_frame_source import TableUiBlockDataFrameSource
from ..models.table_ui_block_dataset_source import TableUiBlockDatasetSource

TableUiBlockSource = Union[TableUiBlockDatasetSource, TableUiBlockDataFrameSource, UnknownType]
