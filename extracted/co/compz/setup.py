"""
Setup configuration for CompZ SDK.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="compz",
    version="1.0.0",
    author="CompliLedger",
    author_email="support@compliledger.com",
    description="Privacy-Preserving Compliance Attestation SDK with Zcash blockchain anchoring",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Compliledger/CompZ",
    project_urls={
        "Bug Tracker": "https://github.com/Compliledger/CompZ/issues",
        "Documentation": "https://github.com/Compliledger/CompZ/blob/main/README.md",
        "Source Code": "https://github.com/Compliledger/CompZ",
    },
    packages=find_packages(exclude=["tests", "tests.*"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Security",
        "Topic :: System :: Systems Administration",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    install_requires=[
        "pydantic>=2.0.0",
        "requests>=2.31.0",
        "typer>=0.9.0",
        "rich>=13.0.0",
        "python-dotenv>=1.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
        "gateway": [
            "fastapi>=0.104.0",
            "uvicorn[standard]>=0.24.0",
            "slowapi>=0.1.9",
            "redis>=5.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "compz=compz.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords=[
        "compliance",
        "attestation",
        "blockchain",
        "zcash",
        "privacy",
        "security",
        "audit",
        "devsecops",
        "pci-dss",
        "soc2",
        "fedramp",
    ],
)
