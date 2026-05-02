import copy
import json
from typing import List

from lgt_jobs.lgt_data.models.bots.base_bot import Source
from lgt_jobs.lgt_data.models.leads.config import BaseConfig


class MessageModel:
    pass

    def __init__(self):
        self.message_id = None
        self.channel_id = None
        self.channel_name = None
        self.message = None
        self.name = None
        self.sender_id = None
        self.source: Source | None = None
        self.companies: List[str] = list()
        self.technologies: List[str] = list()
        self.locations: List[str] = list()
        self.configs: List[BaseConfig] = list()
        self.attachments: List[dict] = []
        self.timestamp = None
        self.tags: List[str] = []

    @classmethod
    def from_dic(cls, dic: dict):
        if not dic:
            return None
        if isinstance(dic.get('attachments'), str):
            dic['attachments'] = json.loads(dic['attachments'])

        model: MessageModel = cls()
        for k, v in dic.items():
            setattr(model, k, v)

        model.source = Source.from_dic(dic.get("source"))
        model.configs = [BaseConfig.from_dic(doc) for doc in dic.get("configs", [])]
        return model

    def to_dic(self):
        result = copy.deepcopy(self.__dict__)

        if result.get('source'):
            result['source'] = Source.to_dic(result.get('source'))
        if result.get('configs'):
            result['configs'] = [BaseConfig.to_dic(config) for config in result.get('configs')]
        return result

