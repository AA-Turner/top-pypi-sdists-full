import httpx

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from asgi_correlation_id import correlation_id

from ..const import CORRELATION_ID_HEADER_KEY_NAME
from ..exception.internal_exception import GatewayTimeoutException, BadGatewayException


async def async_request(app: FastAPI, method, url, current_user: dict = None,
                        request_conn_pool_timeout: float = 0, request_conn_timeout: float = 0,
                        request_write_timeout: float = 0, response_read_timeout: float = 0,
                        **kwargs):
    if request_conn_pool_timeout <= 0:
        request_conn_pool_timeout = app.state.config.REQUEST_CONN_POOL_TIMEOUT
    if request_conn_timeout <= 0:
        request_conn_timeout = app.state.config.REQUEST_CONN_TIMEOUT
    if request_write_timeout <= 0:
        request_write_timeout = app.state.config.REQUEST_WRITE_TIMEOUT
    if response_read_timeout <= 0:
        response_read_timeout = app.state.config.RESPONSE_READ_TIMEOUT

    timeout = httpx.Timeout(connect=request_conn_timeout, read=response_read_timeout,
                            write=request_write_timeout, pool=request_conn_pool_timeout)

    if "headers" in kwargs.keys():
        kwargs.get("headers")[CORRELATION_ID_HEADER_KEY_NAME] = correlation_id.get() or ""
    else:
        kwargs["headers"] = {
            CORRELATION_ID_HEADER_KEY_NAME: correlation_id.get() or ""
        }

    if current_user and "access_token" in current_user:
        if "headers" in kwargs.keys():
            kwargs.get("headers")["Authorization"] = f"Bearer {current_user.get('access_token')}"
        else:
            kwargs["headers"] = {
                "Authorization": f"Bearer {current_user.get('access_token')}"
            }

    try:
        async with httpx.AsyncClient(timeout=timeout, verify=False) as client:
            if "json" in kwargs:
                kwargs["json"] = jsonable_encoder(kwargs["json"])

            app.state.logger.info(f"async_request() request, url: {url}, method: {method}, kwargs: {kwargs}")
            response = await client.request(method, url, **kwargs)
            app.state.logger.info(
                f"async_request() response, url: {url}, method: {method}, kwargs: {kwargs}, response: {response}, response.text: {response.text}")
            return response
    except httpx.TimeoutException as exc:
        app.state.logger.warn(
            f"async_request(), TimeoutException, exc: {exc}, url: {url}, method: {method}, kwargs: {kwargs}")
        raise GatewayTimeoutException(str(exc))
    except Exception as exc:
        app.state.logger.warn(
            f"async_request(), Exception, exc: {exc}, url: {url}, method: {method}, kwargs: {kwargs}")
        raise BadGatewayException(str(exc))


async def send_webhook_message(app: FastAPI, message: str):
    if app.state.config.WEBHOOK_BASE_URL:
        payload = {"text": message}
        try:
            await async_request(app, "POST", app.state.config.WEBHOOK_BASE_URL, json=payload)
        except Exception as e:
            app.state.logger.warn(f"Notify failure, Exception:{e}")
