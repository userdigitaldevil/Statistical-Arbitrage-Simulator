import matplotlib.pyplot as plt

def plot_spread(S1, S2):
    spread = S1 - S2
    plt.figure(figsize=(12, 4))
    plt.plot(spread)
    plt.title('Spread')
    plt.show()

def plot_cum_returns(cum_returns):
    plt.figure(figsize=(12, 4))
    plt.plot(cum_returns)
    plt.title('Cumulative Returns')
    plt.show() 