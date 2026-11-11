use super::{diagnostics::ContextType, marker::Marker};
use std::collections::HashMap;

pub struct DiagnosticsUtils;

impl DiagnosticsUtils {
    pub fn format_diagnostics_metadata(
        context_type: &ContextType,
        markers: &Vec<Marker>,
    ) -> Result<HashMap<String, String>, String> {
        let mut metadata = HashMap::new();

        metadata.insert("context".to_string(), context_type.to_string());

        match serde_json::to_string(&markers) {
            Ok(markers_json) => {
                metadata.insert("markers".to_string(), markers_json);
                Ok(metadata)
            }
            Err(err) => Err(format!("Failed to serialize markers: {err}")),
        }
    }
}
