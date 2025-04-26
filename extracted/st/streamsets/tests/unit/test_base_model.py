# Copyright 2023 StreamSets Inc.

# fmt: off
import json
from copy import copy, deepcopy

import pytest

from streamsets.sdk.sch_models import BaseModel

from .resources.base_model_data import BASE_MODEL_JSON

# fmt: on


@pytest.fixture(scope="function")
def base_model_data():
    data = deepcopy(BASE_MODEL_JSON)
    return data


@pytest.fixture(scope="module")
def attributes_to_ignore():
    return ['provenanceMetaData']


@pytest.fixture(scope="module")
def attributes_to_remap():
    # Mapping is {"new_attribute": "original_attribute"}
    return {'committed_by': 'committer', 'topology_name': 'name'}


@pytest.fixture(scope="module")
def repr_metadata():
    return ['topology_id', 'topology_name']


class Helper(BaseModel):
    def __init__(self, data, base_model_data, attributes_to_ignore, attributes_to_remap, repr_metadata):
        super().__init__(
            data=base_model_data,
            attributes_to_ignore=attributes_to_ignore,
            attributes_to_remap=attributes_to_remap,
            repr_metadata=repr_metadata,
        )
        self.return_value = json.dumps(data)
        self.data = data

    @property
    def foo_property(self):
        return self.data

    @foo_property.setter
    def foo_property(self, data):
        self.data = json.dumps(data)


def test_data_ingest_sanity(base_model_data, attributes_to_ignore, attributes_to_remap, repr_metadata):
    base_model = BaseModel(
        data=base_model_data,
        attributes_to_ignore=attributes_to_ignore,
        attributes_to_remap=attributes_to_remap,
        repr_metadata=repr_metadata,
    )

    assert base_model._data_internal is base_model_data
    assert base_model._attributes_to_ignore is attributes_to_ignore
    assert base_model._attributes_to_remap is attributes_to_remap
    assert base_model._repr_metadata is repr_metadata


def test_getattr_name_in_attributes_to_remap(base_model_data, attributes_to_ignore, attributes_to_remap, repr_metadata):
    base_model = BaseModel(
        data=base_model_data,
        attributes_to_ignore=attributes_to_ignore,
        attributes_to_remap=attributes_to_remap,
        repr_metadata=repr_metadata,
    )

    assert base_model.committed_by == base_model_data['committer']
    assert base_model.topology_name == base_model_data['name']


def test_getattr_python_to_json_attribute(base_model_data, attributes_to_ignore, attributes_to_remap, repr_metadata):
    base_model = BaseModel(
        data=base_model_data,
        attributes_to_ignore=attributes_to_ignore,
        attributes_to_remap=attributes_to_remap,
        repr_metadata=repr_metadata,
    )
    assert base_model.topologyDefinition == base_model_data['topologyDefinition']
    assert base_model.topology_definition == base_model_data['topologyDefinition']


def test_setattr_python_to_json_attribute(base_model_data, attributes_to_ignore, attributes_to_remap, repr_metadata):
    data = {"foo": "baz"}
    helper_obj = Helper(data, base_model_data, attributes_to_ignore, attributes_to_remap, repr_metadata)
    assert helper_obj.foo_property == data  # Sanity check

    # Reassign value so property setter runs json.dumps()
    helper_obj.foo_property = data

    # Expect property setter to get called which returns a json.dumps() of data
    assert helper_obj.foo_property == helper_obj.return_value


def test_attributes_to_ignore_in_base_model(base_model_data, attributes_to_ignore, attributes_to_remap, repr_metadata):
    data = {"foo": "baz"}
    helper_obj = Helper(data, base_model_data, attributes_to_ignore, attributes_to_remap, repr_metadata)
    assert helper_obj._data["provenanceMetaData"] == base_model_data["provenanceMetaData"]  # Sanity check

    # Check if only the specified attribute is ignored
    assert hasattr(helper_obj, "topologyId")
    assert not hasattr(helper_obj, "provenanceMetaData")


def test_override_equal(base_model_data, attributes_to_ignore, attributes_to_remap, repr_metadata):
    base_model = BaseModel(
        data=base_model_data,
        attributes_to_ignore=attributes_to_ignore,
        attributes_to_remap=attributes_to_remap,
        repr_metadata=repr_metadata,
    )
    copy_base_model = BaseModel(
        data=base_model_data,
        attributes_to_ignore=attributes_to_ignore,
        attributes_to_remap=attributes_to_remap,
        repr_metadata=repr_metadata,
    )

    assert base_model == copy_base_model


def test_copying_base_model(base_model_data, attributes_to_ignore, attributes_to_remap, repr_metadata):
    # create a base model that has another base model object as an attribute
    base_model = BaseModel(
        data=base_model_data,
        attributes_to_ignore=attributes_to_ignore,
        attributes_to_remap=attributes_to_remap,
        repr_metadata=repr_metadata,
    )
    sub_base_model = BaseModel(
        data=base_model_data,
        attributes_to_ignore=attributes_to_ignore,
        attributes_to_remap=attributes_to_remap,
        repr_metadata=repr_metadata,
    )
    base_model.sub_base_model = sub_base_model

    # copy to ensure base models are equal but not the same, sub_base_model should be equal and same
    copy_base_model = copy(base_model)
    assert base_model == copy_base_model
    assert id(base_model) != id(copy_base_model)
    assert base_model.sub_base_model == copy_base_model.sub_base_model
    assert id(base_model.sub_base_model) == id(copy_base_model.sub_base_model)


def test_deep_copying_base_model(base_model_data, attributes_to_ignore, attributes_to_remap, repr_metadata):
    # create a base model that has another base model object as an attribute
    base_model = BaseModel(
        data=base_model_data,
        attributes_to_ignore=attributes_to_ignore,
        attributes_to_remap=attributes_to_remap,
        repr_metadata=repr_metadata,
    )
    sub_base_model = BaseModel(
        data=base_model_data,
        attributes_to_ignore=attributes_to_ignore,
        attributes_to_remap=attributes_to_remap,
        repr_metadata=repr_metadata,
    )
    base_model.sub_base_model = sub_base_model

    # deepcopy to ensure both base_model and sub_base_model are equal to deepcopy, but their ids shouldn't be
    deepcopy_base_model = deepcopy(base_model)
    assert base_model == deepcopy_base_model
    assert id(base_model) != id(deepcopy_base_model)
    assert base_model.sub_base_model == deepcopy_base_model.sub_base_model
    assert id(base_model.sub_base_model) != id(deepcopy_base_model.sub_base_model)
