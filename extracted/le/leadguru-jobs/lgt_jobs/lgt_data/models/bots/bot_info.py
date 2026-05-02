import copy


class BotInfo:
    def __init__(self):
        self.id = None
        self.invalid_creds: bool | None = False
        self.source = None
        self.banned: bool | None = False
        self.user_name: str = ''
        self.associated_user: str | None = ''
        self.deleted: bool = False
        self.two_factor_required = False

    @classmethod
    def from_dic(cls, dic: dict):
        if not dic:
            return None

        model = BotInfo()
        for k, v in dic.items():
            if hasattr(model, k):
                setattr(model, k, v)

        if '_id' in dic:
            setattr(model, 'id', dic['_id'])

        return model

    def to_dic(self):
        result = copy.deepcopy(self.__dict__)
        return result
    