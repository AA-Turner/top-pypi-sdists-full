//! Gate fusion (statevector 가속).
//!
//! statevector 의 게이트 적용은 매번 전체(2ⁿ) sweep 이라 게이트 수가 곧 비용이다.
//! 인접 게이트를 하나의 행렬로 융합해 sweep 횟수를 줄인다 (QMin/Qandle 2024-25,
//! Qiskit Aer 가 dense 에서 빠른 핵심 이유):
//!
//! 1. **1q run 융합** — 연속 같은-큐비트 1q 게이트 → 하나의 2×2 (예: `rz·rx·rz`→1).
//! 2. **1q→2q 흡수** — 2q 게이트 직전의 (해당 두 큐비트의) 1q 융합행렬을 그 2q
//!    게이트에 흡수 → 하나의 4×4 (예: `(1q on a)(1q on b)(cz) → 4×4`).
//!
//! **정확성**: 순수 명령열 변환이라 결과 statevector 불변 (서로 다른 큐비트의 1q
//! 는 교환).  융합 결과는 1q/2q `ApplyUnitary` 라 CPU statevector 경로
//! (`apply_unitary_typed` fast-path)에서만 쓴다.  지원 안 되는 2q 게이트(controlled
//! 류) 는 융합 없이 그대로 둔다 (정확성 우선).

use num_complex::Complex;
use qsim_core::Gate;

use crate::instruction::Instruction;

type C = Complex<f64>;
type M2 = [C; 4]; // row-major 2×2
type M4 = [C; 16]; // row-major 4×4

#[inline]
fn matmul2(a: &M2, b: &M2) -> M2 {
    [
        a[0] * b[0] + a[1] * b[2],
        a[0] * b[1] + a[1] * b[3],
        a[2] * b[0] + a[3] * b[2],
        a[2] * b[1] + a[3] * b[3],
    ]
}

#[inline]
fn gate_m2(gate: &Gate) -> M2 {
    let m = gate.matrix_2x2::<f64>();
    [m[0][0], m[0][1], m[1][0], m[1][1]]
}

/// 4×4 행렬곱 a·b (row-major).
fn matmul4(a: &M4, b: &M4) -> M4 {
    let mut out = [C::new(0.0, 0.0); 16];
    for i in 0..4 {
        for j in 0..4 {
            let mut s = C::new(0.0, 0.0);
            for k in 0..4 {
                s += a[i * 4 + k] * b[k * 4 + j];
            }
            out[i * 4 + j] = s;
        }
    }
    out
}

/// kron(hi, lo) — index = 2·bit(hi-qubit) + bit(lo-qubit) (hi=MSB, lo=LSB).
fn kron2(hi: &M2, lo: &M2) -> M4 {
    let mut out = [C::new(0.0, 0.0); 16];
    for i in 0..2 {
        for k in 0..2 {
            for j in 0..2 {
                for l in 0..2 {
                    out[(2 * i + j) * 4 + (2 * k + l)] = hi[i * 2 + k] * lo[j * 2 + l];
                }
            }
        }
    }
    out
}

/// flat Matrix4x4 (row-major) — `apply_two_qubit_gate(.., targets[0], targets[1])`
/// 규약 (index = 2·bit(targets[1]) + bit(targets[0]), 즉 targets[0]=LSB).
fn flat4(m: qsim_core::gates::Matrix4x4<f64>) -> M4 {
    let mut out = [C::new(0.0, 0.0); 16];
    for i in 0..4 {
        for j in 0..4 {
            out[i * 4 + j] = m[i][j];
        }
    }
    out
}

/// 지원하는 2q 게이트의 4×4 (없으면 None — 융합 생략).
fn gate_m4(gate: &Gate) -> Option<M4> {
    Some(match gate {
        // NOTE: CNOT 은 엔진이 apply_controlled_gate (control=MSB 규약) 로 적용해
        // cnot_matrix 가 apply_two_qubit_gate (targets[0]=LSB) 규약과 다르다 →
        // 융합 제외 (flush+emit native).  아래 게이트들은 엔진이
        // apply_two_qubit_gate(.., targets[0], targets[1]) 로 적용해 규약 일치.
        Gate::CZ => flat4(Gate::cz_matrix::<f64>()),
        Gate::SWAP => flat4(Gate::swap_matrix::<f64>()),
        Gate::ISwap => flat4(Gate::iswap_matrix::<f64>()),
        Gate::Rxx(t) => flat4(Gate::rxx_matrix::<f64>(*t)),
        Gate::Ryy(t) => flat4(Gate::ryy_matrix::<f64>(*t)),
        Gate::Rzz(t) => flat4(Gate::rzz_matrix::<f64>(*t)),
        Gate::Dcx => flat4(Gate::dcx_matrix::<f64>()),
        Gate::Ecr => flat4(Gate::ecr_matrix::<f64>()),
        Gate::Rzx(t) => flat4(Gate::rzx_matrix::<f64>(*t)),
        Gate::XxPlusYy(t) => flat4(Gate::xx_plus_yy_matrix::<f64>(*t)),
        Gate::XxMinusYy(t) => flat4(Gate::xx_minus_yy_matrix::<f64>(*t)),
        _ => return None,
    })
}

#[inline]
fn ident2() -> M2 {
    [
        C::new(1.0, 0.0),
        C::new(0.0, 0.0),
        C::new(0.0, 0.0),
        C::new(1.0, 0.0),
    ]
}

/// 명령이 닿는 큐비트들.  `None` = 특정 불가(전체 flush 필요: MeasureAll /
/// reset / noise / control-flow).
fn touched_qubits(inst: &Instruction) -> Option<Vec<usize>> {
    match inst {
        Instruction::ApplyGate { targets, .. } => Some(targets.clone()),
        Instruction::ApplyUnitary { targets, .. } => Some(targets.clone()),
        Instruction::Measure { qubit, .. } => Some(vec![*qubit]),
        Instruction::ApplyNoise { target, .. } => Some(vec![*target]),
        Instruction::ApplyNoise2 { q0, q1, .. } => Some(vec![*q0, *q1]),
        Instruction::Reset { qubit } => Some(vec![*qubit]),
        // MeasureAll / 동적 control-flow 는 닿는 큐비트가 광범위/불확실 → 전체 flush.
        _ => None,
    }
}

/// 인접 게이트를 1q/2q 행렬로 융합한 명령열 (`n` = 큐비트 수).
pub fn fuse_gates(insts: &[Instruction], n: usize) -> Vec<Instruction> {
    let mut pending: Vec<Option<M2>> = vec![None; n];
    let mut out: Vec<Instruction> = Vec::with_capacity(insts.len());

    fn flush(q: usize, pending: &mut [Option<M2>], out: &mut Vec<Instruction>) {
        if let Some(m) = pending[q].take() {
            out.push(Instruction::ApplyUnitary {
                matrix: m.to_vec(),
                targets: vec![q],
            });
        }
    }

    for inst in insts {
        match inst {
            // 1q ApplyGate → pending 누적.
            Instruction::ApplyGate { gate, targets } if targets.len() == 1 => {
                let q = targets[0];
                let g = gate_m2(gate);
                pending[q] = Some(match &pending[q] {
                    Some(p) => matmul2(&g, p),
                    None => g,
                });
            }
            // 1q ApplyUnitary → pending 누적.
            Instruction::ApplyUnitary { matrix, targets } if targets.len() == 1 => {
                let q = targets[0];
                let g: M2 = [matrix[0], matrix[1], matrix[2], matrix[3]];
                pending[q] = Some(match &pending[q] {
                    Some(p) => matmul2(&g, p),
                    None => g,
                });
            }
            // 2q ApplyGate (지원 게이트) → 직전 1q 흡수해 4×4 로 융합.
            Instruction::ApplyGate { gate, targets } if targets.len() == 2 => {
                let (a, b) = (targets[0], targets[1]);
                match gate_m4(gate) {
                    Some(g4) => {
                        let ma = pending[a].take().unwrap_or_else(ident2);
                        let mb = pending[b].take().unwrap_or_else(ident2);
                        // index = 2·bit(b)+bit(a): b=MSB(hi), a=LSB(lo).
                        let pre = kron2(&mb, &ma);
                        let fused = matmul4(&g4, &pre);
                        out.push(Instruction::ApplyUnitary {
                            matrix: fused.to_vec(),
                            targets: vec![a, b],
                        });
                    }
                    None => {
                        // 미지원 2q (controlled 류) — 두 큐비트 flush 후 그대로 emit.
                        flush(a, &mut pending, &mut out);
                        flush(b, &mut pending, &mut out);
                        out.push(inst.clone());
                    }
                }
            }
            // 그 외 (미지원 2q controlled / 3q+ / measure / 2q ApplyUnitary 등):
            // **닿는 큐비트만** flush (나머지 큐비트의 pending 1q 는 disjoint 라
            // 교환 → 융합 유지).  큐비트를 특정할 수 없으면 (MeasureAll / reset /
            // noise / control-flow) 보수적으로 전체 flush.
            other => {
                match touched_qubits(other) {
                    Some(qs) => {
                        for q in qs {
                            if q < n {
                                flush(q, &mut pending, &mut out);
                            }
                        }
                    }
                    None => {
                        for q in 0..n {
                            flush(q, &mut pending, &mut out);
                        }
                    }
                }
                out.push(other.clone());
            }
        }
    }
    for q in 0..n {
        flush(q, &mut pending, &mut out);
    }
    out
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn fuses_1q_run() {
        let insts = vec![
            Instruction::ApplyGate {
                gate: Gate::Rz(0.3),
                targets: vec![0],
            },
            Instruction::ApplyGate {
                gate: Gate::Rx(0.5),
                targets: vec![0],
            },
            Instruction::ApplyGate {
                gate: Gate::H,
                targets: vec![1],
            },
        ];
        let fused = fuse_gates(&insts, 2);
        assert_eq!(fused.len(), 2); // [U(0), U(1)]
        assert!(fused
            .iter()
            .all(|i| matches!(i, Instruction::ApplyUnitary { .. })));
    }

    #[test]
    fn absorbs_1q_into_2q() {
        // (H on 0)(S on 1)(CZ 0,1) → 하나의 4×4 ApplyUnitary.
        let insts = vec![
            Instruction::ApplyGate {
                gate: Gate::H,
                targets: vec![0],
            },
            Instruction::ApplyGate {
                gate: Gate::S,
                targets: vec![1],
            },
            Instruction::ApplyGate {
                gate: Gate::CZ,
                targets: vec![0, 1],
            },
        ];
        let fused = fuse_gates(&insts, 2);
        assert_eq!(fused.len(), 1);
        assert!(
            matches!(&fused[0], Instruction::ApplyUnitary { matrix, targets } if matrix.len() == 16 && targets == &[0, 1])
        );
    }

    #[test]
    fn selective_flush_preserves_other_qubits() {
        // H(0); CRx(1,2) [q0 미접촉]; H(0) → CRx 가 q0 의 pending 을 flush 하지
        // 않아 두 H(0) 가 CRx 를 가로질러 융합된다.  출력=[CRx, U(0)].
        let insts = vec![
            Instruction::ApplyGate {
                gate: Gate::H,
                targets: vec![0],
            },
            Instruction::ApplyGate {
                gate: Gate::CRx(0.5),
                targets: vec![1, 2],
            },
            Instruction::ApplyGate {
                gate: Gate::H,
                targets: vec![0],
            },
        ];
        let fused = fuse_gates(&insts, 3);
        assert_eq!(fused.len(), 2, "{fused:?}");
        assert!(
            matches!(fused[0], Instruction::ApplyGate { ref gate, .. } if matches!(gate, Gate::CRx(_)))
        );
        assert!(matches!(&fused[1], Instruction::ApplyUnitary { targets, .. } if targets == &[0]));
    }

    #[test]
    fn unsupported_2q_flushes() {
        // controlled-RX (미지원 4×4) — 융합 안 하고 1q flush 후 emit.
        let insts = vec![
            Instruction::ApplyGate {
                gate: Gate::H,
                targets: vec![0],
            },
            Instruction::ApplyGate {
                gate: Gate::CRx(0.5),
                targets: vec![0, 1],
            },
        ];
        let fused = fuse_gates(&insts, 2);
        // [U(0), CRx]
        assert_eq!(fused.len(), 2);
        assert!(matches!(fused[0], Instruction::ApplyUnitary { .. }));
        assert!(
            matches!(fused[1], Instruction::ApplyGate { ref gate, .. } if matches!(gate, Gate::CRx(_)))
        );
    }
}
