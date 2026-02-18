"""Steering methods package."""

from .methods.caa import CAAMethod
from .methods.advanced import PRISMMethod, PRISMConfig, MultiDirectionResult
from .methods.advanced import PULSEMethod, PULSEConfig, PULSEResult
from .methods.titan import TITANMethod, TITANConfig, TITANResult, GatingNetwork, IntensityNetwork
from .methods.concept_flow import ConceptFlowMethod, ConceptFlowConfig, ConceptFlowResult
from .rotator import SteeringMethodRotator
from .registry import (
    SteeringMethodRegistry,
    SteeringMethodDefinition,
    SteeringMethodParameter,
    SteeringMethodType,
    get_steering_method,
    list_steering_methods,
    is_valid_steering_method,
)

# Aliases for backward compatibility
CAA = CAAMethod
PRISM = PRISMMethod
PULSE = PULSEMethod
TITAN = TITANMethod
ConceptFlow = ConceptFlowMethod
SteeringMethod = CAAMethod  # Default steering method

__all__ = [
    # Method classes
    "CAAMethod",
    "CAA",
    "PRISMMethod",
    "PRISM",
    "PRISMConfig",
    "MultiDirectionResult",
    "PULSEMethod",
    "PULSE",
    "PULSEConfig",
    "PULSEResult",
    "TITANMethod",
    "TITAN",
    "TITANConfig",
    "TITANResult",
    "GatingNetwork",
    "IntensityNetwork",
    "ConceptFlowMethod",
    "ConceptFlow",
    "ConceptFlowConfig",
    "ConceptFlowResult",
    "SteeringMethod",
    "SteeringMethodRotator",
    # Registry
    "SteeringMethodRegistry",
    "SteeringMethodDefinition",
    "SteeringMethodParameter",
    "SteeringMethodType",
    # Convenience functions
    "get_steering_method",
    "list_steering_methods",
    "is_valid_steering_method",
]
