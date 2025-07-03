from typing import Optional

from ..api import DAPClient
from ..dap_types import Credentials, Format, SnapshotQuery


async def download_snapshot(
    base_url: str,
    credentials: Credentials,
    namespace: str,
    table: str,
    format: Format,
    output_directory: str,
    tracking: Optional[bool] = None,
) -> None:
    query = SnapshotQuery(format=format, mode=None)
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
