from pydantic import Field, ValidationError, model_validator
from pydantic_core import PydanticCustomError

from nsj_rest_lib2.compiler.edl_model.entity_model_base import EntityModelBase
from nsj_rest_lib2.compiler.edl_model.validation_util import (
    resolve_effective_repository_column,
)


class EntityModelRoot(EntityModelBase):
    escopo: str = Field(..., description="Escopo do EDL (define a aplicação).")

    @model_validator(mode="after")
    def validate_repository_and_required_consistency(self) -> "EntityModelRoot":
        """
        Aplica validações estruturais do EDL na entidade raiz.

        Regras:
        - Propriedade PK precisa constar em `required`;
        - Coluna física não pode ser mapeada por mais de uma propriedade;
        - `repository.map` é obrigatório para entidades não mixin;
        - Mixins não devem definir `repository.map`.

        Returns:
            Próprio modelo validado.

        Raises:
            ValidationError: Quando houver inconsistências estruturais.
        """
        line_errors: list[dict] = []

        required_set = set(self.required or [])
        for prop_name, prop_meta in (self.properties or {}).items():
            if getattr(prop_meta, "pk", False) and prop_name not in required_set:
                line_errors.append(
                    {
                        "type": PydanticCustomError(
                            "pk_not_required",
                            "Propriedade PK '{property}' deve constar em required.",
                            {"property": prop_name},
                        ),
                        "loc": ("required",),
                        "input": self.required,
                    }
                )

        repo_properties = self.repository.properties or {}
        column_to_props: dict[str, list[str]] = {}
        for prop_name, prop_meta in (self.properties or {}).items():
            repo_prop_meta = repo_properties.get(prop_name)
            effective_column = resolve_effective_repository_column(
                prop_name=prop_name,
                prop_meta=prop_meta,
                repo_prop_meta=repo_prop_meta,
            )
            if not effective_column:
                continue
            column_to_props.setdefault(effective_column, []).append(prop_name)

        for column_name, prop_names in column_to_props.items():
            if len(prop_names) <= 1:
                continue
            props_sorted = ", ".join(sorted(prop_names))
            line_errors.append(
                {
                    "type": PydanticCustomError(
                        "duplicate_repository_column",
                        (
                            "Coluna física '{column}' mapeada por mais de uma propriedade: "
                            "{properties}."
                        ),
                        {
                            "column": column_name,
                            "properties": props_sorted,
                        },
                    ),
                    "loc": ("repository", "properties"),
                    "input": self.repository.properties,
                }
            )

        repository_map = (
            self.repository.map.strip()
            if isinstance(self.repository.map, str)
            else None
        )
        if self.mixin:
            if repository_map:
                line_errors.append(
                    {
                        "type": PydanticCustomError(
                            "mixin_repository_map_not_allowed",
                            "Mixins não devem definir repository.map.",
                            {},
                        ),
                        "loc": ("repository", "map"),
                        "input": self.repository.map,
                    }
                )
        elif not repository_map:
            line_errors.append(
                {
                    "type": PydanticCustomError(
                        "repository_map_required",
                        "repository.map é obrigatório para entidades não mixin.",
                        {},
                    ),
                    "loc": ("repository", "map"),
                    "input": self.repository.map,
                }
            )

        if line_errors:
            raise ValidationError.from_exception_data(
                self.__class__.__name__,
                line_errors,
            )

        return self
