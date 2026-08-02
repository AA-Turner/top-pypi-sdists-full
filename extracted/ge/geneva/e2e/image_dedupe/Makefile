# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

# Load local overrides (not committed to git).
# Create Makefile.local to set variables persistently, e.g.:
#   echo 'OUTPUT_BASE = s3://my-bucket/phash' > Makefile.local
-include Makefile.local

GENERATE := uv run python generate_synthetic_phashes.py
DUPLICATE_PCT ?= 0.05
SEED ?= 42
WORKERS ?= $(shell nproc 2>/dev/null || sysctl -n hw.ncpu 2>/dev/null || echo 4)
# Base path for output datasets. Override to write to cloud or a different directory.
# Examples:
#   make phash-10m OUTPUT_BASE=s3://my-bucket/phash
#   make phash-10m OUTPUT_BASE=gs://my-bucket/phash
#   make phash-10m OUTPUT_BASE=/mnt/data/phash
OUTPUT_BASE ?= .

.PHONY: phash-10m phash-100m phash-1b phash-25b

phash-10m:
	$(GENERATE) \
		--output $(OUTPUT_BASE)/phash_10m.lance \
		--num-rows 10000000 \
		--duplicate-pct $(DUPLICATE_PCT) \
		--fragment-size 100000 \
		--seed $(SEED) \
		--workers $(WORKERS) \
		--overwrite

phash-100m:
	$(GENERATE) \
		--output $(OUTPUT_BASE)/phash_100m.lance \
		--num-rows 100000000 \
		--duplicate-pct $(DUPLICATE_PCT) \
		--fragment-size 1000000 \
		--seed $(SEED) \
		--workers $(WORKERS) \
		--overwrite

phash-1b:
	$(GENERATE) \
		--output $(OUTPUT_BASE)/phash_1b.lance \
		--num-rows 1000000000 \
		--duplicate-pct $(DUPLICATE_PCT) \
		--fragment-size 1000000 \
		--seed $(SEED) \
		--workers $(WORKERS) \
		--overwrite

# Note: 4 workers on 64-cpu / 128GB RAM with 5M rows/fragment was stable
# when writing to Azure. Higher worker counts caused OOM.
phash-25b:
	$(GENERATE) \
		--output $(OUTPUT_BASE)/phash_25b.lance \
		--num-rows 25000000000 \
		--duplicate-pct $(DUPLICATE_PCT) \
		--fragment-size 5000000 \
		--seed $(SEED) \
		--workers $(WORKERS) \
		--overwrite
