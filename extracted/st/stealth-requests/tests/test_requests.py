import re

import pytest
import stealth_requests as stealth
from stealth_requests import StealthSession, AsyncStealthSession


URL = 'https://httpbin.org'


# --- Sync ---


def test_get():
    resp = stealth.get(f'{URL}/get')
    assert resp.status_code == 200


def test_post():
    resp = stealth.post(f'{URL}/post', json={'key': 'value'})
    assert resp.status_code == 200
    assert resp.json()['json']['key'] == 'value'


def test_session_get():
    with StealthSession() as s:
        resp = s.get(f'{URL}/get')
        assert resp.status_code == 200


def test_session_sets_referer():
    with StealthSession() as s:
        s.get(f'{URL}/get')
        resp = s.get(f'{URL}/headers')
        headers = resp.json()['headers']
        assert f'{URL}/get' in headers.get('Referer', '')


def test_session_has_user_agent():
    with StealthSession() as s:
        resp = s.get(f'{URL}/headers')
        headers = resp.json()['headers']
        assert 'User-Agent' in headers
        assert headers['User-Agent'] != ''


# --- Async ---


@pytest.mark.asyncio
async def test_async_get():
    async with AsyncStealthSession() as s:
        resp = await s.get(f'{URL}/get')
        assert resp.status_code == 200


@pytest.mark.asyncio
async def test_async_post():
    async with AsyncStealthSession() as s:
        resp = await s.post(f'{URL}/post', json={'hello': 'world'})
        assert resp.status_code == 200
        assert resp.json()['json']['hello'] == 'world'


@pytest.mark.asyncio
async def test_async_session_sets_referer():
    async with AsyncStealthSession() as s:
        await s.get(f'{URL}/get')
        resp = await s.get(f'{URL}/headers')
        headers = resp.json()['headers']
        assert f'{URL}/get' in headers.get('Referer', '')


# --- Response features (using a real HTML page) ---

HTML_URL = 'https://books.toscrape.com'


def test_repr():
    resp = stealth.get(f'{URL}/get')
    assert re.fullmatch(r'<StealthResponse \[Status: \d+ Elapsed Time: \d+\.\d+ seconds\]>', repr(resp))


def test_links():
    resp = stealth.get(HTML_URL)
    assert isinstance(resp.links, tuple)
    assert len(resp.links) > 0
    assert all(isinstance(link, str) for link in resp.links)


def test_images():
    resp = stealth.get(HTML_URL)
    assert isinstance(resp.images, tuple)
    assert len(resp.images) > 0
    assert all(isinstance(img, str) for img in resp.images)


def test_emails():
    resp = stealth.get(f'{URL}/html')
    assert isinstance(resp.emails, tuple)


def test_phone_numbers():
    resp = stealth.get(f'{URL}/html')
    assert isinstance(resp.phone_numbers, tuple)


def test_metadata():
    resp = stealth.get(HTML_URL)
    meta = resp.meta
    assert meta.title is not None
    assert isinstance(meta.title, str)
