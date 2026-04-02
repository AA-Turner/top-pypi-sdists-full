from enum import Enum


class MarketplaceCategoryFieldEnum(str, Enum):
    ARTICLES = "articles"
    AVAILABLE_OFFERINGS_COUNT = "available_offerings_count"
    COLUMNS = "columns"
    COMPONENTS = "components"
    DEFAULT_TENANT_CATEGORY = "default_tenant_category"
    DEFAULT_VM_CATEGORY = "default_vm_category"
    DEFAULT_VOLUME_CATEGORY = "default_volume_category"
    DESCRIPTION = "description"
    GROUP = "group"
    ICON = "icon"
    OFFERING_COUNT = "offering_count"
    SECTIONS = "sections"
    TITLE = "title"
    URL = "url"
    UUID = "uuid"

    def __str__(self) -> str:
        return str(self.value)
