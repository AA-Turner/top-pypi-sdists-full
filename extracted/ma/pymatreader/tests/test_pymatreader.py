# Copyright (c) 2018, Dirk Gütlin & Thomas Hartmann
# All rights reserved.
#
# This file is part of the pymatreader Project, see: https://gitlab.com/obob/pymatreader
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""Tests for pymatreader."""

from __future__ import annotations

import warnings
from pathlib import Path

import numpy as np
import pytest
from scipy import sparse

from pymatreader import read_mat

from .helper_functions import _read_xml_data, _sanitize_dict, assertDeepAlmostEqual

test_data_folder = 'tests/test_data'
testdata_v4_fname = 'v4.mat'
testdata_v6_fname = 'v6.mat'
testdata_v7_fname = 'v7.mat'
testdata_v73_fname = 'v73.mat'
testdata_xml = 'xmldata.xml'
testdata_ft_v7_fname = 'ft_v7.mat'
testdata_ft_v73_fname = 'ft_v73.mat'
testdata_eeglab_h5 = 'test_raw_h5.set'
testdata_eeglab_old = 'test_raw.set'
testdata_eeglab_epochs_h5 = 'test_epochs_onefile_h5.set'
testdata_eeglab_epochs = 'test_epochs_onefile.set'
testdata_cell_struct_v6 = 'cell_struct_v6.mat'
testdata_cell_struct_v7 = 'cell_struct_v7.mat'
testdata_cell_struct_v73 = 'cell_struct_v73.mat'
testdata_bti_v7 = 'bti_raw_v7.mat'
testdata_bti_v73 = 'bti_raw_v73.mat'
testdata_unsupported_classes_v7 = 'compare_datetime_with_and_without_time_zone_v7p0.mat'
testdata_unsupported_classes_v73 = 'compare_datetime_with_and_without_time_zone_v7p3.mat'

invalid_fname = 'invalid.mat'


def test_v4v7():
    """Test that the data is read correctly from very old and new mat versions."""
    v4_data = _sanitize_dict(read_mat(Path(test_data_folder, testdata_v4_fname)))
    v7_data = _sanitize_dict(read_mat(Path(test_data_folder, testdata_v7_fname)))

    del v7_data['a_second_cell_array']
    del v7_data['a_struct']
    del v7_data['a_unit64']
    del v7_data['a_cell_array']
    del v7_data['a_heading_cell_array']

    assertDeepAlmostEqual(v4_data, v7_data)


def test_v6v7():
    """Test that the data is read correctly from old and new mat versions."""
    v6_data = _sanitize_dict(read_mat(Path(test_data_folder, testdata_v6_fname)))
    v7_data = _sanitize_dict(read_mat(Path(test_data_folder, testdata_v7_fname)))

    assertDeepAlmostEqual(v6_data, v7_data)


def test_v6v73():
    """Test that the data is read correctly from old and new mat versions."""
    v6_data = _sanitize_dict(read_mat(Path(test_data_folder, testdata_v6_fname)))
    v73_data = _sanitize_dict(read_mat(Path(test_data_folder, testdata_v73_fname)))

    for key, val in v6_data.items():
        if '_complex_' in key:
            assert np.all(np.iscomplex(val))

    assertDeepAlmostEqual(v6_data, v73_data)


def test_v7v73():
    """Test that the data is read correctly from old and new mat versions."""
    v7_data = _sanitize_dict(read_mat(Path(test_data_folder, testdata_v7_fname)))
    v73_data = _sanitize_dict(read_mat(Path(test_data_folder, testdata_v73_fname)))

    for key, val in v7_data.items():
        if '_complex_' in key:
            assert np.all(np.iscomplex(val))

    for key, val in v73_data.items():
        if '_complex_' in key:
            assert np.all(np.iscomplex(val))

    assertDeepAlmostEqual(v7_data, v73_data)


def test_xmlv7():
    """Test that the XML data is read correctly from v7."""
    v7_data = _sanitize_dict(read_mat(Path(test_data_folder, testdata_v7_fname)))
    xml_data = _read_xml_data(Path(test_data_folder, testdata_xml))

    assertDeepAlmostEqual(v7_data, xml_data)


def test_ft_v7v73():
    """Test that the FieldTrip data is read correctly from old and new mat versions."""
    v7_data = _sanitize_dict(read_mat(Path(test_data_folder, testdata_ft_v7_fname), variable_names=('data_epoched',)))
    v73_data = _sanitize_dict(read_mat(Path(test_data_folder, testdata_ft_v73_fname), variable_names=('data_epoched',)))

    assertDeepAlmostEqual(v7_data, v73_data)


def test_bti_v7v73():
    """Test that the BTI data is read correctly from old and new mat versions."""
    v7_data = _sanitize_dict(read_mat(Path(test_data_folder, testdata_bti_v7), variable_names=('data',)))
    v73_data = _sanitize_dict(read_mat(Path(test_data_folder, testdata_bti_v73), variable_names=('data',)))

    assertDeepAlmostEqual(v7_data, v73_data)


def test_cell_struct_v6v7():
    """Test that the cell struct data is read correctly from old and new mat versions."""
    v6_data = _sanitize_dict(read_mat(Path(test_data_folder, testdata_cell_struct_v6)))
    v7_data = _sanitize_dict(read_mat(Path(test_data_folder, testdata_cell_struct_v7)))

    assertDeepAlmostEqual(v6_data, v7_data)


def test_cell_struct_v7v73():
    """Test that the cell struct data is read correctly from old and new mat versions."""
    v7_data = _sanitize_dict(read_mat(Path(test_data_folder, testdata_cell_struct_v7)))
    v73_data = _sanitize_dict(read_mat(Path(test_data_folder, testdata_cell_struct_v73)))

    assertDeepAlmostEqual(v7_data, v73_data)


def test_eeglab_v7v73():
    """Test that the EEGLab data is read correctly from old and new mat versions."""
    v7_data = _sanitize_dict(read_mat(Path(test_data_folder, testdata_eeglab_old)))

    v73_data = _sanitize_dict(read_mat(Path(test_data_folder, testdata_eeglab_h5)))

    assertDeepAlmostEqual(v7_data, v73_data)


def test_raw_h5_eeglab():
    """Test that the EEGLab data is read."""
    read_mat(Path(test_data_folder, testdata_eeglab_h5))


def test_raw_old_eeglab():
    """Test that the old EEGLab data is read."""
    read_mat(Path(test_data_folder, testdata_eeglab_old))


def test_raw_h5_eeglab_event_type():
    """Test that the event type of EEGLab data is read correctly."""
    data = read_mat(Path(test_data_folder, testdata_eeglab_h5))
    from .helper_functions.mne_eeglab_stuff import prepare_events_like_mne

    events = prepare_events_like_mne(data)

    first_event = events[0]
    assert first_event.type
    assert first_event.latency


def test_raw_old_eeglab_event_type():
    """Test that the event type of old EEGLab data is read correctly."""
    data = read_mat(Path(test_data_folder, testdata_eeglab_old))
    from .helper_functions.mne_eeglab_stuff import prepare_events_like_mne

    events = prepare_events_like_mne(data)
    first_event = events[0]
    assert first_event.type
    assert first_event.latency


def test_file_does_not_exist():
    """Test that an error is raised if the file does not exist."""
    with pytest.raises(IOError):
        read_mat(Path(test_data_folder, invalid_fname))


def test_files_with_unsupported_classesv7():
    """Test whether a warning is issued when we come across classes."""
    with warnings.catch_warnings(record=True) as w:
        read_mat(Path(test_data_folder, testdata_unsupported_classes_v7))

        has_warned = False

        for cur_warning in w:
            if str(cur_warning.message) == (
                'Complex objects (like classes) are not '
                'supported. They are imported on a best effort base '
                'but your mileage will vary.'
            ):
                has_warned = True

        assert has_warned


def test_files_with_unsupported_classesv73():
    """Test whether a warning is issued when we come across classes."""
    with warnings.catch_warnings(record=True) as w:
        read_mat(Path(test_data_folder, testdata_unsupported_classes_v73))

        has_warned = False

        for cur_warning in w:
            if str(cur_warning.message) == (
                'Complex objects (like classes) are not '
                'supported. They are imported on a best effort base '
                'but your mileage will vary.'
            ):
                has_warned = True

        assert has_warned


def test_eeglab_epochs():
    """Test reading eeglab epochs."""
    old_data = _sanitize_dict(read_mat(Path(test_data_folder, testdata_eeglab_epochs)))
    new_data = _sanitize_dict(read_mat(Path(test_data_folder, testdata_eeglab_epochs_h5)))

    assertDeepAlmostEqual(old_data, new_data)


@pytest.mark.parametrize('version', ['6', '7', '73'])
def test_string_issue(version):
    """Test that we warn if a string class if found."""
    with warnings.catch_warnings(record=True) as w:
        read_mat(Path(test_data_folder, f'string_v{version}.mat'))
        has_warned = False

        for cur_warning in w:
            if str(cur_warning.message) == (
                'pymatreader cannot import Matlab string variables. '
                'Please convert these variables to char arrays '
                'in Matlab.'
            ):
                has_warned = True

        assert has_warned


@pytest.mark.parametrize('version', ['6', '7', '73'])
def test_cell_with_group(version):
    """Test for cells with groups in them."""
    data = read_mat(Path(test_data_folder, f'struct_in_cell_v{version}.mat'))
    assert data['x']['test']['int'] == 4  # noqa PLR2004
    assert data['x']['test']['float'] == 3.2  # noqa PLR2004


@pytest.mark.parametrize('version', ['4', '6', '7', '73'])
def test_sparse_matrices(version):
    """Test that sparse matrices are read correctly."""
    data = read_mat(Path(test_data_folder, f'sparse_v{version}.mat'))

    N, Nel = data['N'], data['Nel']  # noqa: N806

    assert int(N) == N
    assert int(Nel) == Nel
    N, Nel = int(N), int(Nel)  # ensure they are integers  # noqa: N806

    # Special matrices
    A_empty = data['A_empty']  # noqa: N806
    assert A_empty.shape == (0, 0)
    assert A_empty.nnz == 0
    assert A_empty.dtype == np.float64

    A_single = data['A_single']  # noqa: N806
    assert A_single.shape == (1, 1)
    assert A_single.nnz == 1
    assert A_single.dtype == np.float64

    # Other matrices
    matrix_dim = 10
    assert N == matrix_dim  # noqa:SIM300
    assert Nel == matrix_dim // 2  # noqa:SIM300

    for empty in ['empty_', '']:
        for name in ['col', 'row', 'wide', 'square', 'tall']:
            mat_name = f'A_{empty}{name}'
            print(f'Checking matrix: {mat_name} (version {version})')

            assert mat_name in data

            # Get the sparse matrix
            matrix = data[mat_name]

            # Check that the matrix is a sparse matrix/array
            assert isinstance(matrix, sparse.sparray)

            # Check that the number of non-zero elements matches Nel
            if empty:
                assert matrix.nnz == 0
            else:
                assert matrix.nnz == Nel

            # Check that the data type is correct
            assert matrix.dtype == np.float64

            # Check the shape of the matrix
            mat_shapes = dict(
                col=(N, 1),
                row=(1, N),
                wide=(N, 2 * N),
                square=(N, N),
                tall=(2 * N, N)
            )

            assert matrix.shape == mat_shapes[name]

            # Check every single value of the matrix
            # Load the "true" data from the CSV file
            csv_matrix = np.loadtxt(
                Path(test_data_folder, f'sparse_{empty}{name}.csv'),
                delimiter=','
            ).reshape(mat_shapes[name])

            np.testing.assert_allclose(matrix.toarray(), csv_matrix, atol=1e-15)

