from lgt_jobs.lgt_data.models.base import DictionaryModel


class PostMessage(DictionaryModel):
    id: str
    server_id: str
    server_name: str
    channel_id: str
    channel_name: str

    @classmethod
    def from_dic(cls, dic: dict):
        if not dic:
            return None
        model = cls()
        for k, v in dic.items():
            setattr(model, k, v)
        return model
