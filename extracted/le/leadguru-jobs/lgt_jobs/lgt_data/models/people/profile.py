from lgt_jobs.lgt_data.models.base import DictionaryModel


class Profile(DictionaryModel):
    def __init__(self):
        self.title = ''
        self.phone = ''
        self.skype = ''
        self.display_name = ''
        self.real_name = ''
        self.email = ''
        self.photo_url = ''
        self.main = False
