use crate::BoolDefaultTrue;

#[cfg_attr(feature = "serde", derive(serde::Serialize, serde::Deserialize))]
#[cfg_attr(feature = "serde", serde(deny_unknown_fields))]
#[cfg_attr(feature = "serde", serde(rename_all = "kebab-case"))]
#[cfg_attr(feature = "jsonschema", derive(schemars::JsonSchema))]
#[cfg_attr(feature = "jsonschema", schemars(extend("x-tombi-table-keys-order" = tombi_x_keyword::TableKeysOrder::Ascending)))]
#[derive(Debug, Default, Clone, PartialEq)]
pub struct LspOptions {
    /// # Code Action Feature options.
    pub code_action: Option<LspCodeAction>,

    /// # Completion Feature options.
    pub completion: Option<LspCompletion>,

    /// # Diagnostics Feature options.
    pub diagnostics: Option<LspDiagnostics>,

    /// # Document Link Feature options.
    pub document_link: Option<LspDocumentLink>,

    /// # Formatting Feature options.
    pub formatting: Option<LspFormatting>,

    /// # Goto Declaration Feature options.
    pub goto_declaration: Option<LspGotoDefinition>,

    /// # Goto Definition Feature options.
    pub goto_definition: Option<LspGotoDefinition>,

    /// # Goto Type Definition Feature options.
    pub goto_type_definition: Option<LspGotoDefinition>,

    /// # Hover Feature options.
    pub hover: Option<LspHover>,
}

impl LspOptions {
    pub const fn default() -> Self {
        Self {
            code_action: None,
            completion: None,
            diagnostics: None,
            document_link: None,
            formatting: None,
            goto_declaration: None,
            goto_definition: None,
            goto_type_definition: None,
            hover: None,
        }
    }
}

#[cfg_attr(feature = "serde", derive(serde::Serialize, serde::Deserialize))]
#[cfg_attr(feature = "serde", serde(deny_unknown_fields))]
#[cfg_attr(feature = "serde", serde(rename_all = "kebab-case"))]
#[cfg_attr(feature = "jsonschema", derive(schemars::JsonSchema))]
#[derive(Debug, Default, Clone, PartialEq)]
pub struct LspHover {
    /// # Enable hover feature.
    ///
    /// Whether to enable hover.
    pub enabled: Option<BoolDefaultTrue>,
}

#[cfg_attr(feature = "serde", derive(serde::Serialize, serde::Deserialize))]
#[cfg_attr(feature = "serde", serde(deny_unknown_fields))]
#[cfg_attr(feature = "serde", serde(rename_all = "kebab-case"))]
#[cfg_attr(feature = "jsonschema", derive(schemars::JsonSchema))]
#[derive(Debug, Default, Clone, PartialEq)]
pub struct LspCodeAction {
    /// # Enable code action feature.
    ///
    /// Whether to enable code action.
    pub enabled: Option<BoolDefaultTrue>,
}

#[cfg_attr(feature = "serde", derive(serde::Serialize, serde::Deserialize))]
#[cfg_attr(feature = "serde", serde(deny_unknown_fields))]
#[cfg_attr(feature = "serde", serde(rename_all = "kebab-case"))]
#[cfg_attr(feature = "jsonschema", derive(schemars::JsonSchema))]
#[derive(Debug, Default, Clone, PartialEq)]
pub struct LspCompletion {
    /// # Enable completion feature.
    ///
    /// Whether to enable completion.
    pub enabled: Option<BoolDefaultTrue>,
}

#[cfg_attr(feature = "serde", derive(serde::Serialize, serde::Deserialize))]
#[cfg_attr(feature = "serde", serde(deny_unknown_fields))]
#[cfg_attr(feature = "serde", serde(rename_all = "kebab-case"))]
#[cfg_attr(feature = "jsonschema", derive(schemars::JsonSchema))]
#[derive(Debug, Default, Clone, PartialEq)]
pub struct LspFormatting {
    /// # Enable formatting feature.
    ///
    /// Whether to enable formatting.
    pub enabled: Option<BoolDefaultTrue>,
}

#[cfg_attr(feature = "serde", derive(serde::Serialize, serde::Deserialize))]
#[cfg_attr(feature = "serde", serde(deny_unknown_fields))]
#[cfg_attr(feature = "serde", serde(rename_all = "kebab-case"))]
#[cfg_attr(feature = "jsonschema", derive(schemars::JsonSchema))]
#[derive(Debug, Default, Clone, PartialEq)]
pub struct LspDiagnostics {
    /// # Enable diagnostics feature.
    ///
    /// Whether to enable diagnostics.
    pub enabled: Option<BoolDefaultTrue>,
}

#[cfg_attr(feature = "serde", derive(serde::Serialize, serde::Deserialize))]
#[cfg_attr(feature = "serde", serde(deny_unknown_fields))]
#[cfg_attr(feature = "serde", serde(rename_all = "kebab-case"))]
#[cfg_attr(feature = "jsonschema", derive(schemars::JsonSchema))]
#[derive(Debug, Default, Clone, PartialEq)]
pub struct LspDocumentLink {
    /// # Enable document link feature.
    ///
    /// Whether to enable document link.
    pub enabled: Option<BoolDefaultTrue>,
}

#[cfg_attr(feature = "serde", derive(serde::Serialize, serde::Deserialize))]
#[cfg_attr(feature = "serde", serde(deny_unknown_fields))]
#[cfg_attr(feature = "serde", serde(rename_all = "kebab-case"))]
#[cfg_attr(feature = "jsonschema", derive(schemars::JsonSchema))]
#[derive(Debug, Default, Clone, PartialEq)]
pub struct LspGotoDefinition {
    /// # Enable goto definition feature.
    ///
    /// Whether to enable goto definition.
    pub enabled: Option<BoolDefaultTrue>,
}
