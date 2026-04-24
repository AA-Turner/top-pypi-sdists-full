#  IBM Confidential
#  PID 5900-BAF
#  Copyright StreamSets Inc., an IBM Company 2025

# fmt: off
import pytest

from streamsets.sdk.utils import get_random_string

# fmt: on

TEST_PAGE_SIZE = 5
LEXICOGRAPHICALLY_FIRST = 'A'
LEXICOGRAPHICALLY_LAST = 'Z'
PIPELINE_LABEL = f'test_pagination_pipeline_label_{get_random_string()}'


@pytest.fixture(scope='function')
def sample_pipelines_with_same_name(sch, sch_authoring_sdc_id):
    pipelines = []

    for _ in range(TEST_PAGE_SIZE * 2):
        builder = sch.get_pipeline_builder(engine_type='data_collector', engine_id=sch_authoring_sdc_id)
        pipeline = builder.build(LEXICOGRAPHICALLY_LAST)
        pipeline.add_label(PIPELINE_LABEL)
        sch.publish_pipeline(pipeline)
        pipelines.append(pipeline)

    try:
        yield pipelines
    finally:
        for p in pipelines:
            sch.delete_pipeline(p)


@pytest.fixture(scope='function')
def lexicographically_first_pipeline(sch, sch_authoring_sdc_id):
    builder = sch.get_pipeline_builder(engine_type='data_collector', engine_id=sch_authoring_sdc_id)
    pipeline = builder.build(LEXICOGRAPHICALLY_FIRST)
    pipeline.add_label(PIPELINE_LABEL)

    try:
        yield pipeline
    finally:
        sch.delete_pipeline(pipeline)


def test_new_pipeline_created_during_iteration(sch, sample_pipelines_with_same_name, lexicographically_first_pipeline):
    result_ids = list()
    expected_pipeline_amount = len(sample_pipelines_with_same_name) + 1
    no_of_batches = expected_pipeline_amount // TEST_PAGE_SIZE
    remaining_pipelines = expected_pipeline_amount % TEST_PAGE_SIZE
    # make sure to fetch exact amount of created pipelines
    num_pages = [TEST_PAGE_SIZE] * no_of_batches + [remaining_pipelines]

    assert len(sch.pipelines.get_all(label=PIPELINE_LABEL)) == len(sample_pipelines_with_same_name)

    # workaround to make pagination PAGE_SIZE smaller
    for batch_no in range(no_of_batches + 1):
        current_batch_page_len = num_pages[batch_no]
        batch = sch.pipelines._paginate(
            offset=batch_no * TEST_PAGE_SIZE, len=current_batch_page_len, label=PIPELINE_LABEL
        )

        for item in batch:
            result_ids.append(item.id)

        # simulate pipelines collection update during iteration
        if batch_no == 0:
            sch.publish_pipeline(lexicographically_first_pipeline)

    assert len(result_ids) == expected_pipeline_amount
    filtered_pipelines = sch.pipelines.get_all(label=PIPELINE_LABEL)
    last_pipeline = filtered_pipelines[-1]
    assert last_pipeline.id == lexicographically_first_pipeline.id
    assert last_pipeline.name == lexicographically_first_pipeline.name
