"""Pydantic classes used for Chalk's own SDK models.

Keep the existing v1 models through Python 3.14, which is supported by recent
Pydantic v1 releases and v2's bundled v1 compatibility package. Use native v2
models on Python 3.15 and newer.
"""

import sys
from typing import TYPE_CHECKING

__all__ = ["BaseModel", "Extra", "Field", "ValidationError", "root_validator", "validator", "USE_PYDANTIC_V2"]

# Select the SDK model implementation, independently of the installed Pydantic major.
USE_PYDANTIC_V2 = sys.version_info >= (3, 15)

if TYPE_CHECKING:
    from pydantic import BaseModel, Extra, Field, ValidationError, root_validator, validator
elif USE_PYDANTIC_V2:
    from pydantic import BaseModel as _BaseModel
    from pydantic import Extra, Field, ValidationError, root_validator, validator

    class BaseModel(_BaseModel):
        # V1 accepted numeric values for string fields, including resource requests.
        model_config = {"coerce_numbers_to_str": True, "protected_namespaces": ()}

else:
    try:
        from pydantic.v1 import BaseModel, Extra, Field, ValidationError, root_validator, validator
    except ImportError:
        from pydantic import BaseModel, Extra, Field, ValidationError, root_validator, validator
