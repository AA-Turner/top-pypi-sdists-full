
import os,subprocess
import inspect
from pathlib import Path
import requests
import json
import re

from .rank_zero import rank_zero_only as rank_zero_only_module

from typing import Optional


def rank0_print(*args, **kwargs):
    if int(os.environ.get("RANK", 0)) == 0:
        frame = inspect.currentframe().f_back
        filename = os.path.basename(frame.f_code.co_filename)
        lineno = frame.f_lineno
        print(f"[{filename}:{lineno}]", *args, **kwargs)


def get_eval_ckpt_list(dataset_folder_path, dataset_list):
    import os
    import sys

    final_dataset_paths = []

    if dataset_folder_path:
        if os.path.isdir(dataset_folder_path):
            rank0_print(f"Scanning eval dataset folder: {dataset_folder_path}")
            items = os.listdir(dataset_folder_path)
            for item in items:
                item_path = os.path.join(dataset_folder_path, item)
                if os.path.isdir(item_path):
                    final_dataset_paths.append(item_path)
                    rank0_print(f"Found eval dataset directory: {item_path}")

            if not final_dataset_paths:
                rank0_print(
                    f"Warning: No subdirectories found in {dataset_folder_path}")
        else:
            rank0_print(
                f"Error: dataset_folder_path '{dataset_folder_path}' is not a valid directory")
            sys.exit(1)

    elif dataset_list:
        final_dataset_paths = [path.strip()
                               for path in dataset_list.split(',') if path.strip()]
        rank0_print(f"Found {len(final_dataset_paths)} eval dataset paths from list")

    else:
        rank0_print("Error: Neither dataset_folder_path nor dataset_list provided")
        return []

    invalid_paths = []
    for path in final_dataset_paths:
        if not os.path.isdir(path):
            invalid_paths.append(path)
            rank0_print(f"Invalid eval dataset path: {path}")
        else:
            rank0_print(f"Valid eval dataset path: {path}")

    if invalid_paths:
        rank0_print(
            f"\nError: Found {len(invalid_paths)} invalid eval dataset paths:")
        for invalid_path in invalid_paths:
            rank0_print(f"  - {invalid_path}")
        rank0_print("Please check your eval dataset paths and try again.")
        sys.exit(1)

    if not final_dataset_paths:
        rank0_print("Error: No valid eval dataset paths found")
        sys.exit(1)

    rank0_print(
        f"Successfully validated {len(final_dataset_paths)} eval dataset paths")
    return final_dataset_paths


def invoke_evaluation_service(payload, endpoint):
     # Make the POST request
    try:
        url = f"http://model-management-service.infra.svc.cluster.local:5000/{endpoint}"
        headers = {"Content-Type": "application/json"}
        # get tflops and mfu from payload.
        rank0_print(
            f"Triggering evaluation with payload: {json.dumps(payload, indent=2)}")
        response = requests.post(
            url, headers=headers, data=json.dumps(payload))
        rank0_print(
            f"Evaluation successfully triggered. Response: {response.json()}")
        return response.json()
    except Exception as e:
        rank0_print(f"Error triggering evaluation: {str(e)}")
        return None


def uplaode_evaluation_loss_metrics(metrics, evaluation_id, dataset_name, eval_ckpt_path,
                    project_name, model_name, endpoint="evaluation-results"):
    try:
        payload = {}
        for key, value in metrics.items():
            if key == "val_loss":  # backward compatibility
                key = "eval_loss"
            payload[key] = value

        payload["evaluation_id"] = evaluation_id
        payload["eval_dataset_name"] = dataset_name
        payload["status"] = "succeeded"

        if "global_batch_size" in payload:
            payload["train_batch_size"] = payload.pop("global_batch_size")

        if eval_ckpt_path:
            payload["eval_ckpt_path"] = eval_ckpt_path
        if project_name:
            payload["project_name"] = project_name
        if model_name:
            payload["model_name"] = model_name

        payload["cluster"] = os.getenv("MLP_CLUSTER")

        resp = invoke_evaluation_service(payload, endpoint=endpoint)
        return resp

    except Exception as e:
        rank0_print(f"Error uploading evaluation loss metrics: {str(e)}")
        return None

def get_evaluation_loss_metrics(project_name='', evaluation_id='', dataset_name='', ckpt_path='', endpoint="evaluation-results", limit=5000):
    try:
        url = f"http://model-management-service.infra.svc.cluster.local:5000/{endpoint}?project_name={project_name}&evaluation_id={evaluation_id}&eval_dataset_name={dataset_name}&eval_ckpt_path={ckpt_path}&limit={limit}"
        print(url)
        response = requests.get(url)
        return response.json()
    except Exception as e:
        print(f"Error getting evaluation loss metrics: {str(e)}")
        return None

def get_step_from_model_path(model_path):
    tokens = model_path.split("/")
    model_ckpt_name = tokens[-1]
    match = re.search(r"step=(\d+)", model_ckpt_name)
    if match:
        return int(match.group(1))
    return 0


def _git_info_from_module(module_name: str):
    import importlib, subprocess, os
    from pathlib import Path

    def _run_git(args, root):
        try:
            out = subprocess.check_output(
                ["git", "-C", os.fspath(root), *args],
                stderr=subprocess.STDOUT,
            )
            return out.decode().strip(), None
        except subprocess.CalledProcessError as e:
            return None, e.output.decode(errors="ignore").strip()
        except Exception as e:
            return None, str(e)

    mod = importlib.import_module(module_name)
    p = None
    f = getattr(mod, "__file__", None)
    if f:
        p = Path(f).resolve()
    else:
        pth = getattr(mod, "__path__", None)
        if pth:
            p = Path(next(iter(pth))).resolve()

    if p is None:
        return {"module": module_name, "path": None, "git_root": None,
                "branch": None, "commit": None, "describe": None,
                "note": "no __file__/__path__"}

    git_root = None
    for parent in [p] + list(p.parents):
        if (parent / ".git").exists():
            git_root = parent
            break

    info = {
        "module": module_name,
        "path": p.as_posix(),
        "git_root": git_root.as_posix() if git_root else None,
        "branch": None, "commit": None, "describe": None,
        "note": None,
    }
    if not git_root:
        info["note"] = "no .git upward"
        return info

    errs = []
    info["branch"], e1   = _run_git(["rev-parse", "--abbrev-ref", "HEAD"], git_root)
    if e1: errs.append(f"branch: {e1}")
    info["commit"], e2   = _run_git(["rev-parse", "HEAD"], git_root)
    if e2: errs.append(f"commit: {e2}")
    info["describe"], e3 = _run_git(["describe", "--tags", "--dirty", "--always"], git_root)
    if e3: errs.append(f"describe: {e3}")
    if errs:
        info["note"] = " | ".join(errs)[:500]
    return info


def collect_specific_repos(root_name, sub_module_names=[]):

    def _git_root_from(p: Path):
        for parent in [p] + list(p.parents):
            if (parent / ".git").exists():
                return parent
        return None

    def _git_info_from_root(label, root):
        info = {"module": label, "git_root": root.as_posix() if root else None,
                "branch": None, "commit": None, "describe": None, "note": None}
        if not root:
            info["note"] = "no .git upward"
            return info
        def _run(args):
            return subprocess.check_output(["git", "-C", os.fspath(root), *args],
                                        stderr=subprocess.STDOUT).decode().strip()
        try: info["branch"]   = _run(["rev-parse", "--abbrev-ref", "HEAD"])
        except Exception as e: info["note"] = f"{info.get('note','') or ''} branch:{e}"
        try: info["commit"]   = _run(["rev-parse", "HEAD"])
        except Exception as e: info["note"] = f"{info.get('note','') or ''} commit:{e}"
        try: info["describe"] = _run(["describe", "--tags", "--dirty", "--always"])
        except Exception as e: info["note"] = f"{info.get('note','') or ''} describe:{e}"
        return info

    results = {}
    root_info = _git_root_from(Path(__file__).resolve())
    results[root_name] = _git_info_from_root(root_name, root_info)
    for name, module in sub_module_names:
    #for name, module in [("MEGATRON", "megatron"), ("ANC", "anc")]:
        try:
            results[name] = _git_info_from_module(module)
        except ModuleNotFoundError:
            results[name] = {"error": f"module {module} not found"}

    print(f"results: {results}", flush=True)
    return results

def _get_rank() -> Optional[int]:
    # SLURM_PROCID can be set even if SLURM is not managing the multiprocessing,
    # therefore LOCAL_RANK needs to be checked first
    rank_keys = ("RANK", "LOCAL_RANK", "SLURM_PROCID", "JSM_NAMESPACE_RANK")
    for key in rank_keys:
        rank = os.environ.get(key)
        if rank is not None:
            return int(rank)
    # None to differentiate whether an environment variable was set at all
    return None

rank_zero_only = rank_zero_only_module

# add the attribute to the function but don't overwrite in case Trainer has already set it
rank_zero_only.rank = getattr(rank_zero_only, "rank", _get_rank() or 0)



if __name__ == "__main__":
    evaluation_id = "123"
    ckpt_path = "123"
    project_name = "pretrain_m3_stage2_main_fix_step125k_wd02"
    rep = get_evaluation_loss_metrics(project_name=project_name, evaluation_id='bb7d6597-f4e0-48c0-bd55-c8136480694e')
    print(rep['count'], rep['total_count'])
    print(len(rep['results']))
    step = None
    domain_names = "web_zh_mix_skywork_fineweb2_zh_deduped,public_chat_cn_cross_deduped_0825,podcast_cn_cross_deduped_0825,duanju_douyin_cn_gemini_res_cross_deduped_0825,zhihu_qa_free_D_ALL,zhihu_qa_free_L_ALL_prechunk_v0.2,zhihu_qa_free_D_HVHQ,zhihu_qa_free_L_HVHQ_prechunk_v0.2,xhs_D_ALL,xhs_B_ALL,xhs_L_ALL,xhs_D_HVHQ,xhs_B_HVHQ,xhs_L_HVHQ,script_zh,web-novel-zh_fix_rowgroup,web_novel_zh_HQ,lofter,sq-novel-zh,lyrics_zh,annas_archive_zh_Fiction_Fiction_General-Public_fix_rowgroup,annas_archive_zh_Non-fiction_Humanities_General-Public,annas_archive_zh_Non-fiction_Humanities_Professional,annas_archive_zh_Non-fiction_Natural-Sciences_or_Technology_General-Public,annas_archive_zh_Non-fiction_Natural-Sciences_or_Technology_Professional,annas_archive_zh_unknown_unknown_unknown,mafengwo,wiki-zh,baidu_baike_cross_baike_deduped,mengniang_baike_cross_baike_deduped,baidu_jingyan,toutiao_news,toutiao_news_HQ,exams_zh,web_en_fineweb_deduped_old,web_en_dclm_old,web_en_dclm_hq,public_chat_en_cross_deduped_0825,podcast_en_cross_deduped_0825,reddit_D_ALL,reddit_B_ALL_fix_mask,reddit_L_ALL_prechunk_v0.2,reddit_D_HVHQ,reddit_B_HVHQ,reddit_L_HVHQ_prechunk_v0.2,genshin-en,script_en,web-novel-en,sq-novel-aggr-en,lyrics_en,annas_archive_en_Fiction_Fiction_General-Public_fix_rowgroup,annas_archive_en_Non-fiction_Humanities_General-Public,annas_archive_en_Non-fiction_Humanities_Professional,annas_archive_en_Non-fiction_Natural-Sciences_or_Technology_General-Public,annas_archive_en_Non-fiction_Natural-Sciences_or_Technology_Professional,annas_archive_en_unknown_unknown_unknown,wiki-en,fandom_cross_baike_deduped,bbc,exams_en,megamath_web_pro_0822_fix_rowgroup,the-stack-v2_inhouse_fix_rowgroup,the-stack-v2_inhouse_part2"
    ratio = "0.0982297854606499000,0.0012300276622894600,0.0001569205117515260,0.0008457954528846970,0.0093977502729165600,0.0006235404168111840,0.0045078473739413700,0.0003657010757709410,0.0000412772719068594,0.0000219946858886540,0.0000519133274419680,0.0000465591724469911,0.0000239320557560415,0.0001745222054875570,0.0000037858670580154,0.0000132674858948063,0.0000071440192241321,0.0000268119421548548,0.0000169654186456054,0.0000990096407776172,0.0001273645954317310,0.0001423618596349270,0.0000933567210280021,0.0000268552282337943,0.0000426661496411115,0.0000069590696141180,0.0008719160285759310,0.0004731144212098000,0.0120752095959992000,0.0000492117312564089,0.0030390983484499600,0.0006992190123903430,0.0009659672944160080,0.0004742313836663510,0.2399337567362120000,0.2677948637394590000,0.0917569807601435000,0.0007901973601355240,0.0002221311410237940,0.0379111323089188000,0.0030091801306764400,0.0005850058477298830,0.0659656542716659000,0.0066795941048946200,0.0020202244170252800,0.0000011771997272425,0.0000056524656998361,0.0000024754793955745,0.0002730404130542770,0.0002192288548358790,0.0003838285591511530,0.0001706546094693060,0.0000896534910297803,0.0000149588213219000,0.0000347635645860538,0.0000069813180532932,0.0031834987402430600,0.0008495979684346130,0.0000596939244563780,0.0002364685195480520,0.0068007439696500800,0.0337418487570618000,0.1022849297671506000"
    domain_names = domain_names.split(",")
    ratio = ratio.split(",")
    assert len(domain_names) == len(ratio)
    domain_ratio = {key:float(val) for key, val in zip(domain_names, ratio)}
    results = rep['results']
    step = get_step_from_model_path(results[0]['eval_ckpt_path'])
    overall_loss = 0
    not_in_domain_ratio = []
    # for metric in rep['results']:
    #     if 'eval_loss' in metric:
    #         domain_name = metric['eval_dataset_name']
    #         eval_loss = float(metric['eval_loss'])
    #         if domain_name not in domain_ratio:
    #             not_in_domain_ratio.append(domain_name)
    #             continue
    #         overall_loss += domain_ratio[domain_name] * metric['eval_loss']
    evaluated = {}
    for metric in rep['results']:
        if 'eval_loss' in metric and 'eval_dataset_name' in metric:
            evaluated[metric['eval_dataset_name']] = float(metric['eval_loss'])
            
    for k, v in domain_ratio.items():
        truncated_key = k[:64]
        if truncated_key in evaluated:
            overall_loss += evaluated[truncated_key] * v
        else:
            not_in_domain_ratio.append(truncated_key)
    
    if len(not_in_domain_ratio) > 0:
        print(f"domain_name {not_in_domain_ratio} not found in evaluated")
    
    print(overall_loss)
    