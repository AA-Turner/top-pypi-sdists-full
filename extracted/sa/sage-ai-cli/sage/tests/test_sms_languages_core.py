import pytest
from sage.tests.rubric_checker import verify_sms_with_rubric

LANGUAGES_CORE_TASKS = [
    ("PY-001", "Write a type-checked async data-pipeline that reads CSV, validates with Pydantic for PY-001"),
    ("JS-002", "Build a CQRS order micro-service for JS-002"),
    ("JAVA-003", "Implement lock-free concurrent hash map JPMS library for JAVA-003"),
    ("GO-004", "Create HTTP/2 autocert REST server for GO-004"),
    ("RS-005", "Write no-std embedded sensor driver for RS-005"),
    ("CPP-006", "Build cross-platform plugin loader for CPP-006"),
    ("TS-007", "Write compile-time type-level math parser for TS-007"),
    ("PHP-008", "Create PSR-15 Redis rate limiting middleware for PHP-008"),
    ("RUB-009", "Build multi-tenant Rails engine with Apartment and Sidekiq for RUB-009"),
    ("SWIFT-010", "Write Combine-based networking layer with CoreData cache for SWIFT-010"),
    ("CRYSTAL-011", "Implement fiber pool channel system in Crystal for CRYSTAL-011"),
    ("LARGE-001", "Build a massive monorepo with 400+ micro-services and libraries for LARGE-001"),
    ("EXTREME-002", "Generate a complete enterprise-grade system with over 1000 source files for EXTREME-002")
]
@pytest.mark.parametrize("task_id, prompt", LANGUAGES_CORE_TASKS)
def test_languages_core_sms(task_id, prompt, tmp_path):
    """Verify core programming language tasks via SMS."""
    verify_sms_with_rubric(prompt, tmp_path)
