from pinecone_plugin_interface import PluginMetadata
from .create_index_for_model import CreateIndexForModel
from .search_records import SearchRecords
from .upsert_records import UpsertRecords

__installables__ = [
    PluginMetadata(
        target_object="Pinecone",
        namespace="create_index_for_model",
        implementation_class=CreateIndexForModel,
    ),
    PluginMetadata(
        target_object="Index",
        namespace="search_records",
        implementation_class=SearchRecords,
    ),
    PluginMetadata(
        target_object="Index",
        namespace="upsert_records",
        implementation_class=UpsertRecords,
    ),
]
