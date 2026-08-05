mod http_types;
mod network_client;
pub mod network_error;
pub mod providers;
pub mod proxy_config;
mod statsig_url;

pub use http_types::*;
pub use network_client::*;
pub use network_error::*;
#[cfg(not(feature = "custom_network_provider"))]
pub(crate) use statsig_url::url_path_has_suffix;
pub(crate) use statsig_url::{
    DEFAULT_CDN_ID_LISTS_MANIFEST_URL_PREFIX, DEFAULT_CDN_SPECS_URL, api_from_url,
    config_specs_url, default_cdn_id_lists_manifest_url, get_source_service_and_request_path,
    is_default_cdn_id_lists_manifest_url, is_default_cdn_url,
    normalize_default_cdn_id_lists_manifest_url, replace_url_base,
    should_log_network_request_latency,
};

#[cfg(test)]
mod __tests__;
