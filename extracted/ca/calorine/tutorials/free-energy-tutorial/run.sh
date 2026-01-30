#!/bin/bash

# Iterate over all directories in the current directory
for dir in */; do
    # Check if the directory contains a file named 'gpumd'
    echo "Running gpumd in $dir"
    # Change to the subdirectory and run gpumd
    (cd "$dir" && gpumd)
done

