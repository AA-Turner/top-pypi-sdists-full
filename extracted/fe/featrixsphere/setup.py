#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
#
#  Copyright (c) 2023-2026 Featrix, Inc, All Rights Reserved
#
#  Proprietary and Confidential.  Unauthorized use, copying or dissemination
#  of these materials is strictly prohibited.
#

"""
Setup script for featrixsphere package
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

# Read version from __init__.py
def get_version():
    version_file = this_directory / "featrixsphere" / "__init__.py"
    if version_file.exists():
        for line in version_file.read_text().splitlines():
            if line.startswith("__version__"):
                return line.split('"')[1]
    return "0.1.0"

setup(
    name="featrixsphere",
    version=get_version(),
    author="Featrix",
    author_email="support@featrix.com",
    description="Transform any CSV into a production-ready ML model in minutes, not months.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Featrix/sphere",
    project_urls={
        "Bug Tracker": "https://github.com/Featrix/sphere/issues",
        "Documentation": "https://github.com/Featrix/sphere#readme",
        "Source Code": "https://github.com/Featrix/sphere",
    },
    packages=find_packages(include=['featrixsphere', 'featrixsphere.*']),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.20.0",  # HTTP API calls
        "pandas>=1.0.0",     # CSV operations - core functionality
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.800",
        ],
        "progress": [
            "rich>=10.0.0",  # Beautiful progress bars and terminal output
        ],
        "notebook": [
            "ipython>=7.0.0",  # Jupyter notebook support for enhanced displays
            "ipywidgets>=7.0.0",  # Interactive widgets for 3D plot exploration
        ],
        "interactive": [
            "ipywidgets>=7.0.0",  # Interactive 3D plot controls
            "matplotlib>=3.0.0",  # 3D plotting with widgets
        ],
        "server": [
            "fastapi>=0.68.0",     # API framework
            "uvicorn[standard]>=0.15.0",  # ASGI server
            "celery[redis]>=5.0.0",  # Async task queue with Redis
            "redis>=4.0.0",        # Redis client
            "pydantic-settings>=2.0.0",  # Settings management
            "python-multipart>=0.0.5",  # File upload support
        ],
        "ml": [
            "torch>=1.9.0",        # PyTorch for ML models
            "numpy>=1.21.0",       # Numerical computing
            "scikit-learn>=1.0.0", # Traditional ML algorithms
            "pandas>=1.3.0",       # Enhanced pandas for ML
        ],
        "all": [
            "rich>=10.0.0",
            "ipython>=7.0.0", 
            "ipywidgets>=7.0.0",
            "fastapi>=0.68.0",
            "uvicorn[standard]>=0.15.0",
            "celery[redis]>=5.0.0",
            "redis>=4.0.0",
            "pydantic-settings>=2.0.0",
            "python-multipart>=0.0.5",
            "torch>=1.9.0",
            "numpy>=1.21.0",
            "scikit-learn>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "featrix=featrixsphere.cli:main",
        ],
    },
    keywords=[
        "machine learning",
        "artificial intelligence", 
        "neural networks",
        "embedding spaces",
        "prediction",
        "classification",
        "regression",
        "csv",
        "api",
        "client",
        "featrix",
        "sphere",
        "automl",
        "no-code ml",
    ],
    include_package_data=True,
    zip_safe=False,
) 