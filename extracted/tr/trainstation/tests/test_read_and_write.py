import tempfile
import numpy as np
from trainstation import Optimizer, EnsembleOptimizer, CrossValidationEstimator
from trainstation import read_summary


def setup_Ay():
    # setup dummy objects
    N = 100
    M = 50

    A = np.random.random((N, M))
    y = np.random.normal(0, 1, (N,))
    return A, y


def test_write_opt_summary():

    # setup Optimizer
    A, y = setup_Ay()
    opt = Optimizer((A, y))
    opt.train()

    # write and read summary
    with tempfile.NamedTemporaryFile() as fd:
        opt.write_summary(fd.name)
        summary_read = read_summary(fd.name)

    # test that summary dicts are equal
    summary_ref = opt.summary
    for key, val in summary_ref.items():
        if isinstance(val, np.ndarray):
            assert np.allclose(val, summary_read[key])
        elif isinstance(val, float):
            assert np.isclose(summary_ref[key], summary_read[key])
        else:
            assert summary_ref[key] == summary_read[key]


def test_write_cve_summary():
    # setup CrossValidationEstimator
    A, y = setup_Ay()
    cve = CrossValidationEstimator((A, y))
    cve.train()
    cve.validate()

    # write and read summary
    with tempfile.NamedTemporaryFile() as fd:
        cve.write_summary(fd.name)
        summary_read = read_summary(fd.name)

    # test that summary dicts are equal
    summary_ref = cve.summary
    for key, val in summary_ref.items():
        if isinstance(val, np.ndarray):
            assert np.allclose(val, summary_read[key])
        elif isinstance(val, float):
            assert np.isclose(summary_ref[key], summary_read[key])
        else:
            assert summary_ref[key] == summary_read[key]


def test_write_eopt_summary():
    # setup CrossValidationEstimator
    A, y = setup_Ay()
    eopt = EnsembleOptimizer((A, y))
    eopt.train()

    # write and read summary
    with tempfile.NamedTemporaryFile() as fd:
        eopt.write_summary(fd.name)
        summary_read = read_summary(fd.name)

    # test that summary dicts are equal
    summary_ref = eopt.summary
    for key, val in summary_ref.items():
        if isinstance(val, np.ndarray):
            assert np.allclose(val, summary_read[key])
        elif isinstance(val, float):
            assert np.isclose(summary_ref[key], summary_read[key])
        else:
            assert summary_ref[key] == summary_read[key]
