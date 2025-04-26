#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : config
# @Time         : 2024/11/28 14:47
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
from datetime import timedelta

from celery import Task, shared_task
from kombu import Exchange, Queue
from tenacity import retry, stop_after_attempt, wait_exponential


class RetryableTask(Task):
    # 使用 tenacity 进行更灵活的重试控制
    @retry(
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry_error_callback=lambda retry_state: handle_final_failure(retry_state)
    )
    def run_with_retry(self, *args, **kwargs):
        return self.run(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        return self.run_with_retry(*args, **kwargs)


# 基础配置
broker_url = 'redis://localhost:6379/0'  # 消息代理（推荐使用Redis）
result_backend = 'redis://localhost:6379/1'  # 结果存储

# 时区设置
timezone = 'Asia/Shanghai'
enable_utc = False

# 任务序列化与反序列化配置
task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']

# 任务执行设置
task_soft_time_limit = 10 * 60  # 任务软超时时间（秒）
task_time_limit = 6 * task_soft_time_limit  # 任务硬超时时间（秒）

# 并发配置
worker_concurrency = 8  # worker并发数，一般设置为CPU核心数
worker_prefetch_multiplier = 4  # 预取任务数
worker_max_tasks_per_child = 256  # 每个worker执行多少个任务后自动重启

# 任务队列配置
task_default_queue = 'default'  # 默认队列
task_queues = (
    Queue('default', Exchange('default'), routing_key='default'),
    Queue('high_priority', Exchange('high_priority'), routing_key='high_priority'),
    Queue('low_priority', Exchange('low_priority'), routing_key='low_priority'),
)

# 任务重试配置
task_publish_retry = True  # 发布任务失败时重试
task_publish_retry_policy = {
    'max_retries': 3,  # 最大重试次数
    'interval_start': 0,  # 初始重试等待时间
    'interval_step': 0.2,  # 重试间隔递增步长
    'interval_max': 0.2,  # 最大重试间隔
}

# # 任务路由配置
# task_routes = {
#     'project.tasks.high_priority_task': {'queue': 'high_priority'},
#     'project.tasks.low_priority_task': {'queue': 'low_priority'},
# }
#
# # 定时任务配置
# beat_schedule = {
#     'task-every-30-seconds': {
#         'task': 'project.tasks.periodic_task',
#         'schedule': timedelta(seconds=30),
#     },
# }

# 日志配置
worker_log_format = '[%(asctime)s: %(levelname)s/%(processName)s] %(message)s'
worker_task_log_format = '[%(asctime)s: %(levelname)s/%(processName)s] [%(task_name)s(%(task_id)s)] %(message)s'

# 性能优化
worker_disable_rate_limits = True  # 禁用任务频率限制
task_acks_late = True  # 任务执行完成后再确认
task_reject_on_worker_lost = True  # worker异常关闭时任务会被重新分配

# 任务执行配置
task_always_eager = False  # 是否立即执行任务（调试用）


@shared_task(
    bind=True,
    base=RetryableTask,
)
def complex_task(self, *args, **kwargs):
    try:
        # 任务逻辑
        result = process_data()
        return result
    except TemporaryError as exc:
        # 临时错误，使用指数退避重试
        retry_countdown = min(2 ** self.request.retries * 60, 3600)
        raise self.retry(exc=exc, countdown=retry_countdown)
    except PermanentError as exc:
        # 永久错误，记录并标记失败
        logger.error(f"Permanent error occurred: {exc}")
        raise
