import data_parser as dao_parser
import model
from dao.expert import Expert
from dao.portfolio import Portfolio
from rules import smac, emac
from constants import STOCKS
import sys
import os
import numpy as np

def x_mt(prices, t):
  prices_t = prices[t]
  prices_t_1 = prices[t-1]
  return (np.array(prices_t)/np.array(prices_t_1)).tolist()

def get_params(t):
  if t < 7:
    return 3,3
  elif t >= 7:
    return 3,7
  elif t >= 120:
    return 7,30

def main():

  sys.path.insert(0, os.getcwd())
  days, _ = dao_parser.get_days()

  T = len(days)
  t_min = 5
  profits = np.zeros(T)

  prices_dfs = dao_parser.close_prices(days)
  prices = [df.tolist() for df in prices_dfs]

  smac_exp = Expert(smac.signal, len(days[0]), 2)
  emac_exp = Expert(emac.signal, len(days[0]), 2)

  experts = [smac_exp, emac_exp]
  N = len(experts)

  q = [0.] * N
  h = [0.] * N

  portfolio = Portfolio([0] * 11, STOCKS)

  n1 = [0] * T
  n2 = [0] * T
  for i in range(4, T):
    n1[i] = min(i, 3)
    n2[i] = min(i,3)
    if(i > 7):
      n2[i] = min(i, 7)

    if(i > 120):
      n1[i] = 7
      n2[i] = 30

  # h = exp_gen_alg
  # update expert welath
  # Renormalize expert mixtures
  # Update Portfolio Controls
  # Portfolio Wealth

  print("STARTING SIM")
  for t in range(t_min, T+1):
    print(t)
    prices_t = prices[0:t]
    print("Signals")
    signals = [exp.rule(prices_t, n1[t-1], n2[t-1], port=portfolio) for exp in experts]
    print("Update H")
    h = model.exp_gen_alg(prices_t, n1[0:t], n2[0:t], experts, h, signals)
    print("H: ", h)
    x_mt_lst = x_mt(prices_t, t-1)
    print("Update Experts")
    for i in range(len(experts)):
      experts[i].update_strategy(signals[i])
      experts[i].update_wealth(x_mt_lst)

    for i in range(len(q)):
      q[i] = experts[i].get_wealth()

    print("Normalize Q")
    for i in range(len(q)):
      if(sum(abs(q[j] - 1./N * sum(q)) for j in range(len(q)))) == 0:
        q[i] = 0.
      else:
        q[i] = (q[i] - 1./N * sum(q))/(sum(abs(q[j] - 1./N * sum(q)) for j in range(len(q))))

    print("Update Portfolio Controls")
    portfolio.update_controls(q, h)

    print("Update Portfolio Wealth")
    delta = portfolio.update_wealth(x_mt_lst)
    profits[t-1] = profits[t-2] + delta - 1

  print(profits[T-1])
  print(portfolio.get_wealth())

main()
