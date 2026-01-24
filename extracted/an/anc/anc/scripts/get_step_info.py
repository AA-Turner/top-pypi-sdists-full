import torch
import multiprocessing as mp
import os
import glob
import argparse
import json

def get_step_info_from_ckpt(item):
    ckpt_path, target_paths = item
    ckpt = torch.load(ckpt_path, weights_only=False)
    ds_states = ckpt['ds_states']
    paths = ckpt['paths']
    res = {}
    seed_info = set()
    for i, path in enumerate(paths):
        ds_name = path[0].rsplit("/", 2)[0]
        if ds_name in target_paths:
            res[ds_name] = [ds_state['sampler']['samplers'][i]['step'] for ds_state in ds_states]
            for ds_state in ds_states:
                seed_info.add(ds_state['sampler']['samplers'][i]['seed'])
    assert len(seed_info) == 1, "all seeds must be the same"
    res['seed'] = list(seed_info)[0]
    return ckpt_path, res


def get_all_step_info(ckpt_dir, target_paths):
    ckpt_paths = glob.glob(os.path.join(ckpt_dir, '*.pt'))
    inputs = [(ckpt_path, target_paths) for ckpt_path in ckpt_paths]
    with mp.Pool(16) as pool:
        res = pool.map(get_step_info_from_ckpt, inputs)
    res_dict = {}
    for ckpt_path, step_info in res:
        rank_id = int(os.path.basename(ckpt_path).split('.')[0][2:])
        res_dict[rank_id] = step_info
    return res_dict


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--ckpt_dir', type=str, required=True)
    parser.add_argument('--target_names', type=str, required=True)
    parser.add_argument('--output_path', type=str, required=True)
    parser.add_argument('--target_folder', type=str, required=True)
    args = parser.parse_args()
    target_paths = [os.path.join(args.target_folder, name) for name in args.target_names.split(',')]
    res = get_all_step_info(args.ckpt_dir, target_paths)
    with open(args.output_path, 'w') as f:
        json.dump(res, f)
