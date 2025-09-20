import pathlib

from setuptools import find_packages, setup

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="guardrails-api-client",
    description="Guardrails API Client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    python_requires=">=3.8, <4",
    install_requires=["urllib3 >= 2.1.0, < 3.0.0", "python_dateutil >= 2.8.2", "pydantic >= 2", "typing-extensions >= 4.7.1", "lazy-imports >= 1, < 2"],
    package_data={"guardrails_api_client": ["py.typed", "openapi-spec.json"]},
)
  