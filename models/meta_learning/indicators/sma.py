import numpy as np

def sma_ind(prices, days) -> list:
  value = np.array([0.] * 11)
  t = len(prices) - 1

  for i in range(days-1):
      value += np.array(prices[t - i])

  return (1/days * value).tolist()