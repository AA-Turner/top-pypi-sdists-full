from powerfx._loader import load


def pytest_sessionstart(session):
    """Ensure Microsoft.PowerFx assemblies are loaded before any test imports."""
    load()
