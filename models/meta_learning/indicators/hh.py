import numpy as np

def hh_ind(prices, days) -> list:
  t = len(prices) - 1
  lst = []

  for i in range(days):
    lst.append(max(prices[t-i]))

  return lst