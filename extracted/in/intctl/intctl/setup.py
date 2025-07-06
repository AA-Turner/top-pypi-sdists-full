from setuptools import setup, find_packages

setup(
    name="intctl",
    version="0.1.0",
    description="Bootstrap CLI for provisioning cloud resources (GCP-first)",
    author="Your Name",
    author_email="you@example.com",
    packages=find_packages(),
    install_requires=[
        "typer[all]",
        "python-dotenv",
    ],
    entry_points={
        "console_scripts": [
            "intctl=intctl.cli:app",
        ],
    },
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
