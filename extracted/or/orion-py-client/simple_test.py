#!/usr/bin/env python3
"""
Simple test script as suggested by senior:
1. Take existing data (without partition key)
2. Add partition key column to protobuf DataFrame
3. Push to Kafka and verify
"""

from orion_py_client.client import OrionPyClient
from pyspark.sql import SparkSession
import pyspark.sql.functions as F

def simple_partition_key_test():
    """Simple test: add partition key to existing protobuf DataFrame."""
    
    # Initialize Spark
    spark = SparkSession.builder \
        .appName("SimplePartitionKeyTest") \
        .config("spark.sql.adaptive.enabled", "true") \
        .getOrCreate()
    
    # Initialize Orion client (replace with your actual config)
    client = OrionPyClient(
        features_metadata_source_url="your_metadata_url",
        job_id="your_job_id", 
        job_token="your_job_token"
    )
    
    # Step 1: Create sample data (your existing data)
    sample_data = [
        ("user1", "item1", 0.8, 0.6),
        ("user2", "item2", 0.9, 0.7),
        ("user3", "item3", 0.7, 0.5)
    ]
    
    df = spark.createDataFrame(
        sample_data,
        ["user_id", "item_id", "feature1", "feature2"]
    )
    
    print("=== Step 1: Original DataFrame ===")
    df.show()
    
    # Step 2: Generate protobuf WITHOUT partition key (existing way)
    df_protobuf_existing = client.generate_df_with_protobuf_messages(
        df=df,
        add_kafka_partition_key=False,  # Existing way
        intra_batch_size=1
    )
    
    print("\n=== Step 2: Protobuf DataFrame (existing way) ===")
    print("Schema:", df_protobuf_existing.printSchema())
    print("Columns:", df_protobuf_existing.columns)
    df_protobuf_existing.show(truncate=False)
    
    # Step 3: Generate protobuf WITH partition key (new way)
    df_protobuf_with_key = client.generate_df_with_protobuf_messages(
        df=df,
        add_kafka_partition_key=True,  # New way
        intra_batch_size=1
    )
    
    print("\n=== Step 3: Protobuf DataFrame (with partition key) ===")
    print("Schema:", df_protobuf_with_key.printSchema())
    print("Columns:", df_protobuf_with_key.columns)
    df_protobuf_with_key.show(truncate=False)
    
    # Step 4: Compare the two approaches
    print("\n=== Step 4: Comparison ===")
    print("Existing columns:", df_protobuf_existing.columns)
    print("New columns:", df_protobuf_with_key.columns)
    
    if "partition_key" in df_protobuf_with_key.columns:
        print("✅ SUCCESS: partition_key column added!")
        
        # Show partition key values
        print("\n=== Partition Key Values ===")
        df_protobuf_with_key.select("partition_key").show(truncate=False)
        
        # Step 5: Test Kafka push (optional - uncomment if you have Kafka setup)
        """
        print("\n=== Step 5: Testing Kafka Push ===")
        client.write_protobuf_df_to_kafka(
            df=df_protobuf_with_key,
            kafka_bootstrap_servers="your_kafka_servers:9092",
            kafka_topic="test_partition_key_topic",
            additional_options={
                "kafka.security.protocol": "PLAINTEXT"
            }
        )
        print("✅ Kafka push completed!")
        """
        
    else:
        print("❌ ERROR: partition_key column not found!")
    
    spark.stop()

if __name__ == "__main__":
    simple_partition_key_test() 