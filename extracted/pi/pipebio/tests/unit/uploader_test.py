import unittest
from unittest.mock import MagicMock

from pipebio.column import Column
from pipebio.models.table_column_type import TableColumnType
from pipebio.uploader import Uploader


class UploaderTest(unittest.TestCase):

    def test_uploader_adds_default_schemas_at_init(self):
        """
        Asserts that the uploader extends the input schema with required default columns without editing
        the initial schema reference.
        :return:
        """
        empty_schema = []
        uploader = Uploader(123, empty_schema, MagicMock())
        self.assertEqual(empty_schema, [])
        self.assertEqual(str(uploader.schema), str([Column("id",TableColumnType.INT64),
                                           Column("name", TableColumnType.STRING),
                                           Column("name_sort", TableColumnType.STRING),
                                           Column("description", TableColumnType.STRING),
                                           Column("description_sort", TableColumnType.STRING),
                                           Column("labels", TableColumnType.STRING)]))