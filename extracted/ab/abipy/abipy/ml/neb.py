"""
"""
from __future__ import annotations

import sys
import os
import json
import numpy as np
import pandas as pd

from pathlib import Path
from monty.os.path import find_exts
from monty.string import marquee, list_strings
from abipy.tools.serialization import HasPickleIO
from abipy.tools.iotools import make_executable
from abipy.tools.plotting import get_axarray_fig_plt
from abipy.flowtk.qutils import SlurmJobArray


class AbiMlNeb(HasPickleIO):

    def __init__(self, nn_names, path_dirs: list, slurm_header: str, ext: str="vasp", verbose: int=0):
        self.nn_names = list_strings(nn_names)
        self.path_dirs = path_dirs
        self.slurm_header_nn_name = {nn: slurm_header for nn in self.nn_names}
        self.ext = ext
        self.verbose = verbose

    #def set_slurm_header_for_nn_name(self, nn_name: str, slurm_header: str) -> None:
    #    self.slurm_header_nn_name[nn_name] = slurm_header

    def sbatch_nn_name(self, nn_name) -> int:
        """
        Generate the shell script used to run NEB calculations for the different paths.
        """
        arr_options = []
        for i in range(len(self.path_dirs)):
            dirpath = Path(f"path{i+1}")
            workdir = dirpath / nn_name
            ini_file = str(dirpath / f"ini.{self.ext}")
            fin_file = str(dirpath / f"fin.{self.ext}")
            #log_file = str(workdir / "run.log")
            #err_file = str(workdir / "run.err")
            #opts = f"{ini_file} {fin_file} --nn-name {nn_name} -w {str(workdir)} > {log_file} 2> {err_file}"
            opts = f"{ini_file} {fin_file} --nn-name {nn_name} -w {str(workdir)}"
            arr_options.append(opts)

        header = self.slurm_header_nn_name[nn_name]
        command = "abiml.py neb"
        job_array = SlurmJobArray(header, command, arr_options)
        #print(job_array)
        queue_id = job_array.sbatch(f"job_array_{nn_name}.sh")
        return queue_id

    def process(self):
        """Post-process the results."""
        json_paths = find_exts(TOP, "neb_data.json")
        neb_data_list = []
        for path in json_paths:
            print("About to read json data from", path)
            parts = path.split(os.sep)
            path_index, nn_name = parts[-3], parts[-2]
            path_index = int(path_index.replace("path", ""))
            with open(path, "rt") as fh:
                d = json.load(fh)
                d["path"] = path_index
                d["nn_name"] = nn_name
                neb_data_list.append(d)

        # Sort dict by path.
        neb_data_list = sorted(neb_data_list, key=lambda d: d["path"])

        keys = [
            "nn_name",
            "path",
            "barrier_with_fit",
            "barrier_without_fit",
            "energy_change_with_fit",
            "energy_change_without_fit",
        ]

        d_list = []
        for d in neb_data_list:
            d_list.append({k: d[k] for k in keys})

        df = pd.DataFrame(d_list)
        df.to_csv("K3PS4_ML_barriers.csv")
        print(df)

        ax_list, fig, plt = get_axarray_fig_plt(
            None, nrows=1, ncols=3, sharex=True, sharey=True, squeeze=False)
        ax_list = ax_list.ravel()
        cmap = plt.get_cmap("jet")
        fontsize = 8

        for ix, (ax, nn_name) in enumerate(zip(ax_list, NN_NAMES)):
            my_data_list = [d for d in neb_data_list if d["nn_name"] == nn_name]
            my_data_list = sorted(my_data_list, key=lambda d: d["path"])
            for i, data in enumerate(my_data_list):
                enes = np.array(data["energies_images"])
                ax.plot(enes - enes[0], label=f"path{i+1}", color=cmap(i/len(my_data_list)))

            ax.set_title(nn_name)
            ax.set_xlabel('Image index', fontsize=fontsize)
            ax.set_ylabel(r'$\Delta$ energy [eV]', fontsize=fontsize)
            ax.legend(loc="best", shadow=True, fontsize=fontsize)

        fig.suptitle("K3PS4")
        #plt.show()
