import pytest
from oauthlib.common import Request

from allauth.core.context import request_context
from allauth.idp.oidc.internal.oauthlib.request_validator import (
    OAuthLibRequestValidator,
)


@pytest.mark.parametrize(
    "origin,allowed_origins,is_allowed",
    [
        ("http://origin", ["https://origin"], False),
        ("https://origin", ["https://origin"], True),
        ("https://origin", [], False),
        ("https://origin", ["https://notthis", "https://origin"], True),
    ],
)
def test_is_origin_allowed(origin, allowed_origins, is_allowed, oidc_client, rf):
    oidc_client.set_cors_origins(allowed_origins)
    oidc_client.save()
    request = rf.get("/")
    orequest = Request("/")
    with request_context(request):
        assert (
            OAuthLibRequestValidator().is_origin_allowed(
                oidc_client.id, origin, orequest
            )
            == is_allowed
        )
