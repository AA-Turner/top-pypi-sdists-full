from uuid import UUID
from datetime import datetime, timezone
from typing import Optional
from datamodel import BaseModel, Field
from querysource.conf import async_default_dsn
from querysource.outputs.tables import PgOutput


class AbstractNotificationLog(BaseModel):
    """Abstract base for provider-specific notification log models.

    Contains only the fields common to every notification channel.
    Provider-specific subclasses (ZoomLog, EmailLog, etc.) extend this
    with their own fields, table name and schema.
    """
    recipient_name:    str
    recipient_address: str
    message_content:   str
    task_id:           Optional[UUID] = Field(required=False, default=None)
    program_slug:      str
    created_at:        datetime = Field(required=False, default=lambda: datetime.now(timezone.utc))

    async def save(self) -> None:
        """Upsert this log entry to its provider table."""
        fields = self.columns()
        pk = [name for name, field in fields.items() if field.primary_key]
        output = PgOutput(dsn=async_default_dsn, use_async=True)
        async with output as conn:
            await conn.do_upsert(
                self,
                table_name=self.Meta.name,
                schema=self.Meta.schema,
                primary_keys=pk,
                use_conn=conn.get_connection()
            )
