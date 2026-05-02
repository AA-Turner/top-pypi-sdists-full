"""Reflex Enterprise package."""

from reflex.utils import lazy_loader

# Imported for serializer side effects
import reflex_enterprise.vars as _  # noqa: F401

_MANTINE_MAPPING = {
    "components.mantine.autocomplete": ["autocomplete"],
    "components.mantine.collapse": ["collapse"],
    "components.mantine.combobox": ["combobox"],
    "components.mantine.json_input": ["json_input"],
    "components.mantine.loading_overlay": ["loading_overlay"],
    "components.mantine.multi_select": ["multi_select"],
    "components.mantine.number_formatter": ["number_formatter"],
    "components.mantine.pill": ["pill"],
    "components.mantine.pills_input": ["pills_input"],
    "components.mantine.ring_progress": ["ring_progress"],
    "components.mantine.semi_circle_progress": ["semi_circle_progress"],
    "components.mantine.spoiler": ["spoiler"],
    "components.mantine.tags_input": ["tags_input"],
    "components.mantine.tree": ["tree"],
    "components.mantine.timeline": ["timeline"],
    "components.mantine.dates": ["dates"],
}

_SUBMODULES = {"components"}
_SUBMOD_ATTRS = {
    "app": [("AppEnterprise", "App")],
    "utils": ["arrow_func"],
    "config": [("ConfigEnterprise", "Config")],
    "components": ["mantine"],
    "components.ag_grid": ["ag_grid"],
    "components.ag_charts": ["ag_chart"],
    **_MANTINE_MAPPING,
    "components.ag_grid.wrapper": [
        "model_wrapper",
        "model_wrapper_ssrm",
        "ModelWrapper",
        "ModelWrapperSSRM",
    ],
    "components.dnd": ["dnd"],
    "components.flow": ["flow"],
    "components.map": ["map"],
    "vars": [
        "ArgsFunctionOperationPromise",
        "PassthroughAPI",
        "ElementAPI",
        "JSAPIVar",
        "LambdaVar",
        "LiteralLambdaVar",
        "PromiseVar",
        "is_static",
        "static",
    ],
    "plugins": ["EventHandlerAPIPlugin"],
}

getattr, __dir__, __all__ = lazy_loader.attach(
    __name__,
    submodules=_SUBMODULES,
    submod_attrs=_SUBMOD_ATTRS,
)


def __getattr__(name: str):
    return getattr(name)
