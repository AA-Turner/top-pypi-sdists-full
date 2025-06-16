import pathlib

from setuptools import find_packages, setup

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="guardrails-hub-types",
    version="0.0.0",
    description="Guardrails Hub Types",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    python_requires=">=3.8, <4",
    install_requires=["python_dateutil >= 2.5.3", "setuptools >= 21.0.0", "urllib3 >= 1.25.3, < 2.1.0", "pydantic >= 2", "typing-extensions >= 4.7.1"],
    package_data={"guardrails_api_client": ["py.typed"]},
)
  