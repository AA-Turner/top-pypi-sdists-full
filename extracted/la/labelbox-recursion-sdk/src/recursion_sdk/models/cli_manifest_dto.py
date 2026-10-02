from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.cli_manifest_dto_concepts import CliManifestDtoConcepts
  from ..models.cli_manifest_dto_guides import CliManifestDtoGuides
  from ..models.cli_manifest_dto_operations import CliManifestDtoOperations
  from ..models.cli_manifest_dto_recipes import CliManifestDtoRecipes
  from ..models.cli_manifest_dto_resources import CliManifestDtoResources





T = TypeVar("T", bound="CliManifestDto")



@_attrs_define
class CliManifestDto:
    """ The pre-assembled command manifest the live `recursion` CLI fetches to build its command tree, help, and docs
    surfaces.

        Attributes:
            format_version (float): Manifest schema version; the CLI rejects a version it does not understand.
            hash_ (str): Content hash of the manifest body — also returned as the ETag for conditional fetches.
            operations (CliManifestDtoOperations): Executable operations keyed by operationId — the CLI command tree, flags,
                and shapes.
            resources (CliManifestDtoResources): Reference resource hubs keyed by id — object shapes, operations, and
                intros.
            recipes (CliManifestDtoRecipes): How-to recipes keyed by id — composed SDK / CLI / cURL walkthroughs.
            concepts (CliManifestDtoConcepts): Explanation concept pages keyed by id, each with its markdown body.
            tutorials (list[Any]): Getting-started tutorials, each with its markdown body.
            domains (list[Any]): The product-domain taxonomy that groups the browse surfaces.
            guides (CliManifestDtoGuides | Unset): Authored product guides keyed by id, each with its rendered MDX body.
     """

    format_version: float
    hash_: str
    operations: CliManifestDtoOperations
    resources: CliManifestDtoResources
    recipes: CliManifestDtoRecipes
    concepts: CliManifestDtoConcepts
    tutorials: list[Any]
    domains: list[Any]
    guides: CliManifestDtoGuides | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.cli_manifest_dto_concepts import CliManifestDtoConcepts # noqa: PLC0415
        from ..models.cli_manifest_dto_guides import CliManifestDtoGuides # noqa: PLC0415
        from ..models.cli_manifest_dto_operations import CliManifestDtoOperations # noqa: PLC0415
        from ..models.cli_manifest_dto_recipes import CliManifestDtoRecipes # noqa: PLC0415
        from ..models.cli_manifest_dto_resources import CliManifestDtoResources # noqa: PLC0415
        format_version = self.format_version

        hash_ = self.hash_

        operations = self.operations.to_dict()

        resources = self.resources.to_dict()

        recipes = self.recipes.to_dict()

        concepts = self.concepts.to_dict()

        tutorials = self.tutorials



        domains = self.domains



        guides: dict[str, Any] | Unset = UNSET
        if not isinstance(self.guides, Unset):
            guides = self.guides.to_dict()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "formatVersion": format_version,
            "hash": hash_,
            "operations": operations,
            "resources": resources,
            "recipes": recipes,
            "concepts": concepts,
            "tutorials": tutorials,
            "domains": domains,
        })
        if guides is not UNSET:
            field_dict["guides"] = guides

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.cli_manifest_dto_concepts import CliManifestDtoConcepts # noqa: PLC0415
        from ..models.cli_manifest_dto_guides import CliManifestDtoGuides # noqa: PLC0415
        from ..models.cli_manifest_dto_operations import CliManifestDtoOperations # noqa: PLC0415
        from ..models.cli_manifest_dto_recipes import CliManifestDtoRecipes # noqa: PLC0415
        from ..models.cli_manifest_dto_resources import CliManifestDtoResources # noqa: PLC0415
        d = dict(src_dict)
        format_version = d.pop("formatVersion")

        hash_ = d.pop("hash")

        operations = CliManifestDtoOperations.from_dict(d.pop("operations"))




        resources = CliManifestDtoResources.from_dict(d.pop("resources"))




        recipes = CliManifestDtoRecipes.from_dict(d.pop("recipes"))




        concepts = CliManifestDtoConcepts.from_dict(d.pop("concepts"))




        tutorials = cast(list[Any], d.pop("tutorials"))


        domains = cast(list[Any], d.pop("domains"))


        _guides = d.pop("guides", UNSET)
        guides: CliManifestDtoGuides | Unset
        if isinstance(_guides,  Unset):
            guides = UNSET
        else:
            guides = CliManifestDtoGuides.from_dict(_guides)




        cli_manifest_dto = cls(
            format_version=format_version,
            hash_=hash_,
            operations=operations,
            resources=resources,
            recipes=recipes,
            concepts=concepts,
            tutorials=tutorials,
            domains=domains,
            guides=guides,
        )

        return cli_manifest_dto

