pub use net_provider_global::NetworkProviderGlobal;

use super::NetworkProvider;
#[cfg(feature = "custom_network_provider")]
use net_provider_noop::NetworkProviderNoop;
use std::sync::{Arc, Weak};

#[cfg(not(feature = "custom_network_provider"))]
pub mod net_provider_reqwest;

#[cfg(not(feature = "custom_network_provider"))]
mod event_upload_registry;
mod net_provider_global;
#[cfg(feature = "custom_network_provider")]
mod net_provider_noop;

#[cfg(feature = "custom_network_provider")]
lazy_static::lazy_static! {
    static ref NOOP_NETWORK_PROVIDER: Arc<dyn NetworkProvider> = Arc::new(NetworkProviderNoop {});
}

#[cfg(not(feature = "custom_network_provider"))]
lazy_static::lazy_static! {
    static ref REQWEST_NETWORK_PROVIDER: Arc<net_provider_reqwest::NetworkProviderReqwest> = Arc::new(net_provider_reqwest::NetworkProviderReqwest::new());
}

#[cfg(feature = "custom_network_provider")]
pub fn get_network_provider() -> Weak<dyn NetworkProvider> {
    NetworkProviderGlobal::try_get().unwrap_or_else(|| Arc::downgrade(&NOOP_NETWORK_PROVIDER))
}

#[cfg(not(feature = "custom_network_provider"))]
pub fn get_network_provider() -> Weak<dyn NetworkProvider> {
    get_reqwest_network_provider()
}

#[cfg(not(feature = "custom_network_provider"))]
pub(super) fn get_reqwest_network_provider() -> Weak<net_provider_reqwest::NetworkProviderReqwest> {
    Arc::downgrade(&REQWEST_NETWORK_PROVIDER)
}

#[cfg(not(feature = "custom_network_provider"))]
pub(super) fn get_event_upload_transport() -> Arc<net_provider_reqwest::EventUploadTransport> {
    event_upload_registry::get()
}

#[cfg(not(feature = "custom_network_provider"))]
pub(crate) fn reset_event_upload_transport(
    previous_global: &Arc<crate::statsig_global::StatsigGlobal>,
) {
    event_upload_registry::reset(previous_global);
}
