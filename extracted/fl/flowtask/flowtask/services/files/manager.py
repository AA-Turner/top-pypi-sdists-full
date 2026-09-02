"""
FileManager.

Works with files, download, upload and delete files over FS using an API.

TODO: Send a data-preview (first 10 rows) of uploaded file
TODO: html-template for Uploader preview with "back" button.
"""
import os
import hashlib
from pathlib import Path
import aiofiles
import magic
from aiohttp import web
from aiohttp.web import StreamResponse, FileResponse
from navigator.views import BaseView
from navigator.responses import Response
from ...utils.json import json_encoder
from ...exceptions import (
    FileError
)
from ...conf import FILES_PATH


class FileManagerFactory:
    def __new__(cls, path: Path, subpath: str = 'files') -> bool:
        class CustomFileManager(FileManager):
            pass

        CustomFileManager.define_filepath(path, subpath)
        return CustomFileManager

class FileManager(BaseView):
    """API View for managing Files.
    """
    _path: Path = None
    _subpath: str = None

    @classmethod
    def define_filepath(cls, path: Path, subpath: str = 'files'):
        if isinstance(path, str):
            path = Path(path).resolve()
        cls._path = path
        cls._subpath = subpath

    def __init__(self, request, *args, **kwargs):
        BaseView.__init__(self, request, *args, **kwargs)
        self.mime = magic.Magic(mime=True)

    def file_exists(self, program, filename):
        fpath = self._path.joinpath(program, self._subpath, filename)
        if fpath.exists():
            return fpath
        else:
            return None

    def delete_file(self, filename):
        if filename.exists():
            try:
                filename.unlink()
            except Exception as err:
                raise FileError(
                    f"Error deleting file: {err}"
                ) from err

    async def read_file(self, filename):
        content = None
        try:
            async with aiofiles.open(filename, 'rb') as afp:
                content = await afp.read()
            return content
        except Exception as err:
            raise FileError(
                f"Error reading file: {err}"
            ) from err

    async def get_response(self, headers) -> web.Response:
        """Returns a valid Web.Response"""
        response = StreamResponse(
            status=200,
            reason='OK',
            headers={
                'Pragma': "public",  # required,
                'Expires': '0',
                'Connection': 'keep-alive',
                'Cache-Control': 'must-revalidate, post-check=0, pre-check=0',
                **headers
            }
        )
        response.enable_compression()
        return response

    async def return_file(self, filename, **kwargs) -> web.Response:
        """Returns a File based on a Stream Response
        """
        # HTTP headers for forcing file download
        # TODO: try to discover the content type
        content_type = "application/octet-stream"
        # content_type = "application/vnd.ms-excel"
        content = await self.read_file(filename)
        file = filename.name
        headers = {
            'Content-Type': content_type,
            'Content-Transfer-Encoding': 'binary',
            'Content-Disposition': f'attachment; filename="{file}"'
        }
        if 'headers' in kwargs:
            headers = {**headers, **kwargs['headers']}
        try:
            response = await self.get_response(headers)
            response.headers['X-Content-SHA1'] = hashlib.sha1(file.encode('utf-8')).hexdigest()
            response.content_type = content_type
            # push the content
            response.content_length = len(content)
            await response.prepare(self.request)
            if self.request.transport.is_closing():
                return Response(
                    text=json_encoder({"Closed Output"}), status=404,
                    content_type='application/json'
                )
            await response.write(content)
            await response.write_eof()
            # await resp.drain()
            return response
        except Exception as err:
            raise FileError(
                f"Error reading file {filename} for download: {err}"
            ) from err

    async def save_file(self, filename, content):
        try:
            async with aiofiles.open(filename, 'wb') as out:
                content.seek(0)
                await out.write(content.read())
                await out.flush()
            return True
        except Exception as err:
            raise FileError(
                f"Error Saving File: {err}"
            ) from err

    def list_dir(self, program, filepath):
        fpath = self._path.joinpath(program, self._subpath, filepath)
        file_list = []
        if fpath.exists():
            for f in fpath.iterdir():
                if f.is_file():
                    try:
                        mime = self.mime.from_file(f)
                    except TypeError:
                        mime = None
                    file_stats = os.stat(f)
                    file = {
                        "path": str(f),
                        "filename": f.name,
                        "size": f"{file_stats.st_size / (1024):.2f} Kb",
                        "mimetype": mime
                    }
                    file_list.append(file)
                else:
                    file_list.append(str(f))  # is a directory
        return file_list

    async def get(self):
        """
        GET Method.
        ---
        description: Managing Files.
        tags:
        - File Manager
        consumes:
        - application/json
        produces:
        - application/json
        """
        arguments = self.get_arguments()
        # {'program': 'walmart', 'filepath': ''}
        program = arguments['program']
        try:
            filepath = arguments['filepath']
        except KeyError:
            filepath = None
        try:
            meta = arguments['meta']
        except KeyError:
            meta = None
        if not filepath:
            # return a list of files on root directory
            result = self.list_dir(program, '')
            headers = {
                'X-STATUS': 'OK',
                'X-MESSAGE': 'Root Directory listing'
            }
            return self.json_response(
                response=result,
                headers=headers,
                status=202
            )
        else:
            root, ext = os.path.splitext(filepath)
            if not ext:
                # is a directory, need to list the files in that directory
                result = self.list_dir(program, filepath)
                headers = {
                    'X-STATUS': 'OK',
                    'X-MESSAGE': 'Directory listing'
                }
                return self.json_response(
                    response=result,
                    headers=headers,
                    status=202
                )
            else:
                # get file metadata or download a file
                try:
                    if not meta:
                        if filename := self.file_exists(program, filepath):
                            # getting this file from server using a Stream API
                            headers = {
                                'X-STATUS': 'OK',
                                'X-MESSAGE': 'File Exists',
                                'X-FILENAME': str(filename),
                                "X-DIRECTORY": str(filename.parent),
                                'X-FILESIZE': f"{filename.stat().st_size}"
                            }
                            # return await self.return_file(filename, headers=headers)
                            return FileResponse(filename, headers=headers, status=200)
                        else:
                            # file doesn't exists
                            headers = {
                                'X-STATUS': 'EMPTY',
                                'X-MESSAGE': 'File not Found',
                                'X-FILENAME': ''
                            }
                        return self.no_content(headers=headers)
                    else:
                        ### returning only the File Stats:
                        filename = self.file_exists(program, filepath)
                        headers = {
                            'X-STATUS': 'OK',
                            'X-MESSAGE': 'File Exists',
                            'X-FILENAME': str(filename),
                            'X-FILESIZE': f"{filename.stat().st_size}"
                        }
                        try:
                            mime = self.mime.from_file(filename)
                        except TypeError:
                            mime = "application/octet-stream"
                        fileinfo = {
                            "filename": str(filename),
                            "name": str(filename.name),
                            "directory": str(filename.parent),
                            "mimetype": mime,
                            "size": f"{filename.stat().st_size / (1024):.2f}"
                        }
                        return self.json_response(
                            response=fileinfo,
                            headers=headers,
                            status=200
                        )
                except Exception as err:
                    return self.critical(
                        exception=err
                    )

    async def head(self):
        """
        HEAD Method.
        description: Sent response about file exists or not.
        tags:
        - files
        - File Manager
        - filesystem
        - file
        consumes:
        - application/json
        produces:
        - application/json
        """
        arguments = self.get_arguments()
        # {'program': 'walmart', 'filepath': 'seasonality.xslx'}
        try:
            if filename := self.file_exists(arguments['program'], arguments['filepath']):
                headers = {
                    'X-STATUS': 'OK',
                    'X-MESSAGE': 'File Exists',
                    'X-FILENAME': str(filename),
                    'X-DIRECTORY': str(filename.parent),
                    'X-FILESIZE': f"{filename.stat().st_size}",
                    "X-SIZE": f"{filename.stat().st_size / (1024):.2f} Kb"
                }
                print(headers)
            else:
                # file doesn't exists
                headers = {
                    'X-STATUS': 'EMPTY',
                    'X-MESSAGE': 'File not Found',
                    'X-FILENAME': ''
                }
            return self.no_content(headers=headers)
        except Exception as err:
            return self.critical(
                exception=err
            )

    async def delete(self):
        """
        DELETe Method.
        description: Deletes a File (if exists) on Directory
        tags:
        - files
        - File Manager
        - filesystem
        - file
        consumes:
        - application/json
        produces:
        - application/json
        """
        arguments = self.get_arguments()
        try:
            if filename := self.file_exists(arguments['program'], arguments['filepath']):
                # trying to delete the file:
                try:
                    self.delete_file(filename)
                    # deletes sucessful
                    headers = {
                        'X-STATUS': 'OK',
                        'X-MESSAGE': 'File Deleted',
                        'X-FILENAME': str(filename)
                    }
                    msg = {
                        "response": f'File {filename!s} was deleted successfully'
                    }
                    state = 202
                except Exception as err:
                    headers = {
                        'X-STATUS': 'FAIL',
                        'X-MESSAGE': 'Error Deleting File',
                        'X-ERROR': str(err),
                        'X-FILENAME': str(filename)
                    }
                    msg = {
                        "response": f'Failed deleting file {filename!s}'
                    }
                    state = 401
                return self.json_response(
                    response=msg,
                    headers=headers,
                    status=state
                )
            else:
                # file doesn't exists
                headers = {
                    'X-STATUS': 'EMPTY',
                    'X-MESSAGE': 'File not Found',
                    'X-FILENAME': ''
                }
            return self.no_content(headers=headers)
        except Exception as err:
            return self.critical(
                exception=err
            )

    async def post(self):
        """
        POST Method.
        description: upload a file onto repository directory.
        tags:
        - files
        - File Manager
        - filesystem
        - file
        consumes:
        - application/json
        produces:
        - application/json
        """
        arguments = self.get_arguments()
        program = arguments['program']
        try:
            filepath = arguments['filepath']
        except KeyError:
            filepath = ''

        # post-data
        frm = await self.request.post()
        try:
            file = frm.get('file_name')
        except (ValueError, KeyError) as err:
            return self.error(
                exception=err,
                status=406
            )
        # get the filename for save:
        if filepath != '':
            root, ext = os.path.splitext(filepath)
            if not ext:
                # is a directory, firstly, check if root exists over FS
                print('ROOT ', root)
                filepath = self._path.joinpath(program, 'files', root)
                if not filepath.exists():
                    filepath.mkdir()
                # create the new filename:
                filename = file.filename
                fpath = filepath.joinpath(filename)
            else:
                # is a filename, with (or without) subfolder
                filename = arguments['filepath']
                filepath = self._path.joinpath(program, self._subpath, filename)
                if not filepath.parent.exists():
                    filepath.parent.mkdir()
                # at the end, the new name of the file:
                fpath = filepath
        else:
            # preserving original name
            filename = file.filename
            fpath = self._path.joinpath(program, self._subpath, filename)
        # get file handler
        iofile = file.file
        mimetype = file.content_type
        # fpath = self._path.joinpath(program, 'files', filename)
        # TODO: saving file using a thread executor:
        try:
            if fpath.exists():
                # unlink the previous file
                fpath.unlink()
            if await self.save_file(fpath, iofile):
                headers = {
                    'X-STATUS': 'OK',
                    'X-MESSAGE': 'File Uploaded',
                    'X-FILENAME': str(fpath)
                }
                return self.json_response(
                    response=f"File uploaded successfully: {filename}",
                    headers=headers,
                    status=202
                )
            else:
                headers = {
                    'X-STATUS': 'ERROR',
                    'X-MESSAGE': 'Not Uploaded',
                    'X-FILENAME': str(fpath)
                }
                return self.error(
                    response=f'Cannot upload the file {filename!s}',
                    status=403
                )
        except Exception as err:
            return self.error(
                response=f'Cannot upload file {filename!s}',
                exception=err,
                status=406
            )

    async def put(self):
        """
        PUT Method.
        description: Create a new directory.
        tags:
        - files
        - File Manager
        - filesystem
        - file
        consumes:
        - application/json
        produces:
        - application/json
        """
        arguments = self.get_arguments()
        program = arguments['program']
        try:
            filepath = arguments['filepath']
        except KeyError:
            filepath = ''

        if filepath != '':
            root, ext = os.path.splitext(filepath)
        else:
            root = ''
            ext = None
        try:
            if not ext:
                filepath = self._path.joinpath(program, self._subpath, root)
                if not filepath.exists():
                    filepath.mkdir()
                    headers = {
                        'X-STATUS': 'OK',
                        'X-MESSAGE': 'File Uploaded',
                        'X-FOLDER': str(filepath)
                    }
                    return self.json_response(
                        response="Folder Created successfully",
                        headers=headers,
                        status=202
                    )
                else:
                    headers = {
                        'X-STATUS': 'ERROR',
                        'X-MESSAGE': 'Path exists',
                        'X-FOLDER': str(filepath)
                    }
                    return self.json_response(
                        response='Path exists',
                        headers=headers,
                        status=403
                    )
            else:
                headers = {
                    'X-STATUS': 'ERROR',
                    'X-MESSAGE': 'Path not directory',
                    'X-FOLDER': str(filepath)
                }
                return self.json_response(
                    response='Path not directory',
                    headers=headers,
                    status=403
                )
        except Exception as err:
            raise FileError(
                f"Error Creating Folder: {err}"
            ) from err
