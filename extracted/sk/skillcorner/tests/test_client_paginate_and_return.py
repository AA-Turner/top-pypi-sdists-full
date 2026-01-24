import httpx
import respx

from tests.fixtures import test_client  # noqa


@respx.mock
def test_paginate_and_return_one_page(test_client):
    expected = [1, 2, 3]
    response = {'results': [1, 2, 3], 'next': None}

    respx.get(
        'https://test.skillcorner.fr/items/',
    ).mock(return_value=httpx.Response(200, json=response))

    result = test_client.get_items()
    assert result == expected


@respx.mock
def test_paginate_and_return_two_pages(test_client):
    expected = [1, 2, 3, 4, 5]

    # set pages urls and results + add last 'None' page
    pages = [
        {'url': 'https://test.skillcorner.fr/items/', 'results': [1, 2, 3]},
        {'url': 'https://skillcorner.com/test?foo=bar&offset=3', 'results': [4, 5]},
        {'url': None},
    ]

    # mock all pages
    for page, next_page in zip(pages[0:-1], pages[1:], strict=False):
        response = {'results': page['results'], 'next': next_page['url']}
        respx.get(page['url']).mock(return_value=httpx.Response(200, json=response))

    result = test_client.get_items()
    assert result == expected


@respx.mock
def test_paginate_and_return_three_pages(test_client):
    expected = [1, 2, 3, 4, 5, 6, 12, 14]

    # set pages urls and results + add last 'None' page
    pages = [
        {'url': 'https://test.skillcorner.fr/items/', 'results': [1, 2, 3]},
        {'url': 'https://skillcorner.com/test?foo=bar&offset=3', 'results': [4, 5, 6]},
        {'url': 'https://skillcorner.com/test?foo=bar&offset=6', 'results': [12, 14]},
        {'url': None},
    ]

    # mock all pages
    for page, next_page in zip(pages[0:-1], pages[1:], strict=False):
        response = {'results': page['results'], 'next': next_page['url']}
        respx.get(page['url']).mock(return_value=httpx.Response(200, json=response))

    result = test_client.get_items()
    assert result == expected
