import os
import pytest
from dataengine import assets

DIRNAME = os.path.dirname(os.path.realpath(__file__))

# Mock BaseDataset Inputs
@pytest.fixture
def valid_base_dataset_data():
    return {
        "asset_name": "MyAsset",
        "dirname": DIRNAME,
        "description": "This is a test dataset.",
        "file_path": "data/file.csv",
        "file_format": "csv",
        "separator": ",",
        "location": "local",
        "header": True,
        "schema": {"name": "string", "age": "int"}}


def test_deserialize_base_dataset(valid_base_dataset_data):
    schema = assets.BaseDatasetSchema()
    result = schema.load(valid_base_dataset_data)
    assert isinstance(result, assets.BaseDataset)
    assert result.asset_name == "MyAsset"
    assert result.description == "This is a test dataset."
    assert result.file_path_list == [os.path.join(DIRNAME, "data/file.csv")]


def test_deserialize_base_dataset_with_invalid_file_format(valid_base_dataset_data):
    invalid_data = valid_base_dataset_data.copy()
    invalid_data['file_format'] = 'unsupported_format'
    schema = assets.BaseDatasetSchema()
    with pytest.raises(assets.ValidationError) as excinfo:
        schema.load(invalid_data)
    assert "Invalid file_format" in str(excinfo.value)

def test_base_dataset_instantiation_via_schema(valid_base_dataset_data):
    # Instantiate your schema
    schema = assets.BaseDatasetSchema()
    # Deserialize the input data, which should invoke post_load to create a BaseDataset instance
    result = schema.load(valid_base_dataset_data)
    # Assertions to verify the BaseDataset instance is correctly instantiated
    assert isinstance(result, assets.BaseDataset), "Resulting object is not an instance of BaseDataset"
    assert result.asset_name == valid_base_dataset_data["asset_name"], "Asset name was not set correctly"
    assert result.file_path_list == [
        os.path.join(DIRNAME, valid_base_dataset_data["file_path"])
    ], "File paths were not set correctly"
    assert result.file_format == valid_base_dataset_data["file_format"], "File format was not set correctly"
    assert result.separator == valid_base_dataset_data["separator"], "Separator was not set correctly"
    assert result.location == valid_base_dataset_data["location"], "Location was not set correctly"
    assert result.header == valid_base_dataset_data["header"], "Header flag was not set correctly"
    assert result.schema == valid_base_dataset_data["schema"], "Schema was not set correctly"
