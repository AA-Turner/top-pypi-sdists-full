import httpx
import pytest
import respx
from fitrequest.errors import UnrecognizedParametersError

from skillcorner.client import SkillcornerClient

# TODO test manually client & check how authentication works here
# TODO go over all tests and check if they have meaning
# TODO add test for infinite loop pagination


@respx.mock
def test_get_matches():
    body = {
        'count': 1,
        'result': [
            {
                'id': 46771,
                'date_time': '2021-08-13T19:00:00Z',
                'home_team': {'id': 754, 'short_name': 'Brentford FC'},
                'away_team': {'id': 3, 'short_name': 'Arsenal'},
                'status': 'closed',
            },
        ],
    }
    response = httpx.Response(200, json=body)
    respx.get('https://skillcorner.com/api/matches').mock(return_value=response)

    response = SkillcornerClient().get_matches()
    assert response == body


@respx.mock
def test_get_matches_paginated():
    body_1 = {
        'count': 6,
        'next': 'https://skillcorner.com/api/matches?limit=3&offset=3',
        'previous': None,
        'results': [
            {
                'id': 1,
            },
            {
                'id': 2,
            },
            {
                'id': 3,
            },
        ],
    }
    body_2 = {
        'count': 6,
        'next': None,
        'previous': 'https://skillcorner.com/api/matches?limit=3',
        'results': [
            {
                'id': 4,
            },
            {
                'id': 5,
            },
            {
                'id': 6,
            },
        ],
    }
    expected = [
        {
            'id': 1,
        },
        {
            'id': 2,
        },
        {
            'id': 3,
        },
        {
            'id': 4,
        },
        {
            'id': 5,
        },
        {
            'id': 6,
        },
    ]
    response_2 = httpx.Response(200, json=body_2)
    respx.get('https://skillcorner.com/api/matches?limit=3&offset=3').mock(return_value=response_2)

    response_1 = httpx.Response(200, json=body_1)
    respx.get('https://skillcorner.com/api/matches').mock(return_value=response_1)

    response_final = SkillcornerClient().get_matches()
    assert response_final == expected


@respx.mock
def test_get_matches_with_params_list():
    body = [
        {
            'id': 46771,
            'date_time': '2021-08-13T19:00:00Z',
            'home_team': {'id': 754, 'short_name': 'Brentford FC'},
            'away_team': {'id': 3, 'short_name': 'Arsenal'},
            'status': 'closed',
        },
    ]
    competition_edition = [287, 387]

    params_method = {'competition_edition': competition_edition}
    params_request = {'competition_edition': ','.join(map(str, competition_edition))}

    response = httpx.Response(200, json=body)
    respx.get('https://skillcorner.com/api/matches', params=params_request).mock(return_value=response)

    response = SkillcornerClient().get_matches(params=params_method)
    assert response == body


@respx.mock
def test_get_matches_with_params_str_list():
    body = [
        {
            'id': 46771,
            'date_time': '2021-08-13T19:00:00Z',
            'home_team': {'id': 754, 'short_name': 'Brentford FC'},
            'away_team': {'id': 3, 'short_name': 'Arsenal'},
            'status': 'closed',
        },
    ]
    competition_edition = [287, 387]
    params = {'competition_edition': ','.join(map(str, competition_edition))}

    response = httpx.Response(200, json=body)
    respx.get('https://skillcorner.com/api/matches', params=params).mock(return_value=response)

    response = SkillcornerClient().get_matches(params=params)
    assert response == body


@respx.mock
def test_get_matches_with_params_other_types():
    body = [
        {
            'id': 46771,
            'date_time': '2021-08-13T19:00:00Z',
            'home_team': {'id': 754, 'short_name': 'Brentford FC'},
            'away_team': {'id': 3, 'short_name': 'Arsenal'},
            'status': 'closed',
        },
    ]
    params = {'param1': 1, 'param2': 'b', 'params3': None, 'params4': {'x': 1, 'y': 2}}
    cleaned_params = {key: val for key, val in params.items() if val is not None}

    response = httpx.Response(200, json=body)
    respx.get('https://skillcorner.com/api/matches', params=cleaned_params).mock(return_value=response)

    # fitrequest ignores params with None values
    response = SkillcornerClient().get_matches(params=params)
    assert response == body


@respx.mock
def test_get_matches_with_random_kwargs():
    body = [
        {
            'id': 46771,
            'date_time': '2021-08-13T19:00:00Z',
            'home_team': {'id': 754, 'short_name': 'Brentford FC'},
            'away_team': {'id': 3, 'short_name': 'Arsenal'},
            'status': 'closed',
        },
    ]
    response = httpx.Response(200, json=body)
    respx.get('https://skillcorner.com/api/matches').mock(return_value=response)

    with pytest.raises(UnrecognizedParametersError):
        SkillcornerClient().get_matches(kwarg_1='kwarg_1', kwarg_2='kwarg_2')


@respx.mock
def test_get_matches_with_unknown_arg():
    with pytest.raises(TypeError):
        SkillcornerClient().get_matches({'arg1_is': 'params'}, 'raise_for_status_arg', 'unknown_arg')
