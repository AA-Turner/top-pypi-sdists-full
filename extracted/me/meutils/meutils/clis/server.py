#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : cli_fastapi
# @Time         : 2023/8/4 15:01
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 


from meutils.pipe import *


@cli.command()  # help会覆盖docstring
def celery_consumer(host='0.0.0.0', port: int = 8501):
    """
    # 消费者
    celery -A meutils.serving.celery.tasks worker -l info

    # 生产者
    mecli-server --host 127.0.0.1 --port 8000

    """

    from meutils.serving.fastapi import App
    from meutils.serving.celery.router import router

    app = App()
    app.include_router(router)
    app.run(host=host, port=port)


@cli.command()
def gunicorn_run(
        app: str,  # aiapi.views.apps:app
        project_dir: str = './',  # chdir
        port: int = 8501,
        workers: int = 3,
        threads: int = 2,
        preload: bool = False,
        pythonpath: str = 'python',
        gunicorn_conf: Optional[str] = None,
        max_requests: int = 1000,
        timeout: int = 300
):
    """
    python server.py gunicorn-run aiapi.views.apps:app --project-dir /Users/betterme/PycharmProjects/AI/aiapi

    todo:
        --chdir /Users/betterme/PycharmProjects/AI/aiapi 绝对路径
    """

    gunicorn_conf = gunicorn_conf or get_resolve_path('../serving/fastapi/gunicorn.conf.py', __file__)

    cmd = f"""
    cd {project_dir} && \
    {pythonpath} -m gunicorn -c {gunicorn_conf} \
      -k uvicorn.workers.UvicornWorker \
      --bind 0.0.0.0:{port} \
      --workers {workers} \
      --threads {threads} \
      --timeout {timeout} \
      --max-requests {max_requests} --max-requests-jitter 50 \
      {'--preload' if preload else ''} {app}
    """.strip()

    print(cmd)

    os.system(cmd)




@cli.command()
def uvicorn_run(
        app: str,
        project_dir: str = './',
        port: int = 8501,
        workers: int = 3,
        pythonpath: str = 'python',
        reload: bool = False,
):
    """
    python server.py uvicorn-run main:app --project-dir /Users/betterme/PycharmProjects/AI/aiapi
   -root-path
    """

    cmd = f"""
    cd {project_dir} && \
    {pythonpath} -m uvicorn {app} \
      --host 0.0.0.0 \
      --port {port} \
      --workers {workers}
    """.strip()
    if reload:
        cmd += ' --reload'

    print(cmd)

    os.system(cmd)


if __name__ == '__main__':
    cli()
