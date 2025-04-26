use tombi_ast::Boolean;

use super::LiteralNode;

impl LiteralNode for Boolean {
    fn token(&self) -> Option<tombi_syntax::SyntaxToken> {
        self.token()
    }
}

#[cfg(test)]
mod tests {
    use crate::test_format;

    test_format! {
        #[test]
        fn boolean_true(r#"boolean = true"#) -> Ok(source);
    }

    test_format! {
        #[test]
        fn boolean_false(r#"boolean = false"#) -> Ok(source);
    }
}
