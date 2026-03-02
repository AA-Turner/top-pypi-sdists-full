import json
import logging
import pickle
import numpy as np
from .tools import ScatterData


logger = logging.getLogger()


def read_summary(fname: str) -> dict:
    """ Reads an Optimizer summary file and returns dict with the summary """
    try:
        data = _read_summary_pickle(fname)
        logger.warning('Deprecated file format (pickle). Consider rewriting in new format (json).')
    except pickle.UnpicklingError:
        data = _read_summary_json(fname)
    return data


class OptimizerSummaryEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (np.integer)):
            return int(obj)
        if isinstance(obj, (np.floating)):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, ScatterData):
            return obj.to_dict()
        else:
            return json.JSONEncoder.default(self, obj)


def object_hook(dct: dict) -> dict:

    ndarray_keys = ['parameters', 'train_set', 'test_set', 'rmse_train_splits',
                    'rmse_validation_splits', 'rmse_test_splits', 'parameters_std']
    for key in ndarray_keys:
        if key in dct:
            dct[key] = np.array(dct[key])

    sd_keys = ['scatter_data_train', 'scatter_data_test', 'scatter_data_validation']
    for key in sd_keys:
        if key in dct:
            dct[key] = ScatterData.from_dict(dct[key])
    return dct


def _write_summary_json(fname: str, summary: dict) -> None:
    with open(fname, 'w') as f:
        json.dump(summary, f, cls=OptimizerSummaryEncoder)


def _read_summary_json(fname: str) -> dict:
    with open(fname, 'r') as f:
        return json.load(f, object_hook=object_hook)


def _write_summary_pickle(fname: str, data: dict) -> None:
    """ Write data to pickle file with filename fname """
    with open(fname, 'wb') as handle:
        pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)


def _read_summary_pickle(fname: str) -> dict:
    """ Read pickle file and return content """
    with open(fname, 'rb') as handle:
        return pickle.load(handle)
