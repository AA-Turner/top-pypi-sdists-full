"""Module with OCR class and methods to convert PDF to images."""
import datetime
import hashlib
import json
import re
import shutil
import tempfile
import time

import os
import uuid
import warnings
import zipfile
from pathlib import Path
from typing import List, Tuple
from zipfile import ZipFile

import boto3
from pypdf import PdfReader

from t_ocr._config import AWSConfiguration
from t_ocr.logger import logger
from t_ocr.okta import Okta
from t_ocr.exceptions import StepFunctionAWSError, LimitExceededError, TOCRWarning


class OCR:
    """A class method for OCR. Validates poppler install, converts pdf to images."""

    def __init__(self):
        """Initialize the OCR class. Also check if poppler installed."""
        self.__temp_dir = tempfile.TemporaryDirectory()
        self.__session = None
        self._cache_dir = os.path.join(os.getcwd(), "t_ocr_cache")

        self.__aws_configuration: AWSConfiguration = None

        # Parameters for relogin
        self.__last_login_args: Tuple = None
        self.__session_expiry: datetime.datetime = None

    def __config(self) -> AWSConfiguration:
        if self.__aws_configuration is None:
            session = self.__get_session()
            region = session.region_name
            sts = session.client("sts")
            identity = sts.get_caller_identity()
            account_id = identity["Account"]
            arn = identity["Arn"]
            self.__aws_configuration = AWSConfiguration(account_id, region, arn)
        return self.__aws_configuration

    def bucket_name(self) -> str:
        return self.__config().bucket_name

    def __get_session(self):
        self._refresh_session_if_needed()
        if self.__session is None:  # If you use environment variables to authorize
            self.__session = boto3.Session()
        return self.__session

    def __get_s3_resource(self):
        return self.__get_session().resource("s3")

    def __get_s3_client(self):
        return self.__get_session().client("s3")

    def __step_function(self):
        return self.__get_session().client("stepfunctions")

    def _refresh_session_if_needed(self):
        """
        Refresh the session if it has expired.
        """
        expiration_buffer = datetime.timedelta(minutes=1)
        if (
            self.__session_expiry
            and datetime.datetime.now(datetime.timezone.utc) >= self.__session_expiry - expiration_buffer
        ):
            logger.info("Session expired, refreshing...")
            self._relogin()

    def _relogin(self):
        """
        Re-login using the last used method with stored arguments.
        """
        if self.__last_login_args:
            method, args = self.__last_login_args
            method(*args)

    def login(self, role_arn: str, external_id: str, region: str = "us-east-1", session: boto3.Session = None):
        """
        Login to AWS Textract with role AWS credentials.

        Args:
            role_arn (str): AWS Access Key Id
            external_id (str): AWS Secret access key
            region (str, optional): AWS session token. Defaults to "us-east-1".
            session (boto3.Session, optional): boto3 session. Defaults to None.

        In AWS: IAM > Roles > {Role Name} (In the tab "Trust relationships")
        """
        if session is None:
            sts = boto3.client("sts")
        else:
            sts = session.client("sts")

        response = sts.assume_role(
            RoleArn=role_arn,
            RoleSessionName="thoughtful-codeartifact",
            ExternalId=external_id,
        )
        self.__session = boto3.Session(
            aws_access_key_id=response["Credentials"]["AccessKeyId"],
            aws_secret_access_key=response["Credentials"]["SecretAccessKey"],
            aws_session_token=response["Credentials"]["SessionToken"],
            region_name=region,
        )
        self.__session_expiry = response["Credentials"]["Expiration"]
        self.__last_login_args = (self.login, (role_arn, external_id, region, session))

    def login_via_access_key(
        self, access_key: str, secret_access_key: str, role_arn: str, external_id: str, region: str = "us-east-1"
    ):
        """
        Login to AWS Textract with role AWS credentials using access key.

        Args:
            access_key (str): AWS Access Key Id
            secret_access_key (str): AWS Secret access key
            role_arn (str): AWS Role ARN
            external_id (str): External ID
            region (str, optional): AWS Region. Defaults to "us-east-1".
        """
        session = boto3.Session(
            aws_access_key_id=access_key, aws_secret_access_key=secret_access_key, region_name=region
        )
        self.login(role_arn, external_id, region, session)
        self.__last_login_args = (
            self.login_via_access_key,
            (access_key, secret_access_key, role_arn, external_id, region),
        )

    def login_via_okta(
        self,
        okta_username: str,
        okta_totp: str,
        aws_account_id: str,
        aws_start_url: str,
        aws_role_name: str,
        okta_password: str = "",
        aws_client_name: str = "test_name",
        aws_client_type: str = "public",
        region_name: str = "us-east-1",
    ):
        okta = Okta(
            username=okta_username,
            password=okta_password,
            totp=okta_totp,
            account_id=aws_account_id,
            role_name=aws_role_name,
            client_name=aws_client_name,
            client_type=aws_client_type,
            service_name="sso-oidc",
            region_name=region_name,
            start_url=aws_start_url,
        )
        self.__session, self.__session_expiry = okta.get_aws_session()
        self.__last_login_args = (
            self.login_via_okta,
            (
                okta_username,
                okta_totp,
                aws_account_id,
                aws_start_url,
                aws_role_name,
                okta_password,
                aws_client_name,
                aws_client_type,
                region_name,
            ),
        )

    def __clean_cache(self):
        self.__temp_dir.cleanup()
        self.__temp_dir = tempfile.TemporaryDirectory()

    @staticmethod
    def __get_file_hash(file_path: str) -> str:
        with open(file_path, "rb") as f:
            md5_hash = hashlib.md5(f.read()).hexdigest()
        file_modified_time = os.path.getmtime(file_path)
        hash_code = f"{md5_hash}{file_modified_time}"
        return re.sub(r"[^0-9a-zA-Z]+", "", hash_code)

    @classmethod
    def _get_call_hash(cls, action: str, parsing_method: str, file: str, **kwargs):
        kwargs_str = ""
        for key, value in sorted(kwargs.items(), key=lambda x: x[0]):
            kwargs_str += f"{key}={value}"
        call_str = f"{action}_{parsing_method}_{kwargs_str}_{os.path.basename(file)}"
        call_hash = hashlib.md5(f"{call_str}_{cls.__get_file_hash(file)}".encode()).hexdigest()
        return call_hash

    def _get_cache_file(self, file_name: str):
        return os.path.join(self._cache_dir, file_name)

    def _get_cache_data(self, file_name: str):
        with open(self._get_cache_file(file_name)) as f:
            return json.load(f)

    def _is_cache_exists(self, file_name: str):
        if os.path.exists(self._get_cache_file(file_name)):
            return True
        return False

    def _save_cache_from_dict(self, data: dict, cache_name: str):
        temp_file_path = os.path.join(self.__temp_dir.name, cache_name)
        with open(temp_file_path, "w") as f:
            json.dump(data, f)
        self._save_cache(temp_file_path, cache_name)
        os.remove(temp_file_path)

    @staticmethod
    def is_local_run():
        if os.environ.get("RC_PROCESS_ID"):
            return False
        return True

    def _save_cache(self, file_path: str, cache_name: str):
        if os.environ.get("RC_PROCESS_ID"):
            warnings.warn(
                "You use data caching, if you have finished development and the bot is already in production, "
                "please disable it so as not to waste extra time and not use memory unnecessarily.",
                TOCRWarning,
            )
        if not os.path.exists(self._cache_dir):
            os.makedirs(self._cache_dir)
        shutil.copyfile(file_path, self._get_cache_file(cache_name))

    def convert_pdf_to_images(
        self,
        pdf_path: str or Path,
        dpi: int = 400,
        first_page: int = "first",
        last_page: int = "last",
        output_dir: str or Path = None,
    ) -> List[str]:
        """Convert PDF file to images of each page and returns a list of images path strings.

        Args:
            pdf_path (str): path to PDF file to parse.
            dpi (int, optional): image quality in DPI. Defaults to 400.
            first_page (int, optional): page number where to start OCR. Defaults to "first".
            last_page (int, optional): page number where to stop OCR. Defaults to "last".
            output_dir (str or Path, optional): path to folder where images should be saved,
                by default images will be saved in temp and deleted. Defaults to None.

        Returns:
            List[str]: list of str objects with paths to images.
        """
        self.__clean_cache()
        if output_dir is None:
            _output_dir = self.__temp_dir.name
        else:
            _output_dir = os.path.abspath(output_dir)

        s3_work_folder, pdf_s3_key = self._upload_s3_file(pdf_path)
        try:
            payload = self._get_parsing_configuration_payload(
                bucket_name=self.bucket_name(),
                pdf_s3_key=pdf_s3_key,
                method_type="convert_pdf_to_image",
                s3_work_folder=s3_work_folder,
                dpi=dpi,
                first_page=first_page,
                last_page=last_page,
            )
            response = self._run_t_ocr_step_function(payload, work_dir=s3_work_folder)

            result_s3_key = json.loads(response["output"])["images_zip_s3_key"]

            result_file_path = self._download_s3_file(result_s3_key)
        finally:
            self._delete_s3_folder(s3_work_folder)

        images: List[str] = []
        with ZipFile(result_file_path, "r") as zip_file:
            for file_name in zip_file.namelist():
                image_path = zip_file.extract(file_name, _output_dir)
                images.append(image_path)

        return images

    @staticmethod
    def get_pages_number(pdf_path: str) -> int:
        """Get the number of pages of a PDF document.

        Args:
            pdf_path (str): path to PDF file to parse.

        Returns:
            int: pages number.
        """
        return len(PdfReader(pdf_path).pages)

    @staticmethod
    def _get_parsing_parallel_configuration_payload(
        bucket_name: str, s3_work_folder: str, zip_s3_key: str, files_names: List[str], parsing_payload: dict
    ) -> dict:
        return {
            "s3_work_folder": s3_work_folder,
            "bucket_name": bucket_name,
            "zip_s3_key": zip_s3_key,
            "files_names": files_names,
            "parsing_payload": parsing_payload,
        }

    @staticmethod
    def _get_parsing_configuration_payload(
        bucket_name: str,
        method_type: str,
        s3_work_folder: str = "",
        parsing_tool: str = "",
        pdf_s3_key: str = "",
        image_s3_key: str = "",
        dpi: int = 400,
        tesseract_run_config: str = "",
        first_page: int = "first",
        last_page: int = "last",
        page_numbers: List[int] = [],
        page_num: int = 0,
        textract_features_type: List[str] = [],
    ) -> dict:

        if dpi not in range(200, 800):
            if dpi < 200:
                raise ValueError(
                    f"Consider to use dpi value in range from 200 to 800. "
                    f"For value: '{dpi}' text may be misinterpreted"
                )
            elif dpi > 800:
                raise ValueError(
                    f"Consider to use dpi value in range from 200 to 800. "
                    f"For value: '{dpi}' memory usage will be too high"
                )

        if first_page != "first" and (not isinstance(first_page, int) or first_page < 1):
            raise ValueError("'first_page' parameter may be only 'first' or integer grater than 0")

        if last_page != "last" and (not isinstance(last_page, int) or last_page < 1):
            raise ValueError("'last_page' parameter may be only 'last' or integer grater than 0")

        if page_numbers:
            if not isinstance(page_numbers, list) or not all(isinstance(x, int) for x in page_numbers):
                raise ValueError("'page_numbers' parameter must be a list with integers")
            if len(page_numbers) != len(set(page_numbers)):
                raise ValueError("'page_numbers' must not contain duplicate integers")
            if last_page != "last" or first_page != "first":
                warnings.warn(
                    "If you use the 'page_numbers' parameter, "
                    "the 'first_page' and 'last_page' parameters will be ignored",
                    TOCRWarning,
                )

        if page_num != 0 and (not isinstance(page_num, int) or page_num < 1):
            raise ValueError("'page_num' parameter may be only integer grater than 0")
        return {
            "bucket_name": bucket_name,
            "method_type": method_type,
            "s3_work_folder": s3_work_folder,
            "parsing_tool": parsing_tool,
            "pdf_s3_key": pdf_s3_key,
            "image_s3_key": image_s3_key,
            "dpi": str(dpi),
            "tesseract_run_config": tesseract_run_config,
            "first_page": first_page,
            "last_page": last_page,
            "page_numbers": page_numbers,
            "page_num": page_num,
            "textract_features_type": textract_features_type,
        }

    def _zip_and_upload_s3_files(self, files: List[str], unique_names: bool = True) -> (str, str, List[str]):
        zip_path = os.path.join(self.__temp_dir.name, "files.zip")
        file_names = []
        with zipfile.ZipFile(zip_path, "w") as zip_file:
            for file_path in files:
                if unique_names:
                    file_name, file_ext = os.path.splitext(os.path.basename(file_path))
                    temp_file_name = f"{file_name}__{uuid.uuid4().hex}{file_ext}"
                else:
                    temp_file_name = os.path.basename(file_path)
                zip_file.write(file_path, temp_file_name)
                file_names.append(temp_file_name)

        s3_work_folder, s3_key = self._upload_s3_file(zip_path)
        return s3_work_folder, s3_key, file_names

    def _upload_s3_file(self, file_path: str) -> (str, str):
        s3_work_folder = f"{time.strftime('%Y-%m-%d_%H-%M-%S')}_{uuid.uuid4().hex}"
        s3_key = f"{s3_work_folder}/inputs/{os.path.basename(file_path)}"
        self.__get_s3_client().upload_file(file_path, self.bucket_name(), s3_key)
        return s3_work_folder, s3_key

    def _delete_s3_folder(self, folder_s3_key: str) -> None:
        bucket = self.__get_s3_resource().Bucket(self.bucket_name())
        folder_s3_key = folder_s3_key if folder_s3_key.endswith("/") else f"{folder_s3_key}/"
        bucket.objects.filter(Prefix=folder_s3_key).delete()

    def _download_s3_file(self, s3_key: str) -> str:
        file_path = os.path.join(self.__temp_dir.name, s3_key.split("/")[-1])
        self.__get_s3_client().download_file(self.bucket_name(), s3_key, file_path)
        return file_path

    def _download_s3_fileobj(self, s3_key: str, file: tempfile.TemporaryFile) -> str:
        self.__get_s3_client().download_fileobj(self.bucket_name(), s3_key, file)
        return file.name

    def _run_t_ocr_step_function(self, payload: dict or List[dict], work_dir: str):
        return self._run_step_function(
            state_machine_arn=self.__config().step_function_arn, payload=payload, work_dir=work_dir
        )

    def _run_t_ocr_parallel_step_function(self, payload: dict or List[dict], work_dir: str):
        return self._run_step_function(
            state_machine_arn=self.__config().parallel_step_function_arn, payload=payload, work_dir=work_dir
        )

    @staticmethod
    def _check_parameters_for_parallel_method(
        pdfs_path: List[str], first_page: int, last_page: int, page_numbers: List[int]
    ):
        if len(pdfs_path) != len(set(pdfs_path)):
            raise ValueError(
                "'pdfs_path' argument contains duplicates, "
                "the same file can't be processed in a parallel process more than once"
            )
        if page_numbers:
            if len(page_numbers) > 3:
                raise LimitExceededError(
                    "You are trying to process more than 3 pages. "
                    "The number of pages cannot be more than 3 for the parallel function."
                )
        else:
            if last_page == "last":
                last_page = 3
                warnings.warn(
                    "The parallel function supports a maximum of 3 pages, "
                    "if you don't specify last_page it will default to 3",
                    TOCRWarning,
                )

            if (first_page == "first" and last_page > 3) or (
                first_page != "first" and int(last_page) - int(first_page) > 2
            ):
                raise LimitExceededError(
                    "You are trying to process more than 3 pages. "
                    "The number of pages cannot be more than 3 for the parallel function."
                )

        if len(pdfs_path) > 100:
            raise LimitExceededError(
                f"You are trying to process {len(pdfs_path)} files, "
                "the number of files can't be more than 100 at a time for the parallel function. "
                "Try splitting lists with files into sub-lists of 100 files"
                " and process them one by one"
            )

        return pdfs_path, first_page, last_page, page_numbers

    def _run_step_function(self, state_machine_arn: str, payload: dict or List[dict], work_dir: str):
        new_execution_response = self.__step_function().start_execution(
            stateMachineArn=state_machine_arn, input=json.dumps(payload), name=work_dir
        )

        while True:
            time.sleep(0.2)

            sf_response = self.__step_function().describe_execution(executionArn=new_execution_response["executionArn"])
            status = sf_response["status"]

            if status == "RUNNING":
                continue
            elif status == "FAILED":
                raise Exception(f"! ERROR ! Execution FAILED: {sf_response}")
            else:
                break

        request_id = sf_response["name"]
        execution_arn = sf_response["executionArn"]
        execution_details_url = (
            f"https://{self.__config().region}.console.aws.amazon.com/states/home?"
            f"region={self.__config().region}#/executions/details/{execution_arn}"
        )

        output = json.loads(sf_response["output"])
        if "error" in output:
            lambda_request_id = output["aws_request_id"] if "aws_request_id" in output else ""
            if lambda_request_id and lambda_request_id != request_id:
                lambda_request_id_additional_text = f" (LambdaRequestId {lambda_request_id})"
            else:
                lambda_request_id_additional_text = ""
            error_cause: dict or str = output["error"]["Cause"]
            error_header = f"""
AWS Step Function execution ended with an error.
START RequestId: {request_id}{lambda_request_id_additional_text}
Execution details: {execution_details_url}"""

            if "stackTrace" in error_cause:  # Python code Error
                error_cause = json.loads(error_cause)
                error_message = error_cause["errorMessage"]
                stack_trace = "".join(error_cause["stackTrace"])
                error_type = error_cause["errorType"]

                lambda_error_msg = f"""\n{error_header}

Lambda Traceback (most recent call last):
{stack_trace}{error_type}: {error_message}"""
            else:  # Lambda Error
                error_type = output["error"]["Error"]

                lambda_error_msg = f"""\n{error_header}

Lambda error:
{error_type}: {error_cause}"""

            raise StepFunctionAWSError(lambda_error_msg)
        else:
            return sf_response
