
import pytest as pytest

from snowflake.core._common import CreateMode
from snowflake.core.exceptions import NotFoundError
from snowflake.core.procedure import (
    JavaScriptFunction,
    Procedure,
    ReturnDataType,
)
from tests.utils import random_string


@pytest.mark.min_sf_ver("8.38.0")
def test_drop(procedures):
    procedure_name = random_string(10, "test_create_procedure_")

    procedure = Procedure(
        name=procedure_name,
        arguments=[],
        return_type=ReturnDataType(datatype="REAL"),
        language_config=JavaScriptFunction(),
        body="""return 3.14"""
    )
    try:
        proc = procedures.create(procedure, mode=CreateMode.or_replace)
        assert proc.fetch().name == procedure_name.upper()
    finally:
        proc.drop()
        proc.drop(if_exists=True)

    with pytest.raises(NotFoundError):
        proc.fetch()
