from __future__ import annotations

import setuptools
from setuptools.command.sdist import sdist as _sdist

class CustomSdistCommand(_sdist):
    def make_distribution(self):
        # CRAB-45784: PEP 625 no longer allows distributions (the .tar.gz file) to include non-normalized chars
        # ('-' in this case) in the file name. Replace the name with an underscore only for the distribution without
        # altering SPy's package name.
        # TODO CRAB-35238: This can be removed when setuptools is upgraded to v69.3.0 or later.
        self.distribution.metadata.name = self.distribution.metadata.name.replace("-", "_")
        super().make_distribution()

# Metadata is defined in pyproject.toml [project] section to prevent Dynamic fields
# This setup.py only handles package discovery, build configuration, and custom commands
# When pyproject.toml [project] section exists, setuptools will use it instead of setup.py metadata
setuptools.setup(
    packages=setuptools.find_namespace_packages(exclude=['seeq.sdk', 'seeq.sdk.*']),
    include_package_data=True,
    zip_safe=False,
    # A bug exists in setuptools where `license-files` is incorrectly marked as dynamic. Rely on `license` in
    # pyproject.toml until https://github.com/pypa/setuptools/issues/4960 is fixed.
    license_files=[],
    cmdclass={"sdist": CustomSdistCommand},
)
