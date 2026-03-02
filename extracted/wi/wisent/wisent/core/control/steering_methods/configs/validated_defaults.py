"""Validated default parameters for each steering method.

Each dict contains only parameters with empirically validated
general-purpose defaults. Parameters absent from a dict have no
validated default and MUST be supplied by the optimizer config
(model+task overrides) or explicitly by the user.

Auto-computed parameters (sensor_layer, steering_layers, etc.)
are intentionally absent here -- they are determined at runtime
from the model architecture.
"""

from wisent.core.utils.config_tools.constants import (
    TECZA_NUM_DIRECTIONS,
    DEFAULT_OPTIMIZATION_STEPS,
    TECZA_LEARNING_RATE,
    TECZA_RETAIN_WEIGHT,
    TECZA_INDEPENDENCE_WEIGHT,
    TECZA_MIN_COSINE_SIM,
    TECZA_MAX_COSINE_SIM,
    TETNO_CONDITION_THRESHOLD,
    TETNO_GATE_TEMPERATURE,
    TETNO_ENTROPY_FLOOR,
    TETNO_ENTROPY_CEILING,
    TETNO_MAX_ALPHA,
    GROM_NUM_DIRECTIONS,
    GROM_OPTIMIZATION_STEPS,
    GROM_LEARNING_RATE,
    GROM_BEHAVIOR_WEIGHT,
    GROM_RETAIN_WEIGHT,
    GROM_SPARSE_WEIGHT,
    GROM_MAX_ALPHA,
    MLP_HIDDEN_DIM,
    MLP_NUM_LAYERS,
    MLP_DROPOUT,
    MLP_LEARNING_RATE,
    DEFAULT_WEIGHT_DECAY,
    DEFAULT_VARIANCE_THRESHOLD,
    NURT_TRAINING_EPOCHS,
    NURT_NUM_INTEGRATION_STEPS,
    NURT_T_MAX,
    SZLAK_SINKHORN_REG,
    SZLAK_INFERENCE_K,
    PRZELOM_EPSILON,
    TIKHONOV_REG,
    BROYDEN_DEFAULT_NUM_STEPS,
    BROYDEN_DEFAULT_ALPHA,
    BROYDEN_DEFAULT_ETA,
    BROYDEN_DEFAULT_BETA,
    BROYDEN_DEFAULT_ALPHA_DECAY,
    DEFAULT_STRENGTH,
)

VALIDATED_METHOD_DEFAULTS = {
    "caa": {
        "normalize": True,
    },
    "ostrze": {
        "normalize": True,
        "C": DEFAULT_STRENGTH,
    },
    "tecza": {
        "num_directions": TECZA_NUM_DIRECTIONS,
        "optimization_steps": DEFAULT_OPTIMIZATION_STEPS,
        "learning_rate": TECZA_LEARNING_RATE,
        "retain_weight": TECZA_RETAIN_WEIGHT,
        "independence_weight": TECZA_INDEPENDENCE_WEIGHT,
        "normalize": True,
        "use_caa_init": True,
        "cone_constraint": True,
        "min_cosine_similarity": TECZA_MIN_COSINE_SIM,
        "max_cosine_similarity": TECZA_MAX_COSINE_SIM,
    },
    "tetno": {
        "per_layer_scaling": True,
        "condition_threshold": TETNO_CONDITION_THRESHOLD,
        "gate_temperature": TETNO_GATE_TEMPERATURE,
        "learn_threshold": True,
        "use_entropy_scaling": True,
        "entropy_floor": TETNO_ENTROPY_FLOOR,
        "entropy_ceiling": TETNO_ENTROPY_CEILING,
        "max_alpha": TETNO_MAX_ALPHA,
        "optimization_steps": DEFAULT_OPTIMIZATION_STEPS,
        "learning_rate": TECZA_LEARNING_RATE,
        "normalize": True,
    },
    "grom": {
        "num_directions": GROM_NUM_DIRECTIONS,
        "optimization_steps": GROM_OPTIMIZATION_STEPS,
        "learning_rate": GROM_LEARNING_RATE,
        "behavior_weight": GROM_BEHAVIOR_WEIGHT,
        "retain_weight": GROM_RETAIN_WEIGHT,
        "sparse_weight": GROM_SPARSE_WEIGHT,
        "max_alpha": GROM_MAX_ALPHA,
        "normalize": True,
    },
    "mlp": {
        "hidden_dim": MLP_HIDDEN_DIM,
        "num_layers": MLP_NUM_LAYERS,
        "dropout": MLP_DROPOUT,
        "epochs": DEFAULT_OPTIMIZATION_STEPS,
        "learning_rate": MLP_LEARNING_RATE,
        "weight_decay": DEFAULT_WEIGHT_DECAY,
        "normalize": True,
    },
    "nurt": {
        "variance_threshold": DEFAULT_VARIANCE_THRESHOLD,
        "training_epochs": NURT_TRAINING_EPOCHS,
        "lr": MLP_LEARNING_RATE,
        "num_integration_steps": NURT_NUM_INTEGRATION_STEPS,
        "t_max": NURT_T_MAX,
    },
    "szlak": {
        "sinkhorn_reg": SZLAK_SINKHORN_REG,
        "inference_k": SZLAK_INFERENCE_K,
    },
    "wicher": {
        "variance_threshold": DEFAULT_VARIANCE_THRESHOLD,
        "num_steps": BROYDEN_DEFAULT_NUM_STEPS,
        "alpha": BROYDEN_DEFAULT_ALPHA,
        "eta": BROYDEN_DEFAULT_ETA,
        "beta": BROYDEN_DEFAULT_BETA,
        "alpha_decay": BROYDEN_DEFAULT_ALPHA_DECAY,
    },
    "przelom": {
        "epsilon": PRZELOM_EPSILON,
        "target_mode": "uniform",
        "regularization": TIKHONOV_REG,
        "inference_k": SZLAK_INFERENCE_K,
    },
}
