# %%
import pandas as pd
import pingouin as pg
import scipy as sp
from tableone import TableOne

# %%
def mannwhitneyu_tableone(*args,**kwargs):
    htest = sp.stats.mannwhitneyu(*args, **kwargs)
    return htest.pvalue

def tabletwo(df, groupby='animaltype', mannwhitneyu=True):
    cont_cols = df.columns.tolist()
    if groupby in cont_cols: cont_cols.remove(groupby)

    ttest_equal_var = False

    if mannwhitneyu:
        htest = {col: mannwhitneyu_tableone for col in cont_cols}
        # t1 = TableOne(df, categorical=[], continuous=cont_cols, groupby='animaltype', pval=True, htest_name=True, decimals=2, htest=htest)
        t1 = TableOne(df, categorical=[], continuous=cont_cols, groupby=groupby, pval=True, htest_name=True, decimals=2, htest=htest, ttest_equal_var=ttest_equal_var)
    else:
        t1 = TableOne(df, categorical=[], continuous=cont_cols, groupby=groupby, pval=True, htest_name=True, decimals=2, normal_test=True, ttest_equal_var=ttest_equal_var)
        # t1 = TableOne(df, categorical=[], continuous=cont_cols, groupby=groupby, pval=True, htest_name=True, decimals=2, nonnormal=cont_cols, ttest_equal_var=ttest_equal_var)

    htest_full = {col: pg.mwu for col in cont_cols} # pingouin
    t1_htest = t1.htest_table
    for v in t1_htest.index:
    # for v in t1_scores.htest_table.index:
        is_continuous = t1_htest.loc[v]['continuous']
        is_categorical = ~t1_htest.loc[v]['continuous']
        is_normal = ~t1_htest.loc[v]['nonnormal']

        # if continuous, group data into list of lists
        if is_continuous:
            catlevels = None
            grouped_data = {}
            for s in t1._groupbylvls:
                lvl_data = df.loc[df[groupby] == s, v]
                # coerce to numeric and drop non-numeric data
                lvl_data = lvl_data.apply(pd.to_numeric,
                                            errors='coerce').dropna()
                # append to overall group data
                grouped_data[s] = lvl_data.values
            min_observed = min([len(x) for x in grouped_data.values()])
        # if categorical, create contingency table
        elif is_categorical:
            catlevels = sorted(df[v].astype('category').cat.categories)
            cross_tab = pd.crosstab(df[groupby].rename('_groupby_var_'), df[v])
            min_observed = cross_tab.sum(axis=1).min()
            grouped_data = cross_tab.T.to_dict('list')

        # minimum number of observations across all levels
        # t1_htest.loc[v, 'min_observed'] = min_observed  # type: ignore
        assert min_observed == t1_htest.loc[v, 'min_observed']

        # compute pvalues
        warning_msg = None
        htest_obj, test_name, warning_msg = t1.statistics._p_test(v, grouped_data, is_continuous, is_categorical,  # type: ignore
                                                is_normal,  min_observed, htest_full, ttest_equal_var)  # type: ignore

        effect_cols = ['RBC', 'CLES']
        for effect_col in effect_cols:
            t1_htest.loc[v, effect_col] = htest_obj[effect_col].item()

    return t1