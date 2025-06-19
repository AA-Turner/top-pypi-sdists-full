from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from kubernetes.client.models.v1_job import V1Job
    from kubernetes.client.models.v1_job_status import V1JobStatus


def _is_jobset_child(job: "V1Job"):
    if job.metadata.owner_references:
        for owner_ref in job.metadata.owner_references:
            if owner_ref.kind == "JobSet":
                return owner_ref
    return None


class JobOutcomes:
    KILL = "kill"
    DELETE = "delete"
    LEAVE_UNCHANGED = "leave_unchanged"


def derive_jobset_outcome(jobset_status):
    return (
        JobOutcomes.LEAVE_UNCHANGED
        if jobset_status.get("terminalState", None)
        else JobOutcomes.DELETE
    )


def derive_job_outcome(job_status: "V1JobStatus"):
    if job_status.start_time is None:
        # If the job has not started even then just wipe it!
        return JobOutcomes.DELETE
    if job_status.succeeded or job_status.failed:
        return JobOutcomes.LEAVE_UNCHANGED

    if job_status.completion_time is not None:
        return JobOutcomes.LEAVE_UNCHANGED

    # This means that the job has neither finished or succedded.
    if job_status.active:
        return JobOutcomes.DELETE

    # This means that the job is not active. Had started. There is not succedded/fail.
    # This is a weird state. Better to just kill the job
    return JobOutcomes.DELETE


class PodKiller:
    def __init__(self, kubernetes_client, echo_func, namespace, progress_bar=None):
        self.client = kubernetes_client
        self.echo = echo_func
        self.api_instance = self.client.CoreV1Api()
        self.job_api = self.client.BatchV1Api()
        self._namespace = namespace
        self.jobset_api = None
        self.jobset_api = self.client.CustomObjectsApi()
        self.progress_bar = progress_bar

    def _delete_jobset(self, owner_ref, namespace):
        """Delete a JobSet if it's the owner of a job."""
        if not self.jobset_api:
            self.echo("JobSet API not available, cannot delete JobSet\n")
            return False

        try:
            jobset_name = owner_ref.name
            self.echo(f"Deleting JobSet: {jobset_name}\n")

            self.jobset_api.delete_namespaced_custom_object(
                group="jobset.x-k8s.io",
                version="v1alpha2",
                namespace=namespace,
                plural="jobsets",
                name=jobset_name,
            )
            return True
        except Exception as e:
            self.echo(f"Failed to delete JobSet {owner_ref.name}: {str(e)}\n")
            return False

    def _delete_job(self, job_name, namespace):
        """Delete a Batch Job and check for JobSet owner reference."""
        try:
            # First get the job to check for owner references
            job = self.job_api.read_namespaced_job(name=job_name, namespace=namespace)
            # Check for JobSet owner reference
            jobset_ref = _is_jobset_child(job)
            if jobset_ref:
                if self._delete_jobset(jobset_ref, namespace):
                    return True

            # If no JobSet owner or JobSet deletion failed, delete the job
            self.echo(f"Deleting Batch Job: {job_name}")
            self.job_api.delete_namespaced_job(
                name=job_name, namespace=namespace, propagation_policy="Background"
            )
            return True

        except Exception as e:
            self.echo(f"Failed to delete job {job_name}: {str(e)}")
            return False

    def _kill_pod_process(self, pod):
        """Attempt to kill processes inside a pod."""
        from kubernetes.stream import stream

        try:
            stream(
                self.api_instance.connect_get_namespaced_pod_exec,
                name=pod.metadata.name,
                namespace=pod.metadata.namespace,
                command=["/bin/sh", "-c", "/sbin/killall5"],
                stderr=True,
                stdin=False,
                stdout=True,
                tty=False,
            )
            return True
        except Exception as e:
            self.echo(
                f"Failed to kill processes in pod {pod.metadata.name}: {str(e)}\n"
            )
            return False

    @staticmethod
    def _metaflow_matching_spec(run_id, user, flow_name, annotations, labels):
        # Handle argo prefixes in run_id like in _find_active_pods
        _argo_run_id = None
        if run_id is not None:
            _argo_run_id = run_id[run_id.startswith("argo-") and len("argo-") :]
        return (
            annotations
            and (
                run_id is None
                or (annotations.get("metaflow/run_id") == run_id)
                # we want to also match jobsets launched by argo-workflows
                # This line has no real value since the We already avoid any
                # argo-workflows related terminations.
                or (
                    labels.get("workflows.argoproj.io/workflow") is not None
                    and labels.get("workflows.argoproj.io/workflow") == _argo_run_id
                )
            )
            and (user is None or annotations.get("metaflow/user") == user)
            and (annotations.get("metaflow/flow_name") == flow_name)
        )

    def _find_matching_jobs(self, flow_name, run_id=None, user=None):
        """Find jobs that match the flow_name, run_id, and user criteria using similar logic to _find_active_pods"""

        def paginated_job_finder(namespace):
            continue_token = None
            while True:
                response = self.job_api.list_namespaced_job(
                    namespace=namespace, limit=100, _continue=continue_token
                )
                yield response.items
                continue_token = response.metadata._continue
                if not continue_token:
                    break

        try:
            matching_jobs = []
            for _jobs in paginated_job_finder(self._namespace):
                for job in _jobs:
                    _match = self._metaflow_matching_spec(
                        run_id=run_id,
                        user=user,
                        flow_name=flow_name,
                        annotations=job.metadata.annotations,
                        labels=job.metadata.labels,
                    )
                    if _match:
                        matching_jobs.append(job)
            return matching_jobs
        except Exception as e:
            self.echo(f"Error finding jobs: {str(e)}\n")
            return []

    def _find_matching_jobsets(self, flow_name, run_id=None, user=None):
        """Find jobsets that match the flow_name, run_id, and user criteria using similar logic to _find_active_pods"""
        if not self.jobset_api:
            return []

        def paginated_jobset_finder(namespace):
            continue_token = None
            responses = []
            while True:
                response = self.jobset_api.list_namespaced_custom_object(
                    group="jobset.x-k8s.io",
                    version="v1alpha2",
                    namespace=namespace,
                    plural="jobsets",
                    limit=100,
                    **({"_continue": continue_token} if continue_token else {}),
                )
                continue_token = response.get("metadata", {}).get("continue", None)
                responses.append(response)
                if not continue_token:
                    break
            return responses

        try:
            matching_jobsets = []

            for jobset_response in paginated_jobset_finder(self._namespace):
                for jobset in jobset_response.get("items", []):
                    _match = self._metaflow_matching_spec(
                        run_id=run_id,
                        user=user,
                        flow_name=flow_name,
                        annotations=jobset.get("metadata", {}).get("annotations", {}),
                        labels=jobset.get("metadata", {}).get("labels", {}),
                    )
                    if _match:
                        matching_jobsets.append(jobset)

            return matching_jobsets
        except Exception as e:
            self.echo(f"Error finding jobsets: {str(e)}\n")
            return []

    def _kill_pods_for_job(self, job):
        """Find and kill pods associated with a specific job"""
        job_name = job.metadata.name
        namespace = job.metadata.namespace

        try:
            # Find pods with the job-name label matching this job
            pods = self.api_instance.list_namespaced_pod(
                namespace=namespace, label_selector=f"job-name={job_name}"
            )

            killed_pods = 0
            for pod in pods.items:
                if pod.status.phase in ["Running"]:
                    self.echo(
                        f"Killing processes in pod {pod.metadata.name} for job {job_name}"
                    )
                    if self._kill_pod_process(pod):
                        killed_pods += 1

            return killed_pods > 0
        except Exception as e:
            self.echo(f"Failed to find/kill pods for job {job_name}: {str(e)}")
            return False

    def _handle_job_outcome(self, job, outcome):
        """Handle a job based on the derived outcome"""
        job_name = job.metadata.name
        namespace = job.metadata.namespace

        if outcome == JobOutcomes.LEAVE_UNCHANGED:
            # self.echo(f"Job {job_name} is in terminal state, leaving unchanged")
            return None
        elif outcome == JobOutcomes.DELETE:
            self.echo(f"Deleting Job {job_name}")
            return self._delete_job(job_name, namespace)
        elif outcome == JobOutcomes.KILL:
            self.echo(f"Killing Job {job_name}")
            # First try to kill the pod processes
            pods_killed = self._kill_pods_for_job(job)
            if pods_killed > 0:
                return True
            # Worst case if we are not able to delete any pod, then delete the Job.
            return self._delete_job(job_name, namespace)
        else:
            self.echo(f"Unknown outcome {outcome} for job {job_name}\n")
            return False

    def _handle_jobset_outcome(self, jobset, outcome):
        """Handle a jobset based on the derived outcome"""
        jobset_name = jobset.get("metadata", {}).get("name", "unknown")
        namespace = jobset.get("metadata", {}).get("namespace", self._namespace)

        if outcome == JobOutcomes.LEAVE_UNCHANGED:
            # self.echo(f"JobSet {jobset_name} is in terminal state, leaving unchanged")
            return None
        elif outcome == JobOutcomes.DELETE:
            self.echo(f"Deleting JobSet {jobset_name}")
            try:
                self.jobset_api.delete_namespaced_custom_object(
                    group="jobset.x-k8s.io",
                    version="v1alpha2",
                    namespace=namespace,
                    plural="jobsets",
                    name=jobset_name,
                )
                return True
            except Exception as e:
                self.echo(f"Failed to delete JobSet {jobset_name}: {str(e)}")
                return False
        else:
            self.echo(f"Unknown outcome {outcome} for JobSet {jobset_name}")
            return False

    def extract_matching_jobs_and_jobsets(self, flow_name, run_id, user):
        """Extract matching jobs and jobsets based on the flow_name, run_id, and user criteria"""
        jobs = self._find_matching_jobs(flow_name, run_id, user)
        jobsets = self._find_matching_jobsets(flow_name, run_id, user)
        return [(j, derive_job_outcome(j.status)) for j in jobs], [
            (j, derive_jobset_outcome(j.get("status", {}))) for j in jobsets
        ]

    def process_matching_jobs_and_jobsets(self, flow_name, run_id, user):
        """Process all matching jobs and jobsets based on their derived outcomes"""
        results = []
        progress_update = lambda x: x
        if self.progress_bar:
            progress_update = lambda x: self.progress_bar.update(1, x)

        # Process matching jobs
        _jobs, _jobsets = [], []
        jobs = self._find_matching_jobs(flow_name, run_id, user)
        for job in jobs:
            outcome = derive_job_outcome(job.status)
            result = self._handle_job_outcome(job, outcome)
            # results.append(result)
            if result is not None:
                progress_update("💀 Killing Job %s" % job.metadata.name)
                results.append(result)
                _jobs.append(result)

        # Process matching jobsets
        jobsets = self._find_matching_jobsets(flow_name, run_id, user)
        for jobset in jobsets:
            jobset_status = jobset.get("status", {})
            outcome = derive_jobset_outcome(jobset_status)
            result = self._handle_jobset_outcome(jobset, outcome)
            if result is not None:
                progress_update(
                    "💀 Deleting JobSet %s"
                    % jobset.get("metadata", {}).get("name", "unknown")
                )
                results.append(result)
                _jobsets.append(result)

        return results, len(_jobs), len(_jobsets)

    def process_matching_jobs_and_jobsets_force_all(self, flow_name, run_id, user):
        """Force process ALL matching jobs and jobsets regardless of their status/outcome"""
        results = []
        progress_update = lambda x: x
        if self.progress_bar:
            progress_update = lambda x: self.progress_bar.update(1, x)

        # Process matching jobs - FORCE DELETE ALL
        _jobs, _jobsets = [], []
        jobs = self._find_matching_jobs(flow_name, run_id, user)
        for job in jobs:
            # Force DELETE outcome regardless of actual status
            result = self._handle_job_outcome(job, JobOutcomes.DELETE)
            progress_update("🔥 FORCE Deleting Job %s" % job.metadata.name)
            results.append(
                result if result is not None else True
            )  # Treat None as success for force mode
            _jobs.append(result if result is not None else True)

        # Process matching jobsets - FORCE DELETE ALL
        jobsets = self._find_matching_jobsets(flow_name, run_id, user)
        for jobset in jobsets:
            # Force DELETE outcome regardless of actual status
            result = self._handle_jobset_outcome(jobset, JobOutcomes.DELETE)
            progress_update(
                "🔥 FORCE Deleting JobSet %s"
                % jobset.get("metadata", {}).get("name", "unknown")
            )
            results.append(
                result if result is not None else True
            )  # Treat None as success for force mode
            _jobsets.append(result if result is not None else True)

        return results, len(_jobs), len(_jobsets)
