import click

from tinybird.tb.config import get_display_cloud_host
from tinybird.tb.modules.feedback_manager import FeedbackManager
from tinybird.tb.modules.local_common import TB_LOCAL_ADDRESS


def echo_job_url(token: str, host: str, workspace_name: str, job_url: str):
    if "localhost" in host:
        job_url = f"{job_url.replace('http://localhost:8001', TB_LOCAL_ADDRESS)}?token={token}"
    click.echo(FeedbackManager.gray(message="Job API URL: ") + FeedbackManager.info(message=f"{job_url}"))
    ui_host = get_display_cloud_host(host)
    click.echo(
        FeedbackManager.gray(message="Jobs URL: ") + FeedbackManager.info(message=f"{ui_host}/{workspace_name}/jobs")
    )
