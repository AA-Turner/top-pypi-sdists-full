class Sort:
    col_id: str
    sort: str

    def __init__(self, col_id=None, sort=None):
        self.col_id = col_id
        self.sort = sort if sort is not None else 'asc'

    def __str__(self):
        return f'{self.col_id}({self.sort})'

    def __eq__(self, other):
        return self.col_id == other.col_id and self.sort == other.sort

    @staticmethod
    def from_json(json: dict):
        if not json:
            raise Exception('Error. Sort was not defined but should be.')

        sort = Sort()

        if 'colId' in json:
            sort.col_id = json['colId']
        else:
            raise Exception('Error. json.colId was not defined.')

        if 'sort' in json:
            sort.sort = json['sort']
        else:
            raise Exception('Error. json.sort was not defined.')

        return sort

    def to_json(self):
        return {
            'colId': self.col_id,
            'sort': self.sort
        }