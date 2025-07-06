from cnvrgv2.modules.base.dynamic_attributes import DynamicAttributes


class DatasourceOperationsInterface(DynamicAttributes):
    def list_objects(self, page_size: int):
        raise NotImplementedError

    def download_file(self, file_path: str, destination_path: str, calc_destination_path: bool) -> None:
        raise NotImplementedError
