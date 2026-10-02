"""Trajectory clustering settings for MD post-processing."""

from typing import Annotated, Literal

from pydantic import BaseModel, Field, PositiveFloat, PositiveInt


class KMeansClusteringSettings(BaseModel):
    """K-means trajectory clustering settings.

    :param num_clusters: maximum number of clusters
    """

    num_clusters: PositiveInt = 10
    settings_type: Literal["kmeans"] = "kmeans"


class GreedyClusteringSettings(BaseModel):
    """Greedy neighbourhood trajectory clustering settings.

    Frames within `cutoff_angstrom` RMSD of the current cluster centre are
    assigned to that cluster; the centre is chosen greedily as the frame with
    the most unassigned neighbours.

    :param cutoff_angstrom: RMSD neighbourhood cutoff, in Å
    """

    cutoff_angstrom: PositiveFloat = 2.0
    settings_type: Literal["greedy"] = "greedy"


TrajectoryClustering = Annotated[
    KMeansClusteringSettings | GreedyClusteringSettings,
    Field(discriminator="settings_type"),
]
