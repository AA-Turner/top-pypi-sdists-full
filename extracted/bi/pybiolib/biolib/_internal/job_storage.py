from biolib import utils


def upload_module_input(job_uuid: str, job_auth_token: str, module_input_serialized: bytes) -> None:
    headers = {'Job-Auth-Token': job_auth_token}
    multipart_uploader = utils.MultiPartUploader(
        start_multipart_upload_request=dict(
            requires_biolib_auth=False,
            path=f'/jobs/{job_uuid}/storage/input/start_upload/',
            headers=headers,
        ),
        get_presigned_upload_url_request=dict(
            requires_biolib_auth=False,
            path=f'/jobs/{job_uuid}/storage/input/presigned_upload_url/',
            headers=headers,
        ),
        complete_upload_request=dict(
            requires_biolib_auth=False,
            path=f'/jobs/{job_uuid}/storage/input/complete_upload/',
            headers=headers,
        ),
    )
    multipart_uploader.upload(
        payload_iterator=utils.get_chunk_iterator_from_bytes(module_input_serialized),
        payload_size_in_bytes=len(module_input_serialized),
    )
