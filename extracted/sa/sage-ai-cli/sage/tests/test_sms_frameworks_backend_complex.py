import pytest
from sage.tests.rubric_checker import verify_sms_with_rubric

FRAMEWORKS_BACKEND_TASKS = [
    ("PY-FLK-01", "Build SaaS with Flask, SQLAlchemy, Celery, and ReportLab PDF for PY-FLK-01"),
    ("PY-DJ-02", "Django channels real-time websocket chat with Graphene GraphQL for PY-DJ-02"),
    ("JS-EXP-03", "Express PKCE OAuth2 auth server with RS256 JWT for JS-EXP-03"),
    ("JS-NXT-04", "NestJS BullMQ order payment queues with Prisma for JS-NXT-04"),
    ("JAVA-SPR-05", "Spring Boot 3 Micrometer actuator metrics service for JAVA-SPR-05"),
    ("GO-GIN-06", "Gin TimescaleDB OpenTelemetry trace endpoint for GO-GIN-06"),
    ("RS-ACT-07", "Rust Actix Diesel URL shortener service for RS-ACT-07"),
    ("CPP-POCO-08", "C++ POCO REST file store with ClamAV scan for CPP-POCO-08"),
    ("PHP-LAR-09", "Laravel Livewire multi-step Redis form wizard for PHP-LAR-09"),
    ("RUB-RAI-10", "Rails Hotwire ActionCable collaborate markdown editor for RUB-RAI-10")
]
@pytest.mark.parametrize("task_id, prompt", FRAMEWORKS_BACKEND_TASKS)
def test_frameworks_backend_sms(task_id, prompt, tmp_path):
    """Verify complex backend web framework tasks via SMS."""
    verify_sms_with_rubric(prompt, tmp_path)
