"""The account floor: which WhatsApp accounts a person may see and act on.

One definition for every consumer (inbox lists, counters, search, open by id, assign, send...).
It is separate from the per-agent floor (`restricted_to_own_chats`): APB and `can_see_all_agents_chats`
do not lift it.

The rule itself (`account_floor`) is `domain/whatsapp_accounts.py` (ENG-458) and is re-exported here; `floor_clause` is the Mongo half.

The floor is `None` (every account) or a list of account ids. A `None` entry in the list stands for the
chats with no `account_id`: until the migration stamps every chat they belong to the company's default
account, so the entry is added exactly when the user is allowed the default account.
"""
from typing import Any, Dict

from ...domain.whatsapp_accounts import Floor, account_floor, chat_in_floor
from .chat_scope import chats_of_accounts

__all__ = ["Floor", "account_floor", "chat_in_floor", "floor_clause"]


def floor_clause(floor: Floor) -> Dict[str, Any]:
    """The Mongo filter of the floor: `{}` when there is none."""
    return {} if floor is None else chats_of_accounts(floor)
