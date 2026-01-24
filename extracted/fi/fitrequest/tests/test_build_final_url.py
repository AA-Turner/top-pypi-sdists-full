import pytest
from pydantic_core import ValidationError

from fitrequest.errors import LIMIT_REQUEST_LINE, UrlRequestTooLongError
from fitrequest.method_config import MethodConfig


@pytest.mark.parametrize(
    ('base_url', 'endpoint'),
    [
        ('https://test.skillcorner', 'awesome_endpoint'),
        ('https://test.skillcorner', '/awesome_endpoint'),
        ('https://test.skillcorner/', 'awesome_endpoint'),
        ('https://test.skillcorner/', '/awesome_endpoint'),
    ],
)
def test_build_url_valid(base_url, endpoint):
    expected = 'https://test.skillcorner/awesome_endpoint/1/2'
    method_config = MethodConfig(
        name='url_test',
        base_url=base_url,
        endpoint=endpoint + '/{awesome_id}/{another_awesome_id}',
    )
    assert method_config.url(awesome_id=1, another_awesome_id=2) == expected


def test_build_url_invalid_type():
    with pytest.raises(ValidationError):
        MethodConfig(name='url_test', endpoint=123)


def test_final_request_url_length():
    MethodConfig(base_url='https://toto.com/', name='test', endpoint='/').url()
    name = 'test'
    endpoint = '/'
    base_url = 'https://toto.com/' + ('a' * LIMIT_REQUEST_LINE)

    with pytest.raises(UrlRequestTooLongError) as err:
        MethodConfig(base_url=base_url, name=name, endpoint=endpoint).url()

    url = f'{base_url}{endpoint}'
    assert err.value.url_size_limit == LIMIT_REQUEST_LINE
    assert err.value.url_size == len(url)
    assert err.value.url == url
