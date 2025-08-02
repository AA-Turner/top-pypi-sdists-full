#!/usr/bin/env python3
import textwrap
import json
import h5py


def print_output(fileobj, *args, **kwargs):
    """
    saving print statemets to html_file
    """
    print(textwrap.dedent(*args), file=fileobj, **kwargs)


def save_as_json(data_dict, filename, *args, **kwargs):
    """
    saving dict as json file
    """
    with open(filename, "w") as f:
        json.dump(obj=data_dict, fp=f, *args, **kwargs)


def save_dict_in_hdf(data_dict, filename, keys_to_save=None, group_name=None):
    """
    saving dict as hdf file
    """
    if keys_to_save is None:
        keys_to_save = data_dict.keys()
    if "filename" in keys_to_save and "filename" in data_dict:
        data_dict["filename"] = data_dict["filename"].astype("S")

    with h5py.File(filename, "a") as f:
        if group_name is not None:
            if group_name in f:
                del f[group_name]
            g = f.create_group(group_name)
        else:
            g = f
        for k in keys_to_save:
            if k in g:
                del g[k]
            g.create_dataset(k, data=data_dict[k])
