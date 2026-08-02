E2E_MAKEFILE_DIR := $(dir $(lastword $(MAKEFILE_LIST)))
include $(E2E_MAKEFILE_DIR)config.mk

.PHONY: test-e2e-oxford-pets-gcp test-e2e-oxford-pets-aws test-e2e-oxford-pets-azure
.PHONY: test-e2e-openvid-gcp test-e2e-openvid-aws test-e2e-openvid-azure
.PHONY: test-e2e-document-embedding-gcp test-e2e-document-embedding-aws test-e2e-document-embedding-azure
.PHONY: test-e2e-large-image-embedding-gcp test-e2e-large-image-embedding-aws test-e2e-large-image-embedding-azure
.PHONY: test-e2e-image-dedupe-gcp test-e2e-image-dedupe-aws test-e2e-image-dedupe-azure
.PHONY: test-e2e-whisper-transcription-gcp test-e2e-whisper-transcription-aws test-e2e-whisper-transcription-azure
.PHONY: test-e2e-av-image-curation-gcp test-e2e-av-image-curation-aws test-e2e-av-image-curation-azure
.PHONY: test-e2e-onnx-audio
.PHONY: test-e2e-gcp test-e2e-aws test-e2e-azure
.PHONY: bench-e2e-large-image-embedding-gcp bench-e2e-large-image-embedding-aws bench-e2e-large-image-embedding-azure
.PHONY: upload-manifests-oxford-pets upload-manifests-openvid
.PHONY: upload-manifests-document-embedding upload-manifests-large-image-embedding
.PHONY: upload-manifests-whisper-transcription upload-manifests-image-dedupe
.PHONY: upload-manifests-av-image-curation dry-run-av-image-curation
.PHONY: dry-run-simple dry-run-openclip dry-run-blip dry-run-sentence-transformers dry-run-all
.PHONY: dry-run-openvid-simple dry-run-openvid-embedding-vjepa2 dry-run-openvid-all
.PHONY: dry-run-document-embedding dry-run-large-image-embedding dry-run-whisper-transcription
.PHONY: dry-run-image-dedupe

NUM_IMAGES ?= 100
BATCH_SIZE ?= 4
NUM_DOCS ?= 20
NUM_LARGE_IMAGES ?= 20
NUM_CLIPS ?= 5
ROW_LIMIT ?= 5
NUM_VIDEOS ?= 20

PYTEST_E2E = uv run -m pytest -c ../pytest.ini
COV_OPTS = --cov=../../src/geneva --cov-append -v -s --cov-report=term-missing --durations=0

# E2E Tests - Oxford Pets Suite
test-e2e-oxford-pets-gcp:
	cd e2e/oxford-pets && $(PYTEST_E2E) $(if $(TEST_FILES),$(TEST_FILES),test_drivers) --csp=gcp --test-slug=$(SLUG) --num-images=$(NUM_IMAGES) --batch-size=$(BATCH_SIZE) $(if $(SKIP_GPU),--skip-gpu) $(COV_OPTS)

test-e2e-oxford-pets-aws:
	cd e2e/oxford-pets && $(PYTEST_E2E) test_drivers --csp=aws --test-slug=$(SLUG) --num-images=$(NUM_IMAGES) --batch-size=$(BATCH_SIZE) $(if $(SKIP_GPU),--skip-gpu) $(COV_OPTS)

test-e2e-oxford-pets-azure:
	cd e2e/oxford-pets && $(PYTEST_E2E) test_drivers --csp=azure --test-slug=$(SLUG) --num-images=$(NUM_IMAGES) --batch-size=$(BATCH_SIZE) $(if $(SKIP_GPU),--skip-gpu) $(COV_OPTS)

# E2E Tests - OpenVid Suite
test-e2e-openvid-gcp:
	cd e2e/openvid && $(PYTEST_E2E) $(if $(TEST_FILES),$(TEST_FILES),test_drivers) --csp=gcp --test-slug=$(SLUG) --num-videos=$(NUM_VIDEOS) --batch-size=$(BATCH_SIZE) $(if $(SKIP_GPU),--skip-gpu) $(COV_OPTS)

test-e2e-openvid-aws:
	cd e2e/openvid && $(PYTEST_E2E) test_drivers --csp=aws --test-slug=$(SLUG) --num-videos=$(NUM_VIDEOS) --batch-size=$(BATCH_SIZE) $(if $(SKIP_GPU),--skip-gpu) $(COV_OPTS)

test-e2e-openvid-azure:
	cd e2e/openvid && $(PYTEST_E2E) test_drivers --csp=azure --test-slug=$(SLUG) --num-videos=$(NUM_VIDEOS) --batch-size=$(BATCH_SIZE) $(if $(SKIP_GPU),--skip-gpu) $(COV_OPTS)

test-e2e-openvid-azure:
	cd e2e/openvid && $(PYTEST_E2E) test_drivers --csp=azure --test-slug=$(SLUG) --num-videos=$(NUM_VIDEOS) --batch-size=$(BATCH_SIZE) $(if $(SKIP_GPU),--skip-gpu) $(if $(SOURCE_BUCKET),--source-bucket=$(SOURCE_BUCKET)) $(COV_OPTS)

# E2E Tests - Document Embedding Suite
test-e2e-document-embedding-gcp:
	cd e2e/document_embedding && $(PYTEST_E2E) $(if $(TEST_FILES),$(TEST_FILES),test_drivers) --csp=gcp --test-slug=$(SLUG) --num-docs=$(NUM_DOCS) --batch-size=$(BATCH_SIZE) $(COV_OPTS)

test-e2e-document-embedding-aws:
	cd e2e/document_embedding && $(PYTEST_E2E) test_drivers --csp=aws --test-slug=$(SLUG) --num-docs=$(NUM_DOCS) --batch-size=$(BATCH_SIZE) $(COV_OPTS)

test-e2e-document-embedding-azure:
	cd e2e/document_embedding && $(PYTEST_E2E) test_drivers --csp=azure --test-slug=$(SLUG) --num-docs=$(NUM_DOCS) --batch-size=$(BATCH_SIZE) $(COV_OPTS)

# E2E Tests - Large Image Embedding Suite
test-e2e-large-image-embedding-gcp:
	cd e2e/large_image_embedding && $(PYTEST_E2E) $(if $(TEST_FILES),$(TEST_FILES),test_drivers) --csp=gcp --test-slug=$(SLUG) --num-images=$(NUM_LARGE_IMAGES) --batch-size=$(BATCH_SIZE) $(COV_OPTS)

test-e2e-large-image-embedding-aws:
	cd e2e/large_image_embedding && $(PYTEST_E2E) test_drivers --csp=aws --test-slug=$(SLUG) --num-images=$(NUM_LARGE_IMAGES) --batch-size=$(BATCH_SIZE) $(COV_OPTS)

test-e2e-large-image-embedding-azure:
	cd e2e/large_image_embedding && $(PYTEST_E2E) test_drivers --csp=azure --test-slug=$(SLUG) --num-images=$(NUM_LARGE_IMAGES) --batch-size=$(BATCH_SIZE) $(COV_OPTS)

# E2E Tests - Image Dedupe Suite
test-e2e-image-dedupe-gcp:
	cd e2e/image_dedupe && $(PYTEST_E2E) $(if $(TEST_FILES),$(TEST_FILES),test_drivers) --csp=gcp --test-slug=$(SLUG) --num-images=$(NUM_IMAGES) $(COV_OPTS)

test-e2e-image-dedupe-aws:
	cd e2e/image_dedupe && $(PYTEST_E2E) test_drivers --csp=aws --test-slug=$(SLUG) --num-images=$(NUM_IMAGES) $(COV_OPTS)

test-e2e-image-dedupe-azure:
	cd e2e/image_dedupe && $(PYTEST_E2E) test_drivers --csp=azure --test-slug=$(SLUG) --num-images=$(NUM_IMAGES) $(COV_OPTS)

# E2E Tests - Whisper Transcription Suite
test-e2e-whisper-transcription-gcp:
	cd e2e/whisper_transcription && $(PYTEST_E2E) $(if $(TEST_FILES),$(TEST_FILES),test_drivers) --csp=gcp --test-slug=$(SLUG) $(if $(ROW_LIMIT),--row-limit=$(ROW_LIMIT),) $(if $(NUM_CLIPS),--num-clips=$(NUM_CLIPS),) --checkpoint-size=$(or $(CHECKPOINT_SIZE),$(BATCH_SIZE)) $(if $(SKIP_GPU),--skip-gpu) $(COV_OPTS)

test-e2e-whisper-transcription-aws:
	cd e2e/whisper_transcription && $(PYTEST_E2E) test_drivers --csp=aws --test-slug=$(SLUG) $(if $(ROW_LIMIT),--row-limit=$(ROW_LIMIT),) $(if $(NUM_CLIPS),--num-clips=$(NUM_CLIPS),) --checkpoint-size=$(or $(CHECKPOINT_SIZE),$(BATCH_SIZE)) $(if $(SKIP_GPU),--skip-gpu) $(COV_OPTS)

test-e2e-whisper-transcription-azure:
	cd e2e/whisper_transcription && $(PYTEST_E2E) test_drivers --csp=azure --test-slug=$(SLUG) $(if $(ROW_LIMIT),--row-limit=$(ROW_LIMIT),) $(if $(NUM_CLIPS),--num-clips=$(NUM_CLIPS),) --checkpoint-size=$(or $(CHECKPOINT_SIZE),$(BATCH_SIZE)) $(if $(SKIP_GPU),--skip-gpu) $(COV_OPTS)

# E2E Tests - AV Image Curation Suite
test-e2e-av-image-curation-gcp:
	cd e2e/av_image_curation && $(PYTEST_E2E) $(if $(TEST_FILES),$(TEST_FILES),test_drivers) --csp=gcp --test-slug=$(SLUG) --num-images=$(NUM_IMAGES) --batch-size=$(BATCH_SIZE) $(if $(SKIP_GPU),--skip-gpu) $(COV_OPTS)

test-e2e-av-image-curation-aws:
	cd e2e/av_image_curation && $(PYTEST_E2E) $(if $(TEST_FILES),$(TEST_FILES),test_drivers) --csp=aws --test-slug=$(SLUG) --num-images=$(NUM_IMAGES) --batch-size=$(BATCH_SIZE) $(if $(SKIP_GPU),--skip-gpu) $(COV_OPTS)

test-e2e-av-image-curation-azure:
	cd e2e/av_image_curation && $(PYTEST_E2E) $(if $(TEST_FILES),$(TEST_FILES),test_drivers) --csp=azure --test-slug=$(SLUG) --num-images=$(NUM_IMAGES) --batch-size=$(BATCH_SIZE) $(if $(SKIP_GPU),--skip-gpu) $(COV_OPTS)

# E2E Tests - ONNX Audio Suite (local)
test-e2e-onnx-audio:
	cd e2e/onnx_audio && $(PYTEST_E2E) $(if $(TEST_FILES),$(TEST_FILES),test_drivers) $(COV_OPTS)

# E2E Benchmarks - Large Image Embedding
bench-e2e-large-image-embedding-gcp:
	RAY_ENABLE_UV_RUN_RUNTIME_ENV=0 uv run -m e2e.large_image_embedding.benchmarks.geneva_main \
		--csp=gcp \
		--slug=$(SLUG) \
		$(if $(BUCKET_PATH),--bucket=$(BUCKET_PATH)) \
		$(if $(CLUSTER_NAME),--cluster-name=$(CLUSTER_NAME)) \
		$(if $(DATASET_PATH),--dataset-path="$(DATASET_PATH)") \
		$(if $(filter 0 false FALSE,$(FRESH_RUN)),--no-fresh-run) \
		$(if $(filter 1 true TRUE,$(USE_MERGED_PREPROCESS)),--use-merged-preprocess) \
		$(if $(filter 1 true TRUE,$(SKIP_GPU)),--skip-gpu) \
		--num-images=$(or $(NUM_BENCH_IMAGES),300) \
		--min-checkpoint-size=$(or $(MIN_CHECKPOINT_SIZE),1) \
		--max-checkpoint-size=$(or $(MAX_CHECKPOINT_SIZE),512) \
		$(if $(TASK_SIZE),--task-size=$(TASK_SIZE)) \
		--num-cpu-workers=$(or $(NUM_CPU_WORKERS),5) \
		--num-gpu-workers=$(or $(NUM_GPU_WORKERS),5) \
		--intra-applier-concurrency=$(or $(INTRA_APPLIER_CONCURRENCY),1) \
		$(if $(MANIFEST_NAME),--manifest-name=$(MANIFEST_NAME))

bench-e2e-large-image-embedding-aws:
	RAY_ENABLE_UV_RUN_RUNTIME_ENV=0 uv run -m e2e.large_image_embedding.benchmarks.geneva_main \
		--csp=aws \
		--slug=$(SLUG) \
		$(if $(BUCKET_PATH),--bucket=$(BUCKET_PATH)) \
		$(if $(CLUSTER_NAME),--cluster-name=$(CLUSTER_NAME)) \
		$(if $(DATASET_PATH),--dataset-path="$(DATASET_PATH)") \
		$(if $(filter 0 false FALSE,$(FRESH_RUN)),--no-fresh-run) \
		$(if $(filter 1 true TRUE,$(USE_MERGED_PREPROCESS)),--use-merged-preprocess) \
		$(if $(filter 1 true TRUE,$(SKIP_GPU)),--skip-gpu) \
		--num-images=$(or $(NUM_BENCH_IMAGES),300) \
		--min-checkpoint-size=$(or $(MIN_CHECKPOINT_SIZE),1) \
		--max-checkpoint-size=$(or $(MAX_CHECKPOINT_SIZE),512) \
		$(if $(TASK_SIZE),--task-size=$(TASK_SIZE)) \
		--num-cpu-workers=$(or $(NUM_CPU_WORKERS),5) \
		--num-gpu-workers=$(or $(NUM_GPU_WORKERS),5) \
		--intra-applier-concurrency=$(or $(INTRA_APPLIER_CONCURRENCY),1) \
		$(if $(MANIFEST_NAME),--manifest-name=$(MANIFEST_NAME))

bench-e2e-large-image-embedding-azure:
	RAY_ENABLE_UV_RUN_RUNTIME_ENV=0 uv run -m e2e.large_image_embedding.benchmarks.geneva_main \
		--csp=azure \
		--slug=$(SLUG) \
		$(if $(BUCKET_PATH),--bucket=$(BUCKET_PATH)) \
		$(if $(CLUSTER_NAME),--cluster-name=$(CLUSTER_NAME)) \
		$(if $(DATASET_PATH),--dataset-path="$(DATASET_PATH)") \
		$(if $(filter 0 false FALSE,$(FRESH_RUN)),--no-fresh-run) \
		$(if $(filter 1 true TRUE,$(USE_MERGED_PREPROCESS)),--use-merged-preprocess) \
		$(if $(filter 1 true TRUE,$(SKIP_GPU)),--skip-gpu) \
		--num-images=$(or $(NUM_BENCH_IMAGES),300) \
		--min-checkpoint-size=$(or $(MIN_CHECKPOINT_SIZE),1) \
		--max-checkpoint-size=$(or $(MAX_CHECKPOINT_SIZE),512) \
		$(if $(TASK_SIZE),--task-size=$(TASK_SIZE)) \
		--num-cpu-workers=$(or $(NUM_CPU_WORKERS),5) \
		--num-gpu-workers=$(or $(NUM_GPU_WORKERS),5) \
		--intra-applier-concurrency=$(or $(INTRA_APPLIER_CONCURRENCY),1) \
		$(if $(MANIFEST_NAME),--manifest-name=$(MANIFEST_NAME))

# Convenience targets
test-e2e-gcp: test-e2e-oxford-pets-gcp test-e2e-openvid-gcp test-e2e-document-embedding-gcp test-e2e-large-image-embedding-gcp test-e2e-whisper-transcription-gcp test-e2e-image-dedupe-gcp test-e2e-av-image-curation-gcp

test-e2e-aws: test-e2e-oxford-pets-aws test-e2e-openvid-aws test-e2e-document-embedding-aws test-e2e-large-image-embedding-aws test-e2e-whisper-transcription-aws test-e2e-image-dedupe-aws test-e2e-av-image-curation-aws

test-e2e-azure: test-e2e-oxford-pets-azure test-e2e-openvid-azure test-e2e-document-embedding-azure test-e2e-large-image-embedding-azure test-e2e-whisper-transcription-azure test-e2e-image-dedupe-azure test-e2e-av-image-curation-azure

# E2E Suite-Level Manifest Uploads
upload-manifests-oxford-pets:
	cd e2e/oxford-pets && uv run python upload_manifests.py --bucket $(E2E_DRY_RUN_BUCKET)

upload-manifests-openvid:
	cd e2e/openvid && uv run python upload_manifests.py --bucket $(E2E_DRY_RUN_BUCKET)

upload-manifests-document-embedding:
	cd e2e/document_embedding && uv run python upload_manifests.py --bucket $(E2E_DRY_RUN_BUCKET)

upload-manifests-large-image-embedding:
	cd e2e/large_image_embedding && uv run python upload_manifests.py --bucket $(E2E_DRY_RUN_BUCKET)

upload-manifests-whisper-transcription:
	cd e2e/whisper_transcription && uv run python upload_manifests.py --bucket $(E2E_DRY_RUN_BUCKET)

upload-manifests-image-dedupe:
	cd e2e/image_dedupe && uv run python upload_manifests.py --bucket $(E2E_DRY_RUN_BUCKET)

upload-manifests-av-image-curation:
	cd e2e/av_image_curation && uv run python upload_manifests.py --bucket $(E2E_DRY_RUN_BUCKET)

# E2E Tests - Manifest Dry Run (local testing)
dry-run-simple:
	cd e2e/oxford-pets && uv run python upload_manifests.py --bucket $(E2E_DRY_RUN_BUCKET) --profile simple --dry-run --verbose --generate-zip

dry-run-openclip:
	cd e2e/oxford-pets && uv run python upload_manifests.py --bucket $(E2E_DRY_RUN_BUCKET) --profile openclip --dry-run --verbose --generate-zip

dry-run-blip:
	cd e2e/oxford-pets && uv run python upload_manifests.py --bucket $(E2E_DRY_RUN_BUCKET) --profile blip --dry-run --verbose --generate-zip

dry-run-sentence-transformers:
	cd e2e/oxford-pets && uv run python upload_manifests.py --bucket $(E2E_DRY_RUN_BUCKET) --profile sentence-transformers --dry-run --verbose --generate-zip

dry-run-all: dry-run-simple dry-run-openclip dry-run-blip dry-run-sentence-transformers

dry-run-openvid-simple:
	cd e2e/openvid && uv run python upload_manifests.py --bucket $(E2E_DRY_RUN_BUCKET) --profile simple --dry-run --verbose --generate-zip

dry-run-openvid-embedding-vjepa2:
	cd e2e/openvid && uv run python upload_manifests.py --bucket $(E2E_DRY_RUN_BUCKET) --profile embedding_vjepa2 --dry-run --verbose --generate-zip

dry-run-openvid-all: dry-run-openvid-simple dry-run-openvid-embedding-vjepa2

dry-run-document-embedding:
	cd e2e/document_embedding && uv run python upload_manifests.py --bucket $(E2E_DRY_RUN_BUCKET) --profile pdf_embedding --dry-run --verbose --generate-zip

dry-run-large-image-embedding:
	cd e2e/large_image_embedding && uv run python upload_manifests.py --bucket $(E2E_DRY_RUN_BUCKET) --profile vit_image --dry-run --verbose --generate-zip

dry-run-whisper-transcription:
	cd e2e/whisper_transcription && uv run python upload_manifests.py --bucket $(E2E_DRY_RUN_BUCKET) --profile whisper_transcription --dry-run --verbose --generate-zip

dry-run-image-dedupe:
	cd e2e/image_dedupe && uv run python upload_manifests.py --bucket $(E2E_DRY_RUN_BUCKET) --profile image-hash --dry-run --verbose --generate-zip

dry-run-av-image-curation:
	cd e2e/av_image_curation && uv run python upload_manifests.py --bucket $(E2E_DRY_RUN_BUCKET) --profile av-curation --dry-run --verbose --generate-zip
