from playwright.sync_api import Page

from domino_code_assist.playwright.app import AppHelper
from domino_code_assist.playwright.load_data import LoadDataHelper
from domino_code_assist.playwright.transform import TransformHelper


class AssistentHelper:
    def __init__(self, page: Page) -> None:
        self.page = page

    @property
    def initializer(self):
        return self.page.locator('[aria-label="Domino Code Assist"]')

    @property
    def initialized_text(self):
        return self.page.locator("text=Domino Code Assist initialized")

    @property
    def domino_logo(self):
        return self.page.locator(".domino_code_assist-assistant-menu")

    @property
    def load_data(self):
        return LoadDataHelper(self.page)

    @property
    def app(self):
        return AppHelper(self.page)

    @property
    def transform(self):
        return TransformHelper(self.page)

    @property
    def insert_code(self):
        return self.page.locator("text=Insert Code")
