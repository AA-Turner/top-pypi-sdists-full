from itertools import pairwise

import httpx
import pytest
import respx

from fitrequest.errors import InfinitePaginationError
from tests.demo_paginated import CustomObject, test_client


@respx.mock
@pytest.mark.asyncio
async def test_paginate_and_return_one_page(test_client):
    expected = [CustomObject(oid=1, name='one'), CustomObject(oid=2, name='two'), CustomObject(oid=3, name='three')]
    response = {
        'results': [{'oid': 1, 'name': 'one'}, {'oid': 2, 'name': 'two'}, {'oid': 3, 'name': 'three'}],
        'next': None,
    }

    respx.get(
        'https://test.skillcorner.fr/items/',
    ).mock(return_value=httpx.Response(200, json=response))

    result = await test_client.async_get_items_model()
    assert result == expected


@respx.mock
@pytest.mark.asyncio
async def test_paginate_and_return_two_pages(test_client):
    expected = [
        CustomObject(oid=1, name='one'),
        CustomObject(oid=2, name='two'),
        CustomObject(oid=3, name='three'),
        CustomObject(oid=4, name='for'),
        CustomObject(oid=5, name='five'),
    ]

    # set pages urls and results + add last 'None' page
    pages = [
        {
            'url': 'https://test.skillcorner.fr/items/',
            'results': [{'oid': 1, 'name': 'one'}, {'oid': 2, 'name': 'two'}, {'oid': 3, 'name': 'three'}],
        },
        {
            'url': 'https://skillcorner.com/test?foo=bar&offset=3',
            'results': [{'oid': 4, 'name': 'for'}, {'oid': 5, 'name': 'five'}],
        },
        {'url': None},
    ]

    # mock all pages
    for page, next_page in pairwise(pages):
        response = {'results': page['results'], 'next': next_page['url']}
        respx.get(page['url']).mock(return_value=httpx.Response(200, json=response))

    result = await test_client.async_get_items_model()
    assert result == expected


@respx.mock
@pytest.mark.asyncio
async def test_paginate_and_return_three_pages(test_client):
    expected = [
        CustomObject(oid=1, name='one'),
        CustomObject(oid=2, name='two'),
        CustomObject(oid=3, name='three'),
        CustomObject(oid=4, name='for'),
        CustomObject(oid=5, name='five'),
        CustomObject(oid=6, name='six'),
        CustomObject(oid=12, name='twelve'),
        CustomObject(oid=14, name='fourteen'),
    ]

    # set pages urls and results + add last 'None' page
    pages = [
        {
            'url': 'https://test.skillcorner.fr/items/',
            'results': [{'oid': 1, 'name': 'one'}, {'oid': 2, 'name': 'two'}, {'oid': 3, 'name': 'three'}],
        },
        {
            'url': 'https://skillcorner.com/test?foo=bar&offset=3',
            'results': [{'oid': 4, 'name': 'for'}, {'oid': 5, 'name': 'five'}, {'oid': 6, 'name': 'six'}],
        },
        {
            'url': 'https://skillcorner.com/test?foo=bar&offset=6',
            'results': [{'oid': 12, 'name': 'twelve'}, {'oid': 14, 'name': 'fourteen'}],
        },
        {'url': None},
    ]

    # mock all pages
    for page, next_page in pairwise(pages):
        response = {'results': page['results'], 'next': next_page['url']}
        respx.get(page['url']).mock(return_value=httpx.Response(200, json=response))

    result = await test_client.async_get_items_model()
    assert result == expected


@respx.mock
@pytest.mark.asyncio
async def test_infinite_pagination(test_client):
    # set pages urls and results + add last 'None' page
    pages = [
        {
            'url': 'https://test.skillcorner.fr/items/',
            'results': [{'oid': 1, 'name': 'one'}, {'oid': 2, 'name': 'two'}, {'oid': 3, 'name': 'three'}],
        },
        {
            'url': 'https://skillcorner.com/test?foo=bar&offset=3',
            'results': [{'oid': 4, 'name': 'for'}, {'oid': 5, 'name': 'five'}, {'oid': 6, 'name': 'six'}],
        },
        {
            'url': 'https://skillcorner.com/test?foo=bar&offset=6',
            'results': [{'oid': 12, 'name': 'twelve'}, {'oid': 14, 'name': 'fourteen'}],
        },
        {
            'url': 'https://skillcorner.com/test?foo=bar&offset=6',
            'results': [{'oid': 12, 'name': 'twelve'}, {'oid': 14, 'name': 'fourteen'}],
        },
    ]

    # mock all pages
    for page, next_page in pairwise(pages):
        response = {'results': page['results'], 'next': next_page['url']}
        respx.get(page['url']).mock(return_value=httpx.Response(200, json=response))

    with pytest.raises(InfinitePaginationError) as exc_info:
        await test_client.async_get_items_model()

    assert exc_info.value.url_stack == [
        'https://skillcorner.com/test?foo=bar&offset=3',
        'https://skillcorner.com/test?foo=bar&offset=6',
        'https://skillcorner.com/test?foo=bar&offset=6',
    ]
