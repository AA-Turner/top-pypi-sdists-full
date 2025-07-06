"""General utilities for constructing models from CSV files"""

from pydantic import BaseModel, Field
from typing import Union, List, Type, Any
from typing_extensions import Annotated


def one_of_instance(instances: List[Type[BaseModel]], discriminator="name") -> Annotated[Union[Any], Field]:
    """
    Make an annotated union of class instances
    Parameters
    ----------
    instances : List[Type[BaseModel]]
      A list of class instances.
    discriminator : str
      Each model in instances should have a common field name where each item
      is unique to the model. This will allow pydantic to know which class
      should be deserialized. Default is 'name'.

    Returns
    -------
    Annotated[Union[Any], Field]
      An annotated field that can be used to define a type where a choice from a
      possible set of classes can be selected.

    """
    return Annotated[Union[tuple(type(i) for i in instances)], Field(discriminator=discriminator)]
