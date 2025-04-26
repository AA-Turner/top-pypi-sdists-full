from . import context


def delete(ctx, **kwargs):
    """Delete each of the components of a demo setup."""
    """
     - application demo-container
     - desktop demo-desktop
     - share demo-share
     - application_service demo-container-local-service-0
     - service-account demo-container-service-account
     - connector demo-connector
    """
    apiclient = context.get_apiclient_from_ctx(ctx)

    query_results = apiclient.connectors_api.list_agent_connector(**kwargs)
    for app in query_results.agent_connectors:
        if app.spec.name == "demo-connector":
            print(f"Will delete connector {app.metadata.id}")
            apiclient.connectors_api.delete_connector(
                **kwargs, connector_id=app.metadata.id
            )

    query_results = apiclient.application_api.list_applications(**kwargs)
    for app in query_results.applications:
        if app.name == "demo-container":
            print(f"Will delete application {app.id}")
            apiclient.application_api.delete_application(**kwargs, app_id=app.id)

    query_results = apiclient.app_services_api.list_desktop_resources(**kwargs)
    for app in query_results.desktop_resources:
        if app.spec.name == "demo-desktop":
            print(f"Will delete desktop {app.metadata.id}")
            apiclient.app_services_api.delete_desktop_resource(
                **kwargs, resource_id=app.metadata.id
            )

    query_results = apiclient.app_services_api.list_file_share_services(**kwargs)
    for app in query_results.file_share_services:
        if app.spec.name == "demo-share":
            print(f"Will delete share {app.metadata.id}")
            apiclient.app_services_api.delete_file_share_service(
                **kwargs, file_share_service_id=app.metadata.id
            )

    query_results = apiclient.app_services_api.list_application_services(**kwargs)
    for app in query_results.application_services:
        if app.name == "demo-container-local-service-0":
            print(f"Will delete app-serv {app.id}")
            apiclient.app_services_api.delete_application_service(
                **kwargs, app_service_id=app.id
            )

    query_results = apiclient.user_api.list_service_accounts(**kwargs)
    for sa in query_results.service_accounts:
        if sa.spec.name == "agent-connector-demo-connector-service-account":
            print(f"Will delete service-account {sa.metadata.id}")
            apiclient.user_api.delete_service_account(
                **kwargs, service_account_id=sa.metadata.id
            )
