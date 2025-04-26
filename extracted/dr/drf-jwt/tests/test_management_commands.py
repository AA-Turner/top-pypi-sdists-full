# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf import settings
from django.core.management import call_command
from six import StringIO
from pytest import raises
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


def test_obtain_token_command_should_fail_in_DEBUG_False(
        monkeypatch, user
):
    monkeypatch.setattr(settings, "DEBUG", False)
    with raises(SystemExit):
        call_command('obtain_token', str(user.pk))


def test_obtain_token_command_should_produce_valid_token(
        monkeypatch, user
):
    output = StringIO()
    monkeypatch.setattr(settings, "DEBUG", True)
    call_command('obtain_token', str(user.pk), stdout=output)
    output.seek(0)
    printed_token = output.read()

    payload = JSONWebTokenAuthentication.jwt_decode_token(printed_token.strip().encode())
    assert payload['user_id'] == user.pk
