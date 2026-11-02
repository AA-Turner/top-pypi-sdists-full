"""Capture child declarations against their parent's retained source."""

from dataclasses import dataclass
from typing import ParamSpec, TypeVar

from labqoat._generated.compute_publication import ComputePublication
from labqoat.compute.function import Function
from labqoat.json_document import JsonDocument, JsonValue

P = ParamSpec("P")
R = TypeVar("R")


@dataclass(frozen=True)
class ChildPublication:
    """Use the service's source snapshot while selecting each callee's own declared image and resources."""

    parent: ComputePublication

    def capture(self, function: Function[P, R], arguments: dict[str, JsonValue] | None = None) -> ComputePublication:
        """Worker publication never uploads host files or receives management credentials."""
        declaration = function.capture_for(arguments)
        key = f"{declaration.module}:{function.local.__qualname__}"
        if key not in self.parent.bindings:
            raise ValueError(
                f"{declaration.module}.{function.local.__qualname__} (App {function.app_name!r}) was not published "
                f"with this run. Import it at the top of a module of this App, or declare it on the same App, "
                f"then launch again."
            )
        return ComputePublication(
            app_name=function.app_name,
            source_asset_sha=self.parent.source_asset_sha,
            image=JsonDocument.expect_scalar(self.parent.bindings[key], str),
            images=self.parent.images,
            bindings=self.parent.bindings,
            runtime_version=self.parent.runtime_version,
            recovery_protocol=self.parent.recovery_protocol,
            distributed_recovery_protocol=self.parent.distributed_recovery_protocol,
            workflow_replay_protocol=self.parent.workflow_replay_protocol,
            app=self.parent.app,
            function=declaration,
        )
