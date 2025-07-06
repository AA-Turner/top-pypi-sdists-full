from dataclasses import dataclass
from typing import Dict, List, Optional, Set, Union


def make_default_tags() -> Dict[str, str]:
    from . import __version__

    return {"framework": "async-lambda", "framework-version": __version__}


@dataclass
class AsyncLambdaBuildConfig:
    environment_variables: Dict[str, str]
    policies: List[Union[str, dict]]
    layers: List[str]
    subnet_ids: Set[str]
    security_group_ids: Set[str]
    managed_queue_extras: List[dict]
    method_settings: List[dict]
    tags: Dict[str, str]
    logging_config: Dict[str, str]
    domain_name: Optional[str] = None
    tls_version: Optional[str] = None
    certificate_arn: Optional[str] = None

    @classmethod
    def new(cls, config: dict) -> "AsyncLambdaBuildConfig":
        return cls(
            policies=list(config.get("policies", list())),
            environment_variables=config.get("environment_variables", dict()),
            layers=list(config.get("layers", list())),
            subnet_ids=set(config.get("subnet_ids", set())),
            security_group_ids=set(config.get("security_group_ids", set())),
            managed_queue_extras=list(config.get("managed_queue_extras", list())),
            method_settings=list(config.get("method_settings", list())),
            tags=config.get("tags", dict()),
            logging_config=config.get("logging_config", dict()),
            domain_name=config.get("domain_name"),
            tls_version=config.get("tls_version"),
            certificate_arn=config.get("certificate_arn"),
        )

    def merge(self, other: "AsyncLambdaBuildConfig"):
        self.policies += other.policies
        self.environment_variables.update(other.environment_variables)
        self.layers = list(dict.fromkeys(self.layers + other.layers))
        self.subnet_ids.update(other.subnet_ids)
        self.security_group_ids.update(other.security_group_ids)
        self.managed_queue_extras += other.managed_queue_extras
        self.tags.update(other.tags)
        self.logging_config.update(other.logging_config)
        if other.domain_name is not None:
            self.domain_name = other.domain_name
        if other.tls_version is not None:
            self.tls_version = other.tls_version
        if other.certificate_arn is not None:
            self.certificate_arn = other.certificate_arn


def get_build_config_for_stage(
    config: dict, stage: Optional[str] = None
) -> AsyncLambdaBuildConfig:
    build_config = AsyncLambdaBuildConfig.new(config)
    if stage is not None:
        # Apply Stage Defaults
        stage_config = config.setdefault("stages", {}).setdefault(stage, {})
        build_config.merge(AsyncLambdaBuildConfig.new(stage_config))

    build_config.tags.update(make_default_tags())
    return build_config


def get_build_config_for_task(
    config: dict, task_id: str, stage: Optional[str] = None
) -> AsyncLambdaBuildConfig:
    # Apply Defaults
    build_config = get_build_config_for_stage(config, stage)

    if task_id in config.setdefault("tasks", {}):
        # Apply task defaults
        task_config = config["tasks"].setdefault(task_id, {})
        build_config.merge(AsyncLambdaBuildConfig.new(task_config))

        if stage is not None:
            # Apply task stage defaults
            task_stage_config = task_config.setdefault("stages", {}).setdefault(
                stage, {}
            )
            build_config.merge(AsyncLambdaBuildConfig.new(task_stage_config))
    build_config.tags.update(make_default_tags())
    return build_config
