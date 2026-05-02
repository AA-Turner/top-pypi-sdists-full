from lgt_jobs.lgt_data.models.base import DictionaryModel


class LeadGuruFile(DictionaryModel):
    id: str = None
    blob_path: str
    content_type: str
    file_name: str = None
