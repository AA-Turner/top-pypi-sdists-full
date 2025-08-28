######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.18.0.1+obcheckpoint(0.2.4);ob(v1)                                                    #
# Generated on 2025-08-28T00:53:38.155472                                                            #
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

