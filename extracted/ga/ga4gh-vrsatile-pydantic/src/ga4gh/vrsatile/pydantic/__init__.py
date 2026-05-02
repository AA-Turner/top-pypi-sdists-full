"""Initialize GA4GH VRSATILE Pydantic."""
import logging
from abc import ABC

from pydantic import BaseModel, model_validator, ConfigDict


logger = logging.getLogger("vrsatile-pydantic")


class BaseModelForbidExtra(BaseModel, ABC, extra="forbid"):
    """Base Pydantic model class with extra values forbidden."""

    model_config = ConfigDict(
        populate_by_name=True
    )


class BaseModelDeprecated(BaseModel, ABC):
    """Base Pydantic model class to use for deprecated classes."""

    @model_validator(mode="after")
    def log_deprecated_warning(cls, values):
        """Log warning that object class is deprecated."""
        if hasattr(cls, "_replace_with"):
            logger.warning(f"{cls.__name__} is deprecated. "
                           f"Use {cls._replace_with} instead.")
        else:
            logger.warning(f"{cls.__name__} is deprecated.")
        return values


def return_value(cls, v):
    """Return value from object.

    :param ModelMetaclass cls: Pydantic Model ModelMetaclass
    :param v: Model from vrs or vrsatile
    :return: Value
    """
    if v is not None:
        try:
            if isinstance(v, list):
                tmp = list()
                for item in v:
                    while True:
                        try:
                            item = item.root
                        except AttributeError:
                            break
                    tmp.append(item)
                v = tmp
            else:
                v = v.root
        except AttributeError:
            pass
    return v
