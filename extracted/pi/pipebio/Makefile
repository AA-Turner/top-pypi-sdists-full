.PHONY: unit-test integration-test docs llms llms-check

unit-test:
	pytest -v pytest tests/unit/

integration-test:
	pytest -v tests/integration/

# Generate the in-repo HTML API reference from docstrings + type hints.
# Output is git-ignored and not published; it exists for contributors and to
# catch docstring/signature breakage in CI. Requires the "docs" extra:
#   uv pip install ".[docs]"
docs:
	pdoc pipebio --no-show-source --docformat google -o docs/api

# Regenerate the bundled AI-context artifacts (pipebio/llms.txt + llms-full.txt).
llms:
	python scripts/generate_llms_txt.py

# Verify the committed AI-context artifacts are up to date (used in CI).
llms-check:
	python scripts/generate_llms_txt.py --check