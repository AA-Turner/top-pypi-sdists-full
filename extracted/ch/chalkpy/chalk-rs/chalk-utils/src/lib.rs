pub mod duration;
pub mod namespace;

pub use duration::{
    parse_duration_ms, parse_duration_s, seconds_to_duration_string, CHALK_MAX_DURATION_MS,
    CHALK_MAX_DURATION_S,
};
pub use namespace::{build_namespaced_name, to_snake_case};
