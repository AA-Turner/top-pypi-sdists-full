import time
import boto3
from .logging import lp
import sys


def _wait_for_glue_crawler_to_finish(client, crawler_name):
    """
    The function polls the state of a crawler every 10 seconds as long as the state is not READY.
    The possible states of a crawler are READY, RUNNING and STOPPING. The API used is:
    https://docs.aws.amazon.com/glue/latest/dg/aws-glue-api-crawler-crawling.html#aws-glue-api-crawler-crawling-GetCrawler

    Parameters:
        client:                 boto3 service client instance
        crawler_name (string):  Name of the crawler to be polled

    Returns:
        status (string):        The status of the crwal that has now finished. Can be either SUCCEEDED, CANCELLED or FAILED,
    """
    response = client.get_crawler(Name=crawler_name)
    while response["Crawler"]["State"] != "READY":
        lp(f"Current state of glue crawler {response['Crawler']['State']}")
        time.sleep(10)
        response = client.get_crawler(Name=crawler_name)

    lp(f"Finished status of last crawl: {response['Crawler']['LastCrawl']['Status']}")
    return response["Crawler"]["LastCrawl"]["Status"]


def execute_glue_crawler_task(client, crawler_name):
    """
    The function starts a crawler and then waits for it to finish. The API calls are from the boto3 AWS SDK.
    The crawler is started using https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.start_crawler
    This is the only function that should be called from outside this script.

    Parameters:
        crawler_name (string):  Name of the crawler to be polled
    """
    n_tries = 1
    status = ""
    while n_tries <= 3 and status != "SUCCEEDED":
        lp(f"Attempt number {n_tries} to start crawler")
        client.start_crawler(Name=crawler_name)
        status = _wait_for_glue_crawler_to_finish(client, crawler_name)
        n_tries += 1

    if status != "SUCCEEDED":
        raise Exception("Crawler failed!")


if __name__ == "__main__":
    session = boto3.session.Session(region_name)

    client = session.client(
        "glue",
        region_name,
        aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_access_key,
    )
    crawler_name = sys.argv[1]
    lp(f"Running crawler with name: {crawler_name}")
    execute_glue_crawler_task(client, crawler_name)
