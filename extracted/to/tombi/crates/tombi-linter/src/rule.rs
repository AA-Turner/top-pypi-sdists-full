mod key_empty;
pub use key_empty::KeyEmptyRule;

pub trait Rule<N: tombi_ast::AstNode> {
    fn check(node: &N, l: &mut crate::Linter);
}
