#!/usr/bin/env python3
"""
Test script to verify partition key column name and functionality.
"""

from orion_py_client.client import OrionPyClient
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, ArrayType, FloatType

def test_partition_key_column():
    """Test that partition key column is correctly named 'partition_key'."""
    
    # Initialize Spark
    spark = SparkSession.builder \
        .appName("PartitionKeyTest") \
        .config("spark.sql.adaptive.enabled", "true") \
        .getOrCreate()
    
    # Create a mock client (you'll need to replace with actual config)
    client = OrionPyClient(
        features_metadata_source_url="mock_url",
        job_id="test_job",
        job_token="test_token"
    )
    
    # Create test data
    test_data = [
        ("user1", "item1", 0.8, 0.6, [0.1, 0.2, 0.3]),
        ("user2", "item2", 0.9, 0.7, [0.4, 0.5, 0.6])
    ]
    
    df = spark.createDataFrame(
        test_data,
        ["user_id", "item_id", "feature1", "feature2", "vector_feature"]
    )
    
    print("=== Testing Partition Key Column Name ===")
    print(f"Original DataFrame schema: {df.printSchema()}")
    
    try:
        # Test with partition key enabled
        df_with_partition_key = client.generate_df_with_protobuf_messages(
            df=df,
            add_kafka_partition_key=True,
            intra_batch_size=1
        )
        
        print("\n=== DataFrame with Partition Key ===")
        print(f"Schema: {df_with_partition_key.printSchema()}")
        print(f"Columns: {df_with_partition_key.columns}")
        
        # Verify partition_key column exists
        if "partition_key" in df_with_partition_key.columns:
            print("✅ SUCCESS: 'partition_key' column found!")
            
            # Show sample data
            print("\n=== Sample Data with Partition Keys ===")
            df_with_partition_key.show(truncate=False)
            
            # Verify partition key format
            sample_row = df_with_partition_key.first()
            if sample_row:
                partition_key = sample_row["partition_key"]
                print(f"✅ Partition key format: '{partition_key}'")
                print(f"✅ Partition key type: {type(partition_key)}")
                
        else:
            print("❌ ERROR: 'partition_key' column not found!")
            print(f"Available columns: {df_with_partition_key.columns}")
            
    except Exception as e:
        print(f"❌ ERROR during testing: {str(e)}")
        import traceback
        traceback.print_exc()
    
    finally:
        spark.stop()

if __name__ == "__main__":
    test_partition_key_column() 