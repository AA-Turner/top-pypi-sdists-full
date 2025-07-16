from enum import Enum
from typing import Optional


class PageType(Enum):
    ACTION = "action"
    REPORT = "report"
    RECORD = "recordType"
    INTERFACE = "interface"
    PROCESS_HQ = "processHQ"


class Page:
    """
    Class representing a single Page within a site
    """

    def __init__(self, page_name: str, page_type: PageType, site_stub: str, group_name: Optional[str] = None) -> None:
        self.page_name = page_name
        self.page_type = page_type
        self.group_name = group_name
        self.site_stub = site_stub

    def __str__(self) -> str:
        page_info = f"Page(name={self.page_name}, type={self.page_type}, site={self.site_stub}, group={self.group_name})"
        return page_info

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Page):
            return False
        if self.page_name != other.page_name:
            return False
        if self.page_type != other.page_type:
            return False
        if self.site_stub != other.site_stub:
            return False
        if self.group_name != other.group_name:
            return False
        return True


TEMPO_SITE_STUB = "D6JMim"
TEMPO_ACTIONS_PAGE = Page("actions", PageType.INTERFACE, TEMPO_SITE_STUB)
TEMPO_NEWS_PAGE = Page("news", PageType.INTERFACE, TEMPO_SITE_STUB)
TEMPO_RECORDS_PAGE = Page("records", PageType.INTERFACE, TEMPO_SITE_STUB)
TEMPO_REPORTS_PAGE = Page("reports", PageType.INTERFACE, TEMPO_SITE_STUB)
