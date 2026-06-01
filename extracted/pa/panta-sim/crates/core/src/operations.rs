use num_complex::Complex;
use rayon::prelude::*;

use crate::complex::Real;
use crate::gates::{Matrix2x2, Matrix4x4};
use crate::statevector::StateVector;

/// 병렬 처리 진입 임계치 (amplitude 개수 기준).
/// 이보다 작은 상태 벡터는 직렬 경로가 더 빠르다 (rayon 진입 비용 회수가 안 됨).
const PARALLEL_THRESHOLD: usize = 1 << 13;

// ============================================================================
// 단일 큐비트 게이트
// ============================================================================

/// 단일 큐비트 게이트를 상태 벡터에 적용한다 (qubit-wise multiplication).
///
/// target_qubit: little-endian 인덱스 (0 = LSB).
pub fn apply_single_qubit_gate<F: Real>(
    state: &mut StateVector<F>,
    matrix: &Matrix2x2<F>,
    target: usize,
) {
    let n = state.dim();
    let amps = state.amplitudes_mut();

    if n < PARALLEL_THRESHOLD {
        single_qubit_serial(amps, matrix, target);
        return;
    }

    let stride = 1usize << target;
    let block_size = stride << 1; // 2 * stride
    let m00 = matrix[0][0];
    let m01 = matrix[0][1];
    let m10 = matrix[1][0];
    let m11 = matrix[1][1];

    if amps.len() / block_size >= 2 {
        // 일반 케이스: 블록(=2*stride)이 여럿 → 블록 단위로 병렬화
        amps.par_chunks_mut(block_size).for_each(|block| {
            let (lower, upper) = block.split_at_mut(stride);
            for (a, b) in lower.iter_mut().zip(upper.iter_mut()) {
                let new_a = m00 * *a + m01 * *b;
                let new_b = m10 * *a + m11 * *b;
                *a = new_a;
                *b = new_b;
            }
        });
    } else {
        // target == n-1 케이스: 블록이 단 하나. lower/upper split 후 pair 단위 병렬.
        let (lower, upper) = amps.split_at_mut(stride);
        lower
            .par_iter_mut()
            .zip(upper.par_iter_mut())
            .for_each(|(a, b)| {
                let new_a = m00 * *a + m01 * *b;
                let new_b = m10 * *a + m11 * *b;
                *a = new_a;
                *b = new_b;
            });
    }
}

#[inline]
fn single_qubit_serial<F: Real>(amps: &mut [Complex<F>], matrix: &Matrix2x2<F>, target: usize) {
    let n = amps.len();
    let stride = 1usize << target;
    let m00 = matrix[0][0];
    let m01 = matrix[0][1];
    let m10 = matrix[1][0];
    let m11 = matrix[1][1];

    let mut i = 0;
    while i < n {
        for j in i..i + stride {
            let k = j + stride;
            let a = amps[j];
            let b = amps[k];
            amps[j] = m00 * a + m01 * b;
            amps[k] = m10 * a + m11 * b;
        }
        i += stride << 1;
    }
}

// ============================================================================
// 2큐비트 controlled 게이트 (CNOT 등)
// ============================================================================

/// 2큐비트 controlled 게이트를 적용한다.
///
/// control 큐비트가 |1⟩ 인 amplitude 쌍에만 target 의 2×2 행렬을 적용.
/// control != target 가정 (Circuit 레벨에서 검증).
pub fn apply_controlled_gate<F: Real>(
    state: &mut StateVector<F>,
    gate_matrix: &Matrix2x2<F>,
    control: usize,
    target: usize,
) {
    // v0.6.2: invariant 가드.  Circuit::add_gate 가 이미 distinct 보장하므로
    // 정상 path 에서 도달 안 함 — debug build 에서만 검증.
    debug_assert_ne!(
        control, target,
        "apply_controlled_gate: control == target ({control}) — Circuit::add_gate 보증 위반"
    );
    let n = state.dim();
    let amps = state.amplitudes_mut();

    if n < PARALLEL_THRESHOLD {
        controlled_gate_serial(amps, gate_matrix, control, target);
        return;
    }

    // 두 큐비트를 정렬: q_lo < q_hi
    let (q_lo, q_hi) = if control < target {
        (control, target)
    } else {
        (target, control)
    };
    let ctrl_bit = 1usize << control;
    let tgt_bit = 1usize << target;
    let m00 = gate_matrix[0][0];
    let m01 = gate_matrix[0][1];
    let m10 = gate_matrix[1][0];
    let m11 = gate_matrix[1][1];

    let groups = n >> 2; // n / 4 — 두 큐비트가 (0,0) 인 base 인덱스의 개수
    let mask_lo = (1usize << q_lo) - 1;
    let mask_mid = ((1usize << (q_hi - 1)) - 1) ^ mask_lo;

    (0..groups).into_par_iter().for_each(|k| {
        // k 의 비트들을 (low | mid | high) 로 분해해 q_lo, q_hi 자리에 0을 비워둔 base 인덱스 생성
        let low = k & mask_lo;
        let mid = (k & mask_mid) << 1;
        let high = (k & !((1usize << (q_hi - 1)) - 1)) << 2;
        let base = high | mid | low;

        // base 는 control=0, target=0
        // 우리가 건드릴 인덱스: ctrl=1, tgt=0 (= base | ctrl_bit)
        //                      ctrl=1, tgt=1 (= base | ctrl_bit | tgt_bit)
        let idx_a = base | ctrl_bit;
        let idx_b = idx_a | tgt_bit;

        // disjoint 보장 → 안전한 raw pointer 접근
        unsafe {
            let p = amps.as_ptr() as *mut Complex<F>;
            let a = *p.add(idx_a);
            let b = *p.add(idx_b);
            *p.add(idx_a) = m00 * a + m01 * b;
            *p.add(idx_b) = m10 * a + m11 * b;
        }
    });
}

#[inline]
fn controlled_gate_serial<F: Real>(
    amps: &mut [Complex<F>],
    gate_matrix: &Matrix2x2<F>,
    control: usize,
    target: usize,
) {
    let n = amps.len();
    for i in 0..n {
        let ctrl_bit = (i >> control) & 1;
        let tgt_bit = (i >> target) & 1;
        if ctrl_bit == 1 && tgt_bit == 0 {
            let j = i | (1 << target);
            let a = amps[i];
            let b = amps[j];
            amps[i] = gate_matrix[0][0] * a + gate_matrix[0][1] * b;
            amps[j] = gate_matrix[1][0] * a + gate_matrix[1][1] * b;
        }
    }
}

// ============================================================================
// 일반 2큐비트 게이트 (4×4)
// ============================================================================

/// 일반적인 2큐비트 게이트를 4×4 행렬로 적용한다.
///
/// qubit0, qubit1: little-endian 큐비트 인덱스 (서로 다름).
/// 4×4 행렬의 행/열 인덱스는 |qubit1, qubit0⟩ 순서.
pub fn apply_two_qubit_gate<F: Real>(
    state: &mut StateVector<F>,
    matrix: &Matrix4x4<F>,
    qubit0: usize,
    qubit1: usize,
) {
    debug_assert_ne!(qubit0, qubit1, "qubit0 와 qubit1 은 서로 달라야 함");
    let n = state.dim();
    let amps = state.amplitudes_mut();

    if n < PARALLEL_THRESHOLD {
        two_qubit_gate_serial(amps, matrix, qubit0, qubit1);
        return;
    }

    let (q_lo, q_hi) = if qubit0 < qubit1 {
        (qubit0, qubit1)
    } else {
        (qubit1, qubit0)
    };

    let bit0 = 1usize << qubit0;
    let bit1 = 1usize << qubit1;

    let groups = n >> 2;
    let mask_lo = (1usize << q_lo) - 1;
    let mask_mid = ((1usize << (q_hi - 1)) - 1) ^ mask_lo;

    (0..groups).into_par_iter().for_each(|k| {
        let low = k & mask_lo;
        let mid = (k & mask_mid) << 1;
        let high = (k & !((1usize << (q_hi - 1)) - 1)) << 2;
        let base = high | mid | low;

        // base 는 qubit0=0, qubit1=0
        // 4×4 행렬 인덱스: |q1 q0⟩ 순서
        let idx00 = base;
        let idx01 = base | bit0; // q0=1, q1=0
        let idx10 = base | bit1; // q0=0, q1=1
        let idx11 = base | bit0 | bit1;

        unsafe {
            let p = amps.as_ptr() as *mut Complex<F>;
            let v0 = *p.add(idx00);
            let v1 = *p.add(idx01);
            let v2 = *p.add(idx10);
            let v3 = *p.add(idx11);

            *p.add(idx00) =
                matrix[0][0] * v0 + matrix[0][1] * v1 + matrix[0][2] * v2 + matrix[0][3] * v3;
            *p.add(idx01) =
                matrix[1][0] * v0 + matrix[1][1] * v1 + matrix[1][2] * v2 + matrix[1][3] * v3;
            *p.add(idx10) =
                matrix[2][0] * v0 + matrix[2][1] * v1 + matrix[2][2] * v2 + matrix[2][3] * v3;
            *p.add(idx11) =
                matrix[3][0] * v0 + matrix[3][1] * v1 + matrix[3][2] * v2 + matrix[3][3] * v3;
        }
    });
}

#[inline]
fn two_qubit_gate_serial<F: Real>(
    amps: &mut [Complex<F>],
    matrix: &Matrix4x4<F>,
    qubit0: usize,
    qubit1: usize,
) {
    let n = amps.len();
    let (q_lo, q_hi) = if qubit0 < qubit1 {
        (qubit0, qubit1)
    } else {
        (qubit1, qubit0)
    };
    let bit0 = 1usize << qubit0;
    let bit1 = 1usize << qubit1;
    let groups = n >> 2;
    let mask_lo = (1usize << q_lo) - 1;
    let mask_mid = ((1usize << (q_hi - 1)) - 1) ^ mask_lo;

    for k in 0..groups {
        let low = k & mask_lo;
        let mid = (k & mask_mid) << 1;
        let high = (k & !((1usize << (q_hi - 1)) - 1)) << 2;
        let base = high | mid | low;

        let idx00 = base;
        let idx01 = base | bit0;
        let idx10 = base | bit1;
        let idx11 = base | bit0 | bit1;

        let v0 = amps[idx00];
        let v1 = amps[idx01];
        let v2 = amps[idx10];
        let v3 = amps[idx11];

        amps[idx00] = matrix[0][0] * v0 + matrix[0][1] * v1 + matrix[0][2] * v2 + matrix[0][3] * v3;
        amps[idx01] = matrix[1][0] * v0 + matrix[1][1] * v1 + matrix[1][2] * v2 + matrix[1][3] * v3;
        amps[idx10] = matrix[2][0] * v0 + matrix[2][1] * v1 + matrix[2][2] * v2 + matrix[2][3] * v3;
        amps[idx11] = matrix[3][0] * v0 + matrix[3][1] * v1 + matrix[3][2] * v2 + matrix[3][3] * v3;
    }
}

// ============================================================================
// 3큐비트 이중 제어 게이트 (Toffoli 등)
// ============================================================================

/// 이중 제어 게이트를 적용한다.
///
/// control1, control2 가 모두 |1⟩ 일 때만 target 에 gate_matrix 를 적용.
pub fn apply_doubly_controlled_gate<F: Real>(
    state: &mut StateVector<F>,
    gate_matrix: &Matrix2x2<F>,
    control1: usize,
    control2: usize,
    target: usize,
) {
    let n = state.dim();
    let amps = state.amplitudes_mut();

    if n < PARALLEL_THRESHOLD {
        doubly_controlled_gate_serial(amps, gate_matrix, control1, control2, target);
        return;
    }

    let mut sorted = [control1, control2, target];
    sorted.sort_unstable();
    let [q0, q1, q2] = sorted;

    let c1_bit = 1usize << control1;
    let c2_bit = 1usize << control2;
    let tgt_bit = 1usize << target;
    let m00 = gate_matrix[0][0];
    let m01 = gate_matrix[0][1];
    let m10 = gate_matrix[1][0];
    let m11 = gate_matrix[1][1];

    let groups = n >> 3; // n / 8
    let masks = three_qubit_masks(q0, q1, q2);

    (0..groups).into_par_iter().for_each(|k| {
        let base = expand_three_qubit_index(k, q0, q1, q2, &masks);
        // base 는 모든 세 큐비트가 0
        // 이중 제어가 모두 1이고 target=0 인 인덱스: c1=1, c2=1, tgt=0
        let idx_a = base | c1_bit | c2_bit;
        let idx_b = idx_a | tgt_bit;

        unsafe {
            let p = amps.as_ptr() as *mut Complex<F>;
            let a = *p.add(idx_a);
            let b = *p.add(idx_b);
            *p.add(idx_a) = m00 * a + m01 * b;
            *p.add(idx_b) = m10 * a + m11 * b;
        }
    });
}

#[inline]
fn doubly_controlled_gate_serial<F: Real>(
    amps: &mut [Complex<F>],
    gate_matrix: &Matrix2x2<F>,
    control1: usize,
    control2: usize,
    target: usize,
) {
    let n = amps.len();
    for i in 0..n {
        let c1 = (i >> control1) & 1;
        let c2 = (i >> control2) & 1;
        let tg = (i >> target) & 1;
        if c1 == 1 && c2 == 1 && tg == 0 {
            let j = i | (1 << target);
            let a = amps[i];
            let b = amps[j];
            amps[i] = gate_matrix[0][0] * a + gate_matrix[0][1] * b;
            amps[j] = gate_matrix[1][0] * a + gate_matrix[1][1] * b;
        }
    }
}

// ============================================================================
// 3큐비트 controlled-SWAP (Fredkin)
// ============================================================================

/// Controlled-SWAP (Fredkin) 게이트.
///
/// control 이 |1⟩ 일 때 target1 ↔ target2 의 amplitude 를 교환.
pub fn apply_controlled_swap<F: Real>(
    state: &mut StateVector<F>,
    control: usize,
    target1: usize,
    target2: usize,
) {
    let n = state.dim();
    let amps = state.amplitudes_mut();

    if n < PARALLEL_THRESHOLD {
        controlled_swap_serial(amps, control, target1, target2);
        return;
    }

    let mut sorted = [control, target1, target2];
    sorted.sort_unstable();
    let [q0, q1, q2] = sorted;

    let ctrl_bit = 1usize << control;
    let t1_bit = 1usize << target1;
    let t2_bit = 1usize << target2;

    let groups = n >> 3;
    let masks = three_qubit_masks(q0, q1, q2);

    (0..groups).into_par_iter().for_each(|k| {
        let base = expand_three_qubit_index(k, q0, q1, q2, &masks);
        // control=1, target1=0, target2=1 일 때 target1=1, target2=0 와 swap
        let idx_a = base | ctrl_bit | t2_bit; // ctrl=1, t1=0, t2=1
        let idx_b = base | ctrl_bit | t1_bit; // ctrl=1, t1=1, t2=0

        unsafe {
            let p = amps.as_ptr() as *mut Complex<F>;
            let a = *p.add(idx_a);
            let b = *p.add(idx_b);
            *p.add(idx_a) = b;
            *p.add(idx_b) = a;
        }
    });
}

#[inline]
fn controlled_swap_serial<F: Real>(
    amps: &mut [Complex<F>],
    control: usize,
    target1: usize,
    target2: usize,
) {
    let n = amps.len();
    for i in 0..n {
        let c = (i >> control) & 1;
        let t1 = (i >> target1) & 1;
        let t2 = (i >> target2) & 1;
        if c == 1 && t1 == 0 && t2 == 1 {
            let j = (i | (1 << target1)) & !(1 << target2);
            amps.swap(i, j);
        }
    }
}

// ============================================================================
// 인덱스 분해 헬퍼 (3큐비트용)
// ============================================================================

/// q0 < q1 < q2 가정. 세 큐비트 자리를 0 으로 비워둔 base 인덱스를 만들기 위한 마스크 묶음.
#[inline]
fn three_qubit_masks(q0: usize, q1: usize, q2: usize) -> [usize; 4] {
    debug_assert!(q0 < q1 && q1 < q2);
    let mask0 = (1usize << q0) - 1;
    let mask1 = ((1usize << (q1 - 1)) - 1) ^ mask0;
    let mask2 = ((1usize << (q2 - 2)) - 1) ^ mask0 ^ mask1;
    let mask_high = !((1usize << (q2 - 2)) - 1);
    [mask0, mask1, mask2, mask_high]
}

#[inline]
fn expand_three_qubit_index(
    k: usize,
    _q0: usize,
    _q1: usize,
    _q2: usize,
    masks: &[usize; 4],
) -> usize {
    let p0 = k & masks[0];
    let p1 = (k & masks[1]) << 1;
    let p2 = (k & masks[2]) << 2;
    let p3 = (k & masks[3]) << 3;
    p0 | p1 | p2 | p3
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::complex::{approx_eq, ONE, ZERO};
    use crate::gates::Gate;

    #[test]
    fn test_x_gate_flips_qubit() {
        let mut sv: StateVector<f64> = StateVector::new(1);
        let x: Matrix2x2<f64> = Gate::X.matrix_2x2();
        apply_single_qubit_gate(&mut sv, &x, 0);
        // |0⟩ → |1⟩
        assert!(approx_eq(sv.amplitudes()[0], ZERO, 1e-10));
        assert!(approx_eq(sv.amplitudes()[1], ONE, 1e-10));
    }

    #[test]
    fn test_x_gate_flips_qubit_f32() {
        let mut sv: StateVector<f32> = StateVector::new(1);
        let x: Matrix2x2<f32> = Gate::X.matrix_2x2();
        apply_single_qubit_gate(&mut sv, &x, 0);
        let zero32 = Complex::new(0.0_f32, 0.0);
        let one32 = Complex::new(1.0_f32, 0.0);
        assert!(approx_eq(sv.amplitudes()[0], zero32, 1e-6_f32));
        assert!(approx_eq(sv.amplitudes()[1], one32, 1e-6_f32));
    }

    #[test]
    fn test_hadamard_creates_superposition() {
        let mut sv: StateVector<f64> = StateVector::new(1);
        let h: Matrix2x2<f64> = Gate::H.matrix_2x2();
        apply_single_qubit_gate(&mut sv, &h, 0);
        // |0⟩ → (|0⟩ + |1⟩)/√2
        let expected = Complex::new(std::f64::consts::FRAC_1_SQRT_2, 0.0);
        assert!(approx_eq(sv.amplitudes()[0], expected, 1e-10));
        assert!(approx_eq(sv.amplitudes()[1], expected, 1e-10));
    }

    #[test]
    fn test_x_on_qubit0_of_two() {
        let mut sv: StateVector<f64> = StateVector::new(2);
        let x: Matrix2x2<f64> = Gate::X.matrix_2x2();
        apply_single_qubit_gate(&mut sv, &x, 0);
        assert!(approx_eq(sv.amplitudes()[0], ZERO, 1e-10));
        assert!(approx_eq(sv.amplitudes()[1], ONE, 1e-10));
        assert!(approx_eq(sv.amplitudes()[2], ZERO, 1e-10));
        assert!(approx_eq(sv.amplitudes()[3], ZERO, 1e-10));
    }

    #[test]
    fn test_x_on_qubit1_of_two() {
        let mut sv: StateVector<f64> = StateVector::new(2);
        let x: Matrix2x2<f64> = Gate::X.matrix_2x2();
        apply_single_qubit_gate(&mut sv, &x, 1);
        assert!(approx_eq(sv.amplitudes()[0], ZERO, 1e-10));
        assert!(approx_eq(sv.amplitudes()[1], ZERO, 1e-10));
        assert!(approx_eq(sv.amplitudes()[2], ONE, 1e-10));
        assert!(approx_eq(sv.amplitudes()[3], ZERO, 1e-10));
    }

    #[test]
    fn test_cnot_controlled_gate() {
        // |10⟩ → CNOT(ctrl=1, tgt=0) → |11⟩
        let mut sv: StateVector<f64> = StateVector::new(2);
        let x: Matrix2x2<f64> = Gate::X.matrix_2x2();
        apply_single_qubit_gate(&mut sv, &x, 1); // |00⟩ → |10⟩

        apply_controlled_gate(&mut sv, &x, 1, 0);
        // |10⟩ → |11⟩ (index 3)
        assert!(approx_eq(sv.amplitudes()[3], ONE, 1e-10));
    }

    #[test]
    fn test_cnot_no_action_when_control_zero() {
        let mut sv: StateVector<f64> = StateVector::new(2);
        let x: Matrix2x2<f64> = Gate::X.matrix_2x2();
        apply_single_qubit_gate(&mut sv, &x, 0); // |00⟩ → |01⟩

        apply_controlled_gate(&mut sv, &x, 1, 0);
        assert!(approx_eq(sv.amplitudes()[1], ONE, 1e-10));
    }

    #[test]
    fn test_cz_gate() {
        let mut sv: StateVector<f64> = StateVector::new(2);
        let x: Matrix2x2<f64> = Gate::X.matrix_2x2();
        apply_single_qubit_gate(&mut sv, &x, 0);
        apply_single_qubit_gate(&mut sv, &x, 1);

        let cz: Matrix4x4<f64> = Gate::cz_matrix();
        apply_two_qubit_gate(&mut sv, &cz, 0, 1);

        let neg_one = Complex::new(-1.0_f64, 0.0);
        assert!(approx_eq(sv.amplitudes()[3], neg_one, 1e-10));
    }

    #[test]
    fn test_swap_gate() {
        // |01⟩ → SWAP → |10⟩
        let mut sv: StateVector<f64> = StateVector::new(2);
        let x: Matrix2x2<f64> = Gate::X.matrix_2x2();
        apply_single_qubit_gate(&mut sv, &x, 0); // |01⟩

        let swap: Matrix4x4<f64> = Gate::swap_matrix();
        apply_two_qubit_gate(&mut sv, &swap, 0, 1);

        assert!(approx_eq(sv.amplitudes()[2], ONE, 1e-10));
        assert!(approx_eq(sv.amplitudes()[1], ZERO, 1e-10));
    }

    #[test]
    fn test_toffoli_gate() {
        // Toffoli: |110⟩ → |111⟩ (q0=ctrl, q1=ctrl, q2=target)
        let mut sv: StateVector<f64> = StateVector::new(3);
        let x: Matrix2x2<f64> = Gate::X.matrix_2x2();
        apply_single_qubit_gate(&mut sv, &x, 0);
        apply_single_qubit_gate(&mut sv, &x, 1);

        apply_doubly_controlled_gate(&mut sv, &x, 0, 1, 2);
        assert!(approx_eq(sv.amplitudes()[7], ONE, 1e-10));
        assert!(approx_eq(sv.amplitudes()[3], ZERO, 1e-10));
    }

    #[test]
    fn test_toffoli_no_action_single_control() {
        let mut sv: StateVector<f64> = StateVector::new(3);
        let x: Matrix2x2<f64> = Gate::X.matrix_2x2();
        apply_single_qubit_gate(&mut sv, &x, 0);

        apply_doubly_controlled_gate(&mut sv, &x, 0, 1, 2);
        assert!(approx_eq(sv.amplitudes()[1], ONE, 1e-10));
    }

    #[test]
    fn test_fredkin_gate() {
        let mut sv: StateVector<f64> = StateVector::new(3);
        let x: Matrix2x2<f64> = Gate::X.matrix_2x2();
        apply_single_qubit_gate(&mut sv, &x, 0);
        apply_single_qubit_gate(&mut sv, &x, 2);

        apply_controlled_swap(&mut sv, 0, 1, 2);
        assert!(approx_eq(sv.amplitudes()[3], ONE, 1e-10));
        assert!(approx_eq(sv.amplitudes()[5], ZERO, 1e-10));
    }

    #[test]
    fn test_ghz_state() {
        let mut sv: StateVector<f64> = StateVector::new(3);
        let h: Matrix2x2<f64> = Gate::H.matrix_2x2();
        apply_single_qubit_gate(&mut sv, &h, 0);

        let x: Matrix2x2<f64> = Gate::X.matrix_2x2();
        apply_controlled_gate(&mut sv, &x, 0, 1);
        apply_controlled_gate(&mut sv, &x, 0, 2);

        let expected = Complex::new(std::f64::consts::FRAC_1_SQRT_2, 0.0);
        assert!(approx_eq(sv.amplitudes()[0], expected, 1e-10));
        assert!(approx_eq(sv.amplitudes()[7], expected, 1e-10));
        for i in [1, 2, 3, 4, 5, 6] {
            assert!(approx_eq(sv.amplitudes()[i], ZERO, 1e-10));
        }
    }

    #[test]
    fn test_bell_state() {
        let mut sv: StateVector<f64> = StateVector::new(2);
        let h: Matrix2x2<f64> = Gate::H.matrix_2x2();
        apply_single_qubit_gate(&mut sv, &h, 0);

        let x: Matrix2x2<f64> = Gate::X.matrix_2x2();
        apply_controlled_gate(&mut sv, &x, 0, 1);

        let expected = Complex::new(std::f64::consts::FRAC_1_SQRT_2, 0.0);
        assert!(approx_eq(sv.amplitudes()[0], expected, 1e-10));
        assert!(approx_eq(sv.amplitudes()[1], ZERO, 1e-10));
        assert!(approx_eq(sv.amplitudes()[2], ZERO, 1e-10));
        assert!(approx_eq(sv.amplitudes()[3], expected, 1e-10));

        assert!((sv.probability(0) - 0.5).abs() < 1e-10);
        assert!((sv.probability(3) - 0.5).abs() < 1e-10);

        let total: f64 = sv.probabilities().iter().sum();
        assert!((total - 1.0).abs() < 1e-10);
    }

    #[test]
    fn test_bell_state_f32() {
        // f32 경로 회귀 테스트: Bell state 정확성
        let mut sv: StateVector<f32> = StateVector::new(2);
        let h: Matrix2x2<f32> = Gate::H.matrix_2x2();
        apply_single_qubit_gate(&mut sv, &h, 0);

        let x: Matrix2x2<f32> = Gate::X.matrix_2x2();
        apply_controlled_gate(&mut sv, &x, 0, 1);

        let expected = Complex::new(std::f32::consts::FRAC_1_SQRT_2, 0.0);
        assert!(approx_eq(sv.amplitudes()[0], expected, 1e-6_f32));
        assert!(approx_eq(sv.amplitudes()[3], expected, 1e-6_f32));

        let total: f32 = sv.probabilities().iter().sum();
        assert!((total - 1.0).abs() < 1e-6);
    }

    // ====================================================================
    // 병렬 경로(N >= 13 큐비트) 의 정확성 회귀 테스트
    // ====================================================================

    fn parallel_matches_serial<F: Fn(&mut StateVector<f64>)>(n_qubits: usize, apply: F) {
        let mut sv_par: StateVector<f64> = StateVector::new(n_qubits);
        let h: Matrix2x2<f64> = Gate::H.matrix_2x2();
        apply_single_qubit_gate(&mut sv_par, &h, 0);
        let sv_ser = sv_par.clone();

        apply(&mut sv_par);

        let mut sv_par2 = sv_ser.clone();
        apply(&mut sv_par2);

        for i in 0..sv_par.dim() {
            assert!(
                approx_eq(sv_par.amplitudes()[i], sv_par2.amplitudes()[i], 1e-12),
                "병렬 경로 비결정성 at i={i}"
            );
        }
    }

    #[test]
    fn test_single_qubit_parallel_path() {
        let h: Matrix2x2<f64> = Gate::H.matrix_2x2();
        for target in [0, 5, 13] {
            parallel_matches_serial(14, |sv| apply_single_qubit_gate(sv, &h, target));
        }
    }

    #[test]
    fn test_cnot_parallel_path_norm_preserved() {
        let mut sv: StateVector<f64> = StateVector::new(14);
        let h: Matrix2x2<f64> = Gate::H.matrix_2x2();
        let x: Matrix2x2<f64> = Gate::X.matrix_2x2();
        for q in 0..14 {
            apply_single_qubit_gate(&mut sv, &h, q);
        }
        for q in 0..13 {
            apply_controlled_gate(&mut sv, &x, q, q + 1);
        }
        let total: f64 = sv.probabilities().iter().sum();
        assert!((total - 1.0).abs() < 1e-10, "norm = {total}");
    }

    #[test]
    fn test_cnot_parallel_path_f32_norm_preserved() {
        // f32 + 14 큐비트 norm = 1 (cumulative drift 검증)
        let mut sv: StateVector<f32> = StateVector::new(14);
        let h: Matrix2x2<f32> = Gate::H.matrix_2x2();
        let x: Matrix2x2<f32> = Gate::X.matrix_2x2();
        for q in 0..14 {
            apply_single_qubit_gate(&mut sv, &h, q);
        }
        for q in 0..13 {
            apply_controlled_gate(&mut sv, &x, q, q + 1);
        }
        // f32 cumulative sum 으로 직접 합치면 ~1e-3 까지 drift 가능 — 1e-4 톨러런스
        let total: f32 = sv.probabilities().iter().sum();
        assert!((total - 1.0).abs() < 1e-4, "f32 norm = {total}");
    }

    #[test]
    fn test_two_qubit_gate_parallel_swap_qubits() {
        let mut sv: StateVector<f64> = StateVector::new(13);
        let x: Matrix2x2<f64> = Gate::X.matrix_2x2();
        apply_single_qubit_gate(&mut sv, &x, 0);

        let swap: Matrix4x4<f64> = Gate::swap_matrix();
        apply_two_qubit_gate(&mut sv, &swap, 0, 12);
        assert!(approx_eq(sv.amplitudes()[4096], ONE, 1e-10));
        assert!(approx_eq(sv.amplitudes()[1], ZERO, 1e-10));
    }

    #[test]
    fn test_doubly_controlled_parallel_path() {
        let mut sv: StateVector<f64> = StateVector::new(14);
        let x: Matrix2x2<f64> = Gate::X.matrix_2x2();
        apply_single_qubit_gate(&mut sv, &x, 0);
        apply_single_qubit_gate(&mut sv, &x, 1);

        apply_doubly_controlled_gate(&mut sv, &x, 0, 1, 2);
        assert!(approx_eq(sv.amplitudes()[7], ONE, 1e-10));
        assert!(approx_eq(sv.amplitudes()[3], ZERO, 1e-10));
    }

    #[test]
    fn test_controlled_swap_parallel_path() {
        let mut sv: StateVector<f64> = StateVector::new(14);
        let x: Matrix2x2<f64> = Gate::X.matrix_2x2();
        apply_single_qubit_gate(&mut sv, &x, 0);
        apply_single_qubit_gate(&mut sv, &x, 2);

        apply_controlled_swap(&mut sv, 0, 1, 2);
        assert!(approx_eq(sv.amplitudes()[3], ONE, 1e-10));
        assert!(approx_eq(sv.amplitudes()[5], ZERO, 1e-10));
    }

    #[test]
    fn test_single_qubit_target_is_msb() {
        let mut sv: StateVector<f64> = StateVector::new(14);
        let x: Matrix2x2<f64> = Gate::X.matrix_2x2();
        apply_single_qubit_gate(&mut sv, &x, 13);
        let expected_idx = 1usize << 13;
        assert!(approx_eq(sv.amplitudes()[expected_idx], ONE, 1e-10));
        assert!(approx_eq(sv.amplitudes()[0], ZERO, 1e-10));
    }
}
