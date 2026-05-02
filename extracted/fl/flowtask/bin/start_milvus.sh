#!/bin/bash

# Start milvus-minio container
docker start milvus-minio

# Start milvus-etcd container
docker start milvus-etcd

# Wait for 10 seconds
sleep 10

# Start milvus-standalone container
docker start milvus-standalone

# Start milvus-ui container
docker start milvus-ui
