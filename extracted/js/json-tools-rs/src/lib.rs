//! # JSON Tools RS
//!
//! A Rust library for advanced JSON manipulation, including flattening and unflattening
//! nested JSON structures with configurable filtering and replacement options.
//!
//! ## Features
//!
//! - **Unified API**: Single `JSONTools` entry point for both flattening and unflattening
//! - **Builder Pattern**: Fluent, chainable API for easy configuration
//! - **Advanced Filtering**: Remove empty values (strings, objects, arrays, null values)
//! - **Pattern Replacements**: Support for literal and regex-based key/value replacements
//! - **High Performance**: SIMD-accelerated JSON parsing with optimized algorithms
//! - **Batch Processing**: Handle single JSON strings or arrays of JSON strings
//! - **Comprehensive Error Handling**: Detailed error messages for debugging
//!
//! ## Notes
//!
//! - **Root-level empty arrays**: Flattening an empty array (`[]`) produces `"{}"` (an empty
//!   object), because flattening always yields key-value pairs. Zero elements means zero
//!   key-value pairs, which is represented as an empty object.
//!
//! ## Quick Start with Unified API
//!
//! ### Flattening JSON
//!
//! ```rust
//! use json_tools_rs::{JSONTools, JsonOutput};
//!
//! let json = r#"{"user": {"name": "John", "details": {"age": null, "city": ""}}}"#;
//! let result = JSONTools::new()
//!     .flatten()
//!     .separator("::")
//!     .lowercase_keys(true)
//!     .key_replacement("r'(User|Admin)_'", "")
//!     .value_replacement("@example.com", "@company.org")
//!     .remove_empty_strings(true)
//!     .remove_nulls(true)
//!     .remove_empty_objects(true)
//!     .remove_empty_arrays(true)
//!     .execute(json).unwrap();
//!
//! match result {
//!     JsonOutput::Single(flattened) => {
//!         // Result: {"user::name": "John"}
//!         println!("{}", flattened);
//!     }
//!     JsonOutput::Multiple(_) => unreachable!(),
//! }
//! ```
//!
//! ### Unflattening JSON
//!
//! ```rust
//! use json_tools_rs::{JSONTools, JsonOutput};
//!
//! let flattened = r#"{"user::name": "John", "user::age": 30}"#;
//! let result = JSONTools::new()
//!     .unflatten()
//!     .separator("::")
//!     .lowercase_keys(true)
//!     .key_replacement("r'(User|Admin)_'", "")
//!     .value_replacement("@company.org", "@example.com")
//!     .remove_empty_strings(true)
//!     .remove_nulls(true)
//!     .remove_empty_objects(true)
//!     .remove_empty_arrays(true)
//!     .execute(flattened).unwrap();
//!
//! match result {
//!     JsonOutput::Single(unflattened) => {
//!         // Result: {"user": {"name": "John", "age": 30}}
//!         println!("{}", unflattened);
//!     }
//!     JsonOutput::Multiple(_) => unreachable!(),
//! }
//! ```
//!
//! # Doctests
//!
//! The following doctests demonstrate individual features in a progressive learning format.
//! Each example focuses on a specific capability to help users understand how to use the library effectively.
//!
//! ## 1. Basic Flattening and Unflattening Operations
//!
//! ```rust
//! use json_tools_rs::{JSONTools, JsonOutput};
//!
//! // Basic flattening - converts nested JSON to flat key-value pairs
//! let nested_json = r#"{"user": {"name": "John", "profile": {"age": 30}}}"#;
//! let result = JSONTools::new()
//!     .flatten()
//!     .execute(nested_json).unwrap();
//!
//! match result {
//!     JsonOutput::Single(flattened) => {
//!         // Result: {"user.name": "John", "user.profile.age": 30}
//!         assert!(flattened.contains("user.name"));
//!         assert!(flattened.contains("user.profile.age"));
//!     }
//!     JsonOutput::Multiple(_) => unreachable!(),
//! }
//!
//! // Basic unflattening - converts flat JSON back to nested structure
//! let flat_json = r#"{"user.name": "John", "user.profile.age": 30}"#;
//! let result = JSONTools::new()
//!     .unflatten()
//!     .execute(flat_json).unwrap();
//!
//! match result {
//!     JsonOutput::Single(unflattened) => {
//!         // Result: {"user": {"name": "John", "profile": {"age": 30}}}
//!         assert!(unflattened.contains(r#""user""#));
//!         assert!(unflattened.contains(r#""name":"John""#));
//!     }
//!     JsonOutput::Multiple(_) => unreachable!(),
//! }
//! ```
//!
//! ## 2. Custom Separator Usage
//!
//! ```rust
//! use json_tools_rs::{JSONTools, JsonOutput};
//!
//! // Using custom separator instead of default "."
//! let json = r#"{"company": {"department": {"team": "engineering"}}}"#;
//! let result = JSONTools::new()
//!     .flatten()
//!     .separator("::") // Use "::" instead of "."
//!     .execute(json).unwrap();
//!
//! match result {
//!     JsonOutput::Single(flattened) => {
//!         // Result: {"company::department::team": "engineering"}
//!         assert!(flattened.contains("company::department::team"));
//!         assert!(!flattened.contains("company.department.team"));
//!     }
//!     JsonOutput::Multiple(_) => unreachable!(),
//! }
//! ```
//!
//! ## 3. Key Transformations - Lowercase Keys
//!
//! ```rust
//! use json_tools_rs::{JSONTools, JsonOutput};
//!
//! // Convert all keys to lowercase during processing
//! let json = r#"{"UserName": "John", "UserProfile": {"FirstName": "John"}}"#;
//! let result = JSONTools::new()
//!     .flatten()
//!     .lowercase_keys(true)
//!     .execute(json).unwrap();
//!
//! match result {
//!     JsonOutput::Single(flattened) => {
//!         // Result: {"username": "John", "userprofile.firstname": "John"}
//!         assert!(flattened.contains("username"));
//!         assert!(flattened.contains("userprofile.firstname"));
//!         assert!(!flattened.contains("UserName"));
//!     }
//!     JsonOutput::Multiple(_) => unreachable!(),
//! }
//! ```
//!
//! ## 4. Key Replacement Patterns - Literal Replacement
//!
//! ```rust
//! use json_tools_rs::{JSONTools, JsonOutput};
//!
//! // Replace literal strings in keys
//! let json = r#"{"user_profile_name": "John", "user_profile_age": 30}"#;
//! let result = JSONTools::new()
//!     .flatten()
//!     .key_replacement("user_profile_", "person_") // Replace literal string
//!     .execute(json).unwrap();
//!
//! match result {
//!     JsonOutput::Single(flattened) => {
//!         // Result: {"person_name": "John", "person_age": 30}
//!         assert!(flattened.contains("person_name"));
//!         assert!(flattened.contains("person_age"));
//!         assert!(!flattened.contains("user_profile_"));
//!     }
//!     JsonOutput::Multiple(_) => unreachable!(),
//! }
//! ```
//!
//! ## 5. Key Replacement Patterns - Regex Replacement
//!
//! ```rust
//! use json_tools_rs::{JSONTools, JsonOutput};
//!
//! // Replace using regex patterns in keys
//! let json = r#"{"user_name": "John", "admin_name": "Jane", "guest_name": "Bob"}"#;
//! let result = JSONTools::new()
//!     .flatten()
//!     .key_replacement("r'(user|admin)_'", "person_") // Regex pattern
//!     .execute(json).unwrap();
//!
//! match result {
//!     JsonOutput::Single(flattened) => {
//!         // Result: {"person_name": "John", "person_name": "Jane", "guest_name": "Bob"}
//!         // Note: This would cause collision without collision handling
//!         assert!(flattened.contains("person_name"));
//!         assert!(flattened.contains("guest_name"));
//!     }
//!     JsonOutput::Multiple(_) => unreachable!(),
//! }
//! ```
//!
//! ## 6. Value Replacement Patterns - Literal Replacement
//!
//! ```rust
//! use json_tools_rs::{JSONTools, JsonOutput};
//!
//! // Replace literal strings in values
//! let json = r#"{"email": "user@example.com", "backup_email": "admin@example.com"}"#;
//! let result = JSONTools::new()
//!     .flatten()
//!     .value_replacement("@example.com", "@company.org") // Replace domain
//!     .execute(json).unwrap();
//!
//! match result {
//!     JsonOutput::Single(flattened) => {
//!         // Result: {"email": "user@company.org", "backup_email": "admin@company.org"}
//!         assert!(flattened.contains("@company.org"));
//!         assert!(!flattened.contains("@example.com"));
//!     }
//!     JsonOutput::Multiple(_) => unreachable!(),
//! }
//! ```
//!
//! ## 7. Value Replacement Patterns - Regex Replacement
//!
//! ```rust
//! use json_tools_rs::{JSONTools, JsonOutput};
//!
//! // Replace using regex patterns in values
//! let json = r#"{"role": "super", "level": "admin", "type": "user"}"#;
//! let result = JSONTools::new()
//!     .flatten()
//!     .value_replacement("r'^(super|admin)$'", "administrator") // Regex pattern
//!     .execute(json).unwrap();
//!
//! match result {
//!     JsonOutput::Single(flattened) => {
//!         // Result: {"role": "administrator", "level": "administrator", "type": "user"}
//!         assert!(flattened.contains(r#""role":"administrator""#));
//!         assert!(flattened.contains(r#""level":"administrator""#));
//!         assert!(flattened.contains(r#""type":"user""#));
//!     }
//!     JsonOutput::Multiple(_) => unreachable!(),
//! }
//! ```
//!
//! ## 8. Filtering Options - Remove Empty Strings
//!
//! ```rust
//! use json_tools_rs::{JSONTools, JsonOutput};
//!
//! // Remove keys that have empty string values
//! let json = r#"{"name": "John", "nickname": "", "age": 30}"#;
//! let result = JSONTools::new()
//!     .flatten()
//!     .remove_empty_strings(true)
//!     .execute(json).unwrap();
//!
//! match result {
//!     JsonOutput::Single(flattened) => {
//!         // Result: {"name": "John", "age": 30} - "nickname" removed
//!         assert!(flattened.contains("name"));
//!         assert!(flattened.contains("age"));
//!         assert!(!flattened.contains("nickname"));
//!     }
//!     JsonOutput::Multiple(_) => unreachable!(),
//! }
//! ```
//!
//! ## 9. Filtering Options - Remove Null Values
//!
//! ```rust
//! use json_tools_rs::{JSONTools, JsonOutput};
//!
//! // Remove keys that have null values
//! let json = r#"{"name": "John", "age": null, "city": "NYC"}"#;
//! let result = JSONTools::new()
//!     .flatten()
//!     .remove_nulls(true)
//!     .execute(json).unwrap();
//!
//! match result {
//!     JsonOutput::Single(flattened) => {
//!         // Result: {"name": "John", "city": "NYC"} - "age" removed
//!         assert!(flattened.contains("name"));
//!         assert!(flattened.contains("city"));
//!         assert!(!flattened.contains("age"));
//!     }
//!     JsonOutput::Multiple(_) => unreachable!(),
//! }
//! ```
//!
//! ## 10. Filtering Options - Remove Empty Objects and Arrays
//!
//! ```rust
//! use json_tools_rs::{JSONTools, JsonOutput};
//!
//! // Remove keys that have empty objects or arrays
//! let json = r#"{"user": {"name": "John"}, "tags": [], "metadata": {}}"#;
//! let result = JSONTools::new()
//!     .flatten()
//!     .remove_empty_objects(true)
//!     .remove_empty_arrays(true)
//!     .execute(json).unwrap();
//!
//! match result {
//!     JsonOutput::Single(flattened) => {
//!         // Result: {"user.name": "John"} - "tags" and "metadata" removed
//!         assert!(flattened.contains("user.name"));
//!         assert!(!flattened.contains("tags"));
//!         assert!(!flattened.contains("metadata"));
//!     }
//!     JsonOutput::Multiple(_) => unreachable!(),
//! }
//! ```
//!
//!
//! ## 11. Collision Handling - Collect Values into Arrays
//!
//! ```rust
//! use json_tools_rs::{JSONTools, JsonOutput};
//!
//! // When key replacements cause collisions, collect all values into an array
//! let json = r#"{"user_name": "John", "admin_name": "Jane"}"#;
//! let result = JSONTools::new()
//!     .flatten()
//!     .key_replacement("r'(user|admin)_'", "") // This creates collision: both become "name"
//!     .handle_key_collision(true) // Collect values into array
//!     .execute(json).unwrap();
//!
//! match result {
//!     JsonOutput::Single(flattened) => {
//!         // Result: {"name": ["John", "Jane"]}
//!         assert!(flattened.contains(r#""name":["John","Jane"]"#) ||
//!                 flattened.contains(r#""name": ["John", "Jane"]"#));
//!     }
//!     JsonOutput::Multiple(_) => unreachable!(),
//! }
//! ```
//!
//! ## 12. Comprehensive Integration Example
//!
//! ```rust
//! use json_tools_rs::{JSONTools, JsonOutput};
//!
//! // Comprehensive example combining multiple features for real-world usage
//! let complex_json = r#"{
//!     "User_Profile": {
//!         "Personal_Info": {
//!             "FirstName": "John",
//!             "LastName": "",
//!             "Email": "john@example.com",
//!             "Age": null
//!         },
//!         "Settings": {
//!             "Theme": "dark",
//!             "Notifications": {},
//!             "Tags": []
//!         }
//!     },
//!     "Admin_Profile": {
//!         "Personal_Info": {
//!             "FirstName": "Jane",
//!             "Email": "jane@example.com",
//!             "Role": "super"
//!         }
//!     }
//! }"#;
//!
//! let result = JSONTools::new()
//!     .flatten()
//!     .separator("::") // Use custom separator
//!     .lowercase_keys(true) // Convert all keys to lowercase
//!     .key_replacement("r'(user|admin)_profile::'", "person::") // Normalize profile keys
//!     .key_replacement("personal_info::", "info::") // Simplify nested keys
//!     .value_replacement("@example.com", "@company.org") // Update email domain
//!     .value_replacement("r'^super$'", "administrator") // Normalize role values
//!     .remove_empty_strings(true) // Remove empty string values
//!     .remove_nulls(true) // Remove null values
//!     .remove_empty_objects(true) // Remove empty objects
//!     .remove_empty_arrays(true) // Remove empty arrays
//!     .handle_key_collision(true) // Handle any key collisions by collecting into arrays
//!     .execute(complex_json).unwrap();
//!
//! match result {
//!     JsonOutput::Single(flattened) => {
//!         // Verify the comprehensive transformation worked
//!         // Note: Keys are transformed through multiple steps: lowercase + replacements
//!         assert!(flattened.contains("@company.org"));
//!         assert!(flattened.contains("administrator"));
//!         assert!(!flattened.contains("lastname")); // Empty string removed
//!         assert!(!flattened.contains("age")); // Null removed
//!         assert!(!flattened.contains("notifications")); // Empty object removed
//!         assert!(!flattened.contains("tags")); // Empty array removed
//!         // The exact key structure depends on the order of transformations
//!         println!("Comprehensive transformation result: {}", flattened);
//!     }
//!     JsonOutput::Multiple(_) => unreachable!(),
//! }
//!
//! // Demonstrate unflattening with the same configuration
//! let flat_json = r#"{"person::info::name": "Alice", "person::settings::theme": "light"}"#;
//! let result = JSONTools::new()
//!     .unflatten()
//!     .separator("::")
//!     .execute(flat_json).unwrap();
//!
//! match result {
//!     JsonOutput::Single(unflattened) => {
//!         // Result: {"person": {"info": {"name": "Alice"}, "settings": {"theme": "light"}}}
//!         assert!(unflattened.contains(r#""person""#));
//!         assert!(unflattened.contains(r#""info""#));
//!         assert!(unflattened.contains(r#""settings""#));
//!         println!("Unflattening result: {}", unflattened);
//!     }
//!     JsonOutput::Multiple(_) => unreachable!(),
//! }
//! ```
//!

// Use mimalloc for a real, measured improvement on allocation-heavy workloads --
// interleaved bench_quick comparison (2026-07-30, macOS aarch64, 4 rounds): ~28%
// faster for normal-mode transforms, ~14% faster for unflatten and batch-parallel
// flatten (previously undocumented beyond a generic "~5-10%" estimate; not yet
// measured on other platforms). Only enabled when the mimalloc feature is active
// -- opt-in for `cargo add` consumers who build from source; deliberately NOT
// enabled for published Python wheels, where an earlier attempt hit
// real cross-compilation breakage (aarch64/ppc64le manylinux, musllinux) when
// bundled with a since-reverted PGO effort -- see CHANGELOG.md.
#[cfg(feature = "mimalloc")]
#[global_allocator]
static GLOBAL: mimalloc::MiMalloc = mimalloc::MiMalloc;

// ================================================================================================
// MODULE DECLARATIONS
// ================================================================================================

#[cfg(feature = "python")]
pub(crate) mod arrow_columnar;
mod builder;
pub(crate) mod cache;
mod config;
pub(crate) mod config_json;
pub(crate) mod convert;
mod error;
pub(crate) mod flatten;
pub(crate) mod fxhash;
pub(crate) mod json_parser;
pub(crate) mod transform;
mod types;
pub(crate) mod unflatten;

#[cfg(feature = "python")]
mod python;

#[cfg(test)]
mod tests;

// ================================================================================================
// PUBLIC RE-EXPORTS (preserves backward-compatible import paths)
// ================================================================================================

pub use builder::JSONTools;
pub use config::{
    BooleanConversionConfig, CollisionConfig, DateConversionConfig, FilteringConfig,
    NullConversionConfig, NumberConversionConfig, ProcessingConfig, ReplacementConfig,
    TypeConversionConfig,
};
pub use error::JsonToolsError;
pub use types::{JsonInput, JsonOutput};
