from enum import Enum


class MessageBlocksItemKey(str, Enum):
    ASK_USER_FORM = "ask_user_form"
    CODE = "code"
    HOMEPORT_NAV = "homeport_nav"
    MARKDOWN = "markdown"
    MERMAID = "mermaid"
    RESOURCE_LIST = "resource_list"
    TOOL = "tool"
    VM_ORDER = "vm_order"

    def __str__(self) -> str:
        return str(self.value)
