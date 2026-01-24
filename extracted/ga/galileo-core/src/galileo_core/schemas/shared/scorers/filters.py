from enum import Enum
from typing import Literal, Union

from pydantic import Field
from typing_extensions import Annotated

from galileo_core.schemas.shared.filtered_collection import MapFilter, StringFilter


class ScorerJobFilterNames(str, Enum):
    node_name = "node_name"
    metadata = "metadata"


class NodeNameFilter(StringFilter):
    """
    Filters on node names in scorer jobs.
    """

    name: Literal[ScorerJobFilterNames.node_name] = ScorerJobFilterNames.node_name


class MetadataFilter(MapFilter):
    """
    Filters on metadata key-value pairs in scorer jobs.
    """

    name: Literal[ScorerJobFilterNames.metadata] = ScorerJobFilterNames.metadata


ScorerJobFilter = Annotated[
    Union[NodeNameFilter, MetadataFilter],
    Field(discriminator="name"),
]
