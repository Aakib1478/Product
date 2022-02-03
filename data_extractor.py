from datetime import datetime
import MetaTrader5 as mt5
import pandas as pd
pd.set_option('display.max_columns', 500) # number of columns to be displayed
pd.set_option('display.width', 1500)      # max table width to display
import pytz

login=4999785250
server="MetaQuotes-Demo"
password="5rrpbqmp"


if not mt5.initialize():
    print("initialize() failed, error code =",mt5.last_error())
    quit()

# set time zone to UTC
timezone = pytz.timezone("Etc/UTC")
# create 'datetime' objects in UTC time zone to avoid the implementation of a local time zone offset
utc_from = datetime(2021, 3, 11, tzinfo=timezone)
utc_to = datetime(2022, 1, 13, tzinfo=timezone)
# get bars from USDJPY M5 within the interval of 2020.01.10 00:00 - 2020.01.11 13:00 in UTC time zone
rates = mt5.copy_rates_range("XAUUSD", mt5.TIMEFRAME_M5, utc_from, utc_to)

# shut down connection to the MetaTrader 5 terminal
mt5.shutdown()

# create DataFrame out of the obtained data
rates_frame = pd.DataFrame(rates)
rates_frame.rename(index=str,columns={'time':'old_time'},inplace=True)
rates_frame.rename(index=str,columns={'open':'Open'},inplace=True)
rates_frame.rename(index=str,columns={'high':'High'},inplace=True)
rates_frame.rename(index=str,columns={'low':'Low'},inplace=True)
rates_frame.rename(index=str,columns={'close':'Close'},inplace=True)

# convert time in seconds into the 'datetime' format
rates_frame['date_time']=pd.to_datetime(rates_frame['old_time'], unit='s')
rates_frame['Date'] = pd.to_datetime(rates_frame['date_time']).dt.strftime('%m/%d/%Y')
rates_frame['Time'] = [datetime.time(d) for d in rates_frame['date_time']]
rates_frame['Vol'] = 0
rates_frame['IO'] = 0


rates_frame = rates_frame.drop('date_time', 1)
rates_frame = rates_frame.drop('old_time', 1)
rates_frame = rates_frame.drop('tick_volume', 1)
rates_frame = rates_frame.drop('spread', 1)
rates_frame = rates_frame.drop('real_volume', 1)

new_order = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Vol', 'IO' ]
# rates_frame = rates_frame.reindex(new_order, axis=1)
rates_frame = rates_frame.loc[:, new_order]


# display data
print("\nDisplay dataframe with data")
print(rates_frame.head(10))
rates_frame.to_csv('EUR_5min.csv', index=False)
