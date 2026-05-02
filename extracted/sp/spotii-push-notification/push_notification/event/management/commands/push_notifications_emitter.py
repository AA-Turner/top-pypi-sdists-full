import asyncio
import time
import traceback
from datetime import datetime
from datetime import timedelta
from typing import List

import aiohttp
from django.core.management.base import BaseCommand
from django.db import OperationalError
from django.db import transaction
from django.db.models import Q
from pytz import utc

from django.conf import settings
from push_notification.event.models import PushNotificationEvent


class Command(BaseCommand):
    help = "Send events to registered push notification url"

    retry = settings.PUSH_NOTIFICATIONS.get('RETRY', 10)
    retry_interval = settings.PUSH_NOTIFICATIONS.get('RETRY_INTERVAL', 60)
    connection_timeout = settings.PUSH_NOTIFICATIONS.get('CONNECTION_TIMEOUT', 30)
    read_timeout = settings.PUSH_NOTIFICATIONS.get('READ_TIMEOUT', 30)
    connection_per_host = settings.PUSH_NOTIFICATIONS.get('CONNECTIONS_PER_HOST', 10)
    process_butch = settings.PUSH_NOTIFICATIONS.get('PROCESS_BUTCH', 100)

    def handle(self, *args, **kwargs):
        self.stdout.write("push notifications emitter started")

        while True:
            interval = (datetime.utcnow() - timedelta(seconds=self.retry_interval)).replace(tzinfo=utc)
            try:
                with transaction.atomic():
                    events = PushNotificationEvent.actual_objects.select_for_update(nowait=True).filter(
                        Q(retry__isnull=True) | Q(retry__lt=self.retry),
                        Q(last_retried_at__isnull=True) | Q(last_retried_at__lt=interval)
                    ).all()[:self.process_butch]

                    events_len = len(events)
                    if events_len < 1:
                        time.sleep(1)
                        continue

                    self.stdout.write(
                        "proccessing {} events".format(events_len)
                    )

                    asyncio.run(self.emits(events))
            except Exception as e:
                traceback.print_exc()
            time.sleep(1)

    async def emits(self, events: List[PushNotificationEvent]):
        conn = aiohttp.TCPConnector(limit_per_host=self.connection_per_host)
        async with aiohttp.ClientSession(
                conn_timeout=self.connection_timeout, read_timeout=self.read_timeout,
                connector=conn) as session:
            tasks = []
            for event in events:
                tasks.append(
                    self.emit(session, event)
                )
            await asyncio.gather(*tasks)

    async def emit(self, session: aiohttp.ClientSession, event: PushNotificationEvent):
        event_id = event.event.event_id
        self.stdout.write(
            "emit event {}".format(event_id))
        
        utcnow = datetime.utcnow().replace(tzinfo=utc)
        event.retry = 1 if not event.retry else event.retry + 1
        event.last_retried_at = utcnow

        try:
            res = await event.post(session)
            res.raise_for_status()
            event.processed_at = utcnow
            self.stdout.write(
                "event {} has been delivered to {}".format(
                    event.event.event_id, res.url)
            )
        except Exception as e:
            self.stderr.write(
                "error while delivering the event {}, retry {}: {}".format(
                    event.event.event_id, event.retry, str(e))
            )
        finally:
            event.save()
