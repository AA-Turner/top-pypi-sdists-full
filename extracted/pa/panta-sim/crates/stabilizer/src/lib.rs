//! Stabilizer (Clifford) 시뮬레이터 — Aaronson–Gottesman CHP tableau.
//!
//! Clifford 회로 (H / S / CNOT 로 생성되는 군) 는 stabilizer formalism 으로
//! **다항시간·다항메모리** 시뮬레이션이 가능하다 (Gottesman–Knill 정리).  전체
//! statevector (2ⁿ amplitude) 대신 `2n × (2n+1)` 이진 tableau 만 추적하므로
//! **수천~수만 큐비트** Clifford 회로를 정확히 시뮬레이션할 수 있다.  이것이
//! "수천 큐비트" 시뮬레이터(Quantum Rings 등)가 큰 큐비트 수를 다루는 핵심
//! 방법 중 하나다 (단, 임의 비-Clifford 게이트(T 등)가 많으면 적용 불가).
//!
//! 구현은 Aaronson & Gottesman, *"Improved Simulation of Stabilizer Circuits"*
//! (Phys. Rev. A 70, 052328, 2004) 의 CHP 알고리즘을 따른다:
//! - tableau 의 앞 `n` 행 = **destabilizer**, 뒤 `n` 행 = **stabilizer**,
//!   마지막 1 행 = 측정용 scratch.  각 행은 Pauli 연산자 (x/z 비트 + 부호 r).
//! - 게이트 (H/S/CNOT) 는 tableau 행을 O(n) 업데이트, 측정은 O(n²).
//! - x/z 비트는 `u64` 워드로 패킹 (메모리 효율 + XOR 벡터화).
//!
//! 부호 r 은 `{0,1}` 로 저장하며 phase = `(-1)^r`.  rowsum 의 i-거듭제곱은
//! 논문의 `g` 함수로 계산한다.

use rand::Rng;

pub mod ch_form;
pub mod clifford_t;

/// 지원하지 않는 (비-Clifford) 연산을 만났을 때의 에러.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct NonCliffordError(pub String);

impl std::fmt::Display for NonCliffordError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(
            f,
            "stabilizer 백엔드는 Clifford 회로만 지원합니다: {}",
            self.0
        )
    }
}

impl std::error::Error for NonCliffordError {}

/// Aaronson–Gottesman stabilizer tableau.
///
/// `n` 큐비트에 대해 `2n+1` 개의 Pauli 행 (destabilizer n + stabilizer n +
/// scratch 1) 을 비트패킹으로 보관한다.  `x[row]` / `z[row]` 는 각각 `words`
/// 개의 `u64`, `r[row]` 는 부호 비트.
#[derive(Clone)]
pub struct Tableau {
    n: usize,
    words: usize,
    /// x 비트: `(2n+1) * words` 개의 u64.
    x: Vec<u64>,
    /// z 비트: `(2n+1) * words` 개의 u64.
    z: Vec<u64>,
    /// 부호 비트 r ∈ {0,1}: `2n+1` 개.
    r: Vec<u8>,
}

#[inline]
fn word_bit(q: usize) -> (usize, u64) {
    (q / 64, 1u64 << (q % 64))
}

impl Tableau {
    /// `n` 큐비트의 계산기저 |0…0⟩ 로 초기화한다.
    ///
    /// destabilizer i = X_i, stabilizer i = Z_i, 모든 부호 +.
    pub fn new(n: usize) -> Self {
        let words = n.div_ceil(64).max(1);
        let rows = 2 * n + 1;
        let mut t = Tableau {
            n,
            words,
            x: vec![0u64; rows * words],
            z: vec![0u64; rows * words],
            r: vec![0u8; rows],
        };
        for i in 0..n {
            // destabilizer 행 i = X_i
            t.set_x(i, i, true);
            // stabilizer 행 n+i = Z_i
            t.set_z(n + i, i, true);
        }
        t
    }

    /// 큐비트 수.
    pub fn num_qubits(&self) -> usize {
        self.n
    }

    #[inline]
    fn get_x(&self, row: usize, q: usize) -> bool {
        let (w, b) = word_bit(q);
        self.x[row * self.words + w] & b != 0
    }
    #[inline]
    fn get_z(&self, row: usize, q: usize) -> bool {
        let (w, b) = word_bit(q);
        self.z[row * self.words + w] & b != 0
    }
    #[inline]
    fn set_x(&mut self, row: usize, q: usize, v: bool) {
        let (w, b) = word_bit(q);
        let idx = row * self.words + w;
        if v {
            self.x[idx] |= b;
        } else {
            self.x[idx] &= !b;
        }
    }
    #[inline]
    fn set_z(&mut self, row: usize, q: usize, v: bool) {
        let (w, b) = word_bit(q);
        let idx = row * self.words + w;
        if v {
            self.z[idx] |= b;
        } else {
            self.z[idx] &= !b;
        }
    }

    fn rows(&self) -> usize {
        2 * self.n
    }

    // ---- clifford_t 모듈용 generator 접근자 (pub(crate)) ----

    /// stabilizer 생성자 `i` (행 `n+i`) 의 큐비트 `q` x-비트.
    pub(crate) fn stab_x(&self, i: usize, q: usize) -> bool {
        self.get_x(self.n + i, q)
    }
    /// stabilizer 생성자 `i` 의 큐비트 `q` z-비트.
    pub(crate) fn stab_z(&self, i: usize, q: usize) -> bool {
        self.get_z(self.n + i, q)
    }
    /// stabilizer 생성자 `i` 의 부호 비트 r ∈ {0,1} (phase = (-1)^r).
    pub(crate) fn stab_r(&self, i: usize) -> u8 {
        self.r[self.n + i]
    }

    // ---- primitive Clifford 게이트 (CHP §II) ----

    /// Hadamard.
    pub fn h(&mut self, a: usize) {
        let words = self.words;
        let (wa, ba) = word_bit(a);
        for i in 0..self.rows() {
            let xi = self.x[i * words + wa] & ba != 0;
            let zi = self.z[i * words + wa] & ba != 0;
            self.r[i] ^= (xi & zi) as u8;
            // swap x_ia, z_ia
            if xi != zi {
                self.x[i * words + wa] ^= ba;
                self.z[i * words + wa] ^= ba;
            }
        }
    }

    /// Phase S = diag(1, i).
    pub fn s(&mut self, a: usize) {
        let words = self.words;
        let (wa, ba) = word_bit(a);
        for i in 0..self.rows() {
            let xi = self.x[i * words + wa] & ba != 0;
            let zi = self.z[i * words + wa] & ba != 0;
            self.r[i] ^= (xi & zi) as u8;
            if xi {
                self.z[i * words + wa] ^= ba;
            }
        }
    }

    /// S† = S³.
    pub fn sdg(&mut self, a: usize) {
        self.s(a);
        self.s(a);
        self.s(a);
    }

    /// CNOT (control a, target b).
    pub fn cnot(&mut self, a: usize, b: usize) {
        let words = self.words;
        let (wa, ba) = word_bit(a);
        let (wb, bb) = word_bit(b);
        for i in 0..self.rows() {
            let xa = self.x[i * words + wa] & ba != 0;
            let za = self.z[i * words + wa] & ba != 0;
            let xb = self.x[i * words + wb] & bb != 0;
            let zb = self.z[i * words + wb] & bb != 0;
            self.r[i] ^= (xa & zb & (xb ^ za ^ true)) as u8;
            if xa {
                self.x[i * words + wb] ^= bb;
            }
            if zb {
                self.z[i * words + wa] ^= ba;
            }
        }
    }

    /// Pauli X (= H S² H) — 부호만 갱신.
    pub fn x_gate(&mut self, a: usize) {
        for i in 0..self.rows() {
            self.r[i] ^= self.get_z(i, a) as u8;
        }
    }
    /// Pauli Z.
    pub fn z_gate(&mut self, a: usize) {
        for i in 0..self.rows() {
            self.r[i] ^= self.get_x(i, a) as u8;
        }
    }
    /// Pauli Y.
    pub fn y_gate(&mut self, a: usize) {
        for i in 0..self.rows() {
            self.r[i] ^= (self.get_x(i, a) ^ self.get_z(i, a)) as u8;
        }
    }

    /// √X = H S H.
    pub fn sx(&mut self, a: usize) {
        self.h(a);
        self.s(a);
        self.h(a);
    }
    /// √X† = H S† H.
    pub fn sxdg(&mut self, a: usize) {
        self.h(a);
        self.sdg(a);
        self.h(a);
    }

    /// CZ = H_b · CNOT_ab · H_b.
    pub fn cz(&mut self, a: usize, b: usize) {
        self.h(b);
        self.cnot(a, b);
        self.h(b);
    }

    /// Controlled-Y = S_b · CNOT_ab · S†_b.
    pub fn cy(&mut self, a: usize, b: usize) {
        self.sdg(b);
        self.cnot(a, b);
        self.s(b);
    }

    /// SWAP = 3 CNOT.
    pub fn swap(&mut self, a: usize, b: usize) {
        self.cnot(a, b);
        self.cnot(b, a);
        self.cnot(a, b);
    }

    /// DCX = CNOT_ab · CNOT_ba.
    pub fn dcx(&mut self, a: usize, b: usize) {
        self.cnot(a, b);
        self.cnot(b, a);
    }

    /// iSWAP = |01⟩↔|10⟩ + i.  Clifford 분해: S_a S_b H_a CNOT_ab CNOT_ba H_b.
    pub fn iswap(&mut self, a: usize, b: usize) {
        self.s(a);
        self.s(b);
        self.h(a);
        self.cnot(a, b);
        self.cnot(b, a);
        self.h(b);
    }

    // ---- 측정 (CHP §II measurement) ----

    /// `g` 함수 — Pauli (x1,z1)·(x2,z2) 곱의 i-거듭제곱 (∈ {-1,0,1}).
    #[inline]
    fn g(x1: bool, z1: bool, x2: bool, z2: bool) -> i32 {
        match (x1, z1) {
            (false, false) => 0,
            (true, true) => (z2 as i32) - (x2 as i32),
            (true, false) => (z2 as i32) * (2 * (x2 as i32) - 1),
            (false, true) => (x2 as i32) * (1 - 2 * (z2 as i32)),
        }
    }

    /// rowsum: 행 h ← 행 i · 행 h (Pauli 곱, 부호 포함).
    fn rowsum(&mut self, h: usize, i: usize) {
        let words = self.words;
        let mut acc: i32 = 2 * self.r[h] as i32 + 2 * self.r[i] as i32;
        for q in 0..self.n {
            let (w, b) = word_bit(q);
            let xi = self.x[i * words + w] & b != 0;
            let zi = self.z[i * words + w] & b != 0;
            let xh = self.x[h * words + w] & b != 0;
            let zh = self.z[h * words + w] & b != 0;
            acc += Self::g(xi, zi, xh, zh);
        }
        let m = acc.rem_euclid(4);
        self.r[h] = if m == 0 { 0 } else { 1 };
        // XOR 비트 갱신 (워드 단위 벡터화)
        for w in 0..words {
            self.x[h * words + w] ^= self.x[i * words + w];
            self.z[h * words + w] ^= self.z[i * words + w];
        }
    }

    fn copy_row(&mut self, dst: usize, src: usize) {
        let words = self.words;
        for w in 0..words {
            self.x[dst * words + w] = self.x[src * words + w];
            self.z[dst * words + w] = self.z[src * words + w];
        }
        self.r[dst] = self.r[src];
    }

    fn zero_row(&mut self, row: usize) {
        let words = self.words;
        for w in 0..words {
            self.x[row * words + w] = 0;
            self.z[row * words + w] = 0;
        }
        self.r[row] = 0;
    }

    /// 큐비트 `a` 를 계산기저로 측정하고 결과 비트 (0/1) 를 반환한다.
    ///
    /// 결과에 따라 tableau 가 collapse 된다 (random 결과는 `rng` 로 샘플링).
    pub fn measure<R: Rng>(&mut self, a: usize, rng: &mut R) -> u8 {
        let n = self.n;
        // stabilizer 행 (n..2n) 중 x_pa==1 인 p 탐색 → random outcome.
        let mut p = None;
        for row in n..2 * n {
            if self.get_x(row, a) {
                p = Some(row);
                break;
            }
        }
        if let Some(p) = p {
            // random 결과
            for i in 0..2 * n {
                if i != p && self.get_x(i, a) {
                    self.rowsum(i, p);
                }
            }
            self.copy_row(p - n, p); // destabilizer ← 옛 stabilizer
            self.zero_row(p);
            self.set_z(p, a, true);
            let outcome = rng.gen::<bool>() as u8;
            self.r[p] = outcome;
            outcome
        } else {
            // deterministic 결과: scratch 행 (2n) 으로 계산.
            self.zero_row(2 * n);
            for i in 0..n {
                if self.get_x(i, a) {
                    self.rowsum(2 * n, i + n);
                }
            }
            self.r[2 * n]
        }
    }
}

/// 단일 / 2-큐비트 Clifford 연산 — 회로 변환의 중간 표현.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum CliffordOp {
    H(usize),
    S(usize),
    Sdg(usize),
    X(usize),
    Y(usize),
    Z(usize),
    Sx(usize),
    Sxdg(usize),
    Cnot(usize, usize),
    Cz(usize, usize),
    Cy(usize, usize),
    Swap(usize, usize),
    Iswap(usize, usize),
    Dcx(usize, usize),
}

impl Tableau {
    /// [`CliffordOp`] 하나를 적용한다.
    pub fn apply(&mut self, op: CliffordOp) {
        match op {
            CliffordOp::H(a) => self.h(a),
            CliffordOp::S(a) => self.s(a),
            CliffordOp::Sdg(a) => self.sdg(a),
            CliffordOp::X(a) => self.x_gate(a),
            CliffordOp::Y(a) => self.y_gate(a),
            CliffordOp::Z(a) => self.z_gate(a),
            CliffordOp::Sx(a) => self.sx(a),
            CliffordOp::Sxdg(a) => self.sxdg(a),
            CliffordOp::Cnot(a, b) => self.cnot(a, b),
            CliffordOp::Cz(a, b) => self.cz(a, b),
            CliffordOp::Cy(a, b) => self.cy(a, b),
            CliffordOp::Swap(a, b) => self.swap(a, b),
            CliffordOp::Iswap(a, b) => self.iswap(a, b),
            CliffordOp::Dcx(a, b) => self.dcx(a, b),
        }
    }
}

impl CliffordOp {
    /// 이 연산이 작용하는 큐비트들.
    pub fn qubits(&self) -> Vec<usize> {
        match *self {
            CliffordOp::H(a)
            | CliffordOp::S(a)
            | CliffordOp::Sdg(a)
            | CliffordOp::X(a)
            | CliffordOp::Y(a)
            | CliffordOp::Z(a)
            | CliffordOp::Sx(a)
            | CliffordOp::Sxdg(a) => vec![a],
            CliffordOp::Cnot(a, b)
            | CliffordOp::Cz(a, b)
            | CliffordOp::Cy(a, b)
            | CliffordOp::Swap(a, b)
            | CliffordOp::Iswap(a, b)
            | CliffordOp::Dcx(a, b) => vec![a, b],
        }
    }
}

/// Clifford 회로를 `shots` 회 샘플링해 측정 카운트를 반환한다.
///
/// 게이트를 한 번 적용해 stabilizer 상태를 만든 뒤, 각 shot 마다 tableau 를
/// 복제해 모든 큐비트를 순서대로 측정한다.  반환 비트열은 `outcomes[shot][q]`
/// (q=0 이 LSB) 형식이다.
pub fn sample_counts(
    n: usize,
    ops: &[CliffordOp],
    shots: usize,
    seed: Option<u64>,
) -> Vec<Vec<u8>> {
    use rand::rngs::StdRng;
    use rand::SeedableRng;

    let mut base = Tableau::new(n);
    for &op in ops {
        base.apply(op);
    }
    let mut rng = match seed {
        Some(s) => StdRng::seed_from_u64(s),
        None => StdRng::from_entropy(),
    };
    let mut out = Vec::with_capacity(shots);
    for _ in 0..shots {
        let mut t = base.clone();
        let mut bits = vec![0u8; n];
        for (q, bit) in bits.iter_mut().enumerate() {
            *bit = t.measure(q, &mut rng);
        }
        out.push(bits);
    }
    out
}

/// **Depolarizing 노이즈** trajectory 로 Clifford 회로를 샘플링한다.
///
/// 각 shot 마다 새 tableau 에 게이트를 적용하고, 각 게이트 직후 그 게이트가
/// 닿는 큐비트마다 depolarizing(p) — `I` w.p. `1-3p/4`, `X/Y/Z` 각 `p/4` — 를
/// 무작위 적용한다 (Pauli 에러는 Clifford → stabilizer formalism 유지).
/// 수천 큐비트 노이즈 Clifford 회로 (QEC 코드 등) 를 다항시간에 시뮬레이션.
/// `p = 0` 이면 [`sample_counts`] 와 동치.
pub fn sample_counts_depolarizing(
    n: usize,
    ops: &[CliffordOp],
    shots: usize,
    seed: Option<u64>,
    p: f64,
) -> Vec<Vec<u8>> {
    use rand::rngs::StdRng;
    use rand::SeedableRng;
    if p <= 0.0 {
        return sample_counts(n, ops, shots, seed);
    }
    let mut rng = match seed {
        Some(s) => StdRng::seed_from_u64(s),
        None => StdRng::from_entropy(),
    };
    let mut out = Vec::with_capacity(shots);
    for _ in 0..shots {
        let mut t = Tableau::new(n);
        for &op in ops {
            t.apply(op);
            for q in op.qubits() {
                // I: 1-3p/4, X: p/4, Y: p/4, Z: p/4.
                let r: f64 = rng.gen();
                if r < p / 4.0 {
                    t.x_gate(q);
                } else if r < p / 2.0 {
                    t.y_gate(q);
                } else if r < 3.0 * p / 4.0 {
                    t.z_gate(q);
                }
            }
        }
        let bits: Vec<u8> = (0..n).map(|q| t.measure(q, &mut rng)).collect();
        out.push(bits);
    }
    out
}

#[cfg(test)]
mod tests {
    use super::*;
    use rand::rngs::StdRng;
    use rand::SeedableRng;

    #[test]
    fn plus_state_is_random() {
        // H|0> → 측정 50/50.
        let mut rng = StdRng::seed_from_u64(7);
        let mut ones = 0;
        for _ in 0..2000 {
            let mut t = Tableau::new(1);
            t.h(0);
            ones += t.measure(0, &mut rng) as usize;
        }
        assert!((800..1200).contains(&ones), "ones={ones}");
    }

    #[test]
    fn bell_is_correlated() {
        // (H 0; CNOT 0,1) → 00 / 11 만, 동일 비트.
        let mut rng = StdRng::seed_from_u64(1);
        for _ in 0..500 {
            let mut t = Tableau::new(2);
            t.h(0);
            t.cnot(0, 1);
            let a = t.measure(0, &mut rng);
            let b = t.measure(1, &mut rng);
            assert_eq!(a, b);
        }
    }

    #[test]
    fn x_gate_flips() {
        let mut rng = StdRng::seed_from_u64(2);
        let mut t = Tableau::new(1);
        t.x_gate(0);
        assert_eq!(t.measure(0, &mut rng), 1);
    }

    #[test]
    fn ghz_thousand_qubits() {
        // 1000-큐비트 GHZ: 전부 동일 비트 (0…0 또는 1…1).
        let n = 1000;
        let mut ops = vec![CliffordOp::H(0)];
        for q in 0..n - 1 {
            ops.push(CliffordOp::Cnot(q, q + 1));
        }
        let samples = sample_counts(n, &ops, 20, Some(42));
        for s in &samples {
            let first = s[0];
            assert!(s.iter().all(|&b| b == first));
        }
    }

    #[test]
    fn z_basis_deterministic() {
        // |0> 측정은 항상 0 (deterministic).
        let mut rng = StdRng::seed_from_u64(3);
        let mut t = Tableau::new(3);
        for q in 0..3 {
            assert_eq!(t.measure(q, &mut rng), 0);
        }
    }
}
