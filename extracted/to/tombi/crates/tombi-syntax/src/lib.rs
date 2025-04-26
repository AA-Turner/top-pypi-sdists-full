mod builder;
mod error;
mod generated;
mod language;

pub use builder::SyntaxTreeBuilder;
pub use error::Error;
pub use generated::SyntaxKind;
pub use language::TomlLanguage;
pub use tombi_rg_tree::Direction;

pub type SyntaxNode = tombi_rg_tree::RedNode<TomlLanguage>;
pub type SyntaxToken = tombi_rg_tree::RedToken<TomlLanguage>;
pub type SyntaxElement = tombi_rg_tree::RedElement<TomlLanguage>;
pub type SyntaxNodePtr = tombi_rg_tree::RedNodePtr<TomlLanguage>;
pub type SyntaxNodeChildren = tombi_rg_tree::RedNodeChildren<TomlLanguage>;
pub type SyntaxElementChildren = tombi_rg_tree::RedElementChildren<TomlLanguage>;
pub type PreorderWithTokens = tombi_rg_tree::RedPreorderWithTokens<TomlLanguage>;
