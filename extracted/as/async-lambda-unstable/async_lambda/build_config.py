from dataclasses import dataclass
from typing import Dict, List, Optional, Set, Union


def make_default_tags() -> Dict[str, str]:
    """
    Generates a dictionary of default tags for the async-lambda framework.

    Returns:
        Dict[str, str]: A dictionary containing the framework name and its version.
    """
    from . import __version__

    return {"framework": "async-lambda", "framework-version": __version__}


@dataclass
class AsyncLambdaBuildConfig:
    """
    AsyncLambdaBuildConfig is a configuration container for building AWS Lambda Serverless applications with advanced options.

    Attributes:
        environment_variables (Dict[str, str]): Environment variables to set for the Lambda function.
        policies (List[Union[str, dict]]): List of IAM policy ARNs or policy objects to attach.
        layers (List[str]): List of Lambda layer ARNs to include.
        subnet_ids (Set[str]): Set of subnet IDs for VPC configuration.
        security_group_ids (Set[str]): Set of security group IDs for VPC configuration.
        managed_queue_extras (List[dict]): Additional configuration for managed queues.
        method_settings (List[dict]): API Gateway method settings.
        tags (Dict[str, str]): Tags to assign to the Lambda function.
        logging_config (Dict[str, str]): Logging configuration options.
        domain_name (Optional[str]): Custom domain name for the Lambda/API.
        tls_version (Optional[str]): TLS version to use for the API.
        certificate_arn (Optional[str]): ARN of the SSL certificate for the domain.
        hosted_zone_id (Optional[str]): Hosted zone name for the Lambda/API.
        auto_create_acm_certificate (bool): Whether or not to auto create a certificate in ACM for the domain name. Must be used in conjunction with hosted_zone_id and domain_name to be used.

    Methods:
        new(config: dict) -> AsyncLambdaBuildConfig:
            Creates a new instance from a configuration dictionary.

        merge(other: AsyncLambdaBuildConfig):
            Merges another AsyncLambdaBuildConfig into this one, combining lists and updating dictionaries.
    """

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
    hosted_zone_id: Optional[str] = None
    auto_create_acm_certificate: Optional[bool] = None

    @classmethod
    def new(cls, config: dict) -> "AsyncLambdaBuildConfig":
        """
        Creates a new instance of AsyncLambdaBuildConfig from a configuration dictionary.

        Args:
            config (dict): A dictionary containing configuration options. Supported keys include:
                - policies (list): List of policy ARNs or policy objects.
                - environment_variables (dict): Environment variables for the Lambda function.
                - layers (list): List of Lambda layer ARNs.
                - subnet_ids (set or list): Set or list of subnet IDs for VPC configuration.
                - security_group_ids (set or list): Set or list of security group IDs for VPC configuration.
                - managed_queue_extras (list): Additional managed queue configuration.
                - method_settings (list): List of method settings for API Gateway.
                - tags (dict): Tags to assign to the Lambda function.
                - logging_config (dict): Logging configuration options.
                - domain_name (str, optional): Custom domain name for the Lambda/API.
                - tls_version (str, optional): TLS version to use.
                - certificate_arn (str, optional): ARN of the SSL certificate.
                - hosted_zone_id (str, optional): Hosted zone ID for the Lambda/API.

        Returns:
            AsyncLambdaBuildConfig: A new instance configured with the provided options.
        """
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
            hosted_zone_id=config.get("hosted_zone_id"),
            auto_create_acm_certificate=config.get("auto_create_acm_certificate"),
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
        if other.hosted_zone_id is not None:
            self.hosted_zone_id = other.hosted_zone_id
        if other.auto_create_acm_certificate is not None:
            self.auto_create_acm_certificate = other.auto_create_acm_certificate

    @property
    def function_properties(self):
        function_properties = {}
        if len(self.layers) > 0:
            function_properties["Layers"] = sorted(self.layers)
        if len(self.security_group_ids) > 0 or len(self.subnet_ids) > 0:
            function_properties["VpcConfig"] = {}
            if len(self.security_group_ids) > 0:
                function_properties["VpcConfig"]["SecurityGroupIds"] = sorted(
                    self.security_group_ids
                )
            if len(self.subnet_ids) > 0:
                function_properties["VpcConfig"]["SubnetIds"] = sorted(self.subnet_ids)
        if len(self.logging_config) > 0:
            function_properties["LoggingConfig"] = self.logging_config
        return function_properties


def get_build_config_for_stage(
    config: dict, stage: Optional[str] = None
) -> AsyncLambdaBuildConfig:
    """
    Generates and returns an AsyncLambdaBuildConfig object for a given deployment stage.

    This function initializes a build configuration from the provided config dictionary.
    If a stage is specified, it merges stage-specific configuration values into the build config.
    Default tags are also added to the build config before returning.

    Args:
        config (dict): The base configuration dictionary.
        stage (Optional[str], optional): The deployment stage to apply stage-specific configuration. Defaults to None.

    Returns:
        AsyncLambdaBuildConfig: The resulting build configuration object with stage-specific and default tags applied.
    """
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
    """
    Retrieves and constructs the build configuration for a specific task and optional stage.

    This function applies default build configuration values, then overrides them with
    task-specific and stage-specific configuration if available.

    Args:
        config (dict): The overall configuration dictionary containing tasks and stages.
        task_id (str): The identifier for the task to retrieve configuration for.
        stage (Optional[str], optional): The stage name to retrieve configuration for. Defaults to None.

    Returns:
        AsyncLambdaBuildConfig: The merged build configuration for the specified task and stage.
    """
    # Apply Defaults
    build_config = get_build_config_for_stage(config=config, stage=stage)
    # Retrieve Task-Specific Overrides
    override_config = get_override_build_config_for_task(
        config=config, task_id=task_id, stage=stage
    )
    # Take the super-set of both configurations, prioritizing task-specific values on conflicts
    build_config.merge(override_config)
    return build_config


def get_override_build_config_for_task(
    config: dict, task_id: str, stage: Optional[str] = None
) -> AsyncLambdaBuildConfig:
    """
    Retrieves and constructs the build configuration, containing solely task-specific overrides, for a specific task and optional stage.

    Args:
        config (dict): The overall configuration dictionary containing tasks and stages.
        task_id (str): The identifier for the task to retrieve configuration for.
        stage (Optional[str], optional): The stage name to retrieve configuration for. Defaults to None.

    Returns:
        AsyncLambdaBuildConfig: The build configuration with only override values for the specified task and stage.
    """
    build_config = AsyncLambdaBuildConfig.new({})
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
    return build_config
