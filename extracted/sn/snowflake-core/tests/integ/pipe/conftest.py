import pytest

from snowflake.core.pipe import Pipe
from tests.utils import random_string


@pytest.fixture
def template_pipe(temp_table, temp_stage):
    name = random_string(5, "test_create_pipe_")
    return Pipe(
        name=name,
        comment="template for pipe snowpy testing",
        # TODO(SNOW-1650785): add more attributes when they are implemented in python api
        # auto_ingest=True,
        # error_integration="dummy_error_intergration",
        # aws_sns_topic="arn:aws:sns:us-west-2:001234567890:s3_mybucket",
        # integration="dummy_integration",
        copy_statement=f"COPY into {temp_table.name} from @{temp_stage.name}",
    )


@pytest.fixture
def template_pipe_case_sensitive(temp_table, temp_stage):
    name = random_string(5, "test_create_pipe_")
    name_case_sensitive = '"' + name + '"'
    return Pipe(
        name=name_case_sensitive,
        comment="template for pipe snowpy testing",
        # TODO(SNOW-1650785): add more attributes when they are implemented in python api
        # auto_ingest=True,
        # error_integration="dummy_error_intergration",
        # aws_sns_topic="arn:aws:sns:us-west-2:001234567890:s3_mybucket",
        # integration="dummy_integration",
        copy_statement=f"COPY into {temp_table.name} from @{temp_stage.name}",
    )
