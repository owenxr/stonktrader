import numpy as np

def sign(x):
  if x > 0:
    return 1
  if x < 0:
    return -1
  else:
    return 0

def filter_close(start_day, prices, output_s, f):
  result = []
  for i in range(len(output_s)):
    tmp_lst = []
    for lst in prices[start_day:]:
      if f(output_s[i]):
        tmp_lst.append(lst[i])

    result.append(tmp_lst)
  return result

def get_output_s(prev_exp_cont, current_s):
  output_s = np.zeros(len(current_s))

  if np.all(prev_exp_cont == 0) or np.all(prev_exp_cont == np.NAN):
    output_s = current_s

  else:
    for i in range(len(current_s)):
      if current_s[i] == 0:
        output_s[i] = sign(prev_exp_cont[i])
      else:
        output_s[i] = np.array(current_s)[i]

  return output_s

def controls(prices : list, output_s):
  close_prices = prices[len(prices) - 1]
  if np.all(output_s == 0):
    return np.zeros(len(output_s) + 1)
  
  elif np.all(output_s >= 0):
    start_day = max(0, len(close_prices) - 120)
    
    w = 0.5 * output_s
    np.append(w,-0.5)
    
    filtered = filter_close(start_day, prices, output_s, lambda x: {x > 0})
    vol = []
    for lst in filtered:
      vol.append(np.std(lst))

    for i in range(len(w)):
      if(output_s[i] > 0):
        w[i] = 1/(sum(vol)) * w[i] * vol[i]

  elif np.all(output_s <= 0):
    start_day = max(0, len(close_prices) - 120)
    
    w = 0.5 * output_s
    np.append(w,0.5)
    
    filtered = filter_close(start_day, prices, output_s, lambda x: {x < 0})
    vol = []
    for lst in filtered:
      vol.append(np.std(lst))

    for i in range(len(w)):
      if(output_s[i] < 0):
        w[i] = 1/(sum(vol)) * w[i] * vol[i]

  else:
    start_day = max(0, len(close_prices) - 120)
    
    w = output_s
    np.append(w,0.)
    
    filtered_1 = filter_close(start_day, prices, output_s, lambda x: {x > 0})
    filtered_2 = filter_close(start_day, prices, output_s, lambda x: {x < 0})
    
    vol_1 = []
    for lst in filtered_1:
      tmp = []
      for e in lst:
        tmp.append(e)
      
      vol_1.append(np.std(tmp))

    vol_2 = []
    for lst in filtered_2:
      tmp = []
      for e in lst:
        tmp.append(e)
      
      vol_2.append(np.std(tmp))

    for i in range(len(w)):
      if(output_s[i] > 0):
        w[i] = 0.5 * 1/(sum(abs(e) for e in vol_1)) * w[i] * vol_1[i]
      elif(output_s[i] < 0):
        w[i] = 0.5 * 1/(sum(abs(e) for e in vol_2)) * w[i] * vol_2[i]

    w[len(w)-1] = sum(w)

  return w

def exp_gen_alg(prices, n1, n2, w_set, prev_cont, signals):
  curr_cont = [0.] * len(w_set)
  # Short Term Params
  L = len(n1)
  # Long term Params
  K = len(n2)


  for w_ind in range(len(w_set)):
    for l in range(L):
      l_1 = n1[l]
      for k in range(K):
        if w_set[w_ind].params == 1:
          break

        k_1 = n2[k]
        if k_1 > l_1:
          outputs = get_output_s(prev_cont[w_ind], signals[w_ind])
          weights = controls(prices, np.array(outputs))
          # update h
          curr_cont[w_ind] = weights
        
    if w_set[w_ind].params == 1:
      outputs = get_output_s(prev_cont[w_ind], signals[w_ind])
      weights = controls(prices, np.array(outputs))
      # update h
      curr_cont[w_ind] = weights
            
  return curr_cont
