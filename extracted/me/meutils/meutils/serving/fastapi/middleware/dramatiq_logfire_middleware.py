#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : logfire_middleware
# @Time         : 2026/3/2 23:52
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
import dramatiq
import logfire
from opentelemetry import trace
from opentelemetry.propagate import inject, extract


class LogfireTracingMiddleware(dramatiq.Middleware):
    """
    负责将 Web 端/生产端的 Logfire Trace ID 注入到消息体中，
    并在 Worker 端提取，从而实现跨进程的分布式链路追踪。
    """

    def before_enqueue(self, broker, message, delay):
        # 【生产者端】入队前，提取当前线程的 Trace 上下文，并注入到字典中
        headers = {}
        inject(headers)
        # 将 headers 存入 message.options，Dramatiq 会自动将其序列化并发送
        message.options["otel_headers"] = headers

    def before_process_message(self, broker, message):
        # 【消费者端】处理任务前，从消息中解析出 Trace 上下文
        headers = message.options.get("otel_headers", {})
        context = extract(headers)

        # 将上下文绑定到当前 Worker 线程
        token = trace.attach(context)

        # 开启 Logfire Span 记录任务执行
        span = logfire.span(
            f"Dramatiq Actor: {message.actor_name}",
            message_id=message.message_id,
            queue=message.queue_name
        )

        # 手动开启上下文管理器，并挂载到 message 对象上，保证跨方法的线程安全
        message._logfire_span_ctx = span.__enter__()
        message._logfire_span = span
        message._otel_token = token

    def after_process_message(self, broker, message, *, result=None, exception=None):
        # 【消费者端】任务执行完毕或抛出异常时
        span = getattr(message, "_logfire_span", None)
        if span:
            # 如果有异常，Logfire 会自动将其标记为 Error 并记录 Stacktrace
            if exception:
                span.__exit__(type(exception), exception, exception.__traceback__)
            else:
                span.__exit__(None, None, None)

        # 释放 Worker 线程的上下文
        token = getattr(message, "_otel_token", None)
        if token:
            trace.detach(token)



from dramatiq.brokers.rabbitmq import RabbitmqBroker
from dramatiq.brokers.redis import RedisBroker

broker = RedisBroker()
# 注册 Logfire 追踪中间件
broker.add_middleware(LogfireTracingMiddleware())

dramatiq.set_broker(broker)

