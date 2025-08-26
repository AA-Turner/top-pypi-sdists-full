import enum
from contextlib import suppress
from types import DynamicClassAttribute

from django.conf import settings
from django.db.models import TextChoices
from django.db.models.enums import ChoicesMeta

from wbcore.utils.importlib import import_from_dotted_path

DEFAULT_ICON_BACKEND = "wbcore.contrib.icons.backends.material.IconBackend"
FALLBACK_ICON_VALUE = "FALLBACK_ICON"


class WBIconMeta(ChoicesMeta):
    """A metaclass for creating a enum choices."""

    def __new__(metacls, classname, bases, classdict, **kwds):
        dict.__setitem__(
            classdict, FALLBACK_ICON_VALUE, (FALLBACK_ICON_VALUE, "Fallback Icon")
        )  # add a default member that represent the fallback in case it's not yet implement in the imported backend
        cls = super().__new__(metacls, classname, bases, classdict, **kwds)
        with suppress(ModuleNotFoundError):
            setattr(
                cls,
                "icon_backend",
                import_from_dotted_path(getattr(settings, "WBCORE_ICON_BACKEND", DEFAULT_ICON_BACKEND)),
            )
            icon_backend = cls.icon_backend
            # For each enumeration values, attached an "icon" property to its members
            for member, value in zip(cls.__members__.values(), cls.values):
                member._icon_ = getattr(icon_backend, value, icon_backend.fallback_icon)
        return enum.unique(cls)


class WBIcon(TextChoices, metaclass=WBIconMeta):
    """
    This enumeration defines the supported icons. For each attribute, we expect an equivalent attribute in each of the Icon Backends.

    The actual value of the icon can be retreived using `WBIcon.MY_ICON.icon`

    Procedure to add new icon:
    1) Add the enumeration member in this class (e.g. NEW_ICON = "NEW_ICON", "My new Icon")
    2) For each supported icon backend, create the equivalent attribute pointing to the material icon value (e.g NEW_ICON = "my_new_icon_in_google_material_icons")
    """

    @DynamicClassAttribute
    def icon(self):
        return self._icon_

    ACCOUNT_BALANCE = "ACCOUNT_BALANCE", "Account Balance"
    ADD = "ADD", "Add"
    APPROVE = "APPROVE", "Approve"
    BANK = "BANK", "Bank"
    BIRTHDAY = "BIRTHDAY", "Birthday"
    BOOKMARK = "BOOKMARK", "Bookmark"
    BROADCAST = "BROADCAST", "Broadcast"
    CALENDAR = "CALENDAR", "Calendar"
    CHART_AREA = "CHART_AREA", "Chart area"
    CHART_BARS_HORIZONTAL = "CHART_BARS_HORIZONTAL", "Chart bars horizonal"
    CHART_BARS_VERTICAL = "CHART_BARS_VERTICAL", "Chart bars vertical"
    CHART_BARS_VERTICAL_INCREASING = "CHART_BARS_VERTICAL_INCREASING", "Chart bars vertical increasing"
    CHART_LINE = "CHART_LINE", "Chart line"
    CHART_PIE = "CHART_PIE", "Chart pie"
    CHART_PYRAMID = "CHART_PYRAMID", "Chart piramid"
    CHART_SWITCHES = "CHART_SWITCHES", "Chart switches"
    CHART_WATERFALL = "CHART_WATERFALL", "Chart waterfall"
    CHART_MULTILINE = "CHART_MULTILINE", "Chart multiline"
    CLIPBOARD = "CLIPBOARD", "Clipboard"
    CONFIRM = "CONFIRM", "Confirm"
    CONFIGURE = "CONFIGURE", "configure"
    COPY = "COPY", "Copy"
    CURRENCY_EXCHANGE = "CURRENCY_EXCHANGE", "Currency Exchange"
    DASHBOARD = "DASHBOARD", "Dashboard"
    DATA_GRID = "DATA_GRID", "Data grid"
    DATA_LIST = "DATA_LIST", "Data list"
    DATA_EXPLORATION = "DATA_EXPLORATION", "Data exploration"
    DAY_OFF = "DAY_OFF", "Day off"
    DEAL = "DEAL", "Deal"
    DEAL_MONEY = "DEAL_MONEY", "Deal money"
    DECISION_STEP = "DECISION_STEP", "Decision step"
    DELETE = "DELETE", "Delete"
    DENY = "DENY", "Deny"
    DISABLED = "DISABLED", "Disabled"
    DOCUMENT = "DOCUMENT", "Document"
    DOCUMENT_IN_PROGRESS = "DOCUMENT_IN_PROGRESS", "Document in progress"
    DOCUMENT_PRIVATE = "DOCUMENT_PRIVATE", "Document private"
    DOCUMENT_WITH_DOLLAR = "DOCUMENT_WITH_DOLLAR", "Document with Dollar"
    DOCUMENT_WITH_ATTACHMENT = "DOCUMENT_WITH_ATTACHMENT", "Document with Attachment"
    DOLLAR = "DOLLAR", "Dollar"
    DOWNLOAD = "DOWNLOAD", "Download"
    EDIT = "EDIT", "Edit"
    END = "END", "End"
    ENUMERATION = "ENUMERATION", "Enumeration"
    EURO = "EURO", "Euro"
    EVENT = "EVENT", "Event"
    EVENT_ACCEPTED = "EVENT_ACCEPTED", "Event accepted"
    EXPEND = "EXPEND", "Expend"
    FAVORITE = "FAVORITE", "Favorite"
    FEEDBACK = "FEEDBACK", "Feedback"
    FOLDERS_ADD = "FOLDERS_ADD", "Folders add"
    FOLDERS_MONEY = "FOLDERS_MONEY", "Folders money"
    FOLDERS_OPEN = "FOLDERS_OPEN", "Folders open"
    GENERATE_NEXT = "GENERATE_NEXT", "Generate next"
    GOAL = "GOAL", "Goal"
    GROUPS = "GROUPS", "Groups"
    HISTORY = "HISTORY", "History"
    HOME = "HOME", "Home"
    IGNORE = "IGNORE", "Ignore"
    IMPORT_EXPORT = "IMPORT_EXPORT", "Import Export"
    INFO = "INFO", "Info"
    INVERSE = "INVERSE", "Inverse"
    JOIN_STEP = "JOIN_STEP", "Join Step"
    LINK = "LINK", "Link"
    LOCATION = "LOCATION", "Location"
    LOCK = "LOCK", "Lock"
    LUNCH = "LUNCH", "Lunch"
    MAIL = "MAIL", "Mail"
    MAIL_MONEY = "MAIL_MONEY", "Mail Money"
    MAIL_OPEN = "MAIL_OPEN", "Mail open"
    MAIL_POSTED = "MAIL_POSTED", "Mail posted"
    MERGE = "MERGE", "Merge"
    NEWSPAPER = "NEWSPAPER", "Newspaper"
    NEXT = "NEXT", "Next"
    NOTEBOOK = "NOTEBOOK", "Notebook"
    OTHER = "OTHER", "Other"
    PEOPLE = "PEOPLE", "People"
    PENDING = "PENDING", "Pending"
    PERSON = "PERSON", "Person"
    PERSON_ADD = "PERSON_ADD", "Person Add"
    PHONE = "PHONE", "Phone"
    PHONE_ADD = "PHONE_ADD", "Phone Add"
    PREVIOUS = "PREVIOUS", "Previous"
    PUBLIC = "PUBLIC", "Public"
    QUESTION = "QUESTION", "QUESTION"
    REDO = "REDO", "Redo"
    REFRESH = "REFRESH", "Refresh"
    REGENERATE = "REGENERATE", "Regenerate"
    REJECT = "REJECT", "Reject"
    REPEAT = "REPEAT", "Repeat"
    REPLACE = "REPLACE", "Replace"
    REVIEW = "REVIEW", "Review"
    RUNNING = "RUNNING", "Running"
    SAVE = "SAVE", "Save"
    SCHEDULE = "SCHEDULE", "Schedule"
    SCRIPT = "SCRIPT", "Script"
    SEND = "SEND", "Send"
    SEND_LATER = "SEND_LATER", "Send Later"
    SETTINGS = "SETTINGS", "Settings"
    SHARE = "SHARE", "Share"
    SHRINK = "SHRINK", "Shrink"
    SICK_LEAVE = "SICK_LEAVE", "Sick leave"
    SPLIT = "SPLIT", "Split"
    START = "START", "Start"
    STATS = "STATS", "Stats"
    SUPERVISE = "SUPERVISE", "Supervise"
    SYNCHRONIZE = "SYNCHRONIZE", "Synchronize"
    TABLE = "TABLE", "Table"
    TIME_UP = "TIME_UP", "Time Up"
    TRADE = "TRADE", "Trade"
    TRAINING = "TRAINING", "Training"
    UNDO = "UNDO", "Undo"
    UNFILTER = "UNFILTER", "Unfilter"
    UNFOLD = "UNFOLD", "Unfold"
    UNLINK = "UNLINK", "Unlink"
    UNLOCK = "UNLOCK", "Unlock"
    UPLOAD = "UPLOAD", "Upload"
    VACATION = "VACATION", "Vacation"
    VIEW = "VIEW", "View"
    WARNING = "WARNING", "Warning"
    WORK = "WORK", "Work"
