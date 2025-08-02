from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html


def add_local_openapi_ui_to_api_app(
        *,
        app: FastAPI
):
    @app.get("/docs", include_in_schema=False)
    async def custom_swagger_ui_html():
        return get_swagger_ui_html(
            openapi_url=app.openapi_url,
            title=app.title,
            swagger_js_url="/static/swagger-ui/swagger-ui-bundle.js",
            swagger_css_url="/static/swagger-ui/swagger-ui.css",
            swagger_favicon_url="/static/openapi-favicon.png"
        )

    @app.get("/redoc", include_in_schema=False)
    async def custom_redoc_html():
        return get_redoc_html(
            openapi_url=app.openapi_url,
            title=app.title,
            redoc_js_url="/static/redoc/redoc.standalone.js",
            redoc_favicon_url="/static/openapi-favicon.png"
        )

    return app
