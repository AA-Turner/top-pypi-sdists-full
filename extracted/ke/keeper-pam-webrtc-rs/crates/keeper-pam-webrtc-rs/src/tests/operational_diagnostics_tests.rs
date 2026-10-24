use guacr_handlers::operational_diagnostics::TARGET;
use serde_json::Value;
use std::{fmt, sync::Arc};
use tracing_subscriber::layer::SubscriberExt;

const SECRET: &str = "SELECT 'private-credential-37' /* private-comment-91 */ FROM secret_table";
struct MustNotFormat;
impl fmt::Debug for MustNotFormat {
    fn fmt(&self, _: &mut fmt::Formatter<'_>) -> fmt::Result {
        panic!("private Debug must not be formatted")
    }
}
#[cfg(feature = "python-support")]
#[test]
fn channel_layer_captures_failure_once_with_static_metadata() {
    use crate::operational_diagnostics::ChannelLayer;
    use crate::python::channel_logger::create_channel_logger;
    let (logger, mut receiver) = create_channel_logger(log::LevelFilter::Trace);
    let subscriber = tracing_subscriber::registry().with(ChannelLayer(Arc::new(logger)));
    tracing::subscriber::with_default(subscriber, || {
        tracing::error!(target: "guacr_database::diagnostics", operation = "query",
            outcome = "failed", error_code = 43_i64, elapsed_ms = 4_u64,
            error = SECRET, bind_count = ?MustNotFormat);
        tracing::error!(target: "keeper_pam_webrtc_rs::channel::handler_connections",
            operation = "lifecycle", outcome = "failed", error_code = 44_i64,
            errno = 5_i64, error = ?MustNotFormat);
        tracing::info!(target: "application", "operational startup");
    });
    let record = receiver.try_recv().unwrap();
    assert_eq!(record.target, TARGET);
    assert_eq!(record.level, log::Level::Error);
    assert!(record.file.is_some());
    assert!(record.line.is_some());
    let diagnostic: Value = serde_json::from_str(&record.message).unwrap();
    assert_eq!(diagnostic["error_code"], 43);
    assert_eq!(diagnostic["elapsed_ms"], 4);
    assert_eq!(diagnostic["outcome"], "failed");
    assert!(!record.message.contains("private"));
    let handler = receiver.try_recv().unwrap();
    let diagnostic: Value = serde_json::from_str(&handler.message).unwrap();
    assert_eq!(handler.level, log::Level::Error);
    assert_eq!(diagnostic["source"], "handler");
    assert_eq!(diagnostic["error_code"], 44);
    assert_eq!(diagnostic["errno"], 5);
    let operational = receiver.try_recv().unwrap();
    assert_eq!(operational.target, "application");
    assert_eq!(operational.message, "operational startup");
    assert!(receiver.try_recv().is_err());
}

#[cfg(feature = "python-support")]
#[test]
fn legacy_channel_never_owns_statement_or_unknown_debug() {
    use crate::python::channel_logger::create_channel_logger;
    use log::Log;
    let (logger, mut receiver) = create_channel_logger(log::LevelFilter::Trace);
    logger.log(
        &log::Record::builder()
            .target("sqlx::query")
            .level(log::Level::Debug)
            .args(format_args!("{}", SECRET))
            .file_static(Some(file!()))
            .line(Some(line!()))
            .build(),
    );
    logger.log(
        &log::Record::builder()
            .target("keeperdb_core::driver")
            .level(log::Level::Error)
            .args(format_args!("{:?}", MustNotFormat))
            .build(),
    );
    for level in [log::Level::Debug, log::Level::Error] {
        let record = receiver.try_recv().unwrap();
        assert_eq!(record.target, "keeper_pam_diagnostics");
        assert_eq!(record.level, level);
        assert!(!record.message.contains("private"));
        let diagnostic: Value = serde_json::from_str(&record.message).unwrap();
        assert_eq!(diagnostic["details_omitted"], true);
        assert_eq!(diagnostic["content_omitted"], true);
    }
    assert!(receiver.try_recv().is_err());
}
