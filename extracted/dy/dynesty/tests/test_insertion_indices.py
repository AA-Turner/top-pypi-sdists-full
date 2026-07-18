import numpy as np
import pytest
import dynesty
import dynesty.utils as dyutil
from utils import get_rstate, get_printing

printing = get_printing()


def loglike(x):
    return -0.5 * np.sum(x**2)


def prior_transform(x):
    return (2 * x - 1) * 10


def test_insertion_indices_static_exact():
    rstate = get_rstate()
    sampler = dynesty.NestedSampler(loglike,
                                    prior_transform,
                                    ndim=2,
                                    nlive=80,
                                    rstate=rstate)
    sampler.run_nested(print_progress=printing, dlogz=0.2, add_live=True)
    res = sampler.results

    ins = dyutil.compute_insertion_indices_static(res)

    assert len(ins) == res.niter
    assert np.all(np.isfinite(ins))
    assert np.all(ins >= 0)
    assert np.all(ins <= res.nlive)


def test_insertion_indices_static_requires_final_live_in_strict_mode():
    rstate = get_rstate()
    sampler = dynesty.NestedSampler(loglike,
                                    prior_transform,
                                    ndim=2,
                                    nlive=60,
                                    rstate=rstate)
    sampler.run_nested(print_progress=printing, dlogz=0.2, add_live=False)
    res = sampler.results

    with pytest.raises(ValueError, match='final live points'):
        dyutil.compute_insertion_indices_static(res, strict=True)

    ins = dyutil.compute_insertion_indices_static(res, strict=False)
    assert len(ins) == res.niter
    assert np.any(np.isfinite(ins))
    assert np.any(np.isnan(ins))


def test_insertion_indices_all_samples_static():
    rstate = get_rstate()
    sampler = dynesty.NestedSampler(loglike,
                                    prior_transform,
                                    ndim=2,
                                    nlive=50,
                                    rstate=rstate)
    sampler.run_nested(print_progress=printing, dlogz=0.2, add_live=True)
    res = sampler.results

    ins_dead = dyutil.compute_insertion_indices_static(res)
    ins_all = dyutil.compute_insertion_indices(res)

    assert len(ins_all) == len(res.logl)
    assert np.allclose(ins_all[:res.niter], ins_dead)
    assert np.all(np.isnan(ins_all[res.niter:]))


def test_insertion_indices_all_samples_dynamic():
    rstate = get_rstate()
    sampler = dynesty.DynamicNestedSampler(loglike,
                                           prior_transform,
                                           ndim=2,
                                           nlive=50,
                                           rstate=rstate)
    sampler.run_nested(print_progress=printing,
                       maxiter_init=100,
                       maxiter_batch=80,
                       maxbatch=2)
    res = sampler.results
    ins_all = dyutil.compute_insertion_indices(res)

    assert len(ins_all) == len(res.logl)
    assert np.any(np.isfinite(ins_all))
    assert np.any(np.isnan(ins_all))

    for batch_id in np.unique(res.samples_batch):
        sel = (res.samples_batch == batch_id)
        idx = np.nonzero(sel)[0]
        nsamp_batch = int(np.sum(sel))
        nlive_batch = int(res.batch_nlive[int(batch_id)])
        niter_batch = nsamp_batch - nlive_batch
        samples_it_local = np.asarray(res.samples_it[sel], dtype=int)
        samples_it_local = samples_it_local - samples_it_local.min()
        static_like = dyutil.Results(
            dict(nlive=nlive_batch,
                 niter=niter_batch,
                 ncall=res.ncall[sel],
                 eff=float(100. * nsamp_batch / np.sum(res.ncall[sel])),
                 samples=res.samples[sel],
                 samples_id=res.samples_id[sel],
                 samples_it=samples_it_local,
                 samples_u=res.samples_u[sel],
                 blob=res.blob[sel],
                 logwt=res.logwt[sel],
                 logl=res.logl[sel],
                 logvol=res.logvol[sel],
                 logz=res.logz[sel],
                 logzerr=res.logzerr[sel],
                 information=res.information[sel]))
        ins_batch = dyutil.compute_insertion_indices_static(static_like)
        assert np.allclose(ins_all[idx[:len(ins_batch)]], ins_batch)
        assert np.all(np.isnan(ins_all[idx[len(ins_batch):]]))
