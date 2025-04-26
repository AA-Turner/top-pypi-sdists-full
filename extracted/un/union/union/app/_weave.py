from dataclasses import dataclass
from typing import TYPE_CHECKING

from ._models import AppConfigProtocol, AppSerializationSettings

if TYPE_CHECKING:
    from ._models import App


@dataclass
class WeaveConfig(AppConfigProtocol):
    project: str
    entity: str
    host: str

    def before_to_union_idl(self, app: "App", settings: AppSerializationSettings):
        """Modify app in place at the beginning of `App._to_union_idl`."""
        app.env["WANDB_BASE_URL"] = self.host
        app.env["WANDB_PROJECT"] = self.project

        # When we have links set the link to:
        # f"{host}/{entity}/{project}/weave/traces"
