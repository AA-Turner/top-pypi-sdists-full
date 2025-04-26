# Copyright 2022 StreamSets Inc.

# fmt: off
import traceback

import pytest

from streamsets.sdk.sch_models import KubernetesAgentEvent, KubernetesAgentEvents
from streamsets.sdk.utils import get_random_string

# fmt: on


@pytest.fixture(scope="module")
def sample_environment(sch):
    """A sample Kubernetes environment."""
    try:
        environment_builder = sch.get_environment_builder(environment_type='KUBERNETES')
        environment = environment_builder.build(
            environment_name='Sample K8s Environment {}'.format(get_random_string()),
            environment_type='KUBERNETES',
            environment_tags=['kubernetes-tag-{}'.format(get_random_string())],
            allow_nightly_engine_builds=True,
        )
        environment.kubernetes_namespace = 'streamsets test'
        sch.add_environment(environment)
        # The Kubernetes environment was successfully added to the SCH
        success = True

        sch.activate_environment(environment)

    except Exception as ex:
        success = False
        error_msg = (
            "Unexpected error while trying to create a 'sample_environment' Kubernetes environment : " "{}\n\n{}"
        ).format(ex, traceback.format_exc())

    if success:
        try:
            yield environment
        finally:
            sch.delete_environment(environment)
    else:
        raise AssertionError(error_msg)


def test__given_sample_environment_and_valid_environment_id__when_get_kubernetes_environment_agent_events_then_ok(
    sch, sample_environment
):
    # Given
    environment_id = sample_environment.environment_id

    # When
    # NOTICE that this test explicitly verifies that the SCH's API class implements the whole communication with the
    # Kubernetes environment to retrieve its events.
    events = sch.api_client.get_kubernetes_environment_agent_events(environment_id)

    # Then
    # Check that the response includes the environment events in a JSON body
    event_body = events.response.json()

    assert len(event_body["data"]) == 2
    assert event_body["data"][0]["details"] == "Activated agent token"
    assert event_body["data"][1]["details"] == "Waiting for Agent to connect..."


def test__given_sample_environment_and_kubernetes_agent_events_and_no_kwargs__when_get_all_results_from_api__then_ok(
    sch, sample_environment
):
    # Given
    kwargs = {}
    kubernetes_agent_events = KubernetesAgentEvents(sch, sample_environment.environment_id)

    # When
    # NOTICE that this test explicitly verifies that the events' collection (i.e., KubernetesAgentEvents) implements the
    # whole communication with the Kubernetes environment to retrieve its events.
    result = kubernetes_agent_events._get_all_results_from_api(**kwargs)

    # Then
    # Check that the response follows the expected format.
    assert len(result) == 4  # i.e., kwargs, class_kwargs, class_type, and results
    assert result.kwargs == {}
    assert result.class_kwargs == {}
    assert KubernetesAgentEvent.__name__ in str(result.class_type)

    # Check that the response from the API contains the two events any fresh-new Kubernetes Environment has got.
    # Notice that the API is paginated, and we have received a single page containing the two events.
    assert result.results["len"] == 2
    assert result.results["offset"] == 0
    assert result.results["totalCount"] == result.results["len"]
    assert len(result.results["data"]) == result.results["len"]
    assert result.results["data"][0]["details"] == "Activated agent token"
    assert result.results["data"][1]["details"] == "Waiting for Agent to connect..."


def test__given_sample_environment_and_no_kwargs__when_get_all_results_from_api__then_ok(sample_environment):
    # Given
    kwargs = {}

    # When
    # NOTICE that this test explicitly verifies that the events are an attribute of the environment
    result = sample_environment.agent_event_logs._get_all_results_from_api(**kwargs)

    # Then
    # Check that the response follows the expected format.
    assert len(result) == 4  # i.e., kwargs, class_kwargs, class_type, and results
    assert result.kwargs == {}
    assert result.class_kwargs == {}
    assert KubernetesAgentEvent.__name__ in str(result.class_type)

    # Check that the response from the API contains the two events any fresh-new Kubernetes Environment has got.
    # Notice that the API is paginated, and we have received a single page containing the two events.
    assert result.results["len"] == 2
    assert result.results["offset"] == 0
    assert result.results["totalCount"] == result.results["len"]
    assert len(result.results["data"]) == result.results["len"]
    assert result.results["data"][0]["details"] == "Activated agent token"
    assert result.results["data"][1]["details"] == "Waiting for Agent to connect..."
