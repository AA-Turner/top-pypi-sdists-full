use tombi_json_syntax::SyntaxKind::*;

#[derive(Debug, Default)]
pub struct Lexed {
    pub tokens: Vec<crate::Token>,
    pub errors: Vec<crate::Error>,
}

impl Lexed {
    #[inline]
    pub(crate) fn push_result_token(
        &mut self,
        result_token: Result<crate::Token, crate::Error>,
    ) -> (tombi_text::Span, tombi_text::Range) {
        match result_token {
            Ok(token) => {
                let (span, range) = (token.span(), token.range());
                self.tokens.push(token);

                (span, range)
            }
            Err(error) => {
                let (span, range) = (error.span(), error.range());

                self.tokens.push(crate::Token::new(
                    INVALID_TOKEN,
                    (error.span(), error.range()),
                ));
                self.errors.push(error);

                (span, range)
            }
        }
    }
}
