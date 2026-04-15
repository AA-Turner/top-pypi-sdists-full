use serde::Deserialize;
use std::sync::OnceLock;

static CATALOG_JSON: &str = include_str!("../catalog.json");
static CATALOG: OnceLock<Catalog> = OnceLock::new();

#[derive(Debug, Deserialize)]
pub struct Catalog {
    pub functions: Vec<FunctionDef>,
}

#[derive(Debug, Deserialize)]
pub struct FunctionDef {
    pub name: String,
    pub category: String,
    #[serde(default)]
    pub docs: Option<String>,
    pub overloads: Vec<Overload>,
}

#[derive(Debug, Deserialize)]
pub struct Overload {
    pub params: Vec<Param>,
    #[serde(default)]
    pub return_type: Option<String>,
}

#[derive(Debug, Deserialize)]
pub struct Param {
    pub name: String,
    pub typ: String,
}

impl Catalog {
    pub fn get() -> &'static Catalog {
        CATALOG.get_or_init(|| serde_json::from_str(CATALOG_JSON).expect("invalid catalog.json"))
    }

    pub fn find_function(&self, name: &str) -> Option<&FunctionDef> {
        let lower = name.to_lowercase();
        self.functions.iter().find(|f| f.name.to_lowercase() == lower)
    }

    pub fn functions_with_prefix(&self, prefix: &str) -> Vec<&FunctionDef> {
        let lower = prefix.to_lowercase();
        self.functions
            .iter()
            .filter(|f| f.name.to_lowercase().starts_with(&lower))
            .collect()
    }
}

impl FunctionDef {
    /// Render the first overload as a short signature string, e.g. `abs(x: int64) -> int64`
    pub fn signature_short(&self) -> String {
        match self.overloads.first() {
            Some(overload) => overload.render_signature(&self.name),
            None => format!("{}()", self.name),
        }
    }
}

impl Overload {
    pub fn render_signature(&self, name: &str) -> String {
        let params: Vec<String> = self
            .params
            .iter()
            .map(|p| format!("{}: {}", p.name, p.typ))
            .collect();
        let ret = self
            .return_type
            .as_deref()
            .map(|r| format!(" -> {r}"))
            .unwrap_or_default();
        format!("{name}({}){ret}", params.join(", "))
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_catalog_loads() {
        let catalog = Catalog::get();
        assert!(!catalog.functions.is_empty());
        assert!(catalog.functions.len() > 400);
    }

    #[test]
    fn test_find_function() {
        let catalog = Catalog::get();
        let abs = catalog.find_function("abs").unwrap();
        assert_eq!(abs.name, "abs");
        assert_eq!(abs.category, "Numeric Functions");
        assert!(!abs.overloads.is_empty());
    }

    #[test]
    fn test_prefix_search() {
        let catalog = Catalog::get();
        let results = catalog.functions_with_prefix("abs");
        assert!(!results.is_empty());
        assert!(results.iter().all(|f| f.name.starts_with("abs")));
    }

    #[test]
    fn test_signature_short() {
        let catalog = Catalog::get();
        let abs = catalog.find_function("abs").unwrap();
        let sig = abs.signature_short();
        assert!(sig.contains("abs("));
        assert!(sig.contains("int64"));
    }
}
