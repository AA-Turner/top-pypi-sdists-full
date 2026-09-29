import uuid
from unittest.mock import patch

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.messages.api import get_messages
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.core import mail, validators
from django.core.exceptions import ValidationError
from django.template import Context, Template
from django.test.client import RequestFactory
from django.test.utils import override_settings
from django.urls import reverse

import pytest

import allauth.app_settings
from allauth.account.adapter import get_adapter
from allauth.account.models import EmailAddress
from allauth.account.utils import (
    filter_users_by_username,
    url_str_to_user_pk,
    user_pk_to_url_str,
    user_username,
)
from allauth.core import context

from .test_models import UUIDUser


test_username_validators = [
    validators.RegexValidator(regex=r"^[a-c]+$", message="not abc")
]


def test_url_str_to_pk_identifies_UUID_as_stringlike(db):
    with patch("allauth.account.utils.get_user_model") as mocked_gum:
        mocked_gum.return_value = UUIDUser
        user_id = uuid.uuid4().hex
        assert url_str_to_user_pk(user_id) == uuid.UUID(user_id)


def test_pk_to_url_string_identifies_UUID_as_stringlike():
    with patch("allauth.account.utils.get_user_model") as mocked_gum:
        mocked_gum.return_value = UUIDUser
        user = UUIDUser(is_active=True, email="john@example.com", username="john")
        assert user_pk_to_url_str(user) == user.pk.hex


@override_settings(ACCOUNT_PRESERVE_USERNAME_CASING=False)
def test_username_lower_cased():
    user = get_user_model()()
    user_username(user, "CamelCase")
    assert user_username(user) == "camelcase"
    # TODO: Actually test something
    filter_users_by_username("CamelCase", "FooBar")


@override_settings(ACCOUNT_PRESERVE_USERNAME_CASING=True)
def test_username_case_preserved():
    user = get_user_model()()
    user_username(user, "CamelCase")
    assert user_username(user) == "CamelCase"
    # TODO: Actually test something
    filter_users_by_username("camelcase", "foobar")


def test_user_display():
    user = get_user_model()(username="john<br/>doe")
    expected_name = "john&lt;br/&gt;doe"
    templates = [
        "{% load account %}{% user_display user %}",
        "{% load account %}{% user_display user as x %}{{ x }}",
    ]
    for template in templates:
        t = Template(template)
        content = t.render(Context({"user": user}))
        assert content == expected_name


def test_message_escaping(db):
    request = RequestFactory().get("/")
    SessionMiddleware(lambda request: None).process_request(request)
    MessageMiddleware(lambda request: None).process_request(request)
    user = get_user_model()()
    user_username(user, "'<8")
    context = {"user": user}
    get_adapter().add_message(
        request, messages.SUCCESS, "account/messages/logged_in.txt", context
    )
    msgs = get_messages(request)
    actual_message = msgs._queued_messages[0].message
    assert user.username in actual_message, actual_message


def test_email_escaping(db):
    site_name = "testserver"
    if allauth.app_settings.SITES_ENABLED:
        from django.contrib.sites.models import Site

        site = Site.objects.get_current()
        site.name = site_name = '<enc&"test>'
        site.save()
    u = get_user_model().objects.create(username="test", email="user@example.com")
    request = RequestFactory().get("/")
    SessionMiddleware(lambda request: None).process_request(request)
    MessageMiddleware(lambda request: None).process_request(request)
    EmailAddress.objects.add_email(request, u, u.email, confirm=True)
    assert mail.outbox[0].subject[1:].startswith(site_name)


@override_settings(
    ACCOUNT_USERNAME_VALIDATORS="tests.apps.account.test_utils.test_username_validators"
)
def test_username_validator(db):
    get_adapter().clean_username("abc")
    with pytest.raises(ValidationError):
        get_adapter().clean_username("def")


def test_username_validation_rejects_db_collation_collision(db):
    user = get_user_model().objects.create(username="admin")
    candidates = get_user_model().objects.filter(pk=user.pk)
    with patch(
        "allauth.account.internal.userkit.filter_users_by_username",
        return_value=candidates,
    ):
        with pytest.raises(ValidationError):
            get_adapter().clean_username("ádmin")


@pytest.mark.parametrize(
    ("allowed_hosts", "url", "expected"),
    [
        (["allowed_host", "testserver"], "http://allowed_host/", True),
        (["allowed_host", "testserver"], "http://other_host/", False),
        ([".example.com", "testserver"], "http://bla.example.com", True),
        ([".example.com", "testserver"], "http://example.com", True),
        ([".example.com", "testserver"], "http://not-example.com", False),
        (["*", "allowed_host"], "http://testserver/", True),
        (["*", "allowed_host"], "http://allowed_host/", True),
        (["*", "allowed_host"], "/foo/bar", True),
        (["*", "allowed_host"], "http://foobar.com/", False),
        (["*", "allowed_host"], "http://other_host/", False),
        (["allowed_host", "testserver"], "/foo/bar", True),
    ],
)
def test_is_safe_url(settings, allowed_hosts, url, expected):
    settings.ALLOWED_HOSTS = allowed_hosts
    with context.request_context(RequestFactory().get("/")):
        assert get_adapter().is_safe_url(url) is expected


def test_redirect_noreversematch(auth_client):
    # We used to call `django.shortcuts.redirect()` as is, but that one throws a
    # `NoReverseMatch`, resulting in 500s.
    resp = auth_client.post(f"{reverse('account_logout')}?next=badurlname")
    assert resp["location"] == "/badurlname"
