#include <torch/extension.h>

std::vector<at::Tensor> fabric_sparse_message_forward_cuda(
    at::Tensor q, at::Tensor k_all, at::Tensor v_all, at::Tensor neighbor_idx,
    at::Tensor neighbor_valid, at::Tensor edge_distance, at::Tensor edge_delay,
    at::Tensor step_flat, double distance_scale, bool use_delay);

std::vector<at::Tensor> fabric_sparse_message_backward_cuda(
    at::Tensor grad_msg, at::Tensor q, at::Tensor k_all, at::Tensor v_all,
    at::Tensor neighbor_idx, at::Tensor neighbor_valid, at::Tensor edge_distance,
    at::Tensor edge_delay, at::Tensor step_flat, double distance_scale,
    bool use_delay);

PYBIND11_MODULE(TORCH_EXTENSION_NAME, m) {
  m.def("forward", &fabric_sparse_message_forward_cuda,
        "Fabric sparse message forward (CUDA)");
  m.def("backward", &fabric_sparse_message_backward_cuda,
        "Fabric sparse message backward (CUDA)");
}
