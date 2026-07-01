from spec_kitty_tracker import FieldOwner, OwnershipMode, OwnershipPolicy


def test_external_authoritative_policy() -> None:
    policy = OwnershipPolicy.external_authoritative()
    assert policy.mode == OwnershipMode.EXTERNAL_AUTHORITATIVE
    assert policy.external_can_write("status") is True
    assert policy.local_can_write("status") is False


def test_local_authoritative_policy() -> None:
    policy = OwnershipPolicy.local_authoritative()
    assert policy.mode == OwnershipMode.SPEC_KITTY_AUTHORITATIVE
    assert policy.local_can_write("labels") is True
    assert policy.external_can_write("labels") is False


def test_split_policy() -> None:
    policy = OwnershipPolicy.split(
        field_owners={
            "status": FieldOwner.EXTERNAL,
            "title": FieldOwner.LOCAL,
        },
        default_owner=FieldOwner.SHARED,
    )
    assert policy.owner_for("status") == FieldOwner.EXTERNAL
    assert policy.owner_for("title") == FieldOwner.LOCAL
    assert policy.owner_for("body") == FieldOwner.SHARED
