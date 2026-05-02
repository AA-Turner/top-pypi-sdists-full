import aiohttp
from ...utils.json import json_encoder
from .abstract import AbstractEvent


class WebHook(AbstractEvent):
    def __init__(self, *args, **kwargs):
        self.url = kwargs.pop("url", None)
        super(WebHook, self).__init__(*args, **kwargs)

    async def __call__(self, *args, **kwargs):
        if not self.url:
            raise ValueError("URL was not provided for WebHook event action.")
        status = kwargs.pop("status", "event")
        task = kwargs.pop("task", None)
        program = task.getProgram()
        task_name = f"{program}.{task.taskname}"
        task_id = task.task_id
        try:
            stat = task.stats  # getting the stat object:
            stats = json_encoder(stat.to_json())
        except AttributeError:
            stats = None

        # Extract optional authentication parameters
        auth_type = self._kwargs.get("auth_type", None)
        auth_value = self._kwargs.get("auth_value", None)

        headers = {}
        if auth_type and auth_value:
            if auth_type.lower() == "basic":
                headers["Authorization"] = f"Basic {auth_value}"
            elif auth_type.lower() == "bearer":
                headers["Authorization"] = f"Bearer {auth_value}"
            else:
                raise ValueError(f"Unsupported authentication type: {auth_type}")

        # Prepare the payload. You can customize this based on your needs.
        payload = {
            "task": task_name,
            "id": str(task_id),
            "status": status,
            "message": kwargs.get("message", "Task Completed."),
            "stats": stats,
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.url, json=payload, headers=headers
            ) as response:
                if response.status != 200:
                    # Handle non-200 responses if necessary
                    response = await response.text()
                    self._logger.warning(
                        f"Error on WebHook response: {response}, status: {response.status}"
                    )
                else:
                    # Handle successful webhook call if necessary
                    return
