from lgt_jobs.lgt_data.models.base import DictionaryModel


class TypedField(DictionaryModel):
    type: str
    description: str
