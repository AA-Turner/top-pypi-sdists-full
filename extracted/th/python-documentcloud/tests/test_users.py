# Future
from __future__ import division, print_function, unicode_literals

# Standard Library
from builtins import str


def test_user(client):
    user = client.users.get(client.user_id)
    assert str(user) == user.username
