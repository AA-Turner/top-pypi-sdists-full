import os
from typing import Iterable, Tuple

import click
from otel_extensions import instrumented
from retry import retry

from utf_queue_client.clients.sqa_test_result_producer import (
    SqaTestResultProducerFactory,
)
from utf_queue_client.models.schemas.utf_queue_models.models.python.generated_models import (
    SqaAppBuildResult,
    SqaTestSession,
)
from utf_queue_client.scripts import setup_telemetry
from utf_queue_client.utils import QUEUE_APP_ID, prepare_queue_central_url

NUM_RETRIES = 6


class PublishTestResultsCommander(click.Command):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.params.append(
            click.Option(
                ("--username",),
                envvar="UTF_QUEUE_USERNAME",
                help="UTF queue username",
                required=True,
            )
        )
        self.params.append(
            click.Option(
                ("--password",),
                envvar="UTF_QUEUE_PASSWORD",
                help="UTF queue password",
                required=True,
            )
        )
        self.params.append(
            click.Option(
                ("--data_type",),
                help="type of the data [SESSION_START, SESSION_STOP, BUILD_RESULT']",
                required=True,
            )
        )
        self.params.append(
            click.Option(
                ("--data",),
                multiple=True,
                type=(str, str),
                help="data in dictionary format",
                required=True,
            )
        )


@click.command(cls=PublishTestResultsCommander)
def cli_entrypoint(**kwargs):
    cli(**kwargs)


def cli(
    username: str,
    password: str,
    data_type: str,
    data: Iterable[Tuple[str, str]],
):
    with setup_telemetry():
        url = prepare_queue_central_url(username, password)
        data_dict = {}
        for key, value in data:
            data_dict[key] = value

        @retry(Exception, delay=5, backoff=2, max_delay=30, tries=NUM_RETRIES + 1)
        def retry_wrapper():
            publish_test_results_through_queue(url, data_type, data_dict)

        retry_wrapper()


@instrumented
def publish_test_results_through_queue(url, data_type: str, data_dict: dict):
    os.environ["UTF_QUEUE_SERVER_URL"] = url
    os.environ["UTF_PRODUCER_APP_ID"] = QUEUE_APP_ID
    test_result_producer = SqaTestResultProducerFactory.create_producer()
    if data_type.upper() == "SESSION_START":
        test_result_producer.publish_test_session_start(prepare_session_data(data_dict))
    elif data_type.upper() == "SESSION_STOP":
        test_result_producer.publish_test_session_stop(prepare_session_data(data_dict))
    elif data_type.upper() == "BUILD_RESULT":
        app_build_result = SqaAppBuildResult(
            session_pk_id=data_dict.get("session_pk_id"),
            app_name=data_dict.get("app_name"),
            app_description=data_dict.get("app_description"),
            test_suite_name=data_dict.get("test_suite_name"),
            test_result_type=data_dict.get("test_result_type"),
            executor_name=data_dict.get("executor_name"),
            feature_name=data_dict.get("feature_name"),
            module_name=data_dict.get("module_name"),
            phy_name=data_dict.get("phy_name"),
            test_result=data_dict.get("test_result"),
            engineer_name=data_dict.get("engineer_name"),
            exception_msg=data_dict.get("exception_msg"),
            iot_req_id=data_dict.get("iot_req_id"),
            tool_chain=data_dict.get("tool_chain"),
            notes=data_dict.get("notes"),
            test_duration_sec=data_dict.get("test_duration_sec"),
        )
        test_result_producer.publish_app_build_result(app_build_result)
    else:
        raise RuntimeError(
            "please provide the valid value for the parameter 'data_type'"
        )


@instrumented()
def prepare_session_data(data_dict: dict):
    return SqaTestSession(
        PK_ID=data_dict.get("PK_ID"),
        startTime=data_dict.get("startTime"),
        stopTime=data_dict.get("stopTime"),
        jenkinsJobStatus=data_dict.get("jenkinsJobStatus"),
        duration=data_dict.get("duration"),
        jobType=data_dict.get("jobType"),
        releaseName=data_dict.get("releaseName"),
        branchName=data_dict.get("branchName"),
        stackName=data_dict.get("stackName"),
        SDKBuildNum=data_dict.get("SDKBuildNum"),
        SDKUrl=data_dict.get("SDKUrl"),
        studioUrl=data_dict.get("studioUrl"),
        totalTests=data_dict.get("totalTests"),
        PASS_cnt=data_dict.get("PASS_cnt"),
        FAIL_cnt=data_dict.get("FAIL_cnt"),
        SKIP_cnt=data_dict.get("SKIP_cnt"),
        jenkinsServerName=data_dict.get("jenkinsServerName"),
        jenkinRunNum=data_dict.get("jenkinRunNum"),
        jenkinsJobName=data_dict.get("jenkinsJobName"),
        jenkinsTestResultsUrl=data_dict.get("jenkinsTestResultsUrl"),
        traceId=data_dict.get("traceId"),
        testFramework=data_dict.get("testFramework"),
        SDKVersion=data_dict.get("SDKVersion"),
        test_run_by=data_dict.get("test_run_by"),
    )


if __name__ == "__main__":
    cli_entrypoint()
