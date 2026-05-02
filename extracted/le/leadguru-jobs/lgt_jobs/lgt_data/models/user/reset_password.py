from lgt_jobs.lgt_data.models.base import BaseModel


class UserResetPasswordModel(BaseModel):
    def __init__(self):
        super().__init__()
        self.email = None
