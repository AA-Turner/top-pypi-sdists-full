from pathlib import Path

import boto3
import requests

from pycarlo.core import Client, Query

MC_CLIENT = Client()
S3_CLIENT = boto3.client("s3")


def upload_insights_to_s3(
    destination_bucket: str,
    desired_file_extension: str = ".csv",
) -> None:
    """
    Example function for listing all insights in an account, and uploading any available
    to S3 as a CSV.
    """
    list_insights_query = Query()
    list_insights_query.get_insights()
    for insight in MC_CLIENT(list_insights_query).get_insights:
        report_name = str(Path(insight.name).with_suffix(desired_file_extension))

        if insight.available:
            report_url_query = Query()
            report_url_query.get_report_url(insight_name=insight.name, report_name=report_name)
            report_url = MC_CLIENT(report_url_query).get_report_url.url

            print(f"Uploading {report_name} to {destination_bucket}.")
            S3_CLIENT.upload_fileobj(
                Fileobj=requests.get(url=report_url, stream=True).raw,
                Bucket=destination_bucket,
                Key=report_name,
            )


if __name__ == "__main__":
    upload_insights_to_s3(destination_bucket="<BUCKET-NAME>")
