from typing import NamedTuple, Optional, Dict, Any


class IndexEmbed(NamedTuple):
    """
    IndexEmbed represents the index embedding configuration when creating an index from a model.
    """

    model: str
    """
    The name of the embedding model to use for the index.
    Required.
    """

    field_map: Dict[str, Any]
    """
    A mapping of field names to their types.
    Required.
    """

    metric: Optional[str] = None
    """
    The metric to use for the index. If not provided, the default metric for the model is used.
    Optional.
    """

    read_parameters: Optional[Dict[str, Any]] = None
    """
    The parameters to use when reading from the index.
    Optional.
    """

    write_parameters: Optional[Dict[str, Any]] = None
    """
    The parameters to use when writing to the index.
    Optional.
    """

    def as_dict(self):
        """
        Returns the IndexEmbed as a dictionary.
        """
        return self._asdict()
