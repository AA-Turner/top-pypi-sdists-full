import urllib
from datetime import datetime, timedelta

import pytest
from django.urls import resolve
from django.utils import timezone
from faker import Faker
from rest_framework import exceptions
from rest_framework.test import APIRequestFactory

from wbcore.contrib.authentication.authentication import inject_short_lived_token
from wbcore.contrib.authentication.models import Token, User

fake = Faker()
now = datetime.now()


class TestTokenUnitTests:
    @pytest.fixture
    def request_with_user(self: User):
        request = APIRequestFactory().get("/")
        request.user = self
        return request

    def setup_method(self):
        self.token = Token()

    @pytest.mark.parametrize("is_valid", [True, False])
    def test_check_validity_for_endpoint_for_infinite_token(self, is_valid, mocker):
        mocker.patch.object(self.token, "is_valid", is_valid)
        if self.token.is_valid:
            assert self.token.check_validity_for_endpoint(fake.sentence(), fake.date_time())
        else:
            with pytest.raises(exceptions.AuthenticationFailed) as exc_info:
                assert self.token.check_validity_for_endpoint(fake.sentence(), fake.date_time())
            assert str(exc_info.value) == "Token is not valid anymore"

    def test_check_invalidity_for_endpoint_for_expired_token(self, mocker):
        mocker.patch.object(self.token, "valid_until", now)
        assert self.token.check_validity_for_endpoint(
            self.token.protected_view_name, self.token.valid_until - timedelta(minutes=1)
        )
        with pytest.raises(exceptions.AuthenticationFailed) as exc_info:
            self.token.check_validity_for_endpoint(
                self.token.protected_view_name, self.token.valid_until + timedelta(minutes=1)
            )
        assert str(exc_info.value) == "Token has expired"

    def test_check_invalidity_for_endpoint_for_exhausted_token(self, mocker):
        mocker.patch.object(self.token, "number_usage_left", 2)
        mocker.patch.object(self.token, "save")
        while self.token.number_usage_left > 0:
            assert self.token.check_validity_for_endpoint(self.token.protected_view_name, fake.date_time())
        with pytest.raises(exceptions.AuthenticationFailed) as exc_info:
            self.token.check_validity_for_endpoint(self.token.protected_view_name, fake.date_time())
        assert str(exc_info.value) == "Token usage exhausted"

    def test_check_unvalidity_for_endpoint_for_wrong_endpoint(self, mocker):
        mocker.patch.object(self.token, "protected_view_name", "Some View Name")
        with pytest.raises(exceptions.AuthenticationFailed) as exc_info:
            self.token.check_validity_for_endpoint("wbcore:authentication:wrongview", fake.date_time())
        assert str(exc_info.value) == "Token has limited scope that doesn't match the requested endpoint"

    @pytest.mark.django_db
    @pytest.mark.parametrize("view_name", [(None, "wbcore:authentication:user")])
    def test_generate_token_for_user(self, user, view_name):
        d1 = fake.date_time()
        n1 = fake.pyint()
        token = Token.generate_token_for_user(user, protected_view_name=view_name, valid_until=d1, number_of_usages=n1)
        assert token.user == user
        assert token.protected_view_name == view_name
        assert token.valid_until == d1
        assert token.number_usage_left == n1
        token.is_valid = False
        token.save()  # invalid token to check that retrieving it will enable it

        d2 = fake.date_time()
        n2 = fake.pyint()
        new_token = Token.generate_token_for_user(
            user, protected_view_name=view_name, valid_until=d2, number_of_usages=n2
        )
        assert new_token == token  # check that the uniqueness on schema work
        assert new_token.valid_until == d2
        assert new_token.number_usage_left == n2
        assert new_token.is_valid is True

    @pytest.mark.django_db
    @pytest.mark.parametrize(
        "endpoint,creation_time",
        [
            ("http://localhost:5000/wbcore/authentication/user/", now),
            ("http://localhost:5000/wbcore/authentication/user/?some_param=True", now),
            ("/wbcore/authentication/user/?some_param=True&other_param=foo", now),
        ],
    )
    def test_generate_shareable_link(self, user, endpoint, creation_time):
        creation_time = timezone.make_aware(creation_time)
        parse_url = urllib.parse.urlsplit(urllib.parse.unquote(endpoint))
        base_params = dict(urllib.parse.parse_qsl(parse_url.query))
        link = self.token.generate_shareable_link(endpoint, user, creation_time=creation_time)
        res_params = dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(urllib.parse.unquote(link)).query))

        assert endpoint in link  # check that the resulting endpoint is not modified
        for k, v in base_params.items():  # check that the base query parameters weren't touched
            assert res_params[k] == v
        assert (
            res_params["token"]
            == Token.objects.get(user=user, protected_view_name=resolve(parse_url.path).view_name).key
        )  # check that the token was injected as query parameter

    @pytest.mark.django_db
    @pytest.mark.parametrize("view_name", [("wbcore:authentication:user", None)])
    def test_inject_short_lived_token(self, user, view_name, request_with_user):
        link = fake.url() + "?a=a&b=b"

        @inject_short_lived_token(view_name=view_name)
        def dummy_resources(serializer, instance, request, user, **kwargs):
            return {"resource": link}

        res = dummy_resources(None, None, request_with_user, user)
        res_params = dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(urllib.parse.unquote(res["resource"])).query))
        assert link in res["resource"]  # check that the resulting endpoint is not modified
        assert res_params["a"] == "a"
        assert res_params["b"] == "b"
        assert (
            res_params["token"] == Token.objects.get(user=user, protected_view_name=view_name).key
        )  # check that the token was injected as query parameter
