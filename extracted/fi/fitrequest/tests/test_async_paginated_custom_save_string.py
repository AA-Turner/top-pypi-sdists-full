from itertools import pairwise

import httpx
import pytest
import respx

from fitrequest.errors import InfinitePaginationError
from tests.demo_paginated import test_client


@respx.mock
@pytest.mark.asyncio
async def test_paginate_and_return_one_page(test_client, tmp_path):
    tmp_file = tmp_path / 'out'
    expected = [1, 2, 3]
    response = '1,2,3|'

    respx.get(
        'https://test.skillcorner.fr/items/',
    ).mock(return_value=httpx.Response(200, json=response))

    await test_client.async_get_custom_save_str_items(filepath=tmp_file)
    assert list(map(int, tmp_file.read_text().split())) == expected


@respx.mock
@pytest.mark.asyncio
async def test_paginate_and_return_two_pages(test_client, tmp_path):
    tmp_file = tmp_path / 'out'
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

    await test_client.async_get_custom_save_str_items(filepath=tmp_file)
    assert list(map(int, tmp_file.read_text().split())) == expected


@respx.mock
@pytest.mark.asyncio
async def test_paginate_and_return_three_pages(test_client, tmp_path):
    tmp_file = tmp_path / 'out'
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

    await test_client.async_get_custom_save_str_items(filepath=tmp_file)
    assert list(map(int, tmp_file.read_text().split())) == expected


@respx.mock
@pytest.mark.asyncio
async def test_infinite_pagination(test_client, tmp_path):
    tmp_file = tmp_path / 'out'

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
        await test_client.async_get_custom_save_str_items(filepath=tmp_file)

    assert exc_info.value.url_stack == [
        'https://skillcorner.com/test?foo=bar&offset=3',
        'https://skillcorner.com/test?foo=bar&offset=6',
        'https://skillcorner.com/test?foo=bar&offset=6',
    ]
