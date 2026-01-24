# Benchmark commands

# Capacity benchmark
CLUSTER_NAME ?= dr-small
# WORKLOAD_NAMES supports comma-separated list (e.g., "parallel-small,parallel-tiny")
# Falls back to WORKLOAD_NAME for backwards compatibility
WORKLOAD_NAMES ?= $(WORKLOAD_NAME)
WORKLOAD_NAME ?= parallel-small

# For other benchmarks
BASE_URL ?= https://benchmark-dr-s-2799835ad04b501a95044223ae72ced7.staging.langgraph.app
SLOWEST_N ?= 2
RAMP_MULTIPLIER ?= 2
WAIT_SECONDS ?= 60
CLEAR_DELAY_SECONDS ?= 5
DATA_SIZE ?= 1000
DELAY ?= 0
EXPAND ?= 1
STEPS ?= 100

benchmark-burst:
	make benchmark-reset
	k6 run burst.js

benchmark-ramp:
	make benchmark-reset
	k6 run --out json=raw_data_$(shell date +%Y-%m-%dT%H-%M-%S).json --system-tags=[] ramp.js

benchmark-capacity:
	rm -f capacity_summary.json
	npm install
	LANGSMITH_API_KEY=$(LANGSMITH_API_KEY) \
	CLUSTER_NAME=$(CLUSTER_NAME) \
	WORKLOAD_NAMES=$(WORKLOAD_NAMES) \
	node capacity_runner.mjs

benchmark-charts:
	npm install
	node graphs.js $(shell ls -t raw_data_*.json | head -1) true

benchmark-reset:
	node clean-cli.js

benchmark-new-revision:
	node update-revision.js

benchmark-clean:
	rm -f results_*.json summary_*.json raw_data_*.json *_chart_*.png

benchmark-clean-charts:
	rm -f *_chart_*.png

# Mixed workload benchmark - tests quick runs competing with long runs
QUICK_VUS ?= 250
QUICK_ITERATIONS ?= 1000
QUICK_STEPS ?= 5
QUICK_DATA_SIZE ?= 100
QUICK_MAX_WAIT_SECONDS ?= 120
QUICK_POLL_INTERVAL ?= 2
LONG_VUS ?= 5
LONG_ITERATIONS ?= 10
LONG_STEPS ?= 50
LONG_DELAY ?= 1
LONG_DATA_SIZE ?= 10000
LONG_MAX_WAIT_SECONDS ?= 200
LONG_POLL_INTERVAL ?= 5

benchmark-mixed:
	rm -f mixed_workload_*.json
	npm install
	BASE_URL=$(BASE_URL) \
	SLOWEST_N=$(SLOWEST_N) \
	QUICK_VUS=$(QUICK_VUS) \
	QUICK_ITERATIONS=$(QUICK_ITERATIONS) \
	QUICK_STEPS=$(QUICK_STEPS) \
	QUICK_DATA_SIZE=$(QUICK_DATA_SIZE) \
	QUICK_MAX_WAIT_SECONDS=$(QUICK_MAX_WAIT_SECONDS) \
	QUICK_POLL_INTERVAL=$(QUICK_POLL_INTERVAL) \
	LONG_VUS=$(LONG_VUS) \
	LONG_ITERATIONS=$(LONG_ITERATIONS) \
	LONG_STEPS=$(LONG_STEPS) \
	LONG_DELAY=$(LONG_DELAY) \
	LONG_DATA_SIZE=$(LONG_DATA_SIZE) \
	LONG_MAX_WAIT_SECONDS=$(LONG_MAX_WAIT_SECONDS) \
	LONG_POLL_INTERVAL=$(LONG_POLL_INTERVAL) \
	node mixed_workload_runner.mjs
