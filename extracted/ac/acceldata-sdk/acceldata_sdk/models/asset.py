from dataclasses import asdict

from acceldata_sdk.errors import TorchSdkException
from acceldata_sdk.models.profile import ProfilingType, JobType, Profile, StartProfilingRequest
from acceldata_sdk.models.assetType import AssetType
from acceldata_sdk.models.create_asset import RelationType, CreateAssetRelation, AssetMetadata
from acceldata_sdk.models.datasource import DataSource, SourceType
from acceldata_sdk.models.tags import AssetLabel, CustomAssetMetadata
from acceldata_sdk.models.common_types import ExecutionType


from enum import Enum, auto
from typing import List
import logging

logger = logging.getLogger('asset')
logger.setLevel(logging.INFO)

class Metadata:

    def __init__(self, assetId, createdAt=None, updatedAt=None, currentSnapshot=None, id=None, items=None, metaDataHash=None, snapshots=None, *args, **kwargs):
        self.assetId = assetId
        self.createdAt = createdAt
        self.updatedAt = updatedAt
        self.currentSnapshot = currentSnapshot
        self.id = id
        self.metaDataHash = metaDataHash
        if isinstance(items, list):
            items_list = list(items)
            asset_metadata = []
            for i in items_list:
                asset_mt = AssetMetadata(**i)
                asset_metadata.append(asset_mt)
            self.items = asset_metadata
        else:
            self.items = items
        if isinstance(snapshots, list):
            self.snapshots = list(snapshots)
        else:
            self.snapshots = snapshots

    def __eq__(self, other):
        return self.id == other.id

    def __repr__(self):
        return f"Metadata({self.__dict__})"


class CustomAssetType(Enum):
    SQL_VIEW = auto()
    SQL_VIEW_COLUMN = auto()
    VISUAL_VIEW = auto()
    VISUAL_VIEW_COLUMN = auto()


class Asset:
    def __init__(self,
                 alias=None,
                 assembly=None,
                 assetType: AssetType = None,
                 createdAt=None,
                 currentSnapshot=None,
                 description=None,
                 id=None,
                 isCustom=None,
                 isDeleted=None,
                 name=None,
                 parentId=None,
                 snapshots=None,
                 sourceType: SourceType = None,
                 uid=None,
                 updatedAt=None,
                 client=None,
                 customAssetType: CustomAssetType = None,
                 assemblyId=None,
                 isSegmented=None,
                 *args, **kwargs
                 ):
        """
            Description:
                Asset class
        :param alias: alias of the asset
        :param assembly: (Datasource) data source details
        :param assetType: type of the asset
        :param createdAt: creation time of the asset
        :param currentSnapshot: current version of the asset
        :param description: desc of the asset
        :param id: asset id
        :param isCustom: is custom asset or not
        :param isDeleted: is deleted or not in current version of the datasource
        :param name: name of the asset
        :param parentId: parent id of the asset
        :param snapshots: version list
        :param sourceType: source type of the asset's datasource
        :param uid: uid of the asset
        :param updatedAt: updated time of the asset
        """
        self.alias = alias
        self.createdAt = createdAt
        self.currentSnapshot = currentSnapshot
        self.description = description
        self.id = id
        self.isCustom = isCustom
        self.isDeleted = isDeleted
        self.assemblyId = assemblyId
        self.isSegmented = isSegmented
        self.name = name
        self.parentId = parentId
        self.snapshots = snapshots
        self.uid = uid
        self.updatedAt = updatedAt
        if isinstance(assembly, dict):
            self.datasource = DataSource(**assembly)
        else:
            self.datasource = assembly
        if isinstance(assetType, dict):
            self.assetType = AssetType(**assetType)
        else:
            self.assetType = assetType
        if isinstance(sourceType, dict):
            self.sourceType = SourceType(**sourceType)
        else:
            self.sourceType = sourceType
        if isinstance(customAssetType, dict):
            self.customAssetType = CustomAssetType(**customAssetType)
        else:
            self.customAssetType = customAssetType
        self.client = client

    def __repr__(self):
        return f"Asset({self.__dict__})"

    def get_labels(self):
        return self.client.get_asset_labels(self.id)

    def add_labels(self, labels: List[AssetLabel]):
        lbls = []
        for label in labels:
            label_dict = {
                'key': label.key,
                'value': label.value
            }
            lbls.append(label_dict)
        payload = {
            'labels': lbls
        }
        return self.client.add_asset_labels(self.id, payload)

    def get_tags(self):
        return self.client.get_asset_tags(self.id)

    def add_tag(self, tag):
        payload = {
            "name": tag
        }
        return self.client.add_asset_tag(self.id, payload)

    def get_metadata(self):
        return self.client.get_asset_metadata(self.id)

    def add_custom_metadata(self, custom_metadata: List[CustomAssetMetadata]):
        """
        Description:
            Add custom metadata
        :param custom_metadata: list of CustomAssetMetadata Object
        :return:
        """
        metadts = dict()
        for custom_metadatum in custom_metadata:
            metadts[custom_metadatum.key] = custom_metadatum.value
        return self.client.add_custom_metadata(self.id, metadts)

    def start_profile(self, profiling_type: ProfilingType = None,
                      start_profiling_request: StartProfilingRequest = None) -> Profile:
        payload = {}
        logger.info(
            f"Invoked start_profile method of the Asset\n"
            f"ProfilingType: {profiling_type}\n"
            f"StartProfilingRequest: {start_profiling_request.to_dict() if start_profiling_request else 'None'}"
        )

        if start_profiling_request is None:
            logger.info(
                "StartProfilingRequest is None , executing profile based on profiling type")
            payload = {
                'data': {
                    'profilingType': profiling_type.value
                }
            }

        if start_profiling_request is not None:
            logger.info(f"Marker config: {start_profiling_request.markerConfig}")
            if start_profiling_request.profilingType == ExecutionType.SELECTIVE and not start_profiling_request.markerConfig:
                raise TorchSdkException(
                    f'markerConfig is a mandatory parameter for execution type {ExecutionType.SELECTIVE}')
            else:
                logger.info("Converting start_profiling_request to dictionary")
                payload = start_profiling_request.to_dict()
                logger.info(f"StartProfilingRequest to dictionary: {payload}")
        logger.info(f"Executing Profiling with the following payload: {payload}")
        return self.client.profile_asset(self.id, payload)

    def get_latest_profile_status(self):
        return self.client.get_latest_profile_status(self.id)

    def sample_data(self):
        return self.client.sample_data(self.id)
