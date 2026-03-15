
"""
Module to expose more detailed version info for the installed `scipy`
"""
version = "1.12.0"
full_version = version
short_version = version.split('.dev')[0]
git_revision = "b0377826eea2b557751b78ed13dc42e720d8a15e"
release = 'dev' not in version and '+' not in version

if not release:
    version = full_version
