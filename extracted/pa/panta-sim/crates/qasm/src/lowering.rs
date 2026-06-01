//! AST → simulator [`Circuit`] 변환.
//!
//! - qreg/creg 선언을 모아 (reg_name → (offset, size)) 맵으로 통합.
//! - gate-decl 들을 user-defined gate 룩업 테이블에 저장.
//! - 게이트 호출은 (a) qelib1/stdgates 표 → (b) user-defined inline → (c) UnknownGate
//!   순으로 dispatch.
//! - v0.4.5: `reset q[i];` → `Circuit::reset`, `if (c == N) gate;` →
//!   `Circuit::c_if_last` 정상 lowering. body 는 정확히 1 개 ApplyGate 만 허용
//!   (broadcast / nested If / Reset / Measure 거부).
//! - `opaque`, OpenQASM 3.0 의 `for`/`while`/`box`/`def` 는 여전히 UnsupportedFeature.
//!
//! [`Circuit`]: qsim_simulator::Circuit

use std::collections::HashMap;

use qsim_simulator::Circuit;

use crate::ast::*;
use crate::error::{QasmError, QasmResult};
use crate::gates_lib::apply_named_gate;

const MAX_INLINE_DEPTH: usize = 16;

#[derive(Debug, Clone)]
struct RegInfo {
    offset: usize,
    size: usize,
}

pub fn lower_program(program: Program) -> QasmResult<Circuit> {
    // ----- 1단계: qreg/creg/gate-decl 수집 -----
    let mut qregs: HashMap<String, RegInfo> = HashMap::new();
    let mut cregs: HashMap<String, RegInfo> = HashMap::new();
    let mut gate_decls: HashMap<String, GateDecl> = HashMap::new();
    let mut total_qubits = 0usize;
    let mut total_cbits = 0usize;
    let mut allowed_includes_seen = false;

    for stmt in &program.stmts {
        match stmt {
            Stmt::Include { file, line, col } => {
                // qelib1.inc / stdgates.inc 만 인식. 다른 파일은 error.
                if file != "qelib1.inc" && file != "stdgates.inc" {
                    return Err(QasmError::UnsupportedFeature {
                        message: format!(
                            "include of {file:?} at line {line}:{col} not supported (only qelib1.inc / stdgates.inc)"
                        ),
                        planned_for: "v0.4+",
                    });
                }
                allowed_includes_seen = true;
            }
            Stmt::QregDecl { name, size } => {
                if qregs.contains_key(name) {
                    return Err(QasmError::Lower {
                        message: format!("duplicate qreg/qubit declaration {name:?}"),
                    });
                }
                qregs.insert(
                    name.clone(),
                    RegInfo {
                        offset: total_qubits,
                        size: *size,
                    },
                );
                total_qubits += size;
            }
            Stmt::CregDecl { name, size } => {
                if cregs.contains_key(name) {
                    return Err(QasmError::Lower {
                        message: format!("duplicate creg/bit declaration {name:?}"),
                    });
                }
                cregs.insert(
                    name.clone(),
                    RegInfo {
                        offset: total_cbits,
                        size: *size,
                    },
                );
                total_cbits += size;
            }
            Stmt::GateDecl(decl) => {
                if gate_decls.contains_key(&decl.name) {
                    return Err(QasmError::Lower {
                        message: format!("duplicate gate definition {:?}", decl.name),
                    });
                }
                gate_decls.insert(decl.name.clone(), decl.clone());
            }
            Stmt::OpaqueDecl { name, line, col } => {
                return Err(QasmError::UnsupportedFeature {
                    message: format!(
                        "opaque gate declaration {name:?} at line {line}:{col} not supported"
                    ),
                    planned_for: "v0.5",
                });
            }
            _ => {}
        }
    }
    let _ = allowed_includes_seen; // 현재는 검사만. v0.4 에서 strict mode option.

    let mut circuit = Circuit::new(total_qubits);

    // ----- 2단계: 본문 lowering -----
    for stmt in &program.stmts {
        match stmt {
            Stmt::Include { .. }
            | Stmt::QregDecl { .. }
            | Stmt::CregDecl { .. }
            | Stmt::GateDecl(_)
            | Stmt::OpaqueDecl { .. } => {} // 이미 처리.
            Stmt::Barrier { .. } => {} // no-op.
            Stmt::GateCall(call) => {
                lower_gate_call(&mut circuit, call, &qregs, &gate_decls, &Env::empty(), 0)?;
            }
            Stmt::Measure {
                qubit,
                cbit,
                line,
                col,
            } => {
                let q = resolve_qarg(qubit, &qregs).map_err(|e| with_loc(e, *line, *col))?;
                let c = resolve_carg(cbit, &cregs).map_err(|e| with_loc(e, *line, *col))?;
                if q.len() != c.len() {
                    return Err(QasmError::Lower {
                        message: format!(
                            "measure at line {line}:{col}: qubit/cbit broadcast size mismatch ({} vs {})",
                            q.len(),
                            c.len()
                        ),
                    });
                }
                for (qi, ci) in q.into_iter().zip(c) {
                    circuit.measure(qi, ci);
                }
            }
            Stmt::Reset { qarg, line, col } => {
                let qs = resolve_qarg(qarg, &qregs).map_err(|e| with_loc(e, *line, *col))?;
                for q in qs {
                    circuit.reset(q);
                }
            }
            Stmt::If {
                creg,
                value,
                body,
                line,
                col,
            } => {
                lower_if(
                    &mut circuit,
                    creg,
                    *value,
                    body,
                    &qregs,
                    &cregs,
                    &gate_decls,
                    *line,
                    *col,
                )?;
            }
            Stmt::IfElse {
                creg: cname,
                value,
                then_body,
                else_body,
                line,
                col,
            } => {
                lower_if_else(
                    &mut circuit,
                    cname,
                    *value,
                    then_body,
                    else_body.as_deref(),
                    &qregs,
                    &cregs,
                    &gate_decls,
                    *line,
                    *col,
                )?;
            }
            Stmt::WhileLoop {
                creg: cname,
                value,
                body,
                line,
                col,
            } => {
                lower_while_loop(
                    &mut circuit,
                    cname,
                    *value,
                    body,
                    &qregs,
                    &cregs,
                    &gate_decls,
                    *line,
                    *col,
                )?;
            }
            Stmt::ForLoop {
                var,
                low,
                high,
                body,
                line,
                col,
            } => {
                lower_for_loop(
                    &mut circuit,
                    var,
                    *low,
                    *high,
                    body,
                    &qregs,
                    &cregs,
                    &gate_decls,
                    *line,
                    *col,
                )?;
            }
            Stmt::Switch {
                creg: cname,
                cases,
                line,
                col,
            } => {
                lower_switch(
                    &mut circuit,
                    cname,
                    cases,
                    &qregs,
                    &cregs,
                    &gate_decls,
                    *line,
                    *col,
                )?;
            }
            Stmt::UnsupportedV3 { keyword, line, col } => {
                return Err(QasmError::UnsupportedFeature {
                    message: format!(
                        "OpenQASM 3.0 '{keyword}' (dynamic circuits) at line {line}:{col}"
                    ),
                    planned_for: "v0.5",
                });
            }
        }
    }

    Ok(circuit)
}

/// v0.4.7: stmts 시퀀스를 별도 sub-circuit 에 lowering 한 뒤 그 instructions
/// 를 반환.  block control flow 의 body 처리에 사용.  nested IfElse/While/For/
/// Switch / Reset / Measure / GateCall 모두 가능.
#[allow(clippy::too_many_arguments)]
fn lower_block_to_instructions(
    stmts: &[Stmt],
    n_qubits: usize,
    qregs: &HashMap<String, RegInfo>,
    cregs: &HashMap<String, RegInfo>,
    gate_decls: &HashMap<String, GateDecl>,
) -> QasmResult<Vec<qsim_simulator::Instruction>> {
    let mut sub = Circuit::new(n_qubits);
    for stmt in stmts {
        lower_stmt_into(&mut sub, stmt, qregs, cregs, gate_decls)?;
    }
    Ok(sub.instructions().to_vec())
}

/// 단일 statement 를 lowering 하여 회로에 instruction 들을 push.
///
/// `lower_program` 의 본문 루프와 동일 dispatch.  block 안에서는 `Include`
/// / `QregDecl` / `CregDecl` / `GateDecl` / `OpaqueDecl` 가 안 나와야 정상
/// (parser 가 이미 거부).
#[allow(clippy::too_many_arguments)]
fn lower_stmt_into(
    circuit: &mut Circuit,
    stmt: &Stmt,
    qregs: &HashMap<String, RegInfo>,
    cregs: &HashMap<String, RegInfo>,
    gate_decls: &HashMap<String, GateDecl>,
) -> QasmResult<()> {
    match stmt {
        Stmt::Include { .. }
        | Stmt::QregDecl { .. }
        | Stmt::CregDecl { .. }
        | Stmt::GateDecl(_)
        | Stmt::OpaqueDecl { .. } => Ok(()),
        Stmt::Barrier { .. } => Ok(()),
        Stmt::GateCall(call) => lower_gate_call(circuit, call, qregs, gate_decls, &Env::empty(), 0),
        Stmt::Measure {
            qubit,
            cbit,
            line,
            col,
        } => {
            let q = resolve_qarg(qubit, qregs).map_err(|e| with_loc(e, *line, *col))?;
            let c = resolve_carg(cbit, cregs).map_err(|e| with_loc(e, *line, *col))?;
            if q.len() != c.len() {
                return Err(QasmError::Lower {
                    message: format!(
                        "measure at line {line}:{col}: qubit/cbit broadcast size mismatch ({} vs {})",
                        q.len(),
                        c.len()
                    ),
                });
            }
            for (qq, cc) in q.iter().zip(c.iter()) {
                circuit.measure(*qq, *cc);
            }
            Ok(())
        }
        Stmt::Reset { qarg, line, col } => {
            let qs = resolve_qarg(qarg, qregs).map_err(|e| with_loc(e, *line, *col))?;
            for q in qs {
                circuit.reset(q);
            }
            Ok(())
        }
        Stmt::If {
            creg,
            value,
            body,
            line,
            col,
        } => lower_if(
            circuit, creg, *value, body, qregs, cregs, gate_decls, *line, *col,
        ),
        Stmt::IfElse {
            creg,
            value,
            then_body,
            else_body,
            line,
            col,
        } => lower_if_else(
            circuit,
            creg,
            *value,
            then_body,
            else_body.as_deref(),
            qregs,
            cregs,
            gate_decls,
            *line,
            *col,
        ),
        Stmt::WhileLoop {
            creg,
            value,
            body,
            line,
            col,
        } => lower_while_loop(
            circuit, creg, *value, body, qregs, cregs, gate_decls, *line, *col,
        ),
        Stmt::ForLoop {
            var,
            low,
            high,
            body,
            line,
            col,
        } => lower_for_loop(
            circuit, var, *low, *high, body, qregs, cregs, gate_decls, *line, *col,
        ),
        Stmt::Switch {
            creg,
            cases,
            line,
            col,
        } => lower_switch(circuit, creg, cases, qregs, cregs, gate_decls, *line, *col),
        Stmt::UnsupportedV3 { keyword, line, col } => Err(QasmError::UnsupportedFeature {
            message: format!("OpenQASM 3.0 '{keyword}' (dynamic circuits) at line {line}:{col}"),
            planned_for: "v0.5",
        }),
    }
}

/// v0.4.7: block-form `if (c==N) { ... } else { ... }` lowering.
#[allow(clippy::too_many_arguments)]
fn lower_if_else(
    circuit: &mut Circuit,
    creg_name: &str,
    value: i64,
    then_body: &[Stmt],
    else_body: Option<&[Stmt]>,
    qregs: &HashMap<String, RegInfo>,
    cregs: &HashMap<String, RegInfo>,
    gate_decls: &HashMap<String, GateDecl>,
    line: usize,
    col: usize,
) -> QasmResult<()> {
    let info = cregs
        .get(creg_name)
        .ok_or_else(|| QasmError::IfCregUndefined {
            line,
            col,
            name: creg_name.to_string(),
        })?;
    let max_value: u64 = if info.size >= 64 {
        u64::MAX
    } else {
        (1u64 << info.size) - 1
    };
    if value < 0 || (value as u64) > max_value {
        return Err(QasmError::IfValueOutOfRange {
            line,
            col,
            value,
            max: max_value,
        });
    }
    let cbit_indices: Vec<usize> = (info.offset..info.offset + info.size).collect();
    let n_qubits = circuit.num_qubits();
    let then_insts = lower_block_to_instructions(then_body, n_qubits, qregs, cregs, gate_decls)?;
    let else_insts = match else_body {
        Some(stmts) => Some(lower_block_to_instructions(
            stmts, n_qubits, qregs, cregs, gate_decls,
        )?),
        None => None,
    };
    circuit.add_if_else(cbit_indices, value as u64, then_insts, else_insts);
    Ok(())
}

/// v0.4.7: `while (c == N) { ... }` lowering.  max_iters 는 256 (panta 디폴트).
#[allow(clippy::too_many_arguments)]
fn lower_while_loop(
    circuit: &mut Circuit,
    creg_name: &str,
    value: i64,
    body: &[Stmt],
    qregs: &HashMap<String, RegInfo>,
    cregs: &HashMap<String, RegInfo>,
    gate_decls: &HashMap<String, GateDecl>,
    line: usize,
    col: usize,
) -> QasmResult<()> {
    let info = cregs
        .get(creg_name)
        .ok_or_else(|| QasmError::IfCregUndefined {
            line,
            col,
            name: creg_name.to_string(),
        })?;
    if value < 0 {
        return Err(QasmError::IfValueOutOfRange {
            line,
            col,
            value,
            max: 0,
        });
    }
    let cbit_indices: Vec<usize> = (info.offset..info.offset + info.size).collect();
    let n_qubits = circuit.num_qubits();
    let body_insts = lower_block_to_instructions(body, n_qubits, qregs, cregs, gate_decls)?;
    circuit.add_while_loop(cbit_indices, value as u64, body_insts, 256);
    Ok(())
}

/// v0.4.7: `for var in [low:high] { ... }` lowering — body 를 (high-low+1) 회 반복.
/// loop var 가 body 안 게이트 인자로 사용되면 (현재) error — panta-sim 의
/// fixed-body ForLoop 와 호환 불가.  사용자가 unroll 한 회로로 바꿔야.
#[allow(clippy::too_many_arguments)]
fn lower_for_loop(
    circuit: &mut Circuit,
    _var: &str,
    low: i64,
    high: i64,
    body: &[Stmt],
    qregs: &HashMap<String, RegInfo>,
    cregs: &HashMap<String, RegInfo>,
    gate_decls: &HashMap<String, GateDecl>,
    line: usize,
    col: usize,
) -> QasmResult<()> {
    if high < low {
        // 빈 시퀀스 — for body 0 회 (no-op).
        return Ok(());
    }
    let iterations = (high - low + 1) as usize;
    let n_qubits = circuit.num_qubits();
    let body_insts = lower_block_to_instructions(body, n_qubits, qregs, cregs, gate_decls)
        .map_err(|e| with_loc(e, line, col))?;
    circuit.add_for_loop(iterations, body_insts);
    Ok(())
}

/// v0.4.7: `switch (c) { case N { ... } default { ... } }` lowering.
#[allow(clippy::too_many_arguments)]
fn lower_switch(
    circuit: &mut Circuit,
    creg_name: &str,
    cases: &[(crate::ast::SwitchLabel, Vec<Stmt>)],
    qregs: &HashMap<String, RegInfo>,
    cregs: &HashMap<String, RegInfo>,
    gate_decls: &HashMap<String, GateDecl>,
    line: usize,
    col: usize,
) -> QasmResult<()> {
    let info = cregs
        .get(creg_name)
        .ok_or_else(|| QasmError::IfCregUndefined {
            line,
            col,
            name: creg_name.to_string(),
        })?;
    let cbit_indices: Vec<usize> = (info.offset..info.offset + info.size).collect();
    let n_qubits = circuit.num_qubits();
    let mut rust_cases: Vec<(Option<u64>, Vec<qsim_simulator::Instruction>)> = Vec::new();
    for (label, body) in cases {
        let body_insts = lower_block_to_instructions(body, n_qubits, qregs, cregs, gate_decls)?;
        let label_u = match label {
            crate::ast::SwitchLabel::Value(v) => {
                if *v < 0 {
                    return Err(QasmError::IfValueOutOfRange {
                        line,
                        col,
                        value: *v,
                        max: 0,
                    });
                }
                Some(*v as u64)
            }
            crate::ast::SwitchLabel::Default => None,
        };
        rust_cases.push((label_u, body_insts));
    }
    circuit.add_switch(cbit_indices, rust_cases);
    Ok(())
}

/// `if (creg == value) body` 의 body 를 lowering 후 `c_if_last` 로 wrap.
///
/// body 는 단일 [`Stmt::GateCall`] 만 허용. user-defined gate inline 으로 N 개의
/// instruction 이 발생하면 [`QasmError::IfBodyNotSingleGate`].
#[allow(clippy::too_many_arguments)]
fn lower_if(
    circuit: &mut Circuit,
    creg_name: &str,
    value: i64,
    body: &Stmt,
    qregs: &HashMap<String, RegInfo>,
    cregs: &HashMap<String, RegInfo>,
    gate_decls: &HashMap<String, GateDecl>,
    line: usize,
    col: usize,
) -> QasmResult<()> {
    // 1. creg 조회 (offset, size).
    let info = cregs
        .get(creg_name)
        .ok_or_else(|| QasmError::IfCregUndefined {
            line,
            col,
            name: creg_name.to_string(),
        })?;
    // 2. value 검증.
    let max_value: u64 = if info.size >= 64 {
        u64::MAX
    } else {
        (1u64 << info.size) - 1
    };
    if value < 0 || (value as u64) > max_value {
        return Err(QasmError::IfValueOutOfRange {
            line,
            col,
            value,
            max: max_value,
        });
    }
    // 3. body 가 GateCall 이어야. (Reset / Measure / nested If / Block 거부)
    let call = match body {
        Stmt::GateCall(c) => c,
        _ => {
            return Err(QasmError::IfBodyNotSingleGate {
                line,
                col,
                instructions: 0,
            });
        }
    };
    // 4. body lowering 전후의 instruction 수 차이가 정확히 1 이어야.
    let before = circuit.instructions().len();
    lower_gate_call(circuit, call, qregs, gate_decls, &Env::empty(), 0)?;
    let added = circuit.instructions().len() - before;
    if added != 1 {
        // 부분 lowering 결과를 되돌릴 수 있게 truncate.
        circuit.instructions_mut().truncate(before);
        return Err(QasmError::IfBodyNotSingleGate {
            line,
            col,
            instructions: added,
        });
    }
    // 5. cbit indices = creg 의 flat 인덱스 (LSB = info.offset).
    let cbit_indices: Vec<usize> = (info.offset..info.offset + info.size).collect();
    circuit.c_if_last(cbit_indices, value as u64);
    Ok(())
}

/// 게이트 호출 lowering. user-defined gate 일 경우 inline 확장한다.
#[allow(clippy::only_used_in_recursion)]
fn lower_gate_call(
    circuit: &mut Circuit,
    call: &GateCall,
    qregs: &HashMap<String, RegInfo>,
    gate_decls: &HashMap<String, GateDecl>,
    env: &Env,
    depth: usize,
) -> QasmResult<()> {
    if depth > MAX_INLINE_DEPTH {
        return Err(QasmError::RecursionLimit {
            name: call.name.clone(),
            limit: MAX_INLINE_DEPTH,
        });
    }

    // 파라미터 평가.
    let params: Vec<f64> = call
        .params
        .iter()
        .map(|e| eval_expr(e, env))
        .collect::<QasmResult<_>>()?;

    // qarg 해석.
    let qargs_resolved: Vec<Vec<usize>> = call
        .qargs
        .iter()
        .map(|q| resolve_qarg_in_env(q, qregs, env))
        .collect::<QasmResult<_>>()?;

    // broadcast 길이 결정.
    let broadcast = determine_broadcast(&qargs_resolved, &call.name, call.line, call.col)?;
    for k in 0..broadcast {
        let qubits: Vec<usize> = qargs_resolved
            .iter()
            .map(|qs| if qs.len() == 1 { qs[0] } else { qs[k] })
            .collect();

        // 1) qelib1/stdgates 표 시도
        if apply_named_gate(circuit, &call.name, &params, &qubits, call.line, call.col)? {
            continue;
        }
        // 2) user-defined gate inline
        if let Some(decl) = gate_decls.get(&call.name) {
            inline_user_gate(
                circuit,
                decl,
                &params,
                &qubits,
                qregs,
                gate_decls,
                depth + 1,
            )?;
            continue;
        }
        // 3) 모르는 게이트
        return Err(QasmError::UnknownGate {
            line: call.line,
            col: call.col,
            name: call.name.clone(),
        });
    }
    Ok(())
}

fn inline_user_gate(
    circuit: &mut Circuit,
    decl: &GateDecl,
    params: &[f64],
    qubits: &[usize],
    qregs: &HashMap<String, RegInfo>,
    gate_decls: &HashMap<String, GateDecl>,
    depth: usize,
) -> QasmResult<()> {
    if params.len() != decl.params.len() {
        return Err(QasmError::Lower {
            message: format!(
                "gate {:?} expected {} parameters, got {}",
                decl.name,
                decl.params.len(),
                params.len()
            ),
        });
    }
    if qubits.len() != decl.qubits.len() {
        return Err(QasmError::ArityMismatch {
            line: decl.line,
            col: decl.col,
            gate: decl.name.clone(),
            expected: decl.qubits.len(),
            got: qubits.len(),
        });
    }
    let mut env = Env::empty();
    for (name, value) in decl.params.iter().zip(params.iter()) {
        env.insert_param(name.clone(), *value);
    }
    for (name, qi) in decl.qubits.iter().zip(qubits.iter()) {
        env.insert_qubit(name.clone(), *qi);
    }
    for inner_call in &decl.body {
        lower_gate_call(circuit, inner_call, qregs, gate_decls, &env, depth)?;
    }
    Ok(())
}

#[derive(Debug, Default)]
struct Env {
    params: HashMap<String, f64>,
    qubits: HashMap<String, usize>,
}

impl Env {
    fn empty() -> Self {
        Self::default()
    }
    fn insert_param(&mut self, name: String, value: f64) {
        self.params.insert(name, value);
    }
    fn insert_qubit(&mut self, name: String, idx: usize) {
        self.qubits.insert(name, idx);
    }
}

/// `Stmt::Measure` 등 외부 호출용 — 단일 qarg → 큐비트 인덱스 리스트.
fn resolve_qarg(q: &QArg, qregs: &HashMap<String, RegInfo>) -> QasmResult<Vec<usize>> {
    resolve_qarg_in_env(q, qregs, &Env::empty())
}

/// gate-decl 본문 내 qubit name → 외부 qubit index 매핑 우선, 없으면 qreg lookup.
fn resolve_qarg_in_env(
    q: &QArg,
    qregs: &HashMap<String, RegInfo>,
    env: &Env,
) -> QasmResult<Vec<usize>> {
    match q {
        QArg::Indexed { reg, idx } => {
            if env.qubits.contains_key(reg) {
                return Err(QasmError::Lower {
                    message: format!("indexed qubit '{reg}[{idx}]' inside gate body not allowed"),
                });
            }
            let info = qregs.get(reg).ok_or_else(|| QasmError::Lower {
                message: format!("undefined qreg/qubit register {reg:?}"),
            })?;
            if *idx >= info.size {
                return Err(QasmError::QubitOutOfRange {
                    qubit: *idx,
                    n_qubits: info.size,
                });
            }
            Ok(vec![info.offset + idx])
        }
        QArg::Whole { reg } => {
            // gate-body 안의 매개변수 이름이면 단일 인덱스 반환.
            if let Some(qi) = env.qubits.get(reg) {
                return Ok(vec![*qi]);
            }
            let info = qregs.get(reg).ok_or_else(|| QasmError::Lower {
                message: format!("undefined qreg/qubit register {reg:?}"),
            })?;
            Ok((info.offset..info.offset + info.size).collect())
        }
    }
}

fn resolve_carg(c: &CArg, cregs: &HashMap<String, RegInfo>) -> QasmResult<Vec<usize>> {
    match c {
        CArg::Indexed { reg, idx } => {
            let info = cregs.get(reg).ok_or_else(|| QasmError::Lower {
                message: format!("undefined creg/bit register {reg:?}"),
            })?;
            if *idx >= info.size {
                return Err(QasmError::CbitOutOfRange {
                    cbit: *idx,
                    n_cbits: info.size,
                });
            }
            Ok(vec![info.offset + idx])
        }
        CArg::Whole { reg } => {
            let info = cregs.get(reg).ok_or_else(|| QasmError::Lower {
                message: format!("undefined creg/bit register {reg:?}"),
            })?;
            Ok((info.offset..info.offset + info.size).collect())
        }
    }
}

/// 여러 qarg 가 broadcast (일부는 single-qubit, 일부는 register-whole) 가능 여부 검사.
/// 모두 size-1 이거나, register-whole 들의 size 가 같아야.
fn determine_broadcast(
    qargs: &[Vec<usize>],
    gate: &str,
    line: usize,
    col: usize,
) -> QasmResult<usize> {
    let mut broadcast = 1usize;
    for qs in qargs {
        if qs.len() > 1 {
            if broadcast > 1 && broadcast != qs.len() {
                return Err(QasmError::Lower {
                    message: format!(
                        "gate '{gate}' at line {line}:{col}: broadcast size mismatch ({} vs {})",
                        broadcast,
                        qs.len()
                    ),
                });
            }
            broadcast = qs.len();
        }
    }
    Ok(broadcast)
}

fn with_loc(err: QasmError, line: usize, col: usize) -> QasmError {
    match err {
        QasmError::Lower { message } => QasmError::Lower {
            message: format!("at line {line}:{col}: {message}"),
        },
        e => e,
    }
}

/// 표현식 평가. user-defined gate 안에서는 [`Env`] 의 param 이름을 substitute.
fn eval_expr(e: &Expr, env: &Env) -> QasmResult<f64> {
    match e {
        Expr::Int(n) => Ok(*n as f64),
        Expr::Real(x) => Ok(*x),
        Expr::Pi => Ok(std::f64::consts::PI),
        Expr::Var(name) => env
            .params
            .get(name)
            .copied()
            .ok_or_else(|| QasmError::Lower {
                message: format!("undefined parameter {name:?} in expression"),
            }),
        Expr::Neg(inner) => Ok(-eval_expr(inner, env)?),
        Expr::Bin { op, lhs, rhs } => {
            let l = eval_expr(lhs, env)?;
            let r = eval_expr(rhs, env)?;
            Ok(match op {
                BinOp::Add => l + r,
                BinOp::Sub => l - r,
                BinOp::Mul => l * r,
                BinOp::Div => l / r,
                BinOp::Pow => l.powf(r),
            })
        }
        Expr::Call { fn_, arg } => {
            let v = eval_expr(arg, env)?;
            Ok(match fn_ {
                BuiltinFn::Sin => v.sin(),
                BuiltinFn::Cos => v.cos(),
                BuiltinFn::Tan => v.tan(),
                BuiltinFn::Exp => v.exp(),
                BuiltinFn::Ln => v.ln(),
                BuiltinFn::Sqrt => v.sqrt(),
            })
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::lexer::Lexer;
    use crate::parser::Parser;

    fn lower(src: &str) -> Circuit {
        let toks = Lexer::new(src).tokenize().unwrap();
        let prog = Parser::new(toks).parse_program().unwrap();
        lower_program(prog).unwrap()
    }

    #[test]
    fn test_bell_basic() {
        let c = lower("OPENQASM 2.0; include \"qelib1.inc\"; qreg q[2]; h q[0]; cx q[0], q[1];");
        assert_eq!(c.num_qubits(), 2);
        assert_eq!(c.instructions().len(), 2);
    }

    #[test]
    fn test_two_qregs_offsets() {
        let c = lower("OPENQASM 2.0; qreg a[2]; qreg b[3]; h a[0]; h b[2];");
        assert_eq!(c.num_qubits(), 5);
    }

    #[test]
    fn test_user_defined_gate_inline() {
        let c = lower("OPENQASM 2.0; qreg q[2]; gate bell a, b { h a; cx a, b; } bell q[0], q[1];");
        // bell 호출이 h + cx 두 인스트럭션으로 inline 되어야.
        assert_eq!(c.instructions().len(), 2);
    }

    #[test]
    fn test_parameter_substitution() {
        let c = lower("OPENQASM 2.0; qreg q[1]; gate myrx(a) q { rx(a/2) q; } myrx(pi) q[0];");
        assert_eq!(c.instructions().len(), 1);
    }

    #[test]
    fn test_v3_qubit_decl() {
        let c = lower("OPENQASM 3.0; include \"stdgates.inc\"; qubit[3] q; h q[0]; cx q[0], q[1]; cx q[0], q[2];");
        assert_eq!(c.num_qubits(), 3);
    }

    #[test]
    fn test_measure_emits_instruction() {
        let c = lower(
            "OPENQASM 2.0; qreg q[2]; creg c[2]; h q[0]; cx q[0], q[1]; measure q[0] -> c[0]; measure q[1] -> c[1];",
        );
        assert_eq!(c.num_cbits(), 2);
    }

    #[test]
    fn test_if_lowers_to_c_if_last() {
        // v0.4.5 — `if (c == 1) x q[0];` 는 정상 lowering 된다.
        let c = lower("OPENQASM 2.0; qreg q[1]; creg c[1]; if (c == 1) x q[0];");
        assert_eq!(c.num_cbits(), 1);
        assert_eq!(c.instructions().len(), 1);
        // 마지막 instruction 은 IfEq.
        match c.instructions().last().unwrap() {
            qsim_simulator::Instruction::IfEq {
                cbit_indices,
                value,
                body: _,
            } => {
                assert_eq!(cbit_indices, &[0]);
                assert_eq!(*value, 1);
            }
            other => panic!("expected IfEq, got {other:?}"),
        }
    }

    #[test]
    fn test_reset_lowers_to_reset_instruction() {
        let c = lower("OPENQASM 2.0; qreg q[2]; reset q[0]; reset q[1];");
        assert_eq!(c.num_qubits(), 2);
        assert_eq!(c.instructions().len(), 2);
        for inst in c.instructions() {
            assert!(matches!(inst, qsim_simulator::Instruction::Reset { .. }));
        }
    }

    #[test]
    fn test_reset_register_broadcast() {
        // `reset q;` 는 모든 q 의 reset 으로 broadcast.
        let c = lower("OPENQASM 2.0; qreg q[3]; reset q;");
        assert_eq!(c.instructions().len(), 3);
    }

    #[test]
    fn test_if_multi_bit_creg() {
        let c = lower("OPENQASM 2.0; qreg q[1]; creg c[3]; if (c == 5) x q[0];");
        match c.instructions().last().unwrap() {
            qsim_simulator::Instruction::IfEq {
                cbit_indices,
                value,
                ..
            } => {
                assert_eq!(cbit_indices, &[0, 1, 2]);
                assert_eq!(*value, 5);
            }
            other => panic!("expected IfEq, got {other:?}"),
        }
    }

    #[test]
    fn test_if_undefined_creg_errors() {
        let toks = Lexer::new("OPENQASM 2.0; qreg q[1]; if (c == 1) x q[0];")
            .tokenize()
            .unwrap();
        let prog = Parser::new(toks).parse_program().unwrap();
        let r = lower_program(prog);
        assert!(
            matches!(r, Err(QasmError::IfCregUndefined { .. })),
            "got {r:?}"
        );
    }

    #[test]
    fn test_if_value_out_of_range_errors() {
        // creg c[1] → max value = 1. value=2 거부.
        let toks = Lexer::new("OPENQASM 2.0; qreg q[1]; creg c[1]; if (c == 2) x q[0];")
            .tokenize()
            .unwrap();
        let prog = Parser::new(toks).parse_program().unwrap();
        let r = lower_program(prog);
        assert!(
            matches!(r, Err(QasmError::IfValueOutOfRange { .. })),
            "got {r:?}"
        );
    }

    // 음수 value 는 parser 가 먼저 거부 (`if (c == -1) ...` → Parse error). 그래서
    // lowering 단계의 `value < 0` 검증은 방어적이지만 실제 도달하지 않음.

    #[test]
    fn test_unknown_gate_errors() {
        let toks = Lexer::new("OPENQASM 2.0; qreg q[1]; foo q[0];")
            .tokenize()
            .unwrap();
        let prog = Parser::new(toks).parse_program().unwrap();
        let r = lower_program(prog);
        assert!(matches!(r, Err(QasmError::UnknownGate { .. })));
    }

    #[test]
    fn test_recursive_gate_hits_limit() {
        let toks = Lexer::new("OPENQASM 2.0; qreg q[1]; gate a x { a x; } a q[0];")
            .tokenize()
            .unwrap();
        let prog = Parser::new(toks).parse_program().unwrap();
        let r = lower_program(prog);
        assert!(matches!(r, Err(QasmError::RecursionLimit { .. })));
    }

    #[test]
    fn test_duplicate_qargs_cx_rejected_v0_5_20() {
        // v0.6.2: cx q[0], q[0]; 같은 입력은 controlled-update 가 silent corruption
        // 을 일으키므로 lowering 단계에서 거부.
        let toks = Lexer::new("OPENQASM 2.0; qreg q[1]; cx q[0], q[0];")
            .tokenize()
            .unwrap();
        let prog = Parser::new(toks).parse_program().unwrap();
        let r = lower_program(prog);
        assert!(
            matches!(r, Err(QasmError::DuplicateQargs { .. })),
            "expected DuplicateQargs, got {r:?}"
        );
    }

    #[test]
    fn test_duplicate_qargs_swap_rejected_v0_5_20() {
        let toks = Lexer::new("OPENQASM 2.0; qreg q[2]; swap q[1], q[1];")
            .tokenize()
            .unwrap();
        let prog = Parser::new(toks).parse_program().unwrap();
        let r = lower_program(prog);
        assert!(matches!(r, Err(QasmError::DuplicateQargs { .. })));
    }

    #[test]
    fn test_duplicate_qargs_ccx_rejected_v0_5_20() {
        let toks = Lexer::new("OPENQASM 2.0; qreg q[2]; ccx q[0], q[0], q[1];")
            .tokenize()
            .unwrap();
        let prog = Parser::new(toks).parse_program().unwrap();
        let r = lower_program(prog);
        assert!(matches!(r, Err(QasmError::DuplicateQargs { .. })));
    }
}
