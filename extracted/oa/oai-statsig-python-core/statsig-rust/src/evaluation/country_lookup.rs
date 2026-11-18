use super::{dynamic_string::DynamicString, evaluator_context::EvaluatorContext};
use crate::{DynamicValue, dyn_value, log_d, log_e, user::StatsigUserInternal};
use std::sync::atomic::{AtomicBool, Ordering};

#[cfg(target_arch = "x86_64")]
#[path = "country_lookup_simd.rs"]
mod simd;

pub struct CountryLookup;

static COUNTRY_LOOKUP_LOADED: AtomicBool = AtomicBool::new(false);
const COUNTRY_CODES: &str = include_str!(concat!(env!("OUT_DIR"), "/country_codes"));
const COUNTRY_RANGES: &[[u8; 4]] = include_bytes!(concat!(env!("OUT_DIR"), "/country_ranges"))
    .as_chunks()
    .0;

lazy_static::lazy_static! {
    static ref IP: String = "ip".to_string();
}

const TAG: &str = "CountryLookup";
const UNINITIALIZED_REASON: &str = "CountryLookupNotLoaded";

impl CountryLookup {
    pub(crate) fn is_loaded() -> bool {
        COUNTRY_LOOKUP_LOADED.load(Ordering::Relaxed)
    }

    pub fn load_country_lookup() {
        if !COUNTRY_LOOKUP_LOADED.swap(true, Ordering::Relaxed) {
            log_d!(TAG, "Successfully loaded");
        }
    }

    pub fn get_value_from_ip(
        user: &StatsigUserInternal,
        field: &Option<DynamicString>,
        evaluator_context: &mut EvaluatorContext,
    ) -> Option<DynamicValue> {
        let unwrapped_field = match field {
            Some(f) => f.value.as_str(),
            _ => return None,
        };

        if unwrapped_field != "country" {
            return None;
        }

        let ip = user
            .get_user_value(&Some(DynamicString::from(IP.to_string())))?
            .string_value()?;

        Self::lookup(ip, &mut evaluator_context.result.override_reason)
    }

    fn lookup(
        ip_address: &str,
        override_reason: &mut Option<&'static str>,
    ) -> Option<DynamicValue> {
        if !Self::is_loaded() {
            // Only a four-part address receives the readiness override, even if an octet is invalid.
            if ip_address.splitn(5, '.').count() == 4 {
                *override_reason = Some(UNINITIALIZED_REASON);
                log_e!(
                    TAG,
                    "Failed to load country lookup. Did you disable CountryLookup or did not wait for country lookup to init. Check StatsigOptions configuration"
                );
            }
            return None;
        }
        Self::lookup_numeric(Self::parse_address(ip_address)?)
    }

    fn parse_address(ip_address: &str) -> Option<u32> {
        #[cfg(target_arch = "x86_64")]
        if (7..=15).contains(&ip_address.len())
            && is_x86_feature_detected!("avx512bw")
            && is_x86_feature_detected!("avx512vl")
        {
            // SAFETY: the feature checks and length bound cover the masked load in parse.
            return unsafe { simd::parse(ip_address) };
        }
        Self::parse_scalar(ip_address)
    }

    fn parse_scalar(ip_address: &str) -> Option<u32> {
        let mut parts = ip_address.split('.');
        let n0 = parts.next()?;
        let n1 = parts.next()?;
        let n2 = parts.next()?;
        let n3 = parts.next()?;
        if parts.next().is_some() {
            return None;
        }
        Some(u32::from_be_bytes([
            n0.parse().ok()?,
            n1.parse().ok()?,
            n2.parse().ok()?,
            n3.parse().ok()?,
        ]))
    }

    fn lookup_numeric(ip_address: u32) -> Option<DynamicValue> {
        // Each record combines the inclusive end /24 with its country ID in the low byte.
        let block_start = ip_address & !0xff;
        let mut min = 0;
        let mut max = COUNTRY_RANGES.len();
        while min < max {
            let mid = (min + max) >> 1;
            if u32::from_le_bytes(COUNTRY_RANGES[mid]) < block_start {
                min = mid + 1;
            } else {
                max = mid;
            }
        }
        let country_offset = usize::from(COUNTRY_RANGES[min][0]) * 2;
        let country = &COUNTRY_CODES[country_offset..country_offset + 2];
        (country != "--").then(|| dyn_value!(country))
    }
}

#[cfg(test)]
#[path = "__tests__/country_lookup_tests.rs"]
mod tests;
