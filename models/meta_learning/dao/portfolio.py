class Portfolio:
  def __init__(self, controls, stocks):
    self.controls = controls
    self.stocks = stocks
    self.wealth = 1
  
  def update_controls(self, q, exp_cont):
    print(q)
    self.controls = sum(q[n] * exp_cont[n] for n in range(len(q)))
  
  def update_wealth(self, x_lst):
    delta = sum(self.controls[m] * (x_lst[m] - 1.) for m in range(len(x_lst))) + 1
    self.wealth = self.wealth * delta
    return delta

  def get_wealth(self):
    return self.wealth
  
  def get_controls(self):
    return self.controls