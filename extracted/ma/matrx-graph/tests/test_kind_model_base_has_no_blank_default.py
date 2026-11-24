"""Rule 31: the KindModel base must not default its discriminator to a blank."""

import pytest
from pydantic import ValidationError

from matrx_graph.content_ir.model import KindModel


def test_slugless_base_cannot_mint_a_blank_kind():
    assert KindModel.model_fields["kind_"].is_required()
    with pytest.raises(ValidationError):
        KindModel()


def test_declared_kind_still_defaults_to_its_slug():
    class Thing(KindModel, kind="thing_rule31_probe"):
        name: str = "x"

    assert Thing().model_dump()["__kind"] == "thing_rule31_probe"
