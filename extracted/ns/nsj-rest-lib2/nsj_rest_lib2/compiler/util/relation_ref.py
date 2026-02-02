import re
from dataclasses import dataclass
from typing import Literal, Sequence

from nsj_rest_lib2.compiler.edl_model.entity_model_base import EntityModelBase
from nsj_rest_lib2.compiler.edl_model.primitives import (
    REGEX_EXTERNAL_COMPONENT_REF,
    REGEX_EXTERNAL_REF,
    REGEX_INTERNAL_REF,
)


RelationRefType = Literal["internal", "external", "external_component"]


@dataclass
class RelationRef:
    ref_type: RelationRefType
    scope: str | None
    entity: str
    components: list[str]

    @property
    def entity_key(self) -> str | None:
        if not self.scope:
            return None

        return f"{self.scope}/{self.entity}"

    @property
    def target_id(self) -> str:
        return self.components[-1] if self.components else self.entity

    @property
    def prefx_class_name(self) -> str:
        if not self.components:
            return ""

        prefix_parts: list[str] = [self.entity, *self.components[:-1]]
        return f"_{'_'.join(prefix_parts)}"

    @property
    def is_external(self) -> bool:
        return self.ref_type in {"external", "external_component"}

    def resolve_model(
        self,
        entity_models: dict[str, EntityModelBase],
        base_model: EntityModelBase | None = None,
    ) -> EntityModelBase | None:
        entity_key = self.entity_key
        resolved_base: EntityModelBase | None = None

        if entity_key:
            resolved_base = entity_models.get(entity_key)
        elif base_model:
            resolved_base = base_model

        if not resolved_base:
            return None

        return RelationRefParser.follow_components(resolved_base, self.components)


class RelationRefParser:
    @staticmethod
    def parse(ref: str) -> RelationRef | None:
        internal_match = re.match(REGEX_INTERNAL_REF, ref)
        if internal_match:
            components = RelationRefParser._split_components(internal_match.group(1))
            if not components:
                return None
            entity = components[0]
            extra_components = components[1:] if len(components) > 1 else []
            return RelationRef("internal", None, entity, extra_components)

        external_component_match = re.match(REGEX_EXTERNAL_COMPONENT_REF, ref)
        if external_component_match:
            components = RelationRefParser._split_components(
                external_component_match.group(3)
            )
            return RelationRef(
                "external_component",
                external_component_match.group(1),
                external_component_match.group(2),
                components,
            )

        external_match = re.match(REGEX_EXTERNAL_REF, ref)
        if external_match:
            return RelationRef(
                "external",
                external_match.group(1),
                external_match.group(2),
                [],
            )

        return None

    @staticmethod
    def follow_components(
        base_model: EntityModelBase, components: Sequence[str]
    ) -> EntityModelBase | None:
        target_model: EntityModelBase | None = base_model
        for component in components:
            if not target_model or not target_model.components:
                return None
            target_model = target_model.components.get(component)
            if target_model is None:
                return None

        return target_model

    @staticmethod
    def _split_components(components_path: str) -> list[str]:
        # Remove marcadores opcionais '#/components/' intermediários
        cleaned = components_path.replace("#/components/", "/").replace("#", "")
        return [part for part in cleaned.split("/") if part]
