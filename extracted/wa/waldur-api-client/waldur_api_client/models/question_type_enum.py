from enum import Enum


class QuestionTypeEnum(str, Enum):
    BOOLEAN = "boolean"
    COUNTRY = "country"
    DATE = "date"
    DATETIME = "datetime"
    EMAIL = "email"
    FILE = "file"
    LIKERT = "likert"
    MULTIPLE_FILES = "multiple_files"
    MULTI_SELECT = "multi_select"
    NUMBER = "number"
    PHONE_NUMBER = "phone_number"
    RATING = "rating"
    RICH_TEXT = "rich_text"
    SINGLE_SELECT = "single_select"
    TEXT_AREA = "text_area"
    TEXT_INPUT = "text_input"
    URL = "url"
    YEAR = "year"

    def __str__(self) -> str:
        return str(self.value)
