from indicators import ema
from indicators import sma

emas = {}

def signal(prices, short_per, long_per, **kwargs) -> list:
  portfolio = kwargs['port']

  prev_short = sma.sma_ind(prices, short_per)
  prev_long = sma.sma_ind(prices, long_per)

  if portfolio in emas:
    prev_short = emas[portfolio]['short']
    prev_long = emas[portfolio]['long']
  else:
    emas[portfolio] = {}
    emas[portfolio]['short'] = 0
    emas[portfolio]['long'] = 0

  short = ema.ema_ind(prices, short_per, prev_short)
  long = ema.ema_ind(prices, long_per, prev_long)

  emas[portfolio]['short'] = short
  emas[portfolio]['long'] = long

  return [1 if short[i] > long[i] else -1 if short[i] < long[i] else 0 for i in range(len(short))]