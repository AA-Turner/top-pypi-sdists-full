from typing import Any

from pydantic import BaseModel, ConfigDict

# ============================================================================
# AGENT VARIABLE
# ============================================================================


class AgentVariable(BaseModel):
    """Represents a variable in an agent/prompt"""

    name: str
    value: Any = None
    default_value: Any = None
    required: bool = False
    help_text: str | None = None
    # Frontend display/binding metadata (VariableCustomComponent). Carried verbatim so
    # server-side resolution (e.g. picklist binding -> list_id) has an authoritative,
    # client-unforgeable source. Display-only fields are otherwise ignored by the server.
    custom_component: dict[str, Any] | None = None
    # Scope-context binding. When set, this variable is filled at run time from a scope
    # context item (the active scope of `scope_type_id` supplies the value of `item_key`).
    # Authored on the agent (client-unforgeable). Resolved by
    # ``aidream.api.utils.scope_binding_resolution.resolve_scope_bindings``. Shape:
    # ``{contextItemId, scopeTypeId, itemKey, onMissing}`` (camelCase from the FE).
    binding: dict[str, Any] | None = None

    model_config = ConfigDict(extra="allow")

    def get_value(self) -> Any:
        """Return an explicit value, then the saved Builder default, then empty."""
        if self.value is not None:
            return self._runtime_value(self.value)
        if self.default_value is not None:
            return self._runtime_value(self.default_value)
        return ""

    @staticmethod
    def _runtime_value(value: Any) -> Any:
        from matrx_ai.agents.auto_assignment import has_auto_assign_tag

        if has_auto_assign_tag(value):
            return value
        # Structured values enter prompts as canonical JSON, never Python repr
        # (str({'a': 1}) -> "{'a': 1}" is unparseable for the model and drifts
        # from every JSON contract downstream). Scalars keep plain str().
        # Delegate to THE prompt door (config.prompt_values) — one law, one
        # implementation, shared with TextContent.replace_variables (F4).
        from matrx_ai.config.prompt_values import prompt_safe_value

        return prompt_safe_value(value)

    def picklist_binding(self) -> dict[str, Any] | None:
        """Return the authoritative picklist binding for this variable, or None.

        Shape (when bound): ``{"list_id": str, "multiple": bool}``. Sourced from the
        agent definition (``customComponent.structured_list``, with read-only fallback to
        the legacy ``customComponent.picklist`` key for historical defs), NOT from any
        client payload, so a client can only choose WHICH item — never which list.
        """
        cc = self.custom_component
        if not isinstance(cc, dict):
            return None
        # Canonical key is `structured_list`; `picklist` is the legacy read-only alias.
        pl = cc.get("structured_list") or cc.get("picklist")
        if not isinstance(pl, dict):
            return None
        list_id = pl.get("listId") or pl.get("list_id")
        if not isinstance(list_id, str) or not list_id:
            return None
        return {"list_id": list_id, "multiple": bool(pl.get("multiple", False))}

    def scope_binding(self) -> dict[str, Any] | None:
        """Return the normalized scope-context binding for this variable, or None.

        Shape (when bound): ``{"context_item_id", "scope_type_id", "item_key", "on_missing"}``.
        Sourced from the agent definition (``binding``), accepting both camelCase (FE) and
        snake_case keys. ``item_key`` is what the server resolves against the active scope's
        context items; ``on_missing`` is one of ``empty | skip | error`` (default ``empty``).
        """
        b = self.binding
        if not isinstance(b, dict):
            return None
        item_key = b.get("itemKey") or b.get("item_key")
        context_item_id = b.get("contextItemId") or b.get("context_item_id")
        # A binding needs at least an item_key (portable) or a context_item_id to resolve.
        if not (isinstance(item_key, str) and item_key) and not (
            isinstance(context_item_id, str) and context_item_id
        ):
            return None
        on_missing = (b.get("onMissing") or b.get("on_missing") or "empty").lower()
        if on_missing not in ("empty", "skip", "error"):
            on_missing = "empty"
        return {
            "context_item_id": context_item_id if isinstance(context_item_id, str) else None,
            "scope_type_id": b.get("scopeTypeId") or b.get("scope_type_id"),
            "item_key": item_key if isinstance(item_key, str) else None,
            "on_missing": on_missing,
        }

    @classmethod
    def from_dict(cls, var_def: dict[str, Any]) -> "AgentVariable":
        """
        Create AgentVariable from dictionary.

        Args:
            var_def: Dictionary with keys: name, defaultValue, required, helpText,
                customComponent (optional; carries picklist binding + display config)

        Returns:
            AgentVariable instance
        """
        return cls(
            name=var_def["name"],
            default_value=var_def.get("defaultValue", ""),
            required=var_def.get("required", False),
            help_text=var_def.get("helpText"),
            custom_component=var_def.get("customComponent"),
            binding=var_def.get("binding"),
        )

    @staticmethod
    def from_list(var_defs: list | None) -> dict[str, "AgentVariable"]:
        """
        Parse list of variable definitions into dict of AgentVariables.

        Args:
            var_defs: List of variable definition dicts (from database)

        Returns:
            Dict mapping variable names to AgentVariable instances
        """
        if not var_defs:
            return {}

        return {
            var_def["name"]: AgentVariable.from_dict(var_def) for var_def in var_defs
        }

    def to_dict(self) -> dict[str, Any]:
        """
        Convert the agent variables to a dictionary.
        """
        return {
            "name": self.name,
            "value": self.value,
            "default_value": self.default_value,
            "required": self.required,
            "help_text": self.help_text,
            "custom_component": self.custom_component,
            "binding": self.binding,
        }


def picklist_bindings_from_variables(
    variable_defaults: dict[str, "AgentVariable"] | None,
) -> dict[str, dict[str, Any]]:
    """Build the authoritative ``{var_name: {list_id, multiple}}`` picklist-binding map
    from an agent's variable definitions. Only variables actually bound to a picklist are
    included. This is the trusted source the server uses to resolve picklist references
    (a client supplies only the chosen item id, never the list)."""
    out: dict[str, dict[str, Any]] = {}
    for name, var in (variable_defaults or {}).items():
        binding = var.picklist_binding()
        if binding is not None:
            out[name] = binding
    return out


def scope_bindings_from_variables(
    variable_defaults: dict[str, "AgentVariable"] | None,
) -> dict[str, dict[str, Any]]:
    """Build the authoritative ``{var_name: normalized_scope_binding}`` map from an agent's
    variable definitions. Only variables actually bound to a scope context item are included.
    The normalized binding shape is ``{context_item_id, scope_type_id, item_key, on_missing}``
    (see ``AgentVariable.scope_binding``). This is the trusted source the binding resolver
    consumes — a client cannot forge which context item a variable draws from."""
    out: dict[str, dict[str, Any]] = {}
    for name, var in (variable_defaults or {}).items():
        binding = var.scope_binding()
        if binding is not None:
            out[name] = binding
    return out
