#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import json
import os
from typing import Sequence
from urllib import parse

import pytest

from .client import HttpClient, Response


def resp_diff(src_resp: Response, dst_resp: Response = None, key_whitelist: Sequence[str] = None, **kwargs):
    """Compare two `<class> requests.Response` , and return return detailed results.

    Args:
        src_resp (Response): source response.
        dst_resp (Response, optional): dest response. Defaults to None.
        key_whitelist (Sequence[str], optional): Whitelist keys, will skip comparison. #TODO: .flat dict

    Raises:
        RuntimeError: when env variable missing api key & secret.

    Returns:
        dict: The comparison result, including the meta information of the two requests (method/url/traceid/payload).
    """
    src_resp.encoding = "utf-8"
    url: str = src_resp.url  # contains query params
    parse_res = parse.urlparse(url)
    method = src_resp.request.method
    body = src_resp.request.body
    payload = json.loads(str(body)) if body else None

    if dst_resp is None:
        if "_PYTEST_DIFF_ACCOUNT" not in os.environ:
            raise RuntimeError("env variable missing api key & secret")

        account = json.loads(os.environ["_PYTEST_DIFF_ACCOUNT"])
        if "testnet" in url:
            cli = HttpClient(account["mainnet"]["api_key"], account["mainnet"]["api_secret"])
            dst_url = parse_res._replace(netloc="api.bybit.com").geturl()  # contains query params
        else:
            cli = HttpClient(account["testnet"]["api_key"], account["testnet"]["api_secret"])
            dst_url = parse_res._replace(netloc="api-testnet.bybit.com").geturl()  # contains query params

        if method == "GET":
            dst_resp = cli.request(method, dst_url, **kwargs)
        else:
            dst_resp = cli.request(method, dst_url, payload, **kwargs)
    else:
        dst_url = dst_resp.url

    res = {}
    res["meta"] = {
        "src": {"method": method, "url": url, "payload": payload, "traceid": _get_traceid(src_resp), "content": src_resp.text},
        "dst": {"method": method, "url": dst_url, "payload": payload, "traceid": _get_traceid(dst_resp), "content": dst_resp.text},
    }
    if src_resp.status_code != 200 or dst_resp.status_code != 200:
        res["details"] = f"error status_code, src: {src_resp.status_code}, dst: {dst_resp.status_code}"
    else:
        src = src_resp.json()
        dst = dst_resp.json()
        src_retcode = src.get("retCode") or src.get("ret_code")
        dst_retcode = dst.get("retCode") or dst.get("ret_code")

        if src_retcode != dst_retcode:
            res["result"] = False
            res["details"] = f"different ret code. src: {src_retcode}, dst: {dst_retcode}"
        else:
            res.update(json_schema_diff(src, dst, key_whitelist=key_whitelist))

    return res


def json_schema_diff(src: dict, dst: dict, key_whitelist: Sequence[str] = None) -> dict:
    assert all([type(src) == dict, type(dst) == dict]), "Unsupported parameter type."

    def _recursive_diff(l, r, details, path="/"):
        if type(l) != type(r):
            details.append({"replace": path, "value": r, "details": "type", "src": l})
            return

        delim = "/" if path != "/" else ""

        if key_whitelist and isinstance(l, dict) and isinstance(r, dict):
            for k in key_whitelist:
                if k in l:
                    l.pop(k)
                if k in r:
                    r.pop(k)

        if isinstance(l, dict):
            for k, v in l.items():
                new_path = delim.join([path, k])
                if k not in r:
                    details.append({"remove": new_path, "src": v})
                else:
                    _recursive_diff(v, r[k], details, new_path)
            for k, v in r.items():
                if k in l:
                    continue
                details.append({"add": delim.join([path, k]), "dst": v})
        elif isinstance(l, list):
            ll = len(l)
            lr = len(r)
            if ll > lr:
                for i, item in enumerate(l[lr:], start=lr):
                    details.append({"remove": delim.join([path, str(i)]), "src": item, "details": "array-item"})
            elif lr > ll:
                for i, item in enumerate(r[ll:], start=ll):
                    details.append({"add": delim.join([path, str(i)]), "dst": item, "details": "array-item"})
            minl = min(ll, lr)
            if minl > 0:
                for i, item in enumerate(l[:minl]):
                    _recursive_diff(item, r[i], details, delim.join([path, str(i)]))
        else:
            if type(l) != type(r):
                details.append({"replace": path, "dst": r, "src": l})

    details = []
    _recursive_diff(src, dst, details)

    res = {}
    res["result"] = True if len(details) == 0 else False
    res["details"] = details
    return res


def _get_traceid(resp: Response) -> str:
    return resp.headers.get("traceid", "")


COIN_SYMBOL = {
    "BTC": "BTCUSD",
    "ETH": "ETHUSD",
    "BIT": "BITUSD",
    "SOL": "SOLUSD",
    "DOT": "DOTUSD",
    "ADA": "ADAUSD",
    "LTC": "LTCUSD",
    "XRP": "XRPUSD",
    "EOS": "EOSUSD",
    "MANA": "MANAUSD",
    "USDT": "BITUSDT",
    "USDC": "ETHPERP",
}


def pytest_load_initial_conftests(early_config, args, parser):
    instance_params = None
    symbol_params = None
    tail_num_params = None

    for index, value in enumerate(args):  # --store
        if value.find("--instance") != -1:
            instance_params = (index, value)
        if value.find("--symbol") != -1:
            symbol_params = (index, value)
            symbol = value.strip().split("=")[-1]
            os.environ["_PYTEST_SYMBOL"] = symbol
        if value.find("--tailnum") != -1:
            tail_num_params = (index, value)
            tail_num = value.strip().split("=")[-1]
            os.environ["_PYTEST_TAILNUM"] = tail_num
        if value.find("--env") != -1:
            env = value.strip().split("=")[-1]
            os.environ["_PYTEST_ENV"] = env
        if value.find("--siteid") != -1:
            site_id = value.strip().split("=")[-1]
            os.environ["_PYTEST_SITE_ID"] = site_id

    # overwrite
    if instance_params:
        _, value = instance_params
        if "trading" in value:
            *_, ins = value.split(".")
            coin, tail_num, *_ = ins.split("_")

            if len(tail_num) < 2 or "inter" in tail_num:
                if symbol_params:
                    args[symbol_params[0]] = f"--symbol={COIN_SYMBOL[coin]}"
                else:
                    args.append(f"--symbol={COIN_SYMBOL[coin]}")

                if tail_num_params:
                    args[tail_num_params[0]] = f"--tailnum={tail_num}"
                else:
                    args.append(f"--tailnum={tail_num}")

                os.environ["_PYTEST_TAILNUM"] = tail_num
            elif "qian" in tail_num:
                pytest.exit(reason="skip", returncode=0)


@pytest.fixture(scope="session", autouse=True)
def clear_env():
    yield
    if "_PYTEST_TAILNUM" in os.environ:
        del os.environ["_PYTEST_TAILNUM"]
    if "_PYTEST_DIFF_ACCOUNT" in os.environ:
        del os.environ["_PYTEST_DIFF_ACCOUNT"]
    if "_PYTEST_DIFF_ACCOUNT" in os.environ:
        del os.environ["_PYTEST_SITE_ID"]
