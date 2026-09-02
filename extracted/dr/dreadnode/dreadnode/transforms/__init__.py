import importlib
import typing as t

from dreadnode.core.transforms import PostTransform, Transform

__lazy_submodules__: list[str] = [
    "advanced_jailbreak",
    "adversarial_suffix",
    "agent_skill",
    "agentic_workflow",
    "art_prompt",
    "audio",
    "backdoor_finetune",
    "browser_agent_attacks",
    "cipher",
    "competitive_parity",
    "constitutional",
    "document",
    "documentation_poison",
    "encoding",
    "exfiltration",
    "flip_attack",
    "guardrail_bypass",
    "ide_injection",
    "image",
    "injection",
    "json_tools",
    "language",
    "logic_bomb",
    "mcp_attacks",
    "multi_agent_attacks",
    "multimodal_attacks",
    "past_tense",
    "persuasion",
    "perturbation",
    "pii_extraction",
    "pythonic_tools",
    "rag_poisoning",
    "reasoning_attacks",
    "refine",
    "response_steering",
    "structural_exploits",
    "stylistic",
    "substitution",
    "supply_chain",
    "swap",
    "system_prompt_extraction",
    "text",
    "video",
    "xml_tools",
]

__lazy_components__: dict[str, str] = {
    "JsonToolMode": "dreadnode.transforms.json_tools",
    "make_tools_to_json_transform": "dreadnode.transforms.json_tools",
    "tools_to_json_in_xml_transform": "dreadnode.transforms.json_tools",
    "tools_to_json_transform": "dreadnode.transforms.json_tools",
    "tools_to_json_with_tag_transform": "dreadnode.transforms.json_tools",
    "make_tools_to_pythonic_transform": "dreadnode.transforms.pythonic_tools",
    "tools_to_pythonic_transform": "dreadnode.transforms.pythonic_tools",
    "make_tools_to_xml_transform": "dreadnode.transforms.xml_tools",
}


def __getattr__(name: str) -> t.Any:
    if name in __lazy_submodules__:
        module = importlib.import_module(f".{name}", __name__)
        globals()[name] = module
        return module

    if name in __lazy_components__:
        module_name = __lazy_components__[name]
        module = importlib.import_module(module_name)
        component = getattr(module, name)
        globals()[name] = component
        return component

    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


def get_transform(identifier: str) -> Transform:
    """
    Get a well-known transform by its identifier.

    Args:
        identifier: The identifier of the transform to retrieve.

    Returns:
        The corresponding transform callable.
    """
    from dreadnode.transforms.json_tools import (
        tools_to_json_in_xml_transform,
        tools_to_json_transform,
        tools_to_json_with_tag_transform,
    )
    from dreadnode.transforms.pythonic_tools import tools_to_pythonic_transform

    match identifier:
        case "json":
            return tools_to_json_transform
        case "json-in-xml":
            return tools_to_json_in_xml_transform
        case "json-with-tag":
            return tools_to_json_with_tag_transform
        case "pythonic":
            return tools_to_pythonic_transform
        case _:
            raise ValueError(f"Unknown transform identifier: {identifier}")


__all__ = [
    "JsonToolMode",
    "PostTransform",
    "Transform",
    "advanced_jailbreak",
    "adversarial_suffix",
    "agent_skill",
    "agentic_workflow",
    "art_prompt",
    "audio",
    "backdoor_finetune",
    "browser_agent_attacks",
    "cipher",
    "competitive_parity",
    "constitutional",
    "document",
    "documentation_poison",
    "encoding",
    "exfiltration",
    "get_transform",
    "guardrail_bypass",
    "ide_injection",
    "image",
    "injection",
    "language",
    "make_tools_to_json_transform",
    "make_tools_to_pythonic_transform",
    "make_tools_to_xml_transform",
    "mcp_attacks",
    "multi_agent_attacks",
    "multimodal_attacks",
    "past_tense",
    "persuasion",
    "perturbation",
    "pii_extraction",
    "rag_poisoning",
    "reasoning_attacks",
    "refine",
    "response_steering",
    "structural_exploits",
    "stylistic",
    "substitution",
    "supply_chain",
    "swap",
    "system_prompt_extraction",
    "text",
    "tools_to_json_in_xml_transform",
    "tools_to_json_transform",
    "tools_to_json_with_tag_transform",
    "tools_to_pythonic_transform",
]
