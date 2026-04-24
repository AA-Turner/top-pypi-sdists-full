#  IBM Confidential
#  PID 5900-BAF
#  Copyright StreamSets Inc., an IBM Company 2024

import pytest

from streamsets.sdk.utils import EngineType


@pytest.mark.parametrize('engine_type', [engine_type for engine_type in EngineType])
def test_engine_type_bool(engine_type):
    if engine_type.name != 'NULL':
        assert bool(engine_type)
    else:
        assert not bool(engine_type)


@pytest.mark.parametrize('engine_type', [engine_type for engine_type in EngineType])
def test_engine_type_equality(engine_type):
    assert engine_type == engine_type.value


@pytest.mark.parametrize('engine_type', [engine_type for engine_type in EngineType])
def test_engine_type_str(engine_type):
    r = engine_type.value if engine_type.value else ''
    assert str(engine_type) == r


@pytest.mark.parametrize('engine_type', [engine_type for engine_type in EngineType])
def test_engine_type_hash(engine_type):
    a = {engine_type: 'bar'}
    assert a[engine_type] == a[engine_type.value]
