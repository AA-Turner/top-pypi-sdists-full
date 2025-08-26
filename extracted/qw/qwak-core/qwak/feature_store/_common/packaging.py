import contextlib
import os
import shutil
import tempfile
import zipfile
from io import BytesIO
from pathlib import Path
from shutil import make_archive
from typing import TYPE_CHECKING, Callable, Dict, List, Optional, Union
from uuid import uuid4

import requests
from qwak.clients.feature_store.management_client import FeatureRegistryClient
from qwak.exceptions import QwakException
from qwak.feature_store._common.value import (
    UPDATE_QWAK_SDK_WITH_FEATURE_STORE_EXTRA_MSG,
)
from requests import HTTPError, Response

ZIP_FUNCTION_CONTENT_TYPE = "text/plain"

if TYPE_CHECKING:
    from qwak.feature_store.data_sources.streaming.kafka.deserialization import (
        Deserializer,
    )
    from qwak.feature_store.feature_sets.transformations.transformations import (
        BaseTransformation,
    )


def zip_source_code_dir(base_path: Path) -> Path:
    ignore_patterns = ["*.pyc", "__pycache__"]
    return zip_tree_to_temp_dir(base_path=base_path, ignore_patterns=ignore_patterns)


def zip_tree_to_temp_dir(base_path: Path, ignore_patterns=None) -> Path:
    if ignore_patterns is None:
        ignore_patterns = []

    full_path_to_archive = None
    parent_base_path = base_path.parent if base_path.is_file() else base_path
    tempdir = tempfile.mkdtemp()
    dst: Path = Path(os.path.join(tempdir, parent_base_path.name))
    try:
        shutil.copytree(
            src=parent_base_path,
            dst=dst,
            ignore=shutil.ignore_patterns(*ignore_patterns),
        )

        full_path_to_archive: Path = zip_path_dir_recursively(
            p=dst, dest=tempfile.mkdtemp()
        )
        return full_path_to_archive
    except Exception as e:
        raise QwakException("Failed to copy and zip directory") from e
    finally:
        shutil.rmtree(tempdir, ignore_errors=True)
        if full_path_to_archive:
            shutil.rmtree(full_path_to_archive, ignore_errors=True)


def zip_path_dir_recursively(p: Path, dest: Path) -> Path:
    root_dir: Path = p.parent if p.is_file() else p
    full_path_to_archive: str = make_archive(
        base_name=os.path.join(dest, str(uuid4())),
        format="zip",
        root_dir=root_dir.parent,
        base_dir=root_dir.name,
    )
    return Path(full_path_to_archive)


def zip_function_with_base_folder(
    functions: List[Callable], fs_object_module_dir: Path = None
) -> bytes:
    """
    Prepare zip bytes of the UDF functions and it's parent folder
    In case the functions param is a Callable it will write the pkled code to "function.pkl" (original flow)
    If a list of functions it will write each function to {function_name}.pkl
    Args:
        functions: udf functions
        fs_object_module_dir: parent directory path of the registered feature store object
    Returns:
        bytes representing the zip bytes of the udf functions pkl and module
    """
    try:
        import cloudpickle
    except Exception:
        raise QwakException(
            f"Missing required 'cloudpickle' dependency. {UPDATE_QWAK_SDK_WITH_FEATURE_STORE_EXTRA_MSG}"
        )

    in_memory = BytesIO()
    with chdir(fs_object_module_dir):
        zf = zipfile.ZipFile(in_memory, mode="w")
        with zf:
            if fs_object_module_dir:
                for path in Path.cwd().glob("**/*"):
                    str_path = (
                        f"./{path.relative_to(Path.cwd())}"
                        if path.is_file()
                        else str(path.resolve())
                    )
                    zf.write(str_path, "code" + "/" + str_path)
            for function in functions:
                zf.writestr(f"{function.__name__}.pkl", cloudpickle.dumps(function))
        in_memory.seek(0)
    return in_memory.read()


@contextlib.contextmanager
def chdir(dirname: Path = None):
    """
    chdir to given path and return to previous cwd when done
    Args:
        dirname: dir to chdir into
    """
    current_dir = Path.cwd()
    try:
        if dirname is not None:
            os.chdir(dirname)
        yield
    finally:
        os.chdir(current_dir)


def get_featureset_presign_url(
    features_manager_client: FeatureRegistryClient,
    feature_store_object_name: str,
    feature_store_object_name_suffix: str,
    transformation,
) -> str:
    return features_manager_client.get_presigned_url_v1(
        feature_set_name=feature_store_object_name + feature_store_object_name_suffix,
        transformation=transformation._to_proto(),
    )


def get_data_source_presign_url_v1(
    features_manager_client: FeatureRegistryClient,
    data_source_object_name: str,
    data_source_name_suffix: str,
) -> str:
    return features_manager_client.get_data_source_presigned_url_v1(
        data_source_name=data_source_object_name, object_name=data_source_name_suffix
    )


def upload_artifact(
    feature_store_object_name: str,
    feature_store_object_name_suffix: str,
    functions: List[Callable],
    feature_module_dir: Path,
    features_manager_client: FeatureRegistryClient,
    artifact_object: Union["BaseTransformation", "Deserializer"],
) -> str:
    """
    This function is used for uploading the function code in case a UDF type transformation was used (Pandas/Koalas/Pyspark)
    If a transformation was supplied, meaning we're running for at least batch, will use the SaaS adapted
    function to get the presign URL.
    """
    uploaded_artifact_url: str

    # this is done here to avoid cyclic imports
    from qwak.feature_store.data_sources.streaming.kafka.deserialization import (
        Deserializer,
    )
    from qwak.feature_store.feature_sets.transformations.transformations import (
        BaseTransformation,
    )

    if isinstance(artifact_object, BaseTransformation):
        presign_url = get_featureset_presign_url(
            features_manager_client=features_manager_client,
            feature_store_object_name=feature_store_object_name,
            feature_store_object_name_suffix=feature_store_object_name_suffix,
            transformation=artifact_object,
        )
    elif isinstance(artifact_object, Deserializer):
        presign_url = get_data_source_presign_url_v1(
            features_manager_client=features_manager_client,
            data_source_object_name=feature_store_object_name,
            data_source_name_suffix=feature_store_object_name_suffix,
        )
    else:
        raise QwakException(
            f"Got an unsupported artifact type: {type(artifact_object)}"
        )

    uploaded_artifact_url = base_upload_function_code(
        presign_url, functions, feature_module_dir
    )

    return uploaded_artifact_url


def put_files_content(
    url: str,
    content: bytes,
    content_type: str,
    extra_headers: Optional[Dict[str, str]] = None,
) -> None:
    """
    uploads files content to s3 using presigned url or to jfrog artifactory using url and authentication headers
    """
    extra_headers = extra_headers or {}
    try:
        http_response: Response = requests.put(
            url,
            headers={"content-type": content_type, **extra_headers},
            data=content,
            timeout=300,
        )
        http_response.raise_for_status()
    except HTTPError as e:
        raise QwakException(
            f"Error while uploading artifact. status code: {e.response.status_code} with reason: {e.response.reason}"
        ) from e


def upload_to_s3(presign_url: str, in_memory_zip: bytes, content_type: str) -> str:
    put_files_content(
        url=presign_url,
        content=in_memory_zip,
        content_type=content_type,
    )
    from urllib.parse import urlparse

    parsed_url = urlparse(presign_url)
    postfix = parsed_url.path
    bucket = parsed_url.hostname.split(".s3.")[0]
    s3_path = f"s3://{bucket}{postfix}"  # noqa: E231
    return s3_path


def base_upload_function_code(
    presign_url: str,
    functions: List[Callable],
    feature_module_dir: Path,
) -> str:
    """
    get presign url and prepare a zip file with the functions code and it's module than uploads it to clients' s3 bucket
    Args:
        presign_url: presign url
        functions: udf functions
        feature_module_dir: parent directory path of the feature
    Returns:
        Full path to the zip file uploaded
    """
    in_memory_zip = zip_function_with_base_folder(functions, feature_module_dir)
    return upload_to_s3(
        presign_url=presign_url,
        in_memory_zip=in_memory_zip,
        content_type=ZIP_FUNCTION_CONTENT_TYPE,
    )
