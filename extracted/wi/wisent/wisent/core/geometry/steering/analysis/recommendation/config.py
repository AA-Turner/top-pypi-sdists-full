"""Configurable recommendation parameters.

All thresholds and score weights live in RecommendationConfig.
"""
from __future__ import annotations
import json
from dataclasses import dataclass, fields, asdict
from pathlib import Path

METHODS = ("CAA", "Hyperplane", "MLP", "PRISM", "PULSE", "TITAN",
           "Concept Flow")


@dataclass(slots=True)
class Thresholds:
    linear_probe_high: float = 0.85
    linear_probe_low: float = 0.65
    nonlinearity_gap_significant: float = 0.05
    icd_high: float = 0.7
    icd_low: float = 0.3
    stability_high: float = 0.8
    stability_low: float = 0.5
    multi_concept_silhouette: float = 0.3
    alignment_high: float = 0.3
    alignment_low: float = 0.1
    variance_concentrated: float = 0.15
    effective_dims_low: float = 20.0
    multi_dir_gain_high: float = 0.05
    coherence_high: float = 0.8
    coherence_low: float = 0.5
    icd_top5_threshold: float = 0.4


@dataclass(slots=True)
class ScoreWeights:
    linear_high_caa: float = 2.0
    linear_high_hyperplane: float = 2.0
    linear_high_cf: float = 1.0
    linear_low_mlp: float = 1.0
    linear_low_pulse: float = 1.0
    linear_low_titan: float = 1.0
    linear_low_cf: float = 0.5
    nonlin_gap_mlp: float = 1.5
    nonlin_gap_pulse: float = 0.5
    nonlin_gap_titan: float = 0.5
    nonlin_gap_cf: float = 1.0
    multi_concept_prism: float = 2.0
    multi_concept_titan: float = 1.0
    multi_concept_cf: float = 1.5
    multi_concept_caa: float = -1.0
    multi_concept_hyperplane: float = -0.5
    stab_high_caa: float = 1.0
    stab_high_hyperplane: float = 0.5
    stab_high_cf: float = 0.5
    stab_low_titan: float = 1.0
    stab_low_pulse: float = 0.5
    stab_low_cf: float = 1.0
    stab_low_caa: float = -0.5
    icd_high_caa: float = 1.0
    icd_high_hyperplane: float = 0.5
    icd_high_cf: float = 0.5
    icd_low_titan: float = 0.5
    icd_low_pulse: float = 0.5
    coh_high_caa: float = 0.5
    coh_low_prism: float = 0.5
    coh_low_titan: float = 0.5
    coh_low_cf: float = 0.5
    var_pc1_cf: float = 1.0
    icd_top5_cf: float = 0.5
    mdir_gain_cf: float = 1.0
    mdir_gain_prism: float = 0.5
    eff_dims_cf: float = 0.5
    not_viable_scale: float = 0.5
    confidence_base: float = 0.5


@dataclass(slots=True)
class RecommendationConfig:
    thresholds: Thresholds
    weights: ScoreWeights

    @staticmethod
    def default() -> RecommendationConfig:
        return RecommendationConfig(
            thresholds=Thresholds(), weights=ScoreWeights())

    def save(self, path: str | Path) -> None:
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(asdict(self), indent=2))

    @classmethod
    def load(cls, path: str | Path) -> RecommendationConfig:
        data = json.loads(Path(path).read_text())
        return cls(thresholds=Thresholds(**data["thresholds"]),
                   weights=ScoreWeights(**data["weights"]))

    def param_count(self) -> int:
        return len(fields(self.thresholds)) + len(fields(self.weights))
