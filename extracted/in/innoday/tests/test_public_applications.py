"""`POST /api/v1/public/applications` — job applications from the public site.

The route is unauthenticated and takes a file, so the tests that matter are the
ones about what it refuses: a second application from an address already on
file, a resume that is too large or the wrong kind, and a message outside the
length the form asks for.

The refusal on a duplicate is the point of this table existing. Applications
used to go into a table shared with pixelfuel.io that upserted on the address
alone, so a second application replaced the first and said nothing. Here it is
a 409 in words the applicant can act on.
"""

import base64
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, select

import src.routers.public as public_router
from src.api.app import app
from src.database import get_session
from src.domain.hs_job_application import HSJobApplication
from tests.db_helpers import build_test_engine

PDF = "application/pdf"


@pytest.fixture(autouse=True)
def clear_limiter():
    # Module-level and per-address; a test that inherits another's hits fails
    # for the wrong reason.
    public_router._application_hits = {}
    yield
    public_router._application_hits = {}


@pytest.fixture
def db_engine():
    return build_test_engine()


@pytest.fixture
def db_session(db_engine):
    with Session(db_engine) as session:
        yield session


@pytest.fixture
def client(db_engine):
    def override_get_session():
        with Session(db_engine) as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session
    with patch("src.api.app._assert_schema_at_head"):
        with TestClient(app) as c:
            yield c
    app.dependency_overrides.clear()


def application(**overrides):
    """A complete, valid application. Overrides replace one field at a time."""
    body = {
        "name": "A Person",
        "email": "a.person@example.com",
        "job_role": "software_developer",
        "highest_degree": "bachelors",
        "years_experience": "professional",
        "about_message": "I have built things for a decade and want to build the "
        "next one here, with people who care about the same details. " + "x" * 40,
        "technologies": ["TypeScript", "Postgres"],
        "proficiency_order": ["TypeScript", "Postgres"],
        "github_url": "https://github.com/aperson",
        "linkedin_url": "",
        "resume_filename": "cv.pdf",
        "resume_content_type": PDF,
        "resume_base64": base64.b64encode(b"%PDF-1.4 a resume").decode(),
    }
    body.update(overrides)
    return body


def test_accepts_an_application_and_keeps_what_was_sent(client, db_session):
    response = client.post("/api/v1/public/applications", json=application())

    assert response.status_code == 201
    assert response.json()["status"] == "received"

    stored = db_session.exec(select(HSJobApplication)).one()
    assert stored.email == "a.person@example.com"
    assert stored.job_role == "software_developer"
    # The ranking is the field worth reading first, so it is stored as sent
    # rather than recomputed from the set.
    assert stored.proficiency_order == ["TypeScript", "Postgres"]
    assert stored.resume_bytes == b"%PDF-1.4 a resume"
    assert stored.status == "NEW"
    # An empty optional is stored as absent, not as an empty string.
    assert stored.linkedin_url is None


def test_lowercases_the_address_so_a_duplicate_cannot_hide_behind_case(
    client, db_session
):
    client.post(
        "/api/v1/public/applications", json=application(email="A.Person@Example.com")
    )

    stored = db_session.exec(select(HSJobApplication)).one()
    assert stored.email == "a.person@example.com"


def test_refuses_a_second_application_rather_than_replacing_the_first(
    client, db_session
):
    first = client.post("/api/v1/public/applications", json=application())
    assert first.status_code == 201

    second = client.post(
        "/api/v1/public/applications",
        json=application(name="Someone Else", about_message="y" * 200),
    )

    assert second.status_code == 409
    assert "already have an application" in second.json()["detail"]
    # And the first one is untouched, which is the whole reason for the refusal.
    stored = db_session.exec(select(HSJobApplication)).one()
    assert stored.name == "A Person"


@pytest.mark.parametrize(
    "field,value",
    [
        ("job_role", "chief_of_vibes"),
        ("highest_degree", "doctorate"),
        ("years_experience", "grizzled"),
        ("email", "not-an-address"),
        ("name", "   "),
    ],
)
def test_refuses_what_the_form_never_offers(client, field, value):
    response = client.post(
        "/api/v1/public/applications", json=application(**{field: value})
    )
    assert response.status_code == 400


@pytest.mark.parametrize("length", [99, 701])
def test_holds_the_message_to_the_length_the_form_asks_for(client, length):
    response = client.post(
        "/api/v1/public/applications", json=application(about_message="x" * length)
    )

    assert response.status_code == 400
    assert "characters" in response.json()["detail"]


def test_refuses_a_resume_over_five_megabytes(client):
    too_big = base64.b64encode(b"x" * (5 * 1024 * 1024 + 1)).decode()

    response = client.post(
        "/api/v1/public/applications", json=application(resume_base64=too_big)
    )

    assert response.status_code == 400
    assert "5MB" in response.json()["detail"]


def test_refuses_a_resume_that_is_not_a_document(client):
    response = client.post(
        "/api/v1/public/applications",
        json=application(resume_content_type="image/png"),
    )

    assert response.status_code == 400
    assert "PDF or a Word document" in response.json()["detail"]


def test_takes_an_application_with_no_resume_at_all(client, db_session):
    response = client.post(
        "/api/v1/public/applications",
        json=application(
            resume_base64=None, resume_content_type=None, resume_filename=None
        ),
    )

    assert response.status_code == 201
    assert db_session.exec(select(HSJobApplication)).one().resume_bytes is None


def test_stops_a_script_posting_the_same_form_over_and_over(client):
    # The site holds the signed token and the honeypot; this is the limit that
    # applies to anything posting straight at the endpoint.
    for i in range(3):
        sent = client.post(
            "/api/v1/public/applications",
            json=application(email=f"person{i}@example.com"),
        )
        assert sent.status_code == 201

    fourth = client.post(
        "/api/v1/public/applications", json=application(email="fourth@example.com")
    )

    assert fourth.status_code == 429


def test_counts_the_limit_per_address_not_across_everyone(client):
    for i in range(3):
        client.post(
            "/api/v1/public/applications",
            json=application(email=f"first{i}@example.com"),
        )

    # Somebody else, on a different connection, is unaffected.
    other = client.post(
        "/api/v1/public/applications",
        json=application(email="other@example.com"),
        headers={"x-forwarded-for": "203.0.113.9"},
    )

    assert other.status_code == 201
