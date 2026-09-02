"""
Hook Types.

Hook Types are triggers that can be executed when an event is triggered.

1. FSWatchdog: Watches a specified directory for changes.
"""
from .fs import FSWatchdog
from .web import WebHook
from .imap import IMAPWatchdog
from .tagged import TaggedIMAPWatchdog
from .ssh import SFTPWatchdog
from .upload import UploadHook
from .postgres import PostgresTrigger
from .http import HTTPHook
from .sharepoint import SharePointTrigger
from .mail import EmailTrigger
from .jira import JiraTrigger
# Message Brokers:
from .brokers.mqtt import MQTTTrigger
from .brokers.sqs import SQSTrigger
from .brokers.redis import RedisTrigger
from .brokers.rabbitmq import RabbitMQTrigger
