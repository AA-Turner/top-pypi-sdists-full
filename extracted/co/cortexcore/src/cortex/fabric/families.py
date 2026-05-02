from __future__ import annotations

import torch
import torch.nn as nn
from tensordict import TensorDict, TensorDictBase

from cortex.config import AxonCoreConfig, sLSTMCoreConfig
from cortex.cores import build_core
from cortex.cores.core.axon_core import AxonCore
from cortex.cores.slstm import sLSTMCore
from cortex.fabric.config import FabricFamilyConfig
from cortex.kernels.dispatch import run_axon_rtu, run_slstm_sequence, run_slstm_sequence_packed
from cortex.kernels.pytorch.rtu.rtu_stream_diag import rtu_stream_diag_pytorch
from cortex.types import ResetMask
from cortex.utils import select_backend

_AXON_TRACE_KEYS = (
    "E_nu_c1",
    "E_nu_c2",
    "E_th_c1",
    "E_th_c2",
    "E_w1_c1",
    "E_w1_c2",
    "E_w2_c1",
    "E_w2_c2",
)


def build_family_module(
    config: FabricFamilyConfig,
    hidden_size: int,
    *,
    num_cells: int,
    init_noise_std: float,
) -> nn.Module:
    if config.family_type == "slstm":
        return _BatchedSLSTMFamily(
            config=config,
            hidden_size=hidden_size,
            num_cells=num_cells,
            init_noise_std=init_noise_std,
        )
    if config.family_type == "axoncell":
        return _BatchedAxonFamily(
            config=config,
            hidden_size=hidden_size,
            num_cells=num_cells,
            init_noise_std=init_noise_std,
        )
    raise ValueError(f"Unsupported fabric family type {config.family_type}")


class _BatchedSLSTMFamily(nn.Module):
    def __init__(self, *, config: FabricFamilyConfig, hidden_size: int, num_cells: int, init_noise_std: float) -> None:
        super().__init__()
        self.hidden_size = int(hidden_size)
        self.num_cells = int(num_cells)
        self.init_noise_std = float(init_noise_std)
        self.dropout = nn.Identity()
        if self.num_cells == 0:
            return

        template = build_core(_build_core_config(config, self.hidden_size))
        if not isinstance(template, sLSTMCore):
            raise TypeError(f"Expected sLSTMCore template, got {type(template).__name__}")
        if template.conv1d_core is not None:
            raise ValueError("Fabric sLSTM family does not support conv preprocessing")
        if template.cfg.use_axon_layer:
            raise ValueError("Fabric sLSTM family does not support AxonLayer gates")

        self.num_heads = int(template.num_heads)
        self.head_dim = int(template.head_dim)
        self.outnorm_eps = float(template.outnorm.eps)
        gate_weight = torch.cat(
            (
                template.igate.weight,
                template.fgate.weight,
                template.zgate.weight,
                template.ogate.weight,
            ),
            dim=-1,
        )
        recurrent_kernel = template.recurrent_kernel.view(self.num_heads, 4, self.head_dim, self.head_dim).permute(
            1, 0, 2, 3
        )
        bias = template.bias.permute(1, 0, 2)
        outnorm_weight = template.outnorm.weight

        self.gate_weight_base, self.gate_weight_delta = _init_base_plus_delta(
            gate_weight,
            self.num_cells,
            self.init_noise_std,
        )
        self.recurrent_kernel_base, self.recurrent_kernel_delta = _init_base_plus_delta(
            recurrent_kernel,
            self.num_cells,
            self.init_noise_std,
        )
        self.bias_base, self.bias_delta = _init_base_plus_delta(
            bias,
            self.num_cells,
            self.init_noise_std,
        )
        self.outnorm_weight_base, self.outnorm_weight_delta = _init_base_plus_delta(
            outnorm_weight,
            self.num_cells,
            self.init_noise_std,
        )

    def materialize_params(self) -> dict[str, torch.Tensor] | None:
        if self.num_cells == 0:
            return None
        gate_weight = _base_plus_delta(self.gate_weight_base, self.gate_weight_delta)
        recurrent_kernel = _base_plus_delta(self.recurrent_kernel_base, self.recurrent_kernel_delta)
        bias = _base_plus_delta(self.bias_base, self.bias_delta)
        outnorm_weight = _base_plus_delta(self.outnorm_weight_base, self.outnorm_weight_delta)
        return {
            "gate_weight": gate_weight,
            "gate_weight_fold": gate_weight.reshape(self.num_cells * self.num_heads, self.head_dim, 4 * self.head_dim),
            "recurrent_kernel": recurrent_kernel,
            "recurrent_kernel_fold": recurrent_kernel.permute(1, 0, 2, 3, 4).reshape(
                4,
                self.num_cells * self.num_heads,
                self.head_dim,
                self.head_dim,
            ),
            "bias": bias,
            "bias_fold": bias.permute(1, 0, 2, 3).reshape(4, self.num_cells * self.num_heads, self.head_dim),
            "outnorm_weight": outnorm_weight,
            "outnorm_weight_flat": outnorm_weight.reshape(-1),
        }

    def init_state(self, batch: int, *, device: torch.device | str, dtype: torch.dtype) -> TensorDict:
        zero = torch.zeros(self.num_cells, batch, self.hidden_size, device=device, dtype=dtype)
        return TensorDict(
            {
                "y": zero.clone(),
                "c": zero.clone(),
                "n": zero.clone(),
                "m": zero.clone(),
            },
            batch_size=[self.num_cells, batch],
        )

    def pack_step_state(
        self,
        state: TensorDictBase | None,
        *,
        batch: int,
        device: torch.device | str,
        dtype: torch.dtype,
    ) -> torch.Tensor:
        family_state = state if state is not None else self.init_state(batch=batch, device=device, dtype=dtype)
        return (
            torch.stack(
                (
                    family_state["y"].reshape(self.num_cells, batch, self.num_heads, self.head_dim),
                    family_state["c"].reshape(self.num_cells, batch, self.num_heads, self.head_dim),
                    family_state["n"].reshape(self.num_cells, batch, self.num_heads, self.head_dim),
                    family_state["m"].reshape(self.num_cells, batch, self.num_heads, self.head_dim),
                ),
                dim=0,
            )
            .permute(0, 2, 1, 3, 4)
            .reshape(4, batch, self.num_cells * self.num_heads, self.head_dim)
        )

    def unpack_step_state(self, packed_state: torch.Tensor) -> TensorDict:
        batch = int(packed_state.shape[1])
        return TensorDict(
            {
                "y": packed_state[0].reshape(batch, self.num_cells, self.hidden_size).permute(1, 0, 2),
                "c": packed_state[1].reshape(batch, self.num_cells, self.hidden_size).permute(1, 0, 2),
                "n": packed_state[2].reshape(batch, self.num_cells, self.hidden_size).permute(1, 0, 2),
                "m": packed_state[3].reshape(batch, self.num_cells, self.hidden_size).permute(1, 0, 2),
            },
            batch_size=[self.num_cells, batch],
        )

    def reset_packed_step_state(self, packed_state: torch.Tensor, mask: torch.Tensor) -> torch.Tensor:
        return torch.where(mask.view(1, -1, 1, 1), torch.zeros_like(packed_state), packed_state)

    def reset_state(self, state: TensorDictBase, mask: torch.Tensor) -> TensorDict:
        first = _first_tensor(state)
        zero = self.init_state(batch=mask.shape[0], device=first.device, dtype=first.dtype)
        return _masked_state(mask, zero, state)

    def forward(
        self,
        x: torch.Tensor,
        state: TensorDictBase | None,
        *,
        resets: ResetMask | None = None,
        materialized: dict[str, torch.Tensor] | None = None,
    ) -> tuple[torch.Tensor, TensorDict]:
        if self.num_cells == 0:
            return x, TensorDict({}, batch_size=[0, x.shape[0]])
        if x.dim() != 4:
            raise ValueError(f"Batched sLSTM family expects [B,T,N,H], got {tuple(x.shape)}")

        batch, seq, num_cells, hidden = x.shape
        if num_cells != self.num_cells or hidden != self.hidden_size:
            raise ValueError(
                "Batched sLSTM family expected "
                f"{(self.num_cells, self.hidden_size)} cells/hidden, got {(num_cells, hidden)}"
            )

        family_state = state if state is not None else self.init_state(batch=batch, device=x.device, dtype=x.dtype)
        params = materialized or self.materialize_params()
        assert params is not None
        recurrent_kernel_fold = params["recurrent_kernel_fold"]
        bias_fold = params["bias_fold"]
        outnorm_weight_flat = params["outnorm_weight_flat"]
        x_phys = x.permute(2, 0, 1, 3).contiguous()
        x_heads = x_phys.view(self.num_cells, batch * seq, self.num_heads, self.head_dim)
        wx = (
            torch.bmm(
                x_heads.permute(0, 2, 1, 3).reshape(self.num_cells * self.num_heads, batch * seq, self.head_dim),
                params["gate_weight_fold"],
            )
            .view(
                self.num_cells,
                self.num_heads,
                batch,
                seq,
                4,
                self.head_dim,
            )
            .permute(2, 3, 4, 0, 1, 5)
            .reshape(
                batch,
                seq,
                4,
                self.num_cells * self.num_heads,
                self.head_dim,
            )
        )
        y0 = family_state["y"].reshape(self.num_cells, batch, self.num_heads, self.head_dim)
        c0 = family_state["c"].reshape(self.num_cells, batch, self.num_heads, self.head_dim)
        n0 = family_state["n"].reshape(self.num_cells, batch, self.num_heads, self.head_dim)
        m0 = family_state["m"].reshape(self.num_cells, batch, self.num_heads, self.head_dim)
        resets_bt = _normalize_resets(resets, batch=batch, seq=seq, device=x.device)
        initial_states = (
            torch.stack((y0, c0, n0, m0), dim=0)
            .permute(0, 2, 1, 3, 4)
            .reshape(
                4,
                batch,
                self.num_cells * self.num_heads,
                self.head_dim,
            )
        )
        y_fold, last_state = run_slstm_sequence(
            Wx=wx,
            R=recurrent_kernel_fold,
            b=bias_fold,
            initial_states=initial_states,
            resets=resets_bt,
            hidden_size=self.num_cells * self.hidden_size,
            num_heads=self.num_cells * self.num_heads,
            head_dim=self.head_dim,
            outnorm_weight=outnorm_weight_flat,
            outnorm_bias=None,
            outnorm_eps=self.outnorm_eps,
            dropout=self.dropout,
            is_step=False,
        )
        y = y_fold.view(batch, seq, self.num_cells, self.hidden_size)
        next_state = TensorDict(
            {
                "y": last_state[0].view(batch, self.num_cells, self.hidden_size).permute(1, 0, 2),
                "c": last_state[1].view(batch, self.num_cells, self.hidden_size).permute(1, 0, 2),
                "n": last_state[2].view(batch, self.num_cells, self.hidden_size).permute(1, 0, 2),
                "m": last_state[3].view(batch, self.num_cells, self.hidden_size).permute(1, 0, 2),
            },
            batch_size=[self.num_cells, batch],
        )
        return y, next_state

    def forward_step_packed(
        self,
        x: torch.Tensor,
        packed_state: torch.Tensor | None,
        *,
        resets: ResetMask | None = None,
        materialized: dict[str, torch.Tensor] | None = None,
    ) -> tuple[torch.Tensor, torch.Tensor]:
        if self.num_cells == 0:
            if packed_state is None:
                packed_state = x.new_zeros(4, x.shape[0], 0, self.head_dim)
            return x, packed_state
        if x.dim() != 3:
            raise ValueError(f"Batched sLSTM family step expects [B,N,H], got {tuple(x.shape)}")

        batch, num_cells, hidden = x.shape
        if num_cells != self.num_cells or hidden != self.hidden_size:
            raise ValueError(
                "Batched sLSTM family expected "
                f"{(self.num_cells, self.hidden_size)} cells/hidden, got {(num_cells, hidden)}"
            )

        params = materialized or self.materialize_params()
        assert params is not None
        if packed_state is None:
            packed_state = self.pack_step_state(None, batch=batch, device=x.device, dtype=x.dtype)
        x_heads = x.transpose(0, 1).reshape(self.num_cells, batch, self.num_heads, self.head_dim)
        wx = (
            torch.bmm(
                x_heads.permute(0, 2, 1, 3).reshape(self.num_cells * self.num_heads, batch, self.head_dim),
                params["gate_weight_fold"],
            )
            .view(
                self.num_cells,
                self.num_heads,
                batch,
                1,
                4,
                self.head_dim,
            )
            .permute(2, 3, 4, 0, 1, 5)
            .reshape(batch, 1, 4, self.num_cells * self.num_heads, self.head_dim)
        )
        resets_bt = _normalize_resets(resets, batch=batch, seq=1, device=x.device)
        y_seq, next_packed_state = run_slstm_sequence_packed(
            Wx=wx,
            R=params["recurrent_kernel_fold"],
            b=params["bias_fold"],
            initial_states=packed_state,
            resets=resets_bt,
            hidden_size=self.num_cells * self.hidden_size,
            num_heads=self.num_cells * self.num_heads,
            head_dim=self.head_dim,
            outnorm_weight=params["outnorm_weight_flat"],
            outnorm_bias=None,
            outnorm_eps=self.outnorm_eps,
            dropout=self.dropout,
            is_step=False,
        )
        return y_seq[:, 0].reshape(batch, self.num_cells, self.hidden_size), next_packed_state


class _BatchedAxonFamily(nn.Module):
    def __init__(self, *, config: FabricFamilyConfig, hidden_size: int, num_cells: int, init_noise_std: float) -> None:
        super().__init__()
        self.hidden_size = int(hidden_size)
        self.num_cells = int(num_cells)
        self.init_noise_std = float(init_noise_std)
        if self.num_cells == 0:
            return

        template = build_core(_build_core_config(config, self.hidden_size))
        if not isinstance(template, AxonCore):
            raise TypeError(f"Expected AxonCore template, got {type(template).__name__}")
        if template._use_fullrank:
            raise ValueError("Fabric Axon family does not support full-rank RTU")
        if template._use_srht:
            raise ValueError("Fabric Axon family does not support SRHT preprocessing")

        self.activation_name = template.activation.__class__.__name__
        self.cuda_seq_threshold = int(template.cfg.cuda_seq_threshold)
        self.use_input_proj = bool(getattr(template, "_use_untraced_linear", False))

        self.nu_log_base, self.nu_log_delta = _init_base_plus_delta(
            template.nu_log,
            self.num_cells,
            self.init_noise_std,
        )
        self.theta_log_base, self.theta_log_delta = _init_base_plus_delta(
            template.theta_log,
            self.num_cells,
            self.init_noise_std,
        )
        self.w1_base, self.w1_delta = _init_base_plus_delta(template.w1, self.num_cells, self.init_noise_std)
        self.w2_base, self.w2_delta = _init_base_plus_delta(template.w2, self.num_cells, self.init_noise_std)
        self.out_proj_weight_base, self.out_proj_weight_delta = _init_base_plus_delta(
            template.out_proj.weight,
            self.num_cells,
            self.init_noise_std,
        )
        self.out_proj_bias_base, self.out_proj_bias_delta = _init_base_plus_delta(
            template.out_proj.bias,
            self.num_cells,
            self.init_noise_std,
        )
        if self.use_input_proj:
            self.input_proj_weight_base, self.input_proj_weight_delta = _init_base_plus_delta(
                template.input_proj.weight,
                self.num_cells,
                self.init_noise_std,
            )
        else:
            self.register_parameter("input_proj_weight_base", None)
            self.register_parameter("input_proj_weight_delta", None)

    def materialize_params(self) -> dict[str, torch.Tensor | None] | None:
        if self.num_cells == 0:
            return None
        params: dict[str, torch.Tensor | None] = {
            "nu_log": _base_plus_delta(self.nu_log_base, self.nu_log_delta),
            "theta_log": _base_plus_delta(self.theta_log_base, self.theta_log_delta),
            "w1": _base_plus_delta(self.w1_base, self.w1_delta),
            "w2": _base_plus_delta(self.w2_base, self.w2_delta),
            "out_proj_weight": _base_plus_delta(self.out_proj_weight_base, self.out_proj_weight_delta),
            "out_proj_bias": _base_plus_delta(self.out_proj_bias_base, self.out_proj_bias_delta),
            "input_proj_weight": None,
        }
        params["nu_log_flat"] = params["nu_log"].reshape(-1)
        params["theta_log_flat"] = params["theta_log"].reshape(-1)
        params["w1_flat"] = params["w1"].reshape(-1)
        params["w2_flat"] = params["w2"].reshape(-1)
        params["out_proj_weight_t"] = params["out_proj_weight"].transpose(1, 2).contiguous()
        if self.use_input_proj:
            params["input_proj_weight"] = _base_plus_delta(self.input_proj_weight_base, self.input_proj_weight_delta)
            params["input_proj_weight_t"] = params["input_proj_weight"].transpose(1, 2).contiguous()
        return params

    def init_state(self, batch: int, *, device: torch.device | str, dtype: torch.dtype) -> TensorDict:
        zero = torch.zeros(self.num_cells, batch, self.hidden_size, device=device, dtype=dtype)
        state = TensorDict(
            {
                "hc1": zero.clone(),
                "hc2": zero.clone(),
            },
            batch_size=[self.num_cells, batch],
        )
        for key in _AXON_TRACE_KEYS:
            state[key] = zero.clone()
        return state

    def pack_step_state(
        self,
        state: TensorDictBase | None,
        *,
        batch: int,
        device: torch.device | str,
        dtype: torch.dtype,
    ) -> dict[str, torch.Tensor]:
        family_state = state if state is not None else self.init_state(batch=batch, device=device, dtype=dtype)
        packed = {
            "hc1": family_state["hc1"].permute(1, 0, 2).reshape(batch, self.num_cells * self.hidden_size),
            "hc2": family_state["hc2"].permute(1, 0, 2).reshape(batch, self.num_cells * self.hidden_size),
        }
        for key in _AXON_TRACE_KEYS:
            packed[key] = family_state[key].permute(1, 0, 2).reshape(batch, self.num_cells * self.hidden_size)
        return packed

    def unpack_step_state(self, packed_state: dict[str, torch.Tensor]) -> TensorDict:
        batch = int(packed_state["hc1"].shape[0])
        state = TensorDict(
            {
                "hc1": packed_state["hc1"].view(batch, self.num_cells, self.hidden_size).permute(1, 0, 2).contiguous(),
                "hc2": packed_state["hc2"].view(batch, self.num_cells, self.hidden_size).permute(1, 0, 2).contiguous(),
            },
            batch_size=[self.num_cells, batch],
        )
        for key in _AXON_TRACE_KEYS:
            state[key] = packed_state[key].view(batch, self.num_cells, self.hidden_size).permute(1, 0, 2).contiguous()
        return state

    def reset_packed_step_state(
        self,
        packed_state: dict[str, torch.Tensor],
        mask: torch.Tensor,
    ) -> dict[str, torch.Tensor]:
        return {
            key: torch.where(mask.view(-1, 1), torch.zeros_like(value), value) for key, value in packed_state.items()
        }

    def reset_state(self, state: TensorDictBase, mask: torch.Tensor) -> TensorDict:
        first = _first_tensor(state)
        zero = self.init_state(batch=mask.shape[0], device=first.device, dtype=first.dtype)
        return _masked_state(mask, zero, state)

    def forward(
        self,
        x: torch.Tensor,
        state: TensorDictBase | None,
        *,
        resets: ResetMask | None = None,
        materialized: dict[str, torch.Tensor | None] | None = None,
    ) -> tuple[torch.Tensor, TensorDict]:
        if self.num_cells == 0:
            return x, TensorDict({}, batch_size=[0, x.shape[0]])
        if x.dim() != 4:
            raise ValueError(f"Batched Axon family expects [B,T,N,H], got {tuple(x.shape)}")

        batch, seq, num_cells, hidden = x.shape
        if num_cells != self.num_cells or hidden != self.hidden_size:
            raise ValueError(
                "Batched Axon family expected "
                f"{(self.num_cells, self.hidden_size)} cells/hidden, got {(num_cells, hidden)}"
            )

        family_state = state if state is not None else self.init_state(batch=batch, device=x.device, dtype=x.dtype)
        params = materialized or self.materialize_params()
        assert params is not None
        nu_log = params["nu_log_flat"]
        theta_log = params["theta_log_flat"]
        w1 = params["w1_flat"]
        w2 = params["w2_flat"]
        out_proj_weight_t = params["out_proj_weight_t"]
        out_proj_bias = params["out_proj_bias"]
        x_phys = x.permute(2, 0, 1, 3).contiguous()
        if self.use_input_proj:
            input_proj_weight = params["input_proj_weight"]
            assert input_proj_weight is not None
            input_proj_weight_t = params["input_proj_weight_t"]
            assert input_proj_weight_t is not None
            x_phys = torch.matmul(x_phys, input_proj_weight_t.unsqueeze(1))
        x_fold = x_phys.permute(1, 2, 0, 3).reshape(batch, seq, self.num_cells * self.hidden_size).contiguous()
        resets_bt = _normalize_resets(resets, batch=batch, seq=seq, device=x.device)
        trace_in = tuple(
            family_state[key].permute(1, 0, 2).reshape(batch, self.num_cells * self.hidden_size).contiguous()
            for key in _AXON_TRACE_KEYS
        )
        backend_fn = select_backend(
            triton_fn="cortex.kernels.triton.rtu:rtu_stream_diag_triton",
            pytorch_fn=rtu_stream_diag_pytorch,
            tensor=x_fold,
            cuda_fn="cortex.kernels.cuda.rtu:rtu_stream_diag_cuda",
            allow_cuda=x_fold.is_cuda and seq <= self.cuda_seq_threshold,
        )
        y2h_fold, (h1_fold, h2_fold), trace_out = backend_fn(
            x_btd=x_fold,
            nu_log=nu_log,
            theta_log=theta_log,
            w1=w1,
            w2=w2,
            activation_name=self.activation_name,
            hc1_init_bh=family_state["hc1"].permute(1, 0, 2).reshape(batch, self.num_cells * self.hidden_size),
            hc2_init_bh=family_state["hc2"].permute(1, 0, 2).reshape(batch, self.num_cells * self.hidden_size),
            trace_in=trace_in,
            resets_bt=resets_bt,
        )
        y2h_phys = y2h_fold.view(batch, seq, self.num_cells, 2 * self.hidden_size).permute(2, 0, 1, 3).contiguous()
        y_phys = torch.matmul(y2h_phys, out_proj_weight_t.unsqueeze(1))
        y = y_phys.permute(1, 2, 0, 3).contiguous() + out_proj_bias.view(1, 1, self.num_cells, self.hidden_size)
        next_state = TensorDict(
            {
                "hc1": h1_fold.view(batch, self.num_cells, self.hidden_size).permute(1, 0, 2).contiguous(),
                "hc2": h2_fold.view(batch, self.num_cells, self.hidden_size).permute(1, 0, 2).contiguous(),
            },
            batch_size=[self.num_cells, batch],
        )
        for key, value in zip(_AXON_TRACE_KEYS, trace_out, strict=True):
            next_state[key] = value.view(batch, self.num_cells, self.hidden_size).permute(1, 0, 2).contiguous()
        return y, next_state

    def forward_step(
        self,
        x: torch.Tensor,
        state: TensorDictBase | None,
        *,
        resets: ResetMask | None = None,
        materialized: dict[str, torch.Tensor | None] | None = None,
    ) -> tuple[torch.Tensor, TensorDict]:
        if self.num_cells == 0:
            return x, TensorDict({}, batch_size=[0, x.shape[0]])
        if x.dim() != 3:
            raise ValueError(f"Batched Axon family step expects [B,N,H], got {tuple(x.shape)}")

        batch, num_cells, hidden = x.shape
        if num_cells != self.num_cells or hidden != self.hidden_size:
            raise ValueError(
                "Batched Axon family expected "
                f"{(self.num_cells, self.hidden_size)} cells/hidden, got {(num_cells, hidden)}"
            )

        family_state = state if state is not None else self.init_state(batch=batch, device=x.device, dtype=x.dtype)
        params = materialized or self.materialize_params()
        assert params is not None
        nu_log = params["nu_log_flat"]
        theta_log = params["theta_log_flat"]
        w1 = params["w1_flat"]
        w2 = params["w2_flat"]
        out_proj_weight_t = params["out_proj_weight_t"]
        out_proj_bias = params["out_proj_bias"]

        x_step = x
        if self.use_input_proj:
            input_proj_weight = params["input_proj_weight"]
            assert input_proj_weight is not None
            input_proj_weight_t = params["input_proj_weight_t"]
            assert input_proj_weight_t is not None
            x_step = torch.bmm(x.transpose(0, 1), input_proj_weight_t).transpose(0, 1)
        x_fold = x_step.reshape(batch, 1, self.num_cells * self.hidden_size)
        resets_bt = None
        if resets is not None:
            resets_bt = torch.as_tensor(resets, device=x.device, dtype=torch.bool).view(batch, 1)
        trace_in = tuple(
            family_state[key].permute(1, 0, 2).reshape(batch, self.num_cells * self.hidden_size).contiguous()
            for key in _AXON_TRACE_KEYS
        )
        y2h_fold, h1_fold, h2_fold, trace_out = run_axon_rtu(
            x_btd=x_fold,
            nu_log=nu_log,
            theta_log=theta_log,
            hc1_init_bh=family_state["hc1"].permute(1, 0, 2).reshape(batch, self.num_cells * self.hidden_size),
            hc2_init_bh=family_state["hc2"].permute(1, 0, 2).reshape(batch, self.num_cells * self.hidden_size),
            trace_in=trace_in,
            resets_bt=resets_bt,
            activation_name=self.activation_name,
            out_weight=None,
            out_bias=None,
            use_fullrank=False,
            prefer_cuda=x_fold.is_cuda and 1 <= self.cuda_seq_threshold,
            is_step=True,
            w1=w1,
            w2=w2,
        )
        y_phys = torch.bmm(
            y2h_fold.view(batch, self.num_cells, 2 * self.hidden_size).transpose(0, 1),
            out_proj_weight_t,
        ).transpose(0, 1)
        y = y_phys + out_proj_bias.view(1, self.num_cells, self.hidden_size)
        next_state = TensorDict(
            {
                "hc1": h1_fold.view(batch, self.num_cells, self.hidden_size).permute(1, 0, 2).contiguous(),
                "hc2": h2_fold.view(batch, self.num_cells, self.hidden_size).permute(1, 0, 2).contiguous(),
            },
            batch_size=[self.num_cells, batch],
        )
        for key, value in zip(_AXON_TRACE_KEYS, trace_out, strict=True):
            next_state[key] = value.view(batch, self.num_cells, self.hidden_size).permute(1, 0, 2).contiguous()
        return y, next_state

    def forward_step_packed(
        self,
        x: torch.Tensor,
        packed_state: dict[str, torch.Tensor] | None,
        *,
        resets: ResetMask | None = None,
        materialized: dict[str, torch.Tensor | None] | None = None,
    ) -> tuple[torch.Tensor, dict[str, torch.Tensor]]:
        if self.num_cells == 0:
            if packed_state is None:
                packed_state = {}
            return x, packed_state
        if x.dim() != 3:
            raise ValueError(f"Batched Axon family step expects [B,N,H], got {tuple(x.shape)}")

        batch, num_cells, hidden = x.shape
        if num_cells != self.num_cells or hidden != self.hidden_size:
            raise ValueError(
                "Batched Axon family expected "
                f"{(self.num_cells, self.hidden_size)} cells/hidden, got {(num_cells, hidden)}"
            )

        params = materialized or self.materialize_params()
        assert params is not None
        if packed_state is None:
            packed_state = self.pack_step_state(None, batch=batch, device=x.device, dtype=x.dtype)
        x_step = x
        if self.use_input_proj:
            input_proj_weight = params["input_proj_weight"]
            assert input_proj_weight is not None
            input_proj_weight_t = params["input_proj_weight_t"]
            assert input_proj_weight_t is not None
            x_step = torch.bmm(x.transpose(0, 1), input_proj_weight_t).transpose(0, 1)
        x_fold = x_step.reshape(batch, 1, self.num_cells * self.hidden_size)
        resets_bt = None
        if resets is not None:
            resets_bt = torch.as_tensor(resets, device=x.device, dtype=torch.bool).view(batch, 1)
        y2h_fold, h1_fold, h2_fold, trace_out = run_axon_rtu(
            x_btd=x_fold,
            nu_log=params["nu_log_flat"],
            theta_log=params["theta_log_flat"],
            hc1_init_bh=packed_state["hc1"],
            hc2_init_bh=packed_state["hc2"],
            trace_in=tuple(packed_state[key] for key in _AXON_TRACE_KEYS),
            resets_bt=resets_bt,
            activation_name=self.activation_name,
            out_weight=None,
            out_bias=None,
            use_fullrank=False,
            prefer_cuda=x_fold.is_cuda and 1 <= self.cuda_seq_threshold,
            is_step=True,
            w1=params["w1_flat"],
            w2=params["w2_flat"],
        )
        y_phys = torch.bmm(
            y2h_fold.view(batch, self.num_cells, 2 * self.hidden_size).transpose(0, 1),
            params["out_proj_weight_t"],
        ).transpose(0, 1)
        next_packed_state = {
            "hc1": h1_fold,
            "hc2": h2_fold,
        }
        for key, value in zip(_AXON_TRACE_KEYS, trace_out, strict=True):
            next_packed_state[key] = value
        return y_phys + params["out_proj_bias"].view(1, self.num_cells, self.hidden_size), next_packed_state


def _build_core_config(config: FabricFamilyConfig, hidden_size: int) -> sLSTMCoreConfig | AxonCoreConfig:
    if config.family_type == "slstm":
        return sLSTMCoreConfig(
            hidden_size=hidden_size,
            num_heads=int(config.num_heads) if config.num_heads is not None else _slstm_num_heads(hidden_size),
            conv1d_kernel_size=0,
            dropout=0.0,
        )
    if config.family_type == "axoncell":
        return AxonCoreConfig(
            hidden_size=hidden_size,
            activation="silu",
            use_untraced_linear=True,
        )
    raise ValueError(f"Unsupported fabric family type {config.family_type}")


def _init_base_plus_delta(
    value: torch.Tensor,
    num_cells: int,
    noise_std: float,
) -> tuple[nn.Parameter, nn.Parameter]:
    # Canonicalize size-1 strides so DDP bucket views and GEMM inputs do not inherit
    # odd layouts from permute()d template tensors such as [4, 1, H].
    base = nn.Parameter(value.detach().clone(memory_format=torch.contiguous_format))
    delta = torch.zeros(num_cells, *value.shape, dtype=value.dtype, device=value.device)
    if noise_std > 0.0:
        delta = delta + noise_std * torch.randn_like(delta)
    return base, nn.Parameter(delta)


def _base_plus_delta(base: torch.Tensor, delta: torch.Tensor) -> torch.Tensor:
    return base.unsqueeze(0) + delta


def _normalize_resets(
    resets: ResetMask | None,
    *,
    batch: int,
    seq: int,
    device: torch.device,
) -> torch.Tensor | None:
    if resets is None:
        return None
    mask = torch.as_tensor(resets, device=device, dtype=torch.bool)
    if mask.dim() == 1:
        return mask.view(batch, 1).expand(batch, seq)
    if mask.dim() == 2 and mask.shape == (batch, seq):
        return mask
    raise ValueError(f"Expected resets with shape [B] or [B,T], got {tuple(mask.shape)}")


def _masked_state(mask: torch.Tensor, zero_state: TensorDict, state: TensorDictBase) -> TensorDict:
    out = TensorDict({}, batch_size=zero_state.batch_size)
    mask_view = mask.view(1, mask.shape[0], 1)
    for key in zero_state.keys():
        out[key] = torch.where(mask_view, zero_state[key], state[key])
    return out


def _first_tensor(state: TensorDictBase) -> torch.Tensor:
    for value in state.values():
        if torch.is_tensor(value):
            return value
    raise ValueError("Expected TensorDict state to contain at least one tensor")


def _slstm_num_heads(hidden_size: int) -> int:
    return 1


__all__ = ["build_family_module"]
