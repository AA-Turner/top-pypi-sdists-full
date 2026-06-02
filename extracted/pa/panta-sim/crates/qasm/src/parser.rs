//! 재귀 하강 파서. [`Lexer`] 출력을 [`Program`] AST 로 변환한다.
//!
//! OpenQASM 2.0 와 3.0 공통 subset 을 지원한다 (헤더에서 버전 detect 후 declaration
//! syntax 만 다르게 처리).
//!
//! [`Lexer`]: crate::lexer::Lexer
//! [`Program`]: crate::ast::Program

use crate::ast::*;
use crate::error::{QasmError, QasmResult};
use crate::lexer::{Tok, Token};

pub struct Parser {
    tokens: Vec<Token>,
    pos: usize,
    /// v0.6.9: 선언된 def 서브루틴의 파라미터 종류 시그니처.  호출
    /// `name(classical_or_qubit, ...)` 의 각 인자를 expr / qarg 중 무엇으로
    /// 파싱할지 결정하는 데 사용 (single-pass — def 는 호출 전에 선언돼야 함).
    defs: std::collections::HashMap<String, Vec<crate::ast::DefParamKind>>,
}

impl Parser {
    pub fn new(tokens: Vec<Token>) -> Self {
        Self {
            tokens,
            pos: 0,
            defs: std::collections::HashMap::new(),
        }
    }

    pub fn parse_program(mut self) -> QasmResult<Program> {
        let version = self.parse_header()?;
        let mut stmts = Vec::new();
        while !self.is_eof() {
            stmts.push(self.parse_stmt(version)?);
        }
        Ok(Program { version, stmts })
    }

    // ---------- helpers ----------

    fn cur(&self) -> &Token {
        &self.tokens[self.pos]
    }

    fn is_eof(&self) -> bool {
        matches!(self.cur().kind, Tok::Eof)
    }

    fn bump(&mut self) -> Token {
        let t = self.tokens[self.pos].clone();
        if self.pos + 1 < self.tokens.len() {
            self.pos += 1;
        }
        t
    }

    fn check(&self, kind: &Tok) -> bool {
        std::mem::discriminant(&self.cur().kind) == std::mem::discriminant(kind)
    }

    fn expect(&mut self, kind: Tok, what: &str) -> QasmResult<Token> {
        if std::mem::discriminant(&self.cur().kind) == std::mem::discriminant(&kind) {
            Ok(self.bump())
        } else {
            let cur = self.cur();
            Err(QasmError::Parse {
                line: cur.line,
                col: cur.col,
                message: format!("expected {what}, got {:?}", cur.kind),
            })
        }
    }

    fn parse_ident(&mut self, what: &str) -> QasmResult<String> {
        let tok = self.cur().clone();
        match tok.kind {
            Tok::Ident(s) => {
                self.bump();
                Ok(s)
            }
            other => Err(QasmError::Parse {
                line: tok.line,
                col: tok.col,
                message: format!("expected {what} identifier, got {other:?}"),
            }),
        }
    }

    fn parse_int(&mut self, what: &str) -> QasmResult<i64> {
        let tok = self.cur().clone();
        match tok.kind {
            Tok::Int(n) => {
                self.bump();
                Ok(n)
            }
            other => Err(QasmError::Parse {
                line: tok.line,
                col: tok.col,
                message: format!("expected {what} integer, got {other:?}"),
            }),
        }
    }

    fn parse_size(&mut self, what: &str) -> QasmResult<usize> {
        let tok = self.cur().clone();
        let n = self.parse_int(what)?;
        if n < 0 {
            return Err(QasmError::Parse {
                line: tok.line,
                col: tok.col,
                message: format!("{what}: size must be non-negative, got {n}"),
            });
        }
        Ok(n as usize)
    }

    // ---------- header ----------

    fn parse_header(&mut self) -> QasmResult<QasmVersion> {
        self.expect(Tok::Openqasm, "'OPENQASM'")?;
        let tok = self.cur().clone();
        let version = match &tok.kind {
            Tok::Real(v) => {
                self.bump();
                if (*v - 2.0).abs() < 1e-9 {
                    QasmVersion::V2
                } else if (*v - 3.0).abs() < 1e-9 {
                    QasmVersion::V3
                } else {
                    return Err(QasmError::Parse {
                        line: tok.line,
                        col: tok.col,
                        message: format!("unsupported OPENQASM version {v}"),
                    });
                }
            }
            Tok::Int(v) => {
                self.bump();
                match v {
                    2 => QasmVersion::V2,
                    3 => QasmVersion::V3,
                    other => {
                        return Err(QasmError::Parse {
                            line: tok.line,
                            col: tok.col,
                            message: format!("unsupported OPENQASM version {other}"),
                        });
                    }
                }
            }
            other => {
                return Err(QasmError::Parse {
                    line: tok.line,
                    col: tok.col,
                    message: format!("expected version number after OPENQASM, got {other:?}"),
                });
            }
        };
        self.expect(Tok::Semicolon, "';'")?;
        Ok(version)
    }

    // ---------- statements ----------

    fn parse_stmt(&mut self, version: QasmVersion) -> QasmResult<Stmt> {
        let tok = self.cur().clone();
        match tok.kind {
            Tok::Include => self.parse_include(),
            Tok::Qreg => self.parse_qreg_decl(),
            Tok::Creg => self.parse_creg_decl(),
            Tok::Qubit => self.parse_qubit_decl(),
            Tok::Bit => self.parse_bit_decl(),
            Tok::Gate => self.parse_gate_decl(version),
            Tok::Opaque => self.parse_opaque_decl(),
            Tok::Barrier => self.parse_barrier(),
            Tok::Measure => self.parse_measure(),
            Tok::Reset => self.parse_reset(),
            Tok::If => self.parse_if(version),
            // v0.4.7: 3.0 block control flow.  V2 dialect 면 lowering 단계에서 거부.
            Tok::For => self.parse_for_loop(version),
            Tok::While => self.parse_while_loop(version),
            Tok::Switch => self.parse_switch(version),
            Tok::Box_ => self.parse_box(version),
            Tok::Def => self.parse_def(version),
            Tok::Else => self.parse_unsupported_v3("else"),
            Tok::Ident(ref name) => {
                // v0.6.9: 선언된 def 서브루틴 호출이면 mixed-arg 파서로.
                if self.defs.contains_key(name) {
                    self.parse_def_call()
                } else if self.is_assignment_measure() {
                    // 3.0 assignment-form measurement: `c[i] = measure q[j];` 또는 `c = measure q;`.
                    self.parse_assignment_measure()
                } else {
                    // 일반 gate-call (`h q[0];`).
                    self.parse_gate_call_stmt()
                }
            }
            other => Err(QasmError::Parse {
                line: tok.line,
                col: tok.col,
                message: format!("unexpected token {other:?} at start of statement"),
            }),
        }
    }

    fn parse_include(&mut self) -> QasmResult<Stmt> {
        let kw = self.bump(); // 'include'
        let tok = self.cur().clone();
        let file = match tok.kind {
            Tok::Str(s) => {
                self.bump();
                s
            }
            other => {
                return Err(QasmError::Parse {
                    line: tok.line,
                    col: tok.col,
                    message: format!("expected string after 'include', got {other:?}"),
                });
            }
        };
        self.expect(Tok::Semicolon, "';' after include")?;
        Ok(Stmt::Include {
            file,
            line: kw.line,
            col: kw.col,
        })
    }

    fn parse_qreg_decl(&mut self) -> QasmResult<Stmt> {
        self.bump(); // 'qreg'
        let name = self.parse_ident("qreg name")?;
        self.expect(Tok::LBracket, "'['")?;
        let size = self.parse_size("qreg size")?;
        self.expect(Tok::RBracket, "']'")?;
        self.expect(Tok::Semicolon, "';'")?;
        Ok(Stmt::QregDecl { name, size })
    }

    fn parse_creg_decl(&mut self) -> QasmResult<Stmt> {
        self.bump(); // 'creg'
        let name = self.parse_ident("creg name")?;
        self.expect(Tok::LBracket, "'['")?;
        let size = self.parse_size("creg size")?;
        self.expect(Tok::RBracket, "']'")?;
        self.expect(Tok::Semicolon, "';'")?;
        Ok(Stmt::CregDecl { name, size })
    }

    /// 3.0: `qubit[N] q;` 또는 `qubit q;` (size 1).
    fn parse_qubit_decl(&mut self) -> QasmResult<Stmt> {
        self.bump(); // 'qubit'
        let size = if self.check(&Tok::LBracket) {
            self.bump();
            let n = self.parse_size("qubit size")?;
            self.expect(Tok::RBracket, "']'")?;
            n
        } else {
            1
        };
        let name = self.parse_ident("qubit name")?;
        self.expect(Tok::Semicolon, "';'")?;
        Ok(Stmt::QregDecl { name, size })
    }

    /// 3.0: `bit[N] c;` 또는 `bit c;` (size 1).
    fn parse_bit_decl(&mut self) -> QasmResult<Stmt> {
        self.bump(); // 'bit'
        let size = if self.check(&Tok::LBracket) {
            self.bump();
            let n = self.parse_size("bit size")?;
            self.expect(Tok::RBracket, "']'")?;
            n
        } else {
            1
        };
        let name = self.parse_ident("bit name")?;
        self.expect(Tok::Semicolon, "';'")?;
        Ok(Stmt::CregDecl { name, size })
    }

    fn parse_gate_decl(&mut self, version: QasmVersion) -> QasmResult<Stmt> {
        let kw = self.bump(); // 'gate'
        let name = self.parse_ident("gate name")?;
        let params = if self.check(&Tok::LParen) {
            self.bump();
            let mut ps = Vec::new();
            if !self.check(&Tok::RParen) {
                ps.push(self.parse_ident("gate param")?);
                while self.check(&Tok::Comma) {
                    self.bump();
                    ps.push(self.parse_ident("gate param")?);
                }
            }
            self.expect(Tok::RParen, "')'")?;
            ps
        } else {
            Vec::new()
        };
        let mut qubits = Vec::new();
        qubits.push(self.parse_ident("gate qubit")?);
        while self.check(&Tok::Comma) {
            self.bump();
            qubits.push(self.parse_ident("gate qubit")?);
        }
        self.expect(Tok::LBrace, "'{'")?;
        let mut body = Vec::new();
        while !self.check(&Tok::RBrace) && !self.is_eof() {
            // body 안에서는 gate-call 만 허용. barrier 는 무시 (Qiskit 도 emit).
            if self.check(&Tok::Barrier) {
                let _ = self.parse_barrier()?;
                continue;
            }
            // identifier 로 시작하는 gate-call 만 받는다.
            if let Tok::Ident(_) = self.cur().kind {
                body.push(self.parse_gate_call_inner()?);
            } else {
                let cur = self.cur().clone();
                return Err(QasmError::Parse {
                    line: cur.line,
                    col: cur.col,
                    message: format!(
                        "expected gate call inside gate definition body, got {:?}",
                        cur.kind
                    ),
                });
            }
        }
        self.expect(Tok::RBrace, "'}'")?;
        let _ = version;
        Ok(Stmt::GateDecl(GateDecl {
            name,
            params,
            qubits,
            body,
            line: kw.line,
            col: kw.col,
        }))
    }

    /// v0.6.9: `def name(typed-params) [-> type]? { gate-body }`.
    ///
    /// 지원: classical (int/float/angle/uint, optional `[N]` width), qubit
    /// (단일), qubit[N] (배열, v0.7.3) 파라미터.  body 는 gate-call 만.  반환
    /// 타입 (`-> ...`) / bit 파라미터는 거부.
    fn parse_def(&mut self, version: QasmVersion) -> QasmResult<Stmt> {
        use crate::ast::{DefDecl, DefParam, DefParamKind};
        let kw = self.bump(); // 'def'
        let name = self.parse_ident("def name")?;
        self.expect(Tok::LParen, "'(' after def name")?;
        let mut params: Vec<DefParam> = Vec::new();
        if !self.check(&Tok::RParen) {
            loop {
                params.push(self.parse_def_param()?);
                if self.check(&Tok::Comma) {
                    self.bump();
                } else {
                    break;
                }
            }
        }
        self.expect(Tok::RParen, "')' after def params")?;
        // optional return type `-> TYPE` — 파싱해서 두지만 lowering 에서 거부.
        let has_return = if self.check(&Tok::Arrow) {
            self.bump();
            // 타입 토큰 1개 (+ optional `[N]`) 소비.
            self.bump();
            if self.check(&Tok::LBracket) {
                while !self.check(&Tok::RBracket) && !self.is_eof() {
                    self.bump();
                }
                self.expect(Tok::RBracket, "']'")?;
            }
            true
        } else {
            false
        };
        self.expect(Tok::LBrace, "'{' after def signature")?;
        // v0.7.3: body 는 일반 문장 (gate-call / measure / reset / control-flow).
        // include / 레지스터·게이트 선언 / 중첩 def 는 거부.
        let mut body = Vec::new();
        while !self.check(&Tok::RBrace) && !self.is_eof() {
            let stmt = self.parse_stmt(version)?;
            match &stmt {
                Stmt::Include { .. }
                | Stmt::QregDecl { .. }
                | Stmt::CregDecl { .. }
                | Stmt::GateDecl(_)
                | Stmt::OpaqueDecl { .. }
                | Stmt::DefDecl(_) => {
                    return Err(QasmError::Parse {
                        line: kw.line,
                        col: kw.col,
                        message: "def body 안에는 gate-call / measure / reset / \
                                  control-flow 만 허용됩니다 (선언 / include / 중첩 def 불가)"
                            .to_string(),
                    });
                }
                _ => body.push(stmt),
            }
        }
        self.expect(Tok::RBrace, "'}'")?;
        let _ = version;
        // 시그니처를 등록해 이후 호출 파싱에서 사용.
        let kinds: Vec<DefParamKind> = params.iter().map(|p| p.kind).collect();
        self.defs.insert(name.clone(), kinds);
        if has_return {
            // 반환값 있는 def 는 미지원 — UnsupportedV3 로 표시해 lowering 에서 친화 에러.
            return Ok(Stmt::UnsupportedV3 {
                keyword: "def (return value)",
                line: kw.line,
                col: kw.col,
            });
        }
        Ok(Stmt::DefDecl(DefDecl {
            name,
            params,
            body,
            line: kw.line,
            col: kw.col,
        }))
    }

    /// def 파라미터 1개: `TYPE [width]? NAME`.
    fn parse_def_param(&mut self) -> QasmResult<crate::ast::DefParam> {
        use crate::ast::{DefParam, DefParamKind};
        let cur = self.cur().clone();
        let is_qubit = matches!(&cur.kind, Tok::Qubit);
        let kind = match &cur.kind {
            Tok::Qubit => {
                self.bump();
                DefParamKind::Qubit
            }
            Tok::Int_ => {
                self.bump();
                DefParamKind::Classical
            }
            Tok::Ident(s) if matches!(s.as_str(), "float" | "angle" | "uint") => {
                self.bump();
                DefParamKind::Classical
            }
            other => {
                return Err(QasmError::Parse {
                    line: cur.line,
                    col: cur.col,
                    message: format!(
                        "def 파라미터 타입은 int/float/angle/uint/qubit 만 지원합니다 (got {other:?})"
                    ),
                });
            }
        };
        // optional width designator `[N]`.  qubit[N] → 배열 파라미터 (v0.7.3),
        // classical 의 width 는 무시.
        let mut array_size: Option<usize> = None;
        if self.check(&Tok::LBracket) {
            self.bump();
            // qubit[N] 은 정수 크기, classical width 도 정수 — 첫 정수만 취하고
            // 나머지 토큰은 ']' 까지 소비.
            if is_qubit {
                array_size = Some(self.parse_size("qubit array size")?);
            }
            while !self.check(&Tok::RBracket) && !self.is_eof() {
                self.bump();
            }
            self.expect(Tok::RBracket, "']'")?;
        }
        let name = self.parse_ident("def param name")?;
        let (kind, size) = if kind == DefParamKind::Qubit && array_size.is_some() {
            (DefParamKind::QubitArray, array_size)
        } else {
            (kind, None)
        };
        Ok(DefParam { kind, name, size })
    }

    /// v0.6.9: def 서브루틴 호출 `name(arg, arg, ...);`.  각 인자는 def 의
    /// 파라미터 종류에 따라 expr (classical) 또는 qarg (qubit) 로 파싱.
    fn parse_def_call(&mut self) -> QasmResult<Stmt> {
        use crate::ast::DefArg;
        let name_tok = self.cur().clone();
        let name = self.parse_ident("def name")?;
        let kinds = self
            .defs
            .get(&name)
            .expect("parse_def_call only on known def")
            .clone();
        self.expect(Tok::LParen, "'(' after def call")?;
        let mut args: Vec<DefArg> = Vec::new();
        if !self.check(&Tok::RParen) {
            let mut idx = 0usize;
            loop {
                let kind = kinds.get(idx).copied();
                match kind {
                    Some(crate::ast::DefParamKind::Qubit)
                    | Some(crate::ast::DefParamKind::QubitArray) => {
                        args.push(DefArg::Qubit(self.parse_qarg()?));
                    }
                    Some(crate::ast::DefParamKind::Classical) => {
                        args.push(DefArg::Classical(self.parse_expr()?));
                    }
                    None => {
                        // 인자 개수 초과 — 일단 expr 로 파싱해 lowering 에서 arity 에러.
                        args.push(DefArg::Classical(self.parse_expr()?));
                    }
                }
                idx += 1;
                if self.check(&Tok::Comma) {
                    self.bump();
                } else {
                    break;
                }
            }
        }
        self.expect(Tok::RParen, "')' after def call args")?;
        self.expect(Tok::Semicolon, "';'")?;
        Ok(Stmt::DefCall {
            name,
            args,
            line: name_tok.line,
            col: name_tok.col,
        })
    }

    fn parse_opaque_decl(&mut self) -> QasmResult<Stmt> {
        let kw = self.bump(); // 'opaque'
        let name = self.parse_ident("opaque name")?;
        // params + qargs skip, semicolon 까지 토큰 소비
        while !self.check(&Tok::Semicolon) && !self.is_eof() {
            self.bump();
        }
        self.expect(Tok::Semicolon, "';'")?;
        Ok(Stmt::OpaqueDecl {
            name,
            line: kw.line,
            col: kw.col,
        })
    }

    fn parse_barrier(&mut self) -> QasmResult<Stmt> {
        self.bump(); // 'barrier'
        let mut qargs = Vec::new();
        // semicolon 까지가 비어 있으면 (qiskit 가 가끔 emit) 허용.
        if !self.check(&Tok::Semicolon) {
            qargs.push(self.parse_qarg()?);
            while self.check(&Tok::Comma) {
                self.bump();
                qargs.push(self.parse_qarg()?);
            }
        }
        self.expect(Tok::Semicolon, "';'")?;
        Ok(Stmt::Barrier { qargs })
    }

    fn parse_measure(&mut self) -> QasmResult<Stmt> {
        let kw = self.bump(); // 'measure'
        let qubit = self.parse_qarg()?;
        self.expect(Tok::Arrow, "'->'")?;
        let cbit = self.parse_carg()?;
        self.expect(Tok::Semicolon, "';'")?;
        Ok(Stmt::Measure {
            qubit,
            cbit,
            line: kw.line,
            col: kw.col,
        })
    }

    /// 3.0 assignment-form 인지 lookahead 로 검사: `IDENT (\[ INT \])? =`.
    fn is_assignment_measure(&self) -> bool {
        let mut p = self.pos;
        if !matches!(self.tokens.get(p).map(|t| &t.kind), Some(Tok::Ident(_))) {
            return false;
        }
        p += 1;
        if matches!(self.tokens.get(p).map(|t| &t.kind), Some(Tok::LBracket)) {
            p += 1;
            if !matches!(self.tokens.get(p).map(|t| &t.kind), Some(Tok::Int(_))) {
                return false;
            }
            p += 1;
            if !matches!(self.tokens.get(p).map(|t| &t.kind), Some(Tok::RBracket)) {
                return false;
            }
            p += 1;
        }
        matches!(self.tokens.get(p).map(|t| &t.kind), Some(Tok::Eq))
    }

    /// `c[i] = measure q[j];` 또는 `c = measure q;` 파싱.
    fn parse_assignment_measure(&mut self) -> QasmResult<Stmt> {
        let start = self.cur().clone();
        let cbit = self.parse_carg()?;
        self.expect(Tok::Eq, "'='")?;
        self.expect(Tok::Measure, "'measure'")?;
        let qubit = self.parse_qarg()?;
        self.expect(Tok::Semicolon, "';'")?;
        Ok(Stmt::Measure {
            qubit,
            cbit,
            line: start.line,
            col: start.col,
        })
    }

    fn parse_reset(&mut self) -> QasmResult<Stmt> {
        let kw = self.bump(); // 'reset'
        let qarg = self.parse_qarg()?;
        self.expect(Tok::Semicolon, "';'")?;
        Ok(Stmt::Reset {
            qarg,
            line: kw.line,
            col: kw.col,
        })
    }

    fn parse_if(&mut self, version: QasmVersion) -> QasmResult<Stmt> {
        let kw = self.bump(); // 'if'
        self.expect(Tok::LParen, "'(' after 'if'")?;
        let creg = self.parse_ident("classical register")?;
        self.expect(Tok::EqEq, "'=='")?;
        let value = self.parse_int("if value")?;
        self.expect(Tok::RParen, "')'")?;

        // v0.4.7: block-form `if (c==N) { stmts } [else { stmts }]` 도 허용.
        if self.check(&Tok::LBrace) {
            let then_body = self.parse_block(version)?;
            let else_body = if self.check(&Tok::Else) {
                self.bump();
                if self.check(&Tok::LBrace) {
                    Some(self.parse_block(version)?)
                } else {
                    // `else if`/`else stmt` 케이스: 단일 statement 를 1-element block 으로.
                    Some(vec![self.parse_stmt(version)?])
                }
            } else {
                None
            };
            return Ok(Stmt::IfElse {
                creg,
                value,
                then_body,
                else_body,
                line: kw.line,
                col: kw.col,
            });
        }

        // 기존 single-statement form (v0.4.5).
        let body = Box::new(self.parse_stmt(version)?);
        Ok(Stmt::If {
            creg,
            value,
            body,
            line: kw.line,
            col: kw.col,
        })
    }

    /// v0.4.7: `while (c == N) { stmts }`.
    fn parse_while_loop(&mut self, version: QasmVersion) -> QasmResult<Stmt> {
        let kw = self.bump(); // 'while'
        self.expect(Tok::LParen, "'(' after 'while'")?;
        let creg = self.parse_ident("classical register")?;
        self.expect(Tok::EqEq, "'=='")?;
        let value = self.parse_int("while value")?;
        self.expect(Tok::RParen, "')'")?;
        let body = self.parse_block(version)?;
        Ok(Stmt::WhileLoop {
            creg,
            value,
            body,
            line: kw.line,
            col: kw.col,
        })
    }

    /// v0.4.7: `for [int] var in [low:high] { stmts }` (high 포함).
    /// - panta-sim 호환: low, high 는 ascending integer 시퀀스만.
    /// - loop variable 은 panta 회로에서 unused — type annotation 도 무시.
    fn parse_for_loop(&mut self, version: QasmVersion) -> QasmResult<Stmt> {
        let kw = self.bump(); // 'for'
                              // optional type annotation `int`
        if matches!(self.cur().kind, Tok::Int_) {
            self.bump();
        }
        let var = self.parse_ident("for-loop variable name")?;
        self.expect_ident_kw("in")?;
        // index set: `[low:high]` 또는 `[low:step:high]` (현재는 단순 [low:high] 만).
        self.expect(Tok::LBracket, "'[' after 'in'")?;
        let low = self.parse_int("for-loop range low")?;
        self.expect(Tok::Colon, "':' between low and high")?;
        let next_int = self.parse_int("for-loop range high")?;
        // [low:step:high] 형식: 다음 ':' 이 있으면 step:high, 아니면 [low:high].
        let high = if self.check(&Tok::Colon) {
            self.bump();
            // step 무시 (panta 의 ForLoop 는 ascending integer 시퀀스만 — step 1 가정).
            // 한 단계 더 parse 해서 high 로 사용.
            self.parse_int("for-loop range high")?
        } else {
            next_int
        };
        self.expect(Tok::RBracket, "']'")?;
        let body = self.parse_block(version)?;
        Ok(Stmt::ForLoop {
            var,
            low,
            high,
            body,
            line: kw.line,
            col: kw.col,
        })
    }

    /// v0.6.8: `box [designator]? { stmts }` (OpenQASM 3.0 §7.7).
    /// panta-sim 은 timing 을 모델링하지 않으므로 optional duration designator
    /// (`[100ns]` 등) 는 파싱 후 버리고, body 를 투명한 블록으로 lowering 한다.
    fn parse_box(&mut self, version: QasmVersion) -> QasmResult<Stmt> {
        let kw = self.bump(); // 'box'
                              // optional duration designator `[...]` — depth-aware skip.
        if self.check(&Tok::LBracket) {
            self.bump();
            let mut depth = 1i32;
            while depth > 0 {
                match self.cur().kind {
                    Tok::LBracket => {
                        depth += 1;
                        self.bump();
                    }
                    Tok::RBracket => {
                        depth -= 1;
                        self.bump();
                    }
                    Tok::Eof => break,
                    _ => {
                        self.bump();
                    }
                }
            }
        }
        let body = self.parse_block(version)?;
        Ok(Stmt::Box {
            body,
            line: kw.line,
            col: kw.col,
        })
    }

    /// v0.4.7: `switch (c) { case N { stmts } ... default { stmts } }`.
    fn parse_switch(&mut self, version: QasmVersion) -> QasmResult<Stmt> {
        let kw = self.bump(); // 'switch'
        self.expect(Tok::LParen, "'(' after 'switch'")?;
        let creg = self.parse_ident("classical register")?;
        self.expect(Tok::RParen, "')'")?;
        self.expect(Tok::LBrace, "'{' after switch (cond)")?;
        let mut cases: Vec<(crate::ast::SwitchLabel, Vec<Stmt>)> = Vec::new();
        loop {
            match self.cur().kind {
                Tok::RBrace => {
                    self.bump();
                    break;
                }
                Tok::Case_ => {
                    self.bump();
                    let v = self.parse_int("case value")?;
                    let body = self.parse_block(version)?;
                    cases.push((crate::ast::SwitchLabel::Value(v), body));
                }
                Tok::Default_ => {
                    self.bump();
                    let body = self.parse_block(version)?;
                    cases.push((crate::ast::SwitchLabel::Default, body));
                }
                _ => {
                    let tok = self.cur().clone();
                    return Err(QasmError::Parse {
                        line: tok.line,
                        col: tok.col,
                        message: format!(
                            "unexpected token {:?} in switch — expected 'case', 'default', or '}}'",
                            tok.kind
                        ),
                    });
                }
            }
        }
        Ok(Stmt::Switch {
            creg,
            cases,
            line: kw.line,
            col: kw.col,
        })
    }

    /// `{ stmt; stmt; ... }` block — closing `}` 까지 statement 들을 수집.
    fn parse_block(&mut self, version: QasmVersion) -> QasmResult<Vec<Stmt>> {
        self.expect(Tok::LBrace, "'{'")?;
        let mut stmts = Vec::new();
        while !self.check(&Tok::RBrace) && !self.check(&Tok::Eof) {
            stmts.push(self.parse_stmt(version)?);
        }
        self.expect(Tok::RBrace, "'}'")?;
        Ok(stmts)
    }

    /// `expect_ident_kw("in")` — 다음 토큰이 정확히 그 식별자(키워드) 인지 검사.
    fn expect_ident_kw(&mut self, kw: &str) -> QasmResult<()> {
        let tok = self.cur().clone();
        match &tok.kind {
            Tok::Ident(s) if s == kw => {
                self.bump();
                Ok(())
            }
            _ => Err(QasmError::Parse {
                line: tok.line,
                col: tok.col,
                message: format!("expected keyword {kw:?}, got {:?}", tok.kind),
            }),
        }
    }

    fn parse_unsupported_v3(&mut self, keyword: &'static str) -> QasmResult<Stmt> {
        let tok = self.bump();
        // 토큰 소비를 ';' 또는 '}' 까지 (간단 skip).
        let mut depth = 0i32;
        loop {
            match self.cur().kind {
                Tok::Semicolon if depth == 0 => {
                    self.bump();
                    break;
                }
                Tok::LBrace => {
                    depth += 1;
                    self.bump();
                }
                Tok::RBrace => {
                    if depth > 0 {
                        depth -= 1;
                        self.bump();
                        if depth == 0 {
                            break;
                        }
                    } else {
                        break;
                    }
                }
                Tok::Eof => break,
                _ => {
                    self.bump();
                }
            }
        }
        Ok(Stmt::UnsupportedV3 {
            keyword,
            line: tok.line,
            col: tok.col,
        })
    }

    fn parse_gate_call_stmt(&mut self) -> QasmResult<Stmt> {
        let call = self.parse_gate_call_inner()?;
        Ok(Stmt::GateCall(call))
    }

    fn parse_gate_call_inner(&mut self) -> QasmResult<GateCall> {
        let tok = self.cur().clone();
        let name = self.parse_ident("gate name")?;
        let params = if self.check(&Tok::LParen) {
            self.bump();
            let mut exprs = Vec::new();
            if !self.check(&Tok::RParen) {
                exprs.push(self.parse_expr()?);
                while self.check(&Tok::Comma) {
                    self.bump();
                    exprs.push(self.parse_expr()?);
                }
            }
            self.expect(Tok::RParen, "')'")?;
            exprs
        } else {
            Vec::new()
        };
        // 일부 게이트 (예: OpenQASM 3 의 `gphase(λ);`) 는 큐비트 인자가 없다.
        // 세미콜론이 바로 따라오면 빈 qargs 로 처리하고, 아니면 적어도 하나 파싱.
        let mut qargs = Vec::new();
        if !self.check(&Tok::Semicolon) {
            qargs.push(self.parse_qarg()?);
            while self.check(&Tok::Comma) {
                self.bump();
                qargs.push(self.parse_qarg()?);
            }
        }
        self.expect(Tok::Semicolon, "';'")?;
        Ok(GateCall {
            name,
            params,
            qargs,
            line: tok.line,
            col: tok.col,
        })
    }

    fn parse_qarg(&mut self) -> QasmResult<QArg> {
        let reg = self.parse_ident("qarg register")?;
        if self.check(&Tok::LBracket) {
            self.bump();
            let idx = self.parse_size("qarg index")?;
            self.expect(Tok::RBracket, "']'")?;
            Ok(QArg::Indexed { reg, idx })
        } else {
            Ok(QArg::Whole { reg })
        }
    }

    fn parse_carg(&mut self) -> QasmResult<CArg> {
        let reg = self.parse_ident("carg register")?;
        if self.check(&Tok::LBracket) {
            self.bump();
            let idx = self.parse_size("carg index")?;
            self.expect(Tok::RBracket, "']'")?;
            Ok(CArg::Indexed { reg, idx })
        } else {
            Ok(CArg::Whole { reg })
        }
    }

    // ---------- expression (Pratt) ----------

    fn parse_expr(&mut self) -> QasmResult<Expr> {
        self.parse_add()
    }

    fn parse_add(&mut self) -> QasmResult<Expr> {
        let mut lhs = self.parse_mul()?;
        loop {
            let op = match self.cur().kind {
                Tok::Plus => BinOp::Add,
                Tok::Minus => BinOp::Sub,
                _ => break,
            };
            self.bump();
            let rhs = self.parse_mul()?;
            lhs = Expr::Bin {
                op,
                lhs: Box::new(lhs),
                rhs: Box::new(rhs),
            };
        }
        Ok(lhs)
    }

    fn parse_mul(&mut self) -> QasmResult<Expr> {
        let mut lhs = self.parse_pow()?;
        loop {
            let op = match self.cur().kind {
                Tok::Star => BinOp::Mul,
                Tok::Slash => BinOp::Div,
                _ => break,
            };
            self.bump();
            let rhs = self.parse_pow()?;
            lhs = Expr::Bin {
                op,
                lhs: Box::new(lhs),
                rhs: Box::new(rhs),
            };
        }
        Ok(lhs)
    }

    fn parse_pow(&mut self) -> QasmResult<Expr> {
        // right-associative: a ^ b ^ c = a ^ (b ^ c)
        let lhs = self.parse_unary()?;
        if matches!(self.cur().kind, Tok::Caret) {
            self.bump();
            let rhs = self.parse_pow()?;
            Ok(Expr::Bin {
                op: BinOp::Pow,
                lhs: Box::new(lhs),
                rhs: Box::new(rhs),
            })
        } else {
            Ok(lhs)
        }
    }

    fn parse_unary(&mut self) -> QasmResult<Expr> {
        match self.cur().kind {
            Tok::Minus => {
                self.bump();
                let inner = self.parse_unary()?;
                Ok(Expr::Neg(Box::new(inner)))
            }
            Tok::Plus => {
                self.bump();
                self.parse_unary()
            }
            _ => self.parse_atom(),
        }
    }

    fn parse_atom(&mut self) -> QasmResult<Expr> {
        let tok = self.cur().clone();
        match tok.kind {
            Tok::Int(n) => {
                self.bump();
                Ok(Expr::Int(n))
            }
            Tok::Real(x) => {
                self.bump();
                Ok(Expr::Real(x))
            }
            Tok::Pi => {
                self.bump();
                Ok(Expr::Pi)
            }
            Tok::Ident(name) => {
                self.bump();
                Ok(Expr::Var(name))
            }
            Tok::LParen => {
                self.bump();
                let e = self.parse_expr()?;
                self.expect(Tok::RParen, "')'")?;
                Ok(e)
            }
            Tok::Sin | Tok::Cos | Tok::Tan | Tok::Exp | Tok::Ln | Tok::Sqrt => {
                self.bump();
                let fn_ = match tok.kind {
                    Tok::Sin => BuiltinFn::Sin,
                    Tok::Cos => BuiltinFn::Cos,
                    Tok::Tan => BuiltinFn::Tan,
                    Tok::Exp => BuiltinFn::Exp,
                    Tok::Ln => BuiltinFn::Ln,
                    Tok::Sqrt => BuiltinFn::Sqrt,
                    _ => unreachable!(),
                };
                self.expect(Tok::LParen, "'(' after function name")?;
                let arg = self.parse_expr()?;
                self.expect(Tok::RParen, "')'")?;
                Ok(Expr::Call {
                    fn_,
                    arg: Box::new(arg),
                })
            }
            other => Err(QasmError::Parse {
                line: tok.line,
                col: tok.col,
                message: format!("expected expression atom, got {other:?}"),
            }),
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::lexer::Lexer;

    fn parse(src: &str) -> Program {
        let toks = Lexer::new(src).tokenize().unwrap();
        Parser::new(toks).parse_program().unwrap()
    }

    #[test]
    fn test_minimal_v2_program() {
        let p = parse("OPENQASM 2.0;\ninclude \"qelib1.inc\";\nqreg q[2];\nh q[0];\ncx q[0],q[1];");
        assert_eq!(p.version, QasmVersion::V2);
        assert_eq!(p.stmts.len(), 4);
        assert!(matches!(p.stmts[0], Stmt::Include { .. }));
        assert!(matches!(p.stmts[1], Stmt::QregDecl { .. }));
        match &p.stmts[2] {
            Stmt::GateCall(g) => assert_eq!(g.name, "h"),
            _ => panic!(),
        }
        match &p.stmts[3] {
            Stmt::GateCall(g) => assert_eq!(g.name, "cx"),
            _ => panic!(),
        }
    }

    #[test]
    fn test_minimal_v3_program() {
        let p = parse("OPENQASM 3.0;\ninclude \"stdgates.inc\";\nqubit[2] q;\nbit[2] c;\nh q[0];\nmeasure q[0] -> c[0];");
        assert_eq!(p.version, QasmVersion::V3);
        match &p.stmts[1] {
            Stmt::QregDecl { name, size } => {
                assert_eq!(name, "q");
                assert_eq!(*size, 2);
            }
            _ => panic!(),
        }
        match &p.stmts[2] {
            Stmt::CregDecl { name, size } => {
                assert_eq!(name, "c");
                assert_eq!(*size, 2);
            }
            _ => panic!(),
        }
    }

    #[test]
    fn test_parameterized_gate() {
        let p = parse("OPENQASM 2.0; qreg q[1]; rx(0.5 + pi/4) q[0];");
        match &p.stmts[1] {
            Stmt::GateCall(g) => {
                assert_eq!(g.name, "rx");
                assert_eq!(g.params.len(), 1);
            }
            _ => panic!(),
        }
    }

    #[test]
    fn test_gate_decl_inlines() {
        let p = parse("OPENQASM 2.0; qreg q[2]; gate bell a, b { h a; cx a, b; } bell q[0], q[1];");
        // 2개 stmt: GateDecl + GateCall
        match &p.stmts[1] {
            Stmt::GateDecl(d) => {
                assert_eq!(d.name, "bell");
                assert_eq!(d.qubits.len(), 2);
                assert_eq!(d.body.len(), 2);
            }
            _ => panic!(),
        }
        match &p.stmts[2] {
            Stmt::GateCall(c) => assert_eq!(c.name, "bell"),
            _ => panic!(),
        }
    }

    #[test]
    fn test_measure_and_if() {
        let p =
            parse("OPENQASM 2.0; qreg q[1]; creg c[1]; measure q[0] -> c[0]; if (c == 1) x q[0];");
        assert!(matches!(p.stmts[2], Stmt::Measure { .. }));
        match &p.stmts[3] {
            Stmt::If {
                creg, value, body, ..
            } => {
                assert_eq!(creg, "c");
                assert_eq!(*value, 1);
                assert!(matches!(**body, Stmt::GateCall(_)));
            }
            _ => panic!(),
        }
    }

    #[test]
    fn test_barrier_with_or_without_args() {
        let p = parse("OPENQASM 2.0; qreg q[2]; barrier q[0], q[1]; barrier q;");
        assert!(matches!(p.stmts[1], Stmt::Barrier { .. }));
        assert!(matches!(p.stmts[2], Stmt::Barrier { .. }));
    }

    #[test]
    fn test_v3_def_parses() {
        // v0.4.7: for / while / switch native.  v0.6.8: box.  v0.6.9: def native.
        let p = parse(
            "OPENQASM 3.0; include \"stdgates.inc\"; qubit q; def foo(qubit a) { h a; } foo(q);",
        );
        assert!(p.stmts.iter().any(|s| matches!(s, Stmt::DefDecl(_))));
        assert!(p.stmts.iter().any(|s| matches!(s, Stmt::DefCall { .. })));
    }

    #[test]
    fn test_v3_def_return_value_marked_unsupported() {
        // 반환값 있는 def 는 UnsupportedV3 로 표시되어 lowering 에서 거부.
        let p = parse("OPENQASM 3.0; qubit q; def f(qubit a) -> bit { h a; }");
        assert!(p.stmts.iter().any(|s| matches!(
            s,
            Stmt::UnsupportedV3 {
                keyword: "def (return value)",
                ..
            }
        )));
    }

    #[test]
    fn test_v068_box_parses() {
        // v0.6.8: box { body } 는 native 파싱.
        let p = parse("OPENQASM 3.0; include \"stdgates.inc\"; qubit q; box { h q; }");
        assert!(p.stmts.iter().any(|s| matches!(s, Stmt::Box { .. })));
    }

    #[test]
    fn test_v047_for_loop_parses() {
        // for type var in [low:high] { body }
        let p =
            parse("OPENQASM 3.0; include \"stdgates.inc\"; qubit q; for int i in [0:2] { h q; }");
        assert!(p.stmts.iter().any(|s| matches!(s, Stmt::ForLoop { .. })));
    }

    #[test]
    fn test_v047_while_loop_parses() {
        let p = parse(
            "OPENQASM 3.0; include \"stdgates.inc\"; qubit q; bit c; while (c == 0) { h q; }",
        );
        assert!(p.stmts.iter().any(|s| matches!(s, Stmt::WhileLoop { .. })));
    }

    #[test]
    fn test_v047_switch_parses() {
        let p = parse(
            "OPENQASM 3.0; include \"stdgates.inc\"; qubit q; bit[2] c; \
             switch (c) { case 0 { h q; } case 1 { x q; } default { id q; } }",
        );
        assert!(p.stmts.iter().any(|s| matches!(s, Stmt::Switch { .. })));
    }

    #[test]
    fn test_v047_if_else_block_form_parses() {
        let p = parse(
            "OPENQASM 3.0; include \"stdgates.inc\"; qubit q; bit c; \
             if (c == 1) { h q; } else { x q; }",
        );
        assert!(p.stmts.iter().any(|s| matches!(s, Stmt::IfElse { .. })));
    }
}
