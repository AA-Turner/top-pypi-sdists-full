
"""
Module to expose more detailed version info for the installed `scipy`
"""
version = "1.12.1"
full_version = version
short_version = version.split('.dev')[0]
git_revision = "e78ed281628438c1bfa275b8d6c6b69c0f5f1d92"
release = 'dev' not in version and '+' not in version

if not release:
    version = full_version
