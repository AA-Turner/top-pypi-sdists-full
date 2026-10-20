import os

CONNECTOR_SDK_CAPTURE_PERFORMANCE_METRICS = "CONNECTOR_SDK_CAPTURE_PERFORMANCE_METRICS"
CAPTURE_PERFORMANCE_METRICS_ENABLED = os.environ.get(CONNECTOR_SDK_CAPTURE_PERFORMANCE_METRICS, "false").lower() == "true"
NANOS_PER_MILLI = 1_000_000

# gRPC trailing-metadata keys for performance metrics; must match SdkPerformanceMetrics on the Java side
SDK_BUILD_NS = "x-ft-sdk-build-ns"
QUEUE_WAIT_NS = "x-ft-queue-wait-ns"
SDK_ASSEMBLY_NS = "x-ft-sdk-assembly-ns"
QUEUE_BACKPRESSURE_NS = "x-ft-queue-backpressure-ns"
CHECKPOINT_WAIT_NS = "x-ft-checkpoint-wait-ns"
GRPC_FIRST_SEND_MS = "x-ft-grpc-first-send-ms"
GRPC_SEND_RELATIVE_TOTAL_MS = "x-ft-grpc-send-relative-total-ms"
GRPC_SEND_COUNT = "x-ft-grpc-send-count"
GRPC_TIMESTAMP_OVERFLOW = "x-ft-grpc-timestamp-overflow"
PRODUCER_WALL_NS = "x-ft-producer-wall-ns"
