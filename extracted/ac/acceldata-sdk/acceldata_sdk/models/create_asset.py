from dataclasses import dataclass
from enum import Enum
from typing import List


@dataclass
class AssetMetadata:
    """
    Description:
        Asset metadata item
        :param dataType: (String) data type of the value
        :param key: (String) key
        :param source: (String) source
        :param value: (String) value of metadata
    """
    dataType: str = None
    key: str = None
    source: str = None
    value: str = None


class CreateAsset:

    def __init__(self,
                 name: str,
                 assemblyId: int,
                 uid: str,
                 assetTypeId: int,
                 sourceTypeId: int,
                 isCustom: bool,
                 currentSnapshot: str,
                 snapshots: List[str] = [],
                 description: str = None,
                 parentId: int = None,
                 metadata: List[AssetMetadata] = [],
                 *args, **kwargs
                 ):
        """
        Description:
            Create asset class.
        :param name: name of the asset
        :param assemblyId: data source id in torch catalog
        :param uid: asset uid
        :param assetTypeId: asset type id
        :param sourceTypeId: source type id
        :param isCustom: (bool) is custom asset
        :param currentSnapshot: current version of the datasource
        :param snapshots: version of the datasource
        :param description: description of the asset
        :param parentId: parent id of the asset
        :param metadata: (List[AssetMetadata]) metadata list of the asset
        """
        self.name = name
        self.description = description
        self.assemblyId = assemblyId
        self.uid = uid
        self.assetTypeId = assetTypeId
        self.sourceTypeId = sourceTypeId
        self.isCustom = isCustom
        self.currentSnapshot = currentSnapshot
        self.snapshots = snapshots
        if parentId is not None:
            self.parentId = parentId
        # metadata of an asset
        self.metadata = metadata

    def __eq__(self, other):
        return self.uid == other.uid

    def __repr__(self):
        return f"Asset({self.uid!r})"


class RelationType(Enum):
    """
        Description:
            Relation type between assets
    """
    FOREIGN_KEY = 1
    DEPENDS_ON = 2
    SIBLING = 3


class CreateAssetRelation:

    def __init__(self, fromAssetUUID: str, assemblyId: int, toAssetUUID: str, relationType: RelationType, metaData=None,
                 currentSnapshot=None, snapshots=[], *args, **kwargs):
        """
            Description:
                Used to create relation between any 2 assets
        :param fromAssetUUID: source asset uid
        :param assemblyId:  datasource id
        :param toAssetUUID: sink asset uid
        :param relationType: (RelationType) relation type b/w assets
        :param metaData: (List[AssetMetadata]) metadata list
        :param currentSnapshot: current version of the relation
        :param snapshots: versions of the datasource
        """
        self.fromAssetUUID = fromAssetUUID
        self.assemblyId = assemblyId
        self.toAssetUUID = toAssetUUID
        self.relationType = relationType
        self.metaData = metaData
        self.currentSnapshot = currentSnapshot
        self.snapshots = snapshots

    def __eq__(self, other):
        return self.toAssetUUID == other.toAssetUUID and self.fromAssetUUID == other.fromAssetUUID

    def __repr__(self):
        return f"CreateAssetRelation({self.__dict__})"
