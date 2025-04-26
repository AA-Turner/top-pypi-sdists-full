#
# Copyright (c) 2012-2023 Snowflake Computing Inc. All rights reserved.
#
from io import BytesIO
from textwrap import dedent

import pytest

from snowflake.core.exceptions import NotFoundError
from snowflake.core.service import Service, ServiceSpecStageFile
from tests.utils import random_string


def test_drop(services, session, imagerepo, shared_compute_pool):
    try:
        service_name = random_string(5, "test_service_")
        stage_name = random_string(5, "test_stage_")

        session.sql(f"create temp stage {stage_name};").collect()
        spec_file = "spec.yaml"
        stage_file = f"@{stage_name}"
        spec = f"{stage_file}/{spec_file}"
        session.file.put_stream(
            BytesIO(
                dedent(f"""\
                    spec:
                      containers:
                      - name: hello-world
                        image: {imagerepo}/hello-world:latest
                """).encode()
            ),
            spec,
        )
        test_service = Service(
            name=service_name,
            compute_pool=shared_compute_pool,
            spec=ServiceSpecStageFile(stage=stage_name, spec_file=spec_file),
            min_instances=1,
            max_instances=1,
        )
        s = services.create(test_service)
        s.drop()
        with pytest.raises(
            NotFoundError,
        ):
            # TODO: HTTP response body: {"description": "list index out of range", "error_details": null}
            #  Looks wrong
            s.fetch()

        s = services.create(test_service)
        s.drop()
    finally:
        services[service_name].drop(if_exists=True)
