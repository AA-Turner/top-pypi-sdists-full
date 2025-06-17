######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.17.1+obcheckpoint(0.2.1);ob(v1)                                                   #
# Generated on 2025-06-16T20:11:02.882812                                                            #
######################################################################################################

from __future__ import annotations



TYPE_CHECKING: bool

class JobOutcomes(object, metaclass=type):
    ...

def derive_jobset_outcome(jobset_status):
    ...

def derive_job_outcome(job_status: "V1JobStatus"):
    ...

class PodKiller(object, metaclass=type):
    def __init__(self, kubernetes_client, echo_func, namespace):
        ...
    def process_matching_jobs_and_jobsets(self, flow_name, run_id, user):
        """
        Process all matching jobs and jobsets based on their derived outcomes
        """
        ...
    ...

