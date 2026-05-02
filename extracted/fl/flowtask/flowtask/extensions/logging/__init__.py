"""
LoggingFacility.

API For sending Logs to Backend.
"""
from navconfig.logging import logging
from navigator.views import BaseView
from ...extensions import BaseExtension


class LoggingFacility(BaseExtension):
    def setup(self, app):
        super().setup(app)
        # Logging Facility:
        self.app.router.add_view("/api/v1/log", Logger)


## TODO: migrate to Handler.
class Logger(BaseView):
    """Logging Facility."""

    async def post(self):
        data = await self.json_data()
        print(data)
        try:
            message = data["message"]
            del data["message"]
        except KeyError:
            return self.error(
                request=self.request, response="Log require Message Data", state=406
            )
        # TODO: using jsonschema to validate JSON request
        if "level" in data:
            level = data["level"]
        else:
            level = "debug"
        # adding tags:
        tags = ["Navigator"]
        if "tags" in data:
            tags = data["tags"] + tags
        try:
            if level == "error":
                logging.error(message, extra=data)
            elif level == "debug":
                logging.debug(message, extra=data)
            elif level == "warning":
                logging.warning(message, extra=data)
            elif level == "exception":
                logging.exception(message, extra=data)
            else:
                logging.info(message, extra=data)
            headers = {"X-STATUS": "OK", "X-MESSAGE": "Logging Success"}
            msg = {"message": message}
            return self.json_response(response=msg, headers=headers, state=202)
        except Exception as err:  # pylint: disable=W0703
            headers = {
                "X-STATUS": "Error",
                "X-MESSAGE": "Resource Error: Logging Error",
            }
            msg = {
                "state": "Failed",
                "message": "Error: Failed Logging operation",
                "status": 400,
            }
            return self.error(response=msg, exception=err, headers=headers, state=400)
