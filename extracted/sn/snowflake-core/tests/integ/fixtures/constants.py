import uuid

from typing import NamedTuple, TypedDict


UUID = str(uuid.uuid4()).replace('-', '_').upper()
TEST_DATABASE = f"INTEGRATION_TEST_{UUID}"
TEST_SCHEMA = f"GH_JOB_{UUID}"
TEST_WAREHOUSE = 'TESTWH_PYTHON'
TEST_COMPUTE_POOL = "test_compute_pool"
TEST_IMAGE_REPO_DATABASE = "TESTDB_PYTHON_AUTO"
TEST_IMAGE_REPO_SCHEMA = "TESTSCHEMA_AUTO"
TEST_IMAGE_REPO_QUALIFIED_SCHEMA = f"{TEST_IMAGE_REPO_DATABASE}.{TEST_IMAGE_REPO_SCHEMA}"
TEST_IMAGE_REPO = "test_image_repo_auto"
DEFAULT_IR_URL = (
    "sfengineering-ss-lprpr-test2.registry.snowflakecomputing.com/"
    + f"{TEST_IMAGE_REPO_DATABASE.lower()}/{TEST_IMAGE_REPO_SCHEMA.lower()}/{TEST_IMAGE_REPO.lower()}"
)

class Tuple_database(NamedTuple):
    name: str
    param: str


class DatabaseDict(TypedDict):
    params: str
    schemas: set[str]

class SpcsSetupTuple(NamedTuple):
    instance_family: str
    compute_pool: str


objects_to_setup: dict[str, DatabaseDict] = {
    TEST_DATABASE: {
        "schemas": {
            TEST_SCHEMA,
        },
        "params": "DATA_RETENTION_TIME_IN_DAYS=1",
    },
}
