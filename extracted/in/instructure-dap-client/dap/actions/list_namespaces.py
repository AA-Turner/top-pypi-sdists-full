from typing import Optional

from .. import ui
from ..api import DAPClient
from ..dap_types import Credentials


async def list_namespaces(
    base_url: str,
    credentials: Credentials,
    tracking: Optional[bool] = None,
) -> None:
    async with DAPClient(
        base_url=base_url,
        credentials=credentials,
        tracking=tracking,
    ) as session:
        ui.title("Get list of all namespaces")
        namespaces = await session.get_namespaces()
        ui.success(
            f"Found [bold]{len(namespaces)}[/bold] namespaces: " + ", ".join(namespaces)
        )
        if not ui.is_interactive():
            for n in namespaces:
                print(n)
