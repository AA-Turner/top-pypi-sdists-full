use super::{dynamic_string::DynamicString, evaluator_context::EvaluatorContext};
use crate::{
    DynamicValue, dyn_value, log_d, log_e, unwrap_or_return_with, user::StatsigUserInternal,
};
use parking_lot::{Mutex, RwLock};
use std::sync::Arc;

pub struct CountryLookup;

pub struct CountryLookupData {
    country_codebook: Vec<String>,
    country_codes: Vec<u8>,
    ip_ranges: Vec<i64>,
}

lazy_static::lazy_static! {
    static ref COUNTRY_LOOKUP_DATA: Arc<RwLock<Option<CountryLookupData>>> = Arc::from(RwLock::from(None));
    static ref COUNTRY_LOOKUP_INIT: Mutex<()> = Mutex::new(());
    static ref IP: String = "ip".to_string();
}

#[cfg(test)]
static COUNTRY_LOOKUP_PARSE_COUNT: std::sync::atomic::AtomicUsize =
    std::sync::atomic::AtomicUsize::new(0);

const TAG: &str = "CountryLookup";
const UNINITIALIZED_REASON: &str = "CountryLookupNotLoaded";

pub trait UsizeExt {
    fn post_inc(&mut self) -> Self;
}

impl UsizeExt for usize {
    fn post_inc(&mut self) -> Self {
        let was = *self;
        *self += 1;
        was
    }
}

impl CountryLookup {
    pub(crate) fn is_loaded() -> bool {
        COUNTRY_LOOKUP_DATA
            .try_read()
            .is_some_and(|data| data.is_some())
    }

    pub fn load_country_lookup() {
        match COUNTRY_LOOKUP_DATA.try_read_for(std::time::Duration::from_secs(5)) {
            Some(lock) => {
                if lock.is_some() {
                    log_d!(TAG, "Country Lookup already loaded");
                    return;
                }
            }
            None => {
                log_e!(
                    TAG,
                    "Failed to acquire read lock on country lookup: Failed to lock COUNTRY_LOOKUP_DATA"
                );
                return;
            }
        }

        let Some(_init_guard) = COUNTRY_LOOKUP_INIT.try_lock_for(std::time::Duration::from_secs(5))
        else {
            log_e!(TAG, "Failed to acquire country lookup initialization lock");
            return;
        };

        match COUNTRY_LOOKUP_DATA.try_read_for(std::time::Duration::from_secs(5)) {
            Some(lock) if lock.is_some() => {
                log_d!(TAG, "Country Lookup already loaded");
                return;
            }
            Some(_) => {}
            None => {
                log_e!(
                    TAG,
                    "Failed to acquire read lock on country lookup: Failed to lock COUNTRY_LOOKUP_DATA"
                );
                return;
            }
        }

        #[cfg(test)]
        COUNTRY_LOOKUP_PARSE_COUNT.fetch_add(1, std::sync::atomic::Ordering::Relaxed);

        let bytes = include_bytes!("../../resources/ip_supalite.table");

        let mut country_codebook: Vec<String> = vec![];
        let mut country_codes: Vec<u8> = vec![];
        let mut ip_ranges: Vec<i64> = vec![];

        let mut i = 0;

        while i < bytes.len() {
            let c1 = bytes[i.post_inc()] as char;
            let c2 = bytes[i.post_inc()] as char;

            country_codebook.push(format!("{c1}{c2}"));

            if c1 == '*' {
                break;
            }
        }

        let longs = |index: usize| bytes[index] as i64;

        let mut last_end_range = 0_i64;
        while (i + 1) < bytes.len() {
            let mut count: i64 = 0;
            let n1 = longs(i.post_inc());
            if n1 < 240 {
                count = n1;
            } else if n1 == 242 {
                let n2 = longs(i.post_inc());
                let n3 = longs(i.post_inc());
                count = n2 | (n3 << 8);
            } else if n1 == 243 {
                let n2 = longs(i.post_inc());
                let n3 = longs(i.post_inc());
                let n4 = longs(i.post_inc());
                count = n2 | (n3 << 8) | (n4 << 16);
            }

            last_end_range += count * 256;

            let cc = bytes[i.post_inc()];
            ip_ranges.push(last_end_range);
            country_codes.push(cc)
        }

        let country_lookup = CountryLookupData {
            country_codebook,
            country_codes,
            ip_ranges,
        };

        match COUNTRY_LOOKUP_DATA.try_write_for(std::time::Duration::from_secs(5)) {
            Some(mut lock) => {
                *lock = Some(country_lookup);
                log_d!(TAG, " Successfully Loaded");
            }
            None => {
                log_e!(
                    TAG,
                    "Failed to acquire write lock on country_lookup: Failed to lock COUNTRY_LOOKUP_DATA"
                );
            }
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

        Self::lookup(ip, evaluator_context)
    }

    fn lookup(ip_address: &str, evaluator_context: &mut EvaluatorContext) -> Option<DynamicValue> {
        let parts: Vec<&str> = ip_address.split('.').collect();
        if parts.len() != 4 {
            return None;
        }

        let lock = unwrap_or_return_with!(
            COUNTRY_LOOKUP_DATA.try_read_for(std::time::Duration::from_secs(5)),
            || {
                evaluator_context.result.override_reason = Some(UNINITIALIZED_REASON);
                log_e!(TAG, "Failed to acquire read lock on country lookup");
                None
            }
        );

        let country_lookup_data = unwrap_or_return_with!(lock.as_ref(), || {
            evaluator_context.result.override_reason = Some(UNINITIALIZED_REASON);
            log_e!(
                TAG,
                "Failed to load country lookup. Did you disable CountryLookup or did not wait for country lookup to init. Check StatsigOptions configuration"
            );
            None
        });

        let nums: Vec<Option<i64>> = parts.iter().map(|&x| x.parse().ok()).collect();
        if let (Some(n0), Some(n1), Some(n2), Some(n3)) = (nums[0], nums[1], nums[2], nums[3]) {
            let ip_number = (n0 * 256_i64.pow(3)) + (n1 << 16) + (n2 << 8) + n3;
            return Self::lookup_numeric(ip_number, country_lookup_data);
        }

        None
    }

    fn lookup_numeric(
        ip_address: i64,
        country_lookup_data: &CountryLookupData,
    ) -> Option<DynamicValue> {
        let index = Self::binary_search(ip_address, country_lookup_data);
        let code_index = country_lookup_data.country_codes[index] as usize;
        let cc = country_lookup_data.country_codebook[code_index].clone();
        if cc == "--" {
            return None;
        }
        Some(dyn_value!(cc))
    }

    fn binary_search(value: i64, country_lookup_data: &CountryLookupData) -> usize {
        let mut min = 0;
        let mut max = country_lookup_data.ip_ranges.len();

        while min < max {
            let mid = (min + max) >> 1;
            if country_lookup_data.ip_ranges[mid] <= value {
                min = mid + 1;
            } else {
                max = mid;
            }
        }

        min
    }
}

#[cfg(test)]
mod tests {
    use super::{COUNTRY_LOOKUP_DATA, COUNTRY_LOOKUP_PARSE_COUNT, CountryLookup};
    use rusty_fork::rusty_fork_test;
    use std::sync::atomic::Ordering;
    use std::sync::{Arc, Barrier};

    rusty_fork_test! {
        #[test]
        fn concurrent_country_lookup_initialization_parses_once() {
            assert!(COUNTRY_LOOKUP_DATA.read().is_none());
            assert!(!CountryLookup::is_loaded());
            let barrier = Arc::new(Barrier::new(16));
            let workers: Vec<_> = (0..16)
                .map(|_| {
                    let barrier = Arc::clone(&barrier);
                    std::thread::spawn(move || {
                        barrier.wait();
                        CountryLookup::load_country_lookup();
                    })
                })
                .collect();

            for worker in workers {
                worker.join().unwrap();
            }

            assert!(COUNTRY_LOOKUP_DATA.read().is_some());
            assert!(CountryLookup::is_loaded());
            assert_eq!(COUNTRY_LOOKUP_PARSE_COUNT.load(Ordering::Relaxed), 1);
        }

        #[test]
        fn compact_country_codebook_preserves_known_ipv4_ranges_and_boundaries() {
            CountryLookup::load_country_lookup();
            let lookup = COUNTRY_LOOKUP_DATA.read();
            let data = lookup.as_ref().expect("country lookup should initialize");

            assert_eq!(data.country_codebook.len(), 243);
            assert_eq!(data.country_codes.len(), 198_578);
            assert_eq!(data.ip_ranges.len(), data.country_codes.len());
            assert_eq!(data.ip_ranges.last(), Some(&4_294_967_296));
            assert!(
                data.country_codes
                    .iter()
                    .all(|code| usize::from(*code) < data.country_codebook.len())
            );

            let country_for = |ip: [u8; 4]| {
                let address = i64::from(u32::from_be_bytes(ip));
                CountryLookup::lookup_numeric(address, data)
                    .and_then(|value| value.string_value.map(|country| country.value))
            };

            assert_eq!(country_for([8, 8, 8, 8]).as_deref(), Some("US"));
            assert_eq!(country_for([31, 13, 64, 1]).as_deref(), Some("NL"));
            assert_eq!(country_for([127, 0, 0, 1]), None);
            assert_eq!(country_for([255, 255, 255, 255]), None);

            let first_boundary = data.ip_ranges[0];
            assert_eq!(CountryLookup::binary_search(first_boundary - 1, data), 0);
            assert_eq!(CountryLookup::binary_search(first_boundary, data), 1);
        }
    }
}
