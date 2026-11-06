use super::*;
use crate::sdk_diagnostics::marker::ActionType;
use crate::{EventLoggingAdapter, StatsigHttpEventLoggingAdapter, StatsigOptions, StatsigRuntime};

#[tokio::test]
async fn diagnostics_only_retains_state_and_logger_when_reporting_is_enabled() {
    for disabled in [None, Some(false), Some(true)] {
        let instance_id = format!("diagnostics-state-{disabled:?}");
        let options = Arc::new(StatsigOptions {
            sdk_instance_id: Some(instance_id.clone()),
            disable_remote_telemetry: disabled,
            disable_network: Some(true),
            ..StatsigOptions::default()
        });
        let adapter: Arc<dyn EventLoggingAdapter> = Arc::new(StatsigHttpEventLoggingAdapter::new(
            "secret-state-fixture",
            Some(&options),
        ));
        let logger = EventLogger::new(
            "secret-state-fixture",
            &options,
            &adapter,
            &StatsigRuntime::get_runtime(),
        );
        let owners_before = Arc::strong_count(&logger);
        let diagnostics = Diagnostics::new(logger.clone(), &instance_id);
        let enabled = disabled != Some(true);
        assert_eq!(diagnostics.state.is_some(), enabled);
        assert_eq!(
            Arc::strong_count(&logger),
            owners_before + usize::from(enabled)
        );
        diagnostics.add_marker(None, Marker::new(KeyType::Overall, ActionType::Start, None));
        assert_eq!(
            diagnostics.get_markers(&ContextType::Initialize).is_some(),
            enabled
        );
        assert_eq!(
            diagnostics.should_sample(&ContextType::Initialize, None),
            enabled
        );
        logger.shutdown().await.unwrap();
    }
}
