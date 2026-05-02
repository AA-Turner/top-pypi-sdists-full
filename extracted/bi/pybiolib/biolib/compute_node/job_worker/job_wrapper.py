from biolib.biolib_api_client.job_types import CloudJob, CreatedJobDict
from biolib.compute_node.webserver.webserver_types import ComputeNodeInfo
from biolib.typing_utils import Optional, TypedDict


class JobWrapper(TypedDict):
    access_token: str
    BASE_URL: str  # TODO: refactor this to lower case
    compute_node_info: Optional[ComputeNodeInfo]
    job: CreatedJobDict
    cloud_job: Optional[CloudJob]
    job_temporary_dir: Optional[str]
