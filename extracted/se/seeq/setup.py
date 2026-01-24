from __future__ import annotations

import setuptools

# Metadata is defined in pyproject.toml [project] section to prevent Dynamic fields
# This setup.py only handles package discovery and build configuration
# When pyproject.toml [project] section exists, setuptools will use it instead of setup.py metadata
setuptools.setup(
    packages=setuptools.find_namespace_packages(include=['seeq.sdk', 'seeq.sdk.*']),
    include_package_data=True,
    zip_safe=False,
    # A bug exists in setuptools where `license-files` is incorrectly marked as dynamic. Rely on `license` in
    # pyproject.toml until https://github.com/pypa/setuptools/issues/4960 is fixed.
    license_files=[],
)
