"""Module providing __init__ functionality."""

from matrice.utils import dependencies_check

dependencies_check(
    [
        "httpx",
        "fastapi",
        "uvicorn",
        "pillow",
        "confluent_kafka[snappy]",
        "aiokafka",
        "filterpy",
        "scipy",
        "scikit-learn",
        "matplotlib",
        "scikit-image",
        "python-snappy",
        "pyyaml"
    ]
)

if not dependencies_check(["opencv-python"]):
    dependencies_check(["opencv-python-headless"])

from matrice.deploy.server.server import MatriceDeployServer  # noqa: E402
from matrice.deploy.server.server import MatriceDeployServer as MatriceDeploy  # noqa: E402 # Keep this for backwards compatibility
from matrice.deploy.server.inference.inference_interface import InferenceInterface  # noqa: E402
from matrice.deploy.server.proxy.proxy_interface import MatriceProxyInterface  # noqa: E402
from matrice.deploy.server.stream_worker import StreamWorker, StreamWorkerManager  # noqa: E402
from matrice.deploy.client import MatriceDeployClient  # noqa: E402

__all__ = [
    "MatriceDeploy",
    "MatriceDeployServer",
    "InferenceInterface",
    "MatriceProxyInterface",
    "MatriceDeployClient",
    "StreamWorker",
    "StreamWorkerManager",
]
