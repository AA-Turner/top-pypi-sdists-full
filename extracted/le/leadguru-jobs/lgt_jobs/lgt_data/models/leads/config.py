from lgt_jobs.lgt_data.models.base import DictionaryModel


class BaseConfig(DictionaryModel):
    def __init__(self):
        self.owner = None
        self.id = None


class Config(BaseConfig):
    def __init__(self):
        super().__init__()
        self.name = None
