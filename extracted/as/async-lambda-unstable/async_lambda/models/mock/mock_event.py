from time import time
from typing import List, Optional, Tuple
from urllib.parse import parse_qs, parse_qsl


def MockSQSLambdaEvent(body: str, source_queue_arn: Optional[str] = None) -> dict:
    now_timestamp = int(time())
    if not source_queue_arn:
        source_queue_arn = "arn:aws:sqs:us-east-1:123456789012:my-queue"
    return {
        "Records": [
            {
                "messageId": "059f36b4-87a3-44ab-83d2-661975830a7d",
                "receiptHandle": "AQEBwJnKyrHigUMZj6rYigCgxlaS3SLy0a",
                "body": body,
                "attributes": {
                    "ApproximateReceiveCount": "1",
                    "SentTimestamp": str(now_timestamp),
                    "SenderId": "AIDAIENQZJOLO23YVJ4VO",
                    "ApproximateFirstReceiveTimestamp": str(now_timestamp + 5),
                },
                "messageAttributes": {},
                "md5OfBody": "e4e68fb7bd0e697a0ae8f1bb342846b3",
                "eventSource": "aws:sqs",
                "eventSourceARN": source_queue_arn,
                "awsRegion": "us-east-1",
            }
        ]
    }


def MockSQSBatchLambdaEvent(
    bodies: List[str], source_queue_arn: Optional[str] = None
) -> dict:
    now_timestamp = int(time())
    if not source_queue_arn:
        source_queue_arn = "arn:aws:sqs:us-east-1:123456789012:my-queue"

    records = []
    for body in bodies:
        records.append(
            {
                "messageId": "059f36b4-87a3-44ab-83d2-661975830a7e",
                "receiptHandle": "AQEBwJnKyrHigUMZj6rYigCgxlaS3SLy0b",
                "body": body,
                "attributes": {
                    "ApproximateReceiveCount": "1",
                    "SentTimestamp": str(now_timestamp),
                    "SenderId": "AIDAIENQZJOLO23YVJ4VO",
                    "ApproximateFirstReceiveTimestamp": str(now_timestamp + 5),
                },
                "messageAttributes": {},
                "md5OfBody": "e4e68fb7bd0e697a0ae8f1bb342846b4",
                "eventSource": "aws:sqs",
                "eventSourceARN": source_queue_arn,
                "awsRegion": "us-east-1",
            }
        )
    return {"Records": records}


def MockAPILambdaEvent(
    path: str,
    method: str,
    body: Optional[str] = None,
    query_string: Optional[str] = None,
    headers: Optional[List[Tuple[str, str]]] = None,
) -> dict:
    multi_value_headers = {}
    for key, value in headers or []:
        if key not in multi_value_headers:
            multi_value_headers[key] = []
        multi_value_headers[key].append(value)

    cleaned_querystring = (query_string or "").lstrip("?")

    return {
        "path": path,
        "httpMethod": method.upper(),
        "headers": {key: value for key, value in headers or []},
        "multiValueHeaders": multi_value_headers,
        "queryStringParameters": dict(parse_qsl(cleaned_querystring)),
        "multiValueQueryStringParameters": parse_qs(cleaned_querystring),
        "pathParameters": dict(),
        "requestContext": dict(),
        "body": body,
        "isBase64Encoded": False,
    }
