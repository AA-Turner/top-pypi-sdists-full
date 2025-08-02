import argparse
import json


def in_range(value, bounds):
    lower, upper = bounds

    if lower is not None and value < lower:
        return False

    if upper is not None and value > upper:
        return False

    return True


def compute_limits(recovered, spec):
    param_name = spec["param"]

    lower = compute_limit(recovered, param_name, spec["lower"])
    upper = compute_limit(recovered, param_name, spec["upper"])

    return lower, upper


def compute_limit(recovered, param_name, spec):
    formula = limit_formulae[spec["formula"]]

    return formula(recovered, param_name, **spec["settings"])


def formula_const(recovered, param_name, *, const):
    return const


def formula_v1(recovered, param_name, *,
               const, param_power=0.0, snr_power=0.0, reciprocal=False):
    param_value = recovered[param_name]
    snr_value = recovered["snr"]

    quantity = 1 + const * param_value**param_power * snr_value**snr_power

    if reciprocal:
        quantity = 1.0 / quantity

    return param_value * quantity



limit_formulae = {
    "const": formula_const,
    "v1": formula_v1,
}


def parse_search_bias_bounds(recovered, init_region_spec):
    for range_spec in init_region_spec:
        if not in_range(recovered["snr"], range_spec["snr_range"]):
            continue
        if not in_range(recovered["mchirp"], range_spec["mchirp_range"]):
            continue

        limits = {}
        for limit_spec in range_spec["limits"]:
            limits[limit_spec["param"]] = compute_limits(recovered, limit_spec)
        break

    else:
        raise ValueError("Recovered value outside range")

    return limits


# def main():
#     cli_parser = argparse.ArgumentParser()
#     cli_parser.add_argument("--snr-rec", type=float)
#     cli_parser.add_argument("--mchirp-rec", type=float)
#     cli_parser.add_argument("--mtot-rec", type=float)
#     cli_parser.add_argument("--q-rec", type=float)
#     cli_args = cli_parser.parse_args()

#     recovered = {
#         "snr": cli_args.snr_rec,
#         "mchirp": cli_args.mchirp_rec,
#         "mtot": cli_args.mtot_rec,
#         "q": cli_args.q_rec,
#     }


#     with open("init_region_spec.json", "r") as init_region_spec_file:
#         init_region_spec = json.load(init_region_spec_file)

#     limits = parse_range_spec(recovered, init_region_spec)

#     print(limits)


# if __name__ == "__main__":
#     main()
