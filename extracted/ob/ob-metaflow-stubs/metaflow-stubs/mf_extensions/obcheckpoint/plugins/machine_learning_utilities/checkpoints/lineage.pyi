######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.19.18.1+obcheckpoint(0.2.10);ob(v1)                                                  #
# Generated on 2026-02-03T01:51:07.236957                                                            #
######################################################################################################

from __future__ import annotations

import typing
if typing.TYPE_CHECKING:
    import metaflow.mf_extensions.obcheckpoint.plugins.machine_learning_utilities.datastructures

from ......metadata_provider.metadata import MetaDatum as MetaDatum
from ..datastructures import CheckpointArtifact as CheckpointArtifact
from .core import CheckpointReferenceResolver as CheckpointReferenceResolver

TYPE_CHECKING: bool

def checkpoint_load_related_metadata(checkpoint: metaflow.mf_extensions.obcheckpoint.plugins.machine_learning_utilities.datastructures.CheckpointArtifact, current_attempt):
    ...

def trace_lineage(flow, checkpoint: metaflow.mf_extensions.obcheckpoint.plugins.machine_learning_utilities.datastructures.CheckpointArtifact):
    """
    Trace the lineage of the checkpoint by tracing the previous paths.
    """
    ...

