import httpx
import pytest
import respx
from fitrequest.errors import HTTPStatusError, UnrecognizedParametersError

from skillcorner.client import SkillcornerClient


@respx.mock
def test_get_match():
    body = {
        'date_time': '2021-08-13T19:00:00Z',
        'home_team': {'id': 754, 'short_name': 'Brentford FC'},
        'away_team': {'id': 3, 'short_name': 'Arsenal'},
    }
    match_id = 42
    respx.get(f'https://skillcorner.com/api/match/{match_id}').mock(return_value=httpx.Response(200, json=body))

    response = SkillcornerClient().get_match(match_id=match_id)
    assert response == body


@respx.mock
def test_get_match_raise_on_status():
    err_code = 404
    respx.get('https://skillcorner.com/api/match/7').mock(return_value=httpx.Response(err_code))

    with pytest.raises(HTTPStatusError) as err:
        SkillcornerClient().get_match(7)
    assert err.value.status_code == err_code


@respx.mock
def test_get_match_with_params():
    body = {
        'date_time': '2021-08-13T19:00:00Z',
        'home_team': {'id': 754, 'short_name': 'Brentford FC'},
        'away_team': {'id': 3, 'short_name': 'Arsenal'},
    }
    match_id = 42
    respx.get(f'https://skillcorner.com/api/match/{match_id}').mock(return_value=httpx.Response(200, json=body))

    response = SkillcornerClient().get_match(match_id, {'unused_param': 'foo'})
    assert response == body


@respx.mock
def test_get_match_with_random_kwargs():
    body = {
        'date_time': '2021-08-13T19:00:00Z',
        'home_team': {'id': 754, 'short_name': 'Brentford FC'},
        'away_team': {'id': 3, 'short_name': 'Arsenal'},
    }
    match_id = 42
    respx.get(f'https://skillcorner.com/api/match/{match_id}').mock(return_value=httpx.Response(200, json=body))

    with pytest.raises(UnrecognizedParametersError):
        SkillcornerClient().get_match(match_id, kwarg_1='kwarg_1', kwarg_2='kwarg_2')


@respx.mock
def test_get_match_with_unknown_arg():
    match_id = 33
    with pytest.raises(TypeError):
        SkillcornerClient().get_match(match_id, {'unused_param': 'foo'}, 'raise_for_status_arg', 'unknown_arg')
