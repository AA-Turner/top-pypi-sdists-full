from .abstract import AbstractAction

class ProcessData(AbstractAction):
    """ProcessData.
    Process data received in a webhook event.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.params = kwargs

    async def open(self):
        pass

    async def close(self):
        pass

    async def run(self, hook, *args, **kwargs):
        """
        Sample Action for Processing uploaded files.
        """
        uploaded_files = kwargs.get('uploaded_files', [])
        form_data = kwargs.get('form_data', {})
        notification = kwargs.get('notification', None)
        if notification:
            self._logger.notice(f"Notification: {notification}")
            self._logger.info(
                f"Processing notification from channel '{notification.channel}': {notification.payload}"
            )
        # Process each uploaded file
        results = []
        for file_path in uploaded_files:
            # Open and process the file
            with open(file_path, 'r') as f:
                content = f.read()
                # Do something with the content
                results.append({'file': file_path, 'content_length': len(content)})
        return {'results': results, 'form_data': form_data}
