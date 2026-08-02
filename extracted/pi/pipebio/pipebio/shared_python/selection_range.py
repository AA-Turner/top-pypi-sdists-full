from typing import Optional, List


class SelectionRange:
    start_id: int
    end_id: Optional[int]

    def __init__(self, start_id: int = 1, end_id: Optional[int] = None):
        if not isinstance(start_id, int):
            raise ValueError(f'start_id must be an integer, got {type(start_id).__name__}')
        if start_id < 1:
            raise ValueError(f'start_id must be >= 1, got {start_id}')
        if end_id is not None:
            if not isinstance(end_id, int):
                raise ValueError(f'end_id must be an integer, got {type(end_id).__name__}')
            if end_id < 1:
                raise ValueError(f'end_id must be >= 1, got {end_id}')
            if end_id < start_id:
                raise ValueError(f'end_id ({end_id}) must be >= start_id ({start_id})')
        self.start_id = start_id
        self.end_id = end_id

    @staticmethod
    def from_json(json: dict):
        if not json:
            raise Exception('Error. SelectionRange was not defined but should be.')

        if 'startId' not in json:
            raise Exception('Error. json.startId was not defined.')

        start_id = json['startId']
        end_id = json.get('endId', None)

        return SelectionRange(start_id=start_id, end_id=end_id)

    def to_json(self):
        return {
            'startId': self.start_id,
            'endId': self.end_id
        }


def selection_ranges_to_sql(ranges: List[SelectionRange]) -> str:
    """
    Python equivalent to our frontend rangesToSQL in filter.util.ts
    :param ranges:
    :return:
    """
    if not isinstance(ranges, list):
        return ''

    ranges = sorted(ranges, key=lambda x: x.start_id)

    result = []

    for i, range_ in enumerate(ranges):
        start_id = range_.start_id
        end_id = range_.end_id

        if isinstance(start_id, int):
            if isinstance(end_id, int):
                result.append(f"id BETWEEN {start_id} AND {end_id}")
            elif end_id is None or end_id == '':
                if i == len(ranges) - 1:
                    result.append(f"({start_id} <= id)")
                else:
                    raise ValueError(
                        "Unbound ranges are only allowed on the final range, otherwise they would conflict.")
            else:
                raise ValueError(
                    f"range.endId={end_id} is neither a valid integer nor undefined. End indices must be integers or undefined, indicating unbound.")
        else:
            raise ValueError(f"range.startId={start_id} is not a valid integer. Start indices must be integers.")

    or_clause = ' OR '.join(result)

    maybe_parentheses = 'OR' in or_clause

    return f"({or_clause})" if maybe_parentheses else or_clause