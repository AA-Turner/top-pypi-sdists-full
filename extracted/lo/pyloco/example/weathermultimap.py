# -*- coding: utf-8 -*-

from netCDF4 import Dataset
from pyloco import GroupTask, TaskPath


class WeatherMultimap(GroupTask):
    """read multiple netcdf data files and generate weather map images in parallel

'weathermultimap' task reads multiple netcdf data files and generates weather map
images in parallel

Example(s)
----------

>>> pyloco weathermultimap -o oecd.json
"""

    _name_ = "weathermultimap"
    _version_ = "0.1.0"

    def __init__(self, parent):

        self.add_data_argument("data", nargs="+", required=True,
                help="netcdf data file")
#
#        self.add_option_argument("-d", "--dataset", metavar="dataset",
#                default=default_dataset, help="Dataset code (default='%s')"
#                % default_dataset) 
#
#        self.add_option_argument("-f", "--filter", metavar="filter",
#                default=default_filter, help="Query filter(default='%s')"
#                % default_filter)
#
#        self.add_option_argument("-a", "--agency", metavar="agency",
#                default=default_agency, help="Agency code. (default='%s')"
#                % default_agency) 
#
#        self.add_option_argument("-p", "--params", metavar="params",
#                help="Additional parameters") 
#
#        self.add_option_argument("-o", "--outfile", metavar="outfile",
#                help="Save OECD data in a file") 
#
#        self.register_forward("data", help="OECD stats in JSON format ")

    def perform(self, targs):

        path = TaskPath()

        # append tasks in the created taskblock
        #blk.append_task("netcdfreader")
        #blk.append_task("netcdfreader")
        path.append_task("input")
        path.append_task("print")

        # get the number of data
        ndata = len(targs.data)

        # dupulicate previously created taskblock as many as ndata
        clones = self.copy_taskpath(path, ndata) # share entry and exit

        # assign data to each of taskblocks
        for i, path in enumerate(clones):
            self.connect_taskpath(self, path, self)
            path.load_data(data=targs.data[i])


#    def perform(self, targs):
#
#        # add overwrite=True to overwrite multiprocessing configurations)
#        # self.enable_multiprocessing(targs.multiproc.vargs[0], **targs.multiproc.kwargs)
#
#        # build task graph and assign procs to this initial task graph
#        # repeat
##        ncr = self.insert_task("netcdfreader", after=self, args=nr_args, subargs=nr_subargs, send=...,receive=...)
##        self.insert_task("matplot", after=ncr, args=mp_args, subargsmp_subargs)
#
#        # create a task block with default departure hub and arrival hub,which is self
#        blk = self.taskblock() # add forward kwargs if any
#
#        # append tasks in the created taskblock
#        #blk.append_task("netcdfreader")
#        #blk.append_task("netcdfreader")
#        blk.append_task("input")
#        blk.append_task("print")
#
#        # get the number of data
#        ndata = len(targs.data)
#
#        # dupulicate previously created taskblock as many as ndata
#        self.clone_block(blk, ndata-1) # share entry and exit
#
#        # assign data to each of taskblocks
#        for i, blk in enumerate(self.taskblocks):
#            blk.load_data(data=targs.data[i])
#
#        # Generally, we need to add reduce schedule here
#        # to create data from outputs of each taskblocks
#        # however, we do not need here for this particular task
#
#        for path in targs.data:
#            #rootgrp = Dataset(path, "r", format="NETCDF4")
#            rootgrp = Dataset(path, "r")
#            print (rootgrp.data_model)
#            import pdb; pdb.set_trace()
#            print (rootgrp.data_model)
#            rootgrp.close()

        # Generally, we may need to add forward as usualreduce schedule here
        # however, we do not need here for this particular task
