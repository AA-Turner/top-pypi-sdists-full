# -*- coding: UTF-8 -*-
import boto3

from .const import AWS_CONF_KEY


def init_app(app):
    if not all([getattr(app.state.config, key) for key in AWS_CONF_KEY]):
        # pylint: disable=no-member
        app.state.logger.warn("Lack AWS credential keys, ignore connect to AWS")
        return None

    aws_session = boto3.session.Session(
        aws_access_key_id=app.state.config.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=app.state.config.AWS_SECRET_KEY,
        region_name=app.state.config.AWS_REGION
    )

    # This should be logging when create Logging handlers,
    # But we have too many CloudWatchLogHandler, only print once here.
    if not getattr(app.state.config, "AWS_LOGGROUP_NAME"):
        app.state.logger.info("Lack AWS configuration keys, ignore AWS CloudWatch log handlers")

    return aws_session
