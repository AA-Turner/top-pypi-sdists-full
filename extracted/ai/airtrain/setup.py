from setuptools import setup, find_packages  # type: ignore
import os
import sys
import re
from setuptools.command.install import install


# Read version from __init__.py
def get_version():
    init_path = os.path.join(os.path.dirname(__file__), "airtrain", "__init__.py")
    with open(init_path, "r", encoding="utf-8") as f:
        version_file = f.read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


def get_changelog() -> str:
    """Read the changelog content from absolute path."""
    # Get the absolute path to the setup.py directory
    setup_dir = os.path.dirname(os.path.abspath(__file__))
    changelog_path = os.path.abspath(os.path.join(setup_dir, "changelog.md"))

    with open(changelog_path, "r", encoding="utf-8") as f:
        # Skip the frontmatter and title
        lines = f.readlines()
        changelog_content = []
        skip_frontmatter = False
        for line in lines:
            if line.strip() == "---":
                skip_frontmatter = not skip_frontmatter
                continue
            if not skip_frontmatter and not line.startswith("# Changelog"):
                changelog_content.append(line)
    return "".join(changelog_content)


# Custom install command that sends telemetry
class CustomInstallCommand(install):
    def run(self):
        # Run the standard install
        install.run(self)
        
        # Try to send telemetry after installation
        try:
            # We need to import here to avoid import errors
            # before the package is installed
            sys.path.insert(0, self.install_lib)
            try:
                from airtrain.telemetry import telemetry, PackageInstallTelemetryEvent
                
                # Get the version we just installed
                version = get_version()
                
                # Send telemetry
                telemetry.capture(
                    PackageInstallTelemetryEvent(
                        version=version,
                        python_version=(
                            f"{sys.version_info.major}."
                            f"{sys.version_info.minor}."
                            f"{sys.version_info.micro}"
                        ),
                        install_method="pip" if "pip" in sys.argv else "unknown"
                    )
                )
            except ImportError:
                # The package is not fully installed yet
                pass
        except Exception:
            # Don't let telemetry failures interfere with installation
            pass


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Combine README and Changelog
full_description = f"{long_description}\n\n## Changelog\n{get_changelog()}"

setup(
    name="airtrain",
    version=get_version(),
    author="Dheeraj Pai",
    author_email="helloworldcmu@gmail.com",
    description="A platform for building and deploying AI agents with structured skills",
    long_description=full_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rosaboyle/airtrain.dev",
    packages=find_packages(include=["airtrain", "airtrain.*"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pydantic>=2.10.6",
        "openai>=1.60.1",
        "python-dotenv>=1.0.1",
        "PyYAML>=6.0.2",
        "firebase-admin>=6.6.0",  # Optional, only if using Firebase
        "loguru>=0.7.3",  # For logging
        "requests>=2.32.3",
        "boto3>=1.36.6",  # For AWS services
        "together>=1.3.13",  # For Together AI integration
        "anthropic>=0.45.0",  # For Anthropic AI integration
        "groq>=0.15.0",  # For Groq AI integration
        "cerebras-cloud-sdk>=1.19.0",
        "google-genai>=1.0.0",
        "fireworks-ai>=0.15.12",
        "google-generativeai>=0.8.4",
        "click>=8.0.0",  # For CLI support
        "rich>=13.3.1",  # For beautiful terminal output
        "prompt-toolkit>=3.0.36",  # For interactive prompts
        "colorama>=0.4.6",  # For colored terminal text
        "typer>=0.9.0",  # For building CLI applications
        "posthog>=3.1.0",  # For anonymous telemetry
    ],
    extras_require={
        "dev": [
            "black>=24.10.0",
            "flake8>=7.1.1",
            "isort>=5.13.0",
            "mypy>=1.9.0",
            "pytest>=7.0.0",
            "twine>=4.0.0",
            "build>=0.10.0",
            "types-PyYAML>=6.0",
            "types-requests>=2.31.0",
            "types-Markdown>=3.5.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "airtrain=airtrain.cli.main:main",
        ],
    },
    cmdclass={
        'install': CustomInstallCommand,
    },
)
