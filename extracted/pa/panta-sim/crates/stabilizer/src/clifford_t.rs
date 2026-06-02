//! near-Clifford (Clifford+T) 시뮬레이션 — phase-aware stabilizer amplitude.
//!
//! Clifford 회로는 stabilizer formalism 으로 다항시간이지만 (`crate::Tableau`),
//! T 게이트 (비-Clifford) 가 섞이면 안 된다.  본 모듈은 T 게이트를 **stabilizer
//! 항들의 간섭 합** 으로 분해해 (각 T 가 항 수를 2배), 큰 N · 적은 T-count 의
//! Clifford+T 회로 amplitude `⟨x|C|0…0⟩` 를 정확히 계산한다:
//!
//!   `T|ψ⟩ = e^{iπ/8}(cos(π/8)|ψ⟩ − i sin(π/8) Z|ψ⟩)`  (Z 는 Clifford)
//!
//! → t 개의 T 후 ≤ 2ᵗ 개의 (계수, stabilizer 상태) 항.  최종
//! `⟨x|ψ⟩ = Σ_k c_k ⟨x|φ_k⟩`.  각 stabilizer 상태의 basis amplitude `⟨x|φ_k⟩`
//! 는 **전역 위상까지** 정확해야 항들의 간섭이 맞다 (AG tableau 는 전역 위상을
//! 추적하지 않으므로, canonical Gauss-sum amplitude + 게이트별 전역 위상 ratio
//! 추적으로 보완한다).
//!
//! 핵심 수치 도구는 **F₂→ℤ₄ quadratic Gauss sum** 의 다항시간 (O(k³)) 계산이다
//! ([`gauss_sum`]).

use num_complex::Complex64;

use crate::Tableau;

/// F₂→ℤ₄ quadratic Gauss sum:
/// `Σ_{y∈{0,1}^m} i^{Q(y)}`,  `Q(y) = Σ_i lin_i y_i + 2 Σ_{i<j} coup_{ij} y_i y_j (mod 4)`.
///
/// `lin[i] ∈ {0,1,2,3}`, `coup[i][j] = coup[j][i] ∈ {0,1}` (대각 0).  변수 하나씩
/// 소거하는 O(m³) 알고리즘 — 선형항이 홀수면 √2·e^{±iπ/4} 인자로 fold,
/// 짝수면 hard constraint 로 pivot 변수를 치환한다 (ℤ₄ 위 XOR = Σ − 2Σpairs).
pub fn gauss_sum(lin: &[u8], coup: &[Vec<u8>]) -> Complex64 {
    let m = lin.len();
    if m == 0 {
        return Complex64::new(1.0, 0.0);
    }
    let l0 = lin[0] & 3;
    // var0 의 다른 변수와의 결합 d_j = coup[0][j].
    let d: Vec<u8> = (1..m).map(|j| coup[0][j] & 1).collect();

    if l0 & 1 == 1 {
        // 홀수: 1 + i^{l0}(-1)^{d·y'} = √2 · e^{±iπ/4} · i^{∓(d·y' mod 2)}.
        // 주의: (d·y' mod 2) = Σ d_j y_j − 2 Σ_{j<j'} d_j d_{j'} y_j y_{j'} (XOR 의 ℤ₄ lift).
        // → 선형 lin_j ∓= d_j 뿐 아니라 **2차항 coup_{jj'} ^= d_j·d_{j'}** 보정 필요.
        // l0=1 → e^{+iπ/4}, 지수 −(parity) ;  l0=3 → e^{-iπ/4}, 지수 +(parity).
        let mut lin_new = vec![0u8; m - 1];
        for j in 1..m {
            let shift = if l0 == 1 {
                (4 - d[j - 1]) & 3 // -d_j
            } else {
                d[j - 1] // +d_j
            };
            lin_new[j - 1] = (lin[j] + shift) & 3;
        }
        let mut coup_new = sub_coup(coup, &(1..m).collect::<Vec<_>>());
        // 2차 보정: 남는 두 변수 a<b 모두 d=1 이면 coup ^= 1 (부호는 mod 2 라 무관).
        for a in 0..(m - 1) {
            if d[a] == 0 {
                continue;
            }
            for b in (a + 1)..(m - 1) {
                if d[b] == 1 {
                    coup_new[a][b] ^= 1;
                    coup_new[b][a] = coup_new[a][b];
                }
            }
        }
        let sign = if l0 == 1 { 1.0 } else { -1.0 };
        let factor = Complex64::new(2.0_f64.sqrt(), 0.0)
            * Complex64::from_polar(1.0, sign * std::f64::consts::FRAC_PI_4);
        return factor * gauss_sum(&lin_new, &coup_new);
    }

    // 짝수: i^{l0} = +1 (l0=0) 또는 -1 (l0=2).  제약 d·y' = c.
    let c: u8 = if l0 == 0 { 0 } else { 1 };
    let pivot = (1..m).find(|&j| d[j - 1] == 1);
    match pivot {
        None => {
            // d == 0: 제약은 0 = c.
            if c == 0 {
                let rest: Vec<usize> = (1..m).collect();
                let lin_new: Vec<u8> = rest.iter().map(|&j| lin[j]).collect();
                let coup_new = sub_coup(coup, &rest);
                Complex64::new(2.0, 0.0) * gauss_sum(&lin_new, &coup_new)
            } else {
                Complex64::new(0.0, 0.0)
            }
        }
        Some(t) => {
            // y_t = c ⊕ (⊕_{j∈J} y_j),  J = {j∈1..m : j≠t, d_j=1}.
            let jset: Vec<usize> = (1..m).filter(|&j| j != t && d[j - 1] == 1).collect();
            // 남는 변수 = (1..m) \ {t}.
            let remaining: Vec<usize> = (1..m).filter(|&j| j != t).collect();
            let r = remaining.len();
            let pos: std::collections::HashMap<usize, usize> =
                remaining.iter().enumerate().map(|(i, &v)| (v, i)).collect();

            // 기본: (lin,coup) 를 remaining 으로 제한.
            let mut lin_new: Vec<u8> = remaining.iter().map(|&j| lin[j]).collect();
            let mut coup_new = sub_coup(coup, &remaining);

            let mut k_const: u8 = 0;
            let lt = lin[t] & 3;
            // (A) lin[t]·y_t.
            k_const = (k_const + lt.wrapping_mul(c)) & 3;
            let coef_lin_j = (lt.wrapping_mul((1 + 4 - 2 * c) & 3)) & 3; // lt*(1-2c) mod4
            for &j in &jset {
                let p = pos[&j];
                lin_new[p] = (lin_new[p] + coef_lin_j) & 3;
            }
            // -2·lt·y_j y_{j'}  (j<j' in J): 2·coup 항에 -2·lt 추가
            // → coup += (-lt) mod 2 == lt mod 2.
            let pair_bit = lt & 1;
            for a in 0..jset.len() {
                for b in (a + 1)..jset.len() {
                    let (pa, pb) = (pos[&jset[a]], pos[&jset[b]]);
                    coup_new[pa][pb] = (coup_new[pa][pb] + pair_bit) & 1;
                    coup_new[pb][pa] = coup_new[pa][pb];
                }
            }
            // (B) 2·coup[t][l]·y_t y_l  for l in remaining.
            for &l in &remaining {
                let e = coup[t][l] & 1;
                if e == 0 {
                    continue;
                }
                let pl = pos[&l];
                // 2 e c y_l
                lin_new[pl] = (lin_new[pl] + (2 * e * c)) & 3;
                // 2 e Σ_{j∈J} y_j y_l
                for &j in &jset {
                    if j == l {
                        lin_new[pl] = (lin_new[pl] + 2 * e) & 3;
                    } else {
                        let pj = pos[&j];
                        coup_new[pj][pl] = (coup_new[pj][pl] + e) & 1;
                        coup_new[pl][pj] = coup_new[pj][pl];
                    }
                }
            }
            let _ = r;
            let phase = Complex64::from_polar(1.0, (k_const as f64) * std::f64::consts::FRAC_PI_2);
            Complex64::new(2.0, 0.0) * phase * gauss_sum(&lin_new, &coup_new)
        }
    }
}

/// `coup` 의 부분행렬 (인덱스 `idx` 의 행/열만).
fn sub_coup(coup: &[Vec<u8>], idx: &[usize]) -> Vec<Vec<u8>> {
    idx.iter()
        .map(|&i| idx.iter().map(|&j| coup[i][j]).collect())
        .collect()
}

// ===================== canonical stabilizer amplitude =====================

/// stabilizer 생성자를 `(x, z, phase∈ℤ₄)` 명시 convention 으로 추출한다.
/// 연산자 = `i^{phase} ∏_q X^{x_q} Z^{z_q}`.  AG 행은 `(-1)^r ⊗ Q (Q∈{I,X,Y,Z})`
/// 이고 `Y = i·XZ` 이므로 `phase = (2r + #Y) mod 4`.
fn extract_generators(tab: &Tableau) -> (Vec<Vec<bool>>, Vec<Vec<bool>>, Vec<u8>) {
    let n = tab.num_qubits();
    let mut xg = vec![vec![false; n]; n];
    let mut zg = vec![vec![false; n]; n];
    let mut pg = vec![0u8; n];
    for i in 0..n {
        let mut n_y = 0u32;
        for q in 0..n {
            let xb = tab.stab_x(i, q);
            let zb = tab.stab_z(i, q);
            xg[i][q] = xb;
            zg[i][q] = zb;
            if xb && zb {
                n_y += 1;
            }
        }
        pg[i] = ((2 * tab.stab_r(i) as u32 + n_y) % 4) as u8;
    }
    (xg, zg, pg)
}

/// support 내 기저상태 하나 (clone 측정, 고정 seed → 결정론적).
fn support_basis(tab: &Tableau) -> Vec<u8> {
    use rand::rngs::StdRng;
    use rand::SeedableRng;
    let n = tab.num_qubits();
    let mut t = tab.clone();
    let mut rng = StdRng::seed_from_u64(0xC11FF0D);
    (0..n).map(|q| t.measure(q, &mut rng)).collect()
}

/// F₂ 선형계 `M a = rhs` (M: `n_eq × n_var`) 를 풀어 `(particular, kernel_basis)`
/// 반환.  해 없으면 `None`.
#[allow(clippy::needless_range_loop)]
fn solve_f2(
    m_rows: &[Vec<bool>],
    rhs: &[bool],
    n_var: usize,
) -> Option<(Vec<bool>, Vec<Vec<bool>>)> {
    // 증강 행렬 (각 행 len n_var+1).
    let mut aug: Vec<Vec<bool>> = m_rows
        .iter()
        .zip(rhs.iter())
        .map(|(row, &b)| {
            let mut r = row.clone();
            r.push(b);
            r
        })
        .collect();
    let n_eq = aug.len();
    let mut pivot_col = vec![usize::MAX; n_eq]; // 행 r 의 pivot 열
    let mut where_pivot = vec![usize::MAX; n_var]; // 열 c 의 pivot 행
    let mut rank = 0;
    for col in 0..n_var {
        // pivot 찾기
        let mut sel = None;
        for r in rank..n_eq {
            if aug[r][col] {
                sel = Some(r);
                break;
            }
        }
        let Some(sel) = sel else { continue };
        aug.swap(rank, sel);
        for r in 0..n_eq {
            if r != rank && aug[r][col] {
                for c in col..=n_var {
                    let v = aug[rank][c];
                    aug[r][c] ^= v;
                }
            }
        }
        pivot_col[rank] = col;
        where_pivot[col] = rank;
        rank += 1;
        if rank == n_eq {
            break;
        }
    }
    // 모순 검사 (0 = 1)
    for r in rank..n_eq {
        if aug[r][n_var] {
            return None;
        }
    }
    // particular: free 변수 = 0, pivot 변수 = rhs.
    let mut part = vec![false; n_var];
    for r in 0..rank {
        let pc = pivot_col[r];
        if pc != usize::MAX {
            part[pc] = aug[r][n_var];
        }
    }
    // kernel basis: 각 free 열 c → 벡터 (c=1, pivot 변수 = -aug[pivotrow][c]).
    let mut kernel = Vec::new();
    for c in 0..n_var {
        if where_pivot[c] == usize::MAX {
            // free
            let mut v = vec![false; n_var];
            v[c] = true;
            for r in 0..rank {
                let pc = pivot_col[r];
                if pc != usize::MAX && aug[r][c] {
                    v[pc] = true;
                }
            }
            kernel.push(v);
        }
    }
    Some((part, kernel))
}

/// `S(a) = ∏_i Sᵢ^{a_i}` 의 ℤ₄ 위상 지수 `e(a)` (⟨x|S(a)|x0⟩ = i^{e(a)} when in coset).
fn e_of(a: &[bool], xg: &[Vec<bool>], zg: &[Vec<bool>], pg: &[u8], x0: &[u8]) -> u8 {
    let n = x0.len();
    let mut u = vec![false; n];
    let mut w = vec![false; n];
    let mut p: u32 = 0;
    for (i, &ai) in a.iter().enumerate() {
        if !ai {
            continue;
        }
        // w · xg[i] (mod 2)
        let mut dot = 0u32;
        for q in 0..n {
            if w[q] && xg[i][q] {
                dot ^= 1;
            }
        }
        p = (p + pg[i] as u32 + 2 * dot) % 4;
        for q in 0..n {
            u[q] ^= xg[i][q];
            w[q] ^= zg[i][q];
        }
    }
    let _ = u;
    // e = p + 2 (w · x0)
    let mut dot0 = 0u32;
    for q in 0..n {
        if w[q] && x0[q] == 1 {
            dot0 ^= 1;
        }
    }
    ((p + 2 * dot0) % 4) as u8
}

fn xor_bits(a: &[bool], b: &[bool]) -> Vec<bool> {
    a.iter().zip(b.iter()).map(|(&x, &y)| x ^ y).collect()
}

/// 한 stabilizer 상태(tableau)의 **여러 basis amplitude** 를 빠르게 평가하기 위한
/// 사전계산 컨텍스트.  생성자 추출 · support 기저 `x0` · 커널 기저 · 2차형식 결합
/// 행렬 `coup` (basis 무관) 를 **1회** 계산해 두고, `amplitude(x)` 는 per-x coset
/// 해 + 선형항 + Gauss sum 만 수행한다.  near-Clifford 의 `2ᵗ` 항이 동일 `|Φ⟩` 를
/// 공유하므로 측정·생성자추출·2차형식의 반복 계산을 제거 → 큰 속도 향상.
pub struct StabContext {
    n: usize,
    xg: Vec<Vec<bool>>,
    zg: Vec<Vec<bool>>,
    pg: Vec<u8>,
    x0: Vec<u8>,
    m_rows: Vec<Vec<bool>>,
    kernel: Vec<Vec<bool>>,
    coup: Vec<Vec<u8>>,
    scale: f64,
}

impl StabContext {
    pub fn new(tab: &Tableau) -> Self {
        let n = tab.num_qubits();
        let (xg, zg, pg) = extract_generators(tab);
        let x0 = support_basis(tab);
        let mut m_rows = vec![vec![false; n]; n];
        for q in 0..n {
            for i in 0..n {
                m_rows[q][i] = xg[i][q];
            }
        }
        // 커널은 rhs 무관 — 동차계로 한 번.
        let (_a0, kernel) =
            solve_f2(&m_rows, &vec![false; n], n).expect("homogeneous always solvable");
        let k = kernel.len();
        // 2차형식 결합행렬 (basis 0 기준; 2차 차분은 base 무관).
        let e00 = e_of(&vec![false; n], &xg, &zg, &pg, &x0);
        let e_v: Vec<u8> = (0..k)
            .map(|m| e_of(&kernel[m], &xg, &zg, &pg, &x0))
            .collect();
        let mut coup = vec![vec![0u8; k]; k];
        for m in 0..k {
            for l in (m + 1)..k {
                let amn = xor_bits(&kernel[m], &kernel[l]);
                let emn = e_of(&amn, &xg, &zg, &pg, &x0);
                let cc = (emn as i32 - e_v[m] as i32 - e_v[l] as i32 + e00 as i32).rem_euclid(4);
                debug_assert!(cc % 2 == 0, "quadratic cross term not even: {cc}");
                coup[m][l] = (cc / 2) as u8;
                coup[l][m] = coup[m][l];
            }
        }
        let scale = 2.0_f64.powf((n - k) as f64 / 2.0 - n as f64);
        StabContext {
            n,
            xg,
            zg,
            pg,
            x0,
            m_rows,
            kernel,
            coup,
            scale,
        }
    }

    /// support 내 기저상태 하나 (사전계산된 `x0`).  `amplitude(support_point()) ≠ 0`.
    pub fn support_point(&self) -> &[u8] {
        &self.x0
    }

    /// canonical basis amplitude `⟨x|φ⟩`.
    pub fn amplitude(&self, x: &[u8]) -> Complex64 {
        let n = self.n;
        let mut rhs = vec![false; n];
        for q in 0..n {
            rhs[q] = (x[q] ^ self.x0[q]) == 1;
        }
        let Some((astar, _k)) = solve_f2(&self.m_rows, &rhs, n) else {
            return Complex64::new(0.0, 0.0);
        };
        let k = self.kernel.len();
        let e0 = e_of(&astar, &self.xg, &self.zg, &self.pg, &self.x0);
        let lin: Vec<u8> = (0..k)
            .map(|m| {
                let am = xor_bits(&astar, &self.kernel[m]);
                let em = e_of(&am, &self.xg, &self.zg, &self.pg, &self.x0);
                ((em as i32 - e0 as i32).rem_euclid(4)) as u8
            })
            .collect();
        let gsum = Complex64::from_polar(1.0, (e0 as f64) * std::f64::consts::FRAC_PI_2)
            * gauss_sum(&lin, &self.coup);
        Complex64::new(self.scale, 0.0) * gsum
    }
}

/// canonical stabilizer 상태의 basis amplitude `⟨x|φ⟩` (전역 위상은 deterministic
/// gauge 로 고정 — `PhaseStab` 의 omega 가 실제 위상으로 보정).
pub fn stab_amplitude(tab: &Tableau, x: &[u8]) -> Complex64 {
    StabContext::new(tab).amplitude(x)
}

// ===================== phase-aware stabilizer 상태 =====================

/// 단일 큐비트 Clifford 게이트 종류 (tableau 갱신 + 2×2 행렬 매핑).
#[derive(Clone, Copy)]
enum G1 {
    H,
    S,
    Sdg,
    X,
    Y,
    Z,
    Sx,
    Sxdg,
}

impl G1 {
    fn matrix(self) -> [[Complex64; 2]; 2] {
        let z = Complex64::new(0.0, 0.0);
        let o = Complex64::new(1.0, 0.0);
        let i = Complex64::new(0.0, 1.0);
        let s = Complex64::new(std::f64::consts::FRAC_1_SQRT_2, 0.0);
        let h = 0.5;
        match self {
            G1::H => [[s, s], [s, -s]],
            G1::S => [[o, z], [z, i]],
            G1::Sdg => [[o, z], [z, -i]],
            G1::X => [[z, o], [o, z]],
            G1::Y => [[z, -i], [i, z]],
            G1::Z => [[o, z], [z, -o]],
            G1::Sx => [
                [Complex64::new(h, h), Complex64::new(h, -h)],
                [Complex64::new(h, -h), Complex64::new(h, h)],
            ],
            G1::Sxdg => [
                [Complex64::new(h, -h), Complex64::new(h, h)],
                [Complex64::new(h, h), Complex64::new(h, -h)],
            ],
        }
    }
    fn apply_tab(self, tab: &mut Tableau, q: usize) {
        match self {
            G1::H => tab.h(q),
            G1::S => tab.s(q),
            G1::Sdg => tab.sdg(q),
            G1::X => tab.x_gate(q),
            G1::Y => tab.y_gate(q),
            G1::Z => tab.z_gate(q),
            G1::Sx => tab.sx(q),
            G1::Sxdg => tab.sxdg(q),
        }
    }
}

/// 전역 위상까지 추적하는 stabilizer 상태: 실제 |ψ⟩ = `omega` · canonical(`tab`).
///
/// 게이트 적용 시 tableau 를 갱신하고, 새 상태 support 의 기저 `x*` 에서
/// `⟨x*|G|ψ⟩` (G 행렬 + 옛 canonical amplitude) 와 새 canonical amplitude 의
/// 비율로 `omega` 를 갱신한다 → 전역 위상 정확.
#[derive(Clone)]
pub struct PhaseStab {
    tab: Tableau,
    omega: Complex64,
}

impl PhaseStab {
    /// |0…0⟩.
    pub fn new(n: usize) -> Self {
        PhaseStab {
            tab: Tableau::new(n),
            omega: Complex64::new(1.0, 0.0),
        }
    }

    /// `⟨x|ψ⟩` (전역 위상 포함, 절대값).
    pub fn amplitude(&self, x: &[u8]) -> Complex64 {
        self.omega * stab_amplitude(&self.tab, x)
    }

    fn flip(x: &[u8], q: usize) -> Vec<u8> {
        let mut y = x.to_vec();
        y[q] ^= 1;
        y
    }

    fn apply_1q(&mut self, g: G1, q: usize) {
        // old / new 의 StabContext 를 각 1회만 구축 (support_basis 중복 제거).
        let ctx_old = StabContext::new(&self.tab);
        let omega_old = self.omega;
        g.apply_tab(&mut self.tab, q);
        let ctx_new = StabContext::new(&self.tab);
        let xstar = ctx_new.support_point().to_vec(); // new support 의 기저
        let u = g.matrix();
        let row = xstar[q] as usize;
        let mut y0 = xstar.clone();
        y0[q] = 0;
        let y1 = Self::flip(&y0, q);
        let psi = u[row][0] * omega_old * ctx_old.amplitude(&y0)
            + u[row][1] * omega_old * ctx_old.amplitude(&y1);
        let canon_new = ctx_new.amplitude(&xstar);
        self.omega = psi / canon_new;
    }

    fn apply_cnot(&mut self, c: usize, t: usize) {
        let ctx_old = StabContext::new(&self.tab);
        let omega_old = self.omega;
        self.tab.cnot(c, t);
        let ctx_new = StabContext::new(&self.tab);
        let xstar = ctx_new.support_point().to_vec();
        // CNOT|y⟩=|y with t^=y_c⟩ → 입력 y: y_c=x*_c, y_t = x*_t ⊕ x*_c.
        let mut y = xstar.clone();
        y[t] = xstar[t] ^ xstar[c];
        let psi = omega_old * ctx_old.amplitude(&y);
        let canon_new = ctx_new.amplitude(&xstar);
        self.omega = psi / canon_new;
    }

    // ---- public Clifford 게이트 (primitive 조합) ----
    pub fn h(&mut self, q: usize) {
        self.apply_1q(G1::H, q);
    }
    pub fn s(&mut self, q: usize) {
        self.apply_1q(G1::S, q);
    }
    pub fn sdg(&mut self, q: usize) {
        self.apply_1q(G1::Sdg, q);
    }
    pub fn x(&mut self, q: usize) {
        self.apply_1q(G1::X, q);
    }
    pub fn y(&mut self, q: usize) {
        self.apply_1q(G1::Y, q);
    }
    pub fn z(&mut self, q: usize) {
        self.apply_1q(G1::Z, q);
    }
    pub fn sx(&mut self, q: usize) {
        self.apply_1q(G1::Sx, q);
    }
    pub fn sxdg(&mut self, q: usize) {
        self.apply_1q(G1::Sxdg, q);
    }
    pub fn cnot(&mut self, c: usize, t: usize) {
        self.apply_cnot(c, t);
    }
    pub fn cz(&mut self, a: usize, b: usize) {
        self.h(b);
        self.cnot(a, b);
        self.h(b);
    }
    pub fn cy(&mut self, a: usize, b: usize) {
        self.sdg(b);
        self.cnot(a, b);
        self.s(b);
    }
    pub fn swap(&mut self, a: usize, b: usize) {
        self.cnot(a, b);
        self.cnot(b, a);
        self.cnot(a, b);
    }
    pub fn iswap(&mut self, a: usize, b: usize) {
        self.s(a);
        self.s(b);
        self.h(a);
        self.cnot(a, b);
        self.cnot(b, a);
        self.h(b);
    }
    pub fn dcx(&mut self, a: usize, b: usize) {
        self.cnot(a, b);
        self.cnot(b, a);
    }
}

/// near-Clifford 게이트 (Clifford + T/Tdg).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum CtGate {
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
    T(usize),
    Tdg(usize),
}

/// Clifford+T 회로의 amplitude `⟨x|C|0…0⟩` 를 stabilizer-항 분해로 정확히 계산.
///
/// T 게이트마다 항이 2배 (`≤2^t`).  각 항은 전역 위상까지 정확한 [`PhaseStab`].
/// 최종 `Σ_k c_k ⟨x|φ_k⟩`.  `t_count` 가 크면 (≳25) 항 수가 폭발하므로 비현실적
/// (Bravyi-Gosset 의 더 낮은 base 분해는 후속 최적화 영역).
pub fn clifford_t_amplitude(n: usize, gates: &[CtGate], x: &[u8]) -> Complex64 {
    let cos = (std::f64::consts::FRAC_PI_8).cos();
    let sin = (std::f64::consts::FRAC_PI_8).sin();
    let ep = Complex64::from_polar(1.0, std::f64::consts::FRAC_PI_8); // e^{iπ/8}
    let em = Complex64::from_polar(1.0, -std::f64::consts::FRAC_PI_8);
    let mi = Complex64::new(0.0, -1.0);
    let pi = Complex64::new(0.0, 1.0);

    let mut terms: Vec<(Complex64, PhaseStab)> =
        vec![(Complex64::new(1.0, 0.0), PhaseStab::new(n))];
    for &g in gates {
        match g {
            CtGate::T(q) => {
                let mut next = Vec::with_capacity(terms.len() * 2);
                for (c, ps) in terms.drain(..) {
                    let mut psz = ps.clone();
                    psz.z(q);
                    next.push((c * ep * cos, ps));
                    next.push((c * ep * mi * sin, psz));
                }
                terms = next;
            }
            CtGate::Tdg(q) => {
                let mut next = Vec::with_capacity(terms.len() * 2);
                for (c, ps) in terms.drain(..) {
                    let mut psz = ps.clone();
                    psz.z(q);
                    next.push((c * em * cos, ps));
                    next.push((c * em * pi * sin, psz));
                }
                terms = next;
            }
            other => {
                for (_, ps) in terms.iter_mut() {
                    match other {
                        CtGate::H(q) => ps.h(q),
                        CtGate::S(q) => ps.s(q),
                        CtGate::Sdg(q) => ps.sdg(q),
                        CtGate::X(q) => ps.x(q),
                        CtGate::Y(q) => ps.y(q),
                        CtGate::Z(q) => ps.z(q),
                        CtGate::Sx(q) => ps.sx(q),
                        CtGate::Sxdg(q) => ps.sxdg(q),
                        CtGate::Cnot(a, b) => ps.cnot(a, b),
                        CtGate::Cz(a, b) => ps.cz(a, b),
                        CtGate::Cy(a, b) => ps.cy(a, b),
                        CtGate::Swap(a, b) => ps.swap(a, b),
                        CtGate::Iswap(a, b) => ps.iswap(a, b),
                        CtGate::Dcx(a, b) => ps.dcx(a, b),
                        CtGate::T(_) | CtGate::Tdg(_) => unreachable!(),
                    }
                }
            }
        }
    }
    terms.iter().map(|(c, ps)| *c * ps.amplitude(x)).sum()
}

// ===================== 최적화: Pauli 전파 (Clifford 진화 1회) =====================

/// Pauli 연산자 `i^p ∏_q X^{x_q} Z^{z_q}` (전파/곱셈 편의 convention).
#[derive(Clone)]
struct PauliOp {
    x: Vec<bool>,
    z: Vec<bool>,
    p: u8, // ℤ₄
}

impl PauliOp {
    fn z_on(n: usize, q: usize) -> Self {
        let mut z = vec![false; n];
        z[q] = true;
        PauliOp {
            x: vec![false; n],
            z,
            p: 0,
        }
    }
    /// G P G† forward 켤레 — primitive Clifford 별 규칙.
    fn conj_h(&mut self, q: usize) {
        self.p = (self.p + 2 * (self.x[q] & self.z[q]) as u8) & 3;
        std::mem::swap(&mut self.x[q], &mut self.z[q]);
    }
    fn conj_s(&mut self, q: usize) {
        self.p = (self.p + self.x[q] as u8) & 3;
        self.z[q] ^= self.x[q];
    }
    fn conj_sdg(&mut self, q: usize) {
        self.p = (self.p + 3 * self.x[q] as u8) & 3;
        self.z[q] ^= self.x[q];
    }
    fn conj_x(&mut self, q: usize) {
        self.p = (self.p + 2 * self.z[q] as u8) & 3;
    }
    fn conj_y(&mut self, q: usize) {
        self.p = (self.p + 2 * ((self.x[q] ^ self.z[q]) as u8)) & 3;
    }
    fn conj_z(&mut self, q: usize) {
        self.p = (self.p + 2 * self.x[q] as u8) & 3;
    }
    fn conj_cnot(&mut self, c: usize, t: usize) {
        self.x[t] ^= self.x[c];
        self.z[c] ^= self.z[t];
    }
    /// self ← self · other (Pauli 곱, 위상 포함).
    fn mul(&mut self, other: &PauliOp) {
        // i^{p1+p2+2 (w1·u2)}
        let mut dot = 0u8;
        for q in 0..self.x.len() {
            if self.z[q] && other.x[q] {
                dot ^= 1;
            }
        }
        self.p = (self.p + other.p + 2 * dot) & 3;
        for q in 0..self.x.len() {
            self.x[q] ^= other.x[q];
            self.z[q] ^= other.z[q];
        }
    }
}

/// net Pauli (u,w) 그룹화 엔트리: `((x-bits, z-bits), 누적 계수)`.
type PauliGroup = ((Vec<bool>, Vec<bool>), Complex64);

/// primitive Clifford 게이트 스트림 (composite 는 flatten).
#[derive(Clone, Copy)]
enum Prim {
    H(usize),
    S(usize),
    Sdg(usize),
    X(usize),
    Y(usize),
    Z(usize),
    Cnot(usize, usize),
    T(usize),
    Tdg(usize),
}

/// CtGate 시퀀스를 primitive 스트림으로 flatten (Sx=HSH 등).
fn flatten(gates: &[CtGate]) -> Vec<Prim> {
    let mut out = Vec::new();
    for &g in gates {
        match g {
            CtGate::H(q) => out.push(Prim::H(q)),
            CtGate::S(q) => out.push(Prim::S(q)),
            CtGate::Sdg(q) => out.push(Prim::Sdg(q)),
            CtGate::X(q) => out.push(Prim::X(q)),
            CtGate::Y(q) => out.push(Prim::Y(q)),
            CtGate::Z(q) => out.push(Prim::Z(q)),
            CtGate::Sx(q) => {
                out.push(Prim::H(q));
                out.push(Prim::S(q));
                out.push(Prim::H(q));
            }
            CtGate::Sxdg(q) => {
                out.push(Prim::H(q));
                out.push(Prim::Sdg(q));
                out.push(Prim::H(q));
            }
            CtGate::Cnot(a, b) => out.push(Prim::Cnot(a, b)),
            CtGate::Cz(a, b) => {
                out.push(Prim::H(b));
                out.push(Prim::Cnot(a, b));
                out.push(Prim::H(b));
            }
            CtGate::Cy(a, b) => {
                out.push(Prim::Sdg(b));
                out.push(Prim::Cnot(a, b));
                out.push(Prim::S(b));
            }
            CtGate::Swap(a, b) => {
                out.push(Prim::Cnot(a, b));
                out.push(Prim::Cnot(b, a));
                out.push(Prim::Cnot(a, b));
            }
            CtGate::Iswap(a, b) => {
                out.push(Prim::S(a));
                out.push(Prim::S(b));
                out.push(Prim::H(a));
                out.push(Prim::Cnot(a, b));
                out.push(Prim::Cnot(b, a));
                out.push(Prim::H(b));
            }
            CtGate::Dcx(a, b) => {
                out.push(Prim::Cnot(a, b));
                out.push(Prim::Cnot(b, a));
            }
            CtGate::T(q) => out.push(Prim::T(q)),
            CtGate::Tdg(q) => out.push(Prim::Tdg(q)),
        }
    }
    out
}

/// near-Clifford 회로의 stabilizer-rank 표현: Clifford 진화를 1회 수행한 최종
/// 상태 |Φ⟩ + 각 T 의 회로-끝 전파 Pauli + 분기 계수.
struct NearClifford {
    phi: PhaseStab,
    corr: Vec<PauliOp>,
    a_coeff: Vec<Complex64>,
    b_coeff: Vec<Complex64>,
}

/// Clifford 진화 1회 + T 의 Z 보정 전파.
fn build_near_clifford(n: usize, gates: &[CtGate]) -> NearClifford {
    let cos = (std::f64::consts::FRAC_PI_8).cos();
    let sin = (std::f64::consts::FRAC_PI_8).sin();
    let ep = Complex64::from_polar(1.0, std::f64::consts::FRAC_PI_8);
    let em = Complex64::from_polar(1.0, -std::f64::consts::FRAC_PI_8);
    let mi = Complex64::new(0.0, -1.0);
    let pi = Complex64::new(0.0, 1.0);

    let prims = flatten(gates);
    let mut phi = PhaseStab::new(n);
    let mut corr: Vec<PauliOp> = Vec::new();
    let mut a_coeff: Vec<Complex64> = Vec::new();
    let mut b_coeff: Vec<Complex64> = Vec::new();

    for pr in &prims {
        match *pr {
            Prim::T(q) | Prim::Tdg(q) => {
                corr.push(PauliOp::z_on(n, q));
                if matches!(pr, Prim::T(_)) {
                    a_coeff.push(ep * cos);
                    b_coeff.push(ep * mi * sin);
                } else {
                    a_coeff.push(em * cos);
                    b_coeff.push(em * pi * sin);
                }
            }
            other => match other {
                Prim::H(q) => {
                    phi.h(q);
                    corr.iter_mut().for_each(|c| c.conj_h(q));
                }
                Prim::S(q) => {
                    phi.s(q);
                    corr.iter_mut().for_each(|c| c.conj_s(q));
                }
                Prim::Sdg(q) => {
                    phi.sdg(q);
                    corr.iter_mut().for_each(|c| c.conj_sdg(q));
                }
                Prim::X(q) => {
                    phi.x(q);
                    corr.iter_mut().for_each(|c| c.conj_x(q));
                }
                Prim::Y(q) => {
                    phi.y(q);
                    corr.iter_mut().for_each(|c| c.conj_y(q));
                }
                Prim::Z(q) => {
                    phi.z(q);
                    corr.iter_mut().for_each(|c| c.conj_z(q));
                }
                Prim::Cnot(a, b) => {
                    phi.cnot(a, b);
                    corr.iter_mut().for_each(|c| c.conj_cnot(a, b));
                }
                Prim::T(_) | Prim::Tdg(_) => unreachable!(),
            },
        }
    }
    NearClifford {
        phi,
        corr,
        a_coeff,
        b_coeff,
    }
}

/// `build_near_clifford` 의 ChForm (QFE) 버전 — amplitude 평가가 O(n²~n³)
/// (PhaseStab 의 Gauss-sum O(n³) 보다 빠름).  corr/coeff 는 동일.
fn build_near_clifford_ch(
    n: usize,
    gates: &[CtGate],
) -> (
    crate::ch_form::ChForm,
    Vec<PauliOp>,
    Vec<Complex64>,
    Vec<Complex64>,
) {
    let cos = (std::f64::consts::FRAC_PI_8).cos();
    let sin = (std::f64::consts::FRAC_PI_8).sin();
    let ep = Complex64::from_polar(1.0, std::f64::consts::FRAC_PI_8);
    let em = Complex64::from_polar(1.0, -std::f64::consts::FRAC_PI_8);
    let mi = Complex64::new(0.0, -1.0);
    let pi = Complex64::new(0.0, 1.0);
    let prims = flatten(gates);
    let mut phi = crate::ch_form::ChForm::new(n);
    let mut corr: Vec<PauliOp> = Vec::new();
    let mut a_coeff: Vec<Complex64> = Vec::new();
    let mut b_coeff: Vec<Complex64> = Vec::new();
    for pr in &prims {
        match *pr {
            Prim::T(q) | Prim::Tdg(q) => {
                corr.push(PauliOp::z_on(n, q));
                if matches!(pr, Prim::T(_)) {
                    a_coeff.push(ep * cos);
                    b_coeff.push(ep * mi * sin);
                } else {
                    a_coeff.push(em * cos);
                    b_coeff.push(em * pi * sin);
                }
            }
            Prim::H(q) => {
                phi.h_gate(q);
                corr.iter_mut().for_each(|c| c.conj_h(q));
            }
            Prim::S(q) => {
                phi.s_gate(q);
                corr.iter_mut().for_each(|c| c.conj_s(q));
            }
            Prim::Sdg(q) => {
                phi.sdg_gate(q);
                corr.iter_mut().for_each(|c| c.conj_sdg(q));
            }
            Prim::X(q) => {
                phi.x_gate(q);
                corr.iter_mut().for_each(|c| c.conj_x(q));
            }
            Prim::Y(q) => {
                phi.y_gate(q);
                corr.iter_mut().for_each(|c| c.conj_y(q));
            }
            Prim::Z(q) => {
                phi.z_gate(q);
                corr.iter_mut().for_each(|c| c.conj_z(q));
            }
            Prim::Cnot(a, b) => {
                phi.cx_gate(a, b);
                corr.iter_mut().for_each(|c| c.conj_cnot(a, b));
            }
        }
    }
    (phi, corr, a_coeff, b_coeff)
}

/// near-Clifford amplitude 평가기 — Clifford 진화 1회 (ChForm) + net-Pauli 그룹
/// 사전계산.  여러 x 의 amplitude 를 빠르게 평가한다 (amplitude / 샘플링 공용).
pub struct NearCliffordAmp {
    n: usize,
    phi: crate::ch_form::ChForm,
    /// `phi` 의 미리계산 amplitude 평가기 (B 의 RREF 변환 1회 분할상환).
    eval: crate::ch_form::ChAmpEval,
    /// 그룹: ((u, w), 누적 계수).
    groups: Vec<PauliGroup>,
}

impl NearCliffordAmp {
    pub fn build(n: usize, gates: &[CtGate]) -> Self {
        let (phi, corr, a_coeff, b_coeff) = build_near_clifford_ch(n, gates);
        let t = corr.len();
        use std::collections::HashMap;
        let mut groups: HashMap<(Vec<bool>, Vec<bool>), Complex64> = HashMap::new();
        for mask in 0..(1u64 << t) {
            let mut coeff = Complex64::new(1.0, 0.0);
            let mut ps = PauliOp {
                x: vec![false; n],
                z: vec![false; n],
                p: 0,
            };
            for i in 0..t {
                coeff *= if (mask >> i) & 1 == 1 {
                    b_coeff[i]
                } else {
                    a_coeff[i]
                };
            }
            for i in (0..t).rev() {
                if (mask >> i) & 1 == 1 {
                    ps.mul(&corr[i]);
                }
            }
            let phase_p = Complex64::from_polar(1.0, ps.p as f64 * std::f64::consts::FRAC_PI_2);
            *groups
                .entry((ps.x.clone(), ps.z.clone()))
                .or_insert(Complex64::new(0.0, 0.0)) += coeff * phase_p;
        }
        let eval = phi.amp_eval();
        // HashMap 반복 순서는 인스턴스마다 무작위 → 그룹 순서를 결정적으로
        // 정렬한다.  (float 합 순서 + groups.first() 의 coset 기준이 재현성에
        // 영향을 주므로 필수.)
        let mut groups: Vec<PauliGroup> = groups.into_iter().collect();
        groups.sort_by(|a, b| a.0.cmp(&b.0));
        NearCliffordAmp {
            n,
            phi,
            eval,
            groups,
        }
    }

    /// `⟨x|ψ⟩` (그룹 합을 rayon 병렬).  단일 진폭 평가용.
    pub fn amp(&self, x: &[u8]) -> Complex64 {
        use rayon::prelude::*;
        self.groups.par_iter().map(|g| self.group_term(g, x)).sum()
    }

    /// `⟨x|ψ⟩` (직렬).  체인을 병렬화할 때 (`clifford_t_sample` 다중 체인)
    /// 중첩 병렬을 피하려고 쓴다.
    pub fn amp_serial(&self, x: &[u8]) -> Complex64 {
        self.groups.iter().map(|g| self.group_term(g, x)).sum()
    }

    #[inline]
    fn group_term(&self, ((u, w), gc): &PauliGroup, x: &[u8]) -> Complex64 {
        let xp: Vec<u8> = (0..self.n).map(|q| x[q] ^ u[q] as u8).collect();
        let amp_phi = self.eval.amplitude(&xp);
        let mut sign = 0u8;
        for (&wq, &xq) in w.iter().zip(xp.iter()) {
            if wq && xq == 1 {
                sign ^= 1;
            }
        }
        let s = if sign == 1 { -1.0 } else { 1.0 };
        *gc * Complex64::new(s, 0.0) * amp_phi
    }
}

/// **최적화된** Clifford+T amplitude (`NearCliffordAmp` 1회 빌드 + 평가).
/// 결과는 [`clifford_t_amplitude`] 와 동일.
pub fn clifford_t_amplitude_fast(n: usize, gates: &[CtGate], x: &[u8]) -> Complex64 {
    NearCliffordAmp::build(n, gates).amp(x)
}

/// near-Clifford MCMC 샘플러 — 미리계산된 amplitude 평가기 + 아핀-구조 제안
/// 이동 집합을 보관해 여러 체인을 돌린다.
pub struct MhSampler {
    n: usize,
    nca: NearCliffordAmp,
    /// 아핀-구조 제안 이동 집합 (대칭 involution, nonzero, dedup).
    moves: Vec<Vec<u8>>,
}

impl MhSampler {
    /// 회로로부터 샘플러를 빌드한다 (`NearCliffordAmp` + 제안 이동 집합).
    pub fn build(n: usize, gates: &[CtGate]) -> Self {
        use std::collections::HashSet;
        let nca = NearCliffordAmp::build(n, gates);
        let mut seen: HashSet<Vec<u8>> = HashSet::new();
        let mut moves: Vec<Vec<u8>> = Vec::new();
        let mut add_move = |m: Vec<u8>| {
            if m.iter().any(|&b| b != 0) && seen.insert(m.clone()) {
                moves.push(m);
            }
        };
        // (1) supp(φ) 방향 = B 의 열들 (coset 내부 이동).
        for dir in nca.phi.support_directions() {
            add_move(dir.iter().map(|&b| b as u8).collect());
        }
        // (2) coset 간 이동 u_g ⊕ u_0 (기준 = 첫 그룹).
        if let Some(((u0, _), _)) = nca.groups.first() {
            for ((ug, _), _) in nca.groups.iter() {
                add_move((0..n).map(|q| (ug[q] ^ u0[q]) as u8).collect());
            }
        }
        // (3) 보조: 단일 비트플립.
        for q in 0..n {
            let mut m = vec![0u8; n];
            m[q] = 1;
            add_move(m);
        }
        MhSampler { n, nca, moves }
    }

    #[inline]
    fn prob(&self, x: &[u8]) -> f64 {
        self.nca.amp_serial(x).norm_sqr()
    }

    /// 단일 체인을 돌려 `n_samples` 개를 수집한다 (`burn_in` 후 `thin` 간격).
    /// 시작점은 random restart 로 찾은 support 점.
    fn run_chain(&self, n_samples: usize, burn_in: usize, thin: usize, seed: u64) -> Vec<Vec<u8>> {
        use rand::rngs::StdRng;
        use rand::{Rng, SeedableRng};
        let n = self.n;
        if self.moves.is_empty() {
            return vec![vec![0u8; n]; n_samples];
        }
        let mut rng = StdRng::seed_from_u64(seed);
        let mut cur = vec![0u8; n];
        let mut pcur = self.prob(&cur);
        if pcur <= 0.0 {
            for _ in 0..256 {
                let cand: Vec<u8> = (0..n).map(|_| rng.gen::<bool>() as u8).collect();
                let pc = self.prob(&cand);
                if pc > 0.0 {
                    cur = cand;
                    pcur = pc;
                    break;
                }
            }
        }
        let thin = thin.max(1);
        let total_steps = burn_in + n_samples * thin;
        let mut out = Vec::with_capacity(n_samples);
        for step in 0..total_steps {
            let m = &self.moves[rng.gen_range(0..self.moves.len())];
            let prop: Vec<u8> = (0..n).map(|q| cur[q] ^ m[q]).collect();
            let pprop = self.prob(&prop);
            let accept = if pcur <= 0.0 {
                pprop > 0.0 || rng.gen::<bool>()
            } else {
                pprop >= pcur || rng.gen::<f64>() < pprop / pcur
            };
            if accept {
                cur = prop;
                pcur = pprop;
            }
            if step >= burn_in && (step - burn_in).is_multiple_of(thin) {
                out.push(cur.clone());
            }
        }
        out
    }

    /// `chains` 개의 독립 체인을 **병렬** 로 돌려 표본을 모은다.  각 체인은
    /// 독립 시드 + 독립 random support 시작점 → 다봉 분포에서도 모드 누락을
    /// 줄인다.  반환은 체인별 표본 목록 (진단 계산용).
    pub fn run_chains(
        &self,
        shots: usize,
        burn_in: usize,
        thin: usize,
        chains: usize,
        seed: Option<u64>,
    ) -> Vec<Vec<Vec<u8>>> {
        use rayon::prelude::*;
        let chains = chains.max(1);
        let base = seed.unwrap_or_else(rand::random);
        // shots 를 체인에 분배 (나머지는 앞쪽 체인에).
        let per = shots / chains;
        let rem = shots % chains;
        (0..chains)
            .into_par_iter()
            .map(|c| {
                let ns = per + if c < rem { 1 } else { 0 };
                // 체인마다 독립 시드 (base 와 chain index 혼합).
                let s = base
                    .wrapping_mul(0x9E37_79B9_7F4A_7C15)
                    .wrapping_add(c as u64)
                    .wrapping_add(1);
                self.run_chain(ns, burn_in, thin, s)
            })
            .collect()
    }
}

/// near-Clifford 회로를 **다중 체인 Metropolis-Hastings MCMC** 로 샘플링한다 (근사).
///
/// 타깃 `∝ |⟨x|ψ⟩|²`.  채택확률 `min(1, |ψ(x')|²/|ψ(x)|²)` → 정상분포 =
/// 정확한 출력분포.  amplitude 는 정확 (`NearCliffordAmp`).
///
/// **제안 분포**: stabilizer 유래 상태의 지지집합은 아핀 부분공간들의 합집합
/// `∪_g (u_g ⊕ supp(φ))` 이라, 단일 비트플립은 (예: GHZ `{0…0, 1…1}`) 이들을
/// 연결하지 못해 체인이 한 모드에 갇힌다.  따라서 제안은 아핀 구조를 따르는
/// 대칭 이동 집합 (B 의 열 + `u_g⊕u_0` + 비트플립) 에서 균등 추출한다.
/// 각 이동은 involution 이라 제안이 대칭 → MH 가 타깃을 보존한다.
///
/// `chains` 개의 독립 체인을 병렬로 돌려 (각자 독립 시작점) 모드 누락을 줄이고
/// 표본을 모은다.  반환 `outcomes[shot][q]` (q=0 LSB).  `seed` 재현.
pub fn clifford_t_sample(
    n: usize,
    gates: &[CtGate],
    shots: usize,
    burn_in: usize,
    thin: usize,
    chains: usize,
    seed: Option<u64>,
) -> Vec<Vec<u8>> {
    let sampler = MhSampler::build(n, gates);
    sampler
        .run_chains(shots, burn_in, thin, chains, seed)
        .into_iter()
        .flatten()
        .collect()
}

/// [`clifford_t_sample`] + **Gelman-Rubin 수렴 진단** `R̂`.
///
/// 각 큐비트의 표본 평균(=`P(q=1)`)을 스칼라 관측량으로 보고, 체인 간 분산 `B`
/// 와 체인 내 분산 `W` 로 `R̂ = sqrt((W·(m-1)/m + B/m)/W)` 를 큐비트마다 계산해
/// 최댓값을 반환한다.  `R̂ ≈ 1` (≲1.05) 이면 체인들이 같은 분포로 수렴했다는
/// 신호.  체인이 1개거나 표본이 부족하면 `None`.
pub fn clifford_t_sample_diagnostic(
    n: usize,
    gates: &[CtGate],
    shots: usize,
    burn_in: usize,
    thin: usize,
    chains: usize,
    seed: Option<u64>,
) -> (Vec<Vec<u8>>, Option<f64>) {
    let sampler = MhSampler::build(n, gates);
    let per_chain = sampler.run_chains(shots, burn_in, thin, chains, seed);
    let r_hat = gelman_rubin(&per_chain, n);
    let samples: Vec<Vec<u8>> = per_chain.into_iter().flatten().collect();
    (samples, r_hat)
}

/// 큐비트별 표본평균을 관측량으로 한 Gelman-Rubin `R̂` 의 큐비트 최댓값.
fn gelman_rubin(per_chain: &[Vec<Vec<u8>>], n: usize) -> Option<f64> {
    let m = per_chain.len();
    if m < 2 {
        return None;
    }
    // 각 체인 표본 수가 최소 2 이상이어야 분산 정의됨.
    let lens: Vec<usize> = per_chain.iter().map(|c| c.len()).collect();
    let min_len = *lens.iter().min().unwrap_or(&0);
    if min_len < 2 {
        return None;
    }
    let mut worst: f64 = 1.0;
    for q in 0..n {
        // 체인별 평균과 분산 (관측량 = bit q).
        let mut chain_means = Vec::with_capacity(m);
        let mut w_acc = 0.0; // 체인 내 분산 평균
        for chain in per_chain {
            let len = chain.len() as f64;
            let mean = chain.iter().map(|s| s[q] as f64).sum::<f64>() / len;
            let var = chain
                .iter()
                .map(|s| {
                    let d = s[q] as f64 - mean;
                    d * d
                })
                .sum::<f64>()
                / (len - 1.0);
            chain_means.push(mean);
            w_acc += var;
        }
        let w = w_acc / m as f64;
        if w < 1e-12 {
            // 모든 체인이 이 비트에 대해 상수 (분산 0) → 수렴으로 간주.
            continue;
        }
        let grand = chain_means.iter().sum::<f64>() / m as f64;
        let nbar = min_len as f64;
        let b = nbar / (m as f64 - 1.0)
            * chain_means
                .iter()
                .map(|&cm| {
                    let d = cm - grand;
                    d * d
                })
                .sum::<f64>();
        let var_plus = (nbar - 1.0) / nbar * w + b / nbar;
        let r = (var_plus / w).sqrt();
        if r > worst {
            worst = r;
        }
    }
    Some(worst)
}

// ===================== near-Clifford 기댓값 =====================

impl PauliOp {
    /// 켤레전치 P† = i^{-p+2(x·z)} X^x Z^z (Hermitian Pauli 면 자기 자신).
    fn dagger(&self) -> PauliOp {
        let mut xz = 0u8;
        for q in 0..self.x.len() {
            if self.x[q] && self.z[q] {
                xz ^= 1;
            }
        }
        PauliOp {
            x: self.x.clone(),
            z: self.z.clone(),
            p: ((4 - self.p) + 2 * xz) & 3,
        }
    }
}

/// stabilizer 상태 |Φ⟩ (tableau) 에서 Pauli `q` 의 기댓값 `⟨Φ|q|Φ⟩`.
///
/// `q` 의 `(x,z)` 가 생성자들의 `(x,z)` span 에 없으면 0.  있으면 `q = i^{qp-p}·S(a)`
/// (S(a) 는 군원소, `S(a)|Φ⟩=|Φ⟩`) 이므로 `⟨Φ|q|Φ⟩ = i^{(qp-p) mod 4}` (복소).
/// `q` 가 Hermitian 이면 ∈{0,±1} 이지만, 기댓값 합의 `P_j† P P_k` 처럼 비-Hermitian
/// `q` (예: XZ=−iY) 면 허수값이 나올 수 있다.  전역 위상 무관.
fn pauli_expect_stab(
    tab: &Tableau,
    qx: &[bool],
    qz: &[bool],
    qp: u8,
    xg: &[Vec<bool>],
    zg: &[Vec<bool>],
    pg: &[u8],
) -> Complex64 {
    let n = tab.num_qubits();
    let mut rows = vec![vec![false; n]; 2 * n];
    let mut rhs = vec![false; 2 * n];
    for q in 0..n {
        for i in 0..n {
            rows[q][i] = xg[i][q];
            rows[n + q][i] = zg[i][q];
        }
        rhs[q] = qx[q];
        rhs[n + q] = qz[q];
    }
    let Some((a, _ker)) = solve_f2(&rows, &rhs, n) else {
        return Complex64::new(0.0, 0.0); // q ∉ 군 → 0
    };
    let mut u = vec![false; n];
    let mut w = vec![false; n];
    let mut p: u32 = 0;
    for (i, &ai) in a.iter().enumerate() {
        if !ai {
            continue;
        }
        let mut dot = 0u32;
        for q in 0..n {
            if w[q] && xg[i][q] {
                dot ^= 1;
            }
        }
        p = (p + pg[i] as u32 + 2 * dot) % 4;
        for q in 0..n {
            u[q] ^= xg[i][q];
            w[q] ^= zg[i][q];
        }
    }
    debug_assert!(u == qx.to_vec() && w == qz.to_vec());
    // ⟨Φ|q|Φ⟩ = i^{(qp - p) mod 4}.
    let e = (qp as i32 - p as i32).rem_euclid(4);
    Complex64::from_polar(1.0, e as f64 * std::f64::consts::FRAC_PI_2)
}

/// near-Clifford 회로의 Pauli 기댓값 `⟨ψ|P|ψ⟩` (P = Pauli 문자열).
///
/// `pauli_x[q]`/`pauli_z[q]` 는 큐비트 q 의 Pauli (I:00, X:10, Y:11, Z:01).
/// `|ψ⟩ = Σ_k c_k P_{S_k}|Φ⟩` 이므로
/// `⟨ψ|P|ψ⟩ = Σ_{j,k} c_j* c_k ⟨Φ|P_{S_j}† P P_{S_k}|Φ⟩`, 각 항은 stabilizer
/// 기댓값 (∈{0,±1}).  비용 `O(2^{2t}·n²)` — t 가 작을 때 (≲10) 적합.
/// 전역 위상 무관이라 omega 불필요.
pub fn clifford_t_expectation(
    n: usize,
    gates: &[CtGate],
    pauli_x: &[bool],
    pauli_z: &[bool],
) -> Complex64 {
    use rayon::prelude::*;
    let nc = build_near_clifford(n, gates);
    let tab = &nc.phi.tab;
    let (xg, zg, pg) = extract_generators(tab);
    let t = nc.corr.len();

    // 관측 Pauli (Hermitian): P = i^{#Y} X^x Z^z.
    let mut n_y = 0u8;
    for q in 0..n {
        if pauli_x[q] && pauli_z[q] {
            n_y ^= 1; // mod 2 충분 (phase 2·) — 실제로는 #Y mod 4 필요
        }
    }
    let p_obs = {
        let mut c = 0u32;
        for q in 0..n {
            if pauli_x[q] && pauli_z[q] {
                c += 1;
            }
        }
        (c % 4) as u8
    };
    let _ = n_y;
    let p_obs_op = PauliOp {
        x: pauli_x.to_vec(),
        z: pauli_z.to_vec(),
        p: p_obs,
    };

    // 2^t 항을 net Pauli (u,w) 로 그룹화: |ψ⟩ = Σ_g G_g (X^{u_g}Z^{w_g})|Φ⟩,
    // G_g = Σ_{S→g} coeff_S · i^{p_S}.  pairwise 가 2^{2t} → 2^{2·distinct}.
    use std::collections::HashMap;
    let mut groups: HashMap<(Vec<bool>, Vec<bool>), Complex64> = HashMap::new();
    for mask in 0..(1u64 << t) {
        let mut coeff = Complex64::new(1.0, 0.0);
        for i in 0..t {
            coeff *= if (mask >> i) & 1 == 1 {
                nc.b_coeff[i]
            } else {
                nc.a_coeff[i]
            };
        }
        let mut ps = PauliOp {
            x: vec![false; n],
            z: vec![false; n],
            p: 0,
        };
        for i in (0..t).rev() {
            if (mask >> i) & 1 == 1 {
                ps.mul(&nc.corr[i]);
            }
        }
        let phase_p = Complex64::from_polar(1.0, ps.p as f64 * std::f64::consts::FRAC_PI_2);
        *groups
            .entry((ps.x.clone(), ps.z.clone()))
            .or_insert(Complex64::new(0.0, 0.0)) += coeff * phase_p;
    }
    // 각 그룹 → (PauliOp{u,w,p=0}, G).
    let glist: Vec<(PauliOp, Complex64)> = groups
        .into_iter()
        .map(|((u, w), g)| (PauliOp { x: u, z: w, p: 0 }, g))
        .collect();

    // Σ_{j,k} conj(G_j) G_k ⟨Φ| P_j† H P_k |Φ⟩  (distinct 그룹 pairwise, j 병렬).
    (0..glist.len())
        .into_par_iter()
        .map(|j| {
            let pj_dag = glist[j].0.dagger();
            let mut acc = Complex64::new(0.0, 0.0);
            for (pk, gk) in glist.iter() {
                let mut q = pj_dag.clone();
                q.mul(&p_obs_op);
                q.mul(pk);
                let e = pauli_expect_stab(tab, &q.x, &q.z, q.p, &xg, &zg, &pg);
                if e.norm() > 1e-15 {
                    acc += glist[j].1.conj() * *gk * e;
                }
            }
            acc
        })
        .sum()
}

// ===================== Bravyi–Gosset 저-rank amplitude (2^{t/2}) =====================
//
// 비-adaptive gadget:  T_q|ψ⟩ = √2 · ⟨0|_a CNOT(q→a) (|ψ⟩ ⊗ |A⟩),  |A⟩=(|0⟩+e^{iπ/4}|1⟩)/√2.
//   ⇒ ⟨x|U_{C+T}|0ⁿ⟩ = (√2)ᵗ ⟨x,0ᵗ| W |0ⁿ⟩⊗|magic^t⟩,  W = Clifford (T → CNOT(q,anc)).
// 마법상태 register 를 **rank-2 블록 분해** (χ(|A²⟩)=2, in-sandbox 도출·검증) →
// 2^{⌈t/2⌉} stabilizer 항.  각 항은 (n+t)-큐비트 순수 Clifford 진폭 (PhaseStab).

/// 단일 decomposition prep 게이트 (local 큐비트 0/1 기준).
#[derive(Clone, Copy)]
enum PrepG {
    H(u8),
    S(u8),
    X(u8),
    Cx(u8, u8),
}

/// magic 블록 한 단위의 옵션: (prep 게이트들, 계수).  local 큐비트는 unit 의
/// ancilla 들로 매핑.
struct DecompOption {
    prep: Vec<PrepG>,
    coeff: Complex64,
}

/// |A²⟩ rank-2 분해 (in-sandbox 도출, reconstruction 1e-16).
fn pair_options(dagger: bool) -> [DecompOption; 2] {
    let r = std::f64::consts::FRAC_1_SQRT_2;
    if !dagger {
        // |A²⟩ = (1/√2)σ1 + ((1+i)/2)σ2
        [
            DecompOption {
                prep: vec![PrepG::H(0), PrepG::S(0), PrepG::Cx(0, 1)],
                coeff: Complex64::new(r, 0.0),
            },
            DecompOption {
                prep: vec![
                    PrepG::H(0),
                    PrepG::Cx(0, 1),
                    PrepG::H(0),
                    PrepG::Cx(0, 1),
                    PrepG::H(0),
                ],
                coeff: Complex64::new(0.5, 0.5),
            },
        ]
    } else {
        // |A*²⟩ = ((1-i)/2)σ1' + ((1-i)/2)σ2
        [
            DecompOption {
                prep: vec![PrepG::H(0), PrepG::S(0), PrepG::H(0), PrepG::Cx(0, 1)],
                coeff: Complex64::new(0.5, -0.5),
            },
            DecompOption {
                prep: vec![
                    PrepG::H(0),
                    PrepG::Cx(0, 1),
                    PrepG::H(0),
                    PrepG::Cx(0, 1),
                    PrepG::H(0),
                ],
                coeff: Complex64::new(0.5, -0.5),
            },
        ]
    }
}

/// 단일 magic state |A⟩ = (1/√2)|0⟩ + (e^{±iπ/4}/√2)|1⟩ rank-2 (자명).
fn single_options(dagger: bool) -> [DecompOption; 2] {
    let r = std::f64::consts::FRAC_1_SQRT_2;
    let c1 = if dagger {
        Complex64::new(0.5, -0.5)
    } else {
        Complex64::new(0.5, 0.5)
    };
    [
        DecompOption {
            prep: vec![],
            coeff: Complex64::new(r, 0.0),
        },
        DecompOption {
            prep: vec![PrepG::X(0)],
            coeff: c1,
        },
    ]
}

/// 한 decomposition 단위: ancilla 들(1 또는 2) + 두 옵션.
struct Unit {
    ancillas: Vec<usize>, // global qubit index (n + ...)
    options: [DecompOption; 2],
}

/// W (Clifford on n+t) 의 한 게이트.
#[derive(Clone, Copy)]
enum WOp {
    H(usize),
    S(usize),
    Sdg(usize),
    X(usize),
    Y(usize),
    Z(usize),
    Cnot(usize, usize),
}

/// **Bravyi–Gosset 저-rank** Clifford+T amplitude `⟨x|C|0…0⟩` (2^{⌈t/2⌉} 항).
///
/// gadget 으로 (n+t)-큐비트 Clifford 회로 W 를 만들고, 마법상태 register 를
/// rank-2 블록 분해해 항 수를 `2ᵗ → 2^{⌈t/2⌉}` 로 줄인다.  각 항은 순수 Clifford
/// stabilizer 진폭 (전역 위상 포함).  결과는 [`clifford_t_amplitude_fast`] 와 동일.
pub fn clifford_t_amplitude_lowrank(n: usize, gates: &[CtGate], x: &[u8]) -> Complex64 {
    let prims = flatten(gates);
    // W 구성 + ancilla 타입 기록.
    let mut wops: Vec<WOp> = Vec::new();
    let mut anc_dagger: Vec<bool> = Vec::new(); // ancilla i 가 Tdg(|A*⟩) 면 true
    let mut next_anc = n;
    for pr in &prims {
        match *pr {
            Prim::H(q) => wops.push(WOp::H(q)),
            Prim::S(q) => wops.push(WOp::S(q)),
            Prim::Sdg(q) => wops.push(WOp::Sdg(q)),
            Prim::X(q) => wops.push(WOp::X(q)),
            Prim::Y(q) => wops.push(WOp::Y(q)),
            Prim::Z(q) => wops.push(WOp::Z(q)),
            Prim::Cnot(a, b) => wops.push(WOp::Cnot(a, b)),
            Prim::T(q) => {
                wops.push(WOp::Cnot(q, next_anc));
                anc_dagger.push(false);
                next_anc += 1;
            }
            Prim::Tdg(q) => {
                wops.push(WOp::Cnot(q, next_anc));
                anc_dagger.push(true);
                next_anc += 1;
            }
        }
    }
    let t = anc_dagger.len();
    let ntot = n + t;
    if t == 0 {
        // 순수 Clifford — ChForm 한 번.
        let mut ps = crate::ch_form::ChForm::new(n);
        apply_wops(&mut ps, &wops);
        return ps.amplitude(x);
    }

    // ancilla 들을 타입별로 묶어 unit (pair / single) 생성.
    let t_anc: Vec<usize> = (0..t).filter(|&i| !anc_dagger[i]).map(|i| n + i).collect();
    let tdg_anc: Vec<usize> = (0..t).filter(|&i| anc_dagger[i]).map(|i| n + i).collect();
    let mut units: Vec<Unit> = Vec::new();
    for (anc_list, dag) in [(&t_anc, false), (&tdg_anc, true)] {
        let mut i = 0;
        while i + 1 < anc_list.len() {
            units.push(Unit {
                ancillas: vec![anc_list[i], anc_list[i + 1]],
                options: pair_options(dag),
            });
            i += 2;
        }
        if i < anc_list.len() {
            units.push(Unit {
                ancillas: vec![anc_list[i]],
                options: single_options(dag),
            });
        }
    }
    let u = units.len(); // = ⌈t/2⌉ (타입 혼합 시 약간 더)

    let sqrt2_t = 2.0_f64.powf(t as f64 / 2.0);

    // W 1회 합성: |η⟩ = W†|x,0ᵗ⟩ (basis |x,0ᵗ⟩ 에서 W 역적용).  combo 마다 짧은
    // prep_combo† 만 적용 → per-combo 에서 W (긴 회로) 재적용 제거.
    //   ⟨x,0ᵗ|W·prep|0⟩ = conj(⟨0|prep†·W†|x,0ᵗ⟩) = conj(⟨0|prep†|η⟩).
    let mut eta = crate::ch_form::ChForm::new(ntot);
    for (q, &b) in x.iter().enumerate().take(n) {
        if b == 1 {
            eta.x_gate(q);
        }
    }
    for w in wops.iter().rev() {
        match *w {
            WOp::H(q) => eta.h_gate(q),
            WOp::S(q) => eta.sdg_gate(q), // S† = Sdg
            WOp::Sdg(q) => eta.s_gate(q),
            WOp::X(q) => eta.x_gate(q),
            WOp::Y(q) => eta.y_gate(q),
            WOp::Z(q) => eta.z_gate(q),
            WOp::Cnot(a, b) => eta.cx_gate(a, b), // CNOT† = CNOT
        }
    }
    let zero = vec![0u8; ntot];

    use rayon::prelude::*;
    let total: Complex64 = (0..(1u64 << u))
        .into_par_iter()
        .map(|mask| {
            let mut ps = eta.clone();
            let mut coeff = Complex64::new(1.0, 0.0);
            // prep_combo† : 각 unit 의 선택 옵션 prep 을 **역순·역연산** 으로 적용.
            for (ui, unit) in units.iter().enumerate() {
                let opt = &unit.options[((mask >> ui) & 1) as usize];
                coeff *= opt.coeff;
                let map = |l: u8| unit.ancillas[l as usize];
                for g in opt.prep.iter().rev() {
                    match *g {
                        PrepG::H(a) => ps.h_gate(map(a)),
                        PrepG::S(a) => ps.sdg_gate(map(a)), // S† = Sdg
                        PrepG::X(a) => ps.x_gate(map(a)),
                        PrepG::Cx(a, b) => ps.cx_gate(map(a), map(b)),
                    }
                }
            }
            // ⟨x,0ᵗ|W·prep|0⟩ = conj(⟨0|ps⟩).
            coeff * ps.amplitude(&zero).conj()
        })
        .sum();
    Complex64::new(sqrt2_t, 0.0) * total
}

fn apply_wops(ps: &mut crate::ch_form::ChForm, wops: &[WOp]) {
    for w in wops {
        match *w {
            WOp::H(q) => ps.h_gate(q),
            WOp::S(q) => ps.s_gate(q),
            WOp::Sdg(q) => ps.sdg_gate(q),
            WOp::X(q) => ps.x_gate(q),
            WOp::Y(q) => ps.y_gate(q),
            WOp::Z(q) => ps.z_gate(q),
            WOp::Cnot(a, b) => ps.cx_gate(a, b),
        }
    }
}

// ===================== 테스트용 dense statevector 레퍼런스 =====================

#[cfg(test)]
pub(crate) mod dense {
    use num_complex::Complex64;
    use std::f64::consts::FRAC_1_SQRT_2;

    /// 작은 N dense statevector 시뮬레이터 (테스트 전용).
    pub struct Dense {
        pub n: usize,
        pub amp: Vec<Complex64>,
    }
    impl Dense {
        pub fn new(n: usize) -> Self {
            let mut amp = vec![Complex64::new(0.0, 0.0); 1 << n];
            amp[0] = Complex64::new(1.0, 0.0);
            Dense { n, amp }
        }
        fn one_q(&mut self, q: usize, u: [[Complex64; 2]; 2]) {
            let step = 1usize << q;
            for base in 0..(1 << self.n) {
                if base & step == 0 {
                    let a0 = self.amp[base];
                    let a1 = self.amp[base | step];
                    self.amp[base] = u[0][0] * a0 + u[0][1] * a1;
                    self.amp[base | step] = u[1][0] * a0 + u[1][1] * a1;
                }
            }
        }
        pub fn h(&mut self, q: usize) {
            let s = Complex64::new(FRAC_1_SQRT_2, 0.0);
            self.one_q(q, [[s, s], [s, -s]]);
        }
        pub fn s(&mut self, q: usize) {
            self.one_q(
                q,
                [
                    [Complex64::new(1.0, 0.0), Complex64::new(0.0, 0.0)],
                    [Complex64::new(0.0, 0.0), Complex64::new(0.0, 1.0)],
                ],
            );
        }
        pub fn sdg(&mut self, q: usize) {
            self.one_q(
                q,
                [
                    [Complex64::new(1.0, 0.0), Complex64::new(0.0, 0.0)],
                    [Complex64::new(0.0, 0.0), Complex64::new(0.0, -1.0)],
                ],
            );
        }
        pub fn x(&mut self, q: usize) {
            let o = Complex64::new(1.0, 0.0);
            let z = Complex64::new(0.0, 0.0);
            self.one_q(q, [[z, o], [o, z]]);
        }
        pub fn y(&mut self, q: usize) {
            let i = Complex64::new(0.0, 1.0);
            let z = Complex64::new(0.0, 0.0);
            self.one_q(q, [[z, -i], [i, z]]);
        }
        pub fn z(&mut self, q: usize) {
            let o = Complex64::new(1.0, 0.0);
            let z = Complex64::new(0.0, 0.0);
            self.one_q(q, [[o, z], [z, -o]]);
        }
        pub fn sx(&mut self, q: usize) {
            let h = 0.5;
            self.one_q(
                q,
                [
                    [Complex64::new(h, h), Complex64::new(h, -h)],
                    [Complex64::new(h, -h), Complex64::new(h, h)],
                ],
            );
        }
        pub fn t(&mut self, q: usize) {
            self.one_q(
                q,
                [
                    [Complex64::new(1.0, 0.0), Complex64::new(0.0, 0.0)],
                    [
                        Complex64::new(0.0, 0.0),
                        Complex64::from_polar(1.0, std::f64::consts::FRAC_PI_4),
                    ],
                ],
            );
        }
        pub fn cnot(&mut self, c: usize, t: usize) {
            let cs = 1usize << c;
            let ts = 1usize << t;
            for base in 0..(1 << self.n) {
                if base & cs != 0 && base & ts == 0 {
                    self.amp.swap(base, base | ts);
                }
            }
        }
    }
}

#[cfg(test)]
mod amp_tests {
    use super::*;
    use crate::Tableau;
    use rand::rngs::StdRng;
    use rand::{Rng, SeedableRng};

    #[test]
    fn canonical_amplitude_matches_statevector_up_to_phase() {
        let mut rng = StdRng::seed_from_u64(99);
        for _trial in 0..200 {
            let n = rng.gen_range(1..7);
            let mut tab = Tableau::new(n);
            let mut d = dense::Dense::new(n);
            let depth = rng.gen_range(0..4 * n);
            for _ in 0..depth {
                match rng.gen_range(0..7) {
                    0 => {
                        let q = rng.gen_range(0..n);
                        tab.h(q);
                        d.h(q);
                    }
                    1 => {
                        let q = rng.gen_range(0..n);
                        tab.s(q);
                        d.s(q);
                    }
                    2 => {
                        let q = rng.gen_range(0..n);
                        tab.x_gate(q);
                        d.x(q);
                    }
                    3 => {
                        let q = rng.gen_range(0..n);
                        tab.z_gate(q);
                        d.z(q);
                    }
                    4 => {
                        let q = rng.gen_range(0..n);
                        tab.y_gate(q);
                        d.y(q);
                    }
                    5 => {
                        let q = rng.gen_range(0..n);
                        tab.sdg(q);
                        d.sdg(q);
                    }
                    _ => {
                        if n >= 2 {
                            let a = rng.gen_range(0..n);
                            let mut b = rng.gen_range(0..n);
                            while b == a {
                                b = rng.gen_range(0..n);
                            }
                            tab.cnot(a, b);
                            d.cnot(a, b);
                        }
                    }
                }
            }
            // 참조 위상 기준: |sv| 최대 인덱스.
            let dim = 1 << n;
            let mut ref_idx = 0;
            for i in 0..dim {
                if d.amp[i].norm() > d.amp[ref_idx].norm() {
                    ref_idx = i;
                }
            }
            let ref_bits: Vec<u8> = (0..n).map(|q| ((ref_idx >> q) & 1) as u8).collect();
            let canon_ref = stab_amplitude(&tab, &ref_bits);
            assert!(canon_ref.norm() > 1e-9);
            let global = d.amp[ref_idx] / canon_ref;
            for i in 0..dim {
                let bits: Vec<u8> = (0..n).map(|q| ((i >> q) & 1) as u8).collect();
                let got = stab_amplitude(&tab, &bits) * global;
                assert!(
                    (got - d.amp[i]).norm() < 1e-9,
                    "trial mismatch i={i} got={got} want={}",
                    d.amp[i]
                );
            }
        }
    }

    #[test]
    fn phase_stab_exact_global_phase() {
        // PhaseStab 의 amplitude 가 전역 위상까지 statevector 와 정확히 일치.
        let mut rng = StdRng::seed_from_u64(7);
        for _trial in 0..200 {
            let n = rng.gen_range(1..7);
            let mut ps = PhaseStab::new(n);
            let mut d = dense::Dense::new(n);
            let depth = rng.gen_range(0..4 * n);
            for _ in 0..depth {
                match rng.gen_range(0..7) {
                    0 => {
                        let q = rng.gen_range(0..n);
                        ps.h(q);
                        d.h(q);
                    }
                    1 => {
                        let q = rng.gen_range(0..n);
                        ps.s(q);
                        d.s(q);
                    }
                    2 => {
                        let q = rng.gen_range(0..n);
                        ps.sx(q);
                        d.sx(q);
                    }
                    3 => {
                        let q = rng.gen_range(0..n);
                        ps.z(q);
                        d.z(q);
                    }
                    4 => {
                        let q = rng.gen_range(0..n);
                        ps.y(q);
                        d.y(q);
                    }
                    5 => {
                        let q = rng.gen_range(0..n);
                        ps.sdg(q);
                        d.sdg(q);
                    }
                    _ => {
                        if n >= 2 {
                            let a = rng.gen_range(0..n);
                            let mut b = rng.gen_range(0..n);
                            while b == a {
                                b = rng.gen_range(0..n);
                            }
                            ps.cnot(a, b);
                            d.cnot(a, b);
                        }
                    }
                }
            }
            for i in 0..(1 << n) {
                let bits: Vec<u8> = (0..n).map(|q| ((i >> q) & 1) as u8).collect();
                let got = ps.amplitude(&bits);
                assert!(
                    (got - d.amp[i]).norm() < 1e-9,
                    "i={i} got={got} want={}",
                    d.amp[i]
                );
            }
        }
    }

    #[test]
    fn fast_matches_reference_and_statevector() {
        // 최적화 fast 경로가 reference + statevector 와 정확히 일치 (전역 위상 포함).
        let mut rng = StdRng::seed_from_u64(555);
        for _trial in 0..200 {
            let n = rng.gen_range(1..6);
            let mut gates = Vec::new();
            let mut d = dense::Dense::new(n);
            let depth = rng.gen_range(0..5 * n);
            let mut t_count = 0;
            for _ in 0..depth {
                match rng.gen_range(0..7) {
                    0 => {
                        let q = rng.gen_range(0..n);
                        gates.push(CtGate::H(q));
                        d.h(q);
                    }
                    1 => {
                        let q = rng.gen_range(0..n);
                        gates.push(CtGate::S(q));
                        d.s(q);
                    }
                    2 => {
                        let q = rng.gen_range(0..n);
                        if t_count < 8 {
                            gates.push(CtGate::T(q));
                            d.t(q);
                            t_count += 1;
                        }
                    }
                    3 => {
                        let q = rng.gen_range(0..n);
                        gates.push(CtGate::Sx(q));
                        d.sx(q);
                    }
                    4 => {
                        let q = rng.gen_range(0..n);
                        gates.push(CtGate::Z(q));
                        d.z(q);
                    }
                    5 => {
                        let q = rng.gen_range(0..n);
                        gates.push(CtGate::Y(q));
                        d.y(q);
                    }
                    _ => {
                        if n >= 2 {
                            let a = rng.gen_range(0..n);
                            let mut b = rng.gen_range(0..n);
                            while b == a {
                                b = rng.gen_range(0..n);
                            }
                            gates.push(CtGate::Cnot(a, b));
                            d.cnot(a, b);
                        }
                    }
                }
            }
            for i in 0..(1 << n) {
                let bits: Vec<u8> = (0..n).map(|q| ((i >> q) & 1) as u8).collect();
                let fast = clifford_t_amplitude_fast(n, &gates, &bits);
                let refv = clifford_t_amplitude(n, &gates, &bits);
                assert!(
                    (fast - refv).norm() < 1e-9,
                    "fast vs ref n={n} i={i} fast={fast} ref={refv}"
                );
                assert!(
                    (fast - d.amp[i]).norm() < 1e-9,
                    "fast vs sv n={n} i={i} fast={fast} sv={}",
                    d.amp[i]
                );
            }
        }
    }

    #[test]
    fn expectation_matches_statevector() {
        // ⟨ψ|P|ψ⟩ (near-Clifford) == statevector 기댓값.
        let mut rng = StdRng::seed_from_u64(321);
        for _trial in 0..120 {
            let n = rng.gen_range(1..5);
            let mut gates = Vec::new();
            let mut d = dense::Dense::new(n);
            let depth = rng.gen_range(0..4 * n);
            let mut t_count = 0;
            for _ in 0..depth {
                match rng.gen_range(0..6) {
                    0 => {
                        let q = rng.gen_range(0..n);
                        gates.push(CtGate::H(q));
                        d.h(q);
                    }
                    1 => {
                        let q = rng.gen_range(0..n);
                        gates.push(CtGate::S(q));
                        d.s(q);
                    }
                    2 => {
                        let q = rng.gen_range(0..n);
                        if t_count < 5 {
                            gates.push(CtGate::T(q));
                            d.t(q);
                            t_count += 1;
                        }
                    }
                    3 => {
                        let q = rng.gen_range(0..n);
                        gates.push(CtGate::Sx(q));
                        d.sx(q);
                    }
                    _ => {
                        if n >= 2 {
                            let a = rng.gen_range(0..n);
                            let mut b = rng.gen_range(0..n);
                            while b == a {
                                b = rng.gen_range(0..n);
                            }
                            gates.push(CtGate::Cnot(a, b));
                            d.cnot(a, b);
                        }
                    }
                }
            }
            // 랜덤 Pauli 문자열.
            let mut px = vec![false; n];
            let mut pz = vec![false; n];
            for q in 0..n {
                match rng.gen_range(0..4) {
                    1 => px[q] = true, // X
                    2 => {
                        px[q] = true;
                        pz[q] = true;
                    } // Y
                    3 => pz[q] = true, // Z
                    _ => {}
                }
            }
            let got = clifford_t_expectation(n, &gates, &px, &pz);
            // statevector 기댓값: ⟨ψ|P|ψ⟩ = Σ_x conj(ψ_x) (P ψ)_x.
            let dim = 1 << n;
            let mut pe = Complex64::new(0.0, 0.0);
            for x in 0..dim {
                // (P|x⟩) = i^{#Y on set} ... compute P|x⟩ basis + phase.
                let mut y = x;
                let mut ph = Complex64::new(1.0, 0.0);
                for q in 0..n {
                    let bit = (x >> q) & 1;
                    if pz[q] && bit == 1 {
                        ph = -ph; // Z
                    }
                    if px[q] {
                        y ^= 1 << q; // X flips
                    }
                    if px[q] && pz[q] {
                        // Y = iXZ: Z then X with factor i
                        ph *= Complex64::new(0.0, 1.0);
                    }
                }
                // P|x⟩ = ph|y⟩ → ⟨y|P|x⟩=ph → ⟨ψ|P|ψ⟩ 항 = conj(ψ_y)·ph·ψ_x.
                pe += d.amp[y].conj() * ph * d.amp[x];
            }
            assert!(
                (got - pe).norm() < 1e-9,
                "n={n} t={t_count} got={got} want={pe} gates={gates:?} px={px:?} pz={pz:?}"
            );
        }
    }

    #[test]
    fn lowrank_matches_fast_and_statevector() {
        // Bravyi–Gosset 저-rank (2^{t/2}) == fast (2^t) == statevector.
        let mut rng = StdRng::seed_from_u64(8675);
        for _trial in 0..120 {
            let n = rng.gen_range(1..5);
            let mut gates = Vec::new();
            let mut d = dense::Dense::new(n);
            let depth = rng.gen_range(0..5 * n);
            let mut t_count = 0;
            for _ in 0..depth {
                match rng.gen_range(0..7) {
                    0 => {
                        let q = rng.gen_range(0..n);
                        gates.push(CtGate::H(q));
                        d.h(q);
                    }
                    1 => {
                        let q = rng.gen_range(0..n);
                        gates.push(CtGate::S(q));
                        d.s(q);
                    }
                    2 => {
                        let q = rng.gen_range(0..n);
                        if t_count < 7 {
                            gates.push(CtGate::T(q));
                            d.t(q);
                            t_count += 1;
                        }
                    }
                    3 => {
                        let q = rng.gen_range(0..n);
                        gates.push(CtGate::Sx(q));
                        d.sx(q);
                    }
                    4 => {
                        // Tdg
                        let q = rng.gen_range(0..n);
                        if t_count < 7 {
                            gates.push(CtGate::Tdg(q));
                            // dense Tdg = T^7
                            for _ in 0..7 {
                                d.t(q);
                            }
                            t_count += 1;
                        }
                    }
                    5 => {
                        let q = rng.gen_range(0..n);
                        gates.push(CtGate::Z(q));
                        d.z(q);
                    }
                    _ => {
                        if n >= 2 {
                            let a = rng.gen_range(0..n);
                            let mut b = rng.gen_range(0..n);
                            while b == a {
                                b = rng.gen_range(0..n);
                            }
                            gates.push(CtGate::Cnot(a, b));
                            d.cnot(a, b);
                        }
                    }
                }
            }
            for i in 0..(1 << n) {
                let bits: Vec<u8> = (0..n).map(|q| ((i >> q) & 1) as u8).collect();
                let lr = clifford_t_amplitude_lowrank(n, &gates, &bits);
                let fast = clifford_t_amplitude_fast(n, &gates, &bits);
                assert!(
                    (lr - fast).norm() < 1e-9,
                    "lowrank vs fast n={n} t={t_count} i={i} lr={lr} fast={fast}"
                );
                assert!(
                    (lr - d.amp[i]).norm() < 1e-9,
                    "lowrank vs sv n={n} i={i} lr={lr} sv={}",
                    d.amp[i]
                );
            }
        }
    }

    #[test]
    fn metropolis_sampling_converges_to_distribution() {
        // Metropolis 샘플 경험분포가 정확 |ψ|² (statevector) 로 수렴 (TVD 작음).
        let mut rng = StdRng::seed_from_u64(31);
        for _trial in 0..8 {
            let n = rng.gen_range(2..5);
            let mut gates = Vec::new();
            let mut d = dense::Dense::new(n);
            let mut t_count = 0;
            for _ in 0..(4 * n) {
                match rng.gen_range(0..5) {
                    0 => {
                        let q = rng.gen_range(0..n);
                        gates.push(CtGate::H(q));
                        d.h(q);
                    }
                    1 => {
                        let q = rng.gen_range(0..n);
                        gates.push(CtGate::S(q));
                        d.s(q);
                    }
                    2 => {
                        let q = rng.gen_range(0..n);
                        if t_count < 4 {
                            gates.push(CtGate::T(q));
                            d.t(q);
                            t_count += 1;
                        }
                    }
                    _ => {
                        let a = rng.gen_range(0..n);
                        let mut b = rng.gen_range(0..n);
                        while b == a {
                            b = rng.gen_range(0..n);
                        }
                        gates.push(CtGate::Cnot(a, b));
                        d.cnot(a, b);
                    }
                }
            }
            let dim = 1 << n;
            let exact: Vec<f64> = (0..dim).map(|i| d.amp[i].norm_sqr()).collect();
            let norm: f64 = exact.iter().sum();
            let exact: Vec<f64> = exact.iter().map(|p| p / norm).collect();
            // 충분한 샘플 + burn-in.
            let shots = 40000;
            let samples = clifford_t_sample(n, &gates, shots, 2000, 2, 4, Some(7));
            let mut emp = vec![0.0f64; dim];
            for s in &samples {
                let idx: usize = (0..n).filter(|&q| s[q] == 1).map(|q| 1 << q).sum();
                emp[idx] += 1.0 / shots as f64;
            }
            let tvd: f64 = (0..dim).map(|i| (emp[i] - exact[i]).abs()).sum::<f64>() * 0.5;
            assert!(tvd < 0.05, "n={n} t={t_count} TVD={tvd}");
        }
    }

    #[test]
    fn multichain_diagnostic_and_multimodal() {
        // 두 GHZ 블록 → 4개 분리 모드 (00..0, 0..01..1, 1..10..0, 11..1) 의
        // 다봉 분포.  다중 체인이 모든 모드를 덮고, 수렴 시 R̂≈1 인지 확인.
        let half = 3;
        let n = 2 * half;
        let mut gates = Vec::new();
        // 블록 1: 큐비트 0..half GHZ.
        gates.push(CtGate::H(0));
        for q in 0..(half - 1) {
            gates.push(CtGate::Cnot(q, q + 1));
        }
        // 블록 2: 큐비트 half..n GHZ.
        gates.push(CtGate::H(half));
        for q in half..(n - 1) {
            gates.push(CtGate::Cnot(q, q + 1));
        }
        let (samples, r_hat) =
            clifford_t_sample_diagnostic(n, &gates, 40000, 2000, 2, 8, Some(123));
        // 4개 모드 모두 출현하고 대략 균등 (각 ~25%).
        use std::collections::HashMap;
        let mut counts: HashMap<Vec<u8>, usize> = HashMap::new();
        for s in &samples {
            *counts.entry(s.clone()).or_insert(0) += 1;
        }
        let modes = [
            vec![0u8; n],
            {
                let mut v = vec![0u8; n];
                (half..n).for_each(|q| v[q] = 1);
                v
            },
            {
                let mut v = vec![0u8; n];
                (0..half).for_each(|q| v[q] = 1);
                v
            },
            vec![1u8; n],
        ];
        for m in &modes {
            let c = *counts.get(m).unwrap_or(&0);
            let frac = c as f64 / samples.len() as f64;
            assert!(frac > 0.15 && frac < 0.35, "mode {m:?} frac={frac}");
        }
        // support 밖 (지지집합 아닌) 상태는 없어야 함.
        assert_eq!(counts.len(), 4, "unexpected modes: {:?}", counts.keys());
        // R̂ 수렴.
        let r = r_hat.expect("multi-chain → R̂ should exist");
        assert!(r < 1.1, "R̂={r} (수렴 안 됨)");
    }

    #[test]
    fn clifford_t_amplitude_exact() {
        // Clifford+T 회로의 amplitude 가 statevector 와 정확히 일치 (전역 위상 포함).
        let mut rng = StdRng::seed_from_u64(2024);
        for _trial in 0..150 {
            let n = rng.gen_range(1..6);
            let mut gates = Vec::new();
            let mut d = dense::Dense::new(n);
            let depth = rng.gen_range(0..5 * n);
            let mut t_count = 0;
            for _ in 0..depth {
                match rng.gen_range(0..6) {
                    0 => {
                        let q = rng.gen_range(0..n);
                        gates.push(CtGate::H(q));
                        d.h(q);
                    }
                    1 => {
                        let q = rng.gen_range(0..n);
                        gates.push(CtGate::S(q));
                        d.s(q);
                    }
                    2 => {
                        let q = rng.gen_range(0..n);
                        if t_count < 7 {
                            gates.push(CtGate::T(q));
                            d.t(q);
                            t_count += 1;
                        }
                    }
                    3 => {
                        let q = rng.gen_range(0..n);
                        gates.push(CtGate::X(q));
                        d.x(q);
                    }
                    4 => {
                        let q = rng.gen_range(0..n);
                        gates.push(CtGate::Sx(q));
                        d.sx(q);
                    }
                    _ => {
                        if n >= 2 {
                            let a = rng.gen_range(0..n);
                            let mut b = rng.gen_range(0..n);
                            while b == a {
                                b = rng.gen_range(0..n);
                            }
                            gates.push(CtGate::Cnot(a, b));
                            d.cnot(a, b);
                        }
                    }
                }
            }
            for i in 0..(1 << n) {
                let bits: Vec<u8> = (0..n).map(|q| ((i >> q) & 1) as u8).collect();
                let got = clifford_t_amplitude(n, &gates, &bits);
                assert!(
                    (got - d.amp[i]).norm() < 1e-9,
                    "n={n} t={t_count} i={i} got={got} want={}",
                    d.amp[i]
                );
            }
        }
    }
}

#[cfg(test)]
mod gauss_tests {
    // 대칭 2D 계수 행렬 coup[i][j] 의 인덱스 접근 (검증용 brute-force) — iterator
    // 형태가 오히려 가독성을 해쳐 range-loop 를 허용.
    #![allow(clippy::needless_range_loop)]
    use super::*;

    /// brute-force Gauss sum (2^m 합) — 검증용.
    fn brute(lin: &[u8], coup: &[Vec<u8>]) -> Complex64 {
        let m = lin.len();
        let mut acc = Complex64::new(0.0, 0.0);
        for mask in 0..(1u64 << m) {
            let y: Vec<u8> = (0..m).map(|i| ((mask >> i) & 1) as u8).collect();
            let mut q: i64 = 0;
            for i in 0..m {
                q += (lin[i] as i64) * (y[i] as i64);
            }
            for i in 0..m {
                for j in (i + 1)..m {
                    q += 2 * (coup[i][j] as i64) * (y[i] as i64) * (y[j] as i64);
                }
            }
            let qm = q.rem_euclid(4) as f64;
            acc += Complex64::from_polar(1.0, qm * std::f64::consts::FRAC_PI_2);
        }
        acc
    }

    #[test]
    fn gauss_matches_brute_random() {
        use rand::rngs::StdRng;
        use rand::{Rng, SeedableRng};
        let mut rng = StdRng::seed_from_u64(12345);
        for _trial in 0..3000 {
            let m = rng.gen_range(0..9);
            let lin: Vec<u8> = (0..m).map(|_| rng.gen_range(0..4)).collect();
            let mut coup = vec![vec![0u8; m]; m];
            for i in 0..m {
                for j in (i + 1)..m {
                    let b = rng.gen_range(0..2);
                    coup[i][j] = b;
                    coup[j][i] = b;
                }
            }
            let fast = gauss_sum(&lin, &coup);
            let slow = brute(&lin, &coup);
            assert!(
                (fast - slow).norm() < 1e-9,
                "m={m} lin={lin:?} coup={coup:?} fast={fast} slow={slow}"
            );
        }
    }
}
