import argparse
import os
from collections import defaultdict
from pathlib import Path

from ipfabric import IPFClient
from ipfabric.models import Devices
from ipfabric.scripts.shared import load_env, base_args, parse_base_args
from ipfabric.tools.vulnerabilities import Vulnerabilities

try:
    import pandas as pd
    import openpyxl  # noqa: F401
except ImportError:
    raise ImportError("pandas and openpyxl are required, please install by using `pip3 install pandas openpyxl`.")


def load_cve(ipf: IPFClient, nvd_api_key: str, timeout=60, retries: int = 2):
    vuln = Vulnerabilities(ipf=ipf, nvd_api_key=nvd_api_key, timeout=timeout, retries=retries)
    versions = vuln.check_versions()
    cves = defaultdict(dict)
    for v in versions:
        if v.family not in cves[v.vendor]:
            cves[v.vendor][v.family] = defaultdict(dict)
        cves[v.vendor][v.family][v.version] = v.cves
    return cves


def load_eol(ipf: IPFClient) -> pd.DataFrame:
    eol = ipf.fetch_all(
        "tables/reports/eof/detail",
        columns=[
            "hostname",
            "siteName",
            "deviceSn",
            "vendor",
            "pid",
            "replacement",
            "sn",
            "endSale",
            "endMaintenance",
            "endSupport",
            "url",
            "dscr",
        ],
        filters={
            "or": [
                {"endSale": ["empty", False]},
                {"endMaintenance": ["empty", False]},
                {"endSupport": ["empty", False]},
            ]
        },
    )
    if eol:
        df_eol = pd.DataFrame(eol)
        for eolt in ["endSale", "endMaintenance", "endSupport"]:
            df_eol[eolt] = df_eol[eolt].values.astype(dtype="datetime64[ms]")
    else:
        df_eol = pd.DataFrame()
    return df_eol


def _check_cves(dev, cves, data, clean, error):
    for cve in cves:
        if cve.error:
            error.append(
                [
                    dev.hostname,
                    dev.site_name,
                    dev.sn_hw,
                    str(dev.login_ip.ip),
                    str(dev.login_ipv6),
                    dev.vendor,
                    dev.family,
                    dev.version,
                    None,
                    cve.error,
                ]
            )
            continue
        elif cve.total_results == 0:
            clean.append(
                [
                    dev.hostname,
                    dev.site_name,
                    dev.sn_hw,
                    str(dev.login_ip),
                    str(dev.login_ipv6),
                    dev.vendor,
                    dev.family,
                    dev.version,
                    cve.cpe.cpeName,
                ]
            )
            continue
        for c in cve.cves:
            data.append(
                [
                    dev.hostname,
                    dev.site_name,
                    dev.sn_hw,
                    str(dev.login_ip),
                    str(dev.login_ipv6),
                    dev.vendor,
                    dev.family,
                    dev.version,
                    cve.cpe.cpeName,
                    c.cve_id,
                    c.base_score,
                    c.description,
                    c.url,
                ]
            )
    return data, clean, error


def parse_cve(devices: Devices, cves):
    data, clean, error = list(), list(), list()
    for dev in devices.all:
        if (
            dev.vendor
            and dev.version
            and dev.vendor in cves
            and dev.family in cves[dev.vendor]
            and dev.version in cves[dev.vendor][dev.family]
        ):
            data, clean, error = _check_cves(dev, cves[dev.vendor][dev.family][dev.version], data, clean, error)
        else:
            error.append(
                [
                    dev.hostname,
                    dev.site_name,
                    dev.sn_hw,
                    str(dev.login_ip),
                    dev.vendor,
                    dev.family,
                    dev.version,
                    None,
                    "Unknown Error",
                ]
            )
    return (
        pd.DataFrame(
            data,
            columns=[
                "device",
                "site",
                "serial",
                "ip",
                "ipv6",
                "vendor",
                "family",
                "version",
                "cpe_name",
                "cve_id",
                "cve_base_score",
                "cve_description",
                "cve_url",
            ],
        ),
        pd.DataFrame(
            clean,
            columns=[
                "device",
                "site",
                "serial",
                "ip",
                "ipv6",
                "vendor",
                "family",
                "version",
                "cpe_name",
            ],
        ),
        pd.DataFrame(
            error,
            columns=["device", "site", "serial", "ip", "ipv6", "vendor", "family", "version", "cpe_name", "error"],
        ),
    )


def write_json(df_eol: pd.DataFrame, df_cve: pd.DataFrame, df_clean: pd.DataFrame, df_error: pd.DataFrame, filename):
    json_data = (
        f"{{"
        f'"CVE": {df_cve.to_json(orient="records", date_format="iso")}, '
        f'"No CVE": {df_clean.to_json(orient="records", date_format="iso")}, '
        f'"CVE Error": {df_error.to_json(orient="records", date_format="iso")}, '
        f'"EoL": {df_eol.to_json(orient="records", date_format="iso")}'
        f"}}"
    )
    with open(filename, "w") as f:
        f.write(json_data)


def write_excel(df_eol: pd.DataFrame, df_cve: pd.DataFrame, df_clean: pd.DataFrame, df_error: pd.DataFrame, filename):
    writer = pd.ExcelWriter(filename, engine="openpyxl")
    df_eol.to_excel(writer, sheet_name="End of Life", index=False)
    df_cve.to_excel(writer, sheet_name="CVE DATA", index=False)
    df_clean.to_excel(writer, sheet_name="Clean Devices", index=False)
    df_error.to_excel(writer, sheet_name="CVE ERROR", index=False)
    writer.close()


def main():  # NOSONAR
    load_env()
    arg_parser = argparse.ArgumentParser(
        description="Creates an Excel report of CVEs and EoL for devices in IP Fabric; requires:\n"
        "Python Packages: 'pandas' and 'openpyxl' "
        "(`pip install ipfabric[cve]` or `pip install pandas openpyxl`)\n"
        "NVD_API_KEY: See https://nvd.nist.gov/developers/request-an-api-key",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    arg_parser = base_args(arg_parser)
    arg_parser.add_argument(
        "-n",
        "--nvd-api-key",
        help="NVD_API_KEY from https://nvd.nist.gov/developers/request-an-api-key",
    )
    arg_parser.add_argument(
        "-f",
        "--filename",
        help="Filename to save, defaults to CVE_report.(xlsx|json). "
        "Extension will always be corrected to either '.xlsx' or '.json'.",
    )
    arg_parser.add_argument(
        "-to", "--timeout", help="Timeout for NIST API (Int, Float, or None); default 60 seconds.", default=60
    )
    arg_parser.add_argument("-r", "--retries", help="Number of retries for NIST API errors; default 2.", default=2)
    arg_parser.add_argument(
        "-l", "--site-name", help="Filter on a specific site name (location); case-insensitive equals search."
    )
    arg_parser.add_argument(
        "-j",
        "--json",
        help="Save as JSON output instead of Excel; default is Excel output.",
        action="store_true",
        default=False,
    )
    args = arg_parser.parse_args()
    args = parse_base_args(args)
    if isinstance(args.timeout, str) and args.timeout.lower() == "none":
        args.timeout = None
    else:
        args.timeout = float(args.timeout)
    if args.filename:
        args.filename = Path(args.filename).resolve().with_suffix(".json" if args.json else ".xlsx").absolute()

    ipf = IPFClient(snapshot_id=args.snapshot, base_url=args.base_url, auth=args.auth)

    if args.site_name:
        site = ipf.inventory.sites.all(filters={"siteName": ["ieq", args.site_name]})
        if not site:
            raise ValueError(f"Site Name {args.site_name} not found.")
        elif len(site) > 1:
            raise ValueError(f"Multiple Site Names found for {args.site_name}.")
        ipf.attribute_filters = {"siteName": [site[0]["siteName"]]}

    nvd_api_key = args.nvd_api_key or getattr(ipf, "nvd_api_key", None) or os.environ.get("NVD_API_KEY", None)
    if not nvd_api_key:
        raise ValueError("NIST NVD_API_KEY parsed nor defined in environment variables.")

    df_cve, df_clean, df_error = parse_cve(ipf.devices, load_cve(ipf, nvd_api_key, args.timeout, int(args.retries)))
    df_eol = load_eol(ipf)

    if args.json:
        write_json(df_eol, df_cve, df_clean, df_error, args.filename or "CVE_report.json")
    else:
        write_excel(df_eol, df_cve, df_clean, df_error, args.filename or "CVE_report.xlsx")


if __name__ == "__main__":
    main()
