from ocsf.events.discovery import DiscoveryResult

from ocsf.objects.job import Job

class JobQuery(DiscoveryResult):
    """
    Job Query events report information about scheduled jobs.
    """

    class_uid: int = 5010
    class_name: str = 'Job Query'

    job: Job
