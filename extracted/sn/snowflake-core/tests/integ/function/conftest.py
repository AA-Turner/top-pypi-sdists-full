from io import BytesIO
from textwrap import dedent

import pytest

from pydantic import StrictStr

from snowflake.core.service import (
    Service,
    ServiceSpecStageFile,
)

from ..utils import random_string


@pytest.fixture(scope="session")
def temp_service_for_function(services, session, imagerepo, shared_compute_pool) -> StrictStr:
    stage_name = random_string(5, "test_stage_ff_")
    s_name = random_string(5, "test_service_ff_")
    session.sql(f"create temp stage {stage_name};").collect()
    spec_file = "spec.yaml"
    spec = f"@{stage_name}/{spec_file}"
    session.file.put_stream(
        BytesIO(
            dedent(
                f"""
                spec:
                    containers:
                        - name: hello-world
                          image: {imagerepo}/hello-world:latest
                    endpoints:
                        - name: ep1
                          port: 8000
                        - name: end-point-2
                          port: 8010
                 """
            ).encode()
        ),
        spec,
    )

    test_s = Service(
        name=s_name,
        compute_pool=shared_compute_pool,
        spec=ServiceSpecStageFile(stage=stage_name, spec_file=spec_file),
        min_instances=1,
        max_instances=1,
        comment="created by temp_service for function",
    )
    s = services.create(test_s)
    try:
        yield s
    finally:
        session.sql(f"DROP SERVICE IF EXISTS {s.name}").collect()
