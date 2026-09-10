"""Check the CLI's transport imports/call keywords against its pinned PyPI SDK.

The editable SDK used in CI can hide unpublished APIs. Read the published wheel
as data, verifying its PyPI SHA256, without installing or executing its code.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import io
import json
import sys
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path

CLI_ROOT = Path(__file__).resolve().parents[1]
TRANSPORT_MODULE = "runlayer_sdk.hook_transport"
MAX_DOWNLOAD_BYTES = 10 * 1024 * 1024


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def download(url: str) -> bytes:
    parsed = urllib.parse.urlsplit(url)
    if parsed.scheme != "https" or parsed.netloc not in {
        "pypi.org",
        "files.pythonhosted.org",
    }:
        raise ValueError(f"Unexpected PyPI URL: {url}")
    with urllib.request.build_opener(NoRedirect).open(url, timeout=30) as response:
        content = response.read(MAX_DOWNLOAD_BYTES + 1)
    if len(content) > MAX_DOWNLOAD_BYTES:
        raise ValueError("PyPI response exceeds 10 MiB")
    return content


def published_wheel(version: str) -> bytes:
    metadata = json.loads(
        download(f"https://pypi.org/pypi/runlayer-hooks-sdk/{version}/json")
    )
    wheels = [
        entry
        for entry in metadata["urls"]
        if entry["packagetype"] == "bdist_wheel"
        and entry["filename"].endswith("-py3-none-any.whl")
        and not entry.get("yanked", False)
    ]
    if len(wheels) != 1:
        raise ValueError(f"Expected one non-yanked universal SDK {version} wheel")
    wheel = download(wheels[0]["url"])
    if hashlib.sha256(wheel).hexdigest() != wheels[0]["digests"]["sha256"]:
        raise ValueError("Published SDK wheel SHA256 mismatch")
    return wheel


def check_transport(cli_source: Path, sdk_source: str) -> None:
    required_names: set[str] = set()
    required_keywords: set[str] = set()
    for path in cli_source.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        encoders = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module == TRANSPORT_MODULE:
                for alias in node.names:
                    required_names.add(alias.name)
                    if alias.name == "encode_wire_body":
                        encoders.add(alias.asname or alias.name)
        for node in ast.walk(tree):
            if (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Name)
                and node.func.id in encoders
            ):
                for keyword in node.keywords:
                    if keyword.arg is None:
                        raise ValueError(
                            f"Cannot statically check encoder **kwargs in {path}"
                        )
                    required_keywords.add(keyword.arg)

    if not required_names:
        raise ValueError("No CLI transport imports found")

    sdk = ast.parse(sdk_source, filename="published runlayer_sdk/hook_transport.py")
    symbols: set[str] = set()
    encoder = None
    for node in sdk.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            symbols.add(node.name)
            if isinstance(node, ast.FunctionDef) and node.name == "encode_wire_body":
                encoder = node
        elif isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            symbols.update(
                target.id
                for value in targets
                for target in ast.walk(value)
                if isinstance(target, ast.Name) and isinstance(target.ctx, ast.Store)
            )
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            symbols.update(
                alias.asname or alias.name.split(".")[0] for alias in node.names
            )

    problems = []
    if missing := required_names - symbols:
        problems.append(f"missing transport exports: {', '.join(sorted(missing))}")
    if encoder is None:
        problems.append("missing encode_wire_body function")
    elif encoder.args.kwarg is None:
        accepted = {arg.arg for arg in encoder.args.args + encoder.args.kwonlyargs}
        if unsupported := required_keywords - accepted:
            problems.append(
                f"encode_wire_body rejects CLI keywords: {', '.join(sorted(unsupported))}"
            )
    if problems:
        raise ValueError("; ".join(problems))


def main() -> int:
    # Import lazily so contract tests can use the CLI's minimum Python version.
    import tomllib

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--wheel", type=Path, help="local wheel for offline compatibility diagnostics"
    )
    args = parser.parse_args()
    try:
        manifest = tomllib.loads((CLI_ROOT / "pyproject.toml").read_text())
        pins = [
            dep.removeprefix("runlayer-hooks-sdk==")
            for dep in manifest["project"]["dependencies"]
            if dep.startswith("runlayer-hooks-sdk==")
        ]
        if len(pins) != 1 or not pins[0]:
            raise ValueError("CLI must pin exactly one runlayer-hooks-sdk version")
        wheel = args.wheel.read_bytes() if args.wheel else published_wheel(pins[0])
        with zipfile.ZipFile(io.BytesIO(wheel)) as archive:
            if (
                archive.getinfo("runlayer_sdk/hook_transport.py").file_size
                > MAX_DOWNLOAD_BYTES
            ):
                raise ValueError("SDK transport source exceeds 10 MiB")
            source = archive.read("runlayer_sdk/hook_transport.py").decode("utf-8")
        check_transport(CLI_ROOT / "runlayer_cli", source)
        label = str(args.wheel) if args.wheel else f"PyPI runlayer-hooks-sdk=={pins[0]}"
        print(f"Transport contract matches {label}")
        return 0
    except (OSError, ValueError, KeyError, SyntaxError, zipfile.BadZipFile) as error:
        print(f"Published SDK transport check failed: {error}", file=sys.stderr)
        print(
            "Publish a compatible Python SDK before merging/releasing its CLI pin; releases require a human.",
            file=sys.stderr,
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
