import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import coint

def find_cointegrated_pairs(data: pd.DataFrame, significance: float = 0.05):
    n = data.shape[1]
    score_matrix = np.zeros((n, n))
    pvalue_matrix = np.ones((n, n))
    keys = data.columns
    pairs = []
    for i in range(n):
        for j in range(i+1, n):
            S1 = data[keys[i]]
            S2 = data[keys[j]]
            score, pvalue, _ = coint(S1, S2)
            score_matrix[i, j] = score
            pvalue_matrix[i, j] = pvalue
            if pvalue < significance:
                pairs.append((keys[i], keys[j], pvalue))
    pairs.sort(key=lambda x: x[2])
    return pairs, score_matrix, pvalue_matrix 