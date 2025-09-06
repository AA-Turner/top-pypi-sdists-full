from .utils.helpers import get_features_details, touch_cloud_path, file_exists
import numpy as np


class OrionPyClient:

    def __init__(self, features_metadata_source_url: str, job_id: str, job_token: str, fgs_to_consider: list = []):
        self.features_metadata_source_url = features_metadata_source_url
        self.job_id = job_id
        self.job_token = job_token
        self.fgs_to_consider = fgs_to_consider
        
        (
            offline_src_type_columns,
            offline_col_to_default_values_map,
            onfs_fg_to_onfs_feat_map,
            onfs_fg_to_ofs_feat_map,
            fg_to_datatype_map,
            entity_label,
            entity_column_names,
            offline_col_to_datatype_map,
        ) = get_features_details(
            self.features_metadata_source_url,
            self.job_id,
            self.job_token,
            self.fgs_to_consider,
        )
        self.offline_src_type_columns = offline_src_type_columns
        self.offline_col_to_default_values_map = offline_col_to_default_values_map
        self.onfs_fg_to_onfs_feat_map = onfs_fg_to_onfs_feat_map
        self.onfs_fg_to_ofs_feat_map = onfs_fg_to_ofs_feat_map
        self.fg_to_datatype_map = fg_to_datatype_map
        self.entity_label = entity_label
        self.entity_column_names = entity_column_names
        self.offline_col_to_datatype_map = offline_col_to_datatype_map
        
    def get_offline_col_to_datatype_map(self):
        return self.offline_col_to_datatype_map

    def get_features_details(self):
        return (
            self.offline_src_type_columns,
            self.offline_col_to_default_values_map,
            self.entity_column_names,
        )

    def generate_df_with_protobuf_messages(self, df,  intra_batch_size: int = 20, add_kafka_partition_key: bool = False):
        from pyspark.sql.types import StructType, StructField, BinaryType, LongType

        # Check condition globally once
        should_add_partition_key = add_kafka_partition_key and intra_batch_size == 1
        
        if should_add_partition_key:
            return self._generate_df_with_partition_keys(df, intra_batch_size)
        else:
            return self._generate_df_without_partition_keys(df, intra_batch_size)

    def _generate_df_without_partition_keys(self, df, intra_batch_size: int):
        """Generate DataFrame with protobuf messages without partition keys."""
        from pyspark.sql.types import StructType, StructField, BinaryType, LongType

        def process_partition(iterator):
            """Convert each partition of Spark DataFrame into Protobuf serialized messages."""
            from .proto.persist.persist_pb2 import (
                Query,
                FeatureGroupSchema,
                Data,
                FeatureValues,
                Values,
                Vector,
            )

            # Only consider derived_fp32 feature group
            feature_group_schema = []
            if "derived_fp32" in self.onfs_fg_to_onfs_feat_map:
                feature_group_schema = [
                    FeatureGroupSchema(label="derived_fp32", feature_labels=self.onfs_fg_to_onfs_feat_map["derived_fp32"])
                ]

            current_batch = []
            batch_id = 0

            for row in iterator:
                feature_values = self._create_feature_values(row)
                
                # Construct Data message for current row
                data_msg = Data(
                    key_values=[str(row[col]) for col in self.entity_column_names],
                    feature_values=feature_values,
                )

                current_batch.append(data_msg)

                # When batch is full, create and yield Query message
                if len(current_batch) >= intra_batch_size:
                    query = Query(
                        entity_label=self.entity_label,
                        keys_schema=self.entity_column_names,
                        feature_group_schema=feature_group_schema,
                        data=current_batch,
                    )
                    yield (query.SerializeToString(), batch_id)
                    current_batch = []
                    batch_id += 1

            # Handle any remaining items in the last batch
            if current_batch:
                query = Query(
                    entity_label=self.entity_label,
                    keys_schema=self.entity_column_names,
                    feature_group_schema=feature_group_schema,
                    data=current_batch,
                )
                yield (query.SerializeToString(), batch_id)

        # Define output schema
        protobuf_schema = StructType([
            StructField("value", BinaryType(), False),
            StructField("intra_batch_id", LongType(), False)
        ])

        # Apply mapPartitions
        out_df = df.rdd.mapPartitions(process_partition).toDF(protobuf_schema)
        return out_df

    def _generate_df_with_partition_keys(self, df, intra_batch_size: int):
        """Generate DataFrame with protobuf messages including partition keys."""
        from pyspark.sql.types import StructType, StructField, BinaryType, LongType, StringType

        def process_partition(iterator):
            """Convert each partition of Spark DataFrame into Protobuf serialized messages with partition keys."""
            from .proto.persist.persist_pb2 import (
                Query,
                FeatureGroupSchema,
                Data,
                FeatureValues,
                Values,
                Vector,
            )

            # Only consider derived_fp32 feature group
            feature_group_schema = []
            if "derived_fp32" in self.onfs_fg_to_onfs_feat_map:
                feature_group_schema = [
                    FeatureGroupSchema(label="derived_fp32", feature_labels=self.onfs_fg_to_onfs_feat_map["derived_fp32"])
                ]

            current_batch = []
            batch_id = 0

            for row in iterator:
                feature_values = self._create_feature_values(row)
                
                # Construct Data message for current row
                data_msg = Data(
                    key_values=[str(row[col]) for col in self.entity_column_names],
                    feature_values=feature_values,
                )

                current_batch.append(data_msg)

                # When batch is full, create and yield Query message
                if len(current_batch) >= intra_batch_size:
                    query = Query(
                        entity_label=self.entity_label,
                        keys_schema=self.entity_column_names,
                        feature_group_schema=feature_group_schema,
                        data=current_batch,
                    )
                    
                    # Create partition key from the FIRST row in the batch (since all rows in batch should have same entity)
                    first_row_entity_values = [str(current_batch[0].key_values[i]) for i in range(len(self.entity_column_names))]
                    partition_key = "|".join(first_row_entity_values)
                    print(f"DEBUG: Entity columns: {self.entity_column_names}")
                    print(f"DEBUG: First row key_values: {current_batch[0].key_values}")
                    print(f"DEBUG: Partition key: {partition_key}")
                    yield (query.SerializeToString(), batch_id, partition_key)
                    
                    current_batch = []
                    batch_id += 1

            # Handle any remaining items in the last batch
            if current_batch:
                query = Query(
                    entity_label=self.entity_label,
                    keys_schema=self.entity_column_names,
                    feature_group_schema=feature_group_schema,
                    data=current_batch,
                )
                
                # For the last batch, use the first row's entity values
                first_row_entity_values = [str(current_batch[0].key_values[i]) for i in range(len(self.entity_column_names))]
                partition_key = "|".join(first_row_entity_values)
                print(f"DEBUG: Last batch - Entity columns: {self.entity_column_names}")
                print(f"DEBUG: Last batch - First row key_values: {current_batch[0].key_values}")
                print(f"DEBUG: Last batch - Partition key: {partition_key}")
                yield (query.SerializeToString(), batch_id, partition_key)

        # Define output schema with partition key
        protobuf_schema = StructType([
            StructField("value", BinaryType(), False),
            StructField("intra_batch_id", LongType(), False),
            StructField("key", StringType(), False)
        ])

        # Apply mapPartitions
        out_df = df.rdd.mapPartitions(process_partition).toDF(protobuf_schema)
        return out_df

    def _create_feature_values(self, row):
        """Create feature values for a given row."""
        from .proto.persist.persist_pb2 import FeatureValues, Values, Vector
        
        feature_values = []
        # Only process derived_fp32 feature group
        if "derived_fp32" in self.onfs_fg_to_ofs_feat_map:
            fg_label = "derived_fp32"
            features = self.onfs_fg_to_ofs_feat_map[fg_label]
            curr_datatype = self.fg_to_datatype_map[fg_label]

            values = Values()
            # For Scalar Data types
            
            if curr_datatype == "DataTypeFP8E5M2":
                values.fp32_values.extend(
                    [np.float32(row[feature]) for feature in features]
                )                        
            elif curr_datatype == "DataTypeFP8E4M3":
                values.fp32_values.extend(
                    [np.float32(row[feature]) for feature in features]
                )
            elif curr_datatype == "DataTypeFP16":
                values.fp32_values.extend(
                    [np.float32(row[feature]) for feature in features]
                )
            elif curr_datatype == "DataTypeFP32":
                values.fp32_values.extend(
                    [np.float32(row[feature]) for feature in features]
                )
            elif curr_datatype == "DataTypeFP64":
                values.fp64_values.extend(
                    [np.float64(row[feature]) for feature in features]
                )
            elif curr_datatype == "DataTypeInt8":
                values.int32_values.extend(
                    [np.int32(row[feature]) for feature in features]
                )
            elif curr_datatype == "DataTypeInt16":
                values.int32_values.extend(
                    [np.int32(row[feature]) for feature in features]
                )
            elif curr_datatype == "DataTypeInt32":
                values.int32_values.extend(
                    [np.int32(row[feature]) for feature in features]
                )
            elif curr_datatype == "DataTypeInt64":
                values.int64_values.extend(
                    [np.int64(row[feature]) for feature in features]
                )
            elif curr_datatype == "DataTypeUint8":
                values.uint32_values.extend(
                    [np.uint32(row[feature]) for feature in features]
                )
            elif curr_datatype == "DataTypeUint16":
                values.uint32_values.extend(
                    [np.uint32(row[feature]) for feature in features]
                )
            elif curr_datatype == "DataTypeUint32":
                values.uint32_values.extend(
                    [np.uint32(row[feature]) for feature in features]
                )
            elif curr_datatype == "DataTypeUint64":
                values.uint64_values.extend(
                    [np.uint64(row[feature]) for feature in features]
                )
            elif curr_datatype == "DataTypeString":
                values.string_values.extend(
                    [str(row[feature]) for feature in features]
                )
            elif curr_datatype == "DataTypeBool":
                values.bool_values.extend(
                    [bool(row[feature]) for feature in features]
                )

            # For Vector Data types
            elif curr_datatype == "DataTypeFP16Vector":
                for feature in features:
                    vector_values = Values(
                        fp32_values=[np.float32(x) for x in row[feature]]
                    )
                    values.vector.append(Vector(values=vector_values))
            elif curr_datatype == "DataTypeFP8E5M2Vector":
                for feature in features:
                    vector_values = Values(
                        fp32_values=[np.float32(x) for x in row[feature]]
                    )
                    values.vector.append(Vector(values=vector_values))
            elif curr_datatype == "DataTypeFP8E4M3Vector":
                for feature in features:
                    vector_values = Values(
                        fp32_values=[np.float32(x) for x in row[feature]]
                    )
                    values.vector.append(Vector(values=vector_values))                            
            elif curr_datatype == "DataTypeFP32Vector":
                for feature in features:
                    vector_values = Values(
                        fp32_values=[np.float32(x) for x in row[feature]]
                    )
                    values.vector.append(Vector(values=vector_values))
            elif curr_datatype == "DataTypeFP64Vector":
                for feature in features:
                    vector_values = Values(
                        fp64_values=[np.float64(x) for x in row[feature]]
                    )
                    values.vector.append(Vector(values=vector_values))
            elif curr_datatype == "DataTypeInt8Vector":
                for feature in features:
                    vector_values = Values(
                        int32_values=[np.int32(x) for x in row[feature]]
                    )
                    values.vector.append(Vector(values=vector_values))
            elif curr_datatype == "DataTypeInt16Vector":
                for feature in features:
                    vector_values = Values(
                        int32_values=[np.int32(x) for x in row[feature]]
                    )
                    values.vector.append(Vector(values=vector_values))                            
            elif curr_datatype == "DataTypeInt32Vector":
                for feature in features:
                    vector_values = Values(
                        int32_values=[np.int32(x) for x in row[feature]]
                    )
                    values.vector.append(Vector(values=vector_values))
            elif curr_datatype == "DataTypeInt64Vector":
                for feature in features:
                    vector_values = Values(
                        int64_values=[np.int64(x) for x in row[feature]]
                    )
                    values.vector.append(Vector(values=vector_values))
            elif curr_datatype == "DataTypeUint8Vector":
                for feature in features:
                    vector_values = Values(
                        uint32_values=[np.uint32(x) for x in row[feature]]
                    )
                    values.vector.append(Vector(values=vector_values))
            elif curr_datatype == "DataTypeUint16Vector":
                for feature in features:
                    vector_values = Values(
                        uint32_values=[np.uint32(x) for x in row[feature]]
                    )
                    values.vector.append(Vector(values=vector_values))
            elif curr_datatype == "DataTypeUint32Vector":
                for feature in features:
                    vector_values = Values(
                        uint32_values=[np.uint32(x) for x in row[feature]]
                    )
                    values.vector.append(Vector(values=vector_values))
            elif curr_datatype == "DataTypeUint64Vector":
                for feature in features:
                    vector_values = Values(
                        uint64_values=[np.uint64(x) for x in row[feature]]
                    )
                    values.vector.append(Vector(values=vector_values))
            elif curr_datatype == "DataTypeStringVector":
                for feature in features:
                    vector_values = Values(
                        string_values=[str(x) for x in row[feature]]
                    )
                    values.vector.append(Vector(values=vector_values))
            elif curr_datatype == "DataTypeBoolVector":
                for feature in features:
                    vector_values = Values(
                        bool_values=[bool(x) for x in row[feature]]
                    )
                    values.vector.append(Vector(values=vector_values))
            else:
                raise ValueError(f"Unsupported data type: {curr_datatype} for feature group: {fg_label}")

            feature_values.append(FeatureValues(values=values))
        
        return feature_values


    def write_protobuf_df_to_kafka(
        self,
        spark,
        proto_out_path,
        kafka_bootstrap_servers,
        kafka_topic,
        additional_options={},
        kafka_num_batches=1,
        push_all_data=False
    ):
        """
        Optimized Kafka writing using partitioned proto data
        """
        kafka_config = {
            "kafka.bootstrap.servers": kafka_bootstrap_servers,
            "topic": kafka_topic,
        }
        kafka_config.update(additional_options or {})
        
        if kafka_num_batches == 1:
            # Single batch - read all data
            df = spark.read.parquet(proto_out_path)
            df = df.drop("intra_batch_id") if "intra_batch_id" in df.columns else df
            df.write.format("kafka").options(**kafka_config).save()
            print("Wrote single batch to Kafka")
        else:
            print(f"Writing {kafka_num_batches} batches to Kafka using partitioned reads")

            # Read each batch partition
            for i in range(kafka_num_batches):
                partition_path = f"{proto_out_path}batch_no={i}/"
                is_partition_pushed = file_exists(partition_path + '_PUSHED')

                if push_all_data or not is_partition_pushed:
                    # Dynamic partition pruning read
                    df_batch = spark.read \
                        .option("basePath", proto_out_path) \
                        .parquet(partition_path)
                    
                    # Clean up columns
                    columns_to_drop = [col for col in ["batch_no", "intra_batch_id"] if col in df_batch.columns]
                    if columns_to_drop:
                        df_batch = df_batch.drop(*columns_to_drop)
                    
                    df_batch.write.format("kafka").options(**kafka_config).save()
                    print(f"Wrote batch {i} to Kafka")
                    touch_cloud_path(partition_path, '_PUSHED')
