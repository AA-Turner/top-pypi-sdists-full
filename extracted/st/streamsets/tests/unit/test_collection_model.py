#  IBM Confidential
#  PID 5900-BAF
#  Copyright StreamSets Inc., an IBM Company 2024

# fmt: off
import copy

import pytest

from streamsets.sdk.exceptions import ProjectAccessError
from streamsets.sdk.sch_models import (
    BaseModel, CollectionModel, CollectionModelResults, Connection, Connections, MutableKwargs, SeekableList,
)

from .resources.connections_data import CONNECTION_INTERNAL_JSON

# fmt: on


class ErroneousCollectionModel(CollectionModel):
    """
    A subclass of CollectionModel that does not implement the _get_all_results_from_api function
    """

    pass


class ValidCollectionModel(CollectionModel):
    """
    A subclass of CollectionModel that implements _get_all_results_from_api function
    """

    def __init__(self, control_hub):
        super().__init__(control_hub)
        self.data = [{'id': i} for i in range(100)]
        self.page_size = None

    def _get_all_results_from_api(self, **kwargs):
        kwargs_defaults = {'offset': None, 'len': None}
        kwargs_instance = MutableKwargs(kwargs_defaults, kwargs)
        kwargs_unioned = kwargs_instance.union()

        response = {
            'data': self.data[kwargs_unioned['offset'] : kwargs_unioned['offset'] + kwargs_unioned['len']],
            'offset': kwargs_unioned['offset'] + kwargs_unioned['len'],
            'len': kwargs_unioned['len'],
            'totalCount': len(self.data),
        }

        self.page_size = kwargs_unioned['len']
        kwargs_unused = kwargs_instance.subtract()

        return CollectionModelResults(response, kwargs_unused, BaseModel, {})

    def __len__(self):
        return len(self.data)


class DecreasingLengthCollectionModel(CollectionModel):
    """
    This class is used to test a collection model whose length decreases a lot suddenly

    What we want to test specifically:
    1. Initially we have 150 items
    2. user makes a call to get all items
    3. Since collection model gets minimum of (50, requested_length) we should get 50 items in the initial response
    4. We set the total number of items we have to a total of 50 (deleting 100 items)
    5. We raise an exception if offset is negative in _get_all_results_from_api and if no error is thrown we good.

    If repeated number of calls are made then we only have 50 data points to deal with
    """

    def __init__(self, control_hub):
        super().__init__(control_hub)
        self.data = [{'id': i} for i in range(150)]

    def _get_all_results_from_api(self, **kwargs):
        kwargs_defaults = {'offset': None, 'len': None}
        kwargs_instance = MutableKwargs(kwargs_defaults, kwargs)
        kwargs_unioned = kwargs_instance.union()

        if kwargs_unioned['offset'] < 0:
            raise ValueError("Got negative offset in _get_all_results_from_api")

        response = {
            'data': self.data[kwargs_unioned['offset'] : kwargs_unioned['offset'] + kwargs_unioned['len']],
            'offset': kwargs_unioned['offset'] + kwargs_unioned['len'],
            'len': 0,
            'totalCount': len(self.data),
        }  # len isn't used but is checked for
        kwargs_unused = kwargs_instance.subtract()

        # setting the length of items to 50, we do -50 because we have already seen the first few
        self.data = self.data[-50:]

        return CollectionModelResults(response, kwargs_unused, BaseModel, {})

    def __len__(self):
        return len(self.data)


class ProjectErrorConnectionCollectionModel(Connections):
    def _get_all_results_from_api(self, **kwargs):
        raise ProjectAccessError(code='RESTAPI_08', message='User does not have access to resource.')


def test_not_implemented_error(mocker):
    invalid_collection_model = ErroneousCollectionModel(mocker.Mock())
    with pytest.raises(NotImplementedError):
        invalid_collection_model._get_all_results_from_api()


def test_invalid_offset(mocker):
    valid_collection_model = ValidCollectionModel(mocker.Mock())
    with pytest.raises(ValueError):
        next(valid_collection_model._paginate(offset=-1))  # _paginate is a generator


@pytest.mark.parametrize("offset", [0, 10])
def test_valid_offset(mocker, offset):
    valid_collection_model = ValidCollectionModel(mocker.Mock())

    res = valid_collection_model._paginate(offset=offset)
    res = list(res)

    expected_result_length = len(valid_collection_model.data) - offset
    assert len(res) == expected_result_length


def test_valid_page_size_is_250(mocker):
    valid_collection_model = ValidCollectionModel(mocker.Mock())
    list(valid_collection_model._paginate())
    assert valid_collection_model.page_size == CollectionModel.PAGE_LENGTH


def test_decreasing_length_collection_model(mocker):
    decreasing_collection_model = DecreasingLengthCollectionModel(mocker.Mock())
    res = decreasing_collection_model._paginate(offset=0, len=75)  # we want more items than the page length

    assert len(list(res)) == 75


def test_contains_returns_false_with_project_access_error(mocker):
    error_collection_model = ProjectErrorConnectionCollectionModel(mocker.Mock(), organization='')
    connection = Connection(connection=copy.deepcopy(CONNECTION_INTERNAL_JSON), control_hub=mocker.Mock())

    assert connection not in error_collection_model


@pytest.mark.parametrize(
    'filter_parameters, expected_result',
    [
        ({}, {'totalCount': 100, 'offset': 0, 'len': -1}),
        ({'len': 10}, {'totalCount': 10, 'offset': 0, 'len': 10}),
        ({'offset': 30}, {'totalCount': 70, 'offset': 30, 'len': -1}),
        ({'offset': 95, "len": 10}, {'totalCount': 5, 'offset': 95, 'len': 10}),
    ],
)
def test_get_all_method_with_wrapper(mocker, filter_parameters, expected_result):
    valid_collection_model = ValidCollectionModel(mocker.Mock())
    wrapped_result = valid_collection_model.get_all(with_wrapper=True, **filter_parameters)
    data = wrapped_result.pop('data')
    assert isinstance(data, SeekableList)
    assert expected_result == wrapped_result


@pytest.mark.parametrize(
    'filter_parameters, expected_result',
    [
        ({}, 100),
        ({'len': 10}, 10),
        ({'offset': 95, "len": 10}, 5),
    ],
)
def test_get_all_method_without_wrapper(mocker, filter_parameters, expected_result):
    valid_collection_model = ValidCollectionModel(mocker.Mock())
    data = valid_collection_model.get_all(**filter_parameters)
    assert isinstance(data, SeekableList)
    assert len(data) == expected_result
