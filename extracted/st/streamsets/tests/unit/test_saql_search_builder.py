# Copyright 2023 StreamSets Inc.

# fmt: off
import pytest

from streamsets.sdk.sch_models import SAQLSearch, SAQLSearchBuilder

# fmt: on


@pytest.fixture(scope="function")
def saql_search_json():
    saql_search = {"id": None, "creator": None, "name": None, "createTime": None, "query": ''}
    return saql_search


def set_type_and_mode(saql_search_type, saql_mode_type, saql_search_json):
    saql_search_json['type'] = saql_search_type
    saql_search_json['mode'] = saql_mode_type


@pytest.mark.parametrize(
    'properties',
    (
        {'name': 1, 'operator': 'contains', 'value': '', 'condition': 'AND'},
        {'name': 'name', 'operator': 1, 'value': '', 'condition': 'AND'},
        {'name': 'name', 'operator': 'contains', 'value': 1, 'condition': 'AND'},
        {'name': 'name', 'operator': 'contains', 'value': '', 'condition': 1},
    ),
)
def test_add_filter_invalid_parameter_type(mocker, properties):
    mock_control_hub = mocker.Mock()
    saql_builder = SAQLSearchBuilder(mock_control_hub, SAQLSearch.PipelineType.PIPELINE, SAQLSearch.ModeType.BASIC)

    # Invalid parameter types raise TypeError
    with pytest.raises(TypeError):
        saql_builder.add_filter(
            property_name=properties['name'],
            property_operator=properties['operator'],
            property_value=properties['value'],
            property_condition_combiner=properties['condition'],
        )


def test_add_filter_invalid_mode_type(mocker, saql_search_json):
    mock_control_hub = mocker.Mock()
    set_type_and_mode(SAQLSearch.PipelineType.PIPELINE.value, SAQLSearch.ModeType.ADVANCED.value, saql_search_json)
    saql_builder = SAQLSearchBuilder(saql_search_json, mock_control_hub, SAQLSearch.ModeType.ADVANCED.value)

    assert not saql_builder.query

    # Invalid mode raises ValueError
    with pytest.raises(ValueError):
        saql_builder.add_filter()


def test_add_filter_invalid_property_operator(mocker, saql_search_json):
    mock_control_hub = mocker.Mock()
    set_type_and_mode(SAQLSearch.PipelineType.PIPELINE.value, SAQLSearch.ModeType.BASIC.value, saql_search_json)
    saql_builder = SAQLSearchBuilder(saql_search_json, mock_control_hub, SAQLSearch.ModeType.BASIC.value)

    # Invalid property operator raises ValueError
    with pytest.raises(ValueError):
        saql_builder.add_filter(property_operator='foo')


def test_add_filter_invalid_property_name(mocker, saql_search_json):
    mock_control_hub = mocker.Mock()
    set_type_and_mode(SAQLSearch.PipelineType.PIPELINE.value, SAQLSearch.ModeType.BASIC.value, saql_search_json)
    saql_builder = SAQLSearchBuilder(saql_search_json, mock_control_hub, SAQLSearch.ModeType.BASIC.value)

    # Invalid property name raises ValueError
    with pytest.raises(ValueError):
        saql_builder.add_filter(property_name='foo')


@pytest.mark.parametrize(
    'invalid_name_to_type',
    (
        {'name': 'failover', 'type': SAQLSearch.PipelineType.PIPELINE},
        {'name': 'failover', 'type': SAQLSearch.PipelineType.FRAGMENT},
        {'name': 'label', 'type': SAQLSearch.JobType.JOB_TEMPLATE},
        {'name': 'draft', 'type': SAQLSearch.JobType.JOB_INSTANCE},
        {'name': 'engine_label', 'type': SAQLSearch.JobType.JOB_DRAFT_RUN},
    ),
)
def test_add_filter_invalid_property_name_for_saql_type(mocker, saql_search_json, invalid_name_to_type):
    mock_control_hub = mocker.Mock()
    set_type_and_mode(invalid_name_to_type['type'].value, SAQLSearch.ModeType.BASIC.value, saql_search_json)
    saql_builder = SAQLSearchBuilder(saql_search_json, mock_control_hub, SAQLSearch.ModeType.BASIC.value)

    # Invalid operator to saql type raises ValueError
    with pytest.raises(ValueError):
        saql_builder.add_filter(property_name=invalid_name_to_type['name'])


@pytest.mark.parametrize(
    "saql_search_type, property_name, property_operator,property_value, property_condition_combiner",
    [
        (SAQLSearch.PipelineType.PIPELINE, 'name', 'contains', '', 'AND'),
        (SAQLSearch.PipelineType.FRAGMENT, 'name', 'contains', '', 'AND'),
        (SAQLSearch.JobType.JOB_TEMPLATE, 'name', 'contains', '', 'AND'),
        (SAQLSearch.JobType.JOB_INSTANCE, 'name', 'contains', '', 'AND'),
        (SAQLSearch.JobType.JOB_DRAFT_RUN, 'name', 'contains', '', 'AND'),
        (SAQLSearch.JobType.JOB_RUN, 'status', '==', '', 'AND'),
        (SAQLSearch.JobType.JOB_SEQUENCE, 'name', '==', '', 'AND'),
    ],
)
def test_add_filter_default_values(
    mocker,
    saql_search_json,
    saql_search_type,
    property_name,
    property_operator,
    property_value,
    property_condition_combiner,
):
    mock_control_hub = mocker.Mock()
    set_type_and_mode(saql_search_type.value, SAQLSearch.ModeType.BASIC.value, saql_search_json)
    saql_builder = SAQLSearchBuilder(saql_search_json, mock_control_hub, SAQLSearch.ModeType.BASIC.value)

    saql_builder.add_filter(
        property_name=property_name,
        property_operator=property_operator,
        property_value=property_value,
        property_condition_combiner=property_condition_combiner,
    )

    # Only one query should exist
    assert saql_builder.query[0].get('filter')['name'] == property_name
    assert saql_builder.query[0].get('operator') == property_operator
    assert saql_builder.query[0].get('value') == property_value
    assert saql_builder.query[0].get('conditionCombiner') == property_condition_combiner


def test_build_invalid_name_type(mocker, saql_search_json):
    mock_control_hub = mocker.Mock()
    set_type_and_mode(SAQLSearch.PipelineType.PIPELINE.value, SAQLSearch.ModeType.BASIC.value, saql_search_json)
    saql_builder = SAQLSearchBuilder(saql_search_json, mock_control_hub, SAQLSearch.ModeType.BASIC.value)

    # Invalid parameter types raise TypeError
    with pytest.raises(TypeError):
        saql_builder.build(name=1)


def test_build_empty_filter_basic_mode(mocker, saql_search_json):
    mock_control_hub = mocker.Mock()
    set_type_and_mode(SAQLSearch.PipelineType.PIPELINE.value, SAQLSearch.ModeType.BASIC.value, saql_search_json)
    saql_builder = SAQLSearchBuilder(saql_search_json, mock_control_hub, SAQLSearch.ModeType.BASIC.value)

    # Default values when running empty build() in basic mode
    property_name, property_operator = 'name', 'contains'
    property_value, property_condition_combiner = '', 'AND'
    saql_search_obj = saql_builder.build('foo')

    # Only one query should exist
    assert saql_builder.query[0].get('filter')['name'] == property_name
    assert saql_builder.query[0].get('operator') == property_operator
    assert saql_builder.query[0].get('value') == property_value
    assert saql_builder.query[0].get('conditionCombiner') == property_condition_combiner
    assert isinstance(saql_search_obj, SAQLSearch)  # Sanity check


def test_build_empty_filter_advanced_mode(mocker, saql_search_json):
    mock_control_hub = mocker.Mock()
    set_type_and_mode(SAQLSearch.PipelineType.PIPELINE.value, SAQLSearch.ModeType.ADVANCED.value, saql_search_json)
    saql_builder = SAQLSearchBuilder(saql_search_json, mock_control_hub, SAQLSearch.ModeType.ADVANCED.value)

    saql_search_obj = saql_builder.build('foo')
    assert isinstance(saql_search_obj, SAQLSearch)  # Sanity check
