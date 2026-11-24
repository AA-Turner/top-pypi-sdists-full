from collections.abc import Collection, Mapping
from typing import Any

from pydantic import BaseModel, ValidationError, model_validator

from matrx_graph.input_declaration import VariableDefinition, upgrade_agent_variable

# ============================================================================
# AGENT VARIABLE
# ============================================================================

#: The ``binding.kind`` of a variable filled by a MERGE FIELD (data kits P1). A binding
#: with no ``kind`` is the original scope-context-item binding, unchanged.
MERGE_FIELD_BINDING_KIND = "merge_field"


def _variant_of(binding: dict[str, Any]) -> str | None:
    """The System item variant a binding asks for (``variant``), or None for the default."""
    v = binding.get("variant")
    return v.strip() if isinstance(v, str) and v.strip() else None


class AgentVariable(BaseModel):
    """One declared agent variable at run time: its declaration plus the run's value.

    The declaration IS the one input declaration (``variable_definition``,
    ``matrx_ai.agents.input_declaration``), stored here as the dict
    ``upgrade_agent_variable`` returns, so a stored element of any age reads the same and an
    unknown component type never drops a definition. Nothing here re-declares that shape:
    ``name`` / ``default_value`` / ``required`` / ``help_text`` / ``custom_component`` /
    ``binding`` / ``control`` are read-only views of it. ``value`` is the run's own value.
    """

    declaration: dict[str, Any]
    value: Any = None

    @model_validator(mode="before")
    @classmethod
    def _upgrade(cls, data: Any) -> Any:
        if isinstance(data, dict) and isinstance(data.get("declaration"), dict):
            return {**data, "declaration": upgrade_agent_variable(data["declaration"])}
        return data

    @classmethod
    def declare(cls, name: str, *, value: Any = None, **declared: Any) -> "AgentVariable":
        """Build one from declaration keys (``defaultValue=``, ``customComponent=``, …).

        Strict: the keys are validated against ``VariableDefinition``, so a key the declaration
        does not have is refused here rather than carried. Stored rows go through ``from_dict``.
        """
        definition = VariableDefinition.model_validate({"name": name, **declared})
        return cls(declaration=definition.model_dump(mode="json", exclude_none=True), value=value)

    @property
    def name(self) -> str:
        return str(self.declaration.get("name") or "")

    @property
    def default_value(self) -> Any:
        return self.declaration.get("defaultValue")

    @property
    def required(self) -> bool:
        return bool(self.declaration.get("required"))

    @property
    def help_text(self) -> str | None:
        return self.declaration.get("helpText")

    @property
    def custom_component(self) -> dict[str, Any] | None:
        cc = self.declaration.get("customComponent")
        return cc if isinstance(cc, dict) else None

    @property
    def binding(self) -> dict[str, Any] | None:
        b = self.declaration.get("binding")
        return b if isinstance(b, dict) else None

    @property
    def control(self) -> dict[str, Any] | None:
        c = self.declaration.get("control")
        return c if isinstance(c, dict) else None

    def definition(self) -> VariableDefinition | None:
        """The declaration as the generated model, or None when it does not validate (yet)."""
        try:
            return VariableDefinition.model_validate(self.declaration)
        except ValidationError:
            return None

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

        Shape (when bound): ``{"list_id": str, "multiple": bool}``, plus ``label_column`` /
        ``deliver_column`` when the variable picks a row of any Table. Sourced from the
        agent definition (``customComponent.pick_list``, with read-only fallback to
        the legacy ``structured_list`` / ``picklist`` keys for historical defs), NOT from any
        client payload, so a client can only choose WHICH item — never which list.
        """
        cc = self.custom_component
        if not isinstance(cc, dict):
            return None
        # Canonical key is `pick_list`; `structured_list` and `picklist` are legacy read-only aliases.
        pl = cc.get("pick_list") or cc.get("structured_list") or cc.get("picklist")
        if not isinstance(pl, dict):
            return None
        list_id = pl.get("listId") or pl.get("list_id")
        if not isinstance(list_id, str) or not list_id:
            return None
        binding: dict[str, Any] = {"list_id": list_id, "multiple": bool(pl.get("multiple", False))}
        # A ROW OF ANY TABLE (``labelColumn``): ``list_id`` is that Table's id, the person sees
        # ``labelColumn`` and the agent receives ``deliverColumn`` of the picked row (absent: the
        # whole row), resolved live through a table_cell / table_row reference fence.
        label_column = pl.get("labelColumn")
        if isinstance(label_column, str) and label_column:
            binding["label_column"] = label_column
            deliver_column = pl.get("deliverColumn")
            binding["deliver_column"] = (
                deliver_column if isinstance(deliver_column, str) and deliver_column else None
            )
        return binding

    def scope_binding(self) -> dict[str, Any] | None:
        """Return the normalized scope-context binding for this variable, or None.

        Shape (when bound): ``{"context_item_id", "scope_type_id", "item_key", "on_missing",
        "variant"}`` — ``variant`` names which of a System item's variants the variable reads
        (None: the item's default).
        Sourced from the agent definition (``binding``), accepting both camelCase (FE) and
        snake_case keys. ``item_key`` is what the server resolves against the active scope's
        context items; ``on_missing`` is one of ``empty | skip | error`` (default ``empty``).
        """
        b = self.binding
        if not isinstance(b, dict):
            return None
        if b.get("kind") == MERGE_FIELD_BINDING_KIND:
            # The second binding kind is never a scope binding (see merge_field_binding).
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
            "variant": _variant_of(b),
        }

    def merge_field_binding(self) -> dict[str, Any] | None:
        """Return this variable's merge-field declaration, or None.

        The second binding kind (data kits P1). The binding IS a merge-field declaration —
        exactly the snake_case document ``matrx_records.merge.declaration.parse`` reads —
        with ``kind: "merge_field"`` and the ``key`` implied by the variable's name::

            {"kind": "merge_field", "source": "record",
             "semantic_type": "collection" | "reference" | "value",
             "table_id": "<uuid>", "record_id"?: "<uuid>", "field_key"?: "<key>",
             "match"?: {field_key: value}, "sort"?: {"field": "<key>", "dir": "asc"|"desc"},
             "limit"?: 40,
             "transform"?: {"name": "list", "template": "- {purpose}: {model.name}",
                            "join": "\n", "max": 40},
             "missing"?: "absent" | "block", "override_policy"?: "shown_locked"}

        Returned verbatim (minus ``kind``, plus ``key``) — this package never judges the
        shape; the host parses it and names what is wrong, so a malformed binding is
        announced rather than dropped.
        """
        b = self.binding
        if not isinstance(b, dict) or b.get("kind") != MERGE_FIELD_BINDING_KIND:
            return None
        declaration = {k: v for k, v in b.items() if k != "kind"}
        declaration["key"] = self.name
        return declaration

    @classmethod
    def from_dict(cls, var_def: dict[str, Any]) -> "AgentVariable":
        """One stored ``variable_definitions`` element (any age) -> AgentVariable (tolerant)."""
        return cls(declaration=var_def)

    @staticmethod
    def from_list(var_defs: list | None) -> dict[str, "AgentVariable"]:
        """A stored ``variable_definitions`` list -> ``{name: AgentVariable}``.

        Every element passes through the one tolerant door; an element with no name (or not an
        object) is not a variable and is skipped.
        """
        out: dict[str, AgentVariable] = {}
        for var_def in var_defs or []:
            if isinstance(var_def, dict) and var_def.get("name"):
                variable = AgentVariable.from_dict(var_def)
                out[variable.name] = variable
        return out

    def to_dict(self) -> dict[str, Any]:
        """The declaration (the one input declaration's shape, with ``__kind``)."""
        return dict(self.declaration)


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


def merge_field_bindings_from_variables(
    variable_defaults: dict[str, "AgentVariable"] | None,
) -> dict[str, dict[str, Any]]:
    """``{var_name: merge_field_declaration}`` for every variable whose binding is a merge
    field (see ``AgentVariable.merge_field_binding``). Authored on the agent, so a client
    can never choose which Table a variable reads."""
    out: dict[str, dict[str, Any]] = {}
    for name, var in (variable_defaults or {}).items():
        reader = getattr(var, "merge_field_binding", None)
        declaration = reader() if callable(reader) else None
        if declaration is not None:
            out[name] = declaration
    return out


_TOGGLE_TYPES = ("toggle", "light-switch")


def _toggle_off_label(declared: Any) -> str | None:
    """The off label a toggle run form sends (``toggleValues[0]``, default "No"), else None."""
    cc = getattr(declared, "custom_component", None)
    if not isinstance(cc, dict) or cc.get("type") not in _TOGGLE_TYPES:
        return None
    labels = cc.get("toggleValues") or (cc.get("stash") or {}).get("toggleValues") or []
    return str(labels[0]) if labels else "No"


def _cleared(value: Any) -> bool:
    """The person emptied the field on purpose: blank or whitespace-only text, or an emptied list/dict
    (the client sends the saved default for an untouched field and ``None`` when there is none). The
    screen shows a whitespace-only value as blank, so it is honored as blank: never the default."""
    if isinstance(value, str):
        return not value.strip()
    return isinstance(value, (list, tuple, dict)) and not value


def is_cleared_client_value(value: Any) -> bool:
    """THE one cleared test (public): a client value the composition honors as ``""``."""
    return _cleared(value)


def is_platform_key(name: str) -> bool:
    """A key a door adds for its own use, never a person's variable: ``vsc_*`` (editor state) or a
    ``__name__`` dunder (``__agent_user_input__``)."""
    return name.startswith("vsc_") or (len(name) > 4 and name.startswith("__") and name.endswith("__"))


def compose_variable_values(
    definitions: Mapping[str, Any] | None,
    client: Mapping[str, Any] | None = None,
    bound: Mapping[str, Any] | None = None,
    *,
    defaults: Mapping[str, Any] | None = None,
    ignore_client: Collection[str] = (),
    declared_only: bool | None = None,
) -> dict[str, Any]:
    """THE one composition of a run's first-turn values, used by every door.

    For each DECLARED name: explicit non-empty client value > non-empty bound value > non-empty
    saved default > ``""``. Empty is ``template_substitution.is_empty_value``. The one exception
    is intent made explicit on the wire: a client value of exactly ``""`` means the person
    cleared the field, and is honored as ``""`` (beats bound and default); whitespace-only text
    and an emptied list or dict (a cleared multi-select / pick list) are the same. ``None`` / key
    absent mean untouched and fall back. A toggle whose
    value is its off label becomes an ``OffValue`` (fills as its text, empties a section).
    ``defaults`` adds or overrides saved defaults by name (raw values); ``ignore_client`` names
    whose client value is discarded (a locked merge field).

    Undeclared client keys (``declared_only``, default: on when ``definitions`` is non-empty): a
    key no definition declares is DROPPED, so it can never fill the author's text. Platform keys
    (``is_platform_key``) still pass through for their door's own use, marked
    (``as_platform_value``, any type) so substitution never fills them. With no definitions at all (a raw ``/ai/chat`` call whose
    ``variables`` dict IS the declaration) every client key passes through unchanged and fills:
    today's behavior, kept on purpose. A stored agent's door passes ``declared_only=True``: its
    definitions are the declaration even when they declare nothing."""
    from matrx_ai.config.template_substitution import OffValue, as_platform_value, is_empty_value

    definitions = definitions or {}
    if declared_only is None:
        declared_only = bool(definitions)
    floor: dict[str, Any] = {}
    for name, declared in definitions.items():
        value = getattr(declared, "value", None)
        floor[name] = value if not is_empty_value(value) else getattr(declared, "default_value", None)
    floor.update(defaults or {})

    out: dict[str, Any] = {}
    for name, value in floor.items():
        out[name] = "" if is_empty_value(value) else value
    for name, value in (bound or {}).items():
        if not is_empty_value(value) or name not in out:
            out[name] = "" if value is None else value
    for name, value in (client or {}).items():
        if name in ignore_client:
            continue
        if name not in floor and name not in (bound or {}):
            if not declared_only:
                out[name] = value  # no declaration at all: the client's dict IS the declaration
            elif is_platform_key(name):
                # A door's own key: kept for that door, never filled into text.
                out[name] = as_platform_value(value)
            # else: undeclared — dropped, never fills the author's text
        elif _cleared(value):
            out[name] = ""  # the person cleared it ("" or an emptied multi-select): honored as "", never the default
        elif not is_empty_value(value):
            out[name] = value
    for name, declared in definitions.items():
        off = _toggle_off_label(declared)
        if off is not None and isinstance(out.get(name), str) and out[name] == off:
            out[name] = OffValue(out[name])
    return out
