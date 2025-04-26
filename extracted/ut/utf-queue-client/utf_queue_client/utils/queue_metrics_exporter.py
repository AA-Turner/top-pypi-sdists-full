import gzip
import zlib
from io import BytesIO

from opentelemetry.exporter.otlp.proto.http import Compression
from opentelemetry.exporter.otlp.proto.http.metric_exporter import (
    MetricExportResult,
    MetricsData,
    OTLPMetricExporter,
)
from opentelemetry.sdk.metrics.export import (
    InMemoryMetricReader,
)
from otel_extensions import TelemetryOptions

from utf_queue_client.clients.opentelemetry_data_producer import (
    OpenTelemetryDataProducer,
)

__all__ = ["QUEUE_METRICS_EXPORTER_TYPE_NAME", "QueueMetricsExporter"]

QUEUE_METRICS_EXPORTER_TYPE_NAME = (
    "utf_queue_client.utils.queue_metrics_exporter.QueueMetricsExporter"
)


class QueueMetricsExporter(OTLPMetricExporter):
    def __init__(self, options: TelemetryOptions):
        super().__init__()
        self.reader = InMemoryMetricReader()
        self.producer = OpenTelemetryDataProducer(
            url=options.OTEL_EXPORTER_OTLP_ENDPOINT,
            producer_app_id="QueueMetricsExporter",
        )

    @property
    def compression(self):
        return (
            self._compression.value
            if self._compression != Compression.NoCompression
            else None
        )

    def get_reader(self):
        return self.reader

    def read_and_export(
        self, timeout_millis: float = 10_000, **kwargs
    ) -> MetricExportResult:
        return self.export(
            self.reader.get_metrics_data(), timeout_millis=timeout_millis, **kwargs
        )

    def encode_metrics(self, metrics_data: MetricsData):
        try:
            # This will work with opentelemetry-distro[otlp] 0.39b0 and later
            from opentelemetry.exporter.otlp.proto.common.metrics_encoder import (
                encode_metrics,
            )

            return encode_metrics(metrics_data).SerializeToString()

        except ImportError:
            # This will work with opentelemetry-distro[otlp] 0.38b0 and before
            return self._translate_data(metrics_data).SerializeToString()

    def export(
        self,
        metrics_data: MetricsData,
        timeout_millis: float = 10_000,
        **kwargs,
    ) -> MetricExportResult:
        data = self.encode_metrics(metrics_data)
        if isinstance(data, str):
            data = data.encode()
        if self.compression == Compression.Gzip.value:
            gzip_data = BytesIO()
            with gzip.GzipFile(fileobj=gzip_data, mode="w") as gzip_stream:
                gzip_stream.write(data)
            data = gzip_data.getvalue()
        elif self.compression == Compression.Deflate.value:
            data = zlib.compress(data)
        try:
            self.producer.publish_telemetry_data("METRICS", data, self.compression)
            return MetricExportResult.SUCCESS
        except Exception:
            return MetricExportResult.FAILURE
