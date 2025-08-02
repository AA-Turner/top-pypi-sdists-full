#!/usr/bin/env python3

__author__ = "Anarya Ray, Caitlin Rose, Vinaya Valsan"


import os

import numpy as np
import matplotlib.pyplot as plt


def compute_source_prob(rate_dict, evidence_dict):
    """
    Calculates multicomponent source probability

    Parameters
    ----------
    rate_dict : dict
        categorywise rate
    evidence_dict: dict
        categorywise evidence calculated from PE samples

    Returns
    -------
    dict
        a dictionary of probability for astrophysical categories
        such that the sum of probailities equal to 1.

    """
    rates_weighted_evidence_dict = {
        category: evidence_dict[category] * rate
        for category, rate in rate_dict.items()
    }
    rates_weighted_evidence_sum = sum(rates_weighted_evidence_dict.values())
    src_prob = {
        k: z / rates_weighted_evidence_sum
        for k, z in rates_weighted_evidence_dict.items()
    }

    return src_prob


class ZeroSrcProbError(ValueError):
    def __init__(
        self,
        message="Unable to reweight src_prob with p_terr as"
        " all component of src_prob are zero",
    ):
        self.message = message
        super().__init__(self.message)


def pastro(src_prob, p_terr):
    """
    Combines given p_terr with astrophysical source probabilities.

    Parameters
    ----------
    src_prob
        dictionary of astrophysical probabilities
    p_terr
        terrestrial probability

    Returns
    -------
    dict
        a dictionary of pastro normalized such that the sum of astrophysical
        probabilities and terrestrial probability equals to 1.

    """
    if sum(src_prob.values()) != 0.0:
        pastros = {k: (1 - p_terr) * src_p for k, src_p in src_prob.items()}
        pastros["Terrestrial"] = p_terr

        return pastros
    else:
        raise ZeroSrcProbError()


def renormalize_pastro_with_pipeline_pterr(rapidpe_pastro, pipeline_pastro):
    """
    Combines pipeline p_terr with astrophysical source probabilities.

    Parameters
    ----------
    rapidpe_pastro
        dictionary of pastros including pterr from rapidpe
    pipeline_pastro
        dictionary of pastros including pterr from pipeline

    Returns
    -------
    dict
        a dictionary of pastro normalized with pipeine pterr such that the
        sum of astrophysical probabilities and terrestrial probability
        equals to 1.
    """
    pipeline_p_terr = pipeline_pastro["Terrestrial"]
    rapidpe_pterr_complement = 1.0 - rapidpe_pastro["Terrestrial"]
    if rapidpe_pastro["Terrestrial"] != 1.0:
        src_prob = {
            category: rapidpe_pastro_value / rapidpe_pterr_complement
            for category, rapidpe_pastro_value in rapidpe_pastro.items()
            if category != "Terrestrial"
        }
    else:
        src_prob = {
            category: 0.0
            for category, rapidpe_pastro_value in rapidpe_pastro.items()
            if category != "Terrestrial"
        }

    pastros = pastro(src_prob, pipeline_p_terr)

    return pastros


def plot_pastro(pastro_dict, save_dir, filename="p_astro.png"):
    """
    adapted from gwcelery.tasks
    """

    def _format_prob(prob):
        if prob >= 1:
            return "100%"
        elif prob <= 0:
            return "0%"
        elif prob > 0.99:
            return ">99%"
        elif prob < 0.01:
            return "<1%"
        else:
            return "{}%".format(int(np.round(100 * prob)))

    fname = os.path.join(save_dir, filename)

    probs = list(pastro_dict.values())
    names = list(pastro_dict.keys())

    with plt.style.context("seaborn-white"):
        fig, ax = plt.subplots(figsize=(2.5, 2))
        ax.barh(names, probs)
        for i, prob in enumerate(probs):
            ax.annotate(
                _format_prob(prob),
                (0, i),
                (4, 0),
                textcoords="offset points",
                ha="left",
                va="center",
            )
        ax.set_xlim(0, 1)
        ax.set_xticks([])
        ax.tick_params(left=False)
        for side in ["top", "bottom", "right"]:
            ax.spines[side].set_visible(False)
        fig.tight_layout()
        fig.savefig(fname)
    return
