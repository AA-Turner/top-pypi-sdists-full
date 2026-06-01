from picsellia.types.enums import DataType, DataUploadStatus


def add_data_mandatory_query_parameters(params: dict):
    # As we can now handle processing data and video, we can fetch all data
    params["upload_statuses"] = [
        DataUploadStatus.PENDING.value,
        DataUploadStatus.COMPUTING.value,
        DataUploadStatus.DONE.value,
        DataUploadStatus.ERROR.value,
    ]
    params["types"] = [DataType.IMAGE.value, DataType.VIDEO.value]
    return params
