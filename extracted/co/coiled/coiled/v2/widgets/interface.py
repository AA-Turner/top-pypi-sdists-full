from typing import Any, Mapping, Optional

from typing_extensions import Protocol


class ClusterWidget(Protocol):
    def update(
        self,
        cluster_details: Optional[Mapping[str, Any]],
        logs,
        *args,
        final_update=None,
        **kwargs,
    ) -> None:
        pass
