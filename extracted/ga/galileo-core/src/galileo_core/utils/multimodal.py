from typing import Iterable, Set

from galileo_core.schemas.shared.multimodal import ContentModality, MultimodalCapability, MultimodalCapabilityMapping


def supported_capabilities(modalities: Iterable[ContentModality]) -> Set[MultimodalCapability]:
    """
    Returns the set of supported multimodal capabilities based on the provided modalities.
    A multimodal capability is supported only if ALL of its modalities are present.
    """
    modalities_set = set(modalities) if not isinstance(modalities, set) else modalities
    return {
        capability
        for capability, required_modalities in MultimodalCapabilityMapping.items()
        if modalities_set >= required_modalities
    }
