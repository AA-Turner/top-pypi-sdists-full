#[derive(Debug, Clone, Default, serde::Serialize, serde::Deserialize)]
pub struct ConversionConfig {
    #[serde(default)]
    pub strip_encrypted_reasoning: bool,
}
