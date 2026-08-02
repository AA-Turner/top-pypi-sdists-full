from typing import Optional, List, Union

from pipebio.shared_python.selection_range import SelectionRange
from pipebio.annotate.sort import Sort


def safely_get(object: dict, key: str, default: any) -> any:
    return object[key] \
        if object is not None and key in object and object[key] is not None \
        else default


class Params:
    target_folder_id: Optional[Union[int, str]]
    target_project_id: Optional[int]
    clientSide: bool
    workflow_id: str
    output_names: List[str]

    def __init__(self, params: dict = None):
        target_folder_id = Params.safely_get(params, "targetFolderId", None)
        self.target_folder_id = target_folder_id if target_folder_id else None
        self.target_project_id = Params.safely_get(params, "targetProjectId", None)
        self.workflow_id = Params.safely_get(params, "workflowId", None)
        self.output_names = Params.safely_get(params, "outputNames", [])
        self.clientSide = False

    @staticmethod
    def safely_get(object: dict, key: str, default: any) -> any:
        return safely_get(object, key, default)

    def to_json(self):
        result = {
            'targetFolderId': self.target_folder_id,
            'targetProjectId': self.target_project_id,
            'workflowId': self.workflow_id,
            'outputNames': self.output_names,
        }
        return result


class FilterableSelectableParams(Params):
    filter: str
    selection: List[SelectionRange]
    sort: List[Sort]

    def __init__(self, params: dict = None):
        super().__init__(params)
        self.filter = self.safely_get(params, "filter", '')
        _selection = self.safely_get(params, 'selection', [])
        self.selection = list(SelectionRange.from_json(range) for range in _selection) if _selection else []
        _sort = self.safely_get(params, "sort", [])
        self.sort = list(Sort.from_json(sort_item) for sort_item in _sort) if _sort else [Sort('id', 'asc')]
        self.target_folder_id = self.safely_get(params, "targetFolderId", None)

    def to_json(self):
        also = super().to_json()
        return {
            **also,
            'filter': self.filter if self.filter else '',
            'selection': list(selection_range.to_json() for selection_range in self.selection),
            'sort': list(sort_item.to_json() for sort_item in self.sort),
            'targetFolderId': self.target_folder_id,
        }