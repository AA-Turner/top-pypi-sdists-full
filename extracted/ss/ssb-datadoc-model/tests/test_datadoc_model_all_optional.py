import pytest
from pydantic import ValidationError

from datadoc_model.all_optional.model import (
    DatadocMetadata,
    MetadataContainer,
)


def test_instantiate_no_values_container():
    container = MetadataContainer()
    assert isinstance(container, MetadataContainer)


def test_instantiate_no_values_datadoc():
    datadoc = DatadocMetadata()
    assert isinstance(datadoc, DatadocMetadata)


def test_unknown_field():
    with pytest.raises(ValidationError):
        DatadocMetadata(unknown_field="random_value")
