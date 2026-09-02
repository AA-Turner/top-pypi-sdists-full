from ...interfaces.notification import Notification
from ...exceptions import ActionError
from .abstract import AbstractEvent


class Notify(Notification, AbstractEvent):
    async def __call__(self, *args, **kwargs):
        default_message = self._kwargs.pop("message", None)
        message = kwargs.pop("message", default_message)
        # status = kwargs.pop('status', 'event')
        task = kwargs.pop("task", None)
        provider, recipient = self.get_notify(**self._kwargs)
        # Mask transform of message
        for key, value in self.message.items():
            self.message[key] = self.mask_replacement(value)
        ## TASK:
        if self.provider == "email":
            args = self.get_message(message)
            if hasattr(self, "with_attachment") and self.with_attachment is True:
                # check if result are files (build attachments)
                _vars = task.get_variables()
                if "FILENAMES" in _vars.keys():
                    result = _vars["FILENAMES"]
                elif "FILENAME" in _vars.keys():
                    result = _vars["FILENAME"]
                else:
                    result = kwargs.pop("result", [])
                self.list_attachment = self.get_attachment_files(result)
        elif self.provider == "telegram":
            args = self.get_message(message)
            if hasattr(self, "with_attachment") and self.with_attachment is True:
                _vars = task.get_variables()
                if "FILENAMES" in _vars.keys():
                    result = _vars["FILENAMES"]
                elif "FILENAME" in _vars.keys():
                    result = _vars["FILENAME"]
                else:
                    result = kwargs.pop("result", [])
                self.list_attachment = self.get_attachment_files(result)
                async with provider as notify:
                    result = await notify.send_document(
                        document=self.list_attachment[0],
                        caption=message,
                        disable_notification=True,
                    )
                    return result
        else:
            args = self.get_message(message)
        if self._template:
            args["template"] = self._template
        try:
            async with provider as notify:
                args["recipient"] = recipient
                if self.list_attachment:
                    args["attachments"] = self.list_attachment
                result = await notify.send(**args)
                self._logger.debug(f"Notification Status: {result}")
        except Exception as err:
            raise ActionError(f"Error Creating Notification App: {err}") from err
