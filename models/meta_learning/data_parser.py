import pandas as pd
import os
from pathlib import Path

INTERDAY = os.path.join(os.getcwd(), Path("../../data/interday"))

def get_days():
  days = []  # create an empty list to store the DataFrames
  for filename in os.listdir(INTERDAY):
    if filename.endswith('.csv'):  # check if the file is a CSV file
      filepath = os.path.join(INTERDAY, filename)
      df = pd.read_csv(filepath)  # read the CSV file into a DataFrame
      days.append(df)  # add the DataFrame to the list

  combined = pd.concat(days, ignore_index=True)

  return days, combined

def close_prices(days):
  prices = []
  for df in days:
    prices.append(df['Close'])

  return prices