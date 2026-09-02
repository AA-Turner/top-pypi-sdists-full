#!/bin/bash

BASE_DIR=$(dirname "$(realpath "$0")")/..

# Clean up cache directories
rm -rf "$BASE_DIR"/envd/{,filesystem/,process/}__pycache__

# Function to rename protobuf files
rename_pb_files() {
    local module=$1
    local dir="$BASE_DIR/envd/$module"
    
    if [ -f "$dir/${module}_v1_connect.py" ]; then
        mv "$dir/${module}_v1_connect.py" "$dir/${module}_connect.py"
        mv "$dir/${module}_v1_pb2.py" "$dir/${module}_pb2.py"
        mv "$dir/${module}_v1_pb2.pyi" "$dir/${module}_pb2.pyi"
    fi
}

# Function to fix imports
fix_imports() {
    local module=$1
    local dir="$BASE_DIR/envd/$module" 
    sed -i.bak \
        -e "s/from \. import ${module}_v1_pb2/from \. import ${module}_pb2/g" \
        -e "s/FilesystemName = \"${module}.v1/FilesystemName = \"${module}/g" \
        -e "s/ProcessName = \"${module}.v1/ProcessName = \"${module}/g" \
        "$dir"/*
}

# Process modules
for module in process filesystem; do
    rename_pb_files "$module"
    fix_imports "$module"
done

# Clean up backup files
rm -f "$BASE_DIR"/envd/{process,filesystem}/*.bak
