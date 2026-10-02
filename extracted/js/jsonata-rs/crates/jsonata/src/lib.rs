//! JSONata for Rust — a faithful port of the `jsonata-java` reference port.

pub mod ast;
pub mod datetime;
pub mod error;
pub mod errors;
pub mod evaluator;
pub mod frame;
pub mod functions;
pub mod json;
pub mod parser;
pub mod signature;
pub mod tokenizer;
pub mod value;

pub use error::{JError, JResult};
pub use evaluator::Jsonata;
pub use value::JValue;
