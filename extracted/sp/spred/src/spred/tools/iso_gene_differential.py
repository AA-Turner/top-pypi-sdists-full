from pydeseq2.dds import DeseqDataSet
from pydeseq2.ds import DeseqStats
import numpy as np
import pandas as pd
    
def filter_by_express(df, zero_ratio=0.5, how='isoforms'):
    iso_exp_mtx = (df > 0).sum(axis=1)
    iso_filter_lst = iso_exp_mtx[iso_exp_mtx>len(df.columns)*zero_ratio].index.to_list()
    print(f"{len(iso_filter_lst)} out of {len(df.index)} {how} for further analysis" )
    
    df_tgt = df.loc[iso_filter_lst]
    return df_tgt


def cal_diff(df_mtx, df_meta, group_item, cases_str, control_str, covariance_list=[]):
    # 构建 design 字符串
    design_formula = "~ " + " + ".join([group_item] + covariance_list)
    print(f'design_formula is: {design_formula}')
    
    # 创建 DESeq2 数据集
    dds = DeseqDataSet(
        counts=df_mtx.T.astype(int),
        metadata=df_meta,
        design=design_formula,
        refit_cooks=True
    )
    dds.deseq2()
    # 进行差异表达分析
    ds = DeseqStats(dds, contrast=[group_item, cases_str, control_str])
    ds.summary()
    res = ds.results_df.sort_values('padj')
    
    #df_m = df_anno[['gene_name','transcript_name','transcript_type','gene_type']].merge(res, left_index=True,right_index=True)
    
    return res





