from celery import chain, shared_task
from django.db.models import Model

from wbcore.workers import Queue


@shared_task(queue=Queue.BACKGROUND.value)
def save_instance_as_task(instance):
    instance.save(_with_llm=False)


class LLMMixin(Model):
    _llm_config = []

    def get_all_on_save_with_condition(self):
        for config in self._llm_config:
            if config.on_save and config.check_condition(self):
                yield config

    def save(self, _with_llm: bool = True, _llm_synchronous: bool = False, *args, **kwargs):
        super().save(*args, **kwargs)
        if _with_llm:
            tasks = []
            for index, config in enumerate(self.get_all_on_save_with_condition()):
                tasks.append(config.schedule(self, initial=index == 0))
            if tasks:
                res = chain(*tasks, save_instance_as_task.s())
                if _llm_synchronous:
                    res.apply()
                else:
                    res.apply_async()

    class Meta:
        abstract = True
