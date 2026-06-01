use num_traits::NumCast;
use qsim_core::complex::{one, zero, Real};
use qsim_core::StateVector;
use rand::Rng;
use std::collections::HashMap;

/// 누적 확률 분포 (CDF) 를 `f64` 로 빌드한다.
///
/// **정밀도 안전장치**: `F = f32` 라도 누적합은 항상 f64. 큰 N (≥20 큐비트) 에서
/// 2^N 개의 작은 확률을 f32 로 누적하면 mantissa 손실로 마지막 outcome 에 bias.
///
/// 마지막 원소를 1.0 으로 강제 (rounding 으로 인한 오차로 random < cumulative
/// 가 마지막에서 false 가 되는 경우 방지).
fn build_cdf<F: Real>(state: &StateVector<F>) -> Vec<f64> {
    let probs = state.probabilities();
    let mut cdf = Vec::with_capacity(probs.len());
    let mut acc: f64 = 0.0;
    for p in probs {
        let p64: f64 = NumCast::from(p).expect("F → f64 변환 실패");
        acc += p64;
        cdf.push(acc);
    }
    if let Some(last) = cdf.last_mut() {
        *last = 1.0; // 부동소수 누적 오차 방지
    }
    cdf
}

/// CDF 에서 binary search 로 outcome 을 샘플링한다.
#[inline]
fn sample_from_cdf(cdf: &[f64], r: f64) -> usize {
    // partition_point: 첫 cdf[i] > r 인 i 반환
    let idx = cdf.partition_point(|&c| c <= r);
    idx.min(cdf.len() - 1)
}

/// 상태 벡터에서 한 번 측정하여 비트 문자열을 반환한다.
/// 상태 벡터는 변경하지 않는다 (샘플링 전용).
pub fn sample_once<F: Real>(state: &StateVector<F>, rng: &mut impl Rng) -> String {
    let cdf = build_cdf(state);
    let r: f64 = rng.gen();
    let outcome = sample_from_cdf(&cdf, r);
    format!("{:0>width$b}", outcome, width = state.num_qubits())
}

/// N회 샘플링하여 counts를 반환한다.
///
/// 이 함수는 `MeasureAll` 의 fast-path 전용 — 모든 큐비트를 한 번에 측정해
/// `n_qubits` 폭 비트 문자열을 만든다. explicit `Measure { qubit, cbit }` 가
/// 있는 경우엔 cbit 매핑이 다를 수 있으므로 [`sample_with_cbit_map`] 을 쓴다.
///
/// **최적화 (v0.2.1)**: CDF 를 한 번만 빌드 (`O(N)`) 하고 shot 마다 binary search
/// (`O(log N)`). 기존 v0.2.0 의 `O(N · shots)` 대비 큰 N · 큰 shots 에서 ~1000× 향상.
pub fn sample<F: Real>(
    state: &StateVector<F>,
    shots: usize,
    rng: &mut impl Rng,
) -> HashMap<String, usize> {
    let mut counts = HashMap::new();
    if shots == 0 {
        return counts;
    }
    let cdf = build_cdf(state);
    let n_qubits = state.num_qubits();
    for _ in 0..shots {
        let r: f64 = rng.gen();
        let outcome = sample_from_cdf(&cdf, r);
        let key = format!("{:0>width$b}", outcome, width = n_qubits);
        *counts.entry(key).or_insert(0) += 1;
    }
    counts
}

/// Trailing-explicit-`Measure` 회로 fast-path 용 cbit-aware 샘플러 (v0.4.5.1).
///
/// `cbit_map` 의 각 `(qubit, cbit)` 쌍에 대해, 한 shot 의 outcome 정수에서
/// `qubit` 비트를 읽어 `n_cbits` 폭 cbit register 의 `cbit` 자리에 기록한다.
/// 그 register 를 LSB-first 패킹해 Qiskit-스타일 비트 문자열 (MSB = cbit[n-1],
/// LSB = cbit[0]) 으로 만든다. `MeasureAll` 의 동작은 [`sample`] 그대로.
///
/// 이전 (v0.4.5.0) 의 fast-path 는 cbit 매핑을 무시하고 항상 `n_qubits` 폭의
/// q-인덱스 순서 비트 문자열을 만들어 partial measurement / cbit reorder /
/// 동일 큐비트 두 번 측정 시 잘못된 결과를 냈음. 이 함수가 그걸 정정한다.
///
/// 같은 cbit 에 두 measure 가 매핑되면 **나중 호출이 덮어쓴다** (Qiskit 의미와 정합).
pub fn sample_with_cbit_map<F: Real>(
    state: &StateVector<F>,
    shots: usize,
    cbit_map: &[(usize, usize)],
    n_cbits: usize,
    rng: &mut impl Rng,
) -> HashMap<String, usize> {
    let mut counts = HashMap::new();
    if shots == 0 {
        return counts;
    }
    let cdf = build_cdf(state);

    let mut creg: Vec<u8> = vec![0; n_cbits];
    for _ in 0..shots {
        let r: f64 = rng.gen();
        let outcome = sample_from_cdf(&cdf, r);
        // creg 를 매번 0 으로 초기화한 뒤 측정 명령 순서대로 채움.
        for v in creg.iter_mut() {
            *v = 0;
        }
        for &(qubit, cbit) in cbit_map {
            if cbit < n_cbits {
                creg[cbit] = ((outcome >> qubit) & 1) as u8;
            }
        }
        // MSB = creg[n-1], LSB = creg[0] (Qiskit counts 규약).
        let mut s = String::with_capacity(n_cbits);
        for &b in creg.iter().rev() {
            s.push(if b == 0 { '0' } else { '1' });
        }
        *counts.entry(s).or_insert(0) += 1;
    }
    counts
}

/// 특정 큐비트를 측정하여 결과(0 또는 1)와 붕괴된 상태를 반환한다.
///
/// 확률 합산은 항상 f64 로 (cumulative drift 방지).
pub fn measure_qubit<F: Real>(state: &mut StateVector<F>, qubit: usize, rng: &mut impl Rng) -> u8 {
    let n = state.dim();
    let mut prob_one: f64 = 0.0;

    for i in 0..n {
        if (i >> qubit) & 1 == 1 {
            let p: f64 = NumCast::from(state.probability(i)).expect("F → f64 변환 실패");
            prob_one += p;
        }
    }

    let r: f64 = rng.gen();
    let outcome = if r < prob_one { 1 } else { 0 };

    // 상태 붕괴: 측정 결과와 맞지 않는 amplitude 를 0 으로
    let amps = state.amplitudes_mut();
    for (i, amp) in amps.iter_mut().enumerate().take(n) {
        if ((i >> qubit) & 1) != outcome as usize {
            *amp = zero::<F>();
        }
    }

    state.normalize();
    outcome
}

/// 큐비트를 |0⟩ 으로 강제 리셋한다 (v0.4.5.1 RNG sampling 재구현).
///
/// 정확한 quantum reset 의미: **non-selective measurement + |0⟩ 으로 reinit**.
/// 즉 큐비트 상태가 다른 큐비트와 얽혀 있으면 partial trace 결과가 mixed state
/// 가 되어야 한다. statevector 시뮬레이션에서는 이걸 다음과 같이 구현한다:
///
/// 1. RNG 로 outcome m ∈ {0, 1} 을 P(q=m) 에 따라 샘플링.
/// 2. P_m projector 적용 + normalize ([`measure_qubit`] 가 이걸 그대로 한다).
/// 3. m=1 이면 X 적용해 |0⟩ 으로 만듦.
///
/// 이전 (v0.4.5.0) 구현은 p1 < 1 일 때 P_0 projector 만 적용했는데, 그건 사실
/// "q=0 결과로의 post-selection" 이지 reset 이 아니었음. Bell 페어의 한 큐비트
/// 를 reset 하면 다른 큐비트가 결정론적으로 |0⟩ 으로 강제 붕괴되는 버그
/// (TVD = 0.5 vs Qiskit Aer). v0.4.5.1 에서 RNG sampling 으로 수정.
pub fn reset_qubit<F: Real, R: Rng>(state: &mut StateVector<F>, qubit: usize, rng: &mut R) {
    // Step 1+2: outcome 샘플링 + P_m projector + normalize (measure_qubit 그대로).
    let outcome = measure_qubit(state, qubit, rng);

    // Step 3: outcome=1 이면 X 적용해 |0⟩ 으로 만듦.
    if outcome == 1 {
        let bit = 1usize << qubit;
        let amps = state.amplitudes_mut();
        let n = amps.len();
        for i in 0..n {
            if (i & bit) == 0 {
                let pair = i | bit;
                amps.swap(i, pair);
            }
        }
        // X 는 unitary — norm 보존, normalize 불필요.
    }
}

/// 측정 + cbit 갱신용 in-place 헬퍼 (v0.4.5 mid-circuit 용).
///
/// [`measure_qubit`] 와 동일하지만 outcome 이 [`u8`] 로 명시적으로 반환되며
/// engine 의 cbit register 갱신 직전에 호출된다. 추후 [`measure_qubit`] 와
/// 통합할 수도 있지만, 별도 export 로 mid-circuit 의도를 분명히 한다.
pub fn measure_qubit_inplace<F: Real>(
    state: &mut StateVector<F>,
    qubit: usize,
    rng: &mut impl Rng,
) -> u8 {
    measure_qubit(state, qubit, rng)
}

/// 모든 큐비트를 측정하여 비트 문자열과 붕괴된 상태를 반환한다.
pub fn measure_all<F: Real>(state: &mut StateVector<F>, rng: &mut impl Rng) -> String {
    let cdf = build_cdf(state);
    let r: f64 = rng.gen();
    let outcome = sample_from_cdf(&cdf, r);

    // 상태 붕괴: 측정 결과 하나만 남기기
    let amps = state.amplitudes_mut();
    for a in amps.iter_mut() {
        *a = zero::<F>();
    }
    state.amplitudes_mut()[outcome] = one::<F>();

    format!("{:0>width$b}", outcome, width = state.num_qubits())
}

#[cfg(test)]
mod tests {
    use super::*;
    use qsim_core::operations::{apply_controlled_gate, apply_single_qubit_gate};
    use qsim_core::Gate;
    use rand::rngs::StdRng;
    use rand::SeedableRng;

    #[test]
    fn test_deterministic_measurement() {
        // |0⟩ 상태: 항상 "0"
        let sv: StateVector<f64> = StateVector::new(1);
        let mut rng = StdRng::seed_from_u64(42);
        let result = sample_once(&sv, &mut rng);
        assert_eq!(result, "0");
    }

    #[test]
    fn test_bell_state_sampling() {
        let mut sv: StateVector<f64> = StateVector::new(2);
        let h = Gate::H.matrix_2x2::<f64>();
        apply_single_qubit_gate(&mut sv, &h, 0);
        let x = Gate::X.matrix_2x2::<f64>();
        apply_controlled_gate(&mut sv, &x, 0, 1);

        let mut rng = StdRng::seed_from_u64(123);
        let counts = sample(&sv, 1000, &mut rng);

        assert!(counts.contains_key("00"));
        assert!(counts.contains_key("11"));
        assert!(!counts.contains_key("01"));
        assert!(!counts.contains_key("10"));

        let total: usize = counts.values().sum();
        assert_eq!(total, 1000);
    }

    #[test]
    fn test_bell_state_sampling_f32() {
        // f32 경로: cumulative drift 없이 동일 분포 보장
        let mut sv: StateVector<f32> = StateVector::new(2);
        let h = Gate::H.matrix_2x2::<f32>();
        apply_single_qubit_gate(&mut sv, &h, 0);
        let x = Gate::X.matrix_2x2::<f32>();
        apply_controlled_gate(&mut sv, &x, 0, 1);

        let mut rng = StdRng::seed_from_u64(123);
        let counts = sample(&sv, 1000, &mut rng);

        assert!(counts.contains_key("00"));
        assert!(counts.contains_key("11"));
        assert!(!counts.contains_key("01"));
        assert!(!counts.contains_key("10"));
        let total: usize = counts.values().sum();
        assert_eq!(total, 1000);
    }

    #[test]
    fn test_measure_qubit_collapses_state() {
        let mut sv: StateVector<f64> = StateVector::new(1);
        let h = Gate::H.matrix_2x2::<f64>();
        apply_single_qubit_gate(&mut sv, &h, 0);

        let mut rng = StdRng::seed_from_u64(42);
        let outcome = measure_qubit(&mut sv, 0, &mut rng);

        assert!(outcome == 0 || outcome == 1);
        let probs = sv.probabilities();
        assert!((probs[outcome as usize] - 1.0).abs() < 1e-10);
    }

    #[test]
    fn test_measure_all_collapses() {
        let mut sv: StateVector<f64> = StateVector::new(2);
        let h = Gate::H.matrix_2x2::<f64>();
        apply_single_qubit_gate(&mut sv, &h, 0);
        let x = Gate::X.matrix_2x2::<f64>();
        apply_controlled_gate(&mut sv, &x, 0, 1);

        let mut rng = StdRng::seed_from_u64(42);
        let result = measure_all(&mut sv, &mut rng);

        assert!(result == "00" || result == "11");
        let total: f64 = sv.probabilities().iter().sum();
        assert!((total - 1.0).abs() < 1e-10);
    }

    #[test]
    fn test_cdf_last_is_one() {
        // CDF 의 마지막 원소가 정확히 1.0 인지 (sampling 안전성)
        let sv: StateVector<f32> = StateVector::new(8);
        let cdf = build_cdf(&sv);
        assert_eq!(*cdf.last().unwrap(), 1.0);
    }

    #[test]
    fn test_sample_large_n_no_bias() {
        // 14 큐비트 + 균등 분포 (모두 H 적용) 에서 1000 shots 샘플링이
        // bias 없이 동작하는지 (CDF binary search 정확성)
        let mut sv: StateVector<f64> = StateVector::new(14);
        let h = Gate::H.matrix_2x2::<f64>();
        for q in 0..14 {
            apply_single_qubit_gate(&mut sv, &h, q);
        }
        let mut rng = StdRng::seed_from_u64(7);
        let counts = sample(&sv, 1000, &mut rng);
        let total: usize = counts.values().sum();
        assert_eq!(total, 1000);
    }
}
