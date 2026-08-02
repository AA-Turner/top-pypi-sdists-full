from pipebio.models.table_column_type import TableColumnType


class Field(dict):
    original: str
    name: str
    type: TableColumnType

    def __init__(self, original: str, name: str, type: TableColumnType):
        super().__init__()
        self.original = original
        self.name = name
        self.type = type

    def __repr__(self):
        return f'Field({self.original},{self.name},{self.type.value})'

    def to_json(self) -> dict:
        return {
            'original': self.original,
            'name': self.name,
            'type': self.type.value,
        }