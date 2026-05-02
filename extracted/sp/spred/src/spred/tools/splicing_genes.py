from scipy.stats import norm
from scipy.stats import chi2
from statsmodels.stats.multitest import multipletests
import numpy as np
import pandas as pd

def cal_fixed_effect(effect_sizes, se):
    effect_sizes = np.array(effect_sizes)
    se = np.array(se)
    
    # 检查输入数据长度是否一致
    if len(effect_sizes) != len(se):
        raise ValueError("The lengths of effect_sizes and se must be the same.")
    
    # 至少需要2个数据点才能计算合并效应值
    if len(effect_sizes) < 2:
        raise ValueError("At least two data points are required to perform the meta-analysis.")
    
    # 固定效应权重
    weights_fixed = 1 / se**2
    
    # 固定效应模型的加权平均效应
    fixed_effect_estimate = np.sum(weights_fixed * effect_sizes) / np.sum(weights_fixed)
    
    # 固定效应模型的标准误
    fixed_effect_se = np.sqrt(1 / np.sum(weights_fixed))
    
    # 计算Q值（异质性统计量）
    Q = np.sum(weights_fixed * (effect_sizes - fixed_effect_estimate)**2)
    
    # 自由度
    k = len(effect_sizes)  # 样本数量
    df = k - 1
    
    # Q值的p值
    p_value_q = chi2.sf(Q, df)

    return Q, p_value_q, fixed_effect_estimate, fixed_effect_se

def cal_sdgene(df_tgt):
    all_infos = []
    for idx,val in df_tgt.groupby('gene_name'):
        infos = []
        val = val.dropna()
        if val['transcript_id'].shape[0]>1:
            infos.extend([val['gene_name'].to_list()[0]])
            
            Q,p_Q, effect, se = cal_fixed_effect(np.array(val['log2FoldChange'].to_list()),np.array(val['lfcSE'].to_list()))
            infos.extend([Q,p_Q, effect, se])
            isoforms = []
            for idx2, each in val.iterrows():
                isoforms.append(f"{each['transcript_id']},{each['log2FoldChange']},{each['lfcSE']},{each['pvalue']}")
            infos.append(';'.join(isoforms))
            all_infos.append(infos)
    df  = pd.DataFrame(all_infos,columns = ['gene_name','Q','pvalue', 'effect', 'se','isoforms'])
    df.sort_values('pvalue',inplace=True)
    df['padj'] = multipletests(df['pvalue'],method='fdr_bh')[1]
    return df



