from __future__ import annotations


def pytest_addoption(parser):
    parser.addoption(
        "--update-golden",
        action="store_true",
        default=False,
        help="Regenerate golden-output fixtures for intentional renderer changes.",
    )
