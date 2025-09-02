from dataclasses import dataclass, field
from typing import List, Any

@dataclass
class Config:
    # Parámetros de simulación
    other_method: bool = True
    activate_generate_relax: bool = True
    generate_relax: List[Any] = field(default_factory=lambda: ["bcc", "2.55", 10, 10, 10])
    relax: str = "inputs/dump/fe0"
    defect: List[str] = field(default_factory=lambda: ["inputs/dump/fe4"])
    radius: int = 2
    smoothing_level: int = 0
    smoothing_level_training: int = 0
    cutoff: int = 3
    radius_training: int = 3
    cluster_tolerance: int = 2
    divisions_of_cluster: int = 6
    iteraciones_clusterig: int = 4

    # Columnas para predicción
    PREDICTOR_COLUMNS: List[str] = field(default_factory=lambda: [
        "surface_area",
        "filled_volume",
        "cluster_size",
        "mean_distance",
    ])
