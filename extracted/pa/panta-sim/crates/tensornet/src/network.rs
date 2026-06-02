//! 회로 → tensor network 변환.
//!
//! 각 큐비트는 시간축을 따라 "frontier" 인덱스를 가진다.  초기 |0⟩ 텐서에서
//! 시작해 게이트마다 입력 leg = 현재 frontier, 출력 leg = 새 라벨로 텐서를
//! 추가한다.  amplitude `⟨x|C|0⟩` 는 출력 frontier 를 `⟨x_q|` 로 cap 하면
//! 스칼라로 수축되고, statevector 는 출력 frontier 를 열어 둔다.
//!
//! 행렬 컨벤션: k-큐비트 게이트 행렬은 `2^k × 2^k` row-major 이고 `qubits[0]`
//! 이 행렬 인덱스의 **MSB** (big-endian over the qubit list).  게이트 텐서의
//! 축 순서는 `[out_0…out_{k-1}, in_0…in_{k-1}]` (각 `p` 가 `qubits[p]`).

use num_complex::Complex64;

use crate::tensor::Tensor;

/// 단일 게이트 연산: `2^k × 2^k` row-major unitary + 작용 큐비트.
#[derive(Debug, Clone)]
pub struct GateOp {
    /// `2^k × 2^k` row-major 행렬 (`qubits[0]` = MSB).
    pub matrix: Vec<Complex64>,
    /// 작용 큐비트 (전역 인덱스).
    pub qubits: Vec<usize>,
}

impl GateOp {
    pub fn new(matrix: Vec<Complex64>, qubits: Vec<usize>) -> Self {
        let k = qubits.len();
        debug_assert_eq!(matrix.len(), 1 << (2 * k));
        GateOp { matrix, qubits }
    }
}

/// 회로의 tensor network 표현 (수축 전).
#[derive(Debug, Clone)]
pub struct CircuitNetwork {
    pub tensors: Vec<Tensor>,
    /// statevector 모드에서 열린 출력 인덱스 (큐비트 순서).  amplitude 모드는 빈
    /// 벡터.
    pub open_indices: Vec<usize>,
    pub n_qubits: usize,
}

struct Builder {
    tensors: Vec<Tensor>,
    frontier: Vec<usize>,
    next_label: usize,
}

impl Builder {
    fn new(n_qubits: usize) -> Self {
        // 초기 frontier 라벨 = 0..n.  |0⟩ 텐서를 추가.
        let frontier: Vec<usize> = (0..n_qubits).collect();
        let tensors: Vec<Tensor> = (0..n_qubits)
            .map(|q| {
                Tensor::new(
                    vec![q],
                    vec![2],
                    vec![Complex64::new(1.0, 0.0), Complex64::new(0.0, 0.0)],
                )
            })
            .collect();
        Builder {
            tensors,
            frontier,
            next_label: n_qubits,
        }
    }

    fn fresh(&mut self) -> usize {
        let l = self.next_label;
        self.next_label += 1;
        l
    }

    fn apply(&mut self, op: &GateOp) {
        let k = op.qubits.len();
        // out legs = 새 라벨, in legs = 현재 frontier.
        let in_legs: Vec<usize> = op.qubits.iter().map(|&q| self.frontier[q]).collect();
        let out_legs: Vec<usize> = (0..k).map(|_| self.fresh()).collect();
        // 게이트 텐서 축 = [out…, in…]; data = 행렬 그대로 (row-major).
        let mut indices = out_legs.clone();
        indices.extend_from_slice(&in_legs);
        let dims = vec![2usize; 2 * k];
        self.tensors
            .push(Tensor::new(indices, dims, op.matrix.clone()));
        // frontier 갱신.
        for (p, &q) in op.qubits.iter().enumerate() {
            self.frontier[q] = out_legs[p];
        }
    }
}

/// amplitude `⟨bitstring|C|0…0⟩` 네트워크.  `bitstring[q]` = 큐비트 `q` 의 측정값.
pub fn build_amplitude_network(
    n_qubits: usize,
    ops: &[GateOp],
    bitstring: &[u8],
) -> CircuitNetwork {
    assert_eq!(bitstring.len(), n_qubits);
    let mut b = Builder::new(n_qubits);
    for op in ops {
        b.apply(op);
    }
    // 출력 frontier 를 ⟨x_q| 로 cap.
    for (q, &bit) in bitstring.iter().enumerate() {
        let cap = if bit == 0 {
            vec![Complex64::new(1.0, 0.0), Complex64::new(0.0, 0.0)]
        } else {
            vec![Complex64::new(0.0, 0.0), Complex64::new(1.0, 0.0)]
        };
        b.tensors
            .push(Tensor::new(vec![b.frontier[q]], vec![2], cap));
    }
    CircuitNetwork {
        tensors: b.tensors,
        open_indices: vec![],
        n_qubits,
    }
}

/// 전체 statevector 네트워크 (출력 frontier 를 열어 둠).  `open_indices[q]` =
/// 큐비트 `q` 의 출력 인덱스 라벨.  작은 N 에서만 실용적.
pub fn build_statevector_network(n_qubits: usize, ops: &[GateOp]) -> CircuitNetwork {
    let mut b = Builder::new(n_qubits);
    for op in ops {
        b.apply(op);
    }
    let open: Vec<usize> = b.frontier.clone();
    CircuitNetwork {
        tensors: b.tensors,
        open_indices: open,
        n_qubits,
    }
}
