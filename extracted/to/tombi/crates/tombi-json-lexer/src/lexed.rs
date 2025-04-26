use tombi_json_syntax::SyntaxKind::*;

#[allow(non_camel_case_types)]
type bits = u64;

#[derive(Debug, Default)]
pub struct Lexed {
    pub tokens: Vec<crate::Token>,
    pub joints: Vec<bits>,
    pub errors: Vec<crate::Error>,
}

impl Lexed {
    #[inline]
    pub(crate) fn push_result_token(
        &mut self,
        result_token: Result<crate::Token, crate::Error>,
    ) -> (tombi_text::Span, tombi_text::Range) {
        let idx = self.len();
        if idx % (bits::BITS as usize) == 0 {
            self.joints.push(0);
        }
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

    fn bit_index(&self, n: usize) -> (usize, usize) {
        let idx = n / (bits::BITS as usize);
        let b_idx = n % (bits::BITS as usize);
        (idx, b_idx)
    }

    fn len(&self) -> usize {
        self.tokens.len()
    }

    /// Sets jointness for the last token we've pushed.
    #[inline]
    pub fn set_joint(&mut self) {
        let n = self.len() - 1;
        let (idx, b_idx) = self.bit_index(n);
        self.joints[idx] |= 1 << b_idx;
    }

    pub fn is_joint(&self, n: usize) -> bool {
        let (idx, b_idx) = self.bit_index(n);
        self.joints[idx] & (1 << b_idx) != 0
    }
}
