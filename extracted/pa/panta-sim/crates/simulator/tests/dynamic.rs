//! v0.4.5 dynamic circuit (mid-circuit measurement / reset / classical control)
//! integration tests at the simulator-level (Rust API only).

use qsim_core::complex::approx_eq;
use qsim_core::{NoiseChannel, C64};
use qsim_simulator::{Circuit, ExecutionEngine};

/// H → measure → outcome 따라 결정론적 후속.
/// outcome=0 일 때 |0⟩ 위에 H 한 번 더 → |+⟩, outcome=1 일 때 |1⟩ 위에 H → |−⟩.
/// 본 테스트는 fixed seed 로 outcome 분포가 ~50% 인지 + cbit 이 회로 끝 outcome
/// 으로 packing 되는지 검증.
#[test]
fn test_mid_circuit_measure_collapse_then_h_deterministic() {
    let mut c = Circuit::new(1);
    c.h(0);
    c.measure(0, 0);
    c.h(0); // collapse 후 |0⟩→|+⟩ 또는 |1⟩→|−⟩ — 어느 쪽이든 |+⟩/|−⟩ 동일 |amp|².
    c.measure(0, 0); // 끝 측정 (cbit 0 덮어쓰기) — H 적용 후 50:50.

    // dynamic 회로이므로 trajectory 모드. shots=2000 분포 검증.
    let engine = ExecutionEngine::with_seed(42);
    let result = engine.run(&c, 2000);
    let counts = result.counts();
    let c0 = *counts.get("0").unwrap_or(&0) as f64;
    let c1 = *counts.get("1").unwrap_or(&0) as f64;
    let total = c0 + c1;
    assert_eq!(total as usize, 2000);
    let ratio = c0 / total;
    assert!(
        (ratio - 0.5).abs() < 0.05,
        "mid-circuit + H 후 ratio {ratio} 가 0.5 와 너무 다름"
    );
}

/// Reset 결정론: |1⟩ 후 reset → 항상 |0⟩.
#[test]
fn test_reset_after_x_gives_zero() {
    let mut c = Circuit::new(1);
    c.x(0);
    c.reset(0);
    c.measure(0, 0);

    let engine = ExecutionEngine::with_seed(123);
    let result = engine.run(&c, 100);
    assert_eq!(result.counts().get("0"), Some(&100));
    assert_eq!(result.counts().get("1"), None);
}

/// Reset 후 H → |+⟩ → 50:50.
#[test]
fn test_reset_then_h_gives_uniform() {
    let mut c = Circuit::new(1);
    c.x(0);
    c.reset(0);
    c.h(0);
    c.measure(0, 0);

    let engine = ExecutionEngine::with_seed(7);
    let result = engine.run(&c, 2000);
    let c0 = *result.counts().get("0").unwrap_or(&0) as f64;
    let c1 = *result.counts().get("1").unwrap_or(&0) as f64;
    let ratio = c0 / (c0 + c1);
    assert!(
        (ratio - 0.5).abs() < 0.05,
        "reset+H ratio {ratio} 가 0.5 와 너무 다름"
    );
}

/// Reset 멱등성: reset 두 번 == 한 번.
#[test]
fn test_reset_idempotent() {
    let mut c = Circuit::new(1);
    c.h(0);
    c.reset(0);
    c.reset(0);
    c.measure(0, 0);

    let engine = ExecutionEngine::with_seed(42);
    let result = engine.run(&c, 100);
    assert_eq!(result.counts().get("0"), Some(&100));
}

/// Reset 후에도 다른 큐비트 entangle 보존.
#[test]
fn test_reset_preserves_other_qubit_state() {
    let mut c = Circuit::new(2);
    c.x(1); // q1 = |1⟩
    c.x(0); // q0 = |1⟩
    c.reset(0); // q0 → |0⟩
    c.measure(0, 0);
    c.measure(1, 1);

    let engine = ExecutionEngine::with_seed(42);
    let result = engine.run(&c, 100);
    // cbit string: c1 c0 = "10" (c1=1, c0=0). LSB-first packing → MSB=c[1]=1, LSB=c[0]=0.
    assert_eq!(result.counts().get("10"), Some(&100));
}

/// IfEq 단일 cbit, 조건 true 일 때 X 적용.
#[test]
fn test_if_eq_single_cbit_true_applies_x() {
    let mut c = Circuit::new(2);
    c.x(0); // q0 = |1⟩
    c.measure(0, 0); // c[0] = 1
    c.x(1);
    c.c_if_last(vec![0], 1); // c[0] == 1 → X(1) 적용 → q1 = |1⟩
    c.measure(1, 1);

    let engine = ExecutionEngine::with_seed(42);
    let result = engine.run(&c, 100);
    // c[1]=1 (X applied), c[0]=1 (initial X) → "11"
    assert_eq!(result.counts().get("11"), Some(&100));
}

/// IfEq 단일 cbit, 조건 false 일 때 게이트 스킵.
#[test]
fn test_if_eq_single_cbit_false_skips() {
    let mut c = Circuit::new(2);
    // q0 는 |0⟩ 그대로 → measure → c[0] = 0
    c.measure(0, 0);
    c.x(1);
    c.c_if_last(vec![0], 1); // c[0] == 0 ≠ 1 → X(1) 스킵 → q1 = |0⟩

    // 아 — 위 코드에 문제: x(1) 이 c_if_last 로 wrap 됐지만 c[0]=0 이라 skip.
    // 따라서 q1 은 |0⟩ 유지.
    c.measure(1, 1);

    let engine = ExecutionEngine::with_seed(42);
    let result = engine.run(&c, 100);
    // c[1]=0, c[0]=0 → "00"
    assert_eq!(result.counts().get("00"), Some(&100));
}

/// IfEq multi-cbit: cbits=[0,1], value=3 (0b11) → 둘 다 1 일 때만 fire.
#[test]
fn test_if_eq_multi_cbit_packed_value() {
    let mut c = Circuit::new(3);
    c.x(0);
    c.x(1);
    c.measure(0, 0); // c[0] = 1
    c.measure(1, 1); // c[1] = 1, packed = 0b11 = 3
    c.x(2);
    c.c_if_last(vec![0, 1], 3); // 3 == 3 → X(2) 적용
    c.measure(2, 2);

    let engine = ExecutionEngine::with_seed(42);
    let result = engine.run(&c, 100);
    // c[2]=1, c[1]=1, c[0]=1 → "111"
    assert_eq!(result.counts().get("111"), Some(&100));
}

/// IfEq multi-cbit, 조건 다른 값 일 때 fire 안 함.
#[test]
fn test_if_eq_multi_cbit_value_mismatch_skips() {
    let mut c = Circuit::new(3);
    c.x(0);
    // q1 = |0⟩
    c.measure(0, 0); // c[0] = 1
    c.measure(1, 1); // c[1] = 0, packed = 0b01 = 1
    c.x(2);
    c.c_if_last(vec![0, 1], 3); // 1 ≠ 3 → X(2) 스킵
    c.measure(2, 2);

    let engine = ExecutionEngine::with_seed(42);
    let result = engine.run(&c, 100);
    // c[2]=0, c[1]=0, c[0]=1 → "001"
    assert_eq!(result.counts().get("001"), Some(&100));
}

/// 3-큐비트 teleportation: q0 의 임의 상태 |ψ⟩ 를 q2 로 전송.
/// |ψ⟩ = α|0⟩ + β|1⟩, α² + β² = 1.
/// 회로:
///   prepare q0 (Rx θ → |ψ⟩); Bell pair (H q1; CX q1 q2);
///   CX q0 q1; H q0; measure q0 → c0; measure q1 → c1;
///   X q2 c_if c1==1; Z q2 c_if c0==1;
/// 이론: q2 의 최종 statevector 가 |ψ⟩ 와 일치 (분포 |α|² / |β|²).
#[test]
fn test_teleportation_distribution() {
    use std::f64::consts::PI;
    // Rx(θ) on |0⟩ = cos(θ/2)|0⟩ - i sin(θ/2)|1⟩. θ=PI/3 → P(|0⟩)=cos²(PI/6)=0.75.
    let theta: f64 = PI / 3.0;
    let mut c = Circuit::new(3);
    c.rx(theta, 0);
    c.h(1);
    c.cx(1, 2);
    c.cx(0, 1);
    c.h(0);
    c.measure(0, 0);
    c.measure(1, 1);
    c.x(2);
    c.c_if_last(vec![1], 1);
    c.z(2);
    c.c_if_last(vec![0], 1);
    c.measure(2, 2);

    let engine = ExecutionEngine::with_seed(2025);
    let result = engine.run(&c, 10_000);
    let counts = result.counts();

    // q2 의 marginal P(|0⟩): cbit string 의 c[2]=0 인 모든 outcome 합.
    // counts key 는 c[2]c[1]c[0] (MSB=c[2]).
    let mut p_q2_zero = 0usize;
    let mut p_q2_one = 0usize;
    for (k, &v) in counts.iter() {
        let c2 = k.chars().next().unwrap();
        if c2 == '0' {
            p_q2_zero += v;
        } else {
            p_q2_one += v;
        }
    }
    let total = (p_q2_zero + p_q2_one) as f64;
    let ratio_zero = p_q2_zero as f64 / total;
    // 예상 0.75, 4σ binomial bound at shots=10000 ≈ 0.017
    assert!(
        (ratio_zero - 0.75).abs() < 0.03,
        "teleportation P(|0⟩) ratio {ratio_zero} 가 0.75 와 너무 다름"
    );
}

/// Fast path 회귀: dynamic 도 noise 도 없는 표준 회로 (Bell + measure_all)
/// 가 v0.4.0 동작과 동일.
#[test]
fn test_fast_path_no_regression_bell() {
    let mut c = Circuit::new(2);
    c.h(0);
    c.cx(0, 1);
    c.measure_all();
    let engine = ExecutionEngine::with_seed(42);
    let result = engine.run(&c, 1000);
    let counts = result.counts();
    assert!(counts.contains_key("00"));
    assert!(counts.contains_key("11"));
    assert!(!counts.contains_key("01"));
    assert!(!counts.contains_key("10"));
    let total: usize = counts.values().sum();
    assert_eq!(total, 1000);

    let expected = C64::new(std::f64::consts::FRAC_1_SQRT_2, 0.0);
    let sv = result.statevector_f64().expect("default precision is f64");
    assert!(approx_eq(sv.amplitudes()[0], expected, 1e-10));
    assert!(approx_eq(sv.amplitudes()[3], expected, 1e-10));
}

/// Noise 회귀: BitFlip(p=1) on |0⟩ 가 v0.4.0 trajectory mode 와 동일 outcome.
#[test]
fn test_noise_path_no_regression_bit_flip_one() {
    let mut c = Circuit::new(1);
    c.add_noise(NoiseChannel::BitFlip { p: 1.0 }, 0);
    c.measure_all();
    let engine = ExecutionEngine::with_seed(42);
    let result = engine.run(&c, 100);
    assert_eq!(result.counts().get("1"), Some(&100));
}

/// has_dynamic 의 fast-path 결정 로직 검증.
#[test]
fn test_has_dynamic_classification() {
    // Pure unitary + measure_all → not dynamic
    let mut c1 = Circuit::new(2);
    c1.h(0);
    c1.cx(0, 1);
    c1.measure_all();
    assert!(
        !c1.has_dynamic(),
        "pure unitary + measure_all 은 dynamic 아님"
    );

    // Trailing measures only → not dynamic
    let mut c2 = Circuit::new(2);
    c2.h(0);
    c2.cx(0, 1);
    c2.measure(0, 0);
    c2.measure(1, 1);
    assert!(!c2.has_dynamic(), "trailing measures 묶음은 dynamic 아님");

    // mid-circuit measure → dynamic
    let mut c3 = Circuit::new(2);
    c3.h(0);
    c3.measure(0, 0);
    c3.x(1);
    assert!(c3.has_dynamic(), "mid-circuit measure 는 dynamic");

    // Reset → dynamic
    let mut c4 = Circuit::new(1);
    c4.x(0);
    c4.reset(0);
    assert!(c4.has_dynamic(), "reset 은 dynamic");

    // c_if → dynamic
    let mut c5 = Circuit::new(2);
    c5.x(0);
    c5.measure(0, 0);
    c5.x(1);
    c5.c_if_last(vec![0], 1);
    assert!(c5.has_dynamic(), "c_if 는 dynamic");
}

/// Determinism: 같은 seed 로 같은 결과 (cbit register 도입이 RNG 재현성 깨지 않음).
#[test]
fn test_dynamic_circuit_determinism() {
    let mut c = Circuit::new(2);
    c.h(0);
    c.measure(0, 0);
    c.x(1);
    c.c_if_last(vec![0], 1);
    c.measure(1, 1);

    let engine = ExecutionEngine::with_seed(2024);
    let r1 = engine.run(&c, 500);
    let r2 = engine.run(&c, 500);
    assert_eq!(r1.counts(), r2.counts());
}

// ============================================================================
// v0.4.5.1 hotfix: entangled reset 회귀 테스트
//
// v0.4.5.0 의 reset_qubit 은 p1 < 1 일 때 P_0 projector + normalize 만 적용해
// post-selection 으로 동작했음. Bell 페어의 한 큐비트를 reset 하면 다른 큐비트
// 가 결정론적으로 |0⟩ 으로 강제 붕괴되는 버그 (TVD = 0.5 vs Qiskit Aer).
// v0.4.5.1 의 RNG sampling 재구현 후 q1 marginal = I/2 가 정상 복원되는지.
// ============================================================================

/// Bell pair (|00⟩+|11⟩)/√2 의 q0 reset → q1 marginal 이 I/2 (50:50).
#[test]
fn test_reset_on_entangled_qubit_breaks_entanglement() {
    let mut c = Circuit::new(2);
    c.h(0);
    c.cx(0, 1);
    c.reset(0);
    c.measure_all();

    let engine = ExecutionEngine::with_seed(2024);
    let result = engine.run(&c, 20_000);
    let counts = result.counts();

    // 정상 reset: q0=|0⟩ (결정론), q1 marginal = 50:50.
    // outcome string MSB=q1, LSB=q0 → "00" / "10" 만 나와야.
    let c00 = *counts.get("00").unwrap_or(&0) as f64;
    let c10 = *counts.get("10").unwrap_or(&0) as f64;
    let other: usize = counts
        .iter()
        .filter(|(k, _)| k.as_str() != "00" && k.as_str() != "10")
        .map(|(_, v)| *v)
        .sum();
    assert_eq!(
        other, 0,
        "q0 reset 후 '01'/'11' 없어야 (q0 = |0⟩): {counts:?}"
    );

    let total = c00 + c10;
    assert_eq!(total as usize, 20_000);
    let ratio = c00 / total;
    // 3σ binomial bound (N=20000, p=0.5) ≈ 0.011. 0.02 여유.
    assert!(
        (ratio - 0.5).abs() < 0.02,
        "q1 marginal ratio {ratio} 가 0.5 와 너무 다름 (entangled reset 버그 가능성)"
    );
}

/// Bell pair 의 q1 reset → q0 marginal 도 50:50 (대칭).
#[test]
fn test_reset_on_entangled_qubit_either_side() {
    let mut c = Circuit::new(2);
    c.h(0);
    c.cx(0, 1);
    c.reset(1);
    c.measure_all();

    let engine = ExecutionEngine::with_seed(7);
    let result = engine.run(&c, 20_000);
    let counts = result.counts();

    // q1=|0⟩, q0 marginal = 50:50 → "00" / "01" 만.
    let c00 = *counts.get("00").unwrap_or(&0) as f64;
    let c01 = *counts.get("01").unwrap_or(&0) as f64;
    let total = c00 + c01;
    assert_eq!(total as usize, 20_000);
    let ratio = c00 / total;
    assert!(
        (ratio - 0.5).abs() < 0.02,
        "q1 reset 후 q0 marginal ratio {ratio} ≠ 0.5"
    );
}

/// GHZ-3 의 q0 reset → 나머지 q1, q2 가 maximally mixed 의 partial trace
/// (= ½|00⟩⟨00| + ½|11⟩⟨11|, q1==q2 perfect correlation 유지).
/// 측정 → "000" / "110" 만 ~50:50.
#[test]
fn test_reset_preserves_remaining_entanglement() {
    let mut c = Circuit::new(3);
    c.h(0);
    c.cx(0, 1);
    c.cx(0, 2);
    c.reset(0);
    c.measure_all();

    let engine = ExecutionEngine::with_seed(2025);
    let result = engine.run(&c, 20_000);
    let counts = result.counts();

    // outcome string MSB→LSB = q2 q1 q0. q0 = 0 결정론, q1 == q2 (Bell remnant).
    // 가능한 outcome: "000" (q1=q2=0), "110" (q1=q2=1).
    let c000 = *counts.get("000").unwrap_or(&0) as f64;
    let c110 = *counts.get("110").unwrap_or(&0) as f64;
    let other: usize = counts
        .iter()
        .filter(|(k, _)| k.as_str() != "000" && k.as_str() != "110")
        .map(|(_, v)| *v)
        .sum();
    assert_eq!(other, 0, "GHZ q0 reset 후 q1!=q2 outcome 발생: {counts:?}");

    let total = c000 + c110;
    assert_eq!(total as usize, 20_000);
    let ratio = c000 / total;
    assert!(
        (ratio - 0.5).abs() < 0.02,
        "GHZ q0 reset 후 q1=q2 마진 분포 ratio {ratio} ≠ 0.5"
    );
}

// ============================================================================
// v0.4.5.1 hotfix: trailing-measure fast-path cbit 매핑 회귀 테스트
//
// v0.4.5.0 의 fast-path (run_typed_unitary) 는 explicit Measure { q, c } 가 있어도
// measurement::sample 만 호출해 항상 n_qubits 폭의 q-인덱스 순서 비트 문자열을
// 만들었음. 결과: partial measurement / cbit reorder / 동일 큐비트 두 번 측정 시
// Qiskit Aer 와 다른 분포. v0.4.5.1 에서 sample_with_cbit_map 분기로 정정.
// ============================================================================

/// Partial measurement: 3큐비트 중 q1 만 측정. cbit 0 사용 → counts key 폭 1.
#[test]
fn test_fast_path_partial_measurement_uses_cbit_width() {
    let mut c = Circuit::new(3);
    c.h(0);
    c.h(1);
    c.h(2);
    c.measure(1, 0); // 큐비트 1 만 cbit 0 으로 측정. n_cbits = 1.

    assert!(!c.has_dynamic(), "trailing single measure 는 fast-path");

    let engine = ExecutionEngine::with_seed(42);
    let result = engine.run(&c, 10_000);
    let counts = result.counts();

    // 모든 outcome key 가 정확히 1 비트 폭 ('0' 또는 '1') 이어야.
    for k in counts.keys() {
        assert_eq!(k.len(), 1, "partial measure 의 key 폭이 1 이 아님: {k:?}");
        assert!(k == "0" || k == "1");
    }
    let total: usize = counts.values().sum();
    assert_eq!(total, 10_000);
    // q1 = H|0⟩ marginal = 50:50.
    let c0 = *counts.get("0").unwrap_or(&0) as f64;
    let ratio = c0 / total as f64;
    assert!(
        (ratio - 0.5).abs() < 0.02,
        "partial measure ratio {ratio} ≠ 0.5"
    );
}

/// Cbit reorder: q0→c2, q1→c1, q2→c0 매핑. q0=|1⟩, q1=q2=|0⟩.
/// outcome string MSB→LSB = c2 c1 c0 = q0 q1 q2 = "1 0 0" = "100".
#[test]
fn test_fast_path_cbit_reorder() {
    let mut c = Circuit::new(3);
    c.x(0);
    c.measure(0, 2);
    c.measure(1, 1);
    c.measure(2, 0);

    assert!(!c.has_dynamic(), "trailing measures 묶음은 fast-path");

    let engine = ExecutionEngine::with_seed(1);
    let result = engine.run(&c, 100);
    assert_eq!(
        result.counts().get("100"),
        Some(&100),
        "cbit reorder 결과 잘못: {:?}",
        result.counts()
    );
}

/// Disjoint subset measure: q0 만 측정 (q1, q2 는 H 후 측정 안 함).
/// counts key 폭 = 1, ratio ~ 0.5.
#[test]
fn test_fast_path_disjoint_subset_measure() {
    let mut c = Circuit::new(3);
    c.h(0);
    c.h(1);
    c.h(2);
    c.measure(0, 0);

    let engine = ExecutionEngine::with_seed(7);
    let result = engine.run(&c, 10_000);
    let counts = result.counts();

    for k in counts.keys() {
        assert_eq!(k.len(), 1, "subset measure key 폭 ≠ 1: {k:?}");
    }
    let c0 = *counts.get("0").unwrap_or(&0) as f64;
    let total: usize = counts.values().sum();
    assert_eq!(total, 10_000);
    let ratio = c0 / total as f64;
    assert!((ratio - 0.5).abs() < 0.02, "subset measure ratio {ratio}");
}

/// 회귀 0건: standard MeasureAll 회로 (n_cbits = n_qubits, q==c) 는 동일 결과.
#[test]
fn test_fast_path_measure_all_unchanged() {
    let mut c = Circuit::new(3);
    c.h(0);
    c.cx(0, 1);
    c.cx(0, 2);
    c.measure_all();

    let engine = ExecutionEngine::with_seed(2024);
    let result = engine.run(&c, 5_000);
    let counts = result.counts();

    // GHZ-3: "000" / "111" 만, ~50:50.
    let total: usize = counts.values().sum();
    assert_eq!(total, 5_000);
    for k in counts.keys() {
        assert!(k == "000" || k == "111", "GHZ unexpected outcome: {k}");
    }
    let c000 = *counts.get("000").unwrap_or(&0) as f64;
    let ratio = c000 / total as f64;
    assert!((ratio - 0.5).abs() < 0.03, "MeasureAll ratio {ratio}");
}

/// 회귀 0건: 모든 큐비트가 q==c 매핑된 explicit measure 들 → MeasureAll 와 동일.
#[test]
fn test_fast_path_explicit_measure_qeqc_matches_measure_all() {
    let mut c1 = Circuit::new(3);
    c1.h(0);
    c1.cx(0, 1);
    c1.cx(0, 2);
    c1.measure(0, 0);
    c1.measure(1, 1);
    c1.measure(2, 2);

    let engine = ExecutionEngine::with_seed(2024);
    let result = engine.run(&c1, 5_000);
    let counts = result.counts();

    let total: usize = counts.values().sum();
    assert_eq!(total, 5_000);
    for k in counts.keys() {
        assert!(
            k == "000" || k == "111",
            "GHZ explicit-measure unexpected outcome: {k}"
        );
    }
}

// ============================================================================
// v0.4.7 Cut 7 — Block-form classical control flow tests
// ============================================================================

/// IfElse with else_body: false branch 가 정상 실행.
#[test]
fn test_if_else_false_branch_runs_else_body() {
    // c[0] = 0 (q0 = |0⟩ measure → 0).  if (c==1) X(1) else Y(1).
    // false → Y 적용.  Y|0⟩ = i|1⟩ → measure → 1.
    let mut c = Circuit::new(2);
    c.measure(0, 0);
    c.add_if_else(
        vec![0],
        1,
        vec![qsim_simulator::Instruction::ApplyGate {
            gate: qsim_core::Gate::X,
            targets: vec![1],
        }],
        Some(vec![qsim_simulator::Instruction::ApplyGate {
            gate: qsim_core::Gate::Y,
            targets: vec![1],
        }]),
    );
    c.measure(1, 1);

    let engine = ExecutionEngine::with_seed(42);
    let result = engine.run(&c, 100);
    // c1=1, c0=0 → "10".
    assert_eq!(result.counts().get("10"), Some(&100));
}

/// IfElse with then_body 가 multi-instruction sub-circuit.
#[test]
fn test_if_else_multi_instruction_body() {
    let mut c = Circuit::new(3);
    c.x(0); // q0=1
    c.measure(0, 0);
    // if (c==1) { x(1); x(2); } — body 2 instruction.
    c.add_if_else(
        vec![0],
        1,
        vec![
            qsim_simulator::Instruction::ApplyGate {
                gate: qsim_core::Gate::X,
                targets: vec![1],
            },
            qsim_simulator::Instruction::ApplyGate {
                gate: qsim_core::Gate::X,
                targets: vec![2],
            },
        ],
        None,
    );
    c.measure(1, 1);
    c.measure(2, 2);
    let engine = ExecutionEngine::with_seed(42);
    let result = engine.run(&c, 100);
    // c2=1, c1=1, c0=1 → "111".
    assert_eq!(result.counts().get("111"), Some(&100));
}

/// ForLoop: body 를 N 번 반복.  X 게이트를 짝수 번 반복하면 identity.
#[test]
fn test_for_loop_even_iterations_identity() {
    let mut c = Circuit::new(1);
    c.add_for_loop(
        4, // 짝수 iteration → X⁴ = I → q0 = |0⟩
        vec![qsim_simulator::Instruction::ApplyGate {
            gate: qsim_core::Gate::X,
            targets: vec![0],
        }],
    );
    c.measure(0, 0);
    let engine = ExecutionEngine::with_seed(42);
    let result = engine.run(&c, 100);
    assert_eq!(result.counts().get("0"), Some(&100));
}

/// ForLoop: 홀수 iteration → X 한 번 적용한 것과 동일.
#[test]
fn test_for_loop_odd_iterations_flip() {
    let mut c = Circuit::new(1);
    c.add_for_loop(
        3,
        vec![qsim_simulator::Instruction::ApplyGate {
            gate: qsim_core::Gate::X,
            targets: vec![0],
        }],
    );
    c.measure(0, 0);
    let engine = ExecutionEngine::with_seed(42);
    let result = engine.run(&c, 100);
    assert_eq!(result.counts().get("1"), Some(&100));
}

/// WhileLoop: cond 가 즉시 false 면 body 실행 안 함.
#[test]
fn test_while_loop_cond_false_skips_body() {
    let mut c = Circuit::new(1);
    // c[0] 은 초기 0.  while (c==1) { X(0) } — cond false → body skip.
    c.measure(0, 0); // c[0] = 0
    c.add_while_loop(
        vec![0],
        1,
        vec![qsim_simulator::Instruction::ApplyGate {
            gate: qsim_core::Gate::X,
            targets: vec![0],
        }],
        16,
    );
    c.measure(0, 0); // c[0] = 0 그대로
    let engine = ExecutionEngine::with_seed(42);
    let result = engine.run(&c, 100);
    assert_eq!(result.counts().get("0"), Some(&100));
}

/// WhileLoop: cond 가 body 안에서 갱신되어 종료되는 패턴.
/// c[0] 초기 1, body: X(0); measure(0,0).  X 후 measure → c[0]=1, 다시 X→measure → c[0]=0,
/// while loop 종료.  최종 q0=|0⟩ (X 두 번 적용 후 measure 돼서 |0⟩).
#[test]
fn test_while_loop_body_updates_condition() {
    let mut c = Circuit::new(1);
    c.x(0); // q0=|1⟩
    c.measure(0, 0); // c[0] = 1
    c.add_while_loop(
        vec![0],
        1,
        vec![
            qsim_simulator::Instruction::ApplyGate {
                gate: qsim_core::Gate::X,
                targets: vec![0],
            },
            qsim_simulator::Instruction::Measure { qubit: 0, cbit: 0 },
        ],
        16,
    );
    let engine = ExecutionEngine::with_seed(42);
    let result = engine.run(&c, 100);
    // 1차: c[0]=1, body 실행 후 q0 = |0⟩, measure → c[0]=0. cond fails → 종료.
    // 최종 c[0] = 0 → "0".
    assert_eq!(result.counts().get("0"), Some(&100));
}

/// WhileLoop: max_iters 안전 bound — cond 항상 true 라도 max_iters 회 후 종료.
#[test]
fn test_while_loop_max_iters_safety_bound() {
    let mut c = Circuit::new(1);
    c.x(0);
    c.measure(0, 0); // c[0] = 1
                     // body 가 cond 갱신 안 함 → 무한 loop 위험.  max_iters=10.
    c.add_while_loop(
        vec![0],
        1,
        vec![qsim_simulator::Instruction::ApplyGate {
            gate: qsim_core::Gate::Id,
            targets: vec![0],
        }],
        10,
    );
    let engine = ExecutionEngine::with_seed(42);
    let result = engine.run(&c, 100);
    // max_iters 회 실행 후 종료.  최종 q0=|1⟩, c[0]=1 → "1".
    assert_eq!(result.counts().get("1"), Some(&100));
}

/// Switch: 매칭되는 case 의 body 실행.
#[test]
fn test_switch_case_match() {
    let mut c = Circuit::new(2);
    c.x(0);
    c.measure(0, 0); // c[0] = 1
    c.add_switch(
        vec![0],
        vec![
            (
                Some(0),
                vec![qsim_simulator::Instruction::ApplyGate {
                    gate: qsim_core::Gate::X,
                    targets: vec![1],
                }],
            ),
            (
                Some(1),
                vec![qsim_simulator::Instruction::ApplyGate {
                    gate: qsim_core::Gate::Y,
                    targets: vec![1],
                }],
            ),
            (
                None, // default
                vec![qsim_simulator::Instruction::ApplyGate {
                    gate: qsim_core::Gate::Z,
                    targets: vec![1],
                }],
            ),
        ],
    );
    c.measure(1, 1);
    let engine = ExecutionEngine::with_seed(42);
    let result = engine.run(&c, 100);
    // c[0]=1 매칭 → Y(1) → q1=i|1⟩, measure → 1.  c1=1 c0=1 → "11".
    assert_eq!(result.counts().get("11"), Some(&100));
}

/// Switch: default case (어느 case 와도 매칭 안 될 때).
#[test]
fn test_switch_default_case() {
    let mut c = Circuit::new(2);
    // c[0] = 0
    c.measure(0, 0);
    c.add_switch(
        vec![0],
        vec![
            (
                Some(2), // 어느 매칭 안 됨
                vec![qsim_simulator::Instruction::ApplyGate {
                    gate: qsim_core::Gate::X,
                    targets: vec![1],
                }],
            ),
            (
                None, // default
                vec![qsim_simulator::Instruction::ApplyGate {
                    gate: qsim_core::Gate::H,
                    targets: vec![1],
                }],
            ),
        ],
    );
    c.measure(1, 1);
    let engine = ExecutionEngine::with_seed(123);
    let result = engine.run(&c, 5000);
    // default → H(1) → 50:50.  c1 ∈ {0,1}, c0 = 0.  outcomes "00", "10".
    let c00 = *result.counts().get("00").unwrap_or(&0);
    let c10 = *result.counts().get("10").unwrap_or(&0);
    assert_eq!(c00 + c10, 5000);
    let other: usize = result
        .counts()
        .iter()
        .filter(|(k, _)| k.as_str() != "00" && k.as_str() != "10")
        .map(|(_, v)| *v)
        .sum();
    assert_eq!(other, 0);
}

/// Nested IfElse — IfElse 안에 IfElse.
#[test]
fn test_nested_if_else() {
    use qsim_simulator::Instruction as I;
    let mut c = Circuit::new(2);
    c.x(0);
    c.x(1);
    c.measure(0, 0); // c0=1
    c.measure(1, 1); // c1=1
                     // if (c0==1) { if (c1==1) { x(0) } else { y(0) } } else { z(0) }
    let inner_if_else = I::IfElse {
        cbit_indices: vec![1],
        value: 1,
        then_body: vec![I::ApplyGate {
            gate: qsim_core::Gate::X,
            targets: vec![0],
        }],
        else_body: Some(vec![I::ApplyGate {
            gate: qsim_core::Gate::Y,
            targets: vec![0],
        }]),
    };
    c.add_if_else(
        vec![0],
        1,
        vec![inner_if_else],
        Some(vec![I::ApplyGate {
            gate: qsim_core::Gate::Z,
            targets: vec![0],
        }]),
    );
    // q0 was |1⟩, c0=1 → outer then.  c1=1 → inner then → X|1⟩ = |0⟩.
    c.measure(0, 0);
    let engine = ExecutionEngine::with_seed(42);
    let result = engine.run(&c, 100);
    // 최종 c0=0 (X 후 measure), c1=1 → "10".
    assert_eq!(result.counts().get("10"), Some(&100));
}

/// has_dynamic 이 새 변종들도 dynamic 으로 분류하는지.
#[test]
fn test_has_dynamic_block_control_flow() {
    use qsim_simulator::Instruction as I;
    // IfElse → dynamic.
    let mut c = Circuit::new(1);
    c.measure(0, 0);
    c.add_if_else(vec![0], 0, vec![], None);
    assert!(c.has_dynamic());

    // WhileLoop → dynamic.
    let mut c = Circuit::new(1);
    c.measure(0, 0);
    c.add_while_loop(vec![0], 0, vec![], 16);
    assert!(c.has_dynamic());

    // ForLoop → dynamic.
    let mut c = Circuit::new(1);
    c.add_for_loop(3, vec![]);
    assert!(c.has_dynamic());

    // Switch → dynamic.
    let mut c = Circuit::new(1);
    c.measure(0, 0);
    c.add_switch(vec![0], vec![]);
    assert!(c.has_dynamic());

    // Pure unitary 회로는 dynamic 아님 (회귀).
    let mut c = Circuit::new(2);
    c.h(0);
    c.cx(0, 1);
    c.measure_all();
    assert!(!c.has_dynamic());

    let _ = I::IfElse {
        cbit_indices: vec![],
        value: 0,
        then_body: vec![],
        else_body: None,
    };
}

/// Closure-based builder API smoke test.
#[test]
fn test_circuit_closure_if_else_builder() {
    let mut c = Circuit::new(2);
    c.x(0);
    c.measure(0, 0);
    c.if_else(
        vec![0],
        1,
        |sub| {
            sub.x(1);
        },
        Some(Box::new(|sub: &mut Circuit| {
            sub.y(1);
        })),
    );
    c.measure(1, 1);
    let engine = ExecutionEngine::with_seed(42);
    let result = engine.run(&c, 100);
    assert_eq!(result.counts().get("11"), Some(&100));
}

#[test]
fn test_circuit_closure_for_loop_builder() {
    let mut c = Circuit::new(1);
    c.for_loop(2, |sub| {
        sub.x(0);
    });
    c.measure(0, 0);
    let engine = ExecutionEngine::with_seed(42);
    let result = engine.run(&c, 100);
    assert_eq!(result.counts().get("0"), Some(&100)); // X² = I.
}

#[test]
fn test_circuit_closure_while_loop_builder() {
    let mut c = Circuit::new(1);
    c.x(0);
    c.measure(0, 0);
    c.while_loop(vec![0], 1, 16, |sub| {
        sub.x(0);
        sub.measure(0, 0);
    });
    let engine = ExecutionEngine::with_seed(42);
    let result = engine.run(&c, 100);
    assert_eq!(result.counts().get("0"), Some(&100));
}
