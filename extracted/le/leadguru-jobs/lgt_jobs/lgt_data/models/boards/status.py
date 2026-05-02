from lgt_jobs.lgt_data.models.base import DictionaryModel


class BoardedStatus(DictionaryModel):
    pass

    def __init__(self):
        self.id = None
        self.name = None
        self.order = 0
        self.is_primary = False
        self.default = False
        self.user_leads = 0
        self.collapsed = False
