import copy
from typing import List

from lgt_jobs.lgt_data.models.base import BaseModel
from lgt_jobs.lgt_data.models.boards.status import BoardedStatus


class BoardModel(BaseModel):
    pass

    def __init__(self):
        super().__init__()
        self.name = None
        self.user_id = None
        self.statuses: List[BoardedStatus] = []
        self.is_primary = None
        self.default = False

    @classmethod
    def from_dic(cls, dic: dict):
        if not dic:
            return None

        model = BoardModel()
        for k, v in dic.items():
            setattr(model, k, v)

        model.id = dic.get('_id')
        model.statuses = [BoardedStatus.from_dic(status) for status in dic.get('statuses', [])]
        return model

    def to_dic(self):
        result = copy.deepcopy(self.__dict__)
        result["statuses"] = [BoardedStatus.to_dic(status) for status in self.statuses]

        for status in result['statuses']:
            status['board_id'] = result['id']

        return result
