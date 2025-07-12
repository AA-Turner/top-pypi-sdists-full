######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.21.1+obcheckpoint(0.2.4);ob(v1)                                                   #
# Generated on 2025-07-11T23:29:18.531096                                                            #
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
    def __init__(self, kubernetes_client, echo_func, namespace, progress_bar = None):
        ...
    def extract_matching_jobs_and_jobsets(self, flow_name, run_id, user):
        """
        Extract matching jobs and jobsets based on the flow_name, run_id, and user criteria
        """
        ...
    def process_matching_jobs_and_jobsets(self, flow_name, run_id, user):
        """
        Process all matching jobs and jobsets based on their derived outcomes
        """
        ...
    def process_matching_jobs_and_jobsets_force_all(self, flow_name, run_id, user):
        """
        Force process ALL matching jobs and jobsets regardless of their status/outcome
        """
        ...
    ...

