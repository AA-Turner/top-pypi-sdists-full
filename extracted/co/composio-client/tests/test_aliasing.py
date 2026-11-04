"""Two properties of the rename kernel that no request can currently exercise.

``_aliasing`` renames a dict body's keys and nothing else; ``test_wire_parity``
and ``test_body_path_agreement`` pin *what it renames* against the oracle. This
module pins two things that are not about any particular body:

* the per-model tables it memoizes must not keep a model class alive — the
  generated models are immortal anyway, but a model built at runtime
  (``pydantic.create_model``, a model declared inside a function or a test) must
  still be collectable;
* a ``RootModel`` must be transparent. Walked as a plain name map it declares
  exactly one field, ``root``, which no caller writes, so *every* key would be
  forwarded unrenamed — a silent no-op that looks like success.

Both were latent when they were written down: nothing in the current spec
snapshot has a ``RootModel`` request body, and the client only ever renames
against module-level generated models. They are pinned here so they stay fixed.
"""

from __future__ import annotations

import gc
import weakref
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier
from typing import Annotated, Any, Literal, Optional

import pytest
from pydantic import BaseModel, ConfigDict, Field, RootModel, create_model
from pydantic._internal._model_construction import ModelMetaclass

from composio_client._aliasing import (
    _DISCRIMINATORS_ATTR,
    _FIELD_INDEX_ATTR,
    _alternatives,
    _models,
    rename_to_wire_names,
)
from composio_client._models import SessionConfigHistoryResponse


class _Aliased(BaseModel):
    """One aliased field is enough to tell a rename from a no-op."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    your_domain: str | None = Field(default=None, alias="your-domain")


def _make_local_model() -> type[BaseModel]:
    """A model whose only reference is the one the caller holds."""
    return create_model(
        "Ephemeral",
        __config__=ConfigDict(populate_by_name=True, extra="allow"),
        your_domain=(str | None, Field(default=None, alias="your-domain")),
    )


# --------------------------------------------------------------------------
# 1. the memo may not outlive the class it describes
# --------------------------------------------------------------------------


def test_a_model_used_for_a_rename_is_still_collectable() -> None:
    """The regression test for the memo's lifetime.

    With the ``functools.cache`` this used to use, the cache dict held a strong
    reference to every model class it was ever called with, so this class — and
    everything its ``__mro__`` and closure reach — survived the collection
    below for the life of the process. Verified failing before the fix.
    """
    model = _make_local_model()
    # the rename has to be real: a no-op would never populate the memo, and the
    # test would pass without proving anything.
    assert rename_to_wire_names(model, {"your_domain": "acme.example.com"}) == {
        "your-domain": "acme.example.com"
    }

    ref = weakref.ref(model)
    del model
    gc.collect()

    assert ref() is None, "a model used for one rename outlived the reference to it"


def test_every_memoized_table_is_covered_by_that_guarantee() -> None:
    """Both tables, not just the one an aliased body happens to touch.

    ``_discriminators`` is only built for a union member, so a body that never
    resolves a union would leave it cold and the retention above would say
    nothing about it.
    """

    class _Variant(BaseModel):
        model_config = ConfigDict(populate_by_name=True, extra="allow")

        auth_scheme: Literal["OAUTH2"] = Field(alias="authScheme")
        your_domain: str | None = Field(default=None, alias="your-domain")

    class _Other(BaseModel):
        model_config = ConfigDict(populate_by_name=True, extra="allow")

        auth_scheme: Literal["OAUTH1"] = Field(alias="authScheme")

    # Built rather than declared so the union is an expression: `X | Y`, not
    # `Union[X, Y]`, because `typing.Union[...]` memoizes its result in the
    # typing module's own `_tp_cache` and would keep both members alive no
    # matter what this module does.
    _Body = create_model(
        "_UnionBody",
        __config__=ConfigDict(populate_by_name=True, extra="allow"),
        connection=(_Variant | _Other, ...),
    )

    renamed = rename_to_wire_names(
        _Body, {"connection": {"auth_scheme": "OAUTH2", "your_domain": "acme.example.com"}}
    )
    assert renamed == {"connection": {"authScheme": "OAUTH2", "your-domain": "acme.example.com"}}
    assert _DISCRIMINATORS_ATTR in _Variant.__dict__, "discriminators were never memoized"

    refs = [weakref.ref(cls) for cls in (_Body, _Variant, _Other)]
    del _Body, _Variant, _Other
    gc.collect()

    assert [ref() for ref in refs] == [None, None, None]


def test_the_memo_lives_on_the_class_it_describes() -> None:
    model = _make_local_model()
    assert _FIELD_INDEX_ATTR not in model.__dict__
    rename_to_wire_names(model, {"your_domain": "acme.example.com"})
    assert _FIELD_INDEX_ATTR in model.__dict__


def test_a_subclass_does_not_inherit_its_base_s_table() -> None:
    """The memo is read out of ``cls.__dict__``, never ``getattr``: a subclass
    that adds a field must not be renamed against its base's field set."""
    rename_to_wire_names(_Aliased, {"your_domain": "acme.example.com"})
    assert _FIELD_INDEX_ATTR in _Aliased.__dict__

    class _Extended(_Aliased):
        instance_name: str | None = Field(default=None, alias="instanceName")

    assert rename_to_wire_names(_Extended, {"your_domain": "d", "instance_name": "n"}) == {
        "your-domain": "d",
        "instanceName": "n",
    }


def test_a_class_that_refuses_attribute_assignment_still_renames() -> None:
    """The memo is an optimization, never a requirement.

    A metaclass that forbids class attribute assignment must cost the memo, not
    the rename — this function is contractually unable to fail on a body. The
    stand-in only refuses *our* attributes because pydantic itself assigns to
    the class while building it.
    """

    class _Sealed(ModelMetaclass):
        def __setattr__(cls, name: str, value: Any) -> None:
            if name.startswith("__composio_aliasing"):
                raise AttributeError(name)
            super().__setattr__(name, value)

    class _Unmemoizable(BaseModel, metaclass=_Sealed):
        model_config = ConfigDict(populate_by_name=True, extra="allow")

        your_domain: str | None = Field(default=None, alias="your-domain")

    for _ in range(2):  # the second call takes the same uncached path
        assert rename_to_wire_names(_Unmemoizable, {"your_domain": "acme"}) == {"your-domain": "acme"}
    assert _FIELD_INDEX_ATTR not in _Unmemoizable.__dict__


def test_concurrent_first_renames_of_one_model_agree() -> None:
    """Every request goes through this, on the sync *and* async clients, so a
    cold model may be walked by several threads at once. Racing writers are
    allowed (the table is a pure function of ``model_fields``, so the results
    are equal); a torn or partial read is not."""
    model = _make_local_model()
    threads = 16
    barrier = Barrier(threads)

    def rename() -> dict[str, Any]:
        barrier.wait()  # maximize the overlap on the cold path
        return rename_to_wire_names(model, {"your_domain": "acme.example.com"})

    with ThreadPoolExecutor(max_workers=threads) as pool:
        results = [future.result() for future in [pool.submit(rename) for _ in range(threads)]]

    assert results == [{"your-domain": "acme.example.com"}] * threads


# --------------------------------------------------------------------------
# 2. a RootModel is transparent, never a body with one field called `root`
# --------------------------------------------------------------------------


class _WrappedBody(RootModel[_Aliased]):
    pass


def test_a_root_model_body_renames_against_what_it_wraps() -> None:
    """The regression test for the silent no-op: before the fix this returned
    the caller's mapping verbatim, because the only key the model declared was
    ``root``."""
    assert rename_to_wire_names(_WrappedBody, {"your_domain": "acme.example.com"}) == {
        "your-domain": "acme.example.com"
    }


def test_a_root_model_field_renames_the_mapping_under_it() -> None:
    class _Body(BaseModel):
        model_config = ConfigDict(populate_by_name=True, extra="allow")

        nested: _WrappedBody

    assert rename_to_wire_names(_Body, {"nested": {"your_domain": "d"}}) == {"nested": {"your-domain": "d"}}


def test_a_root_model_over_a_list_renames_each_element() -> None:
    class _WrappedList(RootModel[list[_Aliased]]):
        pass

    class _Body(BaseModel):
        model_config = ConfigDict(populate_by_name=True, extra="allow")

        items: _WrappedList

    assert rename_to_wire_names(_Body, {"items": [{"your_domain": "a"}, {"your_domain": "b"}]}) == {
        "items": [{"your-domain": "a"}, {"your-domain": "b"}]
    }


def test_a_root_model_over_a_dict_renames_each_value() -> None:
    class _WrappedDict(RootModel[dict[str, _Aliased]]):
        pass

    class _Body(BaseModel):
        model_config = ConfigDict(populate_by_name=True, extra="allow")

        by_key: _WrappedDict

    renamed = rename_to_wire_names(_Body, {"by_key": {"first": {"your_domain": "a"}}})
    # the mapping's own keys are data, not field names, and are never renamed
    assert renamed == {"by_key": {"first": {"your-domain": "a"}}}


def test_a_root_model_over_a_scalar_leaves_the_value_alone() -> None:
    class _WrappedScalar(RootModel[str]):
        pass

    class _Body(BaseModel):
        model_config = ConfigDict(populate_by_name=True, extra="allow")

        note: _WrappedScalar

    assert rename_to_wire_names(_Body, {"note": "3600"}) == {"note": "3600"}


def test_a_root_model_over_a_union_still_resolves_per_variant() -> None:
    """Peeling the wrapper must not smear one member's aliases over the union —
    the behavior ``test_tool_router`` pins for ``custom_connection_data``."""

    class _OAuth2(BaseModel):
        model_config = ConfigDict(populate_by_name=True, extra="allow")

        auth_scheme: Literal["OAUTH2"] = Field(alias="authScheme")

    class _OAuth1(BaseModel):
        model_config = ConfigDict(populate_by_name=True, extra="allow")

        auth_scheme: Literal["OAUTH1"] = Field(alias="authScheme")
        redirect_url: str | None = Field(default=None, alias="redirectUrl")

    class _WrappedUnion(RootModel[_OAuth2 | _OAuth1]):
        pass

    assert _models(_WrappedUnion) == [_OAuth2, _OAuth1]
    assert rename_to_wire_names(
        _WrappedUnion, {"auth_scheme": "OAUTH2", "redirect_url": "https://example.com/cb"}
    ) == {"authScheme": "OAUTH2", "redirect_url": "https://example.com/cb"}


def test_a_recursive_root_model_terminates() -> None:
    """The peel is guarded: a root model that (transitively) wraps itself is
    left as a branch rather than unwrapped forever."""

    class _Recursive(RootModel[Optional["_Recursive"]]):
        pass

    _Recursive.model_rebuild()

    assert _alternatives(_Recursive) == [_Recursive, type(None)]
    assert rename_to_wire_names(_Recursive, {"anything": 1}) == {"anything": 1}


@pytest.mark.parametrize(
    ("annotation", "branches"),
    [
        (_Aliased, [_Aliased]),
        (_Aliased | None, [_Aliased, type(None)]),
        # containers are not peeled here — the element type is looked up separately
        (list[_Aliased], [list[_Aliased]]),
        (dict[str, _Aliased], [dict[str, _Aliased]]),
        (Annotated[int, "meta"], [int]),
        (str, [str]),
    ],
    ids=lambda value: str(value),
)
def test_peeling_did_not_disturb_ordinary_annotations(annotation: Any, branches: list[Any]) -> None:
    """The wrapper peel is additive: an annotation with no ``RootModel`` in it
    flattens to exactly the branches it always did."""
    assert _alternatives(annotation) == branches


def test_root_model_responses_are_untouched_by_any_of_this() -> None:
    """Responses are ``model_validate``d by the kernel and never reach this
    module; three of them are ``RootModel`` (``config_history``, ``toolkits``,
    ``tools``). Walking one here must not change how it parses."""
    payload = {"items": [], "total_pages": 1, "current_page": 1, "total_items": 0}
    _models(SessionConfigHistoryResponse)  # the walk the request path would do
    parsed = SessionConfigHistoryResponse.model_validate(payload)
    assert parsed.root.total_items == 0


def test_a_root_model_instance_inside_a_body_is_dumped_by_alias() -> None:
    """A model handed in *inside* a dict is the caller's typed contract, root
    model or not: it is dumped, not walked."""

    class _Body(BaseModel):
        model_config = ConfigDict(populate_by_name=True, extra="allow")

        nested: _WrappedBody

    body = {"nested": _WrappedBody(_Aliased(your_domain="acme.example.com"))}
    assert rename_to_wire_names(_Body, body) == {"nested": {"your-domain": "acme.example.com"}}
