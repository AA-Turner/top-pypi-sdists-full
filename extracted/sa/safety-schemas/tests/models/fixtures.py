import pytest

from safety_schemas.models import PythonSpecification
from safety_schemas.models import Vulnerability
from safety_schemas.models import PythonDependency


@pytest.fixture
def specification_factory():
    def _specification(name, vulnerabilities):
        return PythonSpecification(
            name=name,
            vulnerabilities=vulnerabilities,
        )

    return _specification


@pytest.fixture
def vulnerabilities_factory():
    def _vulnerabilities(ids, severities):
        return [
            Vulnerability(id=id, severity=severity)
            for id, severity in zip(ids, severities)
        ]

    return _vulnerabilities


@pytest.fixture
def dependencies_factory(specification_factory, vulnerabilities_factory):
    def _dependencies(pinned=True):
        dependencies = [
            PythonDependency(
                name="dependency1",
                version="1.0.0" if pinned else None,
                specifications=[
                    specification_factory(
                        name="spec1",
                        vulnerabilities=vulnerabilities_factory(
                            ids=["CVE-2021-1234", "CVE-2021-5678"],
                            severities=["High", "Medium"],
                        ),
                    ),
                    specification_factory(
                        name="spec2",
                        vulnerabilities=vulnerabilities_factory(
                            ids=["CVE-2021-9012"], severities=["Low"]
                        ),
                    ),
                ],
            ),
            PythonDependency(
                name="dependency2",
                version="2.0.0" if pinned else None,
                specifications=[
                    specification_factory(
                        name="spec3",
                        vulnerabilities=vulnerabilities_factory(
                            ids=["CVE-2021-3456"], severities=["Critical"]
                        ),
                    ),
                ],
            ),
        ]
        return dependencies

    return _dependencies
