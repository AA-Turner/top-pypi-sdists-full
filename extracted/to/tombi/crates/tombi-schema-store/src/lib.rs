mod accessor;
mod error;
pub mod json;
mod options;
mod schema;
mod store;
mod value_type;
mod x_taplo;

pub use accessor::{Accessor, Accessors};
pub use error::Error;
pub use options::Options;
pub use schema::*;
pub use store::SchemaStore;
pub use value_type::ValueType;

pub fn get_schema_name(schema_url: &SchemaUrl) -> Option<&str> {
    if let Some(path) = schema_url.path().split('/').last() {
        if !path.is_empty() {
            return Some(path);
        }
    }
    schema_url.host_str()
}
