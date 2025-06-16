import requests
from requests.adapters import HTTPAdapter, Retry

BASE_URL = "https://api.ngc.nvidia.com/v2/orgs/zhxkmsaasxhw/"
POLL_SEC = 1


def _session(api_key):
    s = requests.Session()
    s.headers.update(
        {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
    )
    retry = Retry(total=5, backoff_factor=1.5, status_forcelist=[502, 503, 504])
    s.mount("https://", HTTPAdapter(max_retries=retry))
    return s


def _url(path):
    return BASE_URL.rstrip("/") + path


class NVCTClient:
    def __init__(self, api_key):
        self.sess = _session(api_key)

    # TODO: Handle https://outerboundsco.slack.com/archives/C05QGNR4E06/p1745970955540289
    def create(self, spec):
        r = self.sess.post(_url("/nvct/tasks"), json=spec, timeout=30)
        r.raise_for_status()
        return r.json().get("task", {}).get("id")

    def get(self, task_id):
        r = self.sess.get(_url(f"/nvct/tasks/{task_id}"), timeout=30)
        r.raise_for_status()
        return r.json().get("task", {})

    def cancel(self, task_id):
        r = self.sess.post(_url(f"/nvct/tasks/{task_id}/cancel"), timeout=30)
        r.raise_for_status()


class NVCTRequest(object):
    def __init__(self, name):
        self._spec = {}
        self._spec["name"] = name
        self._spec["gpuSpecification"] = {}
        self._spec["resultHandlingStrategy"] = "NONE"
        self._spec["terminationGracePeriodDuration"] = "PT10M"

    def container_image(self, image):
        self._spec["containerImage"] = image
        return self

    def container_args(self, args):
        self._spec["containerArgs"] = args
        return self

    def env(self, key, value):
        env_list = self._spec.setdefault("containerEnvironment", [])
        env_list.append({"key": key, "value": value})
        return self

    def gpu(self, gpu, instance_type, backend):
        gpu_spec = self._spec["gpuSpecification"]
        gpu_spec["gpu"] = gpu
        gpu_spec["instanceType"] = instance_type
        gpu_spec["backend"] = backend
        return self

    def max_runtime(self, iso_duration):
        self._spec["maxRuntimeDuration"] = iso_duration
        return self

    def max_queued(self, iso_duration="PT72H"):
        self._spec["maxQueuedDuration"] = iso_duration
        return self

    def termination_grace(self, iso_duration="PT10M"):
        self._spec["terminationGracePeriodDuration"] = iso_duration
        return self

    def extra(self, key, value):
        self._spec[key] = value
        return self

    def to_dict(self):
        return self._spec


class NVCTTask:
    def __init__(self, client: NVCTClient, spec):
        self.client = client
        self.spec = spec
        self.id = None
        self.record = None

    def submit(self):
        self.id = self.client.create(self.spec)
        return self.id

    def cancel(self):
        if not self.has_finished:
            self.client.cancel(self.id)

    @property
    def status(self):
        self.record = self.client.get(self.id)
        return self.record["status"]

    @property
    def is_waiting(self):
        return self.status == "QUEUED"

    @property
    def is_running(self):
        return self.status in {"RUNNING", "LAUNCHED"}

    @property
    def has_failed(self):
        return self.status in {"ERRORED", "CANCELED"}

    @property
    def has_succeeded(self):
        return self.status == "COMPLETED"

    @property
    def has_finished(self):
        return self.has_succeeded or self.has_failed
