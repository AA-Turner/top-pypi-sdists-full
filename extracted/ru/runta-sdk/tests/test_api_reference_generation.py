from __future__ import annotations

import hashlib
import subprocess
import sys
import tomllib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_generated_reference_is_human_and_agent_readable(tmp_path: Path) -> None:
    output = tmp_path / "api"
    subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "generate-api-reference.py"),
            "--output",
            str(output),
        ],
        cwd=ROOT,
        check=True,
    )

    pages = sorted((output / "classes").glob("*/*.md"))
    assert len(pages) == 37
    assert all(" declaration\n" in page.read_text() for page in pages)

    runtime = (output / "classes" / "sync" / "Runtime.md").read_text()
    assert "## Runtime access" in runtime
    assert "## Runtime construction" not in runtime
    assert "runtime = client.runtimes.create(...)" in runtime
    assert "### `boot()`" in runtime
    assert "### `start()`" not in runtime
    assert "### `stop()`" not in runtime
    assert "#### Parameters" in runtime
    assert "Runtime.boot() parameters" not in runtime
    assert "def boot(" in runtime

    client = (output / "classes" / "sync" / "Runta.md").read_text()
    assert "## Runta construction" in client
    assert "## Runta access" not in client

    manager = (output / "classes" / "sync" / "RuntimeManager.md").read_text()
    assert "## RuntimeManager methods" in manager
    assert "### `create()`" in manager
    assert "#### Parameters" in manager
    assert "Optional display name for the runtime." in manager
    assert "#### Returns" in manager
    assert "#### Raises" in manager
    assert "#### Examples" in manager
    assert "| — |" not in "\n".join(page.read_text() for page in pages)

    example_pages = {
        "classes/sync/SecretManager.md": 'client.secrets.set("github-token"',
        "classes/async/AsyncSecretManager.md": "await client.secrets.set(",
        "classes/sync/EgressManager.md": "runtime.egress.set_policy(",
        "classes/async/AsyncEgressManager.md": "await runtime.egress.set_policy(",
        "classes/sync/FileManager.md": "runtime.files.write(",
        "classes/async/AsyncFileManager.md": "await runtime.files.write(",
        "classes/sync/RuntimeCheckpointManager.md": "runtime.checkpoints.create(",
        "classes/async/AsyncRuntimeCheckpointManager.md": (
            "await runtime.checkpoints.create("
        ),
    }
    for path, example in example_pages.items():
        content = (output / path).read_text()
        assert "#### Examples" in content
        assert example in content

    contract = (ROOT / "contracts" / "runta-api.openapi.yaml").read_bytes()
    revision = hashlib.sha256(contract).hexdigest()
    sdk_version = tomllib.loads((ROOT / "pyproject.toml").read_text())["project"][
        "version"
    ]
    overview = (output / "index.md").read_text()
    assert f"SDK `{sdk_version}`" in overview
    assert "OpenAPI `3.0.3`" in overview
    assert f"Schema `sha256:{revision[:12]}`" in overview

    llms_index = (output / "llms.txt").read_text()
    llms_full = (output / "llms-full.txt").read_text()
    assert f"Schema revision: sha256:{revision}" in llms_index
    assert "/reference/sdk/python/api/markdown/classes/sync/Runta.md" in llms_index
    assert "<!-- Source: classes/async/AsyncRuntime.md -->" in llms_full
