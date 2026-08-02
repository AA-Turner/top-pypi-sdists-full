# installation: pip install ago

from setuptools import setup, find_packages

setup(
    name="ago",
    version="0.1.1",
    description="ago: Human readable timedeltas",
    keywords="ago human readable time deltas timedelta datetime timestamp",
    long_description=open("README.rst").read(),
    author="Russell Ballestrini",
    author_email="russell.ballestrini@gmail.com",
    url="https://git.unturf.com/python/ago",
    packages=find_packages(exclude="tests"),
    platforms=["All"],
    license="Public Domain",
    py_modules=["ago"],
    include_package_data=True,
)

# ---------------------------------------------------------------------------
# Release process (automated via .gitlab-ci.yml on tag push)
# ---------------------------------------------------------------------------
#
# Cutting a release:
#   1. Bump `version=` above
#   2. git commit -m "X.Y.Z: <one-line summary>"
#   3. git tag -a X.Y.Z -m "X.Y.Z"
#   4. git push origin master X.Y.Z
#
# The CI pipeline builds (python -m build) and uploads (twine upload) on the
# tag push. No manual `python setup.py sdist && twine upload` needed.
#
# ---------------------------------------------------------------------------
# Maintainer setup (one-time, per project) — required for CI uploads to work
# ---------------------------------------------------------------------------
#
# git.unturf.com -> python/<this-project> -> Settings -> Repository ->
#   Protected Tags -> "Protect tag":
#     - Pattern:           *
#     - Allowed to Create: Maintainers (match erldistpy's setting)
#
# This makes tags Protected refs, which lets the Protected/Masked
# TWINE_USERNAME and TWINE_PASSWORD variables (set once at the python/
# group level) reach the tag pipeline. Without Protected Tags, twine 6
# falls through to OIDC trusted publishing and fails because PyPI's
# self-hosted GitLab support is hardcoded to gitlab.com.
#
# Group variables live at:
#   git.unturf.com -> python (group) -> Settings -> CI/CD -> Variables
#   TWINE_USERNAME = __token__
#   TWINE_PASSWORD = <pypi-AgEI...>   (Masked + Protected)
#
# setuptools keyword args: http://peak.telecommunity.com/DevCenter/setuptools
