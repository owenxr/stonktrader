class Expert:
  def __init__(self, rule, num, params):
    self.strategy = [0.] * num
    self.wealth = 1
    self.rule = rule
    self.params = params

  def update_strategy(self, strategy):
    self.strategy = strategy
  
  def update_wealth(self, x_lst):
    delta = sum((self.strategy[m] * (x_lst[m] - 1.)) for m in range(len(x_lst))) + 1

    self.wealth = self.wealth * delta
    return delta
  
  def get_wealth(self):
    return self.wealth