import pandas as pd
import numpy as np

def zscore(series):
    return (series - series.mean()) / np.std(series)

def backtest_pair(S1, S2, entry_z=2, exit_z=0):
    spread = S1 - S2
    z = zscore(spread)
    positions = pd.DataFrame(index=spread.index, columns=['long', 'short'])
    positions['long'] = 0
    positions['short'] = 0

    in_long = False
    in_short = False
    returns = []

    for i in range(1, len(z)):
        if not in_long and z[i] < -entry_z:
            in_long = True
            in_short = False
        elif in_long and z[i] > -exit_z:
            in_long = False

        if not in_short and z[i] > entry_z:
            in_short = True
            in_long = False
        elif in_short and z[i] < exit_z:
            in_short = False

        positions.iloc[i]['long'] = 1 if in_long else 0
        positions.iloc[i]['short'] = 1 if in_short else 0

        ret = 0
        if in_long:
            ret = (S1.iloc[i] - S1.iloc[i-1]) - (S2.iloc[i] - S2.iloc[i-1])
        elif in_short:
            ret = (S2.iloc[i] - S2.iloc[i-1]) - (S1.iloc[i] - S1.iloc[i-1])
        returns.append(ret)

    returns = np.array(returns)
    results = {
        'returns': returns,
        'cum_returns': np.cumsum(returns),
        'positions': positions
    }
    return results 