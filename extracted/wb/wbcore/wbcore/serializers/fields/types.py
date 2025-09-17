from enum import Enum


class WBCoreType(Enum):
    TEXT = "text"
    TELEPHONE = "tel"
    TEXTEDITOR = "texteditor"
    TEMPLATED_TEXTEDITOR = "templatedtexteditor"
    TEXTAREA = "textarea"
    MARKDOWNEDITOR = "markdowneditor"
    NUMBER = "number"
    NUMBERRANGE = "numberrange"
    DATETIME = "datetime"
    DATETIMERANGE = "datetimerange"
    DATE = "date"
    DATERANGE = "daterange"
    TIMERANGE = "timerange"
    DURATION = "duration"
    TIME = "time"
    PRIMARY_KEY = "primary_key"
    BOOLEAN = "boolean"
    SELECT = "select"
    IMAGE = "image"
    FILE = "file"
    LIST = "list"
    PERCENT = "percent"
    JSON = "json"
    JSONTABLE = "table"
    ICON = "iconselect"
    COLOR = "color"
    URL = "url"
    SPARKLINE = "sparkline"
    LANGUAGE = "language"


class ReturnContentType(Enum):
    HTML = "html"
    JSON = "json"
    MARKDOWN = "markdown"


class DisplayMode(Enum):
    DECIMAL = "decimal"
    SHORTENED = "shortened"
    SCIENTIFIC = "scientific"
