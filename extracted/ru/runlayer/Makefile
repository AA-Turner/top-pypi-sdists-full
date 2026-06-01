.PHONY: build clean test-release release install-test version-bump test test-e2e typecheck lint lint-fix format check check-fix package-aiwatch-binary package-aiwatch-macos package-aiwatch-windows package-aiwatch-py2exe package-enforce-binary package-enforce-macos package-enforce-windows


clean:
	rm -rf dist/ build/ *.egg-info

build: clean
	uv build

test-release: build
	@echo "Publishing to Test PyPI..."
	uv publish --index testpypi

release: build
	@echo "Publishing to Production PyPI..."
	uv publish

install-test:
	uvx --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ runlayer

version-bump:
	@if [ -z "$(VERSION)" ]; then \
		echo "Error: VERSION not specified. Usage: make version-bump VERSION=0.1.1"; \
		exit 1; \
	fi
	uv version $(VERSION)

test:
	uv run pytest

test-e2e:
	uv run pytest tests/e2e -m e2e -v --tb=short -n auto

typecheck:
	uv run ty check runlayer_cli

lint:
	uv run ruff check runlayer_cli
	uv run ruff format runlayer_cli --check

format:
	uv run ruff format runlayer_cli

lint-fix:
	uv run ruff check runlayer_cli --fix
	uv run ruff format runlayer_cli

check: lint typecheck
check-fix: lint-fix typecheck

# --- AI Watch packaging ---
#
# macOS .pkgs are built natively per-arch (arm64 on Apple Silicon, x86_64 on
# Intel). CI ships both via the matrix in .github/workflows/release-aiwatch.yml.
# Local `make package-aiwatch-macos` produces a .pkg for the host arch only.

package-aiwatch-binary:
	uv pip install pyinstaller
	uv run pyinstaller packaging/aiwatch.spec

package-aiwatch-macos: package-aiwatch-binary
	./packaging/macos/build_pkg.sh

package-aiwatch-windows:
	uv pip install pyinstaller
	uv run pyinstaller packaging/aiwatch.spec
	powershell -ExecutionPolicy Bypass -File packaging\windows\build_msi.ps1
	powershell -ExecutionPolicy Bypass -File packaging\windows\build_intunewin.ps1

package-aiwatch-py2exe:
	uv pip install py2exe
	uv run python packaging/py2exe/setup_py2exe.py py2exe

# --- aiwatch-enforce (hook binary) packaging ---

package-enforce-binary:
	uv pip install pyinstaller
	uv run pyinstaller packaging/aiwatch-enforce.spec

package-enforce-macos: package-enforce-binary
	./packaging/aiwatch-enforce-macos/build_pkg.sh

package-enforce-windows:
	uv pip install pyinstaller
	uv run pyinstaller packaging/aiwatch-enforce.spec
	powershell -ExecutionPolicy Bypass -File packaging\windows\build_enforce_msi.ps1
	powershell -ExecutionPolicy Bypass -File packaging\windows\build_enforce_intunewin.ps1