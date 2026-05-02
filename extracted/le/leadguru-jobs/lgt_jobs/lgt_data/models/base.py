import copy
from abc import ABC
from datetime import datetime, UTC


class DictionaryModel(ABC):
    @classmethod
    def from_dic(cls, dic: dict):
        if not dic:
            return None

        model = cls()
        for k, v in dic.items():
            setattr(model, k, v)

        if '_id' in dic:
            setattr(model, 'id', dic['_id'])

        return model

    def to_dic(self):
        result = copy.deepcopy(self.__dict__)
        return result


class BaseModel(DictionaryModel):
    def __init__(self):
        self.id = None
        self.created_at = datetime.now(UTC)
