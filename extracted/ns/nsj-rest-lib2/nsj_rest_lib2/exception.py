class MissingEntityConfigException(Exception):
    pass


class MissingDependencyConfigException(Exception):
    """
    Erro de alto nível para falha de carga de dependências de uma entidade.
    """

    def __init__(
        self,
        *,
        entity_resource: str,
        dependency_resource: str,
        dependency_scope: str | None = None,
        dependency_tenant: int | str | None = None,
        dependency_grupo_empresarial: str | None = None,
    ) -> None:
        self.entity_resource = entity_resource
        self.dependency_resource = dependency_resource
        self.dependency_scope = dependency_scope
        self.dependency_tenant = dependency_tenant
        self.dependency_grupo_empresarial = dependency_grupo_empresarial
        super().__init__(self._build_message())

    @property
    def dependency_key(self) -> str:
        # Formato legível para mensagens de API e logs.
        if self.dependency_scope:
            return f"{self.dependency_scope}/{self.dependency_resource}"
        return self.dependency_resource

    def _build_message(self) -> str:
        return (
            f"Missing dependency config '{self.dependency_key}' "
            f"required by '{self.entity_resource}'."
        )
