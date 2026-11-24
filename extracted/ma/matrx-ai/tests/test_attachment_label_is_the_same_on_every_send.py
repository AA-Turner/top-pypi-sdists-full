"""An attachment's ``<attachment …/>`` label has the same bytes on turn 1 and on every replay.

Live finding (static seal check, 2026-11-12): turn 1 rendered ``name_unavailable`` (the live part had
no name yet) and the replay rendered ``name="<id>.png"`` — a name storage made from the id, with an
extension that was wrong for a JPEG. The label changed inside the cached prefix.
"""

from __future__ import annotations

from matrx_ai.config.attached_files import file_block_label
from matrx_ai.config.media_config import ImageContent
from matrx_ai.config.message_config import UnifiedMessage, _media_identity_label

FILE_ID = "5b1e8a4e-1f0c-4b52-9a3e-2d7c6f0e9a11"


def _image(metadata: dict) -> ImageContent:
    return ImageContent(file_id=FILE_ID, mime_type="image/jpeg", metadata=metadata)


def test_turn_one_and_the_replay_render_the_same_label() -> None:
    turn_one = _media_identity_label(_image({}), "user")
    replay = _media_identity_label(_image({"file_name": f"{FILE_ID}.png"}), "user")
    assert turn_one == replay
    assert ".png" not in replay and "name_unavailable" in replay


def test_a_name_found_at_dispatch_is_shown_on_turn_one_and_on_replay() -> None:
    """The preflight size count renders the label BEFORE dispatch names the part: it must not freeze
    the empty name. Dispatch's name is shown on turn 1 and, after a round trip through storage, on replay."""
    part = _image({})
    _media_identity_label(part, "user")  # the preflight render, nameless
    part.metadata["file_name"] = "Holiday.jpg"  # named at dispatch
    turn_one = _media_identity_label(part, "user")
    assert 'name="Holiday.jpg"' in turn_one
    message = UnifiedMessage(role="user", content=[part])
    stored = {"role": "user", "content": [part.to_storage_dict()]}  # the stored row's shape
    replayed = UnifiedMessage.from_dict(stored).content[0]
    assert replayed is not part and _media_identity_label(replayed, "user") == turn_one
    assert message.content[0] is part


def test_a_real_name_is_shown() -> None:
    label = _media_identity_label(_image({"file_name": "Holiday.jpg"}), "user")
    assert 'name="Holiday.jpg"' in label


def test_the_document_label_never_shows_a_made_up_name() -> None:
    entry = {"file_id": FILE_ID, "file_name": f"{FILE_ID}.png"}
    assert file_block_label(entry) == file_block_label({"file_id": FILE_ID})


def test_a_file_source_never_shows_a_made_up_name() -> None:
    from matrx_ai.config.structured_input_config import _with_source_identity

    made_up = _with_source_identity("file", f"{FILE_ID}.png", FILE_ID, "body")
    assert ".png" not in made_up and "name_unavailable" in made_up
    assert 'name="Holiday.jpg"' in _with_source_identity("file", "Holiday.jpg", FILE_ID, "body")
