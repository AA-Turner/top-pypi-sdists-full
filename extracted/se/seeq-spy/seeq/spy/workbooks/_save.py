from __future__ import annotations

import os
import tempfile
import zipfile
from pathlib import Path
from typing import List, Optional, Union

from seeq.base import util
from seeq.spy import _common
from seeq.spy._errors import *
from seeq.spy._status import Status
from seeq.spy.workbooks._workbook import Workbook, WorkbookList


@Status.top_level_spy_function(no_session=True)
def save(
        workbooks: Union[Workbook, List[Workbook], WorkbookList],
        folder_or_zipfile: Optional[Union[str, Path]] = None,
        *,
        datasource_map_folder: Optional[Union[str, Path]] = None,
        include_rendered_content: bool = False,
        pretty_print_html: bool = False,
        overwrite: bool = False,
        errors: Optional[str] = None,
        quiet: Optional[bool] = None,
        status: Optional[Status] = None
):
    """

    Saves a list of workbooks to a folder on disk from Workbook objects in
    memory.

    Parameters
    ----------
    workbooks : {Workbook, list[Workbook], WorkbookList}
        A Workbook object, list of Workbook objects, or WorkbookList to save.

    folder_or_zipfile : {str, pathlib.Path}, default os.getcwd()
        A folder or zip file on disk to which to save the workbooks. It will
        be saved as a "flat" set of subfolders, no other hierarchy will be
        created. The string must end in ".zip" to cause a zip file to be
        created instead of a folder.

    datasource_map_folder : {str, pathlib.Path}, default None
        Specifies a curated set of datasource maps that should accompany the
        workbooks (as opposed to the default maps that were created during the
        spy.workbooks.pull call).

    include_rendered_content : bool, default False
        If True, creates a folder called RenderedTopic within each Topic
        Document folder that includes the embedded content such that you can
        load it in an offline browser. You are required to have pulled the
        workbooks with include_rendered_content=True.

    pretty_print_html : bool, default False
        If True, this function will re-format the HTML of Topic Documents
        and Journals so that it is easy to read in a text editor. If False, the
        HTML will be written exactly as it is stored in Seeq Server. Note that
        setting this to True can cause some minor deviations in rendering after
        a round-trip (i.e. pull/save/load/push).

    overwrite : bool, default False
        If True, will overwrite any existing folder or zip file.

    errors : {'raise', 'catalog'}, default 'raise'
        If 'raise', any errors encountered will cause an exception. If
        'catalog', errors will be added to a 'Result' column in the status.df
        DataFrame (errors='catalog' must be combined with
        status=<Status object>).

    quiet : bool
        If True, suppresses progress output. Note that when status is
        provided, the quiet setting of the Status object that is passed
        in takes precedence.

    status : spy.Status, optional
        If specified, the supplied Status object will be updated as the command
        progresses. It gets filled in with the same information you would see
        in Jupyter in the blue/green/red table below your code while the
        command is executed.
    """
    if not folder_or_zipfile:
        folder_or_zipfile = os.getcwd()

    folder_or_zipfile = os.path.normpath(folder_or_zipfile)

    if not isinstance(workbooks, list):
        workbooks = [workbooks]

    if folder_or_zipfile is None:
        folder_or_zipfile = os.getcwd()

    if not os.path.isabs(folder_or_zipfile):
        folder_or_zipfile = util.safe_abspath(folder_or_zipfile)

    zip_it = folder_or_zipfile.lower().endswith('.zip')

    datasource_maps = None if datasource_map_folder is None else Workbook.load_datasource_maps(
        datasource_map_folder)

    if util.safe_isfile(folder_or_zipfile):
        if overwrite:
            util.safe_remove(folder_or_zipfile)
        else:
            raise SPyRuntimeError(
                f'"{folder_or_zipfile}" already exists. Use overwrite=True to overwrite.')

    save_folder = None
    try:
        save_folder = tempfile.mkdtemp() if zip_it else folder_or_zipfile

        for workbook in workbooks:  # type: Workbook
            if not isinstance(workbook, Workbook):
                raise SPyTypeError('workbooks argument must be a list of Workbook objects')

            workbook_folder_name = '%s (%s)' % (workbook.name, workbook.id)
            workbook_folder = os.path.join(save_folder, util.cleanse_filename(workbook_folder_name))
            workbook_folder = util.cleanse_path(workbook_folder)

            if datasource_maps is not None:
                workbook.datasource_maps = datasource_maps

            status.update('Saving to "%s"' % workbook_folder, Status.RUNNING)
            workbook.save(workbook_folder, include_rendered_content=include_rendered_content,
                          pretty_print_html=pretty_print_html, overwrite=overwrite)

        if zip_it:
            status.update('Zipping "%s"' % folder_or_zipfile, Status.RUNNING)
            util.safe_makedirs(os.path.dirname(folder_or_zipfile), exist_ok=True)
            with zipfile.ZipFile(util.handle_long_filenames(folder_or_zipfile),
                                 "w", zipfile.ZIP_DEFLATED) as z:
                for root, dirs, files in util.safe_walk(save_folder):
                    for file in files:
                        filename = os.path.join(root, file)
                        if util.safe_isfile(filename):  # regular files only
                            archive_name = os.path.join(util.safe_relpath(root, save_folder), file)
                            _common.print_output('Archiving %s' % archive_name)
                            # noinspection PyTypeChecker
                            z.write(filename, archive_name)

    finally:
        if save_folder and zip_it:
            util.safe_rmtree(save_folder)

    status.update('Success', Status.SUCCESS)
