from adam.utils_job.job import Job


class JobStatus:
    ts: float = None

    def job_id(self) -> str:
        pass

    def is_running(self) -> bool:
        pass

    def all_completed(self) -> bool:
        pass

    def succeeded(self) -> int:
        pass

    def failed(self) -> int:
        pass

    def running(self) -> int:
        pass

    def with_ts(self, ts: float):
        self.ts = ts

        return self

    def job(self) -> Job:
        pass

class RunningJobStatus(JobStatus):
    def __init__(self, job_id: str):
        super().__init__()
        self._job_id = job_id

    def job_id(self) -> str:
        return self._job_id

    def is_running(self) -> bool:
        return True

    def all_completed(self) -> bool:
        return False

    def succeeded(self) -> int:
        return 0

    def failed(self) -> int:
        return 0

    def running(self) -> int:
        return 1

    def job(self) -> Job:
        return None
