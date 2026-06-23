import os
import sys

from setuptools import setup, find_packages
from setuptools.command.build_py import build_py


class BuildPyWithRegions(build_py):
    """Fetch latest regions.json from Contentstack CDN before packaging."""

    def run(self):
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        try:
            from contentstack_utils.region_refresh import refresh_regions
            refresh_regions()
        except Exception as exc:
            # Never block a build over a network failure — warn and continue.
            print(f"WARNING: Could not refresh regions.json: {exc}", file=sys.stderr)
        super().run()


with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    long_description = readme.read()

setup(
    name='contentstack_utils',
    packages=find_packages(),
    package_data={
        "contentstack_utils": ["assets/regions.json"],
    },
    description="contentstack_utils is a Utility package for Contentstack headless CMS with an API-first approach.",
    author='contentstack',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/contentstack/contentstack-utils-python",
    license='MIT',
    version='1.6.0',
    install_requires=[

    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
    cmdclass={"build_py": BuildPyWithRegions},
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires='>=3.6',
)
