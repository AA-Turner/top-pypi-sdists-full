use crate::StatsigOptions;

pub(crate) fn http2_enabled(options: Option<&StatsigOptions>) -> bool {
    options
        .and_then(|options| options.prefer_http2)
        .unwrap_or(true)
}
