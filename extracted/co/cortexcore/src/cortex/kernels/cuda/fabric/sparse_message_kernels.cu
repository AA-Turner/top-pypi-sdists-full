#include <cuda.h>
#include <cuda_runtime.h>
#include <torch/extension.h>

#include <cmath>
#include <limits>
#include <vector>

namespace {

inline void check_cuda_tensor(const at::Tensor &tensor, const char *name) {
  TORCH_CHECK(tensor.is_cuda(), name, " must be a CUDA tensor");
  TORCH_CHECK(tensor.is_contiguous(), name, " must be contiguous");
}

inline void check_launch(const char *name) {
  const cudaError_t err = cudaGetLastError();
  TORCH_CHECK(err == cudaSuccess, name, " launch failed: ",
              cudaGetErrorString(err));
}

__global__ void fabric_sparse_message_forward_kernel(
    const float *__restrict__ q, const float *__restrict__ k_all,
    const float *__restrict__ v_all, const int64_t *__restrict__ neighbor_idx,
    const bool *__restrict__ neighbor_valid,
    const float *__restrict__ edge_distance,
    const int64_t *__restrict__ edge_delay, const int64_t *__restrict__ step_flat,
    float *__restrict__ out, int BT, int R, int S, int M, int d_k, int d_v,
    float inv_sqrt_dk, float distance_scale, bool use_delay) {
  const int bt = blockIdx.x;
  const int recv = blockIdx.y;
  const int tid = threadIdx.x;
  if (bt >= BT || recv >= R) {
    return;
  }

  extern __shared__ float shared[];
  float *logits = shared;
  float *weights = shared + M;

  const int neighbor_base = recv * M;
  const int step_value = use_delay ? static_cast<int>(step_flat[bt]) : 0;
  if (tid == 0) {
    float max_logit = -std::numeric_limits<float>::infinity();
    for (int edge = 0; edge < M; ++edge) {
      const int edge_idx = neighbor_base + edge;
      const bool valid = neighbor_valid[edge_idx] &&
                         (!use_delay ||
                          static_cast<int>(edge_delay[edge_idx]) <= step_value);
      if (!valid) {
        logits[edge] = -std::numeric_limits<float>::infinity();
        weights[edge] = 0.0f;
        continue;
      }
      const int send = static_cast<int>(neighbor_idx[edge_idx]);
      const int q_offset = recv * d_k;
      const int k_offset = (bt * S + send) * d_k;
      float dot = 0.0f;
      for (int d = 0; d < d_k; ++d) {
        dot += q[q_offset + d] * k_all[k_offset + d];
      }
      const float logit = dot * inv_sqrt_dk - distance_scale * edge_distance[edge_idx];
      logits[edge] = logit;
      max_logit = logit > max_logit ? logit : max_logit;
    }

    if (!isfinite(max_logit)) {
      for (int edge = 0; edge < M; ++edge) {
        weights[edge] = 0.0f;
      }
    } else {
      float sum = 0.0f;
      for (int edge = 0; edge < M; ++edge) {
        const float weight = isfinite(logits[edge]) ? expf(logits[edge] - max_logit) : 0.0f;
        weights[edge] = weight;
        sum += weight;
      }
      const float inv_sum = sum > 0.0f ? 1.0f / sum : 0.0f;
      for (int edge = 0; edge < M; ++edge) {
        weights[edge] *= inv_sum;
      }
    }
  }
  __syncthreads();

  const int out_offset = (bt * R + recv) * d_v;
  for (int d = tid; d < d_v; d += blockDim.x) {
    float acc = 0.0f;
    for (int edge = 0; edge < M; ++edge) {
      const float weight = weights[edge];
      if (weight == 0.0f) {
        continue;
      }
      const int send = static_cast<int>(neighbor_idx[neighbor_base + edge]);
      acc += weight * v_all[(bt * S + send) * d_v + d];
    }
    out[out_offset + d] = acc;
  }
}

__global__ void fabric_sparse_message_backward_kernel(
    const float *__restrict__ grad_msg, const float *__restrict__ q,
    const float *__restrict__ k_all, const float *__restrict__ v_all,
    const int64_t *__restrict__ neighbor_idx,
    const bool *__restrict__ neighbor_valid,
    const float *__restrict__ edge_distance,
    const int64_t *__restrict__ edge_delay, const int64_t *__restrict__ step_flat,
    float *__restrict__ grad_q, float *__restrict__ grad_k,
    float *__restrict__ grad_v, int BT, int R, int S, int M, int d_k, int d_v,
    float inv_sqrt_dk, float distance_scale, bool use_delay) {
  const int bt = blockIdx.x;
  const int recv = blockIdx.y;
  const int tid = threadIdx.x;
  if (bt >= BT || recv >= R) {
    return;
  }

  extern __shared__ float shared[];
  float *logits = shared;
  float *weights = shared + M;
  float *dweight = shared + (2 * M);
  float *dlogit = shared + (3 * M);

  const int neighbor_base = recv * M;
  const int step_value = use_delay ? static_cast<int>(step_flat[bt]) : 0;
  if (tid == 0) {
    float max_logit = -std::numeric_limits<float>::infinity();
    for (int edge = 0; edge < M; ++edge) {
      const int edge_idx = neighbor_base + edge;
      const bool valid = neighbor_valid[edge_idx] &&
                         (!use_delay ||
                          static_cast<int>(edge_delay[edge_idx]) <= step_value);
      if (!valid) {
        logits[edge] = -std::numeric_limits<float>::infinity();
        weights[edge] = 0.0f;
        dweight[edge] = 0.0f;
        dlogit[edge] = 0.0f;
        continue;
      }
      const int send = static_cast<int>(neighbor_idx[edge_idx]);
      const int q_offset = recv * d_k;
      const int k_offset = (bt * S + send) * d_k;
      float dot = 0.0f;
      for (int d = 0; d < d_k; ++d) {
        dot += q[q_offset + d] * k_all[k_offset + d];
      }
      const float logit = dot * inv_sqrt_dk - distance_scale * edge_distance[edge_idx];
      logits[edge] = logit;
      max_logit = logit > max_logit ? logit : max_logit;
    }

    if (!isfinite(max_logit)) {
      for (int edge = 0; edge < M; ++edge) {
        weights[edge] = 0.0f;
        dweight[edge] = 0.0f;
        dlogit[edge] = 0.0f;
      }
    } else {
      float sum = 0.0f;
      for (int edge = 0; edge < M; ++edge) {
        const float weight = isfinite(logits[edge]) ? expf(logits[edge] - max_logit) : 0.0f;
        weights[edge] = weight;
        sum += weight;
      }
      const float inv_sum = sum > 0.0f ? 1.0f / sum : 0.0f;
      float weighted_sum = 0.0f;
      const int grad_offset = (bt * R + recv) * d_v;
      for (int edge = 0; edge < M; ++edge) {
        weights[edge] *= inv_sum;
        if (weights[edge] == 0.0f) {
          dweight[edge] = 0.0f;
          continue;
        }
        const int send = static_cast<int>(neighbor_idx[neighbor_base + edge]);
        const int v_offset = (bt * S + send) * d_v;
        float dot = 0.0f;
        for (int d = 0; d < d_v; ++d) {
          dot += grad_msg[grad_offset + d] * v_all[v_offset + d];
        }
        dweight[edge] = dot;
        weighted_sum += weights[edge] * dot;
      }
      for (int edge = 0; edge < M; ++edge) {
        dlogit[edge] = weights[edge] * (dweight[edge] - weighted_sum);
      }
    }
  }
  __syncthreads();

  const int grad_offset = (bt * R + recv) * d_v;
  for (int d = tid; d < d_v; d += blockDim.x) {
    const float grad_out = grad_msg[grad_offset + d];
    for (int edge = 0; edge < M; ++edge) {
      const float weight = weights[edge];
      if (weight == 0.0f) {
        continue;
      }
      const int send = static_cast<int>(neighbor_idx[neighbor_base + edge]);
      atomicAdd(&grad_v[(bt * S + send) * d_v + d], weight * grad_out);
    }
  }

  for (int d = tid; d < d_k; d += blockDim.x) {
    const float q_val = q[recv * d_k + d];
    float recv_grad = 0.0f;
    for (int edge = 0; edge < M; ++edge) {
      const float dl = dlogit[edge];
      if (dl == 0.0f) {
        continue;
      }
      const int send = static_cast<int>(neighbor_idx[neighbor_base + edge]);
      const float scaled = dl * inv_sqrt_dk;
      atomicAdd(&grad_k[(bt * S + send) * d_k + d], scaled * q_val);
      recv_grad += scaled * k_all[(bt * S + send) * d_k + d];
    }
    atomicAdd(&grad_q[recv * d_k + d], recv_grad);
  }
}

} // namespace

std::vector<at::Tensor> fabric_sparse_message_forward_cuda(
    at::Tensor q, at::Tensor k_all, at::Tensor v_all, at::Tensor neighbor_idx,
    at::Tensor neighbor_valid, at::Tensor edge_distance, at::Tensor edge_delay,
    at::Tensor step_flat, double distance_scale, bool use_delay) {
  check_cuda_tensor(q, "q");
  check_cuda_tensor(k_all, "k_all");
  check_cuda_tensor(v_all, "v_all");
  check_cuda_tensor(neighbor_idx, "neighbor_idx");
  check_cuda_tensor(neighbor_valid, "neighbor_valid");
  check_cuda_tensor(edge_distance, "edge_distance");
  check_cuda_tensor(edge_delay, "edge_delay");
  check_cuda_tensor(step_flat, "step_flat");
  TORCH_CHECK(q.scalar_type() == at::kFloat, "q must be float32");
  TORCH_CHECK(k_all.scalar_type() == at::kFloat, "k_all must be float32");
  TORCH_CHECK(v_all.scalar_type() == at::kFloat, "v_all must be float32");
  TORCH_CHECK(edge_distance.scalar_type() == at::kFloat,
              "edge_distance must be float32");
  TORCH_CHECK(q.dim() == 2, "q must have shape [N, d_k]");
  TORCH_CHECK(k_all.dim() == 3, "k_all must have shape [BT, N, d_k]");
  TORCH_CHECK(v_all.dim() == 3, "v_all must have shape [BT, N, d_v]");
  TORCH_CHECK(neighbor_idx.dim() == 2,
              "neighbor_idx must have shape [N, M]");
  TORCH_CHECK(neighbor_valid.sizes() == neighbor_idx.sizes(),
              "neighbor_valid must match neighbor_idx shape");
  TORCH_CHECK(edge_distance.sizes() == neighbor_idx.sizes(),
              "edge_distance must match neighbor_idx shape");
  TORCH_CHECK(edge_delay.sizes() == neighbor_idx.sizes(),
              "edge_delay must match neighbor_idx shape");
  TORCH_CHECK(step_flat.dim() == 1, "step_flat must have shape [BT]");
  TORCH_CHECK(k_all.size(0) == step_flat.size(0),
              "step_flat length must equal BT");
  TORCH_CHECK(q.size(0) == neighbor_idx.size(0),
              "q and neighbor_idx must agree on receiver count");
  TORCH_CHECK(k_all.size(1) == v_all.size(1),
              "k_all and v_all must agree on sender count");
  TORCH_CHECK(q.size(1) == k_all.size(2),
              "q and k_all must agree on d_k");

  const int BT = static_cast<int>(k_all.size(0));
  const int R = static_cast<int>(q.size(0));
  const int S = static_cast<int>(k_all.size(1));
  const int M = static_cast<int>(neighbor_idx.size(1));
  const int d_k = static_cast<int>(q.size(1));
  const int d_v = static_cast<int>(v_all.size(2));
  auto out = at::zeros({BT, R, d_v}, v_all.options());

  const dim3 grid(BT, R);
  const int threads = 32;
  const size_t shared_bytes = static_cast<size_t>(2 * M) * sizeof(float);
  fabric_sparse_message_forward_kernel<<<grid, threads, shared_bytes>>>(
      q.data_ptr<float>(), k_all.data_ptr<float>(), v_all.data_ptr<float>(),
      neighbor_idx.data_ptr<int64_t>(), neighbor_valid.data_ptr<bool>(),
      edge_distance.data_ptr<float>(), edge_delay.data_ptr<int64_t>(),
      step_flat.data_ptr<int64_t>(), out.data_ptr<float>(), BT, R, S, M, d_k, d_v,
      1.0f / std::sqrt(static_cast<float>(d_k)),
      static_cast<float>(distance_scale), use_delay);
  check_launch("fabric_sparse_message_forward_kernel");
  return {out};
}

std::vector<at::Tensor> fabric_sparse_message_backward_cuda(
    at::Tensor grad_msg, at::Tensor q, at::Tensor k_all, at::Tensor v_all,
    at::Tensor neighbor_idx, at::Tensor neighbor_valid, at::Tensor edge_distance,
    at::Tensor edge_delay, at::Tensor step_flat, double distance_scale,
    bool use_delay) {
  check_cuda_tensor(grad_msg, "grad_msg");
  check_cuda_tensor(q, "q");
  check_cuda_tensor(k_all, "k_all");
  check_cuda_tensor(v_all, "v_all");
  check_cuda_tensor(neighbor_idx, "neighbor_idx");
  check_cuda_tensor(neighbor_valid, "neighbor_valid");
  check_cuda_tensor(edge_distance, "edge_distance");
  check_cuda_tensor(edge_delay, "edge_delay");
  check_cuda_tensor(step_flat, "step_flat");
  TORCH_CHECK(grad_msg.scalar_type() == at::kFloat,
              "grad_msg must be float32");
  TORCH_CHECK(q.scalar_type() == at::kFloat, "q must be float32");
  TORCH_CHECK(k_all.scalar_type() == at::kFloat, "k_all must be float32");
  TORCH_CHECK(v_all.scalar_type() == at::kFloat, "v_all must be float32");

  TORCH_CHECK(q.dim() == 2, "q must have shape [R, d_k]");
  TORCH_CHECK(k_all.dim() == 3, "k_all must have shape [BT, S, d_k]");
  TORCH_CHECK(v_all.dim() == 3, "v_all must have shape [BT, S, d_v]");
  TORCH_CHECK(neighbor_idx.dim() == 2,
              "neighbor_idx must have shape [R, M]");
  TORCH_CHECK(neighbor_valid.sizes() == neighbor_idx.sizes(),
              "neighbor_valid must match neighbor_idx shape");
  TORCH_CHECK(edge_distance.sizes() == neighbor_idx.sizes(),
              "edge_distance must match neighbor_idx shape");
  TORCH_CHECK(edge_delay.sizes() == neighbor_idx.sizes(),
              "edge_delay must match neighbor_idx shape");
  TORCH_CHECK(step_flat.dim() == 1, "step_flat must have shape [BT]");
  TORCH_CHECK(k_all.size(0) == step_flat.size(0),
              "step_flat length must equal BT");
  TORCH_CHECK(q.size(0) == neighbor_idx.size(0),
              "q and neighbor_idx must agree on receiver count");
  TORCH_CHECK(k_all.size(1) == v_all.size(1),
              "k_all and v_all must agree on sender count");
  TORCH_CHECK(q.size(1) == k_all.size(2),
              "q and k_all must agree on d_k");
  TORCH_CHECK(grad_msg.dim() == 3, "grad_msg must have shape [BT, R, d_v]");
  TORCH_CHECK(grad_msg.size(0) == k_all.size(0),
              "grad_msg and k_all must agree on BT");
  TORCH_CHECK(grad_msg.size(1) == q.size(0),
              "grad_msg and q must agree on receiver count");
  TORCH_CHECK(grad_msg.size(2) == v_all.size(2),
              "grad_msg and v_all must agree on d_v");

  const int BT = static_cast<int>(k_all.size(0));
  const int R = static_cast<int>(q.size(0));
  const int S = static_cast<int>(k_all.size(1));
  const int M = static_cast<int>(neighbor_idx.size(1));
  const int d_k = static_cast<int>(q.size(1));
  const int d_v = static_cast<int>(v_all.size(2));
  auto grad_q = at::zeros_like(q);
  auto grad_k = at::zeros_like(k_all);
  auto grad_v = at::zeros_like(v_all);

  const dim3 grid(BT, R);
  const int threads = 32;
  const size_t shared_bytes = static_cast<size_t>(4 * M) * sizeof(float);
  fabric_sparse_message_backward_kernel<<<grid, threads, shared_bytes>>>(
      grad_msg.data_ptr<float>(), q.data_ptr<float>(), k_all.data_ptr<float>(),
      v_all.data_ptr<float>(), neighbor_idx.data_ptr<int64_t>(),
      neighbor_valid.data_ptr<bool>(), edge_distance.data_ptr<float>(),
      edge_delay.data_ptr<int64_t>(), step_flat.data_ptr<int64_t>(),
      grad_q.data_ptr<float>(), grad_k.data_ptr<float>(),
      grad_v.data_ptr<float>(), BT, R, S, M, d_k, d_v,
      1.0f / std::sqrt(static_cast<float>(d_k)),
      static_cast<float>(distance_scale), use_delay);
  check_launch("fabric_sparse_message_backward_kernel");
  return {grad_q, grad_k, grad_v};
}
