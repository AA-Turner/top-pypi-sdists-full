"""utils test"""

import contextlib
import io
import json
import logging
import os
import pathlib
import platform
import random
import re
import shutil
import stat
import string
import tempfile
from test import check_present, mark_windows_only, raises_nested
from unittest import mock

import numpy as np
import pytest

from cmdstanpy import _DOT_CMDSTAN, _TMPDIR
from cmdstanpy.model import CmdStanModel
from cmdstanpy.progress import _disable_progress, allow_show_progress
from cmdstanpy.utils import (
    EXTENSION,
    SanitizedOrTmpFilePath,
    check_sampler_csv,
    cmdstan_path,
    cmdstan_version,
    cmdstan_version_before,
    do_command,
    flatten_chains,
    get_latest_cmdstan,
    install_cmdstan,
    parse_rdump_value,
    pushd,
    read_metric,
    rload,
    set_cmdstan_path,
    stancsv,
    validate_cmdstan_path,
    validate_dir,
    windows_short_path,
)
from cmdstanpy.utils.filesystem import temp_inits, temp_single_json

HERE = os.path.dirname(os.path.abspath(__file__))
DATAFILES_PATH = os.path.join(HERE, 'data')
BERN_STAN = os.path.join(DATAFILES_PATH, 'bernoulli.stan')
BERN_DATA = os.path.join(DATAFILES_PATH, 'bernoulli.data.json')
BERN_EXE = os.path.join(DATAFILES_PATH, 'bernoulli' + EXTENSION)


def test_default_path() -> None:
    if 'CMDSTAN' in os.environ:
        assert os.path.samefile(cmdstan_path(), os.environ['CMDSTAN'])
        path = os.environ['CMDSTAN']
        with mock.patch.dict("os.environ"):
            del os.environ['CMDSTAN']
            set_cmdstan_path(path)
            assert os.path.samefile(cmdstan_path(), path)
            assert 'CMDSTAN' in os.environ
    else:
        cmdstan_dir = os.path.expanduser(os.path.join('~', _DOT_CMDSTAN))
        install_version = os.path.join(
            cmdstan_dir, get_latest_cmdstan(cmdstan_dir)
        )
        assert os.path.samefile(cmdstan_path(), install_version)
        assert 'CMDSTAN' in os.environ


@pytest.mark.parametrize("bad_dir", ["bad dir", "bad~dir"])
@pytest.mark.parametrize("bad_name", ["bad name", "bad~name"])
def test_non_special_chars_location(bad_dir: str, bad_name: str) -> None:
    with tempfile.TemporaryDirectory(
        prefix="cmdstan_tests", dir=_TMPDIR
    ) as tmpdir:
        good_path = os.path.join(tmpdir, 'good_dir')
        os.mkdir(good_path)
        with SanitizedOrTmpFilePath(good_path) as (pth, is_changed):
            assert os.path.samefile(pth, good_path)
            assert not is_changed

        # prepare files for test
        bad_path = os.path.join(tmpdir, bad_dir)
        os.makedirs(bad_path, exist_ok=True)
        stan = os.path.join(DATAFILES_PATH, 'bernoulli.stan')
        stan_bad = os.path.join(bad_path, bad_name)
        shutil.copy(stan, stan_bad)

        stan_copied = None
        try:
            with SanitizedOrTmpFilePath(stan_bad) as (pth, is_changed):
                stan_copied = pth
                assert os.path.exists(stan_copied)
                assert ' ' not in stan_copied

                # Determine if the file should have been copied, i.e., we either
                # are on a unix-ish system or on windows, the path contains a
                # space, and there is no short path.
                if platform.system() == 'Windows':
                    should_change = ' ' in bad_name or (
                        ' ' in bad_path
                        and not os.path.exists(windows_short_path(bad_path))
                    )
                else:
                    should_change = True
                    assert '~' not in stan_copied

                assert is_changed == should_change
                raise RuntimeError
        except RuntimeError:
            pass

        if platform.system() != 'Windows':
            assert not os.path.exists(stan_copied)

        # cleanup after test
        shutil.rmtree(good_path, ignore_errors=True)
        shutil.rmtree(bad_path, ignore_errors=True)


def test_set_path() -> None:
    if 'CMDSTAN' in os.environ:
        assert os.path.samefile(cmdstan_path(), os.environ['CMDSTAN'])
    else:
        cmdstan_dir = os.path.expanduser(os.path.join('~', _DOT_CMDSTAN))
        install_version = os.path.join(
            cmdstan_dir, get_latest_cmdstan(cmdstan_dir)
        )
        set_cmdstan_path(install_version)
        assert os.path.samefile(install_version, cmdstan_path())
        assert os.path.samefile(install_version, os.environ['CMDSTAN'])


def test_validate_path() -> None:
    if 'CMDSTAN' in os.environ:
        install_version = os.environ.get('CMDSTAN')
    else:
        cmdstan_dir = os.path.expanduser(os.path.join('~', _DOT_CMDSTAN))

        install_version = os.path.join(
            cmdstan_dir, get_latest_cmdstan(cmdstan_dir)
        )

    set_cmdstan_path(install_version)
    validate_cmdstan_path(install_version)
    path_foo = os.path.abspath(os.path.join('releases', 'foo'))
    with pytest.raises(ValueError, match='No CmdStan directory'):
        validate_cmdstan_path(path_foo)

    folder_name = ''.join(
        random.choice(string.ascii_letters) for _ in range(10)
    )
    while os.path.exists(folder_name):
        folder_name = ''.join(
            random.choice(string.ascii_letters) for _ in range(10)
        )
    folder = pathlib.Path(folder_name)
    folder.mkdir(parents=True)
    (folder / "makefile").touch()

    with pytest.raises(ValueError, match='missing binaries'):
        validate_cmdstan_path(str(folder.absolute()))
    shutil.rmtree(folder)


def test_validate_dir() -> None:
    with tempfile.TemporaryDirectory(
        prefix="cmdstan_tests", dir=_TMPDIR
    ) as tmpdir:
        path = os.path.join(tmpdir, 'cmdstan-M.m.p')
        assert not os.path.exists(path)
        validate_dir(path)
        assert os.path.exists(path)

        _, file = tempfile.mkstemp(dir=_TMPDIR)
        with pytest.raises(Exception, match='File exists'):
            validate_dir(file)

        if platform.system() != 'Windows':
            with pytest.raises(Exception, match='Cannot create directory'):
                dir = tempfile.mkdtemp(dir=_TMPDIR)
                os.chmod(dir, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)
                validate_dir(os.path.join(dir, 'cmdstan-M.m.p'))


def test_munge_cmdstan_versions() -> None:
    with tempfile.TemporaryDirectory(
        prefix="cmdstan_tests", dir=_TMPDIR
    ) as tmpdir:
        tdir = os.path.join(tmpdir, 'tmpdir_xxx')
        os.makedirs(tdir)
        os.makedirs(os.path.join(tdir, 'cmdstan-2.22.0-rc1'))
        os.makedirs(os.path.join(tdir, 'cmdstan-2.22.0-rc2'))
        assert get_latest_cmdstan(tdir) == 'cmdstan-2.22.0-rc2'

        os.makedirs(os.path.join(tdir, 'cmdstan-2.22.0'))
        assert get_latest_cmdstan(tdir) == 'cmdstan-2.22.0'


def test_cmdstan_version_before() -> None:
    cmdstan_path()  # sets os.environ['CMDSTAN']
    assert cmdstan_version_before(99, 99)
    assert not cmdstan_version_before(1, 1)


def test_cmdstan_version(caplog: pytest.LogCaptureFixture) -> None:
    with tempfile.TemporaryDirectory(
        prefix="cmdstan_tests", dir=_TMPDIR
    ) as tmpdir:
        tdir = pathlib.Path(tmpdir) / 'tmpdir_xxx'
        fake_path = tdir / 'cmdstan-2.22.0'
        fake_bin = fake_path / 'bin'
        fake_bin.mkdir(parents=True)
        fake_makefile = fake_path / 'makefile'
        fake_makefile.touch()
        (fake_bin / f'stanc{EXTENSION}').touch()
        with mock.patch.dict("os.environ", CMDSTAN=str(fake_path)):
            assert str(fake_path) == cmdstan_path()
            with open(fake_makefile, 'w') as fd:
                fd.write('...  CMDSTAN_VERSION := dont_need_no_mmp\n\n')
            expect = (
                'Cannot parse version, expected "<major>.<minor>.<patch>", '
                'found: "dont_need_no_mmp".'
            )
            with caplog.at_level(logging.INFO):
                cmdstan_version()
            check_present(caplog, ('cmdstanpy', 'INFO', expect))

            fake_makefile.unlink()
            expect = (
                'CmdStan installation {} missing makefile, '
                'cannot get version.'.format(fake_path)
            )
            with caplog.at_level(logging.INFO):
                cmdstan_version()
            check_present(caplog, ('cmdstanpy', 'INFO', expect))
    cmdstan_path()


def test_dict_to_file() -> None:
    file_good = os.path.join(DATAFILES_PATH, 'bernoulli_output_1.csv')
    dict_good = {'a': 0.5}
    created_tmp = None

    with temp_single_json(file_good) as fg1:
        assert os.path.exists(fg1)
    assert os.path.exists(file_good)

    with temp_single_json(dict_good) as fg2:
        assert os.path.exists(fg2)
        with open(fg2) as fg2_d:
            assert json.load(fg2_d) == dict_good
        created_tmp = fg2

    assert not os.path.exists(created_tmp)

    with pytest.raises(AttributeError):
        with temp_single_json(123) as _:
            pass


def test_temp_inits():
    dict_good = {'a': 0.5}
    with temp_inits([dict_good, dict_good]) as base_file:
        fg1 = base_file[:-5] + '_1.json'
        fg2 = base_file[:-5] + '_2.json'
        assert os.path.exists(fg1)
        assert os.path.exists(fg2)
        with open(fg1) as fg1_d:
            assert json.load(fg1_d) == dict_good
        with open(fg2) as fg2_d:
            assert json.load(fg2_d) == dict_good
        created_tmp = (fg1, fg2)

    assert not os.path.exists(created_tmp[0])
    assert not os.path.exists(created_tmp[1])

    with pytest.raises(ValueError):
        with temp_inits([123]) as _:
            pass

    with pytest.raises(ValueError):
        with temp_inits([dict_good], allow_multiple=False) as _:
            pass


def test_check_sampler_csv_1() -> None:
    csv_good = os.path.join(DATAFILES_PATH, 'bernoulli_output_1.csv')
    dict = check_sampler_csv(
        path=csv_good,
        is_fixed_param=False,
        iter_warmup=100,
        iter_sampling=10,
        thin=1,
    )
    assert 'bernoulli_model' == dict['model']
    assert 10 == dict['num_samples']
    assert 10 == dict['draws_sampling']
    assert 8 == len(dict['column_names'])

    with raises_nested(ValueError, 'config error, expected thin = 2'):
        check_sampler_csv(
            path=csv_good, iter_warmup=100, iter_sampling=20, thin=2
        )
    with raises_nested(ValueError, 'config error, expected save_warmup'):
        check_sampler_csv(
            path=csv_good,
            iter_warmup=100,
            iter_sampling=10,
            save_warmup=True,
        )
    with raises_nested(ValueError, 'expected 1000 draws'):
        check_sampler_csv(path=csv_good, iter_warmup=100)


def test_check_sampler_csv_2() -> None:
    csv_bad = os.path.join(DATAFILES_PATH, 'no_such_file.csv')
    with pytest.raises(Exception):
        check_sampler_csv(csv_bad)


def test_check_sampler_csv_3() -> None:
    csv_bad = os.path.join(DATAFILES_PATH, 'output_bad_cols.csv')
    with raises_nested(Exception, '8 items'):
        check_sampler_csv(csv_bad)


def test_check_sampler_csv_4() -> None:
    csv_bad = os.path.join(DATAFILES_PATH, 'output_bad_rows.csv')
    with raises_nested(Exception, 'found 9'):
        check_sampler_csv(csv_bad)


def test_check_sampler_csv_metric_1() -> None:
    csv_bad = os.path.join(DATAFILES_PATH, 'output_bad_metric_1.csv')
    with raises_nested(Exception, 'expecting metric'):
        check_sampler_csv(csv_bad)


def test_check_sampler_csv_metric_2() -> None:
    csv_bad = os.path.join(DATAFILES_PATH, 'output_bad_metric_2.csv')
    with raises_nested(Exception, 'invalid step size'):
        check_sampler_csv(csv_bad)


def test_check_sampler_csv_metric_3() -> None:
    csv_bad = os.path.join(DATAFILES_PATH, 'output_bad_metric_3.csv')
    with raises_nested(
        Exception, 'invalid or missing mass matrix specification'
    ):
        check_sampler_csv(csv_bad)


def test_check_sampler_csv_metric_4() -> None:
    csv_bad = os.path.join(DATAFILES_PATH, 'output_bad_metric_4.csv')
    with raises_nested(
        Exception, 'invalid or missing mass matrix specification'
    ):
        check_sampler_csv(csv_bad)


def test_check_sampler_csv_thin() -> None:
    stan = os.path.join(DATAFILES_PATH, 'bernoulli.stan')
    bern_model = CmdStanModel(stan_file=stan)
    bern_model.compile()
    jdata = os.path.join(DATAFILES_PATH, 'bernoulli.data.json')
    bern_fit = bern_model.sample(
        data=jdata,
        chains=1,
        parallel_chains=1,
        seed=12345,
        iter_sampling=490,
        iter_warmup=490,
        thin=7,
        max_treedepth=11,
        adapt_delta=0.98,
    )
    csv_file = bern_fit.runset.csv_files[0]
    dict = check_sampler_csv(
        path=csv_file,
        is_fixed_param=False,
        iter_sampling=490,
        iter_warmup=490,
        thin=7,
    )
    assert dict['num_samples'] == 490
    assert dict['thin'] == 7
    assert dict['draws_sampling'] == 70
    assert dict['seed'] == 12345
    assert dict['max_depth'] == 11
    assert dict['delta'] == 0.98

    with raises_nested(ValueError, 'config error'):
        check_sampler_csv(
            path=csv_file,
            is_fixed_param=False,
            iter_sampling=490,
            iter_warmup=490,
            thin=9,
        )
    with raises_nested(ValueError, 'expected 490 draws, found 70'):
        check_sampler_csv(
            path=csv_file,
            is_fixed_param=False,
            iter_sampling=490,
            iter_warmup=490,
        )


def test_metric_json_vec() -> None:
    metric_file = os.path.join(DATAFILES_PATH, 'metric_diag.data.json')
    assert read_metric(metric_file) == [3]


def test_metric_json_matrix() -> None:
    metric_file = os.path.join(DATAFILES_PATH, 'metric_dense.data.json')
    assert read_metric(metric_file) == [3, 3]


def test_metric_rdump_vec() -> None:
    metric_file = os.path.join(DATAFILES_PATH, 'metric_diag.data.R')
    assert read_metric(metric_file) == [3]


def test_metric_rdump_matrix() -> None:
    metric_file = os.path.join(DATAFILES_PATH, 'metric_dense.data.R')
    assert read_metric(metric_file) == [3, 3]


def test_metric_json_bad() -> None:
    metric_file = os.path.join(DATAFILES_PATH, 'metric_bad.data.json')
    with pytest.raises(Exception, match='bad or missing entry "inv_metric"'):
        read_metric(metric_file)


def test_metric_rdump_bad_1() -> None:
    metric_file = os.path.join(DATAFILES_PATH, 'metric_bad_1.data.R')
    with pytest.raises(Exception, match='bad or missing entry "inv_metric"'):
        read_metric(metric_file)


def test_metric_rdump_bad_2() -> None:
    metric_file = os.path.join(DATAFILES_PATH, 'metric_bad_2.data.R')
    with pytest.raises(Exception, match='bad or missing entry "inv_metric"'):
        read_metric(metric_file)


def test_metric_missing() -> None:
    metric_file = os.path.join(DATAFILES_PATH, 'no_such_file.json')
    with pytest.raises(Exception, match='No such file or directory'):
        read_metric(metric_file)


@mark_windows_only
def test_windows_short_path_directory() -> None:
    with tempfile.TemporaryDirectory(
        prefix="cmdstan_tests", dir=_TMPDIR
    ) as tmpdir:
        original_path = os.path.join(tmpdir, 'new path')
        os.makedirs(original_path, exist_ok=True)
        assert os.path.exists(original_path)
        assert ' ' in original_path
        short_path = windows_short_path(original_path)
        assert os.path.exists(short_path)
        assert original_path != short_path
        assert ' ' not in short_path


@mark_windows_only
def test_windows_short_path_file() -> None:
    with tempfile.TemporaryDirectory(
        prefix="cmdstan_tests", dir=_TMPDIR
    ) as tmpdir:
        original_path = os.path.join(tmpdir, 'new path', 'my_file.csv')
        os.makedirs(os.path.split(original_path)[0], exist_ok=True)
        assert os.path.exists(os.path.split(original_path)[0])
        assert ' ' in original_path
        assert os.path.splitext(original_path)[1] == '.csv'
        short_path = windows_short_path(original_path)
        assert os.path.exists(os.path.split(short_path)[0])
        assert original_path != short_path
        assert ' ' not in short_path
        assert os.path.splitext(short_path)[1] == '.csv'


@mark_windows_only
def test_windows_short_path_file_with_space() -> None:
    """Test that the function doesn't touch filename."""
    with tempfile.TemporaryDirectory(
        prefix="cmdstan_tests", dir=_TMPDIR
    ) as tmpdir:
        original_path = os.path.join(tmpdir, 'new path', 'my file.csv')
        os.makedirs(os.path.split(original_path)[0], exist_ok=True)
        assert os.path.exists(os.path.split(original_path)[0])
        assert ' ' in original_path
        short_path = windows_short_path(original_path)
        assert os.path.exists(os.path.split(short_path)[0])
        assert original_path != short_path
        assert ' ' in short_path
        assert os.path.splitext(short_path)[1] == '.csv'


def test_rload_metric() -> None:
    dfile = os.path.join(DATAFILES_PATH, 'metric_diag.data.R')
    data_dict = rload(dfile)
    assert data_dict['inv_metric'].shape == (3,)

    dfile = os.path.join(DATAFILES_PATH, 'metric_dense.data.R')
    data_dict = rload(dfile)
    assert data_dict['inv_metric'].shape == (3, 3)


def test_rload_data() -> None:
    dfile = os.path.join(DATAFILES_PATH, 'rdump_test.data.R')
    data_dict = rload(dfile)
    assert data_dict['N'] == 128
    assert data_dict['M'] == 2
    assert data_dict['x'].shape == (128, 2)


def test_rload_jags_data() -> None:
    dfile = os.path.join(DATAFILES_PATH, 'rdump_jags.data.R')
    data_dict = rload(dfile)
    assert data_dict['N'] == 128
    assert data_dict['M'] == 2
    assert data_dict['y'].shape == (128,)


def test_rload_wrong_data() -> None:
    dfile = os.path.join(DATAFILES_PATH, 'metric_diag.data.json')
    data_dict = rload(dfile)
    assert data_dict is None


def test_rload_bad_data_1() -> None:
    dfile = os.path.join(DATAFILES_PATH, 'rdump_bad_1.data.R')
    with pytest.raises(ValueError):
        rload(dfile)


def test_rload_bad_data_2() -> None:
    dfile = os.path.join(DATAFILES_PATH, 'rdump_bad_2.data.R')
    with pytest.raises(ValueError):
        rload(dfile)


def test_rload_bad_data_3() -> None:
    dfile = os.path.join(DATAFILES_PATH, 'rdump_bad_3.data.R')
    with pytest.raises(ValueError):
        rload(dfile)


def test_parse_rdump_value() -> None:
    struct1 = 'structure(c(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16),.Dim=c(2,8))'
    v_struct1 = parse_rdump_value(struct1)
    assert v_struct1.shape == (2, 8)
    assert v_struct1[1, 0] == 2
    assert v_struct1[0, 7] == 15

    struct2 = (
        'structure(c(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16),.Dim=c(1,16))'
    )
    v_struct2 = parse_rdump_value(struct2)
    assert v_struct2.shape == (1, 16)

    struct3 = 'structure(c(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16),.Dim=c(8,2))'
    v_struct3 = parse_rdump_value(struct3)
    assert v_struct3.shape == (8, 2)
    assert v_struct3[1, 0] == 2
    assert v_struct3[7, 0] == 8
    assert v_struct3[0, 1] == 9
    assert v_struct3[6, 1] == 15


def test_capture_console() -> None:
    tmp = io.StringIO()
    do_command(cmd=['ls'], cwd=HERE, fd_out=tmp)
    assert 'test_utils.py' in tmp.getvalue()


def test_exit() -> None:
    sys_stdout = io.StringIO()
    with contextlib.redirect_stdout(sys_stdout):
        args = ['bash', '/bin/junk']
        with pytest.raises(RuntimeError):
            do_command(args, HERE)


def test_restore_cwd() -> None:
    "Ensure do_command in a different cwd restores cwd after error."
    cwd = os.getcwd()
    with pytest.raises(RuntimeError):
        with pushd(os.path.dirname(cwd)):
            raise RuntimeError('error')
    assert cwd == os.getcwd()


def test_good() -> None:
    array_3d = np.empty((200, 4, 4))
    vals = [1.0, 2.0, 3.0, 4.0]
    pos = [(0, 0, 0), (0, 1, 1), (0, 2, 2), (0, 3, 3)]
    draws, chains, cols = zip(*pos)
    array_3d[draws, chains, cols] = vals
    flattened = flatten_chains(array_3d)

    assert flattened.shape == (800, 4)
    assert flattened[0, 0] == 1.0
    assert flattened[200, 1] == 2.0
    assert flattened[400, 2] == 3.0
    assert flattened[600, 3] == 4.0


def test_bad() -> None:
    array_2d = np.empty((200, 4))
    with pytest.raises(ValueError, match='Expecting 3D array'):
        flatten_chains(array_2d)


def test_bad_version(caplog: pytest.LogCaptureFixture) -> None:
    with caplog.at_level(logging.WARNING):
        assert not install_cmdstan(version="0.00.0")
    check_present(
        caplog,
        (
            'cmdstanpy',
            'WARNING',
            re.compile(r"CmdStan installation failed.\nVersion"),
        ),
    )


def test_interactive_extra_args(caplog: pytest.LogCaptureFixture) -> None:
    with caplog.at_level(logging.WARNING):
        assert not install_cmdstan(version="2.29.2", interactive=True)
    check_present(
        caplog,
        (
            'cmdstanpy',
            'WARNING',
            "Interactive installation requested but other arguments"
            " were used.\n\tThese values will be ignored!",
        ),
    )


# this test must run after any tests that check tqdm progress bars
@pytest.mark.order(-1)
def test_show_progress_fns(caplog: pytest.LogCaptureFixture) -> None:
    assert allow_show_progress()
    with caplog.at_level(logging.ERROR):
        logging.getLogger()
        try:
            raise ValueError("error")
        except ValueError as e:
            _disable_progress(e)
    check_present(
        caplog,
        (
            'cmdstanpy',
            'ERROR',
            'Error in progress bar initialization:\n'
            '\terror\n'
            'Disabling progress bars for this session',
        ),
    )
    assert not allow_show_progress()
    try:
        raise ValueError("error")
    except ValueError as e:
        caplog.clear()
        with caplog.at_level(logging.DEBUG):
            logging.getLogger()
            _disable_progress(e)
    msgs = ' '.join(caplog.messages)
    # msg should only be printed once per session - check not found
    assert 'Disabling progress bars for this session' not in msgs
    assert not allow_show_progress()


def test_munge_varnames() -> None:
    var = 'y'
    assert stancsv.munge_varname(var) == 'y'
    var = 'y.2'
    assert stancsv.munge_varname(var) == 'y[2]'
    var = 'y.2.3'
    assert stancsv.munge_varname(var) == 'y[2,3]'

    var = 'y:2'
    assert stancsv.munge_varname(var) == 'y.2'
    var = 'y:2:3'
    assert stancsv.munge_varname(var) == 'y.2.3'
    var = 'y:2.1'
    assert stancsv.munge_varname(var) == 'y.2[1]'
    var = 'y.1:2'
    assert stancsv.munge_varname(var) == 'y[1].2'

    var = 'y.2.3:1.2:5:6'
    assert stancsv.munge_varname(var) == 'y[2,3].1[2].5.6'
