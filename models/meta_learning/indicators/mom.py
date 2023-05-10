import numpy as np

def mom_ind(prices, days) -> list:
  t = len(prices) - 1
  return (np.array(prices[t]) - np.array(prices[t - days])).tolist()