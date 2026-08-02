from typing import Union

from pipebio.models.table_column_type import TableColumnType


class UploadDetail:

    def __init__(self, name: str,
                 type: Union[TableColumnType, str],
                 value: any):
        self.name = name
        self.type = type
        self.value = value

    def __str__(self):
        return f'{self.name}={self.value}'

    def to_json(self):
        return {
            'name': self.name,
            'type': self.type.value if isinstance(self.type, TableColumnType) else self.type,
            'value': self.value,
        }