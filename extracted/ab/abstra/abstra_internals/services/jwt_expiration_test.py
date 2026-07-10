import time
import unittest
from unittest.mock import patch

import jwt as pyjwt

from abstra_internals.services.jwt import _decode_jwt_cached, decode_jwt

AUD = "web-editor-test-project"


def make_token(exp: float, aud: str = AUD) -> str:
    return pyjwt.encode(
        {"authorId": "author-1", "email": "user@test.com", "exp": exp, "aud": aud},
        "any-secret",
        algorithm="HS256",
    )


@patch("abstra_internals.services.jwt.PUBLIC_KEY", None)
class TestDecodeJwtExpiration(unittest.TestCase):
    def setUp(self):
        _decode_jwt_cached.cache_clear()

    def test_valid_token_returns_claims(self):
        token = make_token(exp=time.time() + 3600)
        claims = decode_jwt(token, aud=AUD)
        self.assertIsNotNone(claims)
        assert claims is not None
        self.assertEqual(claims["authorId"], "author-1")

    def test_expired_token_returns_none(self):
        token = make_token(exp=time.time() - 10)
        self.assertIsNone(decode_jwt(token, aud=AUD))

    def test_token_expiring_after_being_cached_returns_none(self):
        # Regression: the lru_cache used to keep a token "valid" for the life
        # of the process even after its exp had passed.
        now = time.time()
        token = make_token(exp=now + 60)

        self.assertIsNotNone(decode_jwt(token, aud=AUD))

        with patch("abstra_internals.services.jwt.time") as mock_time:
            mock_time.time.return_value = now + 120
            self.assertIsNone(decode_jwt(token, aud=AUD))

    def test_wrong_audience_returns_none(self):
        token = make_token(exp=time.time() + 3600, aud="web-editor-other-project")
        self.assertIsNone(decode_jwt(token, aud=AUD))

    def test_skip_verify_ignores_expiration(self):
        # Documented development behavior: skip_verify skips every check.
        token = make_token(exp=time.time() - 10)
        self.assertIsNotNone(decode_jwt(token, skip_verify=True))


if __name__ == "__main__":
    unittest.main()
