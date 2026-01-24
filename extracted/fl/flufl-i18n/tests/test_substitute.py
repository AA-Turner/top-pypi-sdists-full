from types import SimpleNamespace

import pytest

from flufl.i18n._substitute import attrdict


def test_attrdict_parts():
    ant = dict(bee=SimpleNamespace(cat=SimpleNamespace(dog='elk')))
    anteater = attrdict(ant)
    assert anteater['bee.cat.dog'] == 'elk'


def test_attrdict_missing():
    ant = dict(bee=SimpleNamespace(cat=SimpleNamespace(dog='elk')))
    anteater = attrdict(ant)
    with pytest.raises(KeyError) as exc_info:
        anteater['bee.cat.doo']
    assert str(exc_info.value) == "'bee.cat.doo'"
