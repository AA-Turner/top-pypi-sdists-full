import pytest
from rosdistro import Index, DistributionFile, FormatVersionError

def test_unsupported_index_version():
    data = {
        'type': 'index',
        'version': 99,  # Unsupported version
        'distributions': {}
    }
    with pytest.raises(FormatVersionError) as excinfo:
        Index(data, 'http://localhost')
    assert excinfo.value.file_type == 'index'
    assert excinfo.value.version == 99
    assert excinfo.value.supported_versions == [2, 3, 4]
    assert "Unable to handle 'index' format version '99'" in str(excinfo.value)

def test_unsupported_distribution_version():
    data = {
        'type': 'distribution',
        'version': 99,  # Unsupported version
        'repositories': {}
    }
    with pytest.raises(FormatVersionError) as excinfo:
        DistributionFile('foo', data)
    assert excinfo.value.file_type == 'distribution'
    assert excinfo.value.version == 99
    assert excinfo.value.supported_versions == [1, 2]
    assert excinfo.value.file_name == 'foo'
    assert "Unable to handle 'distribution' format version '99' for 'foo'" in str(excinfo.value)
