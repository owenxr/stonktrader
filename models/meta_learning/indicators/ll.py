import numpy as np

def ll_ind(prices, days) -> list:
  t = len(prices) - 1
  lst = []

  for i in range(days):
    lst.append(min(prices[t-i]))

  return lst