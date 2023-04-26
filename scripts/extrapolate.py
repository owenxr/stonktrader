import pandas as pd
import os
from datetime import datetime
from pathlib import Path
import pytz
import csv

################################################################################
#                   Constant                                     
################################################################################
ARCHIVE = os.path.join(os.getcwd(), Path("data/archive"))
ARCHIVE_LST = [os.path.join(ARCHIVE, "2020"), os.path.join(ARCHIVE, "2021"), \
               os.path.join(ARCHIVE, "2022"), os.path.join(ARCHIVE, "2023")]
INTERDAY = os.path.join(os.getcwd(), Path("data/interday"))
COLUMNS = ['TimeStamp', 'SPY', 'QQQ', 'IWM', 'AAPL', 'MSFT', 'NVDA', 'XLK', 'XLP', 'XLY', 'XTN', 'HYG']
STOCKS = ['SPY', 'QQQ', 'IWM', 'AAPL', 'MSFT', 'NVDA', 'XLK', 'XLP', 'XLY', 'XTN', 'HYG']

# YYYY-MM-DD HH:MM:SS.FFF"
datetime_fmt = "%Y-%m-%d %H:%M:%S.%f"

# Grab data for a single day for a stock
def get_interday_info(df, stock):
  open_pr = df[stock].iloc[0]
  close_pr = df[stock].iloc[-1]
  high = df[stock].max()
  low = df[stock].min()

  return open_pr, close_pr, high, low

################################################################################
#                   Parser Data into Interday Data                                       
################################################################################
def parse_interday(df, week_num):
  # Stock, Open, Close, High, Low
  mon_csv = df.loc[df["TimeStamp"].dt.weekday == 0]
  tues_csv = df.loc[df["TimeStamp"].dt.weekday == 1]
  wed_csv = df.loc[df["TimeStamp"].dt.weekday == 2]
  thurs_csv = df.loc[df["TimeStamp"].dt.weekday == 3]
  fri_csv = df.loc[df["TimeStamp"].dt.weekday == 4]

  day_dfs = [mon_csv, tues_csv, wed_csv, thurs_csv, fri_csv]

  decr = 0
  for i in range(len(day_dfs)):
    if day_dfs[i].empty == True:
      decr += 1
      continue

    with open(os.path.join(INTERDAY, f'day{week_num * 5 + i + 1 - decr}.csv'), 'w') as csvfile:
      csv_writer = csv.writer(csvfile, delimiter=',')
      csv_writer.writerow(['Stock', 'Open', 'Close', 'High', 'Low'])
      for s in STOCKS:
        open_pr, close_pr, high, low = get_interday_info(day_dfs[i], s)
        csv_writer.writerow([s, open_pr, close_pr, high, low])


################################################################################
#                   Parser Data into Intraday Data                                       
################################################################################
def parse_intraday(df):
  mon_csv = df.loc[df["TimeStamp"].dt.weekday == 0]
  tues_csv = df.loc[df["TimeStamp"].dt.weekday == 1]
  wed_csv = df.loc[df["TimeStamp"].dt.weekday == 2]
  thurs_csv = df.loc[df["TimeStamp"].dt.weekday == 3]
  fri_csv = df.loc[df["TimeStamp"].dt.weekday == 4]


################################################################################
################################################################################
#
#                   Main Folder Parser                                         
#
################################################################################
################################################################################
week = 0
for folder in ARCHIVE_LST:

  if folder != ".DS_Store":
    file_lst = os.listdir(Path(folder))
    file_lst.sort()

    for file in file_lst:

      dt_fmt = datetime_fmt
      print(file)
      dat = pd.read_csv(os.path.join(folder, file))
      dat.columns = ['ID','TimeStamp','/ES','/NQ','/RTY','SPY','QQQ','IWM','AAPL',\
                     'MSFT','NVDA','XLK','XLF','XLP','XLY','XTN','HYG','/ES SMA20',\
                      '/ES SMA50','/ES volume','TLT','TLT volume']
      dat = dat[COLUMNS]

      # Data Does a Funny Formatting
      if "2020 08 14" in file:
        dt_fmt = "%m/%d/%y %H:%M"
      elif "2020 08 21" in file:
        dt_fmt = "%m/%d/%Y %H:%M"
      elif "2022 11 25" in file:
        dt_fmt = "%m/%d/%Y %H:%M:%S"

      # Use Date Time Formatting for TimeStamp
      dat["TimeStamp"] = pd.to_datetime(dat["TimeStamp"], format=dt_fmt)

      # Set the timezone to US Eastern Time
      eastern_tz = pytz.timezone("US/Eastern")

      # Filter the rows based on Stock Open Time Range
      start_time = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
      start_time = eastern_tz.localize(start_time)
      end_time = datetime.now().replace(hour=16, minute=0, second=0, microsecond=0)
      end_time = eastern_tz.localize(end_time)
      mask = (dat["TimeStamp"].dt.weekday.between(0, 4) &  # Monday to Friday
              (dat["TimeStamp"].dt.time >= start_time.time()) &
              (dat["TimeStamp"].dt.time <= end_time.time()))
      filtered_csv = dat.loc[mask]

      if filtered_csv.empty == False:
        parse_interday(filtered_csv, week)
        week += 1