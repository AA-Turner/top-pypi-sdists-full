"""
FileService.

Work with slug-based file definitions, upload, download, enable tasks, etc.
"""
import asyncio
import logging
import os
import re
import traceback
import uuid
from io import BytesIO, StringIO
from pathlib import Path
import cchardet
import magic
import pandas
import aiofiles
from asyncdb import AsyncDB
from asyncdb.exceptions import NoDataFound
from navigator.conf import asyncpg_url
from navigator.views import BaseView
from ...exceptions import (
    FileError,
    FileNotFound,
    NotSupported,
    TaskFailed,
    TaskNotFound
)
# tasks
from ...services.tasks import launch_task
from ...conf import FILES_PATH
from .model import FileModel


excel_based = [
    "application/vnd.ms-excel.sheet.binary.macroEnabled.12",
    "application/vnd.ms-excel.sheet.macroEnabled.12",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "application/vnd.ms-excel",
    "text/xml"
]


class FileUploaded:
    """
    FileUploaded.
        processing a FileField
    """
    _file = None
    _filefield: str = 'file'
    _content = None
    _directory = None
    _path = None
    _df = None
    _numRows = 0
    _columns = []
    _mimetype = 'application/octet-stream'
    _encoding = 'ISO-8859-1'

    def __init__(self, post, mimetype=None):
        self._file = post[self._filefield]
        self._content = self._file.file.read()
        if mimetype:
            self._mimetype = mimetype
        else:
            self._mimetype = self._file.content_type

    def content(self):
        return self._content

    @property
    def filename(self):
        return self._file.filename

    @property
    def df(self):
        return self._df

    def num_rows(self):
        return self._numRows

    @property
    def columns(self):
        return self._columns

    @property
    def content_type(self):
        return self._mimetype

    def is_empty(self):
        return not bool(self._content)

    def is_mime_valid(self, type):
        if type is not None:
            if self._mimetype == type or self._file.content_type == type:
                return True
            else:
                return False
        else:
            f = magic.Magic(mime=True)
            try:
                mime = f.from_buffer(self._content)
                return bool(mime)
            except Exception:
                # return True # cant enforcing Mime check using mime Magic
                return False

    def valid_name(self, name, pattern, rename=False):
        # TODO: using pattern to validate name structure
        if rename:
            return True
        # print(self._file.filename, pattern, name)
        if pattern is not None:
            return re.match(pattern, self._file.filename)
        elif self._file.filename != name:
            return False
        else:
            return True

    def valid_content(self, **kwargs):
        """
        valid_content.
            check if is a valid content-type
            ex: if is a csv, json or excel, open with pandas, if txt with stream, if image, etc
        """
        if self._mimetype in ('application/octet-stream', 'application/x-zip-compressed', 'application/zip'):
            return [True, None]

        self._encoding = self._get_encoding()
        s = self._get_decoded_content()
        try:
            data = StringIO(s)
            bdata = BytesIO(self._content)
        except Exception as err:
            logging.error(f'Error encoding data: {err}')
            s = str(self._content.decode('latin1').encode('utf-8'), 'utf-8')
            data = StringIO(s)
            bdata = BytesIO(self._content)
        # check if is a valid content-type
        try:            
            if self._mimetype == 'text/csv' or self._mimetype == 'text/plain':
                self._df = pandas.read_csv(
                    data,
                    decimal=',',
                    engine='c',
                    keep_default_na=False,
                    na_values=['TBD', 'NULL', 'null', ''],
                    encoding=self._encoding,
                    skipinitialspace=True,
                    low_memory=False,
                    **kwargs
                )
            elif self._mimetype == 'application/json':
                self._df = pandas.read_json(
                    data,
                    orient='records',
                    encoding=self._encoding,
                    low_memory=False,
                    **kwargs
                )
            elif self._mimetype in excel_based:
                if self._mimetype == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
                    # xlsx or any openxml based document
                    file_engine = 'openpyxl'
                elif self._mimetype == 'application/vnd.ms-excel.sheet.binary.macroEnabled.12':
                    file_engine = 'pyxlsb'
                elif self._mimetype == "application/vnd.ms-excel":
                    file_engine = 'xlrd'
                else:
                    try:
                        ext = Path(self._file.filename).suffix
                    except (AttributeError, ValueError):
                        ext = '.xls'
                    if ext == '.xls':
                        file_engine = 'xlrd'
                    else:
                        file_engine = 'openpyxl'
                self._df = pandas.read_excel(
                    bdata,
                    engine=file_engine,
                    keep_default_na=True,
                    # low_memory=False,
                    **kwargs
                )
            else:
                # TODO: currently is and invalid content
                return [False, f'Error: Invalid content type {self._file.content_type}']
        except pandas.errors.EmptyDataError as err:
            raise Exception(
                f"Error on Empty File: {self._file.filename}, error: {err}"
            ) from err
        except pandas.errors.ParserError as err:
            raise Exception(
                f"Error on Parsing File: {self._file.filename}, error: {err}"
            ) from err
        except ValueError as err:
            raise Exception(
                f"Error on File: {self._file.filename}, error: {err}"
            ) from err
        except Exception as err:
            raise Exception(
                f"Cannot Process File: {self._file.filename}, error: {err}"
            ) from err
        # exists dataframe:
        print(self._df)
        try:
            if self._df.empty:
                return [True, 'DataFrame is Empty']
            else:
                # self._df = self._df.fillna('')
                self._columns = list(self._df.columns)
                self._numRows = len(self._df.index)
                return [True, None]
        except Exception as err:
            return [False, f'Error Processing Dataframe, {err.__class__} {err}']

    def _get_encoding(self):     
        try:
            result_charset = cchardet.detect(self._content)
            confidence = result_charset['confidence']
            encoding = result_charset['encoding']
            if confidence < 0.6:
                logging.warning(
                    f'Warning: charset confidence was only {confidence}'
                )
            if result_charset['encoding'] == 'ascii' or result_charset['encoding'] == 'ASCII':
                encoding = "utf-8"
        except Exception as e:
            print('Error: ', e)
            encoding = 'ISO-8859–1'
        finally:
            if encoding is None:
                encoding = "ISO-8859–1"
        
        logging.debug(f'Detected Encoding is: {encoding}')
        return encoding
        
    def _get_decoded_content(self) -> str:
        for enc in (self._encoding, 'utf-8', 'latin1', 'ascii'):
            try:
                return str(self._content, enc)
            except UnicodeDecodeError:
                continue
        else:
            raise FileError(message="Can't decode file!", status=422)

    @property
    def path(self):
        return self._path

    def directory(self, dirname, filename: str = None):
        if not filename:
            filename = self._file.filename
        self._directory = dirname
        self._path = os.path.join(dirname, filename)

    async def save(self, directory=None, forcing_charset: bool = False):
        if directory:
            self.directory(directory)
        async with aiofiles.open(self._path, 'w+b') as fp:
            try:
                if forcing_charset is True:
                    await fp.write(self._content.decode(self._encoding).encode('utf-8'))
                else:
                    await fp.write(self._content)
                await fp.flush()
            except (ValueError, asyncio.InvalidStateError) as err:
                logging.exception(f'Saving File Error: {err!s}')
                raise
            except Exception as err:
                logging.exception(f'Saving File Error: {err!s}')
                raise


class FileService(BaseView):

    log_data = {}
    file_slug = None
    user_id = None
    scheduler = None
    job = None
    permission = None

    async def get(self):
        """
        ---
        description: Get all the Files objects in the current scope and program
        summary: get the files information and attributes
        tags:
        - FileService
        produces:
        - application/json
        parameters:
        - name: user_id
          description: user id to filter
          in: path
          required: true
          type: integer
        - name: file_slug
          description: file slug
          in: path
          required: true
          type: string
        responses:
            "200":
                description: returns valid data
            "204":
                description: No data
            "403":
                description: Forbidden Call
            "404":
                description: Program o File not found
            "406":
                description: Query Error
        """
        try:
            data = {}
            user_id = self.request.rel_url.query['user_id']
            file_slug = self.request.rel_url.query['file_slug']
        except Exception as e:
            headers = {
                'X-STATUS': 'EMPTY',
                'X-MESSAGE': 'Data not Found',
                'X-ERROR': str(e)
            }
            return self.no_content(headers=headers)
        finally:
            await self.close()

    async def valid_permission(self, user_id, codename):
        """
        valid_permission.
            Check if the user have permission for one func on the system.
        """
        # get from db
        try:
            db_schema = os.environ.get('DB_SCHEMA', 'troc')
            sql = f"SELECT DISTINCT(tug.groups_id), ap.id as permission_id, ap.name as permission_name, ap.codename \
            FROM {db_schema}.troc_user_group tug  \
            LEFT JOIN public.auth_group_permissions agp on agp.group_id = tug.groups_id  \
            LEFT JOIN public.auth_permission ap on ap.id = agp.permission_id \
            WHERE tug.user_id = {user_id} and ap.codename = '{codename}';"
            result = await self.query(sql)
            if result:
                self.permission = result[0]
                return True
            else:
                return False
        except Exception as e:
            return False

    async def put(self):
        """ PUT FileService.
        description: Upload a File and, optionally, running an associated Task
        Parameters:
         file_slug: slug of the file in TROC files table
         program_slug: associated program
         mimetype: optional mime-type, default csv
         module_id: optional module ID
         task: boolean in query-params to disable running task.
         long_running: query-param to attach a Task in a Thread Pool
        """
        error = ''
        no_worker = False
        try:
            qp = self.query_parameters(self.request)
        except ValueError as e:
            logging.exception(f'Error getting Parameters for FileService: {e}')
            return self.critical(
                reason=f'Error getting Parameters for FileService: {e}'
            )
        try:
            runtask = bool(qp['task'])
        except KeyError:
            runtask = False
        logging.debug(f'Run Task is: {runtask}')
        try:
            queued = qp['long_running']
        except KeyError:
            queued = False
        try:
            no_worker = str(qp['no_worker']).lower() in ('true', '1')
        except KeyError:
            no_worker = False
        try:
            post = await self.request.post()
        except Exception as e:
            return self.critical(
                f'Error getting Parameters for FileService: {e}'
            )
        # file slug
        try:
            file_slug = post['file_slug']
        except (TypeError, KeyError):
            file_slug = None
        try:
            program_slug = post['program_slug']
        except (TypeError, KeyError):
            if file_slug:
                program_slug = file_slug.split('_')[0]
            else:
                program_slug = os.environ.get('APP_PROGRAM_SLUG', 'troc')
        # TODO: get program id from program_slug
        try:
            subdir = qp['subdir']
        except KeyError:
            try:
                subdir = post['subdir']
            except KeyError:
                subdir = ''
        # email (optional, used to tag uploaded data with the submitter)
        try:
            email = post['email']
        except (TypeError, KeyError):
            email = None
        # mime type
        try:
            mimetype = post['mimetype']
        except (TypeError, KeyError):
            mimetype = 'text/csv'
        logging.debug(
            f'File Upload for program {program_slug} for slug {file_slug}'
        )
        try:
            # getting the FileField Object
            f = FileUploaded(post, mimetype=mimetype)
            filename = f.filename
            content_type = f.content_type
            logging.debug(
                f'Opening File: {filename} with content type: {content_type}'
            )
        except Exception as e:
            return self.error(
                reason=f"Error on Uploaded File: {e}"
            )
        if f.is_empty():
            headers = {
                'X-STATUS': 'EMPTY',
                'X-MESSAGE': 'File is Empty'
            }
            return self.no_content(headers=headers)
        elif not f.is_mime_valid(mimetype):
            headers = {
                'X-STATUS': 'Error',
                'X-MESSAGE': 'File has wrong mimetype',
                'X-FILENAME': f.filename
            }
            data = {
                "message": f"Wrong mimetype on file {f.filename}:  got {mimetype}, expected: {f.content_type}"
            }
            logging.error(
                f"Wrong mimetype on {f.filename}:  got {mimetype}, expected: {f.content_type}"
            )
            return self.error(response=data, headers=headers, status=401)
        if not file_slug:
            filepath = FILES_PATH.joinpath(program_slug, 'files', subdir)
            if not filepath.exists():
                try:
                    filepath.mkdir(parents=True)
                except Exception as err:
                    logging.error(
                        f'Error creating Directory: {err}'
                    )
            # TODO: get configuration for saving files from frontend
            # TODO: validate user permissions
            # TODO: using the current program directory to upload the file
            f.directory(filepath)
            try:
                await f.save()
                headers = {
                    'X-STATUS': 'OK',
                    'X-MESSAGE': 'File Uploaded'
                }
                data = {
                    "message": f"file was uploaded to directory: {f.path}"
                }
                return self.json_response(response=data, headers=headers)
            except Exception as e:
                return self.critical(reason=f'Uncaught Error on File Uploaded: {e}')
        else:
            try:
                headers = {
                    'X-STATUS': 'Error',
                    'X-MESSAGE': f'File Slug doesnt exists or is disabled {file_slug}',
                    'X-FILENAME': f.filename
                }
                db = AsyncDB('pg', dsn=asyncpg_url)
                async with await db.connection() as conn:
                    FileModel.Meta.connection = conn
                    # getting from model:
                    filedef = await FileModel.get(file_slug=file_slug)
                    logging.debug(f'Detected File Definition: {filedef}')
                    if not filedef:
                        return self.error(
                            response=f"File Slug doesn't Exists: {file_slug}",
                            headers=headers
                        )
            except NoDataFound:
                return self.error(
                    response=f"File Service: Slug not Found: {file_slug}",
                    status=404
                )
            except Exception as err:
                print(err, type(err))
                return self.error(
                    response=f"Error querying File Service: {file_slug}: {err!s}"
                )
            # start validation
            mime = filedef.mimetype
            if mime and not f.is_mime_valid(mime):
                data = {
                    "message": f"Wrong mimetype for File, got: {f.content_type} expected: {mime}"
                }
                return self.error(response=data)
            name = filedef.filename
            attributes = filedef.attributes
            params = filedef.params
            logging.debug(
                f'File Definition: {name}, Attributes: {attributes}, {params}'
            )
            # rename file
            try:
                rename = name['rename']
            except (KeyError, TypeError):
                rename = False
            # create directory
            try:
                create = attributes['create_dir']
            except (KeyError, TypeError):
                create = False

            if 'name' in name:
                if not f.valid_name(name['name'], name['pattern'], rename=rename):
                    data = {
                        "message": f"Wrong Filename for File, expected: {name['name']}"
                    }
                    return self.error(response=data)
                    # file is valid, needs to save:
            try:
                path = name['path']
            except KeyError:
                path = params['data_path']
            path = Path(path).resolve()
            if not path.exists():
                # if doesnt exists path, is a relative path
                logging.debug(f'Saving file on path: {path!s}')
                try:
                    if create is True:
                        path.mkdir(exist_ok=True, parents=True)
                    else:
                        # directory to upload file doesn't exists
                        data = {
                            "message": f"Directory for upload File doesn't exists {path}"
                        }
                        return self.error(response=data)
                except Exception as err:
                    data = {
                        "message": f"Error creating Directory: {err!s}"
                    }
                    return self.error(
                        exception=err,
                        response=data
                    )
            # validacion de contenido (verificar csv, validate columns, data structure, etc)
            try:
                validate = params['validate']
            except (KeyError, TypeError):
                validate = True
            if validate:
                try:
                    pargs = params['pandas']
                except KeyError:
                    pargs = {}
                result, error = f.valid_content(**pargs)
                logging.debug(
                    f'Validate pandas File: {result}, error: {error}')
                if error and not result:
                    data = {"status": error}
                    return self.error(response=data, status=403)
                elif result and error:
                    data = {
                        "status": error,
                        "message": "Empty File"
                    }
                    return self.error(response=data, status=404)
                else:
                    # dataframe is valid, we need to make other validations
                    if filedef.fields:
                        try:
                            case_sensitive = filedef.case_sensitive
                        except Exception:
                            case_sensitive = False
                        if case_sensitive is True:
                            validate_cols = filedef.fields
                            columns = f.columns
                        else:
                            validate_cols = [f.lower() for f in filedef.fields]
                            columns = [c.lower() for c in f.columns]
                        if validate_cols:
                            if validate_cols != columns:
                                data = {
                                    "status": "Error",
                                    "message": "Invalid Column Names",
                                    "expected": validate_cols,
                                    "columns": f.columns
                                }
                                return self.error(response=data, status=401)
                # TODO: make other validations, as data validations, and data quality
                # define the directory to save file
                f.directory(path)
                try:
                    forcing_charset = attributes['forcing_charset']
                except KeyError:
                    forcing_charset = False
                if os.path.exists(f.path) and attributes['overwrite'] is False:
                    # file exists
                    data = {
                        "message": f"File already exists {f.path}"
                    }
                    return self.error(response=data)
                else:
                    try:
                        await f.save(
                            directory=path,
                            forcing_charset=forcing_charset
                        )
                    except OSError as err:
                        logging.exception(
                            f'Connection Aborted on Upload: {err!s}'
                        )
                    except Exception as err:
                        print(err)
                        data = {
                            "message": f"Error Saving File on Path {f.path}"
                        }
                        return self.error(response=data)
                # file exists and was uploaded
                headers = {
                    'X-STATUS': 'OK',
                    'X-MESSAGE': 'File was Uploaded'
                }
                response = {
                    "message": f"file {f.filename} was uploaded to {f.path}",
                    "state": 202
                }
                logging.debug(response['message'])
                result = {}
                run_task = filedef.task_enabled if filedef.task_enabled else runtask
                if run_task is True:
                    # if runtask is True or filedef.task_enabled is True:
                    try:
                        args = params['args']
                    except KeyError:
                        args = {}
                    # need to instanciate a Task Object to launch Task
                    try:
                        queued = params['long_running']
                    except KeyError:
                        pass
                    try:
                        task_id = params['task_id']
                    except (TypeError, ValueError, KeyError):
                        task_id = filedef.file_slug
                    program_slug = filedef.program_slug
                    try:
                        # loop = asyncio.new_event_loop()
                        task_uuid = str(uuid.uuid4())
                        if not filedef.params:
                            params = {}
                        else:
                            params = filedef.params
                        args = {**args, **params}
                        if email:
                            existing = args.get('variables') or {}
                            args['variables'] = {**existing, 'email': email}
                        status, action, result = await launch_task(
                            program_slug=program_slug,
                            # task_id=task_id,
                            loop=self._loop,
                            task_uuid=task_uuid,
                            queued=queued,
                            no_worker=no_worker,
                            **args
                        )
                        result = {
                            "task": f"{program_slug}.{task_id}",
                            "task_execution": task_uuid,
                            "result": f"{status!s}"
                        }
                        if action == 'Executed':
                            state = 200
                        else:
                            state = 202
                        response = {
                            "state": state,
                            "message": f"Task associated with file {f.filename} was {action}",
                            **result
                        }
                    except OSError as err:
                        logging.exception(f'Connection Aborted: {err!s}')
                        return self.error(
                            reason=f'Connection Aborted: {err!s}'
                        )
                    except FileNotFound as err:
                        headers = {
                            'X-STATUS': 'Task Failed',
                            'X-MESSAGE': 'File Not Found'
                        }
                        response = {
                            "message": f"File Not Found {f.filename}",
                            "task": f"{program_slug}.{task_id}",
                            "state": 404,
                            "exception": str(err),
                            **result
                        }
                        return self.error(
                            response=response
                        )
                    except (NotSupported, TaskNotFound, TaskFailed, FileError) as err:
                        headers = {
                            'X-STATUS': 'Task Failed',
                            'X-MESSAGE': 'Task Execution Failed'
                        }
                        response = {
                            "message": f"Task error on associated file {f.filename}",
                            "task": f"{program_slug}.{task_id}",
                            "state": 406,
                            "exception": str(err),
                            **result
                        }
                        return self.error(
                            response=response
                        )
                    except Exception as err:
                        return self.critical(
                            exception=err, stacktrace=traceback.format_exc()
                        )
                try:
                    show_preview = attributes['show_preview']
                except KeyError:
                    show_preview = True
                try:
                    num_preview = attributes['num_preview']
                except KeyError:
                    num_preview = 10
                if show_preview is True:
                    dt = f.df.head(num_preview).fillna('')
                    preview = dt.to_dict(orient='records')
                else:
                    preview = None
                try:
                    data = {
                        "task": f"{program_slug}.{task_id}",
                        'NumRows': f.num_rows(),
                        'columns': f.columns,
                        'data': preview,
                        'status': f"Upload completed: {f.filename}",
                        **response
                    }
                    if response['state'] > 300:
                        return self.error(
                            response=data,
                            headers=headers,
                            exception=response['exception'],
                            status=response['state']
                        )
                    else:
                        return self.json_response(
                            response=data,
                            headers=headers,
                            status=response['state']
                        )
                except OSError as err:
                    logging.exception(f'Connection Aborted: {err!s}')
                finally:
                    del filedef
