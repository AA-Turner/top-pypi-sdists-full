#!/usr/bin/python3

#
# A module to access data from the DFG-funded SPP Computational Literary Studies
#
# Usage:
# from sppcls import sppcls
# df = sppcls.load_df("judenbuche", ["events", "keypassages"])
#
# Author: rja
#
# Changes:
# 2022-09-02 (rja)
# - disabled parsing of comments
# 2022-08-26 (rja)
# - fixed usage example
# - fixed column name (s/word/token/)
# 2022-08-25 (rja)
# - initial version

import pandas as pd
import asyncio

# default repository URL
DEFAULT_REPO = "https://scm.cms.hu-berlin.de/schluesselstellen/spp-cls-dataexchange/data/-/raw/main/"


# FIXME: do we want to support more/all pandas.DataFrame kwargs?
def load_df(work, projects, repository=DEFAULT_REPO, na_values=""):
    """Generates a dataframe with the data of the projects for work."""
    dataframes = [_download(work, p, repository, na_values) for p in projects]
    dataframe = _merge(dataframes, projects)
    _check(dataframe, dataframes)
    return dataframe


async def load_df_async(work, projects, repository=DEFAULT_REPO, na_values=""):
    return await asyncio.get_running_loop().run_in_executor(None, load_df, work, projects, repository, na_values)


def _download(work, project, repository, na_values):
    # FIXME: add proper URL escaping
    url = repository + "/" + work + "/" + project + ".tsv"
    return pd.read_csv(url, sep='\t', na_values=na_values, comment='#')


def _merge(dataframes, projects):
    """Merge the dataframes using a JOIN."""
    dataframe = dataframes[0]
    for df in dataframes[1:]:

        # keep backwards compatible
        if "sent_id" in dataframe.columns:
            dataframe = pd.merge(dataframe, df, on=["id", "sent_id", "token", "start", "end"],
                                 suffixes=_suffixes(projects))
        else:
            dataframe = pd.merge(dataframe, df, on=["id", "token", "start", "end"],
                                 suffixes=_suffixes(projects))

    return dataframe


def _suffixes(projects, delim="_"):
    l = _shortest_prefix_length(projects)
    return [delim + p[:l] for p in projects]


def _shortest_prefix_length(projects):
    """Find the smallest l such that the first l chars of projects are uniqe."""
    # FIXME: avoid fixed length
    for i in range(1, 10):
        if len(set([p[:i] for p in projects])) == len(projects):
            return i
    return None


def _check(dataframe, dataframes):
    for df in dataframes:
        assert len(df) == len(dataframe)


if __name__ == '__main__':
    pass
