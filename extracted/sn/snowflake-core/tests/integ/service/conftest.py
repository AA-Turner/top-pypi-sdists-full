from io import BytesIO
from textwrap import dedent

import pytest as pytest

from snowflake.core.service import ServiceSpecStageFile
from snowflake.core.stage import Stage

from ..utils import random_string


@pytest.fixture(scope="module")
def service_spec_file_on_stage(stages, imagerepo, session) -> ServiceSpecStageFile:
    stage_name = random_string(5, "test_stage_")
    stage = Stage(
        name=stage_name,
        comment="created by service_spec_file_on_stage",
    )
    temp_stage = stages.create(stage)
    try:

        spec_file = "spec.yaml"
        stage_file = f"@{temp_stage.name}"
        spec = f"{stage_file}/{spec_file}"
        session.file.put_stream(
            BytesIO(
                dedent(f"""
                        spec:
                          containers:
                          - name: hello-world
                            image: {imagerepo}/hello-world:latest
                        """).encode()
            ),
            spec,
        )

        yield ServiceSpecStageFile(stage=temp_stage.name, spec_file=spec_file)
    finally:
        temp_stage.drop()
