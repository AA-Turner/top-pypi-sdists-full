
.PHONY: setup setup11 pydeps test test-fault-sweep bench-ci bench bench-gpu-pipeline bench-gpu-pipeline-bootstrap bench-gpu-pipeline-fused test-integration test-all coverage-report
.PHONY: test-resetup lint lint-ci fix docs kind kind-teardown kuberay kuberay11 notebook licenses otel-local otel-local-down
.PHONY: test-integration-gcp test-integration-aws test-stress-gcp test-stress-gcp-explore test-integration-azure
.PHONY: test-pipeline-gcp test-pipeline-aws test-pipeline-azure
.PHONY: test-direct-connect-gcp test-direct-connect-aws test-direct-connect-azure
.PHONY: test-stress-writer-oom-cgroup test-stress-applier-oom-cgroup

setup: kind-teardown kuberay pydeps

setup11: kind-teardown kuberay11 pydeps

pydeps:
	uv sync --all-groups --all-extras --locked

upgrade-pydeps:
	uv sync --all-groups --all-extras

# Ray 2.47+ is known to have some issues with uv.  ray workers would start up
# with no ray library available and hang unit tests.  A workaround is set
# RAY_ENABLE_UV_RUN_RUNTIME_ENV=0.   See this for details:
# https://github.com/ray-project/ray/issues/53848#issuecomment-3056271943

# all unit tests (nightly-only tests excluded; see test-fault-sweep)
test:
	RAY_ENABLE_UV_RUN_RUNTIME_ENV=0 uv run -m pytest src/tests -m "not nightly" --cov=src/geneva --cov-report=term-missing --durations=0

# slow unit tests with local ray
test-ray:
	RAY_ENABLE_UV_RUN_RUNTIME_ENV=0 uv run -m pytest src/tests -m "ray" --cov=src/geneva --cov-report=term-missing --durations=0

# fast unit tests (no ray)
test-fast:
	RAY_ENABLE_UV_RUN_RUNTIME_ENV=0 uv run -m pytest src/tests -m "not ray and not slow" --cov=src/geneva --cov-report=term-missing --durations=0 -n auto

test-flaky:
	# only run flaky tests (currently multibackfill tests)
	RAY_ENABLE_UV_RUN_RUNTIME_ENV=0 uv run -m pytest src/tests --cov=src/geneva -m "multibackfill or limit" --cov-report=term-missing  --durations=0

test-no-flaky:
	RAY_ENABLE_UV_RUN_RUNTIME_ENV=0 uv run -m pytest src/tests --cov=src/geneva -m "not multibackfill and not limit and not nightly" --cov-report=term-missing --durations=0

# Nightly-only: the differential fault sweep. Red by design (exits non-zero on any
# silent/loud finding) until the write-completeness fixes land. Depth and worker count
# default low for local runs and are env-overridable; the nightly workflow raises the
# worker count for its larger runner. See .github/workflows/fault-injection-nightly.yml.
# differential fault-injection sweep (src/tests/differential_fault_sweep.py).
# Extra env knobs pass through: GENEVA_FAULTSWEEP_SRID=off sweeps
# non-stable-row-id sources; GENEVA_FAULTSWEEP_OPS=A,D restricts the op
# alphabet for ad-hoc deep runs; GENEVA_FAULTSWEEP_FLAVORS restricts flavors;
# GENEVA_FAULTSWEEP_VERDICTS_OUT / GENEVA_FAULTSWEEP_COMPARE dump per-case
# verdicts to a JSON file / fail on verdict drift vs such a file (the
# nightly's srid on/off parity check).
test-fault-sweep:
	GENEVA_FAULTSWEEP_MAXLEN=$${GENEVA_FAULTSWEEP_MAXLEN:-1} SWEEP_WORKERS=$${SWEEP_WORKERS:-8} RAY_ENABLE_UV_RUN_RUNTIME_ENV=0 uv run python src/tests/differential_fault_sweep.py

bench-ci:
	# Exclude slow benchmarks (e.g. the video chunking throughput bench): they
	# are stress-scale and run here with the benchmark fixture disabled, which
	# is incompatible with their stats collection. They have dedicated workflows.
	RAY_ENABLE_UV_RUN_RUNTIME_ENV=0 uv run -m pytest src/benches -rx --cov=src/geneva --cov-append -v --benchmark-disable -m "not slow"

bench:
	RAY_ENABLE_UV_RUN_RUNTIME_ENV=0 uv run -m pytest src/benches -v --benchmark-compare --benchmark-autosave --benchmark-save-data --benchmark-group-by=name --benchmark-verbose -s

# Bootstrap the bench dataset only. Downloads Oxford-IIT-Pet from
# Hugging Face and writes ./db/images.lance (~5 min, ~700 MB). Does
# NOT run the CPU preproc that materialises image_rgb — fused-mode
# benches don't need it. Refuses to clobber an existing dataset
# unless invoked with FORCE=1.
bench-gpu-pipeline-bootstrap:
	RAY_ENABLE_UV_RUN_RUNTIME_ENV=0 uv run python src/stress_tests/gpu_pipelining/bench_gpu_embeddings.py --data-load-only $(if $(FORCE),--force-data-load)

# Fused-only sweep — no image_rgb dependency. Builds ./db/images_jpeg.lance
# (idempotent) and runs the fused conditions in bench_gpu_pipelining
# through the public ``t.add_columns + t.backfill`` API. Use
# bench-gpu-pipeline-bootstrap first if ./db/images.lance is missing.
#
# Conditions are split across two invocations because ``--num-readers``
# applies to every condition in one bench run, and the GIL-light vs
# GIL-heavy preprocess paths want different reader counts:
#
#   PIL-style (per-row Python loop holds the GIL):
#     fused_collocated, fused_multi_stream_replicas_collocated
#     Best at 8 readers — adding more contends rather than parallelizes.
#
#   Native-decode (cv2 / nvJPEG release the GIL inside imdecode):
#     fused_cv2_collocated, fused_cv2fast_collocated, fused_nvjpeg_collocated
#     Best at 24 readers (≈ vCPU count − few). See
#     internal_docs/gpu_pipelining.md "GIL-light rule".
#
# Skips ``fused_fat_collocated`` because its UDF declares ``num_cpus=8``
# which compounds with the pipelining multiplier (8 × (1 + 8) = 72 CPUs)
# and wedges Ray's lease queue on any host with < 72 CPUs.
bench-gpu-pipeline-fused:
	RAY_ENABLE_UV_RUN_RUNTIME_ENV=0 uv run python src/stress_tests/gpu_pipelining/prep_jpeg_column.py
	RAY_ENABLE_UV_RUN_RUNTIME_ENV=0 uv run python src/stress_tests/gpu_pipelining/bench_gpu_pipelining.py \
		--num-readers 8 \
		--conditions fused_collocated,fused_multi_stream_replicas_collocated
	RAY_ENABLE_UV_RUN_RUNTIME_ENV=0 uv run python src/stress_tests/gpu_pipelining/bench_gpu_pipelining.py \
		--num-readers 24 \
		--conditions fused_cv2_collocated,fused_cv2fast_collocated,fused_nvjpeg_collocated

# Full GPU-pipelining benchmark sweep. Reproduces the appendix in
# internal_docs/gpu_pipelining.md. Requires a CUDA GPU. On first run
# you'll need to drop --skip-data-load --skip-preproc from the first
# step to bootstrap ./db/images.lance + the image_rgb column (~5 min
# data download + ~60 min CPU preproc). Subsequent runs reuse them.
# Expect ~15-30 min end-to-end on RTX 4000 Ada once the data is
# bootstrapped.
bench-gpu-pipeline: bench-gpu-pipeline-fused
	RAY_ENABLE_UV_RUN_RUNTIME_ENV=0 uv run python src/stress_tests/gpu_pipelining/bench_gpu_embeddings.py --skip-data-load --skip-preproc
	RAY_ENABLE_UV_RUN_RUNTIME_ENV=0 uv run python src/stress_tests/gpu_pipelining/bench_gpu_pipelining.py \
		--num-readers 8 \
		--conditions inline_decode_simple,from_cached_rgb_simple,from_cached_rgb_collocated

# GPU-marked tests are excluded from GCP and AWS to avoid GPU node spin-up
# contention.  They run only on Azure, which has always-on GPU nodes.
# See GEN-439 for the cross-cloud GPU routing strategy.
# test_pipeline.py runs as its own target (and its own CI job) so it can execute
# in parallel with the rest of the integration suite instead of extending a
# single job's wall-clock. The integration targets below exclude it.
test-integration-gcp:
	uv run -m pytest src/integ_tests --ignore=src/integ_tests/direct_connect --ignore=src/integ_tests/test_pipeline.py -m "not phalanx and not gpu" --csp=gcp --test-slug=$(SLUG) $(if $(BUCKET_PATH),--bucket-path=$(BUCKET_PATH)) --cov=src/geneva --cov-append -v -s --cov-report=term-missing --durations=0

test-integration-aws:
	uv run -m pytest src/integ_tests --ignore=src/integ_tests/direct_connect --ignore=src/integ_tests/test_pipeline.py -m "not phalanx and not gpu" --csp=aws --test-slug=$(SLUG) $(if $(BUCKET_PATH),--bucket-path=$(BUCKET_PATH)) --cov=src/geneva --cov-append -v -s --cov-report=term-missing --durations=0

# Azure is the GPU target — GPU-marked tests are NOT excluded here.
test-integration-azure:
	# running locally requires AZURE_STORAGE_ACCOUNT_NAME, AZURE_STORAGE_TOKEN env vars
	# i.e. `export AZURE_STORAGE_TOKEN=$(az account get-access-token --resource https://storage.azure.com/ --query accessToken -o tsv)`
	AZURE_STORAGE_ACCOUNT_NAME=lancedbdevlancedb uv run -m pytest src/integ_tests --ignore=src/integ_tests/direct_connect --ignore=src/integ_tests/test_pipeline.py -m "not phalanx" --csp=azure --test-slug=$(SLUG) $(if $(BUCKET_PATH),--bucket-path=$(BUCKET_PATH)) --cov=src/geneva --cov-append -v -s --cov-report=term-missing --durations=0

# Pipeline tests, split out from the integration targets above so CI can run
# them as a parallel job. GPU exclusion mirrors each cloud's integration policy.
test-pipeline-gcp:
	uv run -m pytest src/integ_tests/test_pipeline.py -m "not phalanx and not gpu" --csp=gcp --test-slug=$(SLUG) $(if $(BUCKET_PATH),--bucket-path=$(BUCKET_PATH)) --cov=src/geneva --cov-append -v -s --cov-report=term-missing --durations=0

test-pipeline-aws:
	uv run -m pytest src/integ_tests/test_pipeline.py -m "not phalanx and not gpu" --csp=aws --test-slug=$(SLUG) $(if $(BUCKET_PATH),--bucket-path=$(BUCKET_PATH)) --cov=src/geneva --cov-append -v -s --cov-report=term-missing --durations=0

test-pipeline-azure:
	AZURE_STORAGE_ACCOUNT_NAME=lancedbdevlancedb uv run -m pytest src/integ_tests/test_pipeline.py -m "not phalanx" --csp=azure --test-slug=$(SLUG) $(if $(BUCKET_PATH),--bucket-path=$(BUCKET_PATH)) --cov=src/geneva --cov-append -v -s --cov-report=term-missing --durations=0

test-phalanx:
	# run aws integration tests against a local phalanx server. V2 dispatch
	# is the default behavior for remote ``db://`` connections — no
	# feature-flag opt-in required.
	AWS_ACCESS_KEY_ID="invalid-creds" AWS_PROFILE="invalid-creds" GENEVA_HOST_OVERRIDE=http://localhost:10024 GENEVA_API_KEY=sk_localtest uv run -m pytest src/integ_tests -m "phalanx" --csp=aws --test-slug=$(SLUG) $(if $(BUCKET_PATH),--bucket-path=$(BUCKET_PATH)) --cov=src/geneva --cov-append -v -s --cov-report=term-missing --durations=0

# test_writer_oom.py, test_applier_oom.py, and test_applier_memory_trim.py
# have their own dedicated CI jobs (``stress-test-writer-oom-cgroup`` /
# ``stress-test-applier-oom-cgroup``) that wrap them in a Docker/Linux
# environment, so they are excluded from the GCP stress runs to avoid running
# them twice and to keep the GCS/K8s-shaped runs focused on tests that actually
# exercise that infrastructure.
test-stress-gcp:
	uv run -m pytest src/stress_tests --ignore=src/stress_tests/test_writer_oom.py --ignore=src/stress_tests/test_applier_oom.py --ignore=src/stress_tests/test_applier_memory_trim.py --csp=gcp --test-slug=$(SLUG) $(if $(BUCKET_PATH),--bucket-path=$(BUCKET_PATH)) --cov=src/geneva --cov-append -v -s --cov-report=term-missing -m "not xfail and not stress_explore" --durations=0

test-stress-gcp-explore:
	uv run -m pytest src/stress_tests --ignore=src/stress_tests/test_writer_oom.py --ignore=src/stress_tests/test_applier_oom.py --ignore=src/stress_tests/test_applier_memory_trim.py --csp=gcp --test-slug=$(SLUG) $(if $(BUCKET_PATH),--bucket-path=$(BUCKET_PATH)) --cov=src/geneva --cov-append -v -s --cov-report=term-missing -m "stress_explore" --durations=0

test-stress-gcp-full:
	uv run -m pytest src/stress_tests --ignore=src/stress_tests/test_writer_oom.py --ignore=src/stress_tests/test_applier_oom.py --ignore=src/stress_tests/test_applier_memory_trim.py --csp=gcp --test-slug=$(SLUG) $(if $(BUCKET_PATH),--bucket-path=$(BUCKET_PATH)) --cov=src/geneva --cov-append -v -s --cov-report=term-missing --durations=0

# Run the writer-OOM stress test inside a Docker container with an
# enforced memory cap, so Ray's memory monitor and the OS OOM-killer
# see a real, hard limit. Works both locally (Docker on Mac/Linux/WSL)
# and on any CI runner with Docker preinstalled (no GCS/K8s needed).
#
# Override the cap, image, or pytest selection via env vars:
#   make test-stress-writer-oom-cgroup WRITER_OOM_MEM_CAP=4G
#   make test-stress-writer-oom-cgroup WRITER_OOM_PYTEST_ARGS="-m stress_explore -k 16MiB-blob"
WRITER_OOM_MEM_CAP ?= 8G
WRITER_OOM_DOCKER_IMAGE ?= ghcr.io/astral-sh/uv:python3.10-bookworm
WRITER_OOM_PYTEST_ARGS ?= -m stress_explore
WRITER_OOM_UV_CACHE_DIR ?= $(HOME)/.cache/uv-stress-writer-oom

test-stress-writer-oom-cgroup:
	mkdir -p "$(WRITER_OOM_UV_CACHE_DIR)"
	# Ensure the cache dir is owned by the host user. Prior runs of
	# this target before the ``--user`` flag was added may have
	# created root-owned files inside the mount; chown+chmod fixes
	# both ownership and any read-only modes.
	docker run --rm -v "$(WRITER_OOM_UV_CACHE_DIR)":/cache alpine sh -c \
		"chown -R $$(id -u):$$(id -g) /cache && chmod -R u+rw /cache"
	docker run --rm \
		--memory=$(WRITER_OOM_MEM_CAP) \
		--memory-swap=$(WRITER_OOM_MEM_CAP) \
		--user $$(id -u):$$(id -g) \
		-v "$(PWD)":/work -w /work \
		-v "$(WRITER_OOM_UV_CACHE_DIR)":/tmp/uv-cache \
		-e HOME=/tmp \
		-e USER=runner \
		-e LOGNAME=runner \
		-e RAY_ENABLE_UV_RUN_RUNTIME_ENV=0 \
		-e UV_CACHE_DIR=/tmp/uv-cache \
		-e UV_PROJECT_ENVIRONMENT=/tmp/venv-stress-writer-oom \
		$(WRITER_OOM_DOCKER_IMAGE) \
		bash -c "uv sync --extra k8s --extra gcp --locked && \
			uv run -m pytest src/stress_tests/test_writer_oom.py \
				$(WRITER_OOM_PYTEST_ARGS) -v -s --durations=0"

# Run applier memory stress tests inside a Docker/Linux container with an
# enforced memory cap. Mirrors the writer-OOM target above. The OOM workload
# intentionally kills an ApplierActor with a per-row allocation above the cap;
# the memory-trim workload needs Linux/glibc ``malloc_trim(0)`` semantics.
#
# Override the cap, image, or pytest selection via env vars:
#   make test-stress-applier-oom-cgroup APPLIER_OOM_MEM_CAP=2G
#   make test-stress-applier-oom-cgroup APPLIER_OOM_PYTEST_ARGS="-k bisect"
APPLIER_OOM_MEM_CAP ?= 4G
APPLIER_OOM_DOCKER_IMAGE ?= ghcr.io/astral-sh/uv:python3.10-bookworm
APPLIER_OOM_PYTEST_ARGS ?= -m stress_explore
APPLIER_OOM_UV_CACHE_DIR ?= $(HOME)/.cache/uv-stress-applier-oom

test-stress-applier-oom-cgroup:
	mkdir -p "$(APPLIER_OOM_UV_CACHE_DIR)"
	docker run --rm -v "$(APPLIER_OOM_UV_CACHE_DIR)":/cache alpine sh -c \
		"chown -R $$(id -u):$$(id -g) /cache && chmod -R u+rw /cache"
	docker run --rm \
		--memory=$(APPLIER_OOM_MEM_CAP) \
		--memory-swap=$(APPLIER_OOM_MEM_CAP) \
		--user $$(id -u):$$(id -g) \
		-v "$(PWD)":/work -w /work \
		-v "$(APPLIER_OOM_UV_CACHE_DIR)":/tmp/uv-cache \
		-e HOME=/tmp \
		-e USER=runner \
		-e LOGNAME=runner \
		-e RAY_ENABLE_UV_RUN_RUNTIME_ENV=0 \
		-e UV_CACHE_DIR=/tmp/uv-cache \
		-e UV_PROJECT_ENVIRONMENT=/tmp/venv-stress-applier-oom \
		$(APPLIER_OOM_DOCKER_IMAGE) \
		bash -c "uv sync --extra k8s --extra gcp --locked && \
			uv pip install --python \"\$$UV_PROJECT_ENVIRONMENT/bin/python\" pytest-timeout && \
			uv run -m pytest src/stress_tests/test_applier_oom.py \
				src/stress_tests/test_applier_memory_trim.py \
				$(APPLIER_OOM_PYTEST_ARGS) -v -s --durations=0"

# Direct-connect integration tests
# Tests Geneva's ability to connect to pre-existing Ray clusters without managing lifecycle.
# Uses hybrid mode: kuberay provisions cluster once per session, Geneva connects via direct network.
test-direct-connect-gcp:
	RAY_ENABLE_UV_RUN_RUNTIME_ENV=0 uv run -m pytest src/integ_tests/direct_connect --csp=gcp --test-slug=$(SLUG) $(if $(BUCKET_PATH),--bucket-path=$(BUCKET_PATH)) --cov=src/geneva --cov-append -v -s --cov-report=term-missing --durations=0

test-direct-connect-aws:
	RAY_ENABLE_UV_RUN_RUNTIME_ENV=0 uv run -m pytest src/integ_tests/direct_connect --csp=aws --test-slug=$(SLUG) $(if $(BUCKET_PATH),--bucket-path=$(BUCKET_PATH)) --cov=src/geneva --cov-append -v -s --cov-report=term-missing --durations=0

test-direct-connect-azure:
	RAY_ENABLE_UV_RUN_RUNTIME_ENV=0 uv run -m pytest src/integ_tests/direct_connect --csp=azure --test-slug=$(SLUG) $(if $(BUCKET_PATH),--bucket-path=$(BUCKET_PATH)) --cov=src/geneva --cov-append -v -s --cov-report=term-missing --durations=0

test-all: test test-integration-gcp test-integration-aws test-integration-azure test-pipeline-gcp test-pipeline-aws test-pipeline-azure

coverage-report:
	uv run coverage xml

test-resetup: setup test

lint:
	uv run ruff format src
	uv run ruff check src
	uv run pyright

lint-ci:
	uv run ruff format --check src
	uv run ruff check src
	uv run pyright

fix:
	uv run ruff format src
	uv run ruff check --fix src
	uv run pyright

# Local observability stack: Grafana (metrics + traces, UI :3000) + Jaeger
# (traces, UI :16686) + Prometheus (metrics, UI :9090) in Docker, plus the
# native otelcol-contrib collector that receives OTLP on :4317. Point geneva at
# it with LANCEDB_OTEL_COLLECTOR_URL=http://localhost:4317.
# The collector runs in the foreground (Ctrl-C to stop); `make otel-local-down`
# stops the Docker services.
otel-local:
	@OTELCOL=$$(command -v otelcol-contrib 2>/dev/null || { [ -x ./otelcol-contrib ] && echo ./otelcol-contrib; }); \
	if [ -z "$$OTELCOL" ]; then \
		echo "ERROR: otelcol-contrib not found. Install it:"; \
		echo "  brew tap open-telemetry/opentelemetry-collector-releases && brew install otelcol-contrib"; \
		echo "  (or download the binary from https://github.com/open-telemetry/opentelemetry-collector-releases/releases"; \
		echo "   and put it on PATH or in this repo root as ./otelcol-contrib)"; \
		exit 1; \
	fi; \
	docker compose -f .github/compose/otel-compose.yaml up -d; \
	echo "Grafana UI:    http://localhost:3000 (metrics + traces, no login)"; \
	echo "Jaeger UI:     http://localhost:16686"; \
	echo "Prometheus UI: http://localhost:9090"; \
	echo "Collector OTLP on :4317 -> export LANCEDB_OTEL_COLLECTOR_URL=http://localhost:4317"; \
	"$$OTELCOL" --config .github/compose/otel-jaeger.yaml

otel-local-down:
	docker compose -f .github/compose/otel-compose.yaml down

docs:
	# uv sync --extra docs # this blows up other dependencies / e.g. notebooks
	cd docs ; uv run mkdocs serve

kind:
	tools/setup_kind_cluster.sh

kind-teardown:
	kind delete cluster --name geneva

kuberay: kind
	tools/setup_kuberay.sh

kuberay11: kind
	KUBERAY_VERSION=1.1.0 tools/setup_kuberay.sh

notebook:
	RAY_ENABLE_UV_RUN_RUNTIME_ENV=0 uv pip install ipykernel ipywidgets jupyterlab_widgets
	RAY_ENABLE_UV_RUN_RUNTIME_ENV=0 uv run jupyter-notebook  --ip=0.0.0.0

# Generate third-party license file
licenses:
	uv sync --all-groups --all-extras --locked
	uv tool run pip-licenses --python .venv/bin/python --format=markdown --with-urls --output-file=PYTHON_THIRD_PARTY_LICENSES.md

pf-api:
	kubectl port-forward svc/geneva-console-api 8000:8000 -n geneva

pf-ui:
	kubectl port-forward svc/geneva-console-ui 3000:3000 -n geneva

up:
	# start enterprise services using docker-compose and stream logs
	# services stay running after Ctrl+C (use `make down` to stop)
	aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 948856271544.dkr.ecr.us-east-1.amazonaws.com
	docker compose -f .github/compose/docker-compose-integ.yml up -d
	docker compose -f .github/compose/docker-compose-integ.yml logs -f

down:
	docker compose -f .github/compose/docker-compose-integ.yml down
