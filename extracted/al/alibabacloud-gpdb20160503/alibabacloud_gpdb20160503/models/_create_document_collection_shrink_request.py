# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from __future__ import annotations

from darabonba.model import DaraModel

class CreateDocumentCollectionShrinkRequest(DaraModel):
    def __init__(
        self,
        algorithm: str = None,
        collection: str = None,
        dbinstance_id: str = None,
        dimension: int = None,
        embedding_model: str = None,
        enable_graph: bool = None,
        entity_types_shrink: str = None,
        external_storage: int = None,
        full_text_retrieval_fields: str = None,
        hnsw_ef_construction: str = None,
        hnsw_m: int = None,
        llmmodel: str = None,
        language: str = None,
        manager_account: str = None,
        manager_account_password: str = None,
        metadata: str = None,
        metadata_indices: str = None,
        metrics: str = None,
        namespace: str = None,
        owner_id: int = None,
        parser: str = None,
        pq_enable: int = None,
        region_id: str = None,
        relationship_types_shrink: str = None,
        sparse_retrieval_fields: str = None,
        sparse_vector_index_config_shrink: str = None,
        support_sparse: bool = None,
        vector_index_config_shrink: str = None,
    ):
        # The vector index algorithm.
        # 
        # Valid values:
        # - hnswflat: HNSW index without quantization compression (default).
        # - novam: Graph index without quantization compression, suitable for high-performance scenarios such as real-time recommendation.
        # - novad: Partitioned index with rabitq quantization, suitable for large-scale, low-cost retrieval scenarios.
        self.algorithm = algorithm
        # The name of the document library to create.
        # 
        # > The name must comply with the object naming conventions of PostgreSQL.
        # 
        # This parameter is required.
        self.collection = collection
        # The instance ID.
        # 
        # > You can call the [DescribeDBInstances](https://help.aliyun.com/document_detail/86911.html) operation to query the details of all AnalyticDB for PostgreSQL instances in a specific region, including the instance IDs.
        # 
        # This parameter is required.
        self.dbinstance_id = dbinstance_id
        # The vector dimensions. The default value is the dimension supported by the embedding algorithm.
        self.dimension = dimension
        # The embedding algorithm. Default value: text-embedding-v3.
        # 
        # > Supported algorithms:
        # > - text-embedding-v3 (recommended, default): 1024, 768, or 512 dimensions
        # > - multimodal-embedding-v1 (recommended): 1024 dimensions, multimodal embedding algorithm
        # > - text-embedding-v1: 1536 dimensions
        # > - text-embedding-v2: 1536 dimensions
        # > - text2vec (not recommended): 1024 dimensions
        # > - m3e-base (not recommended): 768 dimensions
        # > - m3e-small (not recommended): 512 dimensions
        # > - clip-vit-b-32 (not recommended): CLIP ViT-B/32 model, 512 dimensions, image embedding algorithm
        # > - clip-vit-b-16 (not recommended): CLIP ViT-B/16 model, 512 dimensions, image embedding algorithm
        # > - clip-vit-l-14 (not recommended): CLIP ViT-L/14 model, 768 dimensions, image embedding algorithm
        # > - clip-vit-l-14-336px (not recommended): CLIP ViT-L/14@336px model, 768 dimensions, image embedding algorithm
        # > - clip-rn50 (not recommended): CLIP RN50 model, 1024 dimensions, image embedding algorithm
        # > - clip-rn101 (not recommended): CLIP RN101 model, 512 dimensions, image embedding algorithm
        # > - clip-rn50x4 (not recommended): CLIP RN50x4 model, 640 dimensions, image embedding algorithm
        # > - clip-rn50x16 (not recommended): CLIP RN50x16 model, 768 dimensions, image embedding algorithm
        # > - clip-rn50x64 (not recommended): CLIP RN50x64 model, 1024 dimensions, image embedding algorithm
        self.embedding_model = embedding_model
        # Specifies whether to enable knowledge graph construction. Default value: false.
        # 
        # > Before you use this parameter, the instance must be upgraded to a version that supports the graph engine. (During the public preview, submit a ticket to upgrade the version.)
        self.enable_graph = enable_graph
        # The list of entity types.
        # 
        # > This parameter is required when knowledge graph construction is enabled.
        self.entity_types_shrink = entity_types_shrink
        # Specifies whether to use mmap to build the HNSW index. Default value: 0. If data deletion is not required and high data upload speed is needed, we recommend that you set this parameter to 1.
        # 
        # Valid values:
        # - 0: Uses the default segment-page storage to build the index. In this mode, shared_buffer in PostgreSQL can be used for caching, and operations such as deletion and update are supported.
        # - 1: Uses mmap to build the index. In this mode, operations such as deletion and update are not supported.
        # 
        # >Notice: The ExternalStorage parameter is supported only in V6.0. It is not supported in V7.0.
        self.external_storage = external_storage
        # The fields used to retrieve data from the full-text index. Separate multiple fields with commas (,). The fields must be keys defined in Metadata.
        self.full_text_retrieval_fields = full_text_retrieval_fields
        # The size of the candidate set when building the index with the HNSW algorithm. The value must be greater than or equal to 2 × HNSW_M.
        # 
        # > Valid values:
        # >- AnalyticDB for PostgreSQL V6.0 instances: 40 to 4000.
        # >- AnalyticDB for PostgreSQL V7.0 instances: 4 to 1000. Default value: 64.
        self.hnsw_ef_construction = hnsw_ef_construction
        # The maximum number of neighbors in the HNSW algorithm. The operation automatically sets this value based on the vector dimensions. Manual configuration is generally not required.
        # 
        # > Valid values:
        # >- AnalyticDB for PostgreSQL V6.0 instances: 1 to 1000.
        # >- AnalyticDB for PostgreSQL V7.0 instances: 2 to 100. Default value: 16.
        # 
        # > Recommended values based on vector dimensions:
        # >- Less than or equal to 384: 16
        # >- Greater than 384 and less than or equal to 768: 32
        # >- Greater than 768 and less than or equal to 1024: 64
        # >- Greater than 1024: 128
        self.hnsw_m = hnsw_m
        # The name of the LLM. Valid values:
        # - knowledge-extract-standard: Default value.
        # - knowledge-extract-mini
        # > This parameter takes effect only when knowledge graph construction is enabled.
        self.llmmodel = llmmodel
        # The language used to construct the knowledge graph. Valid values:
        # - Simplified Chinese: Simplified Chinese. Default value.
        # - English: English.
        # > This parameter takes effect only when knowledge graph construction is enabled.
        self.language = language
        # The name of the management account that has the rds_superuser permission.
        # 
        # > You can create an account in the console by navigating to Account Management, or by calling the [CreateAccount](https://help.aliyun.com/document_detail/2361789.html) operation.
        # 
        # This parameter is required.
        self.manager_account = manager_account
        # The password of the management account.
        # 
        # This parameter is required.
        self.manager_account_password = manager_account_password
        # The metadata of the vector data, which is a JSON string in MAP format. The key represents the field name, and the value represents the data type.
        # 
        # > Supported data types:
        # > - For a list of data types, see [Data types](https://help.aliyun.com/document_detail/424383.html).
        # > - The money type is not supported.
        # 
        # >Warning: The id, vector, doc_name, content, loader_metadata, source, and to_tsvector fields are reserved and cannot be used.
        self.metadata = metadata
        # The scalar index fields. Separate multiple fields with commas (,). The fields must be keys defined in Metadata.
        self.metadata_indices = metadata_indices
        # The distance metric used when building the vector index.
        # 
        # Valid values:
        # - **l2**: Euclidean distance.
        # - **ip**: Dot product (inner product) distance.
        # - **cosine** (default): Cosine similarity.
        self.metrics = metrics
        # The namespace. Default value: public.
        # 
        # > You can call the [CreateNamespace](https://help.aliyun.com/document_detail/2401495.html) operation to create a namespace, or call the [ListNamespaces](https://help.aliyun.com/document_detail/2401502.html) operation to view the namespace list.
        self.namespace = namespace
        self.owner_id = owner_id
        # The tokenizer used to retrieve data from the full-text index. Default value: zh_cn.
        self.parser = parser
        # Specifies whether to enable the Product Quantization (PQ) algorithm to accelerate index building. It is recommended to enable this feature when the data volume exceeds 500,000. Valid values:
        # - 0: Disable.
        # - 1: Enable (default).
        self.pq_enable = pq_enable
        # The region ID of the instance.
        # 
        # This parameter is required.
        self.region_id = region_id
        # The list of relationship edge types.
        # 
        # > This parameter is required when knowledge graph construction is enabled.
        self.relationship_types_shrink = relationship_types_shrink
        # The metadata fields used to build sparse vectors. Separate multiple fields with commas (,). The fields must be keys defined in Metadata.
        self.sparse_retrieval_fields = sparse_retrieval_fields
        # The sparse vector index configuration. If this parameter is specified, a sparse vector index is created.
        self.sparse_vector_index_config_shrink = sparse_vector_index_config_shrink
        # Specifies whether to support sparse vectors. Default value: false.
        self.support_sparse = support_sparse
        # The dense vector index configuration.
        self.vector_index_config_shrink = vector_index_config_shrink

    def validate(self):
        pass

    def to_map(self):
        result = dict()
        _map = super().to_map()
        if _map is not None:
            result = _map
        if self.algorithm is not None:
            result['Algorithm'] = self.algorithm

        if self.collection is not None:
            result['Collection'] = self.collection

        if self.dbinstance_id is not None:
            result['DBInstanceId'] = self.dbinstance_id

        if self.dimension is not None:
            result['Dimension'] = self.dimension

        if self.embedding_model is not None:
            result['EmbeddingModel'] = self.embedding_model

        if self.enable_graph is not None:
            result['EnableGraph'] = self.enable_graph

        if self.entity_types_shrink is not None:
            result['EntityTypes'] = self.entity_types_shrink

        if self.external_storage is not None:
            result['ExternalStorage'] = self.external_storage

        if self.full_text_retrieval_fields is not None:
            result['FullTextRetrievalFields'] = self.full_text_retrieval_fields

        if self.hnsw_ef_construction is not None:
            result['HnswEfConstruction'] = self.hnsw_ef_construction

        if self.hnsw_m is not None:
            result['HnswM'] = self.hnsw_m

        if self.llmmodel is not None:
            result['LLMModel'] = self.llmmodel

        if self.language is not None:
            result['Language'] = self.language

        if self.manager_account is not None:
            result['ManagerAccount'] = self.manager_account

        if self.manager_account_password is not None:
            result['ManagerAccountPassword'] = self.manager_account_password

        if self.metadata is not None:
            result['Metadata'] = self.metadata

        if self.metadata_indices is not None:
            result['MetadataIndices'] = self.metadata_indices

        if self.metrics is not None:
            result['Metrics'] = self.metrics

        if self.namespace is not None:
            result['Namespace'] = self.namespace

        if self.owner_id is not None:
            result['OwnerId'] = self.owner_id

        if self.parser is not None:
            result['Parser'] = self.parser

        if self.pq_enable is not None:
            result['PqEnable'] = self.pq_enable

        if self.region_id is not None:
            result['RegionId'] = self.region_id

        if self.relationship_types_shrink is not None:
            result['RelationshipTypes'] = self.relationship_types_shrink

        if self.sparse_retrieval_fields is not None:
            result['SparseRetrievalFields'] = self.sparse_retrieval_fields

        if self.sparse_vector_index_config_shrink is not None:
            result['SparseVectorIndexConfig'] = self.sparse_vector_index_config_shrink

        if self.support_sparse is not None:
            result['SupportSparse'] = self.support_sparse

        if self.vector_index_config_shrink is not None:
            result['VectorIndexConfig'] = self.vector_index_config_shrink

        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Algorithm') is not None:
            self.algorithm = m.get('Algorithm')

        if m.get('Collection') is not None:
            self.collection = m.get('Collection')

        if m.get('DBInstanceId') is not None:
            self.dbinstance_id = m.get('DBInstanceId')

        if m.get('Dimension') is not None:
            self.dimension = m.get('Dimension')

        if m.get('EmbeddingModel') is not None:
            self.embedding_model = m.get('EmbeddingModel')

        if m.get('EnableGraph') is not None:
            self.enable_graph = m.get('EnableGraph')

        if m.get('EntityTypes') is not None:
            self.entity_types_shrink = m.get('EntityTypes')

        if m.get('ExternalStorage') is not None:
            self.external_storage = m.get('ExternalStorage')

        if m.get('FullTextRetrievalFields') is not None:
            self.full_text_retrieval_fields = m.get('FullTextRetrievalFields')

        if m.get('HnswEfConstruction') is not None:
            self.hnsw_ef_construction = m.get('HnswEfConstruction')

        if m.get('HnswM') is not None:
            self.hnsw_m = m.get('HnswM')

        if m.get('LLMModel') is not None:
            self.llmmodel = m.get('LLMModel')

        if m.get('Language') is not None:
            self.language = m.get('Language')

        if m.get('ManagerAccount') is not None:
            self.manager_account = m.get('ManagerAccount')

        if m.get('ManagerAccountPassword') is not None:
            self.manager_account_password = m.get('ManagerAccountPassword')

        if m.get('Metadata') is not None:
            self.metadata = m.get('Metadata')

        if m.get('MetadataIndices') is not None:
            self.metadata_indices = m.get('MetadataIndices')

        if m.get('Metrics') is not None:
            self.metrics = m.get('Metrics')

        if m.get('Namespace') is not None:
            self.namespace = m.get('Namespace')

        if m.get('OwnerId') is not None:
            self.owner_id = m.get('OwnerId')

        if m.get('Parser') is not None:
            self.parser = m.get('Parser')

        if m.get('PqEnable') is not None:
            self.pq_enable = m.get('PqEnable')

        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')

        if m.get('RelationshipTypes') is not None:
            self.relationship_types_shrink = m.get('RelationshipTypes')

        if m.get('SparseRetrievalFields') is not None:
            self.sparse_retrieval_fields = m.get('SparseRetrievalFields')

        if m.get('SparseVectorIndexConfig') is not None:
            self.sparse_vector_index_config_shrink = m.get('SparseVectorIndexConfig')

        if m.get('SupportSparse') is not None:
            self.support_sparse = m.get('SupportSparse')

        if m.get('VectorIndexConfig') is not None:
            self.vector_index_config_shrink = m.get('VectorIndexConfig')

        return self

