import pytest
import torch
import torch.distributions as D

from torch_einops_utils import kl_divergence
from torch_einops_utils.stable import kl_divergence as stable_kl_divergence
from torch_einops_utils.stable import log_softmax
from torch_einops_utils.stable_softmax import log_softmax as shim_log_softmax

param = pytest.mark.parametrize

# family table: name -> (ctor, param_sampler)

def _sample_params(name, eps, seed = 0):
    g = torch.Generator().manual_seed(seed)
    n = 16
    rand = lambda *s: torch.rand(*s, generator = g, dtype = torch.float64)
    randn = lambda *s: torch.randn(*s, generator = g, dtype = torch.float64)
    near_pos = lambda x, lo = 1e-2: (x * (1. + eps * randn(*x.shape))).clamp_min(lo)
    near_prob = lambda x: (x + eps * randn(*x.shape)).clamp(0.05, 0.95)

    if name in ('exponential', 'poisson'):
        hi = 3. if name == 'exponential' else 10.
        p = 0.5 + hi * rand(n)
        q = near_pos(p, 1e-3) if eps else 0.5 + hi * rand(n)
        return (p,), (q,)

    if name in ('normal', 'laplace', 'cauchy'):
        pl, ps = randn(n), 0.5 + 2. * rand(n)
        ql, qs = (pl + eps * randn(n), near_pos(ps, 1e-3)) if eps else (randn(n), 0.5 + 2. * rand(n))
        return (pl, ps), (ql, qs)

    if name == 'uniform':
        pl = randn(n)
        ph = pl + 0.5 + 2. * rand(n)
        ql = pl - (eps * rand(n) if eps else 0.1 + rand(n))
        qh = ph + (eps * rand(n) if eps else 0.1 + rand(n))
        return (pl, ph), (ql, qh)

    if name == 'pareto':
        sq, ap = 0.5 + 2. * rand(n), 0.5 + 3. * rand(n)
        sp = sq * (1. + eps * rand(n)) if eps else sq + 0.1 + rand(n)
        aq = near_pos(ap, 0.1) if eps else 0.5 + 3. * rand(n)
        return (sp, ap), (sq, aq)

    if name in ('gamma', 'beta'):
        p1, p2 = 0.5 + 5. * rand(n), 0.5 + 5. * rand(n)
        q1, q2 = (near_pos(p1), near_pos(p2)) if eps else (0.5 + 5. * rand(n), 0.5 + 5. * rand(n))
        return (p1, p2), (q1, q2)

    if name == 'dirichlet':
        p = 0.5 + 5. * rand(n, 4)
        q = near_pos(p) if eps else 0.5 + 5. * rand(n, 4)
        return (p,), (q,)

    if name in ('bernoulli_probs', 'binomial_probs', 'geometric_probs'):
        p = 0.1 + 0.8 * rand(n)
        q = near_prob(p) if eps else 0.1 + 0.8 * rand(n)
        return (p,), (q,)

    if name in ('bernoulli_logits', 'binomial_logits', 'geometric_logits'):
        p = 2. * randn(n)
        q = p + eps * randn(n) if eps else 2. * randn(n)
        return (p,), (q,)

    if name == 'categorical_probs':
        p = (0.1 + rand(n, 6))
        p = p / p.sum(-1, keepdim = True)
        q = (p + eps * randn(n, 6)).clamp_min(0.01) if eps else 0.1 + rand(n, 6)
        return (p,), (q / q.sum(-1, keepdim = True),)

    if name == 'categorical_logits':
        p = 2. * randn(n, 6)
        q = p + eps * randn(n, 6) if eps else 2. * randn(n, 6)
        return (p,), (q,)

    if name == 'mvn':
        d = 4
        make_tril = lambda: torch.tril(0.5 * randn(n, d, d), diagonal = -1) + torch.diag_embed(0.5 + rand(n, d))
        mu_p, l_p = randn(n, d), make_tril()
        mu_q = mu_p + eps * randn(n, d) if eps else randn(n, d)
        l_q = l_p + torch.tril(eps * randn(n, d, d)) if eps else make_tril()
        return (mu_p, l_p), (mu_q, l_q)

    raise ValueError(name)

CTORS = {
    'exponential':        D.Exponential,
    'poisson':            D.Poisson,
    'normal':             D.Normal,
    'laplace':            D.Laplace,
    'cauchy':             D.Cauchy,
    'uniform':            D.Uniform,
    'pareto':             D.Pareto,
    'gamma':              D.Gamma,
    'beta':               D.Beta,
    'dirichlet':          D.Dirichlet,
    'bernoulli_probs':    lambda p: D.Bernoulli(probs = p),
    'bernoulli_logits':   lambda z: D.Bernoulli(logits = z),
    'binomial_probs':     lambda p: D.Binomial(10, probs = p),
    'binomial_logits':    lambda z: D.Binomial(10, logits = z),
    'geometric_probs':    lambda p: D.Geometric(probs = p),
    'geometric_logits':   lambda z: D.Geometric(logits = z),
    'categorical_probs':  lambda p: D.Categorical(probs = p),
    'categorical_logits': lambda z: D.Categorical(logits = z),
    'mvn':                lambda mu, tril: D.MultivariateNormal(mu, scale_tril = tril),
}

ALL_FAMILIES = list(CTORS)

def make_pair(name, dtype, eps = None, identical = False):
    ps, qs = _sample_params(name, eps)
    ps = tuple(t.to(dtype).detach().requires_grad_() for t in ps)
    qs = tuple(t.detach().clone().requires_grad_() for t in ps) if identical else tuple(t.to(dtype).detach().requires_grad_() for t in qs)
    ctor = CTORS[name]
    return ctor(*ps), ctor(*qs), ps + qs

def grad_targets_and_fp64(name, p, q, leaves):
    if name == 'categorical_logits':
        targets = (p.logits, q.logits)
    elif name == 'categorical_probs':
        targets = (p.probs, q.probs)
    else:
        targets = leaves

    leaves64 = tuple(t.detach().double().requires_grad_() for t in targets)
    h = len(leaves64) // 2
    ctor = CTORS[name]
    return targets, ctor(*leaves64[:h]), ctor(*leaves64[h:]), leaves64

# exports & paper examples

def test_exports_and_shim():
    assert kl_divergence is stable_kl_divergence
    assert log_softmax is shim_log_softmax

def test_paper_examples():
    p, q = D.Normal(torch.tensor(0.), torch.tensor(1.)), D.Normal(torch.tensor(1e-4), torch.tensor(1.))
    assert D.kl_divergence(p, q).item() == 0.
    assert torch.allclose(kl_divergence(p, q), torch.tensor(5e-9), rtol = 1e-5)

    ep, eq = D.Exponential(torch.tensor(1.)), D.Exponential(torch.tensor(1.0001))
    assert D.kl_divergence(ep, eq).item() == 0.
    assert torch.allclose(kl_divergence(ep, eq), torch.tensor(5.0013e-9), rtol = 1e-3)

    torch.manual_seed(0)
    t = torch.randn(1, 32000).half()
    s = (t.float() + 1e-2 * torch.randn(1, 32000)).half()
    cp, cq = D.Categorical(logits = t), D.Categorical(logits = s)
    assert D.kl_divergence(cp, cq).item() < 0.

    kl = kl_divergence(cp, cq)
    ref = kl_divergence(D.Categorical(logits = cp.logits.double()), D.Categorical(logits = cq.logits.double()))
    assert kl.dtype == torch.float16 and kl.item() > 0.
    assert torch.allclose(kl.double(), ref, rtol = 1e-3)

# accuracy, exact identity & low precision across all families

@param('family', ALL_FAMILIES)
@param('high_precision', [True, False])
def test_matches_torch_well_separated(family, high_precision):
    p, q, leaves = make_pair(family, torch.float32)
    targets, p64, q64, leaves64 = grad_targets_and_fp64(family, p, q, leaves)

    kl = kl_divergence(p, q, high_precision = high_precision)
    grads = torch.autograd.grad(kl.sum(), targets)

    kl_ref = D.kl_divergence(p64, q64)
    grads_ref = torch.autograd.grad(kl_ref.sum(), leaves64)

    assert kl.dtype == torch.float32
    assert torch.allclose(kl.double(), kl_ref, rtol = 1e-5, atol = 1e-6)

    for g, g_ref in zip(grads, grads_ref):
        assert g.dtype == torch.float32
        if family == 'mvn' and g.ndim == 3:
            assert torch.allclose(g.double(), torch.tril(g_ref), rtol = 1e-4, atol = 1e-5)
            assert torch.equal(torch.triu(g, diagonal = 1), torch.zeros_like(torch.triu(g, diagonal = 1)))
        else:
            assert torch.allclose(g.double(), g_ref, rtol = 1e-4, atol = 1e-5)

@param('family', ALL_FAMILIES)
@param('high_precision', [True, False])
def test_exact_zero_at_identity(family, high_precision):
    p, q, leaves = make_pair(family, torch.float32, identical = True)
    kl = kl_divergence(p, q, high_precision = high_precision)
    grads = torch.autograd.grad(kl.sum(), leaves)

    assert torch.equal(kl, torch.zeros_like(kl))

    if family not in {'uniform', 'pareto'}:
        assert all(torch.equal(g, torch.zeros_like(g)) for g in grads)

@param('family', ALL_FAMILIES)
@param('high_precision', [True, False])
def test_near_equality_fp32(family, high_precision):
    p, q, leaves = make_pair(family, torch.float32, eps = 1e-4)
    targets, p64, q64, leaves64 = grad_targets_and_fp64(family, p, q, leaves)

    kl = kl_divergence(p, q, high_precision = high_precision)
    grads = torch.autograd.grad(kl.sum(), targets)

    kl_ref = kl_divergence(p64, q64)
    grads_ref = torch.autograd.grad(kl_ref.sum(), leaves64)

    assert (kl >= 0).all()
    assert torch.allclose(kl.double(), kl_ref, rtol = 1e-4, atol = 1e-12)
    assert all(torch.isfinite(g).all() and torch.allclose(g.double(), g_ref, rtol = 1e-3, atol = 1e-7) for g, g_ref in zip(grads, grads_ref))

@param('family', ALL_FAMILIES)
@param('dtype', [torch.float16, torch.bfloat16])
def test_low_precision(family, dtype):
    p, q, leaves = make_pair(family, dtype, eps = 1e-2)
    targets, p64, q64, leaves64 = grad_targets_and_fp64(family, p, q, leaves)

    kl = kl_divergence(p, q, high_precision = True)
    grads = torch.autograd.grad(kl.sum(), targets)

    kl_ref = kl_divergence(p64, q64)
    grads_ref = torch.autograd.grad(kl_ref.sum(), leaves64)

    rtol = 1e-2 if dtype == torch.float16 else 5e-2
    assert kl.dtype == dtype and (kl >= 0).all()
    assert torch.allclose(kl.double(), kl_ref, rtol = rtol, atol = 1e-7)
    assert all(g.dtype == dtype and torch.isfinite(g).all() and torch.allclose(g.double(), g_ref, rtol = rtol, atol = 1e-4) for g, g_ref in zip(grads, grads_ref))

    if family != 'mvn':
        kl_native = kl_divergence(p, q, high_precision = False)
        grads_native = torch.autograd.grad(kl_native.sum(), leaves)
        assert kl_native.dtype == dtype and (kl_native >= 0).all() and torch.isfinite(kl_native).all()
        assert all(g.dtype == dtype and torch.isfinite(g).all() for g in grads_native)

# invariances, boundaries, wrappers & mps

@param('high_precision', [True, False])
def test_invariances(high_precision):
    # Normal Pythagorean triple: sigma_q^2 == sigma_p^2 + (mu_p - mu_q)^2 -> dKL/dsigma_q == 0
    pl, ps = torch.tensor([3., 329.], requires_grad = True), torch.tensor([4., 1080.], requires_grad = True)
    ql, qs = torch.tensor([0., 0.], requires_grad = True), torch.tensor([5., 1129.], requires_grad = True)
    _, _, _, g_qs = torch.autograd.grad(kl_divergence(D.Normal(pl, ps), D.Normal(ql, qs), high_precision = high_precision).sum(), (pl, ps, ql, qs))
    assert torch.allclose(g_qs, torch.zeros_like(g_qs), atol = 1e-15 if high_precision else 1e-7)

    # Categorical dyadic logit shift & probability scale invariance
    z = torch.tensor([[1.5, -0.5, 2.0, -4.0]], requires_grad = True)
    p, q = D.Categorical(logits = z), D.Categorical(logits = z.detach().clone())
    p.logits, q.logits = z, z + 8.0
    kl = kl_divergence(p, q, high_precision = high_precision)
    assert torch.equal(kl, torch.zeros_like(kl))
    assert torch.equal(torch.autograd.grad(kl.sum(), (z,))[0], torch.zeros_like(z))

    x = torch.tensor([[0.1, 0.2, 0.3, 0.4]], requires_grad = True)
    y = (x.detach() * 4.).requires_grad_()
    kl_p = kl_divergence(D.Categorical(probs = x), D.Categorical(probs = y), high_precision = high_precision)
    assert torch.equal(kl_p, torch.zeros_like(kl_p))
    assert all(torch.equal(g, torch.zeros_like(g)) for g in torch.autograd.grad(kl_p.sum(), (x, y)))

def test_boundaries_and_edges():
    # Categorical zero probs, -inf logits, +inf support mismatch & far logit gap
    x, y = torch.tensor([0.5, 0.5, 0.], requires_grad = True), torch.tensor([0.4, 0.4, 0.2], requires_grad = True)
    kl = kl_divergence(D.Categorical(probs = x), D.Categorical(probs = y))
    gx, gy = torch.autograd.grad(kl, (x, y))
    assert torch.allclose(kl, -torch.tensor(0.8).log(), rtol = 1e-6)
    assert torch.allclose(gx[:2], torch.zeros(2), atol = 1e-6)
    assert torch.allclose(gy, torch.tensor([-0.25, -0.25, 1.]), atol = 1e-6)

    z, w = torch.tensor([0., 0., -float('inf')], requires_grad = True), torch.tensor([0., 0., 0.], requires_grad = True)
    kl_l = kl_divergence(D.Categorical(logits = z), D.Categorical(logits = w))
    gz, gw = torch.autograd.grad(kl_l, (z, w))
    assert torch.allclose(kl_l, torch.tensor(1.5).log(), rtol = 1e-6)
    assert torch.allclose(gz, torch.zeros(3), atol = 1e-6)
    assert torch.allclose(gw, torch.tensor([1. / 3. - 0.5, 1. / 3. - 0.5, 1. / 3.]), atol = 1e-6)

    assert torch.isinf(kl_divergence(D.Categorical(probs = torch.tensor([0.5, 0.5])), D.Categorical(probs = torch.tensor([1., 0.]))))

    zf = torch.tensor([[1000., 0.], [-1000., 0.]], requires_grad = True)
    wf = torch.tensor([[-1000., 0.], [1000., 0.]], requires_grad = True)
    kl_f = kl_divergence(D.Categorical(logits = zf), D.Categorical(logits = wf))
    assert torch.allclose(kl_f, torch.tensor([1000., 1000.]), rtol = 1e-5)
    assert all(torch.isfinite(g).all() for g in torch.autograd.grad(kl_f.sum(), (zf, wf)))

    # Bernoulli / Geometric boundaries & extreme logits
    kl_b = kl_divergence(D.Bernoulli(probs = torch.tensor([0., 1., 0.5, 0.])), D.Bernoulli(probs = torch.tensor([0.2, 0.8, 0., 0.])))
    assert torch.allclose(kl_b[:2], -torch.tensor([0.8, 0.8]).log()) and torch.isinf(kl_b[2]) and kl_b[3] == 0.

    zl = torch.tensor([100., -100., 500.], requires_grad = True)
    wl = torch.tensor([100. + 1e-4, -100. - 1e-4, -500.], requires_grad = True)
    kl_bl = kl_divergence(D.Bernoulli(logits = zl), D.Bernoulli(logits = wl))
    assert (kl_bl >= 0).all() and torch.isfinite(kl_bl).all()
    assert all(torch.isfinite(g).all() for g in torch.autograd.grad(kl_bl.sum(), (zl, wl)))
    assert torch.isfinite(kl_divergence(D.Geometric(logits = zl[:2]), D.Geometric(logits = wl[:2]))).all()

    # Uniform & Pareto outside support
    assert torch.isinf(kl_divergence(D.Uniform(0., 2.), D.Uniform(0.5, 2.)))
    assert torch.isinf(kl_divergence(D.Pareto(1., 2.), D.Pareto(2., 2.)))

def test_broadcasting_and_mvn_covariance():
    p, q = D.Bernoulli(probs = torch.tensor([[0.2], [0.7]])), D.Bernoulli(logits = torch.tensor([-1., 0.5, 2.]))
    ref = D.kl_divergence(D.Bernoulli(probs = p.probs.expand(2, 3)), D.Bernoulli(logits = q.logits.expand(2, 3)))
    assert torch.allclose(kl_divergence(p, q), ref, rtol = 1e-5, atol = 1e-6)

    torch.manual_seed(0)
    a = torch.randn(3, 8, 8)
    cov_p = (a @ a.mT + torch.eye(8)).requires_grad_()
    cov_q = (cov_p.detach() + 1e-5 * torch.eye(8)).requires_grad_()
    mu_p = torch.randn(3, 8, requires_grad = True)
    mu_q = (mu_p.detach() + 1e-5 * torch.randn(3, 8)).requires_grad_()
    kl = kl_divergence(D.MultivariateNormal(mu_p, covariance_matrix = cov_p), D.MultivariateNormal(mu_q, covariance_matrix = cov_q))
    assert (kl >= 0).all() and torch.isfinite(kl).all()
    assert all(torch.isfinite(g).all() for g in torch.autograd.grad(kl.sum(), (mu_p, cov_p, mu_q, cov_q)))

def test_wrappers_and_fallback():
    kl_ind = kl_divergence(D.Independent(D.Normal(torch.zeros(4, 3), torch.ones(4, 3)), 1), D.Independent(D.Normal(torch.full((4, 3), 1e-4), torch.ones(4, 3)), 1))
    assert kl_ind.shape == (4,) and torch.allclose(kl_ind, torch.full((4,), 1.5e-8), rtol = 1e-5)

    class ScaledBeta(D.TransformedDistribution):
        pass

    t = D.AffineTransform(-1., 2.)
    a1, a0 = torch.tensor([2., 5.]), torch.tensor([3., 4.])
    c1, c0 = a1 + 1e-5, a0 - 1e-5
    assert torch.equal(kl_divergence(ScaledBeta(D.Beta(a1, a0), t), ScaledBeta(D.Beta(c1, c0), t)), kl_divergence(D.Beta(a1, a0), D.Beta(c1, c0)))

    z = torch.randn(4, 5)
    w = z + 1e-5 * torch.randn_like(z)
    assert torch.equal(kl_divergence(D.OneHotCategorical(logits = z), D.OneHotCategorical(logits = w)), kl_divergence(D.Categorical(logits = z), D.Categorical(logits = w)))

    ep, gq = D.Exponential(torch.tensor([2.])), D.Gamma(torch.tensor([4.]), torch.tensor([5.]))
    assert torch.allclose(kl_divergence(ep, gq), D.kl_divergence(ep, gq))

    with pytest.raises(NotImplementedError):
        kl_divergence(D.Binomial(5, probs = torch.tensor(0.5)), D.Binomial(6, probs = torch.tensor(0.5)))

@pytest.mark.skipif(not torch.backends.mps.is_available(), reason = 'mps not available')
@param('dtype', [torch.float32, torch.float16])
def test_mps(dtype):
    z = torch.randn(4, 5, device = 'mps', dtype = dtype, requires_grad = True)
    w = (z.detach() + 1e-3 * torch.randn_like(z)).requires_grad_(True)
    kl = kl_divergence(D.Categorical(logits = z), D.Categorical(logits = w))
    assert kl.device.type == 'mps' and kl.dtype == dtype and (kl >= 0).all()
    assert all(torch.isfinite(g).all() for g in torch.autograd.grad(kl.sum(), (z, w)))

    mu = torch.randn(4, device = 'mps', dtype = dtype)
    kl_n = kl_divergence(D.Normal(mu, mu.abs() + 1.), D.Normal(mu, mu.abs() + 1.))
    assert kl_n.dtype == dtype and torch.equal(kl_n, torch.zeros_like(kl_n))
