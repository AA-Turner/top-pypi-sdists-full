from itertools import pairwise

import httpx
import pytest
import respx

from fitrequest.errors import InfinitePaginationError
from tests.demo_paginated import test_client


@respx.mock
def test_paginate_and_return_one_page(test_client):
    expected = [1, 2, 3]
    response = '1,2,3|'

    respx.get(
        'https://test.skillcorner.fr/items/',
    ).mock(return_value=httpx.Response(200, json=response))

    result = test_client.get_custom_str_items()
    assert result == expected


@respx.mock
def test_paginate_and_return_two_pages(test_client):
    expected = [1, 2, 3, 4, 5]

    # set pages urls and results + add last 'None' page
    pages = [
        {'url': 'https://test.skillcorner.fr/items/', 'results': ['1', '2', '3']},
        {'url': 'https://skillcorner.com/test?foo=bar&offset=3', 'results': ['4', '5']},
        {'url': ''},
    ]

    # mock all pages
    for page, next_page in pairwise(pages):
        response = ','.join(page['results']) + '|' + next_page['url']
        respx.get(page['url']).mock(return_value=httpx.Response(200, json=response))

    result = test_client.get_custom_str_items()
    assert result == expected


@respx.mock
def test_paginate_and_return_three_pages(test_client):
    expected = [1, 2, 3, 4, 5, 6, 12, 14]

    # set pages urls and results + add last 'None' page
    pages = [
        {'url': 'https://test.skillcorner.fr/items/', 'results': ['1', '2', '3']},
        {'url': 'https://skillcorner.com/test?foo=bar&offset=3', 'results': ['4', '5', '6']},
        {'url': 'https://skillcorner.com/test?foo=bar&offset=6', 'results': ['12', '14']},
        {'url': ''},
    ]

    # mock all pages
    for page, next_page in pairwise(pages):
        response = ','.join(page['results']) + '|' + next_page['url']
        respx.get(page['url']).mock(return_value=httpx.Response(200, json=response))

    result = test_client.get_custom_str_items()
    assert result == expected


@respx.mock
def test_infinite_pagination(test_client):
    # set pages urls and results + add last 'None' page
    pages = [
        {'url': 'https://test.skillcorner.fr/items/', 'results': ['1', '2', '3']},
        {'url': 'https://skillcorner.com/test?foo=bar&offset=3', 'results': ['4', '5', '6']},
        {'url': 'https://skillcorner.com/test?foo=bar&offset=6', 'results': ['12', '14']},
        {'url': 'https://skillcorner.com/test?foo=bar&offset=6', 'results': ['12', '14']},
    ]

    # mock all pages
    for page, next_page in pairwise(pages):
        response = ','.join(page['results']) + '|' + next_page['url']
        respx.get(page['url']).mock(return_value=httpx.Response(200, json=response))

    with pytest.raises(InfinitePaginationError) as exc_info:
        test_client.get_custom_str_items()

    assert exc_info.value.url_stack == [
        'https://skillcorner.com/test?foo=bar&offset=3',
        'https://skillcorner.com/test?foo=bar&offset=6',
        'https://skillcorner.com/test?foo=bar&offset=6',
    ]
