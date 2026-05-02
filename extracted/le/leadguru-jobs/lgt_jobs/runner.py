import json
from datetime import datetime, UTC
from lgt_jobs.lgt_common.pubsub.messages import publish_message2_pubsub
from lgt_jobs.lgt_data.engine import DelayedJob
from lgt_jobs.basejobs import InvalidJobTypeException, BaseBackgroundJobData, BaseBackgroundJob
from lgt_jobs.env import background_jobs_topic


def datetime_converter(o):
    if isinstance(o, datetime):
        return o.__str__()


class BackgroundJobRunner:
    @staticmethod
    def run(jobs_map: dict, data: dict):
        """
        @:param data received after dump
        @:param jobs_map job instance mapping
        """
        job_type_name = data["job_type"]
        job = jobs_map.get(job_type_name, None)

        if not job:
            raise InvalidJobTypeException(f"Unable to find job '{job_type_name}' in the list of modules")

        return job().run(data["data"])

    @staticmethod
    def submit(job: type, data: BaseBackgroundJobData):
        job_data = BaseBackgroundJob.dumps(job, data.dict())
        BackgroundJobRunner.submit_data(job_data)

    @staticmethod
    def submit_data(data: dict, topic: str = None):
        json_str = json.dumps(data, ensure_ascii=False, default=datetime_converter)
        BackgroundJobRunner.submit_json(json_str, topic)

    @staticmethod
    def submit_json(json_str: str, topic: str = None):
        if not topic:
            topic = background_jobs_topic
        print(topic)
        publish_message2_pubsub(topic, message_json=json_str)

    @staticmethod
    def schedule(jib: str, job: type, data: BaseBackgroundJobData, scheduled_at: datetime):
        job_data = BaseBackgroundJob.dumps(job, data.model_dump())
        DelayedJob(
            jib=jib,
            created_at=datetime.now(UTC),
            scheduled_at=scheduled_at,
            job_type=job.__name__,
            data=json.dumps(job_data, ensure_ascii=False, default=datetime_converter)
        ).save()

    @staticmethod
    def reschedule(jib: str, job: type, data: BaseBackgroundJobData, scheduled_at: datetime):
        BackgroundJobRunner.remove_schedule(jib)
        BackgroundJobRunner.schedule(jib, job, data, scheduled_at)

    @staticmethod
    def remove_schedule(jib: str):
        [job.delete() for job in DelayedJob.objects(jib=jib)]
