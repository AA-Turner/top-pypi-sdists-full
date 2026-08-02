# Clean old builds
rm -rf ./build ./dist ./pipebio.egg-info

# First make sure uv is installed
if ! command -v uv &> /dev/null; then
    echo "Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
fi

# Install publish dependency
uv pip install twine

# Build with pyproject.toml (preferred over setup.py)
uv build

# pypi.org - used only for testing packaging/distribution.
# Requires an entry in you .pypirc that matches "pypi" - see https://packaging.python.org/en/latest/specifications/pypirc/
# To install from here use `uv pip install -i https://pypi.org/simple/ pipebio`.
twine upload -r pypi dist/*
# twine upload --repository-url https://pypi.org/legacy/ dist/* - will ask for creds on command line.
