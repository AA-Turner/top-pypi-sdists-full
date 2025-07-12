from typing import Optional

from typing_extensions import Literal

from tecton._internals.tecton_pydantic import StrictModel
from tecton_proto.args import feature_view__client_pb2 as feature_view_pb2


class IcebergConfig(StrictModel):
    """(Config Class) IcebergConfig Class.

    This class describes the attributes of Iceberg-based offline feature store storage for the feature definition.

    :param num_entity_buckets: The number of buckets for the bucket transform partition based on the first entity key.
    :param subdirectory_override: This is for the location of the feature data in the offline store.
    By default, all feature views will be under the subdirectory 'ws/<workspace_name>' if this param is not specified.
    """

    kind: Literal["IcebergConfig"] = "IcebergConfig"  # Used for YAML parsing as a Pydantic discriminator.
    num_entity_buckets: int = 1000
    subdirectory_override: Optional[str] = None

    def _to_proto(self):
        """
        Converts the IcebergConfig instance to a proto object.
        :return: OfflineFeatureStoreConfig proto object
        """
        store_config = feature_view_pb2.OfflineFeatureStoreConfig()
        store_config.iceberg.num_entity_buckets = self.num_entity_buckets
        if self.subdirectory_override:
            store_config.subdirectory_override = self.subdirectory_override
        return store_config

    @classmethod
    def from_proto(cls, proto: feature_view_pb2.OfflineFeatureStoreConfig):
        """
        Converts the proto object to the IcebergConfig class.
        :param proto: Protobuf representation of the offline feature store.
        :return: IcebergConfig instance.
        """
        return cls(
            num_entity_buckets=proto.iceberg.num_entity_buckets,
            subdirectory_override=proto.subdirectory_override or None,
        )
