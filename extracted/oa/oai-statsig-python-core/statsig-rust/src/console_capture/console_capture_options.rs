use crate::{StatsigUser, console_capture::console_log_line_levels::StatsigLogLineLevel};

#[derive(Clone, Default)]
pub struct ConsoleCaptureOptions {
    pub enabled: bool,
    pub log_levels: Option<Vec<StatsigLogLineLevel>>,
    pub user: Option<StatsigUser>,
    pub max_keys: Option<u64>,
    pub max_depth: Option<u64>,
    pub max_length: Option<u64>,
}
