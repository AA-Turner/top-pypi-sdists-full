#!/bin/bash
set -euo pipefail

# Install apt packages
sudo apt-get update
sudo apt-get install -y libgtest-dev clang-format cmake
