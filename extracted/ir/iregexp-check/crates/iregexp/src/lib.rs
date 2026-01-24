//! A checking implementation of [I-Regexp](https://datatracker.ietf.org/doc/html/rfc9485).
//!
//! ```
//! let valid = iregexp::check(r"[ab]{3}");
//! assert_eq!(valid, true);
//!
//! let valid = iregexp::check(r"[0-9]*?");
//! assert_eq!(valid, false);
//! ```
use pest::Parser;
pub mod parser;
pub use parser::{IRegexp, Rule};

/// Return _true_ if regular expression _pattern_ is valid according I-Regexp.
pub fn check(pattern: &str) -> bool {
    IRegexp::parse(Rule::pattern, pattern).is_ok()
}
