from setuptools import setup, find_packages

setup(
    name         = "sourcemeta_jsonschema",
    version      = "16.2.0",
    description  = "The CLI for working with JSON Schema. Covers formatting, linting, testing, and much more for both local development and CI/CD pipelines. By a member of the JSON Schema Technical Steering Committee",
    author       = "Sourcemeta",
    author_email = "hello@sourcemeta.com",
    url          = "https://github.com/sourcemeta/jsonschema",
    license      = "AGPL-3.0",
    packages     = find_packages(),
    include_package_data = True,
    package_data = {
        "sourcemeta_jsonschema": ["*.exe", "jsonschema-*"]
    },
    python_requires = ">=3.7",
    entry_points = {
        "console_scripts": [
            "jsonschema = sourcemeta_jsonschema.__main__:main"
        ]
    }
)
