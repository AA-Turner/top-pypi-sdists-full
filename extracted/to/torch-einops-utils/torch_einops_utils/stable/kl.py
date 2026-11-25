# Yang, Tang, Chen, Qian, Chen, Yang & Cui. The KL Divergence Is Never Negative, Except in PyTorch. 2026.
# https://arxiv.org/abs/2611.30835

from __future__ import annotations

import math
from functools import reduce

import torch
import torch.distributions as D
import torch.nn.functional as F
from einops import rearrange
from torch.autograd import Function

from torch_einops_utils.torch_einops_utils import default, exists

# series coefficients

_PHI_COEFS = {
    dtype: tuple(1. / (2 * k + 1) for k in range(1, terms + 1))
    for dtype, terms in (
        (torch.float16, 9),
        (torch.bfloat16, 9),
        (torch.float32, 17),
        (torch.float64, 36),
    )
}

_XI_COEFS = tuple(1. / math.factorial(k + 2) for k in range(18))

_OMEGA_COEFS = (1. / 6, -1. / 30, 1. / 42, -1. / 30, 5. / 66, -691. / 2730, 7. / 6)

# 8-point Gauss-Legendre nodes u in (0, 1) and weights w * (1 - u) for integral Bregman remainders

_GL8 = (
    (0.019855071751231912, 0.04960931821952938),
    (0.10166676129318664,  0.099886137453735535),
    (0.2372337950418355,   0.1196424138732155),
    (0.40828267875217511,  0.10730313838033538),
    (0.59171732124782495,  0.074038753308845615),
    (0.7627662049581645,   0.037210909065728208),
    (0.89833323870681336,  0.011304379772951553),
    (0.98014492824876809,  0.0010049499256588031),
)

# high-precision evaluation with single rounding
# round-to-odd in fp32 prevents double rounding when narrowing fp64 -> fp16 / bf16

def _round_to(val, dtype):
    if val.dtype != torch.float64 or dtype not in (torch.float16, torch.bfloat16):
        return val.to(dtype)

    fp32 = val.to(torch.float32).contiguous()
    widened = fp32.to(torch.float64)
    inexact = widened != val

    bits = fp32.view(torch.int32)
    towards_zero = torch.where(widened.abs() > val.abs(), bits - 1, bits)
    rounded_odd = torch.where(inexact, towards_zero | 1, bits)

    use_odd = torch.isfinite(val) & inexact
    return torch.where(use_odd, rounded_odd.view(torch.float32), fp32).to(dtype)

class _Widen(Function):
    @staticmethod
    def forward(ctx, x, compute_dtype):
        ctx.input_dtype = x.dtype
        ctx.compute_dtype = compute_dtype
        return x.to(compute_dtype)

    @staticmethod
    def backward(ctx, grad_output):
        if not exists(grad_output):
            return None, None

        grad = _round_to(grad_output.to(ctx.compute_dtype), ctx.input_dtype)
        return grad, None

class _Narrow(Function):
    @staticmethod
    def forward(ctx, val, target_dtype):
        ctx.compute_dtype = val.dtype
        return _round_to(val, target_dtype)

    @staticmethod
    def backward(ctx, grad_output):
        return grad_output.to(ctx.compute_dtype), None

def _eval(fn, high_precision, *tensors):
    dtype = reduce(torch.promote_types, (t.dtype for t in tensors))
    tensors = tuple(t.to(dtype) for t in tensors)

    compute_dtype = torch.float32 if tensors[0].device.type == 'mps' else torch.float64

    if not high_precision or dtype in (compute_dtype, torch.float64):
        return fn(*tensors)

    widened = (_Widen.apply(t, compute_dtype) for t in tensors)
    return _Narrow.apply(fn(*widened), dtype)

# scalar helpers

def _horner(x, coefs):
    acc = torch.full_like(x, coefs[-1])

    for c in reversed(coefs[:-1]):
        acc = acc * x + c

    return acc

def _log_ratio(b, a, rel = None):
    # log(b / a) without cancellation near 1 or underflow far from 1

    rel = default(rel, (b - a) / a)
    use_log1p = torch.isfinite(rel) & (rel >= -0.75)

    safe_rel = rel.masked_fill(~use_log1p, 0.)
    return torch.where(use_log1p, safe_rel.log1p(), b.log() - a.log())

def _softplus(x):
    # exact softplus without F.softplus's threshold = 20 cutoff

    return x.clamp_min(0.) + (-x.abs()).exp().log1p()

def _omega(x):
    # x * psi_1(x) - 1 > 0, strictly decreasing
    # asymptotic Bernoulli series avoids cancellation for x >= 16

    is_large = x >= 16.
    inv = 1. / x.masked_fill(~is_large, 16.)
    inv_sq = inv * inv
    small_x = x.masked_fill(is_large, 1.)

    asymptotic = 0.5 * inv + inv_sq * _horner(inv_sq, _OMEGA_COEFS)
    exact = small_x * torch.special.polygamma(1, small_x) - 1.
    return torch.where(is_large, asymptotic, exact)

def _phi_forward(b, a, diff = None):
    # phi(b / a - 1) = (b - a) / a - log(b / a) >= 0
    # evaluated via convergent atanh series on [-3/4, 3]

    diff = default(diff, b - a)
    x = diff / a

    is_finite = torch.isfinite(x)
    in_series = is_finite & (x >= -0.75) & (x <= 3.)

    safe_x = x.masked_fill(~in_series, 0.)
    s = (diff / (a + b)).masked_fill(~in_series, 0.)
    s_sq = s * s

    series = safe_x * s - 2. * (s * s_sq) * _horner(s_sq, _PHI_COEFS[x.dtype])
    outer = x.masked_fill(~is_finite, 0.) - _log_ratio(b, a, x)
    return torch.where(in_series, series, outer).clamp_min(0.)

# atomic non-negative autograd primitives
# every closed-form KL decomposes into a non-negative sum of these four

class _Phi(Function):
    # phi(b / a - 1) = (b - a) / a - log(b / a) >= 0

    @staticmethod
    def forward(ctx, b, a, diff = None):
        diff = default(diff, b - a)
        ctx.save_for_backward(b, a, diff)
        return _phi_forward(b, a, diff = diff)

    @staticmethod
    def backward(ctx, grad_output):
        b, a, diff = ctx.saved_tensors
        x = diff / a

        grad_b = grad_output * (x / b) if ctx.needs_input_grad[0] else None
        grad_a = grad_output * (-x / a) if ctx.needs_input_grad[1] else None
        return grad_b, grad_a, None

class _BregmanKL(Function):
    # q - p - p * log(q / p) = p * phi(q / p - 1) >= 0, with limit q at p = 0

    @staticmethod
    def forward(ctx, p, q, diff = None):
        p_zero = p == 0
        q_zero = q == 0
        active = ~p_zero & ~q_zero

        safe_p = p.masked_fill(~active, 1.)
        safe_q = q.masked_fill(~active, 1.)
        diff = default(diff, q - p).masked_fill(~active, 0.)

        boundary = q.masked_fill(~p_zero, float('inf'))
        kl = torch.where(active, safe_p * _phi_forward(safe_q, safe_p, diff = diff), boundary)

        ctx.save_for_backward(safe_p, safe_q, diff, p_zero, active)
        return kl

    @staticmethod
    def backward(ctx, grad_output):
        safe_p, safe_q, diff, p_zero, active = ctx.saved_tensors
        zero = torch.zeros_like(safe_p)

        grad_p = grad_output * torch.where(active, -_log_ratio(safe_q, safe_p, diff / safe_p), zero) if ctx.needs_input_grad[0] else None
        grad_q = grad_output * torch.where(active, diff / safe_q, zero.masked_fill(p_zero, 1.)) if ctx.needs_input_grad[1] else None
        return grad_p, grad_q, None

class _Xi(Function):
    # expm1(t) - t >= 0 via power series near 0; exact derivative is expm1(t)

    @staticmethod
    def forward(ctx, t):
        is_small = t.abs() < 0.25
        safe_t = t.masked_fill(~is_small, 0.)

        series = safe_t * safe_t * _horner(safe_t, _XI_COEFS)
        ctx.save_for_backward(t)
        return torch.where(is_small, series, t.expm1() - t).clamp_min(0.)

    @staticmethod
    def backward(ctx, grad_output):
        t, = ctx.saved_tensors
        return grad_output * t.expm1()

def _zero_support_correction(kl, grad_w, p, w_safe, p_zero, has_zero):
    # add -log Q(support(P)) when P assigns zero probability (-inf logit) to some categories

    lse_out = torch.logsumexp(w_safe.masked_fill(~p_zero, -float('inf')), dim = -1)
    lse_in = torch.logsumexp(w_safe.masked_fill(p_zero, -float('inf')), dim = -1)

    delta = torch.where(has_zero, lse_out - lse_in, -float('inf'))
    kl = kl + torch.where(torch.isneginf(delta), 0., _softplus(delta))

    q_in = rearrange(torch.where(has_zero, (-delta).sigmoid(), 1.), '... -> ... 1')
    q_out = rearrange(torch.where(has_zero, delta.sigmoid(), 0.), '... -> ... 1')
    grad_w = torch.where(p_zero, F.softmax(w_safe, dim = -1), q_in * grad_w - q_out * p)

    return kl, grad_w

def _far_logits_fallback(kl, grad_z, grad_w, log_p, p, w_safe, is_far):
    # standard log-space formula when extreme logit gaps overflow expm1

    log_q = F.log_softmax(w_safe, dim = -1)
    log_ratio = (log_p - log_q).masked_fill(p <= 0, 0.)
    kl_far = (p * log_ratio).sum(dim = -1)

    far_mask = rearrange(is_far, '... -> ... 1')
    kl = torch.where(is_far, kl_far, kl)
    grad_z = torch.where(far_mask, (p * (log_ratio - rearrange(kl_far, '... -> ... 1'))).masked_fill(p <= 0, 0.), grad_z)
    grad_w = torch.where(far_mask, log_q.exp() - p, grad_w)

    return kl, grad_z, grad_w

class _CategoricalLogitsKL(Function):
    # KL(softmax(z) || softmax(w)) = sum_k p_k * xi(t_k) >= 0, directly from logits

    @staticmethod
    def forward(ctx, z, w):
        p_zero = torch.isneginf(z)
        q_zero = torch.isneginf(w)
        all_zero = p_zero.all(dim = -1)
        has_inf = (~p_zero & q_zero).any(dim = -1)
        invalid = all_zero | has_inf

        invalid_mask = rearrange(invalid, '... -> ... 1')
        z_safe = z.masked_fill(invalid_mask, 0.)
        w_safe = w.masked_fill(invalid_mask, 0.)
        w_in = w_safe.masked_fill(p_zero | q_zero, 0.)

        log_p = F.log_softmax(z_safe, dim = -1)
        p = log_p.exp().masked_fill(p_zero, 0.)

        # center logit differences at P's mode -> exact zero for shifted logits

        diff = w_in - z_safe.masked_fill(p_zero, 0.)
        pivot = diff.gather(-1, z_safe.argmax(dim = -1, keepdim = True))
        s = (diff - pivot).masked_fill(p_zero, 0.)

        def p_expm1(x):
            val = torch.where(x > 30., (log_p + x).exp() - p, p * x.expm1())
            return val.masked_fill(p_zero, 0.)

        e1 = p_expm1(s).sum(dim = -1, keepdim = True)
        l1 = e1.log1p()

        # single recentering pass when Q's mass concentrates far from P's mode

        recenter = (e1 < -0.5) & torch.isfinite(l1)
        s2 = torch.where(recenter & ~p_zero, s - l1, s)
        l2 = p_expm1(s2).sum(dim = -1, keepdim = True).log1p()
        t = torch.where(recenter, s2 - l2, s - l1).masked_fill(p_zero, 0.)

        is_far = ~torch.isfinite(t).all(dim = -1)
        safe_t = t.masked_fill(rearrange(is_far, '... -> ... 1'), 0.)

        terms = torch.where(
            safe_t > 30.,
            (log_p + safe_t).exp() - p * (1. + safe_t),
            p * _Xi.apply(safe_t)
        ).clamp_min(0.)

        kl = terms.masked_fill(p_zero, 0.).sum(dim = -1)
        grad_z = (p * (-safe_t - rearrange(kl, '... -> ... 1'))).masked_fill(p_zero, 0.)
        grad_w = p_expm1(safe_t)

        # lazy boundary corrections

        has_zero = p_zero.any(dim = -1) & ~invalid
        if has_zero.any():
            kl, grad_w = _zero_support_correction(kl, grad_w, p, w_safe, p_zero, has_zero)

        if is_far.any():
            kl, grad_z, grad_w = _far_logits_fallback(kl, grad_z, grad_w, log_p, p, w_safe, is_far)

        all_zero_mask = rearrange(all_zero, '... -> ... 1')
        has_inf_mask = rearrange(has_inf, '... -> ... 1')

        kl = torch.where(all_zero, float('nan'), kl.masked_fill(has_inf, float('inf')))
        grad_z = torch.where(all_zero_mask, float('nan'), grad_z.masked_fill(has_inf_mask, 0.))
        grad_w = torch.where(all_zero_mask, float('nan'), grad_w.masked_fill(has_inf_mask, 0.))

        ctx.save_for_backward(
            grad_z if ctx.needs_input_grad[0] else None,
            grad_w if ctx.needs_input_grad[1] else None,
        )
        return kl

    @staticmethod
    def backward(ctx, grad_output):
        grad_z, grad_w = ctx.saved_tensors
        grad_output = rearrange(grad_output, '... -> ... 1')

        return (
            grad_output * grad_z if exists(grad_z) else None,
            grad_output * grad_w if exists(grad_w) else None,
        )

_phi = _Phi.apply
_bregman = _BregmanKL.apply
_xi = _Xi.apply
_logits_kl = _CategoricalLogitsKL.apply

# integral Bregman divergences for gamma, dirichlet & beta
# v(x) = lgamma(x) - x * log(x) + x has v''(x) = omega(x) / x > 0

def _gamma_bregman(conc_q, conc_p):
    ratio = conc_q / conc_p
    is_near = (ratio >= 0.5) & (ratio <= 2.)

    safe_p = conc_p.masked_fill(~is_near, 1.)
    diff = (conc_q - conc_p).masked_fill(~is_near, 0.)
    diff_sq = diff.square()

    bv_near = torch.zeros_like(conc_p)
    for u, weight in _GL8:
        x = safe_p + u * diff
        bv_near = bv_near + weight * diff_sq * (_omega(x) / x)

    if is_near.all():
        return bv_near

    far_p = conc_p.masked_fill(is_near, 1.)
    far_q = conc_q.masked_fill(is_near, 1.)
    bv_far = (
        torch.lgamma(far_q) - torch.lgamma(far_p)
        + (far_p - far_q) * torch.digamma(far_p)
        + (far_q - far_p)
        - far_q * _log_ratio(far_q, far_p)
    ).clamp_min(0.)

    return torch.where(is_near, bv_near, bv_far)

def _dirichlet_kl_near(alpha_p, alpha_q):
    sum_p = alpha_p.sum(dim = -1, keepdim = True)
    sum_q = alpha_q.sum(dim = -1, keepdim = True)
    diff = alpha_q - alpha_p
    cross = diff * sum_p - diff.sum(dim = -1, keepdim = True) * alpha_p

    # mean-alignment phi term + strictly non-negative Hessian integral of B_V(alpha_q, alpha_p)

    kl = (alpha_q * _phi(alpha_p * sum_q, alpha_q * sum_p, -cross)).sum(dim = -1)

    for u, weight in _GL8:
        x = alpha_p + u * diff
        s = x.sum(dim = -1, keepdim = True)
        omega_x = _omega(x)
        omega_s = _omega(s)

        diag_term = x * (omega_x - omega_s).clamp_min(0.) * (diff / x).square()
        cross_term = omega_s * x * (cross / (x * s)).square()
        kl = kl + weight * (diag_term + cross_term).sum(dim = -1)

    return kl

def _dirichlet_kl_far(alpha_p, alpha_q):
    sum_p = alpha_p.sum(dim = -1, keepdim = True)
    sum_q = alpha_q.sum(dim = -1, keepdim = True)

    return (
        torch.lgamma(sum_p.squeeze(-1)) - torch.lgamma(sum_q.squeeze(-1))
        + (torch.lgamma(alpha_q) - torch.lgamma(alpha_p)).sum(dim = -1)
        + ((alpha_p - alpha_q) * (torch.digamma(alpha_p) - torch.digamma(sum_p))).sum(dim = -1)
    ).clamp_min(0.)

# registration & parameterization helpers

_REGISTRY = {}

def _register(dist_cls):
    def decorator(fn):
        _REGISTRY[dist_cls] = fn
        return fn

    return decorator

def _register_params(dist_cls, *attrs):
    def decorator(fn):
        def handler(p, q, high_precision):
            args = torch.broadcast_tensors(*(getattr(d, attr) for d in (p, q) for attr in attrs))
            return _eval(fn, high_precision, *args)

        _REGISTRY[dist_cls] = handler
        return fn

    return decorator

def _use_logits(p, q):
    def kind(dist):
        if hasattr(dist, '_param'):
            return 'probs' if dist._param is dist.__dict__.get('probs') else 'logits'

        return 'logits' if ('logits' in dist.__dict__ and 'probs' not in dist.__dict__) else 'probs'

    return kind(p) == 'logits' and kind(q) == 'logits'

def _register_logits_or_probs(dist_cls):
    def decorator(fn):
        def handler(p, q, high_precision):
            use_logits = _use_logits(p, q)
            attr = 'logits' if use_logits else 'probs'
            args = torch.broadcast_tensors(getattr(p, attr), getattr(q, attr))
            return _eval(lambda a, b: fn(a, b, use_logits), high_precision, *args)

        _REGISTRY[dist_cls] = handler
        return fn

    return decorator

def _binary_logits(z):
    is_pos_inf = torch.isposinf(z)
    zero = torch.zeros_like(z).masked_fill(is_pos_inf, -float('inf'))
    return torch.stack((zero, z.masked_fill(is_pos_inf, 0.)), dim = -1)

def _binary_kl(p, q, use_logits):
    if use_logits:
        return _logits_kl(_binary_logits(p), _binary_logits(q))

    return _bregman(p, q) + _bregman(1. - p, 1. - q, p - q)

# continuous families

@_register_params(D.Exponential, 'rate')
def _exponential_kl(rate_p, rate_q):
    return _phi(rate_q, rate_p)

@_register_params(D.Normal, 'loc', 'scale')
def _normal_kl(mean_p, std_p, mean_q, std_q):
    rel_std = (std_p - std_q) / std_q
    rel_mean = (mean_p - mean_q) / std_q
    return _phi(std_p, std_q) + 0.5 * rel_std.square() + 0.5 * rel_mean.square()

@_register_params(D.Laplace, 'loc', 'scale')
def _laplace_kl(loc_p, scale_p, loc_q, scale_q):
    dist = (loc_p - loc_q).abs() / scale_p
    return _phi(scale_p, scale_q) + (scale_p / scale_q) * _xi(-dist)

@_register_params(D.Cauchy, 'loc', 'scale')
def _cauchy_kl(loc_p, scale_p, loc_q, scale_q):
    diff_loc = loc_p - loc_q
    tiny = torch.finfo(scale_p.dtype).tiny
    norm = torch.maximum(torch.maximum(scale_p, scale_q), diff_loc.abs()).detach().clamp_min(tiny)

    a = (scale_p - scale_q) / norm
    b = diff_loc / norm
    return ((a.square() + b.square()) / (4. * (scale_p / norm) * (scale_q / norm))).log1p()

@_register_params(D.Uniform, 'low', 'high')
def _uniform_kl(low_p, high_p, low_q, high_q):
    outside = (low_q > low_p) | (high_q < high_p)
    width_p = high_p - low_p
    width_q = (high_q - low_q).masked_fill(outside, 1.)
    rel = (((high_q - high_p) + (low_p - low_q)) / width_p).masked_fill(outside, 0.)

    return _log_ratio(width_q, width_p, rel).masked_fill(outside, float('inf'))

@_register_params(D.Pareto, 'scale', 'alpha')
def _pareto_kl(scale_p, alpha_p, scale_q, alpha_q):
    nested = scale_p >= scale_q
    safe_scale_p = torch.where(nested, scale_p, scale_q)
    return (alpha_q * _log_ratio(safe_scale_p, scale_q) + _phi(alpha_q, alpha_p)).masked_fill(~nested, float('inf'))

def _mvn_kl_from_tril(mean_p, tril_p, mean_q, tril_q):
    solve = torch.linalg.solve_triangular
    n_mat = solve(tril_q, torch.tril(tril_p - tril_q), upper = False)
    v = solve(tril_q, rearrange(mean_p - mean_q, '... d -> ... d 1'), upper = False).squeeze(-1)

    diag_p = tril_p.diagonal(dim1 = -2, dim2 = -1)
    diag_q = tril_q.diagonal(dim1 = -2, dim2 = -1)

    return (
        _phi(diag_p, diag_q).sum(dim = -1)
        + 0.5 * n_mat.square().sum(dim = (-2, -1))
        + 0.5 * v.square().sum(dim = -1)
    )

@_register(D.MultivariateNormal)
def _mvn_kl(p, q, high_precision):
    batch = torch.broadcast_shapes(p.batch_shape, q.batch_shape)
    dim = p.event_shape[0]

    args = (
        p.loc.expand(*batch, dim),
        p.scale_tril.expand(*batch, dim, dim),
        q.loc.expand(*batch, dim),
        q.scale_tril.expand(*batch, dim, dim),
    )

    return _eval(_mvn_kl_from_tril, high_precision, *args)

# gamma, dirichlet & beta

@_register_params(D.Gamma, 'concentration', 'rate')
def _gamma_kl(conc_p, rate_p, conc_q, rate_q):
    mean_diff = conc_p * (rate_q - rate_p) - (conc_q - conc_p) * rate_p
    return conc_q * _phi(conc_p * rate_q, conc_q * rate_p, mean_diff) + _gamma_bregman(conc_q, conc_p)

@_register_params(D.Dirichlet, 'concentration')
def _dirichlet_kl(alpha_p, alpha_q):
    ratio = alpha_q / alpha_p
    is_near = ((ratio >= 0.5) & (ratio <= 2.)).all(dim = -1)
    near_mask = rearrange(is_near, '... -> ... 1')

    kl_near = _dirichlet_kl_near(
        alpha_p.masked_fill(~near_mask, 1.),
        alpha_q.masked_fill(~near_mask, 1.),
    )

    if is_near.all():
        return kl_near

    kl_far = _dirichlet_kl_far(
        alpha_p.masked_fill(near_mask, 1.),
        alpha_q.masked_fill(near_mask, 1.),
    )

    return torch.where(is_near, kl_near, kl_far)

@_register_params(D.Beta, 'concentration1', 'concentration0')
def _beta_kl(conc1_p, conc0_p, conc1_q, conc0_q):
    return _dirichlet_kl(
        torch.stack((conc1_p, conc0_p), dim = -1),
        torch.stack((conc1_q, conc0_q), dim = -1),
    )

# discrete families

@_register_params(D.Poisson, 'rate')
def _poisson_kl(rate_p, rate_q):
    return _bregman(rate_p, rate_q)

@_register_logits_or_probs(D.Categorical)
def _categorical_kl(p, q, use_logits):
    if use_logits:
        return _logits_kl(p, q)

    p = p / p.sum(dim = -1, keepdim = True)
    q = q / q.sum(dim = -1, keepdim = True)
    return _bregman(p, q).sum(dim = -1)

@_register(D.OneHotCategorical)
def _one_hot_categorical_kl(p, q, high_precision):
    return kl_divergence(p._categorical, q._categorical, high_precision = high_precision)

@_register_logits_or_probs(D.Bernoulli)
def _bernoulli_kl(p, q, use_logits):
    return _binary_kl(p, q, use_logits)

@_register(D.Binomial)
def _binomial_kl(p, q, high_precision):
    if not torch.equal(*torch.broadcast_tensors(p.total_count, q.total_count)):
        return D.kl_divergence(p, q)

    use_logits = _use_logits(p, q)
    attr = 'logits' if use_logits else 'probs'
    a, b = torch.broadcast_tensors(getattr(p, attr), getattr(q, attr))
    count = torch.broadcast_to(p.total_count, a.shape).to(torch.promote_types(a.dtype, b.dtype))

    return _eval(lambda n, x, y: n * _binary_kl(x, y, use_logits), high_precision, count, a, b)

@_register_logits_or_probs(D.Geometric)
def _geometric_kl(p, q, use_logits):
    kl = _binary_kl(p, q, use_logits)

    if use_logits:
        at_boundary = torch.isinf(p) | torch.isinf(q)
        scaled = torch.where(at_boundary, kl, kl / p.sigmoid())
        return scaled.masked_fill(torch.isneginf(p), float('nan'))

    safe_p = p.masked_fill(p == 0, 1.)
    return (kl / safe_p).masked_fill(p == 0, float('nan'))

# wrapper distributions

@_register(D.Independent)
def _independent_kl(p, q, high_precision):
    if p.reinterpreted_batch_ndims != q.reinterpreted_batch_ndims:
        return D.kl_divergence(p, q)

    kl = kl_divergence(p.base_dist, q.base_dist, high_precision = high_precision)
    ndims = p.reinterpreted_batch_ndims
    return kl.sum(dim = tuple(range(-ndims, 0))) if ndims > 0 else kl

@_register(D.TransformedDistribution)
def _transformed_kl(p, q, high_precision):
    if p.transforms != q.transforms or p.event_shape != q.event_shape:
        return D.kl_divergence(p, q)

    return kl_divergence(p.base_dist, q.base_dist, high_precision = high_precision)

# public api

def _lookup(dist_cls):
    for cls in dist_cls.__mro__:
        if cls in _REGISTRY:
            return _REGISTRY[cls]

    return None

def categorical_kl(logits_p, logits_q, high_precision: bool = True):
    logits_p, logits_q = torch.broadcast_tensors(logits_p, logits_q)
    return _eval(_logits_kl, high_precision, logits_p, logits_q)

def bernoulli_kl(logits_p, logits_q, high_precision: bool = True):
    logits_p, logits_q = torch.broadcast_tensors(logits_p, logits_q)
    return _eval(lambda p, q: _binary_kl(p, q, True), high_precision, logits_p, logits_q)

def kl_divergence(
    p: D.Distribution,
    q: D.Distribution,
    high_precision: bool = True
):
    handler = _lookup(type(p)) if type(p) is type(q) else None
    return handler(p, q, high_precision) if exists(handler) else D.kl_divergence(p, q)
