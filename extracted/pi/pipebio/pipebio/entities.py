"""Operations on PipeBio entities (documents and folders).

An *entity* is any node in the PipeBio document tree: folders, sequence
documents, alignments, reports, and so on. This module wraps the ``entities``
API endpoints for creating, fetching, deleting, and merging assay data into
entities, and is exposed as :attr:`PipebioClient.entities`.
"""

import os.path
import re
from multiprocessing.pool import ThreadPool
from pathlib import Path
from typing import Any, Dict, List

import pandas as pd
import requests
from requests_toolbelt.sessions import BaseUrlSession

from pipebio.attachments import Attachments
from pipebio.column import Column
from pipebio.jobs import Jobs
from pipebio.models.entity_types import EntityTypes
from pipebio.models.job_status import JobStatus
from pipebio.models.job_type import JobType
from pipebio.models.table_column_type import TableColumnType
from pipebio.models.upload_summary import UploadSummary
from pipebio.util import Util


class Entities:
    """Wraps the ``entities`` API endpoints.

    Obtain an instance via :attr:`PipebioClient.entities` rather than
    constructing it directly.
    """

    _url: str
    _session: BaseUrlSession
    _user: Any
    attachments_service: Attachments
    jobs_service: Jobs

    def __init__(self, session: BaseUrlSession, user: Any) -> None:
        """Initialise the service.

        Args:
            session: An authenticated base-url session from the client.
            user: The authenticated user object, used to resolve the owning
                organization for operations that create jobs (e.g.
                :func:`merge`).
        """
        self._url = 'entities'
        self._session = session
        self._user = user
        self.attachments_service = Attachments(session)
        self.jobs_service = Jobs(session, user)

    def create_file(self,
                    project_id: str,
                    name: str,
                    parent_id: str = None,
                    entity_type: EntityTypes = EntityTypes.SEQUENCE_DOCUMENT,
                    visible: bool = False) -> dict:
        """Create a new entity (document or folder).

        Args:
            project_id: Id of the project (shareable) to create the entity in.
            name: Display name for the new entity.
            parent_id: Optional id of the parent folder.
            entity_type: The :class:`~pipebio.models.entity_types.EntityTypes`
                to create. Defaults to a sequence document.
            visible: Whether the entity is immediately visible in the UI.

        Returns:
            The created entity object.

        .. API reference (generated - do not edit) ::

        **POST** ``/entities``

        Create

        Create a new entity, such as a folder or document

        API request body:
            * ``name`` -- Human-readable name for the new entity.
            * ``shareableId`` -- Id of the project (shareable) the entity belongs to.
            * ``type`` -- Type of entity to create, such as a folder or document.
            * ``visible`` (optional) -- Whether the entity is visible in the project tree.
            * ``parentId`` (optional) -- Id of the parent folder; omit to create at the project root.
            * ``sequenceDocumentKind`` (optional) -- For sequence documents, the kind of sequences they hold.
            * ``sequenceCount`` (optional) -- Number of sequences contained in the document.
            * ``attributes`` (optional) -- Arbitrary key/value metadata to attach to the entity.

        .. end API reference ::
        """
        print(f'create_file for parent_id:{str(parent_id)} name:{str(name)}')

        payload = {
            'name': name,
            'type': entity_type.value,
            'visible': visible,
            'shareableId': project_id,
        }

        if parent_id is not None:
            payload['parentId'] = str(parent_id)

        response = self._session.post(
            self._url,
            json=payload,
        )
        print(f'create_file response: {str(response.status_code)}')
        Util.raise_detailed_error(response)
        return response.json()

    def create_folder(self, project_id: str, name: str, parent_id: str = None, visible: bool = False) -> dict:
        """Create a new folder entity.

        Args:
            project_id: Id of the project (shareable) to create the folder in.
            name: Display name for the folder.
            parent_id: Optional id of the parent folder.
            visible: Whether the folder is immediately visible in the UI.

        Returns:
            The created folder entity object.
        """
        return self.create_file(
            project_id=project_id,
            name=name,
            parent_id=parent_id,
            entity_type=EntityTypes.FOLDER,
            visible=visible
        )

    def mark_file_visible(self, entity_summary: UploadSummary) -> dict:
        """Make a previously hidden entity visible in the UI.

        Args:
            entity_summary: Summary of the entity to update.

        Returns:
            The updated entity object.

        .. API reference (generated - do not edit) ::

        **PATCH** ``/entities/{id}``

        Update

        Update entity properties. Only properties that are included in the request body will be affected; the rest will be unchanged.

        API parameters:
            * ``id`` (path) -- Id of the entity to update.
            * ``allowDeleted`` (query) -- If true, also update the entity when it has been soft-deleted.

        API request body:
            * ``name`` (optional) -- New name for the entity.
            * ``visible`` (optional) -- Whether the entity is visible in the project tree.
            * ``sequenceCount`` (optional) -- Number of sequences contained in the document.
            * ``sequenceDocumentKind`` -- For sequence documents, the kind of sequences they hold.
            * ``type`` (optional) -- Type of the entity, such as a folder or document.
            * ``attributes`` (optional) -- Arbitrary key/value metadata to attach to the entity.

        .. end API reference ::
        """
        print('marking visible:', entity_summary)
        response = self._session.patch(
            f'{self._url}/{entity_summary.id}',
            json=entity_summary.to_json(),
        )
        print('mark_file_visible response:' + str(response.status_code))
        print('mark_file_visible text    :' + str(response.text))
        Util.raise_detailed_error(response)
        return response.json()

    def get(self, entity_id: str, allow_deleted: bool = False) -> dict:
        """Fetch a single entity by id.

        Args:
            entity_id: Id of the entity to fetch.
            allow_deleted: Whether to return the entity when it has been
                soft-deleted.

        Returns:
            The entity object.

        .. API reference (generated - do not edit) ::

        **GET** ``/entities/{id}``

        Get one

        Get a specific entity such as a folder or document.

        API parameters:
            * ``id`` (path) -- Id of the entity (document or folder) to fetch.
            * ``allowDeleted`` (query) -- If true, also return the entity when it has been soft-deleted.
            * ``includeMigrationDetails`` (query) -- If true, include AWS migration metadata in the response.

        .. end API reference ::
        """
        params = {'allowDeleted': 'true'} if allow_deleted else None
        response = self._session.get(f'{self._url}/{entity_id}', params=params)
        Util.raise_detailed_error(response)
        return response.json()

    def get_all(self, entity_ids: List[str]) -> List[dict]:
        """Fetch multiple entities in parallel.

        Args:
            entity_ids: Ids of the entities to fetch.

        Returns:
            The list of entity objects (order is not guaranteed).
        """
        results = list(ThreadPool(8).imap_unordered(lambda entity_id: self.get(entity_id), entity_ids))
        for result in results:
            print(result)
        return results

    def delete(self, entity_ids: list) -> None:
        """Delete one or more entities.

        Args:
            entity_ids: Ids of the entities to delete.

        .. API reference (generated - do not edit) ::

        **DELETE** ``/entities``

        Delete

        Delete one or more entities

        API request body:
            * ``ids`` -- Ids of the entities to delete.

        .. end API reference ::
        """
        headers = {"Content-Type": "application/json"}
        data = {"ids": entity_ids}
        response = self._session.delete(f'{self._url}', json=data, headers=headers)
        Util.raise_detailed_error(response)

    @staticmethod
    def merge_fields(schema_a: List[Column], schema_b: List[Column]) -> List[Column]:
        result = []
        result.extend(schema_a)

        for column in schema_b:
            found = next((col for col in result if col.name == column.name), None)
            if found is None:
                result.append(column)

        return result

    def get_fields_for_all_entities(self, entity_ids: List[str]) -> List[Column]:
        schema = []
        for entity_id in entity_ids:
            new_schema = self.get_fields(entity_id)
            schema = Entities.merge_fields(schema, new_schema)
        return schema

    def get_fields(self, entity_id: str, ignore_id: bool = False) -> List[Column]:
        """Return the column fields (schema) for a document.

        Args:
            entity_id: Id of the document to inspect.
            ignore_id: If ``True``, omit the ``id`` field from the result.

        Returns:
            The list of :class:`~pipebio.column.Column` definitions. Raises if
            the entity has no fields (e.g. it is a folder).

        .. API reference (generated - do not edit) ::

        **GET** ``/entities/{id}/fields``

        List entity fields

        If this entity is a document containing sequences, list all fields (columns). Otherwise (e.g. if the entity is a folder) will return an error.

        API parameters:
            * ``id`` (path) -- Id of the document whose fields (columns) to list.
            * ``allowDeleted`` (query) -- If true, also operate on the document when it has been soft-deleted.
            * ``getMinMax`` (query) -- If true, include per-column minimum and maximum values.
            * ``includeSortCols`` (query) -- If true, include hidden helper columns used for sorting.

        .. end API reference ::
        """
        response = self._session.get(f'{self._url}/{entity_id}/fields')
        Util.raise_detailed_error(response)
        columns = []
        for field in response.json():

            if ignore_id and field == 'id':
                continue
            else:
                # Not all columns have field so we need to check it's set.
                description = field['description'] if 'description' in field else None
                columns.append(Column(field['name'], TableColumnType[field['type']], description))

        return columns

    def download_original_file(self, entity_id: str, destination_filename: str) -> str:
        """Download the original uploaded file for a document.

        Two requests are made: one to obtain a signed URL
        (``GET /api/v2/entities/:id/original``) and one to download the file
        from that URL.

        Args:
            entity_id: Id of the document whose original file to download.
            destination_filename: Local path to write the downloaded file to.

        Returns:
            The ``destination_filename`` that was written.

        .. API reference (generated - do not edit) ::

        **GET** ``/entities/{id}/original``

        Original file

        Generate signed url to download original file entity was created from

        API parameters:
            * ``id`` (path) -- Id of the entity whose original uploaded file to download.
            * ``allowDeleted`` (query) -- If true, also operate on the entity when it has been soft-deleted.

        .. end API reference ::
        """
        # First request a signed url from PipeBio.
        signed_url_response = self._session.get(f'{self._url}/{entity_id}/original')

        # Did the signed-url request work ok?
        Util.raise_detailed_error(signed_url_response)

        # Parse the results to get the signed url.
        download_url = signed_url_response.json()['url']

        # Download the original file.
        download_response = requests.get(download_url)

        # Did the download request work ok?
        Util.raise_detailed_error(download_response)

        # Write the result to disk in chunks.
        with open(destination_filename, 'wb') as f:
            for chunk in download_response.iter_content(chunk_size=8192):
                f.write(chunk)

        return destination_filename

    @staticmethod
    def convert_pandas_type(pandas_type: str) -> TableColumnType:
        if pandas_type == 'int64':
            return TableColumnType.INT64
        elif pandas_type == 'float64':
            return TableColumnType.BIGNUMERIC
        else:
            return TableColumnType.STRING

    def get_file_handle(self, absolute_file_path: str) -> pd.DataFrame:
        """Read a tabular file into a pandas DataFrame.

        Attempts to read the file as Excel first, then falls back to
        comma-separated and finally tab-separated parsing.

        Args:
            absolute_file_path: Path to the local tabular file.

        Returns:
            The parsed :class:`pandas.DataFrame`.
        """
        try:
            # Try as excel, fallback to csv/tsv.
            read_file = pd.read_excel(absolute_file_path)
            return read_file
        except Exception:
            # try as csv
            read_file = pd.read_table(absolute_file_path, sep=",")
            columns_length = len(read_file.columns.to_list())
            if columns_length > 1:
                return read_file
            else:
                read_file = pd.read_table(absolute_file_path, sep="\t")
                return read_file

    def merge(self,
              entity_id: str,
              assay_absolute_file_path: str,
              assay_column: str,
              entity_column: str,
              append_unmatched_rows: bool = False,
              timeout_seconds: int = 60 * 60,
              ) -> Dict[str, Any]:
        """Merge tabular assay data into a sequence document.

        Reads a local csv/tsv/excel assay file and left-joins its rows onto the
        sequence document: every assay column becomes a new column on the
        document, and each document row is filled from the assay row whose
        ``assay_column`` value equals that row's ``entity_column`` value. This is
        equivalent to `add assay data
        <https://docs.pipebio.com/docs/assay-and-functional-data#add-assay-data>`_
        in the web app.

        The merge is performed in three steps:

        1. The assay file is converted to TSV and uploaded directly to storage
           via a presigned URL (no job is created for the upload).
        2. A ``MergeAssayDataJob`` referencing the uploaded file is created.
        3. This call blocks, polling until that job completes.

        Example:
            Merge binding scores keyed by clone name into a document whose
            ``name`` column holds the same clone names::

                client.entities.merge(
                    entity_id="12345",
                    assay_absolute_file_path="/data/binding_scores.csv",
                    assay_column="clone_id",   # header in binding_scores.csv
                    entity_column="name",      # column on document 12345
                )

        Args:
            entity_id: Id of the sequence document to merge the assay data into.
            assay_absolute_file_path: Absolute path to the tabular assay file on
                local disk (``.csv``, ``.tsv`` or ``.xlsx``); its first row must
                be a header.
            assay_column: Name of the join-key column *in the assay file* (a
                header from ``assay_absolute_file_path``).
            entity_column: Name of the join-key column *on the document* (e.g.
                ``"name"``) whose values are matched against ``assay_column``.
            append_unmatched_rows: If ``True``, assay rows that match no document
                row (e.g. controls) are appended to the document as new rows;
                if ``False`` they are discarded.
            timeout_seconds: Maximum seconds to wait for the merge job to finish
                before raising. Defaults to one hour.

        Returns:
            The completed ``MergeAssayDataJob`` as a ``dict`` (the polled job
            object, including its final ``status``).

        Raises:
            ValueError: If the assay file does not exist, or ``assay_column`` is
                not a header in the assay file.
            Exception: If the merge job fails or the timeout elapses.
        """
        if not os.path.isfile(assay_absolute_file_path):
            raise ValueError(f'File "{assay_absolute_file_path}" does not exist')

        path = Path(assay_absolute_file_path)
        stem = path.stem
        suffix = path.suffix[1:]
        # filtered_name = f'{stem}{suffix}'
        filtered_name = re.sub('[^a-zA-Z0-9]', '', f'{stem}{suffix}')
        # Mimicking the current front end functionality, if there are already columns with filtered name, append 2
        # to the end e.g. AdimabAssayxlsx becomes AdimabAssayxlsx2 and AdimabAssayxlsx2 becomes AdimabAssayxlsx22.
        columns = self.get_fields(entity_id)
        existing_assay_columns = list(filter(lambda c: c.name.startswith(filtered_name), columns))
        if len(existing_assay_columns) > 0:
            # Get the longest prefix
            prefixes = list(map(lambda c: c.name.split('_')[0], existing_assay_columns))
            longest_prefix = max(prefixes, key=len)
            filtered_name = f'{longest_prefix}2'

        # Data must be merged as tsv, so use pandas here to transform it.
        read_file = self.get_file_handle(assay_absolute_file_path)
        tsv_content = read_file.to_csv(index=False, header=True, sep='\t')

        # The MergeAssayDataJob matches the assay join column against the schema
        # field names below, so resolve it to the same safe name (not the raw
        # header) as we build the schema.
        assay_table_field = None
        fields_dict = read_file.dtypes.to_dict()
        schema = []
        for key in list(fields_dict.keys()):
            _type = Entities.convert_pandas_type(str(fields_dict[key]))
            safe_name = re.sub('[^a-zA-Z0-9]', '', key)
            if safe_name == 'id':
                # "id" is reserved, so an assay "id" column is stored as
                # "..._AssayImport_1". Capturing assay_table_field from the same
                # resolved name below means joining on this column just works,
                # which is why the old explicit assay_column remap is gone.
                safe_name = f'{filtered_name}_AssayImport_1'
                if len(safe_name) > 128:
                    safe_name = f'{safe_name[:125]}...'
            else:
                safe_name = f'{filtered_name}_{safe_name}'
            if key == assay_column:
                assay_table_field = safe_name
            schema.append({'name': safe_name, 'type': _type.value, 'description': ''})

        if assay_table_field is None:
            raise ValueError(f'Assay column "{assay_column}" not found in "{assay_absolute_file_path}"')

        # Upload the assay file directly to storage via a presigned URL.
        s3_key = self._upload_assay_file(tsv_content)

        # Create the merge job against the uploaded file and wait for it to
        # finish, reusing the shared Jobs service for creation and polling.
        entity = self.get(entity_id)
        job_id = self.jobs_service.create(
            shareable_id=entity['ownerId'],
            job_type=JobType.MergeAssayDataJob,
            name='Merge assay data',
            input_entity_ids=[entity_id],
            params={
                'entityId': entity_id,
                'targetTableField': entity_column,
                'assayTableField': assay_table_field,
                'schema': schema,
                'mappings': [],
                'appendUnmatchedRows': append_unmatched_rows,
                's3Key': s3_key,
            },
        )

        job = self.jobs_service.poll_job(job_id, timeout_seconds)
        if job['status'] == JobStatus.FAILED.value:
            messages = job.get('messages') or []
            detail = '; '.join(messages) if messages else 'no error detail provided'
            raise Exception(f'Merge job {job_id} failed: {detail}')
        return job

    def _upload_assay_file(self, tsv_content: str) -> str:
        """Upload assay TSV content via a presigned URL and return its S3 key.

        Requests a presigned URL (``POST /uploads/signed-url``) and PUTs the
        bytes directly to it. This does not create a job.

        Args:
            tsv_content: The tab-separated assay data to upload.

        Returns:
            The S3 key the data was uploaded under.

        .. API reference (generated - do not edit) ::

        **POST** ``/uploads/signed-url``

        Create upload URL

        Generate a presigned URL for direct-to-S3 upload. Does not create a job.

        API request body:
            * ``contentType`` (optional) -- MIME type of the file being uploaded.

        .. end API reference ::
        """
        content_type = 'text/tab-separated-values'
        signed_url_response = self._session.post(
            'uploads/signed-url', json={'contentType': content_type}
        )
        Util.raise_detailed_error(signed_url_response)

        signed = signed_url_response.json()

        # The URL and headers are presigned by the server and must be sent
        # unmodified, so PUT directly rather than via the authenticated session.
        upload_response = requests.put(
            signed['url'],
            data=tsv_content.encode('utf-8'),
            headers=signed['headers'],
            timeout=60 * 60,
        )
        Util.raise_detailed_error(upload_response)

        return signed['key']
