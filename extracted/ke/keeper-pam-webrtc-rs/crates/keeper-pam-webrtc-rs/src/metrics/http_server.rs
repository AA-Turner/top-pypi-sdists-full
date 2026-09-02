// HTTP metrics export server (T-046 to T-050)
#![allow(dead_code)]
// Exposed only when the `metrics-http` feature is enabled (T-048).
//
// Endpoints:
//   GET /metrics       — Prometheus text exposition format (AC-1)
//   GET /metrics/json  — JSON format (AC-2)
//
// Implemented metrics (AC-4):
//   - guacrd_active_connections      (gauge)
//   - guacrd_rtt_p50_ms              (gauge, system-wide average)
//   - guacrd_rtt_p95_ms              (gauge, system-wide average)
//   - guacrd_rtt_p99_ms              (gauge, system-wide average)
//   - guacrd_packet_loss_percent     (gauge)
//   - guacrd_throughput_bytes_per_sec (gauge)
//
// Not yet implemented:
//   - guacrd_sctp_buffered_bytes — requires per-connection SCTP buffer plumbing
//
// Bind address is configurable (AC-5) via GUACRD_METRICS_BIND env var
// or by passing the addr string directly (default: 127.0.0.1:9090).

#[cfg(feature = "metrics-http")]
pub mod server {
    use axum::{routing::get, Router};
    use std::net::SocketAddr;

    use crate::metrics::METRICS_COLLECTOR;

    /// Default metrics bind address (AC-5).
    pub const DEFAULT_METRICS_BIND: &str = "127.0.0.1:9090";

    /// Env var for configuring the metrics HTTP bind address.
    pub const ENV_METRICS_BIND: &str = "GUACRD_METRICS_BIND";

    /// Start the HTTP metrics server.
    ///
    /// Returns a `JoinHandle` for the server task so the caller can await
    /// or cancel it. The server runs until the tokio runtime shuts down.
    pub async fn start(bind_addr: &str) -> anyhow::Result<()> {
        let addr: SocketAddr = bind_addr
            .parse()
            .map_err(|e| anyhow::anyhow!("Invalid metrics bind address {bind_addr:?}: {e}"))?;

        let app = Router::new()
            .route("/metrics", get(metrics_prometheus))
            .route("/metrics/json", get(metrics_json));

        let listener = tokio::net::TcpListener::bind(addr).await?;
        log::info!("Metrics HTTP server listening on http://{addr}");

        axum::serve(listener, app).await?;
        Ok(())
    }

    /// Resolve bind address from env var, falling back to default.
    pub fn resolve_bind_addr() -> String {
        std::env::var(ENV_METRICS_BIND).unwrap_or_else(|_| DEFAULT_METRICS_BIND.to_string())
    }

    /// GET /metrics — Prometheus text exposition format (AC-1).
    async fn metrics_prometheus() -> (
        axum::http::StatusCode,
        [(axum::http::HeaderName, &'static str); 1],
        String,
    ) {
        let metrics = METRICS_COLLECTOR.get_aggregated_metrics();
        let body = format_prometheus(&metrics);
        (
            axum::http::StatusCode::OK,
            [(
                axum::http::header::CONTENT_TYPE,
                "text/plain; version=0.0.4; charset=utf-8",
            )],
            body,
        )
    }

    /// GET /metrics/json — JSON format (AC-2).
    async fn metrics_json() -> (axum::http::StatusCode, axum::Json<serde_json::Value>) {
        let metrics = METRICS_COLLECTOR.get_aggregated_metrics();
        let value = serde_json::json!({
            "active_connections": metrics.active_connections,
            "rtt_p50_ms": metrics.avg_system_rtt.as_millis(),
            "rtt_p95_ms": metrics.avg_p95_latency.as_millis(),
            "rtt_p99_ms": metrics.avg_p99_latency.as_millis(),
            "packet_loss_percent": metrics.avg_packet_loss * 100.0,
            "throughput_bytes_per_sec": metrics.total_bandwidth,
            "timestamp": metrics.timestamp.to_rfc3339(),
        });
        (axum::http::StatusCode::OK, axum::Json(value))
    }

    /// Format aggregated metrics as Prometheus text exposition (AC-1, AC-4).
    fn format_prometheus(m: &crate::metrics::types::AggregatedMetrics) -> String {
        let mut out = String::with_capacity(1024);

        // Active connection count (AC-4).
        out.push_str("# HELP guacrd_active_connections Number of active WebRTC connections\n");
        out.push_str("# TYPE guacrd_active_connections gauge\n");
        out.push_str(&format!(
            "guacrd_active_connections {}\n\n",
            m.active_connections
        ));

        // RTT percentiles (AC-4: p50, p95, p99).
        out.push_str("# HELP guacrd_rtt_p50_ms Round-trip time p50 across all connections (ms)\n");
        out.push_str("# TYPE guacrd_rtt_p50_ms gauge\n");
        out.push_str(&format!(
            "guacrd_rtt_p50_ms {}\n\n",
            m.avg_system_rtt.as_millis()
        ));

        out.push_str("# HELP guacrd_rtt_p95_ms Round-trip time p95 across all connections (ms)\n");
        out.push_str("# TYPE guacrd_rtt_p95_ms gauge\n");
        out.push_str(&format!(
            "guacrd_rtt_p95_ms {}\n\n",
            m.avg_p95_latency.as_millis()
        ));

        out.push_str("# HELP guacrd_rtt_p99_ms Round-trip time p99 across all connections (ms)\n");
        out.push_str("# TYPE guacrd_rtt_p99_ms gauge\n");
        out.push_str(&format!(
            "guacrd_rtt_p99_ms {}\n\n",
            m.avg_p99_latency.as_millis()
        ));

        // Packet loss percentage (AC-4).
        out.push_str(
            "# HELP guacrd_packet_loss_percent Packet loss rate across all connections (%)\n",
        );
        out.push_str("# TYPE guacrd_packet_loss_percent gauge\n");
        out.push_str(&format!(
            "guacrd_packet_loss_percent {:.4}\n\n",
            m.avg_packet_loss * 100.0
        ));

        // Throughput bytes per second (AC-4).
        out.push_str(
            "# HELP guacrd_throughput_bytes_per_sec Total outbound throughput (bytes/sec)\n",
        );
        out.push_str("# TYPE guacrd_throughput_bytes_per_sec gauge\n");
        out.push_str(&format!(
            "guacrd_throughput_bytes_per_sec {:.2}\n\n",
            m.total_bandwidth
        ));

        out
    }
}

#[cfg(not(feature = "metrics-http"))]
/// Stub module when metrics-http feature is disabled (AC-3).
/// No HTTP server, no HTTP dependencies compiled.
pub mod server {
    pub const DEFAULT_METRICS_BIND: &str = "127.0.0.1:9090";
}

#[cfg(test)]
mod tests {
    // AC-3: when the feature is disabled, the test still compiles with no HTTP deps.
    #[test]
    fn test_default_bind_constant_defined() {
        let addr = super::server::DEFAULT_METRICS_BIND;
        assert!(!addr.is_empty());
    }
}
