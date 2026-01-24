from skillcorner.pagination import _is_response_paginated


def test_is_response_paginated_not_a_dict_bytes_true():
    response = b'foobar'
    assert _is_response_paginated(response) is True


def test_is_response_paginated_not_a_dict_list_true():
    response = [1, 2, 3]
    assert _is_response_paginated(response) is True


def test_is_response_paginated_with_next_to_None_false():
    response = {'foo': 'bar', 'next': None}
    assert _is_response_paginated(response) is False


def test_is_response_paginated_without_next_true():
    response = {'foo': 'bar'}
    assert _is_response_paginated(response) is True


def test_is_response_paginated_false():
    response = {'foo': 'bar', 'next': 'url_for_next_results'}
    assert _is_response_paginated(response) is False
