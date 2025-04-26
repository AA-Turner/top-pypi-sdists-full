"""
This module will house all automated slack app logic.
"""
import io
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


def post_dataframe_as_message(channel, token, pandas_df, message):
    """
        Posts a pandas DataFrame to a Slack channel.

        Args:
            channel (str): The ID or name of the Slack channel to post to.
            token (str): The Slack API token to use for authentication.
            pandas_df (pd.DataFrame): The DataFrame to post to the channel.
            message (str): A message to include with the DataFrame.

        Returns:
            None.
    """
    post_text = (
        # Place the message above the DataFrame
        message + "\n\n" +
        # Convert the DataFrame to a string surrounded by backticks
        # Source for formatting: https://stackoverflow.com/questions/66713432
        "``` \n" + pandas_df.to_markdown(index=False, floatfmt='') + "\n ```")
    # Initialize a Slack WebClient instance
    client = WebClient(token=token)
    # Post the message to Slack
    try:
        response = client.chat_postMessage(channel=channel, text=post_text)
        print("Message posted to Slack")
    except SlackApiError as e:
        print("Error posting message to Slack: {}".format(e))


def post_dataframe_as_csv(channel_id, token, pandas_df, filename):
    """
        Posts a pandas DataFrame to a Slack channel.

        Args:
            channel_id (str): The ID or name of the Slack channel to post to.
            token (str): The Slack API token to use for authentication.
            pandas_df (pd.DataFrame): The DataFrame to post to the channel.
            filename (str): Filename for downloadable CSV.

        Returns:
            None.
    """
    # Write the DataFrame to a CSV in a buffer
    csv_buffer = io.StringIO()
    pandas_df.to_csv(csv_buffer, index=False)
    # Initialize a Slack WebClient instance
    client = WebClient(token=token)
    # Upload the CSV to a Slack channel
    try:
        response = client.files_upload_v2(
            channel=channel_id, filename=filename,
            content=csv_buffer.getvalue(),
            initial_comment="*~~~ CSV DOWNLOAD ~~~*")
        print("CSV posted to Slack")
    except SlackApiError as e:
        print("Error posting CSV to Slack: {}".format(e))
