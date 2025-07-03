from typing import Optional

from .. import ui
from ..api import DAPClient
from ..dap_types import Credentials


async def list_tables(
    base_url: str,
    credentials: Credentials,
    namespace: str,
    tracking: Optional[bool] = None,
) -> None:
    async with DAPClient(
        base_url=base_url,
        credentials=credentials,
        tracking=tracking,
    ) as session:
        ui.title(f"Get list of all tables in [bold]{namespace}[/bold] namespace")
        tables = await session.get_tables(namespace)
        ui.success(
            f"Found [bold]{len(tables)}[/bold] tables in [bold]{namespace}[/bold] namespace: "
            + ", ".join(tables)
        )
        if not ui.is_interactive():
            # TODO: non interactive output to stdout should be revised, use json for all commands?
            for t in tables:
                print(t)
