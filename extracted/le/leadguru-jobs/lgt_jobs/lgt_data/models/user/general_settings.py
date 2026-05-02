from lgt_jobs.lgt_data.models.base import DictionaryModel


class GeneralSettings(DictionaryModel):
    def __init__(self):
        self.theme: str | None = None
        self.ask_pipeline_and_status: bool = False
        self.ask_follow_up: bool = False
        self.dashboard_is_starting_page: bool = False
