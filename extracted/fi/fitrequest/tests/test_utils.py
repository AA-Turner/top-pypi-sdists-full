from collections.abc import Iterable

import jinja2
import pytest
from pydantic import BaseModel

from fitrequest.templating import KeepPlaceholderUndefined
from fitrequest.utils import extract_method_params, format_url, is_basemodel_subclass, string_varnames


def test_extract_method_params():
    def hello(name: str, team: str) -> str:
        return f'Hello! My name is {name}, and I work on the {team} team.'

    assert extract_method_params(hello, {'name': 'lucien', 'team': 'dev', 'age': 33}) == {
        'name': 'lucien',
        'team': 'dev',
    }
    assert extract_method_params(hello, {'name': 'lucien', 'age': 33}) == {'name': 'lucien'}


def test_string_varnames():
    jinja_env = jinja2.Environment(
        variable_start_string='{',
        variable_end_string='}',
        autoescape=True,  # ruff S701
        undefined=KeepPlaceholderUndefined,
    )

    assert string_varnames(jinja_env, 'Hello {name}, do you have the {amount} € you owe me ?') == ['name', 'amount']
    assert string_varnames(jinja_env, 'Hey, No') == []

    with pytest.raises(jinja2.exceptions.TemplateSyntaxError):
        string_varnames(jinja_env, 'Late fees are going up by {}%.')


def test_format_url():
    assert format_url('https://toto.com///index.html') == 'https://toto.com/index.html'
    assert format_url('https://toto.com//index.html') == 'https://toto.com/index.html'
    assert format_url('https://toto.com/index.html') == 'https://toto.com/index.html'
    assert format_url('https://toto.com') == 'https://toto.com'


def test_is_basemodel_subclass():
    class Person(BaseModel):
        name: str
        age: int

    assert is_basemodel_subclass(BaseModel)
    assert is_basemodel_subclass(Person)
    assert not is_basemodel_subclass(BaseModel | None)
    assert not is_basemodel_subclass(Person | str | int | None)
    assert not is_basemodel_subclass(Iterable[BaseModel])
    assert not is_basemodel_subclass(Iterable[Person])
    assert not is_basemodel_subclass(list[BaseModel])
    assert not is_basemodel_subclass(set[Person])
    assert not is_basemodel_subclass(int)
    assert not is_basemodel_subclass(str)
