/// Taplo schema extension
///
/// See https://taplo.tamasfe.dev/configuration/developing-schemas.html#schema-extension
#[derive(Debug, Default, Clone, serde::Serialize, serde::Deserialize)]
pub struct XTaplo {
    pub hidden: Option<bool>,
}
