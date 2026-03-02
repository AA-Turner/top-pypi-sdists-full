from typing import Iterable, Type

from dlt.common.pipeline import LoadInfo
import dlthub

from .config.config import Project
from .exceptions import ProjectException, ProjectExplicitEntityNotFound
from .entity_factory import EntityFactory


class PipelineManager:
    def __init__(
        self, project_config: Project, factory_class: Type[EntityFactory] = EntityFactory
    ) -> None:
        self.project_config = project_config
        self.factory = factory_class(project_config)

    def run_pipeline(
        self, pipeline_name: str, limit: int = None, resources: Iterable[str] = None
    ) -> LoadInfo:
        """
        Get a pipeline, DltSource and run it with the dlthub.runner
        """
        pipeline_config = self.factory._get_pipeline_config(pipeline_name)

        if not pipeline_config:
            raise ProjectExplicitEntityNotFound(
                self.project_config.project_dir, "pipeline", pipeline_name
            )

        source_name = pipeline_config.get("source")
        if not source_name:
            raise ProjectException(
                self.project_config.project_dir,
                f"Source is not defined for pipeline '{pipeline_name}'",
            )

        # create pipeline before we create the source
        pipeline = self.factory.get_pipeline(pipeline_name)

        # config will be injected when source is instantiated without args
        # NOTE: args defined in yaml will be automatically passed like for any other provider
        # TODO: there are non injectable arguments (without defaults), we could pass them here from
        # config. Currently they are not supported
        source = self.factory.get_source(source_name)()
        if limit is not None:
            source = source.add_limit(limit)
        if resources:
            source = source.with_resources(*resources)

        # get additional data contract from dataset
        if dataset_config := self.project_config.datasets.get(pipeline_config.get("dataset_name")):
            schema_contract = dataset_config.get("contract")
        else:
            schema_contract = None
        # TODO: see WritableDataset for relevant to do.
        # ad hoc schema contract must not change schema (but here they will)

        runner_kwargs = self.factory._get_runner_config(pipeline_name)
        return dlthub.runner(pipeline, **runner_kwargs).run(source, schema_contract=schema_contract)  # type: ignore[no-any-return]
