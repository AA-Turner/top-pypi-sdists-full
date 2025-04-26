import unittest.mock as mock

from tap_aftership.streams import TrackingsPaginator


def test_paginator_has_more():
    mock_response = mock.MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": {"trackings": ["not_empty"]}, "page": 1}

    p = TrackingsPaginator(1)
    assert p.has_more(mock_response)


def test_paginator_no_more_items():
    mock_response = mock.MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": {"trackings": []}, "page": 1}

    p = TrackingsPaginator(1)
    assert not p.has_more(mock_response)


def test_high_page_number():
    mock_response = mock.MagicMock()
    mock_response.status_code = 400
    mock_response.json.return_value = {"data": {"trackings": ["not_empty"]}, "page": 1}

    p = TrackingsPaginator(1)
    assert not p.has_more(mock_response)
