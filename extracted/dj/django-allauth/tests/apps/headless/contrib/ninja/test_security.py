from django.contrib.auth import HASH_SESSION_KEY

from allauth.headless.constants import Client
from allauth.headless.contrib.ninja.security import XSessionTokenAuth


def test_authenticate(rf, user, headless_client, auth_client):
    if headless_client == Client.BROWSER:
        return
    request = rf.get("/", HTTP_X_SESSION_TOKEN=auth_client.session_token)
    auth_user = XSessionTokenAuth()(request)
    assert auth_user.pk == user.pk


def test_invalid_authentication(rf, user, headless_client, auth_client):
    if headless_client == Client.BROWSER:
        return
    request = rf.get("/", HTTP_X_SESSION_TOKEN="wrong")
    result = XSessionTokenAuth()(request)
    assert result is None


def test_authenticate_rejects_stale_session_auth_hash(
    rf, user, headless_client, auth_client, password_factory
):
    if headless_client == Client.BROWSER:
        return
    user.set_password(password_factory())
    user.save()
    request = rf.get("/", HTTP_X_SESSION_TOKEN=auth_client.session_token)
    assert XSessionTokenAuth()(request) is None


def test_authenticate_survives_session_auth_hash_update(
    rf, user, headless_client, auth_client, password_factory
):
    if headless_client == Client.BROWSER:
        return
    session = auth_client.headless_session()
    user.set_password(password_factory())
    user.save()
    session[HASH_SESSION_KEY] = user.get_session_auth_hash()
    session.save()
    request = rf.get("/", HTTP_X_SESSION_TOKEN=auth_client.session_token)
    auth_user = XSessionTokenAuth()(request)
    assert auth_user.pk == user.pk


def test_authenticate_with_unusable_password(rf, user, headless_client, client):
    if headless_client == Client.BROWSER:
        return
    user.set_unusable_password()
    user.save(update_fields=["password"])
    client.force_login(user)
    request = rf.get("/", HTTP_X_SESSION_TOKEN=client.session_token)
    auth_user = XSessionTokenAuth()(request)
    assert auth_user.pk == user.pk
