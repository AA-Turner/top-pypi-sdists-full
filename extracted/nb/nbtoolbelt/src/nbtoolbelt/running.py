"""
Functions for running

Copyright (c) 2017 - Eindhoven University of Technology, The Netherlands

This software is made available under the terms of the MIT License.
"""

import sys
from argparse import Namespace

import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
from nbconvert.preprocessors.execute import CellExecutionError
from nbformat import NotebookNode

from .cleaning import clean_code_output, clean_code_metadata, truncate_output_streams

TEST = False


def ipc_kernel_manager_factory(ipc_path):
    try:
        from jupyter_client import AsyncKernelManager as _BaseKernelManager
    except ImportError:
        from jupyter_client import KernelManager as _BaseKernelManager

    class IPCKernelManager(_BaseKernelManager):
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
