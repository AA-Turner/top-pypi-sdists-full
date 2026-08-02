import requests
import pytest

from jaraco.net.http.cookies import ShelvedCookieJar, Shelf


@pytest.fixture
def session(tmp_path):
    session = requests.Session()
    session.cookies = ShelvedCookieJar.create(tmp_path)
    return session


def test_cookie_shelved(responses, session):
    responses.get('http://any/', headers={'Set-Cookie': 'foo=bar'})
    session.get('http://any/')
    assert session.cookies

    assert ShelvedCookieJar(Shelf(session.cookies.shelf.filename))


def test_cookie_get(responses, session):
    responses.get('http://any/', headers={'Set-Cookie': 'foo=bar'})
    session.get('http://any/')
    assert session.cookies.get('foo') == 'bar'
    assert session.cookies.get('missing') is None
