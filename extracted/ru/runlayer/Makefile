.PHONY: build clean test-release release install-test version-bump test test-e2e test-install-scripts typecheck lint lint-fix format regex-engine check check-fix package-aiwatch-binary package-aiwatch-hook-macos package-aiwatch-hook-windows package-aiwatch-hook-linux package-aiwatch-macos package-aiwatch-windows package-aiwatch-py2exe package-cli-binary package-cli-macos package-cli-windows package-cli-linux package-aiwatch-linux package-desktop-macos package-desktop-windows


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
	@if [ -z "$(VERSION)" ] && [ -z "$(BUMP)" ]; then \
		echo "Error: specify VERSION or BUMP. Usage: make version-bump VERSION=0.1.1  |  make version-bump BUMP=patch|minor|major"; \
		exit 1; \
	fi
	@if [ -n "$(VERSION)" ]; then \
		uv version "$(VERSION)"; \
	else \
		uv version --bump "$(BUMP)"; \
	fi

test:
	uv run pytest

test-e2e:
	uv run pytest tests/e2e -m e2e -v --tb=short -n auto

test-install-scripts:
	shellcheck packaging/install/install.sh packaging/install/tests/test_install_sh.sh
	bash packaging/install/tests/test_install_sh.sh
	pwsh -NoProfile -Command '$$results = Invoke-ScriptAnalyzer -Path "packaging/install/install.ps1" -Severity Warning,Error; if ($$results) { $$results | Format-Table -AutoSize; exit 1 }'
	pwsh -NoProfile -File packaging/install/tests/Invoke-Tests.ps1

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

regex-engine:
	uv run python scripts/check_regex_engine.py

check: lint typecheck regex-engine
check-fix: lint-fix typecheck regex-engine

# --- AI Watch packaging (single onedir: `aiwatch` EXE + native `aiwatch-hook`) ---
# Local builds produce host-arch only; CI matrix in release-aiwatch.yml ships both arches.
# The PyInstaller freeze replaces dist/aiwatch wholesale, so the Go shim is always
# built after it and before the platform packaging step.

AIWATCH_VERSION = $(shell grep -E '^version = ' pyproject.toml | head -1 | cut -d'"' -f2)
HOOK_SHIM_DIR = ../aiwatch-hook-shim

package-aiwatch-binary:
	uv pip install pyinstaller
	uv run pyinstaller --noconfirm packaging/aiwatch.spec

# macOS ships one universal2 shim so client hook configs are arch-neutral, even
# though the PyInstaller executable stays host-arch.
package-aiwatch-hook-macos: package-aiwatch-binary
	SHIM_TMP="$$(mktemp -d)" && \
		(cd $(HOOK_SHIM_DIR) && \
			CGO_ENABLED=0 GOOS=darwin GOARCH=arm64 go build -trimpath \
				-ldflags "-X main.version=$(AIWATCH_VERSION)" \
				-o "$$SHIM_TMP/arm64" ./cmd/aiwatch-hook && \
			CGO_ENABLED=0 GOOS=darwin GOARCH=amd64 go build -trimpath \
				-ldflags "-X main.version=$(AIWATCH_VERSION)" \
				-o "$$SHIM_TMP/amd64" ./cmd/aiwatch-hook) && \
		lipo -create "$$SHIM_TMP/arm64" "$$SHIM_TMP/amd64" \
			-output dist/aiwatch/aiwatch-hook && \
		chmod +x dist/aiwatch/aiwatch-hook && \
		rm -rf "$$SHIM_TMP"

package-aiwatch-hook-linux: package-aiwatch-binary
	cd $(HOOK_SHIM_DIR) && CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -trimpath \
		-ldflags "-X main.version=$(AIWATCH_VERSION)" \
		-o ../cli/dist/aiwatch/aiwatch-hook ./cmd/aiwatch-hook

# PowerShell so the recipe works whether make's shell is cmd.exe or a bash port.
package-aiwatch-hook-windows: package-aiwatch-binary
	powershell -ExecutionPolicy Bypass -File packaging\windows\build_hook_shim.ps1

package-aiwatch-macos: package-aiwatch-hook-macos
	./packaging/macos/build_pkg.sh

package-aiwatch-windows: package-aiwatch-hook-windows
	powershell -ExecutionPolicy Bypass -File packaging\windows\build_msi.ps1
	powershell -ExecutionPolicy Bypass -File packaging\windows\build_intunewin.ps1

package-aiwatch-linux: package-aiwatch-hook-linux
	./packaging/linux/build_aiwatch_packages.sh

package-aiwatch-py2exe:
	uv pip install py2exe
	uv run python packaging/py2exe/setup_py2exe.py py2exe

# --- Full Runlayer CLI packaging (single onedir, one `runlayer` EXE) ---
# Local builds produce host-arch only; CI matrix in release-runlayer-cli.yml
# ships macOS arm64+x86_64, Windows x64, and Linux x86_64.

package-cli-binary:
	uv pip install pyinstaller
	uv run pyinstaller --noconfirm packaging/runlayer.spec

package-cli-macos: package-cli-binary
	./packaging/macos/build_pkg_runlayer.sh

package-cli-windows:
	uv pip install pyinstaller
	uv run pyinstaller --noconfirm packaging/runlayer.spec
	powershell -ExecutionPolicy Bypass -File packaging\windows\build_msi_runlayer.ps1
	powershell -ExecutionPolicy Bypass -File packaging\windows\build_intunewin_runlayer.ps1

package-cli-linux: package-cli-binary
	./packaging/linux/build_packages.sh

# --- Runlayer desktop packaging (full CLI + native tray, no Linux variant) ---

package-desktop-macos: package-cli-binary
	../desktop/macos/build-app.sh
	INCLUDE_DESKTOP=1 ./packaging/macos/build_pkg_runlayer.sh

package-desktop-windows:
	uv pip install pyinstaller
	uv run pyinstaller --noconfirm packaging/runlayer.spec
	powershell -ExecutionPolicy Bypass -File ..\desktop\windows\build.ps1
	powershell -ExecutionPolicy Bypass -File packaging\windows\build_msi_runlayer.ps1 -IncludeDesktop
	powershell -ExecutionPolicy Bypass -File packaging\windows\build_intunewin_runlayer.ps1 -IncludeDesktop