# -*- coding: utf-8 -*-

from datetime import datetime
from datetime import timedelta
from django.utils import timezone

import pytest

from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.blacklist.models import BlacklistedToken
from rest_framework_jwt.settings import api_settings

import uuid


@pytest.mark.parametrize(
    'id_setting', ['require', 'include']
)
def test_token_is_blocked_by_id(user, monkeypatch, id_setting):
    monkeypatch.setattr(api_settings, "JWT_TOKEN_ID", id_setting)
    payload = JSONWebTokenAuthentication.jwt_create_payload(user)
    token = JSONWebTokenAuthentication.jwt_encode_payload(payload)

    expiration = timezone.now() + timedelta(days=1)
    BlacklistedToken(
        token_id=payload['jti'],
        expires_at=expiration,
        user=user,
    ).save()

    assert BlacklistedToken.is_blocked(token, payload) is True



@pytest.mark.parametrize(
    'id_setting', ['require', 'include']
)
def test_refreshed_token_is_blocked_by_original_id(user, call_auth_refresh_endpoint, monkeypatch, id_setting):
    monkeypatch.setattr(api_settings, "JWT_TOKEN_ID", id_setting)
    original_payload = JSONWebTokenAuthentication.jwt_create_payload(user)
    original_token = JSONWebTokenAuthentication.jwt_encode_payload(original_payload)

    refresh_response = call_auth_refresh_endpoint(original_token)
    refreshed_token = refresh_response.json()['token']
    payload = JSONWebTokenAuthentication.jwt_decode_token(refreshed_token)

    expiration = timezone.now() + timedelta(days=1)
    BlacklistedToken(
        token_id=original_payload['jti'],
        expires_at=expiration,
        user=user,
    ).save()

    assert BlacklistedToken.is_blocked(refreshed_token, payload) is True


@pytest.mark.parametrize(
    'id_setting', ['include', 'off']
)
def test_token_is_blocked_by_value(user, monkeypatch, id_setting):
    monkeypatch.setattr(api_settings, "JWT_TOKEN_ID", id_setting)
    payload = JSONWebTokenAuthentication.jwt_create_payload(user)
    token = JSONWebTokenAuthentication.jwt_encode_payload(payload)

    expiration = timezone.now() + timedelta(days=1)
    BlacklistedToken(
        token=token,
        expires_at=expiration,
        user=user,
    ).save()

    assert BlacklistedToken.is_blocked(token, payload) is True


def test_token_is_not_blocked_by_value_when_ids_required(user, monkeypatch):
    monkeypatch.setattr(api_settings, "JWT_TOKEN_ID", "require")
    payload = JSONWebTokenAuthentication.jwt_create_payload(user)
    token = JSONWebTokenAuthentication.jwt_encode_payload(payload)

    expiration = timezone.now() + timedelta(days=1)
    BlacklistedToken(
        token=token,
        expires_at=expiration,
        user=user,
    ).save()

    assert BlacklistedToken.is_blocked(token, payload) is False


def test_token_is_not_blocked_by_id_when_ids_disabled(user, monkeypatch):
    monkeypatch.setattr(api_settings, "JWT_TOKEN_ID", "off")
    payload = JSONWebTokenAuthentication.jwt_create_payload(user)
    payload['jti'] = uuid.uuid4()
    token = JSONWebTokenAuthentication.jwt_encode_payload(payload)

    expiration = timezone.now() + timedelta(days=1)
    BlacklistedToken(
        token_id=payload['jti'],
        expires_at=expiration,
        user=user,
    ).save()

    assert BlacklistedToken.is_blocked(token, payload) is False



def test_token_has_expected_string_representation(user):
    payload = JSONWebTokenAuthentication.jwt_create_payload(user)
    token = JSONWebTokenAuthentication.jwt_encode_payload(payload)

    expiration = datetime(2021, 11, 1, 12, 34, 56, 123456, tzinfo=timezone.utc)
    banned_token = BlacklistedToken(
        token=token,
        token_id=payload['jti'],
        expires_at=expiration,
        user=user,
    )

    assert str(banned_token) == 'Blacklisted token - username - 2021-11-01 12:34:56.123456+00:00'
