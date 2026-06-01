"""Tests for UserClaims dataclass."""

from datetime import UTC, datetime, timedelta

from csrd.models.claims import UserClaims


class TestUserClaims:
    def test_defaults(self):
        claims = UserClaims()
        assert claims.sub == ""
        assert claims.user_name == ""
        assert claims.authorities == []
        assert claims.iat is not None
        assert claims.exp is not None

    def test_exp_auto_generated(self):
        claims = UserClaims(sub="user1")
        assert claims.exp == claims.iat + timedelta(hours=1)

    def test_custom_exp_preserved(self):
        custom_exp = datetime(2030, 1, 1, tzinfo=UTC)
        claims = UserClaims(sub="user1", exp=custom_exp)
        assert claims.exp == custom_exp

    def test_authorities_list(self):
        claims = UserClaims(sub="admin", authorities=["ROLE_ADMIN", "ROLE_USER"])
        assert len(claims.authorities) == 2
        assert "ROLE_ADMIN" in claims.authorities

    def test_mutable_authorities(self):
        claims = UserClaims()
        claims.authorities.append("NEW_ROLE")
        # Verify the default_factory creates independent lists
        claims2 = UserClaims()
        assert "NEW_ROLE" not in claims2.authorities

    def test_user_name_falls_back_to_sub(self):
        claims = UserClaims(sub="frost")
        assert claims.user_name == "frost"

    def test_user_name_explicit_value_wins(self):
        claims = UserClaims(sub="frost", user_name="FrostMN")
        assert claims.user_name == "FrostMN"
