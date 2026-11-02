from __future__ import annotations

import ast
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest
import matrx_files.ephemeral_objects as ephemeral_objects

from matrx_files.backends.s3_backend import S3Backend
from matrx_files.ephemeral_objects import (
    EPHEMERAL_LIFECYCLE_TAG_KEY,
    PREVIEW_RENDER_POLICY,
    EphemeralObjectPolicy,
    validate_ephemeral_object_policies,
)
from matrx_files.service import FileService


def _fake_s3() -> S3Backend:
    backend = S3Backend.__new__(S3Backend)
    backend._client = MagicMock()
    backend._configured = True
    backend._default_bucket = "matrx-user-files"
    backend._region = "us-east-1"
    return backend


def _policy(name: str, tag: str, rule_id: str, days: int = 1) -> EphemeralObjectPolicy:
    return EphemeralObjectPolicy(
        name=name,
        tag_value=tag,
        expiration_days=days,
        lifecycle_rule_id=rule_id,
    )


def test_preview_policy_builds_tag_scoped_lifecycle_rule() -> None:
    assert PREVIEW_RENDER_POLICY.object_tags == {
        EPHEMERAL_LIFECYCLE_TAG_KEY: "preview-render"
    }
    assert PREVIEW_RENDER_POLICY.s3_lifecycle_rule() == {
        "ID": "matrx-expire-preview-render-scratch",
        "Filter": {
            "Tag": {
                "Key": EPHEMERAL_LIFECYCLE_TAG_KEY,
                "Value": "preview-render",
            }
        },
        "Status": "Enabled",
        "Expiration": {"Days": 1},
    }


def test_lifecycle_rule_expires_after_the_policys_own_retention() -> None:
    rule = _policy("weekly", "weekly-scratch", "matrx-expire-weekly", days=7).s3_lifecycle_rule()

    assert rule["Expiration"] == {"Days": 7}
    assert rule["Filter"] == {"Tag": {"Key": "matrx-ephemeral-kind", "Value": "weekly-scratch"}}


@pytest.mark.parametrize(
    ("overrides", "message"),
    [
        ({"name": "  "}, "name must not be empty"),
        ({"tag_value": ""}, "tag_value must not be empty"),
        ({"expiration_days": 0}, "expiration_days must be at least 1"),
        ({"lifecycle_rule_id": " "}, "lifecycle_rule_id must not be empty"),
    ],
)
def test_policy_refuses_a_field_that_would_make_an_unscoped_or_instant_rule(
    overrides: dict[str, object], message: str
) -> None:
    fields: dict[str, object] = {
        "name": "scratch",
        "tag_value": "scratch",
        "expiration_days": 1,
        "lifecycle_rule_id": "matrx-expire-scratch",
    }
    fields.update(overrides)

    with pytest.raises(ValueError, match=message):
        EphemeralObjectPolicy(**fields)  # type: ignore[arg-type]


@pytest.mark.parametrize("attribute", ["name", "tag_value", "lifecycle_rule_id"])
def test_policy_registry_rejects_identifier_collisions(attribute: str) -> None:
    first = _policy("first", "first-tag", "first-rule")
    values = {
        "name": "second",
        "tag_value": "second-tag",
        "lifecycle_rule_id": "second-rule",
    }
    values[attribute] = getattr(first, attribute)
    second = _policy(values["name"], values["tag_value"], values["lifecycle_rule_id"])

    with pytest.raises(ValueError, match=f"duplicate {attribute}"):
        validate_ephemeral_object_policies([first, second])


def test_s3_ephemeral_put_attaches_policy_tag_atomically() -> None:
    backend = _fake_s3()

    backend.write_ephemeral(
        "matrx-user-files/owner/system-files/previews/a.jpg",
        b"preview",
        policy=PREVIEW_RENDER_POLICY,
        content_type="image/jpeg",
    )

    kwargs = backend._client.put_object.call_args.kwargs
    assert kwargs["Tagging"] == "matrx-ephemeral-kind=preview-render"
    assert kwargs["ContentType"] == "image/jpeg"
    backend._client.put_object_tagging.assert_not_called()


def test_s3_ephemeral_overwrite_replaces_managed_tag_set(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    backend = _fake_s3()
    replacement = _policy("replacement", "replacement", "replacement-rule")
    monkeypatch.setattr(
        ephemeral_objects,
        "EPHEMERAL_OBJECT_POLICIES",
        (PREVIEW_RENDER_POLICY, replacement),
    )
    path = "matrx-user-files/owner/system-files/previews/a.jpg"

    backend.write_ephemeral(path, b"first", policy=PREVIEW_RENDER_POLICY)
    backend.write_ephemeral(path, b"second", policy=replacement)

    calls = backend._client.put_object.call_args_list
    assert calls[0].kwargs["Tagging"] == "matrx-ephemeral-kind=preview-render"
    assert calls[1].kwargs["Tagging"] == "matrx-ephemeral-kind=replacement"
    backend._client.put_object_tagging.assert_not_called()


def test_s3_ephemeral_write_rejects_policy_without_owned_lifecycle_rule() -> None:
    backend = _fake_s3()

    with pytest.raises(ValueError, match="is not registered"):
        backend.write_ephemeral(
            "matrx-user-files/owner/system-files/previews/a.jpg",
            b"preview",
            policy=_policy("ad-hoc", "ad-hoc", "ad-hoc-rule"),
        )

    backend._client.put_object.assert_not_called()


def test_s3_ephemeral_write_rejects_a_stale_copy_of_a_registered_policy() -> None:
    # Same registered name, different tag: its objects would match no owned rule.
    backend = _fake_s3()
    stale = _policy("preview_render", "preview-render-v0", "matrx-expire-preview-render-scratch")

    with pytest.raises(ValueError, match="differs from the registered policy"):
        backend.write_ephemeral(
            "matrx-user-files/owner/system-files/previews/a.jpg",
            b"preview",
            policy=stale,
        )

    backend._client.put_object.assert_not_called()


def test_s3_ephemeral_multipart_attaches_tag_at_initiation() -> None:
    backend = _fake_s3()
    backend._client.create_multipart_upload.return_value = {"UploadId": "upload"}
    backend._client.upload_part.return_value = {"ETag": "etag"}

    backend.write_ephemeral(
        "matrx-user-files/owner/system-files/previews/large.jpg",
        b"x" * (8 * 1024 * 1024),
        policy=PREVIEW_RENDER_POLICY,
        content_type="image/jpeg",
    )

    kwargs = backend._client.create_multipart_upload.call_args.kwargs
    assert kwargs["Tagging"] == "matrx-ephemeral-kind=preview-render"
    backend._client.put_object_tagging.assert_not_called()


# The sync_engine doubles below are SimpleNamespaces with no `db` / `_db`
# attribute: any attempt by the producer to create or read a file row raises
# AttributeError and fails the test. That — not an assertion — is the
# "without a DB row" forcing function.


@pytest.mark.asyncio
async def test_preview_render_consumes_ephemeral_write_without_db_row() -> None:
    class FakeRouter:
        def __init__(self) -> None:
            self.writes: list[dict[str, object]] = []

        async def write_ephemeral_async(
            self,
            uri: str,
            content: bytes,
            *,
            policy: EphemeralObjectPolicy,
            content_type: str,
        ) -> bool:
            self.writes.append(
                {
                    "uri": uri,
                    "content": content,
                    "policy": policy,
                    "content_type": content_type,
                }
            )
            return True

        async def get_url_async(self, uri: str, **kwargs: object) -> str:
            return f"https://signed.invalid/{uri}"

    class FakeImageHandler:
        @staticmethod
        def render_studio_variant(content: bytes, spec: dict[str, object]) -> dict[str, object]:
            return {
                "preset_id": "preview",
                "width": 10,
                "height": 10,
                "format": "jpeg",
                "quality": 80,
                "size": 7,
                "fit": "cover",
                "position": "center",
                "notes": [],
                "bytes": b"preview",
            }

    router = FakeRouter()
    sync_engine = SimpleNamespace(
        router=router,
        config=SimpleNamespace(resolve_s3_bucket=lambda: "matrx-user-files"),
    )
    manager = SimpleNamespace(sync_engine=sync_engine, image_handler=FakeImageHandler())
    service = FileService.for_file_manager(manager)

    result = await service.render_preview(
        b"source",
        [{"preset_id": "preview"}],
        max_inline_bytes=0,
    )

    assert result[0]["ephemeral_url"].startswith("https://signed.invalid/")
    assert "signed_url" not in result[0]
    assert router.writes == [
        {
            "uri": "s3://matrx-user-files/anonymous/system-files/previews/preview-10x10.jpeg",
            "content": b"preview",
            "policy": PREVIEW_RENDER_POLICY,
            "content_type": "image/jpeg",
        }
    ]


@pytest.mark.asyncio
async def test_pdf_compression_consumes_ephemeral_write_without_db_row(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class FakeRouter:
        def __init__(self) -> None:
            self.writes: list[dict[str, object]] = []

        async def write_ephemeral_async(
            self,
            uri: str,
            content: bytes,
            *,
            policy: EphemeralObjectPolicy,
            content_type: str,
        ) -> bool:
            self.writes.append(
                {
                    "uri": uri,
                    "content": content,
                    "policy": policy,
                    "content_type": content_type,
                }
            )
            return True

        async def get_url_async(self, uri: str, **kwargs: object) -> str:
            return f"https://signed.invalid/{uri}"

    async def fake_compress(
        content: bytes,
        *,
        level: int,
        max_size_bytes: int | None,
    ) -> SimpleNamespace:
        return SimpleNamespace(
            content=b"compressed",
            level_used=level,
            cap_satisfied=True,
            strategy_used="test",
        )

    monkeypatch.setattr(
        "matrx_files.specific_handlers.pdf.compress_pdf_bytes_capped_async",
        fake_compress,
    )
    router = FakeRouter()
    sync_engine = SimpleNamespace(
        router=router,
        config=SimpleNamespace(resolve_s3_bucket=lambda: "matrx-user-files"),
    )
    manager = SimpleNamespace(sync_engine=sync_engine, image_handler=SimpleNamespace())
    service = FileService.for_file_manager(manager)

    result = await service.compress_pdf(b"source-pdf", level=3, max_inline_bytes=0)

    assert result["ephemeral_url"].startswith("https://signed.invalid/")
    assert "signed_url" not in result
    assert router.writes == [
        {
            "uri": "s3://matrx-user-files/anonymous/system-files/previews/compressed-3.pdf",
            "content": b"compressed",
            "policy": PREVIEW_RENDER_POLICY,
            "content_type": "application/pdf",
        }
    ]


def _preview_producer_census(package_root: Path) -> tuple[set[tuple[str, str]], list[str]]:
    """Every function that builds a ``PREVIEWS.path(...)`` is a row-less preview
    producer; each must write through exactly one ``write_ephemeral_async`` and
    never an ordinary ``write_async``. Returns (producers, violations)."""
    producers: set[tuple[str, str]] = set()
    violations: list[str] = []
    for source_path in package_root.rglob("*.py"):
        tree = ast.parse(source_path.read_text())
        for method in ast.walk(tree):
            if not isinstance(method, ast.FunctionDef | ast.AsyncFunctionDef):
                continue
            uses_preview_path = any(
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Attribute)
                and node.func.attr == "path"
                and isinstance(node.func.value, ast.Name)
                and node.func.value.id == "PREVIEWS"
                for node in ast.walk(method)
            )
            if not uses_preview_path:
                continue
            relative = str(source_path.relative_to(package_root))
            producers.add((relative, method.name))
            attributes = [
                node.attr for node in ast.walk(method) if isinstance(node, ast.Attribute)
            ]
            if attributes.count("write_ephemeral_async") != 1 or "write_async" in attributes:
                violations.append(
                    f"{relative}:{method.lineno} {method.name} writes preview scratch without "
                    "exactly one write_ephemeral_async (fix: route it through the "
                    "EPHEMERAL_OBJECT_LIFECYCLE registry)"
                )
    return producers, violations


def test_every_rowless_preview_producer_uses_ephemeral_write_api() -> None:
    # Resolve the INSTALLED package, not a source-tree layout guess — in the
    # independence gate the tests run from a bare copied dir where the package
    # is wheel-installed and Path(__file__).parents[1]/matrx_files is empty.
    import matrx_files

    producers, violations = _preview_producer_census(Path(matrx_files.__file__).parent)

    assert violations == []
    assert producers == {
        ("service.py", "compress_pdf"),
        ("service.py", "render_preview"),
    }


def test_preview_producer_census_flags_an_ordinary_write(tmp_path: Path) -> None:
    # Self-test: the census must be able to fail.
    (tmp_path / "leaky.py").write_text(
        "async def leak(router):\n"
        "    path = PREVIEWS.path('x.jpg')\n"
        "    await router.write_async(path, b'')\n"
    )
    (tmp_path / "lawful.py").write_text(
        "async def keep(router, policy):\n"
        "    path = PREVIEWS.path('y.jpg')\n"
        "    await router.write_ephemeral_async(path, b'', policy=policy)\n"
    )

    producers, violations = _preview_producer_census(tmp_path)

    assert producers == {("leaky.py", "leak"), ("lawful.py", "keep")}
    assert len(violations) == 1
    assert violations[0].startswith("leaky.py:1 leak writes preview scratch")
