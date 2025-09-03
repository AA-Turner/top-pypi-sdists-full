import json
import smtplib
import ssl
from email.message import EmailMessage
from typing import List

import requests
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from bigeye_sdk.log import get_logger

log = get_logger(__name__)


def send_email(
        server_name: str,
        port: int,
        user_name: str,
        password: str,
        sender: str,
        subject: str,
        recipient: List[str],
        body: str
):
    msg = EmailMessage()
    msg.set_content(body, subtype="html")
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = recipient
    context = ssl.create_default_context()
    with smtplib.SMTP(host=server_name, port=port) as smtp:
        smtp.starttls(context=context)
        smtp.login(user=user_name, password=password)
        smtp.send_message(msg=msg, from_addr=sender, to_addrs=recipient)


def post_slack_snippet(slack_token: str, slack_channel: List[str], body: dict, text: str, title: str):
    client = WebClient(token=slack_token)

    for c in slack_channel:
        try:
            # Snippets require the channel ID instead of the name. Posting a message to precede it returns the ID
            response = client.chat_postMessage(channel=c, text=text, mrkdwn=True)
            client.files_upload_v2(content=json.dumps(body, indent=True), channel=response["channel"], snippet_type="json",
                                   title=title)
        except SlackApiError as e:
            log.error(f"Error posting to channel {c}: {e.response['error']}")


def post_webhook_request(webhook_url: List[str], data: dict, headers: dict = {}):
    headers.update({"Content-Type": "application/json"})
    for url in webhook_url:
        requests.post(
            url=url, data=json.dumps(data, indent=True), headers=headers
        )
