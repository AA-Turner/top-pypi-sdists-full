import json
import boto3
import logging

def publish(
        topic_arn: str, 
        message: dict,
        region_name: str = "us-east-1",
        session=None,
        attr_exclude: list = list()):
    """ 
    Publish message to SNS Topic

    Parameters:
    topic_arn (str): Topic ARN where publish message to
    message (dict): DICT to publish as JSON into SNS
    region_name (str): AWS Region where to create session
    session: Existing boto3 session
    attr_exclude (list): List of keys to not post as attribute
    
    Returns:
    boto3 client.publish() response
    """

    sns = boto3.client("sns", region_name=region_name)

    message_to_publish = force_message_format(message)
    attributes = parse_attributes(message, attr_exclude)

    response = sns.publish(
        TopicArn=topic_arn,
        Message=message_to_publish,
        MessageAttributes=attributes
    )

    return response

def parse_attributes(message, attr_exclude: list) -> dict:

    logging.debug("Parsing message sttributes.")
    if type(message) == str:
        message = json.loads(message)

    if type(message) != dict:
        return {}

    attritubes = {}
    for key in message.keys():
        
        # Skip data field. Its important only in message body
        if key.lower() in attr_exclude:
            continue

        if type(message.get(key)) in [dict, object]:
            continue

        try:
            attritubes[key] = {
                "DataType": "String",
                "StringValue": str(message.get(key))
            }
        except Exception as ex:
            logging.error("Error parsing value to attribute: {}:{}".format(key, message.get(key)))

    logging.debug("Attributes: {}".format(attritubes))

    return attritubes


def force_message_format(message) -> str:
    if type(message) == dict:
        return json.dumps(message, default=str)
    return message