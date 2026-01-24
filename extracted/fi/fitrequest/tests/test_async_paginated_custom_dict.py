from itertools import pairwise

import httpx
import pytest
import respx

from fitrequest.errors import InfinitePaginationError
from tests.demo_paginated import test_client


@respx.mock
@pytest.mark.asyncio
async def test_paginate_and_return_one_page(test_client):
    expected = [1, 2, 3]
    response = {'data': [1, 2, 3], 'next_page': None}

    respx.get(
        'https://test.skillcorner.fr/items/',
    ).mock(return_value=httpx.Response(200, json=response))

    result = await test_client.async_get_custom_dict_items()
    assert result == expected


@respx.mock
@pytest.mark.asyncio
async def test_paginate_and_return_two_pages(test_client):
    expected = [1, 2, 3, 4, 5]

    # set pages urls and results + add last 'None' page
    pages = [
        {'url': 'https://test.skillcorner.fr/items/', 'data': [1, 2, 3]},
        {'url': 'https://skillcorner.com/test?foo=bar&offset=3', 'data': [4, 5]},
        {'url': None},
    ]

    # mock all pages
    for page, next_page in pairwise(pages):
        response = {'data': page['data'], 'next_page': next_page['url']}
        respx.get(page['url']).mock(return_value=httpx.Response(200, json=response))

    result = await test_client.async_get_custom_dict_items()
    assert result == expected


@respx.mock
@pytest.mark.asyncio
async def test_paginate_and_return_three_pages(test_client):
    expected = [1, 2, 3, 4, 5, 6, 12, 14]

    # set pages urls and results + add last 'None' page
    pages = [
        {'url': 'https://test.skillcorner.fr/items/', 'data': [1, 2, 3]},
        {'url': 'https://skillcorner.com/test?foo=bar&offset=3', 'data': [4, 5, 6]},
        {'url': 'https://skillcorner.com/test?foo=bar&offset=6', 'data': [12, 14]},
        {'url': None},
    ]

    # mock all pages
    for page, next_page in pairwise(pages):
        response = {'data': page['data'], 'next_page': next_page['url']}
        respx.get(page['url']).mock(return_value=httpx.Response(200, json=response))

    result = await test_client.async_get_custom_dict_items()
    assert result == expected


@respx.mock
@pytest.mark.asyncio
async def test_infinite_pagination(test_client):
    # set pages urls and results + add last 'None' page
    pages = [
        {'url': 'https://test.skillcorner.fr/items/', 'data': [1, 2, 3]},
        {'url': 'https://skillcorner.com/test?foo=bar&offset=3', 'data': [4, 5, 6]},
        {'url': 'https://skillcorner.com/test?foo=bar&offset=6', 'data': [12, 14]},
        {'url': 'https://skillcorner.com/test?foo=bar&offset=6', 'data': [12, 14]},
    ]

    # mock all pages
    for page, next_page in pairwise(pages):
        response = {'data': page['data'], 'next_page': next_page['url']}
        respx.get(page['url']).mock(return_value=httpx.Response(200, json=response))

    with pytest.raises(InfinitePaginationError) as exc_info:
        await test_client.async_get_custom_dict_items()

    assert exc_info.value.url_stack == [
        'https://skillcorner.com/test?foo=bar&offset=3',
        'https://skillcorner.com/test?foo=bar&offset=6',
        'https://skillcorner.com/test?foo=bar&offset=6',
    ]
