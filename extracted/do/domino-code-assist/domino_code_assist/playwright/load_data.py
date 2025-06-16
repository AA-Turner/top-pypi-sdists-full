from playwright.sync_api import Page


class LoadDataHelper:
    def __init__(self, page: Page) -> None:
        self.page = page

    @property
    def menu_item(self):
        return self.page.locator('div[role="listbox"] >> text=Load data')

    @property
    def dialog(self):
        return self.page.locator(".v-dialog__content--active")

    @property
    def project_files(self):
        return ProjectFileHelper(self.page, self)

    @property
    def insert_code(self):
        return self.dialog.locator('button:has-text("Run")')


class ProjectFileHelper:
    def __init__(self, page: Page, load_data: LoadDataHelper) -> None:
        self.page = page
        self.load_data = load_data

    @property
    def tab_item(self):
        return self.load_data.dialog.locator("text=Project Files")

    @property
    def file_browser(self):
        return self.load_data.dialog.locator(".solara-file-browser")
