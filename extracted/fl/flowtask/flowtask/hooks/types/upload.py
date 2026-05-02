import os
from typing import Optional, List
from aiohttp import web
from .http import HTTPHook


class UploadHook(HTTPHook):
    """UploadHook.

    A Trigger that handles file uploads via HTTP POST/PUT requests.
    """

    methods: list = ["POST", "PUT"]

    def __init__(
        self,
        *args,
        allowed_mime_types: Optional[List[str]] = None,
        allowed_file_names: Optional[List[str]] = None,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.allowed_mime_types = allowed_mime_types
        self.allowed_file_names = allowed_file_names

    async def post(self, request: web.Request):
        # Use handle_upload to get uploaded files and form data
        try:
            uploaded_files_info, form_data = await self.handle_upload(request)
        except Exception as e:
            # Return error response
            return self.response(
                response={'error': str(e)},
                status=400,
                content_type='application/json'
            )

        # Validate files if necessary
        for file_info in uploaded_files_info:
            file_path = file_info['file_path']
            file_name = file_info['file_name']
            mime_type = file_info['mime_type']

            if self.allowed_mime_types and mime_type not in self.allowed_mime_types:
                return self.response(
                    response={'error': f'Invalid mime type: {mime_type}'},
                    status=400,
                    content_type='application/json'
                )

            if self.allowed_file_names and file_name not in self.allowed_file_names:
                return self.response(
                    response={'error': f'Invalid file name: {file_name}'},
                    status=400,
                    content_type='application/json'
                )

        # Prepare data to pass to run_actions
        data = {
            'uploaded_files': [str(file_info['file_path']) for file_info in uploaded_files_info],
            'form_data': form_data
        }
        # Run actions
        result = await self.run_actions(**data)
        return self.response(
            response=result,
            status=self.default_status
        )

    async def put(self, request: web.Request):
        return await self.post(request)

    async def run_actions(self, **data):
        result = await super().run_actions(**data)
        try:
            # Clean up uploaded files after actions have run
            uploaded_files = data.get('uploaded_files', [])
            for file_path in uploaded_files:
                try:
                    os.remove(file_path)
                    self._logger.info(f"Deleted temporary file: {file_path}")
                except Exception as e:
                    self._logger.warning(f"Failed to delete temporary file {file_path}: {e}")
        finally:
            return result
