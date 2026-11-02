"""File wire shapes carry the two row-access words (access ladder T-13).

Every response carries ``published_to_web`` + ``shown_to``; a request that still sends the
retiring level word is reconciled at the boundary (matrx_utils.row_access tests); ``shown_to`` refuses values
the DB enum does not hold.
"""

from __future__ import annotations

import inspect

import pytest
from pydantic import ValidationError

from matrx_files.asset_envelope import Asset, AssetPatchRequest, CopyInfo, FileRef
from matrx_files.api.router_files import _BulkBody, _PatchBody
from matrx_files.cloud_sync.models import SyncResult
from matrx_files.cloud_sync.sync_engine import SyncEngine, _legacy_write_access, row_access_insert_columns
from matrx_files.service import FileService
from matrx_utils.row_access import SHOWN_TO_VALUES

RESPONSE_MODELS = (
    (Asset, {"file_id": "f", "folder": "some/dir"}),
    (FileRef, {"file_id": "f"}),
)


@pytest.mark.parametrize("shown", SHOWN_TO_VALUES)
@pytest.mark.parametrize("model,base", RESPONSE_MODELS, ids=lambda m: getattr(m, "__name__", ""))
def test_every_shown_to_value_survives_response_models(model, base, shown) -> None:
    out = model(**base, published_to_web=True, shown_to=shown)
    assert (out.published_to_web, out.shown_to) == (True, shown)


@pytest.mark.parametrize("model,base", RESPONSE_MODELS, ids=lambda m: getattr(m, "__name__", ""))
def test_an_unknown_shown_to_is_refused_on_the_way_out(model, base) -> None:
    with pytest.raises(ValidationError):
        model(**base, shown_to="personal")


def test_copy_info_carries_the_web_lane() -> None:
    assert CopyInfo(file_id="f", file_path="a/b.png", published_to_web=True).published_to_web is True


def test_requests_carry_the_new_words() -> None:
    body = AssetPatchRequest(published_to_web=False, shown_to="my_team")
    assert (body.published_to_web, body.shown_to) == (False, "my_team")


def test_unstated_engine_insert_is_private_and_listed_to_its_creator() -> None:
    columns = row_access_insert_columns(None, None, "user-1")

    assert columns["published_to_web"] is False
    assert columns["shown_to"] == "only_me"


@pytest.mark.parametrize(
    ("visibility", "published", "shown", "wants_link"),
    (("public", True, None, False), ("personal", False, "only_me", False), ("link", False, None, True)),
)
def test_retiring_write_keyword_has_one_compatible_access_seam(
    visibility: str, published: bool, shown: str | None, wants_link: bool
) -> None:
    assert _legacy_write_access(None, None, visibility) == (published, shown, wants_link)
    assert "visibility" in inspect.signature(SyncEngine.managed_write_async).parameters
    assert "visibility" in inspect.signature(FileService.upload_simple).parameters


def test_link_write_result_carries_a_retrievable_share_url() -> None:
    result = SyncResult(file_id="f", storage_uri="s3://private/u/f", version_number=1,
                        share_token="token-1", share_url="/share/token-1")
    assert result.share_url == f"/share/{result.share_token}"


def test_router_keeps_t13_patch_and_bulk_operations_open() -> None:
    patch = _PatchBody(published_to_web=True, shown_to="everyone")
    assert (patch.published_to_web, patch.shown_to) == (True, "everyone")
    assert _BulkBody(ids=["f"], op="publish", args={"published_to_web": True}).op == "publish"
    assert _BulkBody(ids=["f"], op="shown_to", args={"shown_to": "my_team"}).op == "shown_to"
