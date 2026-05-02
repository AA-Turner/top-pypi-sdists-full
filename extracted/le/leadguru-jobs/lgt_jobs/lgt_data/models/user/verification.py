from datetime import datetime, UTC

from lgt_jobs.lgt_data.models.base import DictionaryModel


class UserVerificationModel(DictionaryModel):
    pass

    def __init__(self):
        super().__init__()
        self.email = None
        self.created_at = datetime.now(UTC)
