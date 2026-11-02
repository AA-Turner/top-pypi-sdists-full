"""The rule of the account floor, with no infrastructure: what `services/whatsapp_accounts/account_floor.py` and the
domain modules (notifications) share.

The floor is `None` (every account) or a list of account ids; a `None` entry stands for the chats with no
`account_id` (the company's default account).
"""
from typing import List, Optional

Floor = Optional[List[Optional[str]]]


def chat_in_floor(floor: Floor, chat_account_id: Optional[str]) -> bool:
    """May a person with this floor see a chat of `chat_account_id` (None = unstamped chat)?"""
    return floor is None or chat_account_id in floor
