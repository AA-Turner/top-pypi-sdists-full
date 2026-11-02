"""The sources of one account, as a Mongo filter.

Sources are per account (E1): the organic, the contact import, the coexistence echo and the inferred-ad
source exist once per account, and every other source belongs to exactly one account. Until the migration
stamps `account_id` on every source, the company's DEFAULT account also owns the sources that have none.

This is the Mongo form of the ownership rule. The in-memory form is `models.whatsapp.ownership`
(`belongs_to_account` / `same_account`): one rule, two forms, so they cannot disagree. It takes the two facts
the rule needs, not a whole `AccountContext` (which carries the token and costs reads): the account id (None
only for a company with no accounts yet) and whether it is the default one.
"""
from typing import Any, Dict, Optional


def sources_of_account(account_id: Optional[str], is_default: bool) -> Dict[str, Any]:
    """Mongo filter for the sources the account owns (`{company_id}` is added by the caller)."""
    if is_default:
        # `None` matches a missing field and an explicit null.
        return {"account_id": {"$in": [account_id, None]}} if account_id else {"account_id": None}
    return {"account_id": account_id}
