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
from kombu import Exchange, Queue

# 基础配置
broker_url = 'redis://localhost:6379/0'  # 消息代理（推荐使用Redis）
broker_url = os.getenv('REDIS_URL', broker_url)

# result_backend = f"redis://localhost:6379/1"  # 结果存储
result_backend = f"{broker_url.replace('/0', '')}/1"  # 结果存储

# logger.debug(result_backend)

# 添加以下配置增加可靠性
broker_connection_retry = True
broker_connection_max_retries = 5
broker_connection_retry_on_startup = True

# 时区设置
enable_utc = False
timezone = 'Asia/Shanghai'

# 任务序列化与反序列化配置
task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']

# 并发配置
# worker_pool = 'solo'  # 工作进程池类型，可选：'prefork'、'eventlet'、'gevent'
worker_pool_restarts = True
worker_concurrency = 8  # worker并发数，一般设置为CPU核心数
worker_prefetch_multiplier = 3  # 预取任务数
worker_max_tasks_per_child = 256  # 每个worker执行多少个任务后自动重启

# 任务队列配置
task_default_queue = 'default'  # 默认队列
task_queues = (
    Queue('default', Exchange('default'), routing_key='default'),
    Queue('high_priority', Exchange('high_priority'), routing_key='high_priority'),
    Queue('low_priority', Exchange('low_priority'), routing_key='low_priority'),
)

# 任务执行设置
task_soft_time_limit = 10 * 60  # 任务软超时时间（秒）
task_time_limit = 2 * task_soft_time_limit  # 任务硬超时时间（秒）

# 任务重试配置
task_publish_retry = True  # 发布任务失败时重试
task_publish_retry_policy = {
    'max_retries': 5,  # 最大重试次数
    'interval_start': 0,  # 初始重试等待时间
    'interval_step': 2,  # 重试间隔递增步长
    'interval_max': 16,  # 最大重试间隔
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
task_acks_late = True  # 任务执行完成后再确认
task_reject_on_worker_lost = True  # worker异常关闭时任务会被重新分配
worker_disable_rate_limits = True  # 禁用任务频率限制

# 结果后端配置
result_expires = 30 * 24 * 3600  # 结果过期时间（秒）
result_persistent = True  # 结果持久化存储

# 任务执行配置
# task_always_eager = False  # 是否立即执行任务（调试用）

# 添加任务持久化配置
celery_task_store_errors_even_if_ignored = True
celery_task_ignore_result = False  # 不忽略结果
celery_task_track_started = True  # 跟踪任务状态

# Redis 持久化配置
broker_transport_options = {
    'visibility_timeout': 43200,  # 12小时
    'fanout_prefix': True,
    'fanout_patterns': True,
}
