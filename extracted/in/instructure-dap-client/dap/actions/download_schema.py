from typing import Optional

from ..api import DAPClient
from ..dap_types import Credentials


async def download_schema(
    base_url: str,
    credentials: Credentials,
    namespace: str,
    table: str,
    output_directory: str,
    tracking: Optional[bool] = None,
) -> None:
    async with DAPClient(
        base_url=base_url,
        credentials=credentials,
        tracking=tracking,
    ) as session:
        await session.download_tables_schema(namespace, table, output_directory)
