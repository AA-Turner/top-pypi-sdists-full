from typing import Any, Optional, Union, TYPE_CHECKING, Dict, List

import dlt
from dlt.common import logger
from dlt.common.destination import AnyDestination, Destination
from dlt.common.schema import Schema
from dlt.common.typing import Unpack
from dlt.sources import AnySourceFactory, SourceReference
from dlt.common.validation import validate_dict


from dlthub.destinations.dataset import WritableDataset
from dlthub.project.config.typing import PipelineRunConfig
from dlthub._runner.utils import parse_retry_policy


if TYPE_CHECKING:
    from dlthub.legacy.transformations.transformations import Transformation
    from dlthub.legacy.transformations.config import TransformationConfig
    from dlthub.cache.cache import Cache
else:
    Transformation = Any
    TransformationConfig = Any
    Cache = Any


from .config.config import Project
from .config.typing import DatasetConfig, PipelineConfig, SourceConfig, DestinationConfig
from .exceptions import ProjectException, ProjectExplicitEntityNotFound, InvalidDestinationException


class EntityFactory:
    """
    A factory class for managing and creating project entities such as sources, destinations,
    datasets, caches, transformations, and pipelines. It provides methods to retrieve or create
    these entities based on the project configuration, with support for explicit and implicit
    configurations.
    """

    def __init__(self, project_config: Project):
        """
        Initializes the EntityFactory with the given project configuration.

        Args:
            project_config (Project): The project configuration object containing settings
            for managing sources, destinations, datasets, caches, transformations, and pipelines.

        Example:
            >>> from dlthub.project.entity_factory import EntityFactory
            >>> from dlthub.project.config.config import Project
            >>> project_config = Project({
            ...     "sources": {"my_source": {"type": "sql_database"}},
            ...     "destinations": {"my_dest": {"type": "postgres"}},
            ...     "datasets": {"my_dataset": {"destination": "my_dest"}},
            ... }, settings={})

        """
        self.project_config = project_config

    def get_source(self, source_ref_or_name: str) -> AnySourceFactory:
        """
        Creates a source factory based on the provided source reference or name.

        This method retrieves the source configuration from the project settings using the
        provided `source_ref_or_name`. If no specific configuration is found, it assumes the
        source reference is implicit. The method resolves the source type and applies any
        additional arguments (`with_args`) from the configuration. It then creates and returns
        a source factory instance.

        Args:
            source_ref_or_name (str): The reference or name of the source to create a factory for.

        Returns:
            AnySourceFactory: A source factory instance configured with the specified reference or
            name.

        Raises:
            ProjectExplicitEntityNotFound: If the source configuration is not found and undefined
            entities are not allowed.

        Behavior:
            - Retrieves the source configuration from the project settings.
            - If no configuration is found, assumes the source reference is implicit.
            - Resolves the source type from the configuration or uses the provided reference/name.
            - Applies additional arguments (`with_args`) from the configuration.
            - Overrides the default section name with the source name for compatibility with
                the configuration system.
            - Creates and returns a source factory instance.

        Example:
            >>> entity_factory = EntityFactory(project_config)
            >>> source = entity_factory.get_source("my_source")

            # Using an implicit source reference
            >>> source = entity_factory.get_source("dlt.sources.sql_database")
            # OR
            >>> source = entity_factory.get_source("sql_database")

        """
        source_config = self._get_source_config(source_ref_or_name)
        if source_config is None:
            # no specific config, assumes we use source ref
            source_config = {}

        # get source type from config or use source name as reference
        # this makes source implicit
        source_type = source_config.get("type") or source_ref_or_name

        # check if "with_args" is present
        with_args_dict = source_config.get("with_args") or {}
        # Override the default section name with the source name to make the configuration
        # compatible with the CustomLoaderDocProvider we are using in config.Config
        source_factory = SourceReference.find(source_type).clone(
            name=source_ref_or_name, section=source_ref_or_name, **with_args_dict
        )
        return source_factory

    def get_destination(self, destination_ref_or_name: str) -> AnyDestination:
        """
        Instantiates a destination from the project configuration using the provided
        `destination_ref_or_name`, or, if not explicitly forbidden by the project settings,
        instantiates an ad hoc destinations for one the predefined destinations (e.g. duckdb,
        postgres, etc.).

        Args:
            destination_ref_or_name (str): The reference or name of the destination to retrieve or
            create.

        Returns:
            AnyDestination: An instance of the resolved or created destination.

        Raises:
            ProjectExplicitEntityNotFound: If the destination is not found and undefined entities
            are not allowed.

        Behavior:
            - If the destination configuration is an instance of `Destination`, it is returned
                directly.
            - If the configuration contains a `type` field, a named destination is created using the
                `Destination.from_reference` method.
            - If no `type` is specified, the shorthand notation is used to create the destination.

        Example:
            >>> entity_factory = EntityFactory({"destinations": {"my_dest": {"type": "postgres"}}})
            >>> destination = entity_factory.get_destination("my_dest")
            # or (if project.allow_undefined_entities: True)
            >>> ad_hoc_destination = entity_factory.get_destination("dlt.destinations.duckdb")
            # or
            >>> ad_hoc_destination = entity_factory.get_destination("duckdb")
        """
        destination_config = self._get_destination_config(destination_ref_or_name)
        if destination_config is None:
            # allows for ad hoc destinations
            destination_config = {}

        # accept destination factory instance
        if isinstance(destination_config, Destination):
            return destination_config

        if destination_type := destination_config.get("type"):
            # create named destination
            return Destination.from_reference(
                destination_type, destination_name=destination_ref_or_name
            )
        else:
            # if destination does not have a type, use shorthand notation
            return Destination.from_reference(destination_ref_or_name)

    def get_dataset(
        self,
        dataset_name: str,
        destination_name: str = None,
        schema: Union[Schema, str, None] = None,
    ) -> WritableDataset:
        """
        Retrieves or creates a writable dataset instance based on the provided dataset name and
        destination.

        This method resolves the dataset configuration from the project settings using the provided
        `dataset_name`. It also determines the possible destinations for the dataset, either
        explicitly defined in the configuration or inferred from available pipelines. If no
        destination is provided, the first available destination is selected. The method ensures
        that the specified destination is valid for the dataset.

        Args:
            dataset_name (str): The name of the dataset to retrieve or create.
            destination_name (str, optional): The name of the destination to associate with the
                dataset. If not provided, the first available destination is used.
            schema (Union[Schema, str, None], optional): The schema to associate with the dataset.
                Can be a `Schema` object, a string representing the schema name, or `None`.

        Returns:
            WritableDataset: An instance of the writable dataset configured with the specified
                dataset name, destination, and schema.

        Raises:
            InvalidDestinationException: If the specified destination is not valid for the dataset
                or if no valid destinations are available.

        Behavior:
            - Resolves the dataset configuration from the project settings.
            - Determines the possible destinations for the dataset, either explicitly defined or
                inferred from pipelines.
            - Validates the specified destination against the available destinations.
            - Creates and returns a `WritableDataset` instance with the resolved configuration.

        Example:
            >>> entity_factory = EntityFactory(project_config)
            >>> dataset = entity_factory.get_dataset("my_dataset", destination_name="postgres")

            # Using the first available destination
            >>> dataset = entity_factory.get_dataset("my_dataset")
        """
        # force if datasets must be explicit
        dataset_config = self._get_dataset_config(dataset_name)
        # get possible destinations for dataset_name using explicit config and available pipelines
        available_destinations = self._resolve_dataset_destinations(dataset_name)
        if not destination_name:
            destination_name = available_destinations[0]
        elif destination_name not in available_destinations:
            raise InvalidDestinationException(
                self.project_config.project_dir,
                dataset_name,
                destination_name,
                available_destinations,
            )
        return WritableDataset(
            dataset_config,
            destination=self.get_destination(destination_name),
            dataset_name=dataset_name,
            schema=schema,
        )

    def get_cache(self, name: str) -> Cache:
        """
        Retrieves and instantiates a cache based on the provided cache name.
        Any associated input and output datasets from the cache's configuration are resolved and
        converted into dataset instances.

        Args:
            name (str): The name of the cache to retrieve or create. If `"."` or not provided, the
                first available cache is used.

        Returns:
            Cache: An instance of the cache configured with the specified name and its associated
            inputs and outputs.

        Raises:
            ProjectException: If no caches are defined in the project configuration.
            ProjectExplicitEntityNotFound: If the specified cache name is not found in the project
            configuration.

        Example:
            >>> entity_factory = EntityFactory(project_config)
            >>> cache = entity_factory.get_cache("my_cache")

            # Using the first available cache
            >>> cache = entity_factory.get_cache(".")
        """
        from dlthub.cache.cache import create_cache as _create_cache

        available_caches = list(self.project_config.caches.keys())

        # TODO: allow for explicit cache with default settings, we can also implement cache registry
        if not available_caches:
            raise ProjectException(self.project_config.project_dir, "No caches found in project.")

        # TODO: apply the . notation to all entities or drop it
        if not name or name == ".":
            name = available_caches[0]
            logger.info(f"No cache name given, taking the first discovered: {name}")

        cache_config = self.project_config.caches.get(name)

        if not cache_config:
            raise ProjectExplicitEntityNotFound(self.project_config.project_dir, "cache", name)

        # create dataset instances from strings
        cache_config["name"] = name
        # create factories from config
        for input in cache_config.get("inputs", []):
            dataset = input["dataset"]
            if isinstance(dataset, str):
                input["dataset"] = self.get_dataset(dataset)
        for output in cache_config.get("outputs", []):
            dataset = output["dataset"]
            if isinstance(dataset, str):
                output["dataset"] = self.get_dataset(dataset)

        return _create_cache(cache_config)

    def get_transformation(self, name: str) -> Transformation:
        """
        Retrieves and instantiates a transformation based on the provided transformation name.

        This method resolves the transformation configuration from the project settings using the
        provided `name`. If no name is provided or the name is `"."`, the first available
        transformation in the project configuration is selected. The method ensures that the
        specified transformation exists and is properly configured. It also resolves any associated
        cache references.

        Args:
            name (str): The name of the transformation to retrieve or create. If `"."` or not
                provided, the first available transformation is used.

        Returns:
            Transformation: An instance of the transformation configured with the specified name and
            its associated cache.

        Raises:
            ProjectException: If no transformations are defined in the project configuration.
            ProjectExplicitEntityNotFound: If the specified transformation name is not found in the
            project configuration.

        Behavior:
            - Resolves the transformation configuration from the project settings.
            - If no transformation name is provided or the name is `"."`, selects the first
                available transformation.
            - Ensures that the specified transformation exists in the project configuration.
            - Resolves any associated cache references and includes them in the transformation
                configuration.
            - Creates and returns a transformation instance using the resolved configuration.

        Example:
            >>> entity_factory = EntityFactory(project_config)
            >>> transformation = entity_factory.get_transformation("my_transformation")

            # Using the first available transformation
            >>> transformation = entity_factory.get_transformation(".")
        """
        from dlthub.legacy.transformations.transformations import (
            create_transformation as _create_transformation,
        )

        # TODO: apply the . notation to all entities or drop it
        available_ts = list(self.project_config.transformations.keys())

        if not available_ts:
            raise ProjectException(
                self.project_config.project_dir, "No transformations found in project."
            )

        if not name or name == ".":
            name = available_ts[0]
            logger.info(f"No transformation name given, taking the first discovered: {name}")

        transformation_config: TransformationConfig
        if transformation_config := self.project_config.transformations.get(name):
            transformation_config["name"] = name
            # resolve cache
            if cache_name := transformation_config.get("cache"):
                transformation_config["cache"] = self.get_cache(cache_name)
            return _create_transformation(transformation_config)
        else:
            raise ProjectExplicitEntityNotFound(
                self.project_config.project_dir, "transformation", name
            )

    def get_pipeline(
        self, pipeline_name: str, **explicit_config: Unpack[PipelineConfig]
    ) -> dlt.Pipeline:
        """Creates a pipeline using expicitly declared `pipeline_name` or by pipeline
        registry (tbd.)

        Applies `explict_config` that may be passed by pipeline runner to override defaults.
        """
        """
        Retrieves or creates a pipeline instance based on the provided pipeline name and
        the project configuration or a given explicit configuration.

        Args:
            pipeline_name (str): The name of the pipeline to retrieve or create.
            **explicit_config (Unpack[PipelineConfig]): Optional explicit configuration to override
                the configured pipeline settings.

        Returns:
            dlt.Pipeline: An instance of the pipeline configured with the specified name,
                destination, and dataset.

        Raises:
            ProjectException: If the pipeline configuration does not define a destination or dataset
            ProjectExplicitEntityNotFound: If the specified pipeline name is not found in the
                project configuration and undefined entities are not allowed.

        Behavior:
            - Resolves the pipeline configuration from the project settings.
            - Applies any explicit configuration passed via `explicit_config` to override defaults.
            - Validates that the pipeline has a defined destination and dataset.
            - Creates a dataset instance, which also validates the destination and dataset
                configuration.
            - Returns a pipeline instance configured with the resolved destination and dataset.

        Example:
            >>> entity_factory = EntityFactory(project_config)
            >>> pipeline = entity_factory.get_pipeline("my_pipeline")
            # Overriding the dataset_name in the project's pipeline configuration:
            >>> pipeline = entity_factory.get_pipeline("my_pipeline", dataset_name="custom_dataset")
        """

        pipeline_config = self._get_pipeline_config(pipeline_name)
        if pipeline_config is None:
            pipeline_config = {}
        if explicit_config:
            # apply explicit config, make sure we create copy not to change the original
            pipeline_config = {**pipeline_config, **explicit_config}

        destination_name = pipeline_config.get("destination")
        if not destination_name:
            raise ProjectException(
                self.project_config.project_dir,
                f"Destination is not defined for pipeline '{pipeline_name}'",
            )

        # verify if a valid dataset exists
        dataset_name = pipeline_config.get("dataset_name")
        if not dataset_name:
            raise ProjectException(
                self.project_config.project_dir,
                f"Dataset is not defined for pipeline '{pipeline_name}'",
            )

        # create dataset, which also creates destination and does required checks
        # NOTE: destination is not physically accessed
        dataset_ = self.get_dataset(dataset_name, destination_name)
        return dlt.pipeline(
            pipeline_name,
            destination=dataset_._destination,
            dataset_name=dataset_name,
        )

    def list_sources(self) -> List[str]:
        """
        Lists all sources in the project configuration
        """
        return list(self.project_config.sources.keys())

    def list_destinations(self) -> List[str]:
        """
        Lists all destinations in the project configuration
        """
        return list(self.project_config.destinations.keys())

    def list_datasets(self) -> List[str]:
        """
        Lists all datasets in the project configuration
        If `allow_undefined_entities` is set to True, it also lists datasets inferred from pipelines
        """
        datasets = list(self.project_config.datasets.keys())
        if self.allow_undefined_entities:
            for pipeline_name in self.list_pipelines():
                dataset_name = self._resolve_pipeline_dataset(pipeline_name)
                if dataset_name and dataset_name not in datasets:
                    datasets.append(dataset_name)
        return datasets

    def list_pipelines(self) -> List[str]:
        """
        Lists all pipelines in the project configuration
        """
        return list(self.project_config.pipelines.keys())

    def list_caches(self) -> List[str]:
        """
        Lists all caches in the project configuration
        """
        return list(self.project_config.caches.keys())

    def list_transformations(self) -> List[str]:
        """
        Lists all transformations in the project configuration
        """
        return list(self.project_config.transformations.keys())

    @property
    def allow_undefined_entities(self) -> bool:
        return self.project_config.settings.get("allow_undefined_entities", True)

    def _get_pipeline_config(self, pipeline_name: str) -> Optional[PipelineConfig]:
        pipeline_config = self.project_config.pipelines.get(pipeline_name)
        if not self.allow_undefined_entities and not pipeline_config:
            raise ProjectExplicitEntityNotFound(
                self.project_config.project_dir, "pipeline", pipeline_name
            )
        # TODO: consider cloning all configs to prevent modification of the original
        return pipeline_config

    def _get_source_config(self, source_name: str) -> Optional[SourceConfig]:
        source_config = self.project_config.sources.get(source_name)
        if not self.allow_undefined_entities and not source_config:
            raise ProjectExplicitEntityNotFound(
                self.project_config.project_dir, "source", source_name
            )
        return source_config

    def _get_destination_config(self, destination_name: str) -> Optional[DestinationConfig]:
        destination_config = self.project_config.destinations.get(destination_name)
        if not self.allow_undefined_entities and not destination_config:
            raise ProjectExplicitEntityNotFound(
                self.project_config.project_dir, "destination", destination_name
            )
        return destination_config

    def _get_dataset_config(self, dataset_name: str) -> Optional[DatasetConfig]:
        dataset_config = self.project_config.datasets.get(dataset_name)
        if not self.allow_undefined_entities and not dataset_config:
            raise ProjectExplicitEntityNotFound(
                self.project_config.project_dir, "dataset", dataset_name
            )
        return dataset_config

    def _resolve_dataset_destinations(self, dataset_name: str) -> List[str]:
        """Infers possible destinations from the pipelines if not explicitly limited"""

        dataset_config = self._get_dataset_config(dataset_name) or {}
        available_destinations = dataset_config.get("destination")

        # if no explicit destinations, take them from defined pipelines
        if available_destinations is None:
            available_destinations = []
            for pipeline_config in self.project_config.pipelines.values():
                if pipeline_config:
                    if dataset_name == pipeline_config.get("dataset_name"):
                        if destination_name := pipeline_config.get("destination"):
                            available_destinations.append(destination_name)

        if not available_destinations:
            raise InvalidDestinationException(
                self.project_config.project_dir,
                dataset_name,
                None,
                available_destinations,
            )

        # deduplicate but preserve order
        seen: Dict[str, str] = {}
        return [seen.setdefault(x, x) for x in available_destinations if x not in seen]

    def _resolve_pipeline_dataset(self, pipeline_name: str) -> Optional[str]:
        """Infers possible implicit datasets from the pipeline if not explicitly limited"""

        config = self._get_pipeline_config(pipeline_name)
        if config:
            dataset_name = config.get("dataset_name")
            if dataset_name:
                return dataset_name
        return None

    def _get_runner_config(self, pipeline_name: str) -> Dict[str, Any]:
        """Validate and build runner keyword args from pipeline run configuration in dlt.yml"""
        run_config = self._get_pipeline_config(pipeline_name).get("run_config", {})
        if not run_config:
            return {}

        validate_dict(spec=PipelineRunConfig, doc=run_config, path=".")

        runner_args: Dict[str, Any] = {}

        for key in ("run_from_clean_folder", "retry_pipeline_steps"):
            if key in run_config:
                runner_args[key] = run_config[key]  # type: ignore[literal-required]

        if "retry_policy" in run_config:
            runner_args["retry_policy"] = parse_retry_policy(run_config["retry_policy"])

        # store_trace_info - can be bool or pipeline name
        if "store_trace_info" in run_config:
            trace_info = run_config["store_trace_info"]
            if isinstance(trace_info, bool):
                runner_args["store_trace_info"] = trace_info
            else:
                # Try to get pipeline by name
                if trace_info in self.project_config.pipelines:
                    runner_args["store_trace_info"] = self.get_pipeline(str(trace_info))
                else:
                    raise ProjectException(
                        self.project_config.project_dir,
                        f"Trace pipeline `{trace_info}` not defined in dlt.yml",
                    )
        return runner_args
