import os
from pathlib import Path
from typing import Any, Dict, Optional

from qwak.exceptions import QwakException
from qwak.feature_store._common import packaging
from qwak.feature_store._common.source_code_spec import (
    JfrogArtifact,
    SourceCodeSpec,
    ZipArtifact,
)


class SourceCodeSpecFactory:
    @staticmethod
    def _upload_source_code_dir(
        main_entity_path: Path, url: str, extra_headers: Dict[str, Any]
    ):
        zip_location: Optional[Path] = None
        try:
            zip_location = packaging.zip_source_code_dir(base_path=main_entity_path)
            with open(zip_location, "rb") as zip_file:
                packaging.put_files_content(
                    url=url,
                    content=zip_file.read(),
                    content_type="application/octet-stream",
                    extra_headers=extra_headers,
                )
        except Exception as e:
            raise QwakException("Got an error while trying to upload file.") from e
        finally:
            if zip_location:
                os.remove(zip_location)

    @classmethod
    def get_zip_source_code_spec(
        cls,
        main_entity_path: Path,
        url: str,
        extra_headers: Optional[Dict[str, str]] = None,
    ) -> SourceCodeSpec:
        """
        Zips and upload the artifact,
        the main "entity" relative path is set as the main_entity_path
        """
        cls._upload_source_code_dir(
            main_entity_path=main_entity_path,
            url=url,
            extra_headers=extra_headers or {},
        )

        parent_base_path = (
            main_entity_path.parent if main_entity_path.is_file() else main_entity_path
        )

        if cls._is_artifactory_source_code(extra_headers):
            return cls._build_artifactory_source_code_spec(
                url=url,
                parent_base_path=parent_base_path,
                main_entity_path=main_entity_path,
            )
        else:
            return cls._build_qwak_source_code_spec(
                url=url,
                parent_base_path=parent_base_path,
                main_entity_path=main_entity_path,
            )

    @classmethod
    def _is_artifactory_source_code(
        cls, extra_headers: Optional[Dict[str, str]]
    ) -> bool:
        """
        Check if the source code is from Artifactory by checking the extra headers.
        """
        if not extra_headers:
            return False
        return True

    @classmethod
    def _build_artifactory_source_code_spec(
        cls, url: str, parent_base_path: Path, main_entity_path: Path
    ) -> SourceCodeSpec:
        return SourceCodeSpec(
            artifact=ZipArtifact(
                jfrog_artifact_path=JfrogArtifact(path=url),
                main_file=str(
                    Path(parent_base_path.name) / Path(main_entity_path.name)
                ),
            )
        )

    @classmethod
    def _build_qwak_source_code_spec(
        cls, url: str, parent_base_path: Path, main_entity_path: Path
    ) -> SourceCodeSpec:
        return SourceCodeSpec(
            artifact=ZipArtifact(
                qwak_artifact_path=url,
                main_file=str(
                    Path(parent_base_path.name) / Path(main_entity_path.name)
                ),
            )
        )
