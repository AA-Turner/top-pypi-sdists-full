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
    let mut def_decls: HashMap<String, DefDecl> = HashMap::new();
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
            Stmt::DefDecl(decl) => {
                if def_decls.contains_key(&decl.name) || gate_decls.contains_key(&decl.name) {
                    return Err(QasmError::Lower {
                        message: format!("duplicate def/gate definition {:?}", decl.name),
                    });
                }
                def_decls.insert(decl.name.clone(), decl.clone());
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
                    &Env::empty(),
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
                    &Env::empty(),
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
                    &Env::empty(),
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
                    &Env::empty(),
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
                    &Env::empty(),
                    *line,
                    *col,
                )?;
            }
            Stmt::Box { body, .. } => {
                // box 는 timing/scope wrapper — body 를 투명하게 직접 lowering.
                for s in body {
                    lower_stmt_into(&mut circuit, s, &qregs, &cregs, &gate_decls, &Env::empty())?;
                }
            }
            Stmt::DefDecl(_) => {} // 이미 pass 1 에서 수집.
            Stmt::DefCall {
                name,
                args,
                line,
                col,
            } => {
                lower_def_call(
                    &mut circuit,
                    name,
                    args,
                    &def_decls,
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
                    planned_for: "v0.7",
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
    env: &Env,
) -> QasmResult<Vec<qsim_simulator::Instruction>> {
    let mut sub = Circuit::new(n_qubits);
    for stmt in stmts {
        lower_stmt_into(&mut sub, stmt, qregs, cregs, gate_decls, env)?;
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
    env: &Env,
) -> QasmResult<()> {
    match stmt {
        Stmt::Include { .. }
        | Stmt::QregDecl { .. }
        | Stmt::CregDecl { .. }
        | Stmt::GateDecl(_)
        | Stmt::OpaqueDecl { .. } => Ok(()),
        Stmt::Barrier { .. } => Ok(()),
        Stmt::GateCall(call) => lower_gate_call(circuit, call, qregs, gate_decls, env, 0),
        Stmt::Measure {
            qubit,
            cbit,
            line,
            col,
        } => {
            let q = resolve_qarg_in_env(qubit, qregs, env).map_err(|e| with_loc(e, *line, *col))?;
            let c = resolve_carg_in_env(cbit, cregs, env).map_err(|e| with_loc(e, *line, *col))?;
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
            let qs = resolve_qarg_in_env(qarg, qregs, env).map_err(|e| with_loc(e, *line, *col))?;
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
            circuit, creg, *value, body, qregs, cregs, gate_decls, env, *line, *col,
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
            env,
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
            circuit, creg, *value, body, qregs, cregs, gate_decls, env, *line, *col,
        ),
        Stmt::ForLoop {
            var,
            low,
            high,
            body,
            line,
            col,
        } => lower_for_loop(
            circuit, var, *low, *high, body, qregs, cregs, gate_decls, env, *line, *col,
        ),
        Stmt::Switch {
            creg,
            cases,
            line,
            col,
        } => lower_switch(
            circuit, creg, cases, qregs, cregs, gate_decls, env, *line, *col,
        ),
        Stmt::Box { body, .. } => {
            for s in body {
                lower_stmt_into(circuit, s, qregs, cregs, gate_decls, env)?;
            }
            Ok(())
        }
        Stmt::DefDecl(_) => Ok(()), // pass 1 수집.
        Stmt::DefCall {
            name, line, col, ..
        } => Err(QasmError::UnsupportedFeature {
            message: format!(
                "def 호출 {name:?} 가 control-flow / box block 안에 있습니다 \
                 (line {line}:{col}) — v0.6.9 는 top-level def 호출만 지원합니다"
            ),
            planned_for: "v0.7",
        }),
        Stmt::UnsupportedV3 { keyword, line, col } => Err(QasmError::UnsupportedFeature {
            message: format!("OpenQASM 3.0 '{keyword}' (dynamic circuits) at line {line}:{col}"),
            planned_for: "v0.7",
        }),
    }
}

/// v0.6.9: def 서브루틴 호출을 인라인 확장한다.  classical 인자는 f64 로
/// 평가해 body 의 angle 표현식에, qubit 인자는 실제 큐비트 인덱스 (단일/배열)
/// 에 바인딩한 [`Env`] 를 만들어 body 문장들을 lowering 한다 (v0.7.3: gate-call
/// 뿐 아니라 measure / reset / control-flow 도 허용).
#[allow(clippy::too_many_arguments)]
fn lower_def_call(
    circuit: &mut Circuit,
    name: &str,
    args: &[DefArg],
    def_decls: &HashMap<String, DefDecl>,
    qregs: &HashMap<String, RegInfo>,
    cregs: &HashMap<String, RegInfo>,
    gate_decls: &HashMap<String, GateDecl>,
    line: usize,
    col: usize,
) -> QasmResult<()> {
    let decl = def_decls.get(name).ok_or_else(|| QasmError::UnknownGate {
        line,
        col,
        name: name.to_string(),
    })?;
    if args.len() != decl.params.len() {
        return Err(QasmError::ArityMismatch {
            line,
            col,
            gate: name.to_string(),
            expected: decl.params.len(),
            got: args.len(),
        });
    }
    let mut env = Env::empty();
    for (param, arg) in decl.params.iter().zip(args.iter()) {
        match (param.kind, arg) {
            (DefParamKind::Classical, DefArg::Classical(expr)) => {
                let value = eval_expr(expr, &Env::empty())?;
                env.insert_param(param.name.clone(), value);
            }
            (DefParamKind::Qubit, DefArg::Qubit(qarg)) => {
                let qs = resolve_qarg(qarg, qregs).map_err(|e| with_loc(e, line, col))?;
                if qs.len() != 1 {
                    return Err(QasmError::Lower {
                        message: format!(
                            "def {name:?} 의 qubit 인자는 단일 큐비트여야 합니다 \
                             (레지스터 전체 전달 불가, {} 큐비트)",
                            qs.len()
                        ),
                    });
                }
                env.insert_qubit(param.name.clone(), qs[0]);
            }
            (DefParamKind::QubitArray, DefArg::Qubit(qarg)) => {
                let qs = resolve_qarg(qarg, qregs).map_err(|e| with_loc(e, line, col))?;
                if let Some(decl_size) = param.size {
                    if qs.len() != decl_size {
                        return Err(QasmError::Lower {
                            message: format!(
                                "def {name:?} 의 qubit 배열 파라미터 {:?} 는 크기 \
                                 {decl_size} 인데 {} 큐비트가 전달되었습니다",
                                param.name,
                                qs.len()
                            ),
                        });
                    }
                }
                env.insert_qubit_array(param.name.clone(), qs);
            }
            (DefParamKind::Bit, DefArg::Cbit(carg)) => {
                let cs = resolve_carg(carg, cregs).map_err(|e| with_loc(e, line, col))?;
                if cs.len() != 1 {
                    return Err(QasmError::Lower {
                        message: format!(
                            "def {name:?} 의 bit 인자는 단일 bit 여야 합니다 ({} bit)",
                            cs.len()
                        ),
                    });
                }
                env.insert_cbit(param.name.clone(), cs[0]);
            }
            (DefParamKind::BitArray, DefArg::Cbit(carg)) => {
                let cs = resolve_carg(carg, cregs).map_err(|e| with_loc(e, line, col))?;
                if let Some(decl_size) = param.size {
                    if cs.len() != decl_size {
                        return Err(QasmError::Lower {
                            message: format!(
                                "def {name:?} 의 bit 배열 파라미터 {:?} 는 크기 \
                                 {decl_size} 인데 {} bit 가 전달되었습니다",
                                param.name,
                                cs.len()
                            ),
                        });
                    }
                }
                env.insert_cbit_array(param.name.clone(), cs);
            }
            (DefParamKind::Classical, DefArg::Qubit(_)) => {
                return Err(QasmError::Lower {
                    message: format!(
                        "def {name:?}: classical 파라미터 {:?} 에 qubit 인자 전달",
                        param.name
                    ),
                });
            }
            // 파라미터/인자 종류 불일치 (qubit↔classical/bit, bit↔classical/qubit 등).
            (DefParamKind::Qubit, _)
            | (DefParamKind::QubitArray, _)
            | (DefParamKind::Bit, _)
            | (DefParamKind::BitArray, _)
            | (DefParamKind::Classical, DefArg::Cbit(_)) => {
                return Err(QasmError::Lower {
                    message: format!(
                        "def {name:?}: 파라미터 {:?} 에 인자 종류 불일치",
                        param.name
                    ),
                });
            }
        }
    }
    for stmt in &decl.body {
        lower_stmt_into(circuit, stmt, qregs, cregs, gate_decls, &env)?;
    }
    Ok(())
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
    env: &Env,
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
    let then_insts =
        lower_block_to_instructions(then_body, n_qubits, qregs, cregs, gate_decls, env)?;
    let else_insts = match else_body {
        Some(stmts) => Some(lower_block_to_instructions(
            stmts, n_qubits, qregs, cregs, gate_decls, env,
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
    env: &Env,
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
    let body_insts = lower_block_to_instructions(body, n_qubits, qregs, cregs, gate_decls, env)?;
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
    env: &Env,
    line: usize,
    col: usize,
) -> QasmResult<()> {
    if high < low {
        // 빈 시퀀스 — for body 0 회 (no-op).
        return Ok(());
    }
    let iterations = (high - low + 1) as usize;
    let n_qubits = circuit.num_qubits();
    let body_insts = lower_block_to_instructions(body, n_qubits, qregs, cregs, gate_decls, env)
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
    env: &Env,
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
        let body_insts =
            lower_block_to_instructions(body, n_qubits, qregs, cregs, gate_decls, env)?;
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
    env: &Env,
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
    lower_gate_call(circuit, call, qregs, gate_decls, env, 0)?;
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
    /// def 의 qubit 배열 파라미터 (`qubit[N] q`) → 바인딩된 큐비트 인덱스들.
    /// body 에서 `q[i]` 인덱싱으로 해석된다 (v0.7.3).
    qubit_arrays: HashMap<String, Vec<usize>>,
    /// def 의 bit 파라미터 (`bit b`) → 바인딩된 호출자 cbit 인덱스 (v1.3.2).
    cbits: HashMap<String, usize>,
    /// def 의 bit 배열 파라미터 (`bit[N] b`) → 바인딩된 cbit 인덱스들 (v1.3.2).
    cbit_arrays: HashMap<String, Vec<usize>>,
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
    fn insert_qubit_array(&mut self, name: String, qubits: Vec<usize>) {
        self.qubit_arrays.insert(name, qubits);
    }
    fn insert_cbit(&mut self, name: String, idx: usize) {
        self.cbits.insert(name, idx);
    }
    fn insert_cbit_array(&mut self, name: String, cbits: Vec<usize>) {
        self.cbit_arrays.insert(name, cbits);
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
            // def 의 qubit 배열 파라미터 `q[i]` → 바인딩된 인덱스 (v0.7.3).
            if let Some(arr) = env.qubit_arrays.get(reg) {
                if *idx >= arr.len() {
                    return Err(QasmError::QubitOutOfRange {
                        qubit: *idx,
                        n_qubits: arr.len(),
                    });
                }
                return Ok(vec![arr[*idx]]);
            }
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
            // def 의 qubit 배열 파라미터 전체 (`q`) → 바인딩된 인덱스 전체.
            if let Some(arr) = env.qubit_arrays.get(reg) {
                return Ok(arr.clone());
            }
            let info = qregs.get(reg).ok_or_else(|| QasmError::Lower {
                message: format!("undefined qreg/qubit register {reg:?}"),
            })?;
            Ok((info.offset..info.offset + info.size).collect())
        }
    }
}

fn resolve_carg(c: &CArg, cregs: &HashMap<String, RegInfo>) -> QasmResult<Vec<usize>> {
    resolve_carg_in_env(c, cregs, &Env::empty())
}

/// def body 내 cbit 참조 해석 — def 의 bit 파라미터 이름이면 바인딩된 cbit
/// 인덱스 (v1.3.2), 아니면 creg lookup.  `resolve_qarg_in_env` 의 cbit 대응.
fn resolve_carg_in_env(
    c: &CArg,
    cregs: &HashMap<String, RegInfo>,
    env: &Env,
) -> QasmResult<Vec<usize>> {
    match c {
        CArg::Indexed { reg, idx } => {
            // bit[N] 파라미터 `b[i]` → 바인딩된 cbit.
            if let Some(arr) = env.cbit_arrays.get(reg) {
                if *idx >= arr.len() {
                    return Err(QasmError::CbitOutOfRange {
                        cbit: *idx,
                        n_cbits: arr.len(),
                    });
                }
                return Ok(vec![arr[*idx]]);
            }
            if env.cbits.contains_key(reg) {
                return Err(QasmError::Lower {
                    message: format!(
                        "indexed bit '{reg}[{idx}]' — 단일 bit 파라미터는 인덱싱 불가"
                    ),
                });
            }
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
            // 단일 bit 파라미터 (`b`).
            if let Some(ci) = env.cbits.get(reg) {
                return Ok(vec![*ci]);
            }
            // bit[N] 파라미터 전체 (`b`).
            if let Some(arr) = env.cbit_arrays.get(reg) {
                return Ok(arr.clone());
            }
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
    fn test_def_subroutine_inline() {
        // v0.6.9: def 가 호출 시 body 로 인라인.
        let c = lower(
            "OPENQASM 3.0; include \"stdgates.inc\"; qubit[2] q; \
             def bell(qubit a, qubit b) { h a; cx a, b; } bell(q[0], q[1]);",
        );
        assert_eq!(c.num_qubits(), 2);
        // h + cx = 2 instructions.
        assert_eq!(c.instructions().len(), 2);
    }

    #[test]
    fn test_def_classical_param() {
        // classical 파라미터가 angle 표현식에 바인딩.
        let c = lower(
            "OPENQASM 3.0; include \"stdgates.inc\"; qubit[1] q; \
             def myrot(angle t, qubit a) { rx(t/2) a; } myrot(pi, q[0]);",
        );
        assert_eq!(c.instructions().len(), 1);
    }

    #[test]
    fn test_def_mixed_classical_qubit_args() {
        // int + qubit 혼합 인자, 호출 순서 매칭.
        let c = lower(
            "OPENQASM 3.0; include \"stdgates.inc\"; qubit[2] q; \
             def f(qubit a, angle t, qubit b) { rz(t) a; cx a, b; } f(q[0], 0.5, q[1]);",
        );
        assert_eq!(c.instructions().len(), 2);
    }

    /// def body 의 Measure 명령이 기록하는 (qubit, cbit) 쌍을 수집.
    fn measures(c: &Circuit) -> Vec<(usize, usize)> {
        c.instructions()
            .iter()
            .filter_map(|i| match i {
                qsim_simulator::Instruction::Measure { qubit, cbit } => Some((*qubit, *cbit)),
                _ => None,
            })
            .collect()
    }

    #[test]
    fn test_def_bit_param_measure_writes_caller_cbit() {
        // v1.3.2: def 가 bit 파라미터로 받은 호출자 cbit 에 측정 결과를 기록.
        let c = lower(
            "OPENQASM 3.0; include \"stdgates.inc\"; qubit[1] q; bit[2] c; \
             def meas(qubit a, bit b) { h a; measure a -> b; } meas(q[0], c[1]);",
        );
        // measure 가 호출자 cbit c[1] (= index 1) 에 기록되어야.
        assert_eq!(measures(&c), vec![(0, 1)]);
    }

    #[test]
    fn test_def_bit_array_param_broadcast() {
        // bit[2] 배열 파라미터: `measure a -> b` 가 두 cbit 으로 broadcast.
        let c = lower(
            "OPENQASM 3.0; include \"stdgates.inc\"; qubit[2] q; bit[2] c; \
             def measall(qubit[2] a, bit[2] b) { h a[0]; cx a[0], a[1]; measure a -> b; } \
             measall(q, c);",
        );
        assert_eq!(measures(&c), vec![(0, 0), (1, 1)]);
    }

    #[test]
    fn test_def_bit_array_indexed() {
        // bit[2] b 의 b[0] 인덱싱 → 호출자 creg 의 해당 cbit.
        let c = lower(
            "OPENQASM 3.0; include \"stdgates.inc\"; qubit[1] q; bit[2] c; \
             def f(qubit a, bit[2] b) { measure a -> b[0]; } f(q[0], c);",
        );
        assert_eq!(measures(&c), vec![(0, 0)]);
    }

    #[test]
    fn test_def_bit_array_size_mismatch_errors() {
        // bit[2] 파라미터에 크기 3 creg 전달 → 거부.
        let src = "OPENQASM 3.0; include \"stdgates.inc\"; qubit[1] q; bit[3] c; \
             def f(qubit a, bit[2] b) { measure a -> b[0]; } f(q[0], c);";
        let toks = Lexer::new(src).tokenize().unwrap();
        let prog = Parser::new(toks).parse_program().unwrap();
        assert!(lower_program(prog).is_err());
    }

    #[test]
    fn test_def_bit_param_type_mismatch_errors() {
        // bit 파라미터에 qubit 인자 전달 → 거부 (call-site 가 carg 를 파싱하므로
        // 실제로는 파싱 단계에서 qubit ref 를 carg 로 읽어 lower 에서 미정의 creg).
        let src = "OPENQASM 3.0; include \"stdgates.inc\"; qubit[2] q; bit[1] c; \
             def f(qubit a, bit b) { measure a -> b; } f(q[0], q[1]);";
        let toks = Lexer::new(src).tokenize().unwrap();
        let prog = Parser::new(toks).parse_program().unwrap();
        assert!(lower_program(prog).is_err());
    }

    #[test]
    fn test_def_return_value_unsupported() {
        let src = "OPENQASM 3.0; include \"stdgates.inc\"; qubit[1] q; \
             def f(qubit a) -> bit { h a; } f(q[0]);";
        let toks = Lexer::new(src).tokenize().unwrap();
        let prog = Parser::new(toks).parse_program().unwrap();
        assert!(lower_program(prog).is_err());
    }

    #[test]
    fn test_def_arity_mismatch() {
        let src = "OPENQASM 3.0; include \"stdgates.inc\"; qubit[2] q; \
             def bell(qubit a, qubit b) { h a; cx a, b; } bell(q[0]);";
        let toks = Lexer::new(src).tokenize().unwrap();
        let prog = Parser::new(toks).parse_program().unwrap();
        assert!(lower_program(prog).is_err());
    }

    #[test]
    fn test_box_transparent_lowering() {
        // v0.6.8 — `box { ... }` 는 body 를 투명하게 lowering (게이트 개수 동일).
        let c = lower(
            "OPENQASM 3.0; include \"stdgates.inc\"; qubit[2] q; box { h q[0]; cx q[0], q[1]; }",
        );
        assert_eq!(c.num_qubits(), 2);
        assert_eq!(c.instructions().len(), 2);
    }

    #[test]
    fn test_box_with_designator_ignored() {
        // duration designator 는 무시되고 body 만 lowering.
        let c = lower(
            "OPENQASM 3.0; include \"stdgates.inc\"; qubit[1] q; box[100ns] { h q[0]; x q[0]; }",
        );
        assert_eq!(c.instructions().len(), 2);
    }

    #[test]
    fn test_box_nested_in_for() {
        // box 가 다른 블록 안에 중첩돼도 동작.
        let c = lower(
            "OPENQASM 3.0; include \"stdgates.inc\"; qubit[1] q; for int i in [0:2] { box { x q[0]; } }",
        );
        assert_eq!(c.num_qubits(), 1);
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
