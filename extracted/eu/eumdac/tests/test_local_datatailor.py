import pytest

from eumdac.errors import EumdacError


def test_urls(monkeypatch, tmp_path):
    from eumdac.local_tailor import new_url_filename, all_url_filenames, resolve_url, remove_url
    from eumdac.token import URLs

    test_url_id = "test"
    test_url = URLs()

    def mock_get_url_path():
        return tmp_path

    monkeypatch.setattr("eumdac.local_tailor.get_url_path", mock_get_url_path)

    test_path = new_url_filename(test_url_id)
    assert not test_path.exists()
    with test_path.open("w") as tf:
        test_url.write(tf)
    assert test_path.exists()

    # requesting an existing id works
    new_url_filename(test_url_id)

    # resolving an existing url succeeds
    resolve_url(test_url_id)

    # remove all urls
    url_paths = all_url_filenames()
    for up in url_paths:
        remove_url(up.stem)
        assert not up.exists()

    # resolving a removed url raises
    with pytest.raises(EumdacError):
        resolve_url(test_url_id)


def test_local_tailor(monkeypatch, tmp_path):
    from eumdac.local_tailor import (
        new_local_tailor,
        get_local_tailor,
        remove_local_tailor,
        is_online,
        get_api_url,
    )
    from eumdac.token import URLs

    tailor_id = "test"
    tailor_url = "http://NON.EXISTANT:40000"

    def mock_get_url_path():
        return tmp_path

    monkeypatch.setattr("eumdac.local_tailor.get_url_path", mock_get_url_path)

    tailor_path = new_local_tailor(tailor_id, tailor_url)
    assert tailor_path.exists()

    # creating the same tailor_id works
    new_local_tailor(tailor_id, tailor_url)

    _ = get_local_tailor(tailor_id)

    assert is_online(tailor_path) == False
    assert get_api_url(tailor_path).startswith(tailor_url)

    remove_local_tailor(tailor_id)
    # retrieving removed tailor_id fails
    with pytest.raises(EumdacError):
        get_local_tailor(tailor_id)
