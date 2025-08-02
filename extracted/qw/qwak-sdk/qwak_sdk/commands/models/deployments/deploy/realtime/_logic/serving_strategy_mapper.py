from __future__ import annotations

from typing import Dict, List

from _qwak_proto.qwak.auto_scaling.v1.auto_scaling_pb2 import AutoScalingConfig
from _qwak_proto.qwak.deployment.deployment_pb2 import (
    RealTimeConfig,
    ServingStrategy,
    TrafficConfig,
)
from _qwak_proto.qwak.ecosystem.v0.ecosystem_pb2 import UserContextEnvironmentDetails
from qwak.exceptions import QwakException

from qwak_sdk.commands.audience._logic.config.v1.audience_config import AudienceConfig
from qwak_sdk.commands.models.deployments.deploy._logic.deploy_config import (
    DeployConfig,
)


def create_realtime_serving_strategy(
    auto_scaling: AutoScalingConfig,
    audiences: List[AudienceConfig],
    fallback_variation: str,
    variation_name: str,
    variation_protected_state: bool = False,
) -> ServingStrategy:
    return ServingStrategy(
        realtime_config=(
            RealTimeConfig(
                auto_scaling_config=auto_scaling,
                traffic_config=TrafficConfig(
                    selected_variation_name=variation_name,
                    audience_routes_entries=[
                        audience.to_audience_route_entry(index)
                        for index, audience in enumerate(audiences)
                    ],
                    fallback_variation=fallback_variation,
                    selected_variation_protect_state=variation_protected_state,
                ),
            )
        )
    )


def create_realtime_serving_strategy_from_deploy_config(
    deploy_config: DeployConfig,
    environment_name_to_config: Dict[str, UserContextEnvironmentDetails],
) -> Dict[str, ServingStrategy]:
    serving_strategies = {}
    errors = []
    variation_name = deploy_config.realtime.variation_name or "default"
    variation_protected_state = deploy_config.realtime.variation_protected_state
    fallback_variation = deploy_config.realtime.fallback_variation
    auto_scaling = (
        deploy_config.auto_scaling.to_autoscaling_api()
        if deploy_config.auto_scaling
        else None
    )
    for env_name, env_config in environment_name_to_config.items():
        try:
            serving_strategies[env_config.id] = create_realtime_serving_strategy(
                auto_scaling,
                deploy_config.realtime.audiences,
                fallback_variation,
                variation_name,
                variation_protected_state,
            )

        except QwakException as e:
            errors.append(e.message)

    if errors:
        raise QwakException("\n".join(errors))

    return serving_strategies
