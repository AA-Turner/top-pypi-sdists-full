from __future__ import absolute_import

import os
import uuid
from uuid import UUID

import requests

from tmo.api.base_api import BaseApi

SUPPORTED_BYOM_FORMATS = ["PMML", "ONNX", "H2O", "H2O_DAI", "DATAROBOT", "DATAIKU"]


class TrainedModelArtefactsApi(BaseApi):

    path = "/api/trainedModels/{}/artefacts"
    type = "TRAINED_MODEL_ARTEFACTS"

    def _get_header_params(self):
        return self._get_standard_header_params()

    def list_artefacts(self, trained_model_id: UUID):
        """
        returns all trained models

        Parameters:
           trained_model_id (uuid): Trained Model Id

        Returns:
            (list): all trained model artefacts
        """

        return self.tmo_client.get_request(
            path=(f"{self.path}/listObjects").format(trained_model_id),  # noqa
            header_params=self._get_header_params(),
            query_params={},
        )["objects"]

    def get_signed_download_url(self, trained_model_id: UUID, artefact: str):
        """
        returns a signed url for the artefact

        Parameters:
           trained_model_id (uuid): Trained Model Id
           artefact (str): The artefact to generate the signed url for

        Returns:
            (str): the signed url
        """
        query_params = self.generate_params(["objectKey"], [artefact])

        response = self.tmo_client.get_request(
            path=(f"{self.path}/signedDownloadUrl").format(trained_model_id),  # noqa
            header_params=self._get_header_params(),
            query_params=query_params,
        )

        return response["endpoint"], response.get("headers", "")

    def get_signed_upload_url(self, trained_model_id: UUID, artefact: str):
        """
        returns a signed url for the artefact

        Parameters:
           trained_model_id (uuid): Trained Model Id
           artefact (str): The artefact to generate the signed url for

        Returns:
            (str): the signed url
        """
        query_params = self.generate_params(["objectKey"], [artefact])

        response = self.tmo_client.get_request(
            path=(f"{self.path}/signedUploadUrl").format(trained_model_id),  # noqa
            header_params=self._get_header_params(),
            query_params=query_params,
        )

        return response["endpoint"], response.get("headers", "")

    def download_artefacts(self, trained_model_id: UUID, path: str = "."):
        """
        downloads all artefacts for the given trained model

        Parameters:
           trained_model_id (uuid): Trained Model Id
           path (str): the path to download the artefacts to (default cwd)

        Returns:
            None
        """

        for artefact in self.list_artefacts(trained_model_id):
            signed_url, headers = self.get_signed_download_url(
                trained_model_id, artefact
            )
            response = requests.get(
                signed_url,
                headers=headers,  # noqa
                verify=self.tmo_client.session.verify,
            )

            output_file = "{}/{}".format(path, artefact)
            if not os.path.exists(os.path.dirname(output_file)):
                os.makedirs(os.path.dirname(output_file))

            with open(output_file, "wb") as f:
                for chunk in response.iter_content(chunk_size=1024 * 1024):
                    f.write(chunk)

    def upload_artefacts(
        self, import_id: UUID, artefacts: list = None, artefacts_folder: str = None
    ):
        """
        uploads artefacts for the given trained model

        Parameters:
           import_id (uuid): Trained Model Id
           artefacts (list): The artefact paths to upload (must specify this or artefacts_folder)
           artefacts_folder (str): The artefact folder (must specify this or artefacts list)
        Returns:
            None
        """

        if artefacts is None and artefacts_folder is None:
            raise ValueError(
                "Either artefacts or artefacts_folder argument must be specified"
            )

        if artefacts is not None:
            for artefact in artefacts:
                object_key = os.path.basename(artefact)
                self.__upload_artefact(artefact, object_key, import_id)

        else:
            for root, d, files in os.walk(artefacts_folder):
                for file in files:
                    object_key = os.path.relpath(
                        os.path.join(root, file), artefacts_folder
                    )
                    self.__upload_artefact(
                        os.path.join(root, file), object_key, import_id
                    )

    def upload_byom_model(
        self, byom_format: str, file_path: str, import_id: str = None
    ):
        """Simplified method to upload just a single file as BYOM model version.
        File is renamed during upload, so any local filename could be used.

        Args:
            byom_format (str): One of supported formats, e.g. PMML, ONNX, H2O
            file_path (str): local file path to a model artefact
            import_id (str, optional): by default import_id is randomly generated. If required, specific import_id could be provided.

        Raises:
            ValueError: if format string is not one of supported formats

        Returns:
            str: import_id that could be used by import_byom method
        """
        if byom_format not in SUPPORTED_BYOM_FORMATS:
            raise ValueError(
                f"The format {byom_format} is not supported for simplified BYOM import,"
                " use `import_file` instead"
            )

        if not import_id:
            import_id = str(uuid.uuid4())

        self.__upload_artefact(file_path, f"model.{byom_format.lower()}", import_id)
        return import_id

    def __upload_artefact(self, artefact, object_key, import_id):
        signed_url, headers = self.get_signed_upload_url(import_id, object_key)
        # don't use tmo_client.session here as we don't want to send auth info.
        upload_resp = requests.put(
            signed_url,
            headers=headers,  # noqa
            data=open(artefact, "rb"),
            verify=self.tmo_client.session.verify,
        )
        upload_resp.raise_for_status()
