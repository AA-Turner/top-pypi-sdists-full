"""Dispatcher: turn a declarative :class:`TargetSpec` into a runnable ``@task``."""

import typing as t

from dreadnode.airt.targets.http import http_target
from dreadnode.airt.targets.spec import TargetSpec
from dreadnode.airt.targets.streaming.nova_sonic import nova_sonic_target
from dreadnode.core.task import Task


def build_target(spec: TargetSpec) -> Task[..., t.Any]:
    """Build a dreadnode ``@task`` target from a :class:`TargetSpec`.

    Example (HTTP, Azure AI Foundry)::

        target = build_target(TargetSpec(
            endpoint="https://my.westus.inference.ml.azure.com/score",
            auth=TargetAuth(type="api_key", header="Authorization", value_prefix="Bearer ",
                            env_var="AZURE_FOUNDRY_KEY"),
            request_template='{"input_data": {"input_string": ["{prompt}"]}}',
            response_text_path="$.output",
        ))

    Example (streaming, Amazon Nova Sonic S2S)::

        target = build_target(TargetSpec(
            transport="streaming", protocol="nova_sonic", endpoint="us-east-1",
            options={"voice": "matthew"},
        ))
    """
    if spec.transport == "http":
        return http_target(spec)
    if spec.transport == "streaming":
        if spec.protocol == "nova_sonic":
            return nova_sonic_target(
                region=spec.endpoint or "us-east-1", name=spec.name, **spec.options
            )
        raise ValueError(f"Unknown streaming protocol: {spec.protocol!r}")
    raise ValueError(f"Unknown transport: {spec.transport!r}")
