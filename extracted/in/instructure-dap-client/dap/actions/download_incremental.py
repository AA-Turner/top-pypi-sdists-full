from datetime import datetime
from typing import Optional

from ..api import DAPClient
from ..dap_types import Credentials, Format, IncrementalQuery


async def download_incremental(
    base_url: str,
    credentials: Credentials,
    namespace: str,
    table: str,
    format: Format,
    output_directory: str,
    since: datetime,
    until: Optional[datetime],
    tracking: Optional[bool] = None,
) -> None:
    query = IncrementalQuery(
        format=format,
        mode=None,
        since=since,
        until=until,
    )
    async with DAPClient(
        base_url=base_url,
        credentials=credentials,
        tracking=tracking,
    ) as session:
        await session.download_tables_data(
            namespace,
            table,
            query,
            output_directory,
        )
