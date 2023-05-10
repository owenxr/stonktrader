import numpy as np
from dao.portfolio import Portfolio

def ema_ind(prices, days, prev) -> list:
  alpha = 2. / (days + 1.)

  prices_arr = np.array(prices)

  return (alpha * prices_arr[days] + (1.-alpha) * np.array(prev)).tolist()