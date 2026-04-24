#  IBM Confidential
#  PID 5900-BAF
#  Copyright StreamSets Inc., an IBM Company 2025

# fmt: off
import pytest
from tests.unit.resources.job import job_data

from streamsets.sdk.exceptions import UnpublishedError
from streamsets.sdk.sch_models import JobBuilder

# fmt: on


class MockControlHub:
    def __init__(self):
        self.organization = "12345"


class DummyPipeline:
    def __init__(self):
        self.id = None


@pytest.fixture(scope="function")
def dummy_pipeline():
    return DummyPipeline()


def test_job_builder_build_unpublished_pipeline(dummy_pipeline):
    sch = MockControlHub()

    job_builder = JobBuilder(job=job_data, control_hub=sch)
    with pytest.raises(UnpublishedError):
        job_builder.build('some job name', dummy_pipeline)
