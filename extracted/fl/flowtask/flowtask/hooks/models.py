from datetime import datetime
from dataclasses import InitVar
from datamodel import Field
from asyncdb.models import Model
from uuid import UUID, uuid4

class HookObject(Model):
    trigger_id: UUID = Field(required=True, primary_key=True, default=uuid4, db_default="auto")
    name: str = Field(required=True)
    definition: dict = Field(required=True)
    created_by: int = Field(required=False)
    created_at: datetime = Field(required=False, default=datetime.now())

    class Meta:
        name: str = "triggers"
        schema: str = "navigator"
        strict: bool = False
