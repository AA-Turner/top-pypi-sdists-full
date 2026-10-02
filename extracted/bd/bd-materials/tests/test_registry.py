"""Name -> material lookup tests.

The registry derives itself from the catalog, so what needs proving is that the
derivation is complete and faithful: every material reachable by name, every name
yielding exactly what the equivalent family call does, and a fresh (non-shared)
``FinishedMaterial`` per lookup. Plus the guard rails on unknown/ill-typed input.
"""

import pytest

from bd_materials import finishes
from bd_materials.finished import FinishedMaterial
from bd_materials.materials import ALL_MATERIALS, metals, wood
from bd_materials.materials.metals import Alu
from bd_materials.materials.wood import Hardwood
from bd_materials.registry import (
    canonical_name,
    factory,
    material_names,
    resolve,
)

NAMES = material_names()


def test_names_cover_families_and_grades():
    """155 names: 61 family/species functions + one per catalog material."""
    assert len(NAMES) == 61 + len(ALL_MATERIALS)
    assert len(set(NAMES)) == len(NAMES)


@pytest.mark.parametrize("name", NAMES)
def test_every_name_resolves(name):
    """Each registered name yields a FinishedMaterial."""
    assert isinstance(resolve(name), FinishedMaterial)


@pytest.mark.parametrize("material", ALL_MATERIALS, ids=lambda m: m.name)
def test_every_material_reachable_by_grade_name(material):
    """A material's own name resolves to that exact material."""
    assert resolve(material.name).material is material


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        ("aluminum", metals.aluminum()),
        ("oak", wood.oak()),
        ("Alu_G7075_T6", metals.aluminum(Alu.G7075_T6)),
        ("hardwood_oak", wood.hardwood(Hardwood.OAK)),
    ],
)
def test_resolve_matches_the_family_call(name, expected):
    """A name builds what the equivalent family/grade call builds."""
    assert repr(resolve(name)) == repr(expected)
    assert resolve(name).material is expected.material


@pytest.mark.parametrize("name", ["ALUMINUM", "  Aluminum  ", "aluminum"])
def test_lookup_is_case_and_space_insensitive(name):
    """Names fold case and surrounding whitespace."""
    assert resolve(name).material.name == "Alu_G6061_T6"


@pytest.mark.parametrize("name", ["mild_steel", "mild steel", "Mild-Steel"])
def test_spaces_and_hyphens_read_as_underscores(name):
    """A separator in a name may be written as ``_``, ``-`` or a space."""
    assert resolve(name).material.family == "mild_steel"


def test_trailing_underscore_stripped_from_family_name():
    """``abs_`` (dodging the builtin) is keyed ``abs``."""
    assert resolve("abs").material.name == "ABS_GENERIC"
    assert "abs_" not in NAMES


def test_each_lookup_is_a_fresh_instance():
    """FinishedMaterial is mutable, so a per-part change must not leak."""
    first, second = resolve("aluminum"), resolve("aluminum")
    assert first is not second
    first.color = "red"
    assert second.color is None


def test_factory_returns_the_uncalled_family_function():
    """``factory`` hands back the function, so per-part args can be passed."""
    fm = factory("aluminum")(finish=finishes.anodize("blue"))
    assert repr(fm) == repr(metals.aluminum(finish=finishes.anodize("blue")))


def test_factory_grade_name_takes_the_same_arguments():
    """A grade name binds the grade only -- the other family args still apply."""
    fm = factory("Alu_G7075_T6")(density=2790)
    assert fm.material.name == "Alu_G7075_T6"
    assert fm.material.density == 2790
    # the override is per-part: the catalog material is untouched
    assert resolve("Alu_G7075_T6").material.density == 2810


def test_objects_pass_through_resolve():
    """A FinishedMaterial is returned as-is; a bare Material is wrapped."""
    fm = metals.aluminum(finish=finishes.brushed())
    assert resolve(fm) is fm
    wrapped = resolve(fm.material)
    assert isinstance(wrapped, FinishedMaterial)
    assert wrapped.material is fm.material


def test_unknown_name_suggests_the_closest():
    """A near miss names the candidates it was close to."""
    with pytest.raises(ValueError, match="did you mean.*aluminum"):
        resolve("alumnium")


def test_unknown_name_points_at_the_listing():
    """Every miss points at ``material_names()``, near or wild."""
    with pytest.raises(ValueError, match="material_names"):
        resolve("alumnium")
    with pytest.raises(ValueError, match="material_names"):
        resolve("zzzzzz")


def test_custom_materials_are_not_registered():
    """The registry is the catalog; a user-defined material is not in it."""
    with pytest.raises(ValueError, match="unknown material"):
        resolve("MyAlloy")


@pytest.mark.parametrize("bad", [42, None, ["aluminum"]])
def test_wrong_type_raises(bad):
    """Only a name or a material object is accepted."""
    with pytest.raises(TypeError):
        resolve(bad)


@pytest.mark.parametrize("material", ALL_MATERIALS, ids=lambda m: m.name)
def test_canonical_name_round_trips(material):
    """``canonical_name`` yields a name ``resolve`` maps back to the same material."""
    assert resolve(canonical_name(material)).material is material


def test_finished_material_exposes_the_material_name():
    """``FinishedMaterial.name`` delegates to the material's catalog name."""
    fm = metals.aluminum(finish=finishes.brushed())
    assert fm.name == fm.material.name == "Alu_G6061_T6"


def test_canonical_name_of_a_finished_material_names_the_grade():
    """The grade name, not the family name -- exact even if a default grade changes."""
    assert canonical_name(resolve("aluminum")) == "Alu_G6061_T6"
    assert canonical_name(metals.aluminum(finish=finishes.brushed())) == "Alu_G6061_T6"


def test_canonical_name_rejects_a_custom_material():
    """A user-defined material has no name resolve() would accept."""
    custom = metals.custom_metal(name="MyAlloy", density=4200)
    with pytest.raises(ValueError, match="not a catalog material"):
        canonical_name(custom)


@pytest.mark.parametrize("bad", ["aluminum", 42])
def test_canonical_name_wrong_type_raises(bad):
    """``canonical_name`` takes a material object, not a name."""
    with pytest.raises(TypeError):
        canonical_name(bad)
