use guacr_handlers::operational_diagnostics::{project_event, TARGET};
use tracing::{Event, Metadata, Subscriber};
use tracing_subscriber::fmt::format::{DefaultFields, FormatFields, Writer};
#[cfg(feature = "python-support")]
pub(crate) struct ChannelLayer(pub std::sync::Arc<crate::python::channel_logger::ChannelLogger>);

#[cfg(feature = "python-support")]
impl<S: Subscriber> tracing_subscriber::Layer<S> for ChannelLayer {
    fn enabled(
        &self,
        metadata: &Metadata<'_>,
        _: tracing_subscriber::layer::Context<'_, S>,
    ) -> bool {
        self.0.level_enabled(tracing_log_level(metadata.level()))
    }

    fn on_event(&self, event: &Event<'_>, _: tracing_subscriber::layer::Context<'_, S>) {
        let metadata = event.metadata();
        if !self.0.level_enabled(tracing_log_level(metadata.level())) {
            return;
        }
        let projected = project_event(event);
        let (target, message) = if let Some(message) = projected {
            (TARGET, message)
        } else {
            let mut message = String::new();
            let _ = DefaultFields::new().format_fields(Writer::new(&mut message), event);
            (metadata.target(), message)
        };
        // Direct transport, not log!, avoids LogTracer recursion and duplicate fallback.
        self.0.send(crate::python::channel_logger::LogRecord {
            level: tracing_log_level(metadata.level()),
            target: target.into(),
            message,
            module_path: metadata.module_path().map(String::from),
            file: metadata.file().map(String::from),
            line: metadata.line(),
        });
    }
}

#[cfg(feature = "python-support")]
fn tracing_log_level(level: &tracing::Level) -> log::Level {
    match *level {
        tracing::Level::ERROR => log::Level::Error,
        tracing::Level::WARN => log::Level::Warn,
        tracing::Level::INFO => log::Level::Info,
        tracing::Level::DEBUG => log::Level::Debug,
        _ => log::Level::Trace,
    }
}
