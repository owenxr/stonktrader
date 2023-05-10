from indicators import sma
import numpy as np

def signal(prices, short_per, long_per, **kwargs):
  short = sma.sma_ind(prices, short_per)
  long = sma.sma_ind(prices, long_per)

  return [1 if short[i] > long[i] else -1 if short[i] < long[i] else 0 for i in range(len(short))]