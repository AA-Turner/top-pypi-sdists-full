#  IBM Confidential
#  PID 5900-BAF
#  Copyright StreamSets Inc., an IBM Company 2024

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
    return ['id', 'topology_name']


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


class HelperChild(Helper):
    def __init__(self, data, base_model_data, attributes_to_ignore, attributes_to_remap, repr_metadata):
        super().__init__(
            data=base_model_data,
            attributes_to_ignore=attributes_to_ignore,
            attributes_to_remap=attributes_to_remap,
            repr_metadata=repr_metadata,
        )
        self.return_value = json.dumps(data)
        self.data = data


class DirTester(BaseModel):
    def __init__(self, data, base_model_data, attributes_to_ignore, attributes_to_remap, repr_metadata):
        super().__init__(
            data=base_model_data,
            attributes_to_ignore=attributes_to_ignore,
            attributes_to_remap=attributes_to_remap,
            repr_metadata=repr_metadata,
        )
        self.data = data
        self.return_value = json.dumps(data)

    def func1(self):
        return self.data

    def func2(self):
        return self.return_value


class DirTester2:
    def __init__(self, data):
        self.data = data
        self.return_value = json.dumps(data)

    def func1(self):
        return self.data

    def func2(self):
        return self.return_value


def test_dir_functionality(base_model_data, attributes_to_ignore, attributes_to_remap, repr_metadata):
    base_model = BaseModel(
        data=base_model_data,
        attributes_to_ignore=attributes_to_ignore,
        attributes_to_remap=attributes_to_remap,
        repr_metadata=repr_metadata,
    )

    dir_tester = DirTester(
        data={"foo": "baz"},
        base_model_data=base_model_data,
        attributes_to_ignore=attributes_to_ignore,
        attributes_to_remap=attributes_to_remap,
        repr_metadata=repr_metadata,
    )

    dir_tester2 = DirTester2(data={"foo": "baz"})

    base_model_dir = dir(base_model)
    dir_tester_dir = dir(dir_tester)
    dir_tester2_dir = dir(dir_tester2)

    base_model_dir_len = len(base_model_dir)
    dir_tester_dir_len = len(dir_tester_dir)

    assert dir_tester_dir_len > base_model_dir_len
    assert dir_tester_dir_len == base_model_dir_len + 4
    assert set(dir_tester2_dir).issubset(set(dir_tester_dir))


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


@pytest.mark.xfail(reason="This test will fail until TLKT-1621 is resolved", strict=True)
def test_child_setattr(base_model_data, attributes_to_ignore, attributes_to_remap, repr_metadata):
    data = {"foo": "baz"}
    helper_child_obj = HelperChild(data, base_model_data, attributes_to_ignore, attributes_to_remap, repr_metadata)
    assert helper_child_obj.foo_property == data  # Sanity check

    # Reassign value so property setter runs json.dumps()
    helper_child_obj.foo_property = data

    # Expect property setter to get called which returns a json.dumps() of data
    assert helper_child_obj.foo_property == helper_child_obj.return_value


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


def test_copy_creates_new_instance(base_model_data, attributes_to_ignore, attributes_to_remap, repr_metadata):
    """Test that __copy__ creates a new instance with the same class."""
    base_model = BaseModel(
        data=base_model_data,
        attributes_to_ignore=attributes_to_ignore,
        attributes_to_remap=attributes_to_remap,
        repr_metadata=repr_metadata,
    )

    copied_model = copy(base_model)

    # Verify it's a new instance
    assert id(base_model) != id(copied_model)
    # Verify it's the same class
    assert type(base_model) == type(copied_model)
    assert base_model.__class__ == copied_model.__class__


def test_deepcopy_creates_new_instance(base_model_data, attributes_to_ignore, attributes_to_remap, repr_metadata):
    """Test that __deepcopy__ creates a new instance with the same class."""
    base_model = BaseModel(
        data=base_model_data,
        attributes_to_ignore=attributes_to_ignore,
        attributes_to_remap=attributes_to_remap,
        repr_metadata=repr_metadata,
    )

    deepcopied_model = deepcopy(base_model)

    # Verify it's a new instance
    assert id(base_model) != id(deepcopied_model)
    # Verify it's the same class
    assert type(base_model) == type(deepcopied_model)
    assert base_model.__class__ == deepcopied_model.__class__


def test_copy_preserves_dict_attributes(base_model_data, attributes_to_ignore, attributes_to_remap, repr_metadata):
    """Test that __copy__ preserves all __dict__ attributes."""
    base_model = BaseModel(
        data=base_model_data,
        attributes_to_ignore=attributes_to_ignore,
        attributes_to_remap=attributes_to_remap,
        repr_metadata=repr_metadata,
    )

    # Add custom attributes
    base_model.custom_string = "test"
    base_model.custom_number = 42
    base_model.custom_list = [1, 2, 3]

    copied_model = copy(base_model)

    # Verify all attributes are present
    assert copied_model.custom_string == "test"
    assert copied_model.custom_number == 42
    assert copied_model.custom_list == [1, 2, 3]

    # Verify shallow copy behavior - mutable objects are shared
    assert id(copied_model.custom_list) == id(base_model.custom_list)


def test_deepcopy_preserves_dict_attributes(base_model_data, attributes_to_ignore, attributes_to_remap, repr_metadata):
    """Test that __deepcopy__ preserves all __dict__ attributes with deep copies."""
    base_model = BaseModel(
        data=base_model_data,
        attributes_to_ignore=attributes_to_ignore,
        attributes_to_remap=attributes_to_remap,
        repr_metadata=repr_metadata,
    )

    # Add custom attributes
    base_model.custom_string = "test"
    base_model.custom_number = 42
    base_model.custom_list = [1, 2, 3]

    deepcopied_model = deepcopy(base_model)

    # Verify all attributes are present
    assert deepcopied_model.custom_string == "test"
    assert deepcopied_model.custom_number == 42
    assert deepcopied_model.custom_list == [1, 2, 3]

    # Verify deep copy behavior - mutable objects are independent
    assert id(deepcopied_model.custom_list) != id(base_model.custom_list)


def test_copy_with_load_data_method(base_model_data, attributes_to_ignore, attributes_to_remap, repr_metadata):
    """Test that __copy__ calls _load_data if it exists."""

    class ModelWithLoadData(BaseModel):
        def __init__(self, data, attributes_to_ignore=None, attributes_to_remap=None, repr_metadata=None):
            super().__init__(data, attributes_to_ignore, attributes_to_remap, repr_metadata)
            self.load_data_called = False

        def _load_data(self):
            self.load_data_called = True

    model = ModelWithLoadData(
        data=base_model_data,
        attributes_to_ignore=attributes_to_ignore,
        attributes_to_remap=attributes_to_remap,
        repr_metadata=repr_metadata,
    )

    assert model.load_data_called is False

    copied_model = copy(model)

    # Verify _load_data was called
    assert model.load_data_called is True
    assert copied_model.load_data_called is True


def test_deepcopy_with_load_data_method(base_model_data, attributes_to_ignore, attributes_to_remap, repr_metadata):
    """Test that __deepcopy__ calls _load_data if it exists."""

    class ModelWithLoadData(BaseModel):
        def __init__(self, data, attributes_to_ignore=None, attributes_to_remap=None, repr_metadata=None):
            super().__init__(data, attributes_to_ignore, attributes_to_remap, repr_metadata)
            self.load_data_called = False

        def _load_data(self):
            self.load_data_called = True

    model = ModelWithLoadData(
        data=base_model_data,
        attributes_to_ignore=attributes_to_ignore,
        attributes_to_remap=attributes_to_remap,
        repr_metadata=repr_metadata,
    )

    assert model.load_data_called is False

    deepcopied_model = deepcopy(model)

    # Verify _load_data was called
    assert model.load_data_called is True
    assert deepcopied_model.load_data_called is True


def test_copy_without_load_data_method(base_model_data, attributes_to_ignore, attributes_to_remap, repr_metadata):
    """Test that __copy__ works when _load_data doesn't exist."""
    base_model = BaseModel(
        data=base_model_data,
        attributes_to_ignore=attributes_to_ignore,
        attributes_to_remap=attributes_to_remap,
        repr_metadata=repr_metadata,
    )

    # Verify no _load_data method
    assert not hasattr(base_model, '_load_data')

    # Should not raise an error
    copied_model = copy(base_model)

    assert base_model == copied_model
    assert id(base_model) != id(copied_model)


def test_deepcopy_without_load_data_method(base_model_data, attributes_to_ignore, attributes_to_remap, repr_metadata):
    """Test that __deepcopy__ works when _load_data doesn't exist."""
    base_model = BaseModel(
        data=base_model_data,
        attributes_to_ignore=attributes_to_ignore,
        attributes_to_remap=attributes_to_remap,
        repr_metadata=repr_metadata,
    )

    # Verify no _load_data method
    assert not hasattr(base_model, '_load_data')

    # Should not raise an error
    deepcopied_model = deepcopy(base_model)

    assert base_model == deepcopied_model
    assert id(base_model) != id(deepcopied_model)
