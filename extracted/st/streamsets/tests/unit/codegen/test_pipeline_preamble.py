#  IBM Confidential
#  PID 5900-BAF
#  Copyright StreamSets Inc., an IBM Company 2025
import textwrap

import pytest

from streamsets.sdk.codegen.preambles import PipelinePreamble
from streamsets.sdk.codegen.sources.source import PipelineDto


@pytest.fixture(scope="function")
def pipeline_dto_mock():
    return PipelineDto(
        pipeline_config={"info": {"sdcId": "926c0861-957e-4fe0-b48c-cb18067ab9d7"}},
        pipeline_rules={},
        library_definitions={},
    )


def test_if_pipeline_preamble_generate_correct_code(pipeline_dto_mock):
    preamble = PipelinePreamble(source_data=pipeline_dto_mock)
    assert str(preamble) == textwrap.dedent(
        """\
    import os
    from streamsets.sdk import ControlHub


    sch = ControlHub(
        os.getenv("SCH_CREDENTIAL_ID"),
        os.getenv("SCH_TOKEN")
    )

    engine = sch.engines.get(id="926c0861-957e-4fe0-b48c-cb18067ab9d7")
    pipeline_builder = sch.get_pipeline_builder(engine_type="COLLECTOR", engine_id=engine.id)"""
    )


def test_if_pipeline_preamble_with_aster_param_generate_correct_code(pipeline_dto_mock):
    preamble = PipelinePreamble(source_data=pipeline_dto_mock, aster_url="https://dev.hub.streamsets.com")
    assert str(preamble) == textwrap.dedent(
        """\
    import os
    from streamsets.sdk import ControlHub


    sch = ControlHub(
        os.getenv("SCH_CREDENTIAL_ID"),
        os.getenv("SCH_TOKEN"),
        aster_url="https://dev.hub.streamsets.com"
    )

    engine = sch.engines.get(id="926c0861-957e-4fe0-b48c-cb18067ab9d7")
    pipeline_builder = sch.get_pipeline_builder(engine_type="COLLECTOR", engine_id=engine.id)"""
    )
