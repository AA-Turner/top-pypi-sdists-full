from typing import Union

from pydantic import Field, TypeAdapter
from typing_extensions import Annotated

from galileo_core.schemas.logging.session import Session
from galileo_core.schemas.logging.span import Span
from galileo_core.schemas.logging.trace import Trace

Step = Annotated[Union[Session, Trace, Span], Field(discriminator="type")]

StepAdapter: TypeAdapter[Step] = TypeAdapter(Step)
