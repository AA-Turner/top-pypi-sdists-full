//! OpenQASM 2.0 / 3.0 토크나이저.
//!
//! single-pass byte scan, allocation 최소화. 코멘트 (`// ...`) 와 공백을 건너뛰고
//! 키워드/식별자/숫자/문자열/심볼을 [`Token`] 으로 emit 한다.

use crate::error::{QasmError, QasmResult};

/// 토큰 종류. payload 가 필요한 토큰 (식별자, 숫자, 문자열) 외에는 단위 변형.
#[derive(Debug, Clone, PartialEq)]
pub enum Tok {
    // 키워드 (2.0 / 3.0 공통)
    Openqasm,
    Include,
    Qreg,
    Creg,
    Gate,
    Opaque,
    Barrier,
    Measure,
    Reset,
    If,
    // 3.0 추가 키워드
    Qubit,
    Bit,
    Else,
    For,
    While,
    Box_,
    Def,
    // v0.4.7: switch / case / default
    Switch,
    Case_,
    Default_,
    // v0.4.7: int (for-loop 의 type annotation: `for int _ in ...`)
    Int_,
    // 함수 (수식 안에서 식별자로 처리되지만 구분 위해 keyword 화)
    Sin,
    Cos,
    Tan,
    Exp,
    Ln,
    Sqrt,
    // 상수
    Pi,
    // 식별자
    Ident(String),
    // 정수
    Int(i64),
    // 실수
    Real(f64),
    // 문자열 (include 인자)
    Str(String),
    // 기호
    LParen,
    RParen,
    LBracket,
    RBracket,
    LBrace,
    RBrace,
    Comma,
    Semicolon,
    Colon,
    Plus,
    Minus,
    Star,
    Slash,
    Caret,
    Arrow, // ->
    EqEq,  // ==
    Eq,    // = (3.0 assignment-form measurement: c = measure q;)
    Eof,
}

#[derive(Debug, Clone, PartialEq)]
pub struct Token {
    pub kind: Tok,
    pub line: usize,
    pub col: usize,
}

pub struct Lexer<'a> {
    src: &'a [u8],
    pos: usize,
    line: usize,
    col: usize,
}

impl<'a> Lexer<'a> {
    pub fn new(src: &'a str) -> Self {
        Self {
            src: src.as_bytes(),
            pos: 0,
            line: 1,
            col: 1,
        }
    }

    /// 모든 토큰을 EOF 까지 모아 반환.
    pub fn tokenize(mut self) -> QasmResult<Vec<Token>> {
        let mut out = Vec::new();
        loop {
            let tok = self.next_token()?;
            let is_eof = matches!(tok.kind, Tok::Eof);
            out.push(tok);
            if is_eof {
                break;
            }
        }
        Ok(out)
    }

    fn peek(&self) -> Option<u8> {
        self.src.get(self.pos).copied()
    }

    fn peek_at(&self, offset: usize) -> Option<u8> {
        self.src.get(self.pos + offset).copied()
    }

    fn advance(&mut self) -> Option<u8> {
        let c = self.peek()?;
        self.pos += 1;
        if c == b'\n' {
            self.line += 1;
            self.col = 1;
        } else {
            self.col += 1;
        }
        Some(c)
    }

    fn skip_whitespace_and_comments(&mut self) {
        loop {
            match self.peek() {
                Some(c) if c.is_ascii_whitespace() => {
                    self.advance();
                }
                Some(b'/') if self.peek_at(1) == Some(b'/') => {
                    while let Some(c) = self.peek() {
                        if c == b'\n' {
                            break;
                        }
                        self.advance();
                    }
                }
                _ => break,
            }
        }
    }

    fn next_token(&mut self) -> QasmResult<Token> {
        self.skip_whitespace_and_comments();
        let line = self.line;
        let col = self.col;
        let Some(c) = self.peek() else {
            return Ok(Token {
                kind: Tok::Eof,
                line,
                col,
            });
        };

        // 식별자 / 키워드
        if c.is_ascii_alphabetic() || c == b'_' {
            return Ok(self.lex_ident(line, col));
        }
        // 숫자 (정수 또는 실수)
        if c.is_ascii_digit() || (c == b'.' && self.peek_at(1).is_some_and(|n| n.is_ascii_digit()))
        {
            return self.lex_number(line, col);
        }
        // 문자열 리터럴 (include 인자)
        if c == b'"' {
            return self.lex_string(line, col);
        }

        // 심볼
        let kind = match c {
            b'(' => {
                self.advance();
                Tok::LParen
            }
            b')' => {
                self.advance();
                Tok::RParen
            }
            b'[' => {
                self.advance();
                Tok::LBracket
            }
            b']' => {
                self.advance();
                Tok::RBracket
            }
            b'{' => {
                self.advance();
                Tok::LBrace
            }
            b'}' => {
                self.advance();
                Tok::RBrace
            }
            b',' => {
                self.advance();
                Tok::Comma
            }
            b';' => {
                self.advance();
                Tok::Semicolon
            }
            b':' => {
                self.advance();
                Tok::Colon
            }
            b'+' => {
                self.advance();
                Tok::Plus
            }
            b'-' => {
                self.advance();
                if self.peek() == Some(b'>') {
                    self.advance();
                    Tok::Arrow
                } else {
                    Tok::Minus
                }
            }
            b'*' => {
                self.advance();
                Tok::Star
            }
            b'/' => {
                self.advance();
                Tok::Slash
            }
            b'^' => {
                self.advance();
                Tok::Caret
            }
            b'=' => {
                self.advance();
                if self.peek() == Some(b'=') {
                    self.advance();
                    Tok::EqEq
                } else {
                    Tok::Eq
                }
            }
            other => {
                return Err(QasmError::Lex {
                    line,
                    col,
                    message: format!("unexpected character {:?}", other as char),
                })
            }
        };
        Ok(Token { kind, line, col })
    }

    fn lex_ident(&mut self, line: usize, col: usize) -> Token {
        let start = self.pos;
        while let Some(c) = self.peek() {
            if c.is_ascii_alphanumeric() || c == b'_' {
                self.advance();
            } else {
                break;
            }
        }
        let s = std::str::from_utf8(&self.src[start..self.pos])
            .expect("ASCII-only identifier")
            .to_string();
        let kind = match s.as_str() {
            "OPENQASM" => Tok::Openqasm,
            "include" => Tok::Include,
            "qreg" => Tok::Qreg,
            "creg" => Tok::Creg,
            "gate" => Tok::Gate,
            "opaque" => Tok::Opaque,
            "barrier" => Tok::Barrier,
            "measure" => Tok::Measure,
            "reset" => Tok::Reset,
            "if" => Tok::If,
            "qubit" => Tok::Qubit,
            "bit" => Tok::Bit,
            "else" => Tok::Else,
            "for" => Tok::For,
            "while" => Tok::While,
            "box" => Tok::Box_,
            "def" => Tok::Def,
            "switch" => Tok::Switch,
            "case" => Tok::Case_,
            "default" => Tok::Default_,
            "int" => Tok::Int_,
            "sin" => Tok::Sin,
            "cos" => Tok::Cos,
            "tan" => Tok::Tan,
            "exp" => Tok::Exp,
            "ln" => Tok::Ln,
            "sqrt" => Tok::Sqrt,
            "pi" => Tok::Pi,
            _ => Tok::Ident(s),
        };
        Token { kind, line, col }
    }

    fn lex_number(&mut self, line: usize, col: usize) -> QasmResult<Token> {
        let start = self.pos;
        let mut has_dot = false;
        let mut has_exp = false;
        while let Some(c) = self.peek() {
            if c.is_ascii_digit() {
                self.advance();
            } else if c == b'.' && !has_dot && !has_exp {
                has_dot = true;
                self.advance();
            } else if (c == b'e' || c == b'E') && !has_exp {
                has_exp = true;
                self.advance();
                if let Some(next) = self.peek() {
                    if next == b'+' || next == b'-' {
                        self.advance();
                    }
                }
            } else {
                break;
            }
        }
        let s = std::str::from_utf8(&self.src[start..self.pos]).expect("ASCII-only number");
        let kind = if has_dot || has_exp {
            Tok::Real(s.parse::<f64>().map_err(|e| QasmError::Lex {
                line,
                col,
                message: format!("invalid real {s:?}: {e}"),
            })?)
        } else {
            Tok::Int(s.parse::<i64>().map_err(|e| QasmError::Lex {
                line,
                col,
                message: format!("invalid integer {s:?}: {e}"),
            })?)
        };
        Ok(Token { kind, line, col })
    }

    fn lex_string(&mut self, line: usize, col: usize) -> QasmResult<Token> {
        self.advance(); // 시작 따옴표
        let start = self.pos;
        while let Some(c) = self.peek() {
            if c == b'"' {
                let s = std::str::from_utf8(&self.src[start..self.pos])
                    .map_err(|e| QasmError::Lex {
                        line,
                        col,
                        message: format!("non-utf8 string: {e}"),
                    })?
                    .to_string();
                self.advance(); // 끝 따옴표
                return Ok(Token {
                    kind: Tok::Str(s),
                    line,
                    col,
                });
            }
            if c == b'\n' {
                return Err(QasmError::Lex {
                    line,
                    col,
                    message: "unterminated string literal".into(),
                });
            }
            self.advance();
        }
        Err(QasmError::Lex {
            line,
            col,
            message: "unterminated string literal at EOF".into(),
        })
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn kinds(src: &str) -> Vec<Tok> {
        Lexer::new(src)
            .tokenize()
            .unwrap()
            .into_iter()
            .map(|t| t.kind)
            .collect()
    }

    #[test]
    fn test_basic_tokens() {
        let toks = kinds("OPENQASM 2.0;\ninclude \"qelib1.inc\";");
        assert_eq!(
            toks,
            vec![
                Tok::Openqasm,
                Tok::Real(2.0),
                Tok::Semicolon,
                Tok::Include,
                Tok::Str("qelib1.inc".into()),
                Tok::Semicolon,
                Tok::Eof,
            ]
        );
    }

    #[test]
    fn test_qreg_creg_gate_call() {
        let toks = kinds("qreg q[3]; creg c[3]; h q[0]; cx q[0],q[1];");
        let expected = vec![
            Tok::Qreg,
            Tok::Ident("q".into()),
            Tok::LBracket,
            Tok::Int(3),
            Tok::RBracket,
            Tok::Semicolon,
            Tok::Creg,
            Tok::Ident("c".into()),
            Tok::LBracket,
            Tok::Int(3),
            Tok::RBracket,
            Tok::Semicolon,
            Tok::Ident("h".into()),
            Tok::Ident("q".into()),
            Tok::LBracket,
            Tok::Int(0),
            Tok::RBracket,
            Tok::Semicolon,
            Tok::Ident("cx".into()),
            Tok::Ident("q".into()),
            Tok::LBracket,
            Tok::Int(0),
            Tok::RBracket,
            Tok::Comma,
            Tok::Ident("q".into()),
            Tok::LBracket,
            Tok::Int(1),
            Tok::RBracket,
            Tok::Semicolon,
            Tok::Eof,
        ];
        assert_eq!(toks, expected);
    }

    #[test]
    fn test_real_number_with_exp() {
        let toks = kinds("rx(1.5e-3) q[0];");
        assert_eq!(
            toks,
            vec![
                Tok::Ident("rx".into()),
                Tok::LParen,
                Tok::Real(1.5e-3),
                Tok::RParen,
                Tok::Ident("q".into()),
                Tok::LBracket,
                Tok::Int(0),
                Tok::RBracket,
                Tok::Semicolon,
                Tok::Eof,
            ]
        );
    }

    #[test]
    fn test_pi_keyword_and_arithmetic() {
        let toks = kinds("rx(pi/2 + 0.5) q[0];");
        assert!(toks.contains(&Tok::Pi));
        assert!(toks.contains(&Tok::Slash));
        assert!(toks.contains(&Tok::Plus));
    }

    #[test]
    fn test_arrow_and_eqeq() {
        let toks = kinds("measure q[0] -> c[0]; if (c == 1) x q[0];");
        assert!(toks.contains(&Tok::Arrow));
        assert!(toks.contains(&Tok::EqEq));
        assert!(toks.contains(&Tok::Measure));
        assert!(toks.contains(&Tok::If));
    }

    #[test]
    fn test_comment_skip() {
        let toks = kinds("// foo bar\n  h q[0]; // trailing\nx q[0];");
        let n_h = toks
            .iter()
            .filter(|t| matches!(t, Tok::Ident(s) if s == "h"))
            .count();
        let n_x = toks
            .iter()
            .filter(|t| matches!(t, Tok::Ident(s) if s == "x"))
            .count();
        assert_eq!(n_h, 1);
        assert_eq!(n_x, 1);
    }

    #[test]
    fn test_qasm3_keywords() {
        let toks = kinds("qubit[2] q; bit[2] c;");
        assert!(toks.contains(&Tok::Qubit));
        assert!(toks.contains(&Tok::Bit));
    }

    #[test]
    fn test_unterminated_string_errors() {
        let r = Lexer::new("include \"foo").tokenize();
        assert!(matches!(r, Err(QasmError::Lex { .. })));
    }

    #[test]
    fn test_unexpected_char_errors() {
        let r = Lexer::new("h q[0] @").tokenize();
        assert!(matches!(r, Err(QasmError::Lex { .. })));
    }
}
