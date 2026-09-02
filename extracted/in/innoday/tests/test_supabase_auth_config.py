"""Invariants for `supabase/config.toml`, the auth control plane.

This file is not code, so nothing caught a bad edit until it reached the live
project via `supabase config push` — where the failure mode is silence. Every
assertion below corresponds to a real way this config has broken or could break
auth without raising anything:

* `[auth.email] enable_signup = false` disables the **entire email provider** —
  no login, no invites, no OTP — despite looking like a signup toggle. Email is
  InnoDay's only provider, so that one character takes down onboarding. See #436.
* A `pass` written as a literal puts a live SMTP credential in git.
* An `admin_email` outside the SES-verified domain fails at send time with an
  opaque authorization error, indistinguishable from the rate limit.
* `email_sent` left at the built-in cap wastes the SMTP capacity it gates.
* Losing a `/ui/*` redirect URL makes Supabase silently ignore `redirect_to` and
  fall back to Site URL, stranding invitees (#414 territory).
"""

import re
import tomllib
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = REPO_ROOT / "supabase" / "config.toml"
TF_VARIABLES = REPO_ROOT / "infra" / "terraform" / "variables.tf"


@pytest.fixture(scope="module")
def config() -> dict:
    with CONFIG_PATH.open("rb") as fh:
        return tomllib.load(fh)


@pytest.fixture(scope="module")
def auth(config) -> dict:
    return config["auth"]


class TestSignupToggles:
    """The two `enable_signup` keys are different switches. Do not sync them."""

    def test_public_signup_is_disabled(self, auth):
        assert auth["enable_signup"] is False, (
            "[auth] enable_signup maps to GOTRUE_DISABLE_SIGNUP. Everyone here "
            "arrives by admin invite, so public signup should stay off."
        )

    def test_email_provider_stays_enabled(self, auth):
        """The trap. false here = no login, no invites, no OTP at all."""
        assert auth["email"]["enable_signup"] is True, (
            "[auth.email] enable_signup maps to GOTRUE_EXTERNAL_EMAIL_ENABLED, "
            "the master switch for the email provider — NOT a signup toggle. "
            "Setting it false disables login, magic links, OTP and invites. "
            "Email is the only auth provider, so this takes down onboarding. "
            "Restrict signup with [auth] enable_signup instead. See #436."
        )

    def test_anonymous_signins_stay_disabled(self, auth):
        assert auth["enable_anonymous_sign_ins"] is False


class TestSmtp:
    def test_smtp_is_enabled(self, auth):
        assert auth["email"]["smtp"]["enabled"] is True

    @pytest.mark.parametrize("field", ["pass", "user"])
    def test_credentials_come_from_the_environment(self, auth, field):
        value = auth["email"]["smtp"][field]
        assert re.fullmatch(r"env\(\w+\)", value), (
            f"[auth.email.smtp] {field} must be an env() reference, not a "
            f"literal — a literal would commit a live credential. Got {value!r}."
        )

    def test_no_literal_credential_anywhere_in_the_file(self):
        """Cheap backstop against a pasted AWS key or SMTP password."""
        body = CONFIG_PATH.read_text()
        for pattern, what in [
            (r"AKIA[0-9A-Z]{16}", "an AWS access key id"),
            (r"BI[A-Za-z0-9+/]{40,}", "an SES SMTP password"),
            (r"\bsk-ant-[A-Za-z0-9-]{20,}", "an Anthropic API key"),
        ]:
            assert not re.search(pattern, body), (
                f"config.toml appears to contain {what}"
            )

    def test_host_is_a_regional_ses_endpoint(self, auth):
        host = auth["email"]["smtp"]["host"]
        assert re.fullmatch(r"email-smtp\.[a-z0-9-]+\.amazonaws\.com", host), (
            f"Expected a regional SES SMTP endpoint, got {host!r}."
        )

    def test_host_region_matches_terraform(self, auth):
        """The SMTP password is region-salted — a host/credential region mismatch
        fails authentication, so the two files must agree."""
        host = auth["email"]["smtp"]["host"]
        host_region = host.split(".")[1]
        tf = TF_VARIABLES.read_text()
        tf_region = re.search(
            r'variable\s+"aws_region".*?default\s*=\s*"([^"]+)"', tf, re.S
        )
        assert tf_region, "could not read aws_region default from variables.tf"
        assert host_region == tf_region.group(1), (
            f"config.toml SMTP host is in {host_region} but Terraform provisions "
            f"SES in {tf_region.group(1)}. The SMTP password derivation is "
            "region-salted, so this combination cannot authenticate."
        )

    def test_port_is_starttls(self, auth):
        assert auth["email"]["smtp"]["port"] == 587


class TestSenderIdentity:
    def test_sender_matches_the_terraform_verified_address(self, auth):
        """Drift here is a silent send failure, not an error at push time."""
        admin_email = auth["email"]["smtp"]["admin_email"]
        tf = TF_VARIABLES.read_text()
        tf_from = re.search(
            r'variable\s+"ses_from_address".*?default\s*=\s*"([^"]+)"', tf, re.S
        )
        assert tf_from, "could not read ses_from_address default from variables.tf"
        assert admin_email == tf_from.group(1), (
            f"config.toml sends as {admin_email!r} but Terraform verifies and "
            f"authorises {tf_from.group(1)!r}. The IAM policy pins the From "
            "address, so a mismatch fails every send."
        )

    def test_sender_is_within_the_verified_domain(self, auth):
        admin_email = auth["email"]["smtp"]["admin_email"]
        tf = TF_VARIABLES.read_text()
        tf_domain = re.search(
            r'variable\s+"ses_domain".*?default\s*=\s*"([^"]+)"', tf, re.S
        )
        assert tf_domain, "could not read ses_domain default from variables.tf"
        assert admin_email.endswith("@" + tf_domain.group(1))


class TestRateLimit:
    def test_email_cap_was_raised_past_the_builtin_limit(self, config):
        sent = config["auth"]["rate_limit"]["email_sent"]
        assert sent > 2, (
            "2 is the built-in mailer's un-raisable cap. With custom SMTP "
            "enabled, leaving it at 2 wastes the capacity SES provides."
        )

    def test_email_cap_stays_coherent_with_the_ses_sandbox(self, config):
        """SES sandbox allows 200/day. A high hourly cap lets Supabase accept
        sends SES then rejects, moving the failure somewhere harder to read."""
        sent = config["auth"]["rate_limit"]["email_sent"]
        assert sent <= 100, (
            f"email_sent={sent}/hour can exceed the SES sandbox's 200/day. "
            "Raise it only together with SES production access."
        )


class TestRedirectAllowlist:
    """Supabase matches redirect_to exactly and silently falls back to Site URL
    when it is not listed — the #414 failure mode."""

    @pytest.mark.parametrize(
        "url",
        [
            "https://www.inno.day/ui/auth/callback",
            "https://www.inno.day/ui/invite/accept",
        ],
    )
    def test_current_ui_urls_are_allowlisted(self, auth, url):
        assert url in auth["additional_redirect_urls"]

    @pytest.mark.parametrize(
        "url",
        [
            "https://www.inno.day/auth/callback",
            "https://www.inno.day/invite/accept",
        ],
    )
    def test_legacy_urls_remain_allowlisted(self, auth, url):
        """Invite emails already delivered carry the pre-/ui paths."""
        assert url in auth["additional_redirect_urls"]

    def test_no_bare_apex_urls(self, auth):
        """The bare apex serves nothing: `https://inno.day/health` returns
        GoDaddy's 404 page, and no 301 to www is configured (#619). Supabase
        matches the URL it was given, so a bare-apex entry would send someone
        from their email to that error page."""
        bare = [
            u
            for u in auth["additional_redirect_urls"]
            if u.startswith("https://inno.day")
        ]
        assert not bare, f"bare-apex redirect URLs are never matched: {bare}"

    def test_site_url_uses_www(self, auth):
        assert auth["site_url"] == "https://www.inno.day"
