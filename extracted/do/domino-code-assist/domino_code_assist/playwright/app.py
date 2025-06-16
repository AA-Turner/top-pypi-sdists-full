from playwright.sync_api import Page


class AppHelper:
    def __init__(self, page: Page) -> None:
        self.page = page

    @property
    def menu_item(self):
        return self.page.locator('div[role="listbox"] >> text=App')

    @property
    def dialog(self):
        return self.page.locator(".v-dialog__content--active")

    @property
    def insert_code(self):
        return self.dialog.locator('button:has-text("Run")')

    @property
    def preview(self):
        return self.page.locator('button:has-text("Preview")')

    def insert_object(self, name):
        self.page.locator(f'_vue=v-switch[label="{name}"]').click()
