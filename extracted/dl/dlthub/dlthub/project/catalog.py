from typing import Dict

from dlthub.destinations.dataset import WritableDataset, DatasetConfig

from .entity_factory import EntityFactory
from .project_context import ProjectRunContext


class Catalog:
    def __init__(self, project: ProjectRunContext):
        """A catalog of data available in `project`. You can use it to inspect datasets and tables
        on destinations they are available and read/write data via dataframes, arrow or dbapi.
        """
        self._factory = EntityFactory(project.project)
        self._project_config = project.project
        self._project = project

    def __getitem__(self, dataset_name: str) -> WritableDataset:
        return self.dataset(dataset_name=dataset_name)

    def __getattr__(self, dataset_name: str) -> WritableDataset:
        return self.dataset(dataset_name=dataset_name)

    def dataset(self, dataset_name: str, destination_name: str = None) -> WritableDataset:
        return self._factory.get_dataset(dataset_name, destination_name=destination_name)

    @property
    def datasets(self) -> Dict[str, DatasetConfig]:
        # TODO: those are only explicit datasets. we need a method
        # that returns both explicit and implicit datasets, same for other entities
        return self._project_config.datasets

    def __str__(self) -> str:
        msg = f"Datasets in project {self._project.name} for profile {self._project.profile}:\n"
        datasets = self._project_config.datasets
        if datasets:
            for dataset_name, _ in datasets.items():
                dataset = self.dataset(dataset_name=dataset_name)
                msg += (
                    f"{dataset_name}@{dataset._destination.destination_name}"
                    + f"[{str(dataset._destination.configuration(None, accept_partial=True))}]\n"
                )
        else:
            msg += "No datasets found"
        return msg
