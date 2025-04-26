from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from chalk.client import DatasetRevision


class BaseCatalog(Protocol):
    def write_to_catalog(self, revision: "DatasetRevision", destination: str) -> None:
        ...
