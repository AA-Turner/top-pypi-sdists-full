import copy
from datetime import datetime, UTC
from typing import Optional, List

from bson import ObjectId

from lgt_jobs.lgt_data.models.base import DictionaryModel
from lgt_jobs.lgt_data.models.bots.base_bot import BaseBotModel, Source


class DedicatedBotModel(BaseBotModel):
    def __init__(self):
        super().__init__()
        self.user_id: ObjectId | None = None
        self.updated_at: Optional[datetime] = datetime.now(UTC)
        self.servers: List[Server] = []
        self.state = 0
        self.source: Source | None = None

    def to_dic(self):
        result = copy.deepcopy(self.__dict__)

        if result.get('source'):
            result['source'] = Source.to_dic(result.get('source'))

        result['servers'] = [Server.to_dic(server) for server in self.servers]
        return result

    @classmethod
    def from_dic(cls, dic: dict):
        if not dic:
            return None

        model: DedicatedBotModel = cls()
        for k, v in dic.items():
            setattr(model, k, v)

        if '_id' in dic:
            setattr(model, 'id', dic['_id'])

        model.source = Source.from_dic(dic.get("source"))
        model.servers = [Server.from_dic(server) for server in dic.get("servers", [])]
        return model


class Server:
    pass

    def __init__(self):
        self.id = None
        self.name: str | None = None
        self.title: str | None = None
        self.channels: List[Channel] = []
        self.icon = None
        self.active = False
        self.deleted = False
        self.read_only = False
        self.subscribers = 0
        self.approximate_member_count = 0
        self.messages_received: int = 0
        self.messages_filtered: int = 0

    @classmethod
    def from_dic(cls, dic: dict):
        if not dic:
            return None

        model = cls()
        for k, v in dic.items():
            if hasattr(model, k):
                setattr(model, k, v)

        model.channels = [Channel.from_dic(channel) for channel in dic.get("channels", [])]
        return model

    @classmethod
    def from_discord_response(cls, dic: dict):
        if not dic:
            return None

        model = cls()
        for k, v in dic.items():
            if hasattr(model, k):
                setattr(model, k, v)

        model.channels = [Channel.from_dic(channel) for channel in dic.get("channels", [])]
        model.subscribers = dic.get('approximate_member_count')
        return model

    def to_dic(self):
        result = copy.deepcopy(self.__dict__)
        result['channels'] = [Channel.to_dic(channel) for channel in self.channels]
        return result


class Channel(DictionaryModel):
    pass

    def __init__(self):
        self.id = None
        self.name = None
        self.type = None
        self.is_member = True
        self.active = True
        self.subscribers = 0
