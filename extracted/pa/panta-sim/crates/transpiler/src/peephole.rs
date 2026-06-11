//! Peephole 최적화 패스.
//!
//! 회로 정확성 (statevector ≡ before/after, 1e-12) 을 보존하면서 게이트 수를
//! 줄이는 가벼운 변환들을 fixed-point iteration 으로 적용한다.
//!
//! 활성화된 패스:
//! 1. **회전 합성**: 같은 큐비트 위 인접 `Rx(a)·Rx(b)` → `Rx(a+b)` (Ry, Rz 동등).
//! 2. **2-게이트 항등식**:
//!    - `X·X` / `Y·Y` / `Z·Z` / `H·H` → drop (Pauli involution)
//!    - `S·S` → `Z`,  `Sdg·Sdg` → `Z`,  `T·T` → `S`,  `Tdg·Tdg` → `Sdg`
//!    - `S·Sdg` / `Sdg·S` / `T·Tdg` / `Tdg·T` → drop
//! 3. **3-게이트 항등식**:
//!    - `H·X·H` → `Z`,  `H·Z·H` → `X`
//! 4. **trivial drop**: `Id`, `Rx(0)`/`Ry(0)`/`Rz(0)` 제거.
//!
//! 변환은 instruction 의 같은 큐비트 인접 (intervening op 없음) 일 때만 적용.

use qsim_core::Gate;
use qsim_simulator::{Circuit, Instruction};

const ANGLE_EPS: f64 = 1e-12;

/// peephole 최적화 통계.
#[derive(Debug, Default, Clone, Copy)]
pub struct PeepholeStats {
    /// 수렴까지 사용된 패스 횟수.
    pub passes: usize,
    /// 제거된 게이트 수.
    pub gates_removed: usize,
    /// 합성된 게이트 쌍 수 (예: Rz·Rz → Rz 는 1회).
    pub gates_merged: usize,
}

/// 회로에 peephole 패스를 fixed-point 까지 반복 적용한다 (in-place).
///
/// `max_iters` 회 안에 수렴하지 않으면 중단하고 stats 반환.
pub fn peephole_optimize(circuit: &mut Circuit, max_iters: usize) -> PeepholeStats {
    let mut stats = PeepholeStats::default();
    for iter in 0..max_iters {
        let before_len = circuit.instructions().len();
        let pass_stats = run_single_pass(circuit);
        stats.gates_removed += pass_stats.gates_removed;
        stats.gates_merged += pass_stats.gates_merged;
        let after_len = circuit.instructions().len();
        if after_len == before_len && pass_stats.gates_merged == 0 {
            stats.passes = iter + 1;
            return stats;
        }
    }
    stats.passes = max_iters;
    stats
}

#[derive(Default)]
struct PassStats {
    gates_removed: usize,
    gates_merged: usize,
}

fn run_single_pass(circuit: &mut Circuit) -> PassStats {
    let original = std::mem::take(circuit.instructions_mut());
    let mut out: Vec<Instruction> = Vec::with_capacity(original.len());
    let mut stats = PassStats::default();
    // 제거된 ±I 게이트가 남긴 전역 위상 누적 (마지막에 회로에 보상).
    let mut phase_acc = 0.0_f64;

    for inst in original {
        // 1) trivial drop (Id, 0-각도 회전, −I 회전은 위상 보상).
        if let Instruction::ApplyGate { gate, targets: _ } = &inst {
            if let Some(lambda) = scalar_phase(gate) {
                phase_acc += lambda;
                stats.gates_removed += 1;
                continue;
            }
        }

        // 2) 직전 게이트와의 2-게이트 패턴 매칭.
        if let Some(merged) = try_merge_with_last(&mut out, &inst) {
            match merged {
                MergeOutcome::Replaced => stats.gates_merged += 1,
                MergeOutcome::Cancelled { phase } => {
                    phase_acc += phase;
                    stats.gates_removed += 2;
                }
            }
            continue;
        }

        // 3) 직전 두 게이트와의 3-게이트 패턴 (H·X·H, H·Z·H).
        if try_collapse_hxh(&mut out, &inst) {
            stats.gates_merged += 1;
            continue;
        }

        out.push(inst);
    }

    *circuit.instructions_mut() = out;
    if phase_acc != 0.0 {
        circuit.add_global_phase(phase_acc);
    }
    stats
}

#[derive(Debug)]
enum MergeOutcome {
    /// 두 게이트를 하나로 합성 (예: Rz·Rz → Rz, S·S → Z).
    Replaced,
    /// 두 게이트가 상쇄되어 둘 다 제거됨 (예: X·X → ∅).  `phase` 는 제거가
    /// 남기는 전역 위상 (예: `Rx(a)·Rx(b)`, a+b ≡ 2π (mod 4π) 이면 곱이
    /// −I 라 π).  호출자가 `Circuit::add_global_phase` 로 보상해야 한다.
    Cancelled { phase: f64 },
}

/// 게이트가 스칼라 `e^{iλ}·I` 면 `Some(λ)` — 제거 가능하되 λ 를 회로
/// global phase 에 보상해야 한다.
///
/// 반각 컨벤션에서 `R(2π) = −I` 이므로 회전각은 **mod 4π** 로 봐야 한다 —
/// 이전 구현은 mod 2π 로 `R(2π)` 를 그냥 버려서 statevector 부호가 뒤집혔다.
fn scalar_phase(gate: &Gate) -> Option<f64> {
    match gate {
        Gate::Id => Some(0.0),
        Gate::Rx(t) | Gate::Ry(t) | Gate::Rz(t) => rotation_scalar_phase(*t),
        _ => None,
    }
}

/// `R(θ)` 가 ±I 인지: θ ≡ 0 (mod 4π) → `Some(0)`, θ ≡ 2π (mod 4π) →
/// `Some(π)` (= −I), 그 외 `None`.
fn rotation_scalar_phase(theta: f64) -> Option<f64> {
    use std::f64::consts::PI;
    let r = theta.rem_euclid(4.0 * PI);
    if r < ANGLE_EPS || (4.0 * PI - r) < ANGLE_EPS {
        Some(0.0)
    } else if (r - 2.0 * PI).abs() < ANGLE_EPS {
        Some(PI)
    } else {
        None
    }
}

/// 1큐비트 게이트 + 그 1개 큐비트 인덱스를 추출. 다른 케이스는 None.
fn as_single_qubit(inst: &Instruction) -> Option<(&Gate, usize)> {
    match inst {
        Instruction::ApplyGate { gate, targets } if targets.len() == 1 => Some((gate, targets[0])),
        _ => None,
    }
}

fn try_merge_with_last(out: &mut Vec<Instruction>, current: &Instruction) -> Option<MergeOutcome> {
    let (cur_gate, cur_q) = as_single_qubit(current)?;
    let last = out.last()?;
    let (last_gate, last_q) = as_single_qubit(last)?;
    if cur_q != last_q {
        return None;
    }

    // 회전 합성 (Rx, Ry, Rz). 합 각도가 0 (mod 2π) 이면 cancel.
    if let Some((axis, a, b)) = match_rotation_pair(last_gate, cur_gate) {
        out.pop();
        let summed = a + b;
        if let Some(phase) = rotation_scalar_phase(summed) {
            return Some(MergeOutcome::Cancelled { phase });
        }
        let merged_gate = match axis {
            RotAxis::X => Gate::Rx(summed),
            RotAxis::Y => Gate::Ry(summed),
            RotAxis::Z => Gate::Rz(summed),
        };
        out.push(Instruction::ApplyGate {
            gate: merged_gate,
            targets: vec![cur_q],
        });
        return Some(MergeOutcome::Replaced);
    }

    // 2-게이트 항등식.
    if let Some(replacement) = match_two_gate_identity(last_gate, cur_gate) {
        out.pop();
        match replacement {
            Some(g) => {
                out.push(Instruction::ApplyGate {
                    gate: g,
                    targets: vec![cur_q],
                });
                return Some(MergeOutcome::Replaced);
            }
            None => return Some(MergeOutcome::Cancelled { phase: 0.0 }),
        }
    }

    None
}

#[derive(Clone, Copy)]
enum RotAxis {
    X,
    Y,
    Z,
}

fn match_rotation_pair(a: &Gate, b: &Gate) -> Option<(RotAxis, f64, f64)> {
    match (a, b) {
        (Gate::Rx(x), Gate::Rx(y)) => Some((RotAxis::X, *x, *y)),
        (Gate::Ry(x), Gate::Ry(y)) => Some((RotAxis::Y, *x, *y)),
        (Gate::Rz(x), Gate::Rz(y)) => Some((RotAxis::Z, *x, *y)),
        _ => None,
    }
}

/// 두 게이트의 항등식 매칭. `Some(None)` = 둘 다 제거, `Some(Some(g))` = `g` 로 교체,
/// `None` = 매칭 안 됨.
#[allow(clippy::option_option)]
fn match_two_gate_identity(a: &Gate, b: &Gate) -> Option<Option<Gate>> {
    use Gate::*;
    match (a, b) {
        // Pauli involution
        (X, X) | (Y, Y) | (Z, Z) | (H, H) => Some(None),
        // S 계열
        (S, S) => Some(Some(Z)),
        (Sdg, Sdg) => Some(Some(Z)),
        (S, Sdg) | (Sdg, S) => Some(None),
        // T 계열
        (T, T) => Some(Some(S)),
        (Tdg, Tdg) => Some(Some(Sdg)),
        (T, Tdg) | (Tdg, T) => Some(None),
        _ => None,
    }
}

/// 직전 두 게이트와 현재 게이트가 H·X·H 또는 H·Z·H 패턴이면 단일 게이트로 collapse.
fn try_collapse_hxh(out: &mut Vec<Instruction>, current: &Instruction) -> bool {
    let (cur_gate, cur_q) = match as_single_qubit(current) {
        Some(p) => p,
        None => return false,
    };
    if !matches!(cur_gate, Gate::H) {
        return false;
    }
    if out.len() < 2 {
        return false;
    }
    let n = out.len();
    let (mid_gate, mid_q) = match as_single_qubit(&out[n - 1]) {
        Some(p) => p,
        None => return false,
    };
    let (first_gate, first_q) = match as_single_qubit(&out[n - 2]) {
        Some(p) => p,
        None => return false,
    };
    if first_q != cur_q || mid_q != cur_q || !matches!(first_gate, Gate::H) {
        return false;
    }
    let replacement = match mid_gate {
        Gate::X => Gate::Z,
        Gate::Z => Gate::X,
        _ => return false,
    };
    out.pop();
    out.pop();
    out.push(Instruction::ApplyGate {
        gate: replacement,
        targets: vec![cur_q],
    });
    true
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::f64::consts::PI;

    fn count_gates(c: &Circuit) -> usize {
        c.instructions().len()
    }

    #[test]
    fn test_rz_rz_merge() {
        let mut qc = Circuit::new(1);
        qc.rz(0.3, 0);
        qc.rz(0.4, 0);
        let stats = peephole_optimize(&mut qc, 16);
        assert_eq!(count_gates(&qc), 1);
        if let Instruction::ApplyGate {
            gate: Gate::Rz(theta),
            ..
        } = &qc.instructions()[0]
        {
            assert!((theta - 0.7).abs() < 1e-12);
        } else {
            panic!("expected Rz");
        }
        assert_eq!(stats.gates_merged, 1);
    }

    #[test]
    fn test_rx_rx_merge_cancels_when_zero_sum() {
        let mut qc = Circuit::new(1);
        qc.rx(0.5, 0);
        qc.rx(-0.5, 0);
        peephole_optimize(&mut qc, 16);
        assert_eq!(count_gates(&qc), 0);
    }

    #[test]
    fn test_x_x_cancel() {
        let mut qc = Circuit::new(1);
        qc.x(0);
        qc.x(0);
        peephole_optimize(&mut qc, 16);
        assert_eq!(count_gates(&qc), 0);
    }

    #[test]
    fn test_h_h_cancel() {
        let mut qc = Circuit::new(1);
        qc.h(0);
        qc.h(0);
        peephole_optimize(&mut qc, 16);
        assert_eq!(count_gates(&qc), 0);
    }

    #[test]
    fn test_s_s_to_z() {
        let mut qc = Circuit::new(1);
        qc.s(0);
        qc.s(0);
        peephole_optimize(&mut qc, 16);
        assert_eq!(count_gates(&qc), 1);
        assert!(matches!(
            &qc.instructions()[0],
            Instruction::ApplyGate { gate: Gate::Z, .. }
        ));
    }

    #[test]
    fn test_t_tdg_cancel() {
        let mut qc = Circuit::new(1);
        qc.t(0);
        qc.tdg(0);
        peephole_optimize(&mut qc, 16);
        assert_eq!(count_gates(&qc), 0);
    }

    #[test]
    fn test_hxh_to_z() {
        let mut qc = Circuit::new(1);
        qc.h(0);
        qc.x(0);
        qc.h(0);
        peephole_optimize(&mut qc, 16);
        assert_eq!(count_gates(&qc), 1);
        assert!(matches!(
            &qc.instructions()[0],
            Instruction::ApplyGate { gate: Gate::Z, .. }
        ));
    }

    #[test]
    fn test_hzh_to_x() {
        let mut qc = Circuit::new(1);
        qc.h(0);
        qc.z(0);
        qc.h(0);
        peephole_optimize(&mut qc, 16);
        assert_eq!(count_gates(&qc), 1);
        assert!(matches!(
            &qc.instructions()[0],
            Instruction::ApplyGate { gate: Gate::X, .. }
        ));
    }

    #[test]
    fn test_intervening_op_blocks_merge() {
        // Rz q0; H q0; Rz q0  → 합성 안 됨 (중간에 H)
        let mut qc = Circuit::new(1);
        qc.rz(0.3, 0);
        qc.h(0);
        qc.rz(0.4, 0);
        peephole_optimize(&mut qc, 16);
        assert_eq!(count_gates(&qc), 3);
    }

    #[test]
    fn test_different_qubit_does_not_merge() {
        // 큐비트 다르면 인접 패턴 매칭 안 됨.
        let mut qc = Circuit::new(2);
        qc.rz(0.3, 0);
        qc.rz(0.4, 1);
        peephole_optimize(&mut qc, 16);
        assert_eq!(count_gates(&qc), 2);
    }

    #[test]
    fn test_trivial_id_dropped() {
        let mut qc = Circuit::new(1);
        qc.id(0);
        qc.h(0);
        qc.id(0);
        peephole_optimize(&mut qc, 16);
        assert_eq!(count_gates(&qc), 1);
    }

    #[test]
    fn test_rz_zero_dropped() {
        let mut qc = Circuit::new(1);
        qc.h(0);
        qc.rz(0.0, 0);
        qc.h(0);
        // rz(0) 삭제 후 H·H → cancel.
        peephole_optimize(&mut qc, 16);
        assert_eq!(count_gates(&qc), 0);
    }

    #[test]
    fn test_iterated_passes_converge() {
        // Rx(a)·Rx(-a) 후 H·H → 두 패스 필요할 수 있음.
        let mut qc = Circuit::new(1);
        qc.h(0);
        qc.rx(0.5, 0);
        qc.rx(-0.5, 0);
        qc.h(0);
        peephole_optimize(&mut qc, 16);
        assert_eq!(count_gates(&qc), 0);
    }

    #[test]
    fn test_max_iters_stops() {
        // 절대 수렴하지 않는 케이스는 인위적으로 만들기 어렵다 — 그냥 정상 회로로
        // max_iters 가 작아도 안전한지 확인.
        let mut qc = Circuit::new(1);
        for _ in 0..50 {
            qc.x(0);
        }
        let stats = peephole_optimize(&mut qc, 4);
        // X 짝수 개 → 0 (충분한 패스가 있으면), 아니면 일부 잔존.
        assert!(stats.passes <= 4);
    }

    #[test]
    fn test_2pi_rotation_dropped() {
        // R(2π) = −I — 게이트는 제거하되 전역 위상 π 를 보상해야 statevector
        // 부호가 보존된다 (이전 구현은 위상 없이 버려 −1 이 사라졌음).
        let mut qc = Circuit::new(1);
        qc.rz(2.0 * PI, 0);
        peephole_optimize(&mut qc, 16);
        assert_eq!(count_gates(&qc), 0);
        assert!((qc.global_phase() - PI).abs() < 1e-12);
    }

    #[test]
    fn test_4pi_rotation_dropped_no_phase() {
        // R(4π) = +I — 위상 보상 없이 제거.
        let mut qc = Circuit::new(1);
        qc.rx(4.0 * PI, 0);
        peephole_optimize(&mut qc, 16);
        assert_eq!(count_gates(&qc), 0);
        assert!(qc.global_phase().abs() < 1e-12);
    }

    #[test]
    fn test_rotation_pair_summing_to_2pi_keeps_phase() {
        // Rx(π)·Rx(π) = Rx(2π) = −I — cancel + 전역 위상 π.
        let mut qc = Circuit::new(1);
        qc.rx(PI, 0);
        qc.rx(PI, 0);
        peephole_optimize(&mut qc, 16);
        assert_eq!(count_gates(&qc), 0);
        assert!((qc.global_phase() - PI).abs() < 1e-12);
    }

    #[test]
    fn test_two_qubit_gate_is_barrier() {
        // CNOT 는 1큐비트 게이트가 아니므로 양옆의 1큐비트 게이트를 합치지 않음.
        let mut qc = Circuit::new(2);
        qc.rz(0.3, 0);
        qc.cx(0, 1);
        qc.rz(0.4, 0);
        peephole_optimize(&mut qc, 16);
        assert_eq!(count_gates(&qc), 3);
    }

    #[test]
    fn test_measurement_is_barrier() {
        let mut qc = Circuit::new(1);
        qc.rz(0.3, 0);
        qc.measure(0, 0);
        qc.rz(0.4, 0);
        peephole_optimize(&mut qc, 16);
        assert_eq!(count_gates(&qc), 3);
    }
}
