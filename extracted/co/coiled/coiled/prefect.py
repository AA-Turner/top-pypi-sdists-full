from packaging.version import Version

try:
    import prefect  # type: ignore # noqa
except ImportError as e:
    raise ImportError("The `coiled.prefect` module requires `prefect` to be installed.") from e

from typing import Optional

import dask.config
import pydantic
from prefect.blocks.core import Block  # type: ignore

if Version(prefect.__version__).major < 3 and Version(pydantic.__version__).major >= 2:
    # Prefect docs say this is required for pydantic>=2
    # https://docs.prefect.io/latest/concepts/blocks/#secret-fields
    from pydantic.v1 import Field, SecretStr
else:
    from pydantic import Field, SecretStr


class Credentials(Block):
    _block_type_name = "Coiled Credentials"
    _logo_url = "https://blog.coiled.io/_static/logo.svg"
    _documentation_url = "https://docs.coiled.io/user_guide/labs/prefect.html"
    _code_example = """
    ```python
    from coiled.prefect import Credentials

    Credentials.load("BLOCK_NAME").login()
    ```
    """

    token: SecretStr = Field(default=..., description="Coiled API token.")
    account: Optional[str] = Field(default=None, description="Deprecated, use ``workspace``.")
    workspace: Optional[str] = Field(default=None, description="Coiled workspace to use.")

    def login(self):
        workspace = self.workspace or self.account
        dask.config.set({
            "coiled.token": self.token.get_secret_value(),
            "coiled.account": workspace,
            "coiled.workspace": workspace,
        })
