""" SPPAM SPARSE tests

The sparse tests fail.  Set accept_sparse=True in sppam.py and fix SPPAM to allow the sparse tests to pass.

===============================================================
Author: Rolf Carlson, Carlson Research, LLC <hrolfrc@gmail.com>
License: 3-clause BSD
===============================================================

"""
import pytest
from scipy.sparse import issparse
from sklearn.feature_extraction.text import TfidfVectorizer

from sppam import SPPAM


@pytest.fixture
def sparse_data():
    """ Make a sparse classification problem for visual inspection. """

    text = [
        "It was the best of times",
        "it was the worst of times",
        "it was the age of wisdom",
        "it was the age of foolishness"
    ]

    X = TfidfVectorizer().fit_transform(text)
    # samples 0 and 2 are positive
    # samples 1 and 3 are negative
    y = [1, 0, 1, 0]

    return X, y


def test_sppam_sparse(sparse_data):
    X, y = sparse_data

    assert issparse(X) == True
    assert X.shape == (4, 10)

    # the sparse representation
    # (0, 4)	0.3169454420370736
    # (0, 1)	0.6073596130854014
    # (0, 5)	0.3169454420370736
    # (0, 7)	0.3169454420370736
    # (0, 3)	0.3169454420370736
    # (1, 9)	0.6073596130854014
    # (1, 6)	0.4788492951654494
    # (1, 4)	0.3169454420370736
    # (1, 5)	0.3169454420370736
    # (1, 7)	0.3169454420370736
    # (1, 3)	0.3169454420370736
    # (2, 8)	0.6073596130854014
    # (2, 0)	0.4788492951654494
    # (2, 4)	0.3169454420370736
    # (2, 5)	0.3169454420370736
    # (2, 7)	0.3169454420370736
    # (2, 3)	0.3169454420370736
    # (3, 2)	0.6073596130854014
    # (3, 0)	0.4788492951654494
    # (3, 4)	0.3169454420370736
    # (3, 5)	0.3169454420370736
    # (3, 7)	0.3169454420370736
    # (3, 3)	0.3169454420370736

    # the dense representation with 4 rows and 10 columns
    # assert repr(np.round(X.toarray(), 2)) == [
    #     [0., 0.61, 0., 0.32, 0.32, 0.32, 0.48, 0.32, 0., 0.],
    #     [0., 0., 0., 0.32, 0.32, 0.32, 0.48, 0.32, 0., 0.61],
    #     [0.48, 0., 0., 0.32, 0.32, 0.32, 0., 0.32, 0.61, 0.],
    #     [0.48, 0., 0.61, 0.32, 0.32, 0.32, 0., 0.32, 0., 0.]
    # ]

    clf = SPPAM()

    clf.fit(X, y)
    assert hasattr(clf, 'is_fitted_')
    assert hasattr(clf, 'classes_')
    assert hasattr(clf, 'X_')
    assert hasattr(clf, 'y_')

    # assert clf.auc_ == [0.5, 0.875, 1.0]
    assert clf.coef_ == [1, 1, -1, 0, 0, 0, 0, 0, 0, 0]

    y_pred = clf.predict(X)
    assert y_pred.shape == (X.shape[0],)
