from datetime import datetime, timezone
from datamodel import Field
from .abstract import AbstractPayload


class Account(AbstractPayload):
    """
    {
            "metadata": {
                "type": "retailer",
                "transaction_type": "UPSERT",
                "source": "MainEvent",
                "client": "global",
                "client_id": 1,
                "orgid": null,
                "timestamp": 1742240432.348096
            },
            "payload": {
                "account_id": 26,
                "account_name": "Brandsmart",
                "active": true
            }
        },
    """
    account_id: int = Field(primary_key=True, required=True)
    account_name: str
    active: bool = Field(default=True)
    retailer: int
    inserted_at: datetime = Field(default=datetime.now(tz=timezone.utc))

    class Meta:
        strict = True
        as_objects = True
        name = 'accounts'
        schema: str = 'networkninja'

    def __post_init__(self):
        super().__post_init__()
        self.retailer = self.account_id
