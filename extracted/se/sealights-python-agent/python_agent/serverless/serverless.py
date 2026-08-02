import logging
import os
import shutil
from typing import List, Dict
from urllib.parse import urlparse

from python_agent.build_scanner.app import scan_files
from python_agent.common.config_data import ConfigData
from python_agent.utils import disableable
from .lambda_config import LambdaConfig

log = logging.getLogger(__name__)

sealights_layer_path = os.path.join(os.path.dirname(__file__), "sealights_layer")
sealights_layer_zip_filename = "sealights_layer.zip"


class Serverless(object):
    def __init__(
        self,
        config_data: ConfigData,
        collectorurl: str,
        exportlayerpath: str,
        slconfigpaths: list,
    ):
        self.collector_url = collectorurl
        self.config_data = config_data
        self.export_layer_path = exportlayerpath
        self.sl_config_paths = slconfigpaths
        self.build_digest: Dict[str, Dict[str, List[int]]] = {}

    @disableable()
    def execute(self):
        log.info("Starting Sealights lambda configuration setup")
        try:
            self.validate()
        except Exception as e:
            log.exception(str(e))
            return
        if self.export_layer_path is not None:
            self.export_sealights_layer_code()
        else:
            log.info("Skipping Sealights Layer export")
        try:
            self.populate_build_digest()
        except Exception as e:
            log.exception(str(e))
            return
        try:
            self.save_sl_config()
        except Exception as e:
            log.exception(str(e))

        log.info("Sealights lambda configuration setup completed")

    def populate_build_digest(self):
        excluded = self.config_data.additionalParams.get("exclude")
        included = self.config_data.additionalParams.get("include")
        workspacepath = self.config_data.additionalParams.get("workspacepath")
        scanned_files = scan_files(workspacepath, included, excluded)
        if not scanned_files or len(scanned_files) == 0:
            return
        for full_path, file_data in scanned_files.items():
            file_path = full_path.replace("\\", "/")
            methods_dict: Dict[str, List[int]] = {}
            for method in file_data.methods:
                methods_dict[method.uniqueId] = method.lines
            if methods_dict:
                self.build_digest[file_path] = methods_dict

    def validate(self):
        if self.collector_url is not None:
            try:
                parsed_collector_url = urlparse(self.collector_url)
                if not parsed_collector_url.scheme or not parsed_collector_url.netloc:
                    raise Exception("Sealights Collector URL is invalid")
            except Exception as e:
                raise Exception(f"Sealgiths Collector URL is invalid, {e}")

    def export_sealights_layer_code(self):
        log.info(
            f"Exporting Sealights lambda layer to {os.path.join(self.export_layer_path, 'sealights_layer')}"
        )
        try:
            if os.path.exists(os.path.join(self.export_layer_path, "sealights_layer")):
                shutil.rmtree(os.path.join(self.export_layer_path, "sealights_layer"))

            os.makedirs(self.export_layer_path, exist_ok=True)
            shutil.copytree(
                sealights_layer_path,
                os.path.join(self.export_layer_path, "sealights_layer"),
            )

            return True  # Copy operation successful
        except Exception as e:
            raise Exception(f"Failed to export Sealights Layer code, {e}")

    def filter_build_digest(
        self, build_digest: Dict[str, Dict[str, List[int]]], full_path
    ) -> Dict[str, Dict[str, List[int]]]:
        filtered_build_digest = {}
        for file_path, methods in build_digest.items():
            if file_path.startswith(full_path):
                trimmed_file_path = file_path[len(full_path) :].lstrip("/")
                filtered_build_digest[trimmed_file_path] = methods
        return filtered_build_digest

    def save_sl_config(self):
        sl_config = LambdaConfig(
            self.config_data.appName,
            self.config_data.buildName,
            self.config_data.branchName,
            self.config_data.buildSessionId,
            self.collector_url,
            self.build_digest,
            self.config_data.token,
        )

        for sl_config_path in self.sl_config_paths:
            sl_config.buildDigest = self.filter_build_digest(
                self.build_digest, os.path.abspath(sl_config_path).replace("\\", "/")
            )
            filepath = os.path.join(sl_config_path, "sl_lambda_config.json")
            try:
                sl_config.save_to_file(filepath)
                log.info(f"Saving Sealights config file to {sl_config_path}")
            except Exception as e:
                log.exception(
                    f"Failed to save Sealights config file to {sl_config_path}, {e}"
                )
                continue
