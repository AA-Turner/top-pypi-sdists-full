# Copyright Contributors to the Pyro project.
# SPDX-License-Identifier: Apache-2.0

import pytest

from pyroapi import handlers, infer, pyro, pyro_backend, register_backend
from pyroapi.testing import MODELS

PACKAGE_NAME = {
    "pyro": "pyro",
    "minipyro": "pyro",
    "numpy": "numpyro",
    "funsor": "funsor",
}


@pytest.mark.filterwarnings("ignore", category=UserWarning)
@pytest.mark.parametrize('model', MODELS)
@pytest.mark.parametrize('backend', ['pyro', 'numpy'])
def test_mcmc_interface(model, backend):
    pytest.importorskip(PACKAGE_NAME[backend])
    with pyro_backend(backend), handlers.seed(rng_seed=20):
        f = MODELS[model]()
        model, args, kwargs = f['model'], f.get('model_args', ()), f.get('model_kwargs', {})
        nuts_kernel = infer.NUTS(model=model)
        mcmc = infer.MCMC(nuts_kernel, num_samples=10, warmup_steps=10)
        mcmc.run(*args, **kwargs)
        mcmc.summary()


@pytest.mark.parametrize('backend', ['funsor', 'minipyro', 'numpy', 'pyro'])
def test_not_implemented(backend):
    pytest.importorskip(PACKAGE_NAME[backend])
    with pyro_backend(backend):
        pyro.sample  # should be implemented
        pyro.param  # should be implemented
        with pytest.raises(NotImplementedError):
            pyro.nonexistent_primitive


@pytest.mark.parametrize('model', MODELS)
@pytest.mark.parametrize('backend', [
    pytest.param("funsor", marks=[pytest.mark.xfail(
        reason="temporarily blocked by https://github.com/pyro-ppl/funsor/pull/327")]),
    'minipyro',
    'numpy',
    'pyro',
])
@pytest.mark.xfail(reason='Not supported by backend.')
def test_model_sample(model, backend):
    pytest.importorskip(PACKAGE_NAME[backend])
    with pyro_backend(backend), handlers.seed(rng_seed=2):
        f = MODELS[model]()
        model, model_args, model_kwargs = f['model'], f.get('model_args', ()), f.get('model_kwargs', {})
        model(*model_args, **model_kwargs)


@pytest.mark.parametrize('model', MODELS)
@pytest.mark.parametrize('backend', [
    pytest.param("funsor", marks=[pytest.mark.xfail(reason="not implemented")]),
    'minipyro',
    'numpy',
    'pyro',
])
def test_trace_handler(model, backend):
    pytest.importorskip(PACKAGE_NAME[backend])
    with pyro_backend(backend), handlers.seed(rng_seed=2):
        f = MODELS[model]()
        model, model_args, model_kwargs = f['model'], f.get('model_args', ()), f.get('model_kwargs', {})
        # should be implemented
        handlers.trace(model).get_trace(*model_args, **model_kwargs)


@pytest.mark.parametrize('model', MODELS)
def test_register_backend(model):
    pytest.importorskip("pyro")
    register_backend("foo", {
        "infer": "pyro.contrib.minipyro",
        "optim": "pyro.contrib.minipyro",
        "pyro": "pyro.contrib.minipyro",
    })
    with pyro_backend("foo"):
        f = MODELS[model]()
        model, model_args, model_kwargs = f['model'], f.get('model_args', ()), f.get('model_kwargs', {})
        handlers.trace(model).get_trace(*model_args, **model_kwargs)
