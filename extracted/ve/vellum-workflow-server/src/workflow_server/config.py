import os

from dotenv import load_dotenv

load_dotenv()

VEMBDA_PUBLIC_KEY = """
-----BEGIN PUBLIC KEY-----
MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEA3VrSo+PIYLsKaLwp6Kuw
TKzWHaAfJuoVaZtcc0WCVV6nS3wuyTtzHSc81gNT4AotIMgYExu80pG64MwZ2f57
iQPeMXSMQwcp49PRTwwAYXrb/XFhra56mwPOmNLPFHz4hChvJvAx8R4h+otUvkEZ
BRGgOICV5eMsELpvEz1Dn/pnw42UcNFI8kEAZJfVaj8izsGlYDK55QOZB+D/hETR
s7V0g9r9zjYwxmwNAAlRkQtJ4BzbrztqJt5uUVGEAmORgGdCsRU81Fd42GyHZxVY
WaAoPuqFj/Hd9PPvKuSZk/HBsxNBbyEp1zFoi8MxaVBgCpcWVEQWAsRo+ak9v6oN
yxxfZx8zshV0z2c79OpVre8rd+3dJviCIjTgClOe+ior0bpUSvd3q3gj5/ZLWo2v
uRJxsH4EXcJndcp3wbC4y98N61towHwzKdDIr1y3vmO2kh+m7MGg4mqMZs652Y4r
groREv+ohDej8CzU9CWSx5dE2leA1iIzLvKlbpkCIaQ4oFBUh9DlIZuCRGufgXBU
Tav8XWrbhG9nKJ+Gb3Jsol2YmDn+cdDIT8gs+dpe2/UyXH7YE0Oz0X3BVek17nej
nnTwu1M91VsPGq0tTcSi/AY53EO51YZr77Ln8ue694l2emyJDyj041bAmPAQOb26
czy4Vhr2WxlC6p9ekb3PY/8CAwEAAQ==
-----END PUBLIC KEY-----
"""

NAMESPACE = os.getenv("NAMESPACE")
IS_VPC = os.getenv("IS_VPC", "").lower() == "true"
MEMORY_LIMIT_MB = int(os.getenv("MEMORY_LIMIT_MB", "2048"))
PORT = os.getenv("PORT", "8000")
VELLUM_API_URL_HOST = os.getenv("VELLUM_API_URL_HOST", "localhost")
VELLUM_API_URL_PORT = os.getenv("VELLUM_API_URL_PORT", 8000)

# Set VELLUM_API_URL for SDK when using local Vellum API
if os.getenv("USE_LOCAL_VELLUM_API") == "true" and "VELLUM_API_URL" not in os.environ:
    os.environ["VELLUM_API_URL"] = "http://{}:{}".format(VELLUM_API_URL_HOST, VELLUM_API_URL_PORT)

CONCURRENCY = int(os.getenv("CONCURRENCY", "8"))
CONTAINER_IMAGE = os.getenv("CONTAINER_IMAGE", "python-workflow-runtime:latest")
ENABLE_PROCESS_WRAPPER = os.getenv("ENABLE_PROCESS_WRAPPER", "true").lower() == "true"

# This controls if we should just load a module already available in the py path for running
# a workflow. Currently used for running agent builder end to end locally
LOCAL_WORKFLOW_MODULE = os.getenv("LOCAL_WORKFLOW_MODULE")
# The deployment name to match against when using local mode so you can still run your normal workflow
LOCAL_DEPLOYMENT = os.getenv("LOCAL_DEPLOYMENT")

IS_ASYNC_MODE = os.getenv("IS_ASYNC_MODE", "false").lower() == "true"
IS_POOL_MODE = os.getenv("IS_POOL_MODE", "false").lower() == "true"


def is_development() -> bool:
    return os.getenv("FLASK_ENV", "local") == "local"
