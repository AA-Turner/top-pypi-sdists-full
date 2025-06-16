from playwright.sync_api import Page


class TransformHelper:
    def __init__(self, page: Page) -> None:
        self.page = page

    @property
    def menu_item(self):
        return self.page.locator('div[role="listbox"] >> text=Transformations')

    @property
    def dialog(self):
        return self.page.locator(".v-dialog__content--active")

    @property
    def add_transformation(self):
        return self.page.locator("text=Add transformation >> xpath=..")

    @property
    def insert_code(self):
        return self.dialog.locator('button:has-text("Run")')

    @property
    def preview(self):
        return self.page.locator('button:has-text("Preview")')

    def choose_dataframe(self, name):
        self.page.locator('div[role="button"]:has-text("DataFrame")').click()
        self.page.locator(f'div[role="option"] >> text={name}').click()

    def table_cell(self, row, column):
        return self.page.locator(f"tr:nth-child({row}) td:nth-child({column})")

    @property
    def filter_like(self):
        return TransformFilterLike(self.page, self)


class TransformFilterLike:
    def __init__(self, page: Page, transform: TransformHelper) -> None:
        self.page = page
        self.transform = transform

    @property
    def dialog(self):
        # it seems like vue=v-dialog does not work
        return self.page.locator("_vue=v-card >> _vue=v-card-title >> text=Filter like >> .. >> ..")

    @property
    def apply(self):
        return self.dialog.locator('button:has-text("Apply")')

    @property
    def column(self):
        return self.dialog.locator('_vue=v-select[label="Column"]')

    @property
    def column_text(self):
        return self.column.locator(".v-select__selection").text_content()

    @property
    def operator(self):
        return self.dialog.locator('_vue=v-select[label="Operator"]')

    @property
    def operator_text(self):
        return self.operator.locator(".v-select__selection").text_content()

    @property
    def value(self):
        return self.dialog.locator('_vue=v-text-field[label="Value"]')

    @property
    def value_text(self):
        return self.value.locator("input").input_value()

    @value_text.setter
    def value_text(self, value):
        self.value.locator("input").fill(value)

    @property
    def new_dataframe_name(self):
        return self.dialog.locator('_vue=v-text-field[label="New dataframe name"]')

    @property
    def new_dataframe_name_text(self):
        return self.new_dataframe_name.locator("input").input_value()

    @new_dataframe_name_text.setter
    def new_dataframe_name_text(self, value):
        self.new_dataframe_name.locator("input").fill(value)
