from frogml_storage.models.frogml_entity_type_info import FrogMLEntityTypeInfo


# The following method affect e2e tests.
def build_download_success_log(
    entity_type_info: FrogMLEntityTypeInfo, entity_name: str, version: str
) -> str:
    return (
        f'{entity_type_info.entity_type.capitalize()}: "{entity_name}", version: "{version}"'
        f" has been downloaded successfully"
    )


# The following method affect e2e tests.
def build_upload_success_log(
    entity_type_info: FrogMLEntityTypeInfo, entity_name: str, version: str
) -> str:
    return (
        f'{entity_type_info.entity_type.capitalize()}: "{entity_name}", version: "{version}"'
        f" has been uploaded successfully"
    )
