use std::collections::{HashMap, HashSet};

use lsp_types::Location;
use ruff_python_ast::Stmt;
use ruff_python_trivia::CommentRanges;

pub type ImportAliasMap = HashMap<String, HashMap<String, HashSet<String>>>;
pub type KwargLocationMap = HashMap<String, Location>;

#[derive(Clone, Debug)]
pub struct ParsedFileCache {
    pub path: String,
    pub source: String,
    pub stmts: Vec<Stmt>,
    pub imports: ImportAliasMap,
    pub comment_ranges: CommentRanges,
}
