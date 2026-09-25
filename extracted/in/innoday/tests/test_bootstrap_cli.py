"""Operator bootstrap CLI: `python scripts/bootstrap_cli.py seed-user` (PF-350 §5.0).

Verifies the command creates a platform user, mints a working CLI token, is
idempotent (promotes rather than duplicating), and refuses to run without the
INNODAY_ALLOW_BOOTSTRAP opt-in. The module lives in scripts/ (source-only, not
packaged), so it's loaded by path.
"""

import importlib.util
from pathlib import Path

from sqlmodel import Session, select

from src.domain.cli_token import CLIToken, hash_cli_token
from src.domain.user import User
from tests.db_helpers import build_test_engine

_BOOTSTRAP_PATH = (
    Path(__file__).resolve().parent.parent / "scripts" / "bootstrap_cli.py"
)
_spec = importlib.util.spec_from_file_location("bootstrap_cli", _BOOTSTRAP_PATH)
bootstrap_cli = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(bootstrap_cli)


def _wire_engine(monkeypatch):
    """Point the bootstrap CLI at a fresh in-memory DB, enable the opt-in gate,
    and return that engine."""
    monkeypatch.setenv("INNODAY_ALLOW_BOOTSTRAP", "1")
    engine = build_test_engine()
    monkeypatch.setattr(bootstrap_cli, "engine", engine)
    return engine


def test_seed_user_creates_platform_user_and_token(monkeypatch, capsys):
    engine = _wire_engine(monkeypatch)

    rc = bootstrap_cli.main(["seed-user", "founder@hs.com", "--name", "Founder"])
    assert rc == 0

    out = capsys.readouterr().out
    assert "Created platform user founder@hs.com" in out
    # the raw token is printed exactly once and looks right (PAT + plat0 sentinel)
    assert "idt_plat0." in out

    with Session(engine) as s:
        user = s.exec(select(User).where(User.email == "founder@hs.com")).first()
        assert user is not None and user.is_platform_member is True
        # a valid token row exists for them
        tokens = s.exec(select(CLIToken).where(CLIToken.user_id == user.id)).all()
        assert len(tokens) == 1 and tokens[0].is_valid()


def test_seed_user_is_idempotent(monkeypatch, capsys):
    engine = _wire_engine(monkeypatch)

    bootstrap_cli.main(["seed-user", "dev@hs.com"])
    capsys.readouterr()  # clear
    rc = bootstrap_cli.main(["seed-user", "dev@hs.com"])
    assert rc == 0
    assert "Promoted existing user" in capsys.readouterr().out

    with Session(engine) as s:
        users = s.exec(select(User).where(User.email == "dev@hs.com")).all()
        assert len(users) == 1  # not duplicated


def test_minted_token_hash_is_stored_not_raw(monkeypatch, capsys):
    engine = _wire_engine(monkeypatch)
    bootstrap_cli.main(["seed-user", "sec@hs.com"])
    out = capsys.readouterr().out
    raw = next(
        line.strip() for line in out.splitlines() if line.strip().startswith("idt_")
    )
    with Session(engine) as s:
        tok = s.exec(select(CLIToken)).first()
        # only the hash is persisted, never the raw token
        assert tok.token_hash == hash_cli_token(raw)
        assert tok.token_hash != raw


def test_refuses_without_optin_flag(monkeypatch, capsys):
    """Without INNODAY_ALLOW_BOOTSTRAP the command refuses (exit 2) and seeds
    nothing, even with a valid DB."""
    engine = build_test_engine()
    monkeypatch.setattr(bootstrap_cli, "engine", engine)
    monkeypatch.delenv("INNODAY_ALLOW_BOOTSTRAP", raising=False)

    rc = bootstrap_cli.main(["seed-user", "nope@hs.com"])
    assert rc == 2
    with Session(engine) as s:
        assert s.exec(select(User).where(User.email == "nope@hs.com")).first() is None


def _seed_tier(engine):
    from uuid import uuid4

    from src.domain.license import LicenseTier
    from src.utils.license_utils import TOP_LICENSE_TIER_NAME

    with Session(engine) as s:
        s.add(
            LicenseTier(id=str(uuid4()), name=TOP_LICENSE_TIER_NAME, display_name="T")
        )
        s.commit()


def test_create_org_makes_the_owner_its_admin(monkeypatch, capsys):
    """Creating an organization moved here from the CLI and MCP (PF-457)."""
    from src.domain.organization import Organization, OrganizationMembership

    engine = _wire_engine(monkeypatch)
    _seed_tier(engine)
    bootstrap_cli.main(["seed-user", "owner@example.com"])

    rc = bootstrap_cli.main(
        ["create-org", "Acme Corp", "--alias", "acme", "--owner", "owner@example.com"]
    )

    assert rc == 0
    assert "acme" in capsys.readouterr().out
    with Session(engine) as s:
        org = s.exec(select(Organization).where(Organization.alias == "acme")).one()
        owner = s.exec(select(User).where(User.email == "owner@example.com")).one()
        membership = s.exec(
            select(OrganizationMembership).where(
                OrganizationMembership.organization_id == org.id
            )
        ).one()
        assert membership.user_id == owner.id and membership.is_owner


def test_create_org_needs_an_existing_owner(monkeypatch, capsys):
    engine = _wire_engine(monkeypatch)
    _seed_tier(engine)

    rc = bootstrap_cli.main(["create-org", "Acme", "--owner", "nobody@example.com"])

    assert rc == 1
    assert "seed-user" in capsys.readouterr().err


def test_create_org_refuses_a_taken_alias(monkeypatch, capsys):
    engine = _wire_engine(monkeypatch)
    _seed_tier(engine)
    bootstrap_cli.main(["seed-user", "owner@example.com"])
    bootstrap_cli.main(
        ["create-org", "A", "--alias", "acme", "--owner", "owner@example.com"]
    )

    rc = bootstrap_cli.main(
        ["create-org", "B", "--alias", "acme", "--owner", "owner@example.com"]
    )

    assert rc == 1
    assert "acme" in capsys.readouterr().err


def test_create_org_lowercases_the_alias(monkeypatch, capsys):
    """Lookups match aliases exactly and every other path stores them
    lowercase, so `Acme` would be unfindable by `innoday orgs env-setup Acme`."""
    from src.domain.organization import Organization

    engine = _wire_engine(monkeypatch)
    _seed_tier(engine)
    bootstrap_cli.main(["seed-user", "owner@example.com"])

    rc = bootstrap_cli.main(
        ["create-org", "Acme", "--alias", "Acme", "--owner", "owner@example.com"]
    )

    assert rc == 0
    with Session(engine) as s:
        assert s.exec(select(Organization).where(Organization.alias == "acme")).one()


def test_create_org_applies_the_api_length_limits(monkeypatch, capsys):
    engine = _wire_engine(monkeypatch)
    _seed_tier(engine)
    bootstrap_cli.main(["seed-user", "owner@example.com"])

    rc = bootstrap_cli.main(
        ["create-org", "A", "--alias", "x" * 51, "--owner", "owner@example.com"]
    )

    assert rc == 1
