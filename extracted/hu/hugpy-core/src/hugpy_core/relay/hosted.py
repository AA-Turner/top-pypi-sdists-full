"""Wire optional hosted arms before their routes or background jobs execute."""


def configure_arms(app):
    from hugpy_core.relay import internal, inference_catalog, inference_requests
    from hugpy_core.relay.video_transport import execute_task, observe_task, cancel_task

    def executor(caller):
        def execute(**kwargs):
            with internal.app_context(app):
                return internal.execute_prompt(caller=caller, **kwargs)
        return execute

    try:
        from hugpy_video.intel import plane
    except ModuleNotFoundError as exc:
        if exc.name != 'hugpy_video':
            raise
    else:
        plane.set_model_task_source(inference_catalog.model_tasks)
        plane.set_model_catalog_source(inference_catalog.video_models)
        plane.set_text_model_source(inference_catalog.text_models)
        plane.set_task_executor(lambda req: execute_task(app, req))
        plane.set_prompt_executor(executor('video'))
        plane.set_task_observer(observe_task)
        # An older installed video has no canceller seam; core still hosts it.
        set_canceller = getattr(plane, 'set_task_canceller', None)
        if set_canceller is not None:
            set_canceller(cancel_task)
        from hugpy_core.web.routes import catalog_rows, workers_list
        from hugpy_core.config.settings import task_bindings
        from hugpy_core.web.console_routes import queue_feed
        from hugpy_core.web.api_access import principal, valid_use_authorization
        def workers():
            with internal.app_context(app):
                return workers_list().get_json()
        plane.set_core_sources(catalog=catalog_rows, workers=workers, queue=queue_feed,
                               verify_use_key=valid_use_authorization, principal=principal,
                               picker_models=inference_catalog.picker_models,
                               task_bindings=lambda: task_bindings(surface='video'),
                               assist_submit=lambda body: inference_requests.submit('video-assist', body),
                               assist_ticket=lambda ticket: inference_requests.ticket(ticket, kind='video-assist'),
                               assist_stream=lambda ticket: inference_requests.stream(ticket, kind='video-assist'))

    try:
        from hugpy_media import host
    except ModuleNotFoundError as exc:
        if exc.name != 'hugpy_media':
            raise
    else:
        from hugpy_core.registry.central_store import rows as central_rows
        host.configure(executor=executor('media'), catalog=inference_catalog.media_models,
                       central_catalog=central_rows)
