import os

from setuptools import find_packages, setup

# Declare your non-python data files:
# Files underneath configuration/ will be copied into the build preserving the
# subdirectory structure if they exist.
data_files = []
for root, dirs, files in os.walk("configuration"):
    data_files.append(
        (os.path.relpath(root, "configuration"), [os.path.join(root, f) for f in files])
    )

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="aws-glue-sessions",
    version="1.0.9",
    description="Glue Interactive Sessions Jupyter kernel that integrates almost anywhere Jupyter does including your favorite IDEs.",
    url="https://aws.amazon.com/glue/",
    author="Glue Development Team",
    author_email="glue-sessions-preview@amazon.com",
    license="Apache 2.0 License",
    # declare your packages
    packages=find_packages(where="src", exclude=("test",)),
    package_dir={"": "src"},
    package_data={"": ["**/*.json", "**/*.sh", "**/*.png", "**/**/*.json"]},
    include_package_data=True,
    # include data files
    data_files=data_files,
    entry_points="""
        [console_scripts]
        install-glue-kernels = aws_glue_interactive_sessions_kernel.glue_kernel:install
    """,
    # Enable build-time format checking
    check_format=False,
    # Enable Wheel generation on brazil-build release
    require_wheel=True,
    # Enable type checking
    test_mypy=False,
    # Enable linting at build time
    test_flake8=False,
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        "autovizwidget>=0.6",
        "ipython>=4.0.2",
        "nose",
        "requests",
        "ipykernel>=6.12.1",
        "ipywidgets>5.0.0",
        "notebook>=4.2",
        "tornado>=4",
        "boto3>=1.21.31",
        "botocore>=1.24.24",
        "Click",
        "importlib_metadata>=4.11.3",
        "rich",
        "tabulate"
    ],
    license_files=['LICENSE']
)
