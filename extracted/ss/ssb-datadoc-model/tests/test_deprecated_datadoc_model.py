"""These tests go against the original import path which is now deprecated
and should be removed in the next major release.

Potentially some of the tests can be retained and moved to other test modules
if they still provide value.
"""

import pytest
from pydantic import ValidationError

from datadoc_model.model import DatadocMetadata, MetadataContainer


def test_instantiate_no_values_container():
    container = MetadataContainer()
    assert isinstance(container, MetadataContainer)


def test_instantiate_no_values_datadoc():
    datadoc = DatadocMetadata()
    assert isinstance(datadoc, DatadocMetadata)


def test_unknown_field():
    with pytest.raises(ValidationError):
        DatadocMetadata(unknown_field="random_value")
