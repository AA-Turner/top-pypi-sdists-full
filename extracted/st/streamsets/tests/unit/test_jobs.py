#  IBM Confidential
#  PID 5900-BAF
#  Copyright StreamSets Inc., an IBM Company 2024

# fmt: off

from copy import deepcopy

import pytest

from streamsets.sdk.sch_models import Job

from .resources.jobs_data import DUMMY_JOB_JSON_1


# fmt: on
class MockControlHub:
    def __init__(self):
        self.organization = "12345"


@pytest.fixture(scope="function")
def dummy_job():
    json = deepcopy(DUMMY_JOB_JSON_1)
    return Job(json, MockControlHub())


def test_job_tag_supports_colons(dummy_job):
    tag_name = 'test:colon'
    dummy_job.add_tag(tag_name)
    assert [tag.tag for tag in dummy_job.tags] == [tag_name]
    dummy_job.remove_tag(tag_name)
    assert not dummy_job.tags
