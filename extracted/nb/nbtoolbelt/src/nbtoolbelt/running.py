"""
Functions for running

Copyright (c) 2017 - Eindhoven University of Technology, The Netherlands

This software is made available under the terms of the MIT License.
"""

import os
import sys
import tempfile
from argparse import Namespace
from typing import Any

import nbformat
from nbclient.exceptions import CellExecutionError
from nbconvert.preprocessors import ExecutePreprocessor
from nbformat import NotebookNode

from .cleaning import clean_code_output, clean_code_metadata, truncate_output_streams

TEST = False


def ensure_secure_tempdir() -> None:
    """Use a temp directory where Jupyter connection files can be chmodded."""
    probe_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False) as probe:
            probe_path = probe.name
        os.chmod(probe_path, 0o600)
        if os.stat(probe_path).st_mode & 0o777 != 0o600:
            tempfile.tempdir = '/tmp'
    except OSError:
        tempfile.tempdir = '/tmp'
    finally:
        if probe_path:
            try:
                os.remove(probe_path)
            except OSError:
                pass


def ipc_kernel_manager_factory(ipc_path):
    try:
        from jupyter_client.manager import AsyncKernelManager
        base_kernel_manager: type[Any] = AsyncKernelManager
    except ImportError:
        from jupyter_client.manager import KernelManager
        base_kernel_manager = KernelManager

    class IPCKernelManager(base_kernel_manager):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, transport='ipc', ip=ipc_path, **kwargs)

    return IPCKernelManager


def run_nb(nb: NotebookNode, args: Namespace) -> None:
    """Run notebook.

    .. note:: **Modifies**: ``nb``

    :param nb: notebook to run
    :param args: arguments (options)
    """
    # clean up before execution
    if args.clean_before:
        clean_code_output(nb)
        clean_code_metadata(nb, args.clean_before_metadata)

    if args.append_cell:
        nb.cells.append(nbformat.v4.new_code_cell(args.appended_cell))

    ep_kwargs = {
        'timeout': args.timeout,
        'allow_errors': args.allow_errors,
        'interrupt_on_timeout': args.interrupt_on_timeout,
        'record_timing': args.record_timing,
    }

    if args.ipc:
        ep_kwargs['kernel_manager_class'] = ipc_kernel_manager_factory(args.ipc)
    if args.kernel_name:
        ep_kwargs['kernel_name'] = args.kernel_name

    # run notebook
    ensure_secure_tempdir()
    ep = ExecutePreprocessor(**ep_kwargs)
    try:
        resources = {'metadata': {'path': args.run_path}}  # set working directory
        _ = ep.preprocess(nb, resources)  # nb is executed in-place, locally
    except (CellExecutionError, TimeoutError) as e:  # only possible if not args.allow_errors or if timeout
        if getattr(args, 'assert'):  # args.assert gives syntax error
            raise
        else:
            print('{}: {}'.format(type(e).__name__, e), file=sys.stderr)
    finally:
        # clean up after execution
        if args.clean_after:
            clean_code_metadata(nb, args.clean_after_metadata)

        if args.streams_head >= 0:
            truncate_output_streams(nb, args)
