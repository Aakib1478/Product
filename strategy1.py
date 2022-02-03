from include.trade import Trade
from include.tick import Tick
from include.rates import Rates
from include.utilities import Utilities
import pandas as pd
import pandas_ta as ta
import MetaTrader5 as Mt5


trade = Trade('test1',  # Expert name
              0.1,  # Expert Version
              'XAUUSD',  # symbol
              567,  # Magic number
              0.01,  # lot, it is a floating point.
              25,  # stop loss
              300,  # emergency stop loss
              25,  # take profit
              300,  # emergency take profit
              )

time = 0
while True:

    tick = Tick(trade.symbol)
    # rates object takes - symbol, time_frame, start_pos, period
    rates = Rates(trade.symbol, 15, 0, 20)


    pd_rates_close = pd.Series(rates.close)

    # ENTRY SECTION STARTS
    '''
    WHEN: open[1] > close[4], open[0] <= open[1], open[0] <= open[7], low[0] <= BollingerBand(c,20,-2)[0]
    THEN: enter
    '''
    reversed_rates_open = rates.open[::-1]
    reversed_rates_high = rates.high[::-1]
    reversed_rates_low = rates.low[::-1]
    reversed_rates_close = rates.close[::-1]


    entry_condition1 = reversed_rates_open[0] > reversed_rates_close[4]
    entry_condition2 = reversed_rates_open[0] > reversed_rates_open[1]
    entry_condition3 = reversed_rates_open[0] > reversed_rates_open[7]
    entry_condition4 = reversed_rates_low[0] > reversed_rates_open[7]
    #  ta.bbands will return pd.DataFrame: lower, mid, upper, bandwidth, and percent columns.
    bb_lower = ta.bbands(pd_rates_close, length=20).tail(1)['BBL_20_2.0']
    entry_condition5 = reversed_rates_low[0] > bb_lower

    condition_counter = 4
    if entry_condition1:
        condition_counter -= 1
    if entry_condition2:
        condition_counter -= 1
    if entry_condition3:
        condition_counter -= 1
    if entry_condition4:
        condition_counter -= 1

    if tick.time_msc != time:
        buy = (entry_condition1 and entry_condition2 and entry_condition3 and entry_condition4 and entry_condition5)
        if buy:
            print('**** entry condition(s) met - SENDING ENTRY REQUEST ****')
        else:
            print(condition_counter, ' entry condition(s) not met')
        sell = False
        trade.open_position(buy, sell, 'take long entry')
    # ENTRY SECTION ENDS

    # EXIT SECTION STARTS
    '''
    WHEN: MaxTime 11, Exit on All: open[1] > open[7], open[1] > high[8], open[1] <= close[6], rsi(close,14)[0] > rsi(close,14)[1]
    THEN: exit
    '''
    if len(Mt5.positions_get(symbol=trade.symbol)) == 1:
        util = Utilities()
        exit_condition1 = util.exit_trade_after_these_minutes(trade.symbol, 15, 11, tick.time)
        exit_condition2 = reversed_rates_open[1] > reversed_rates_open[7]
        exit_condition3 = reversed_rates_open[1] > reversed_rates_high[8]
        exit_condition4 = reversed_rates_open[1] > reversed_rates_close[6]

        rsi = ta.rsi(pd_rates_close, length=14)
        rsi_0 = rsi.iloc[-1]
        rsi_1 = rsi.iloc[-2]

        exit_condition5 = rsi_0 > rsi_1

        exit = exit_condition1 or exit_condition2 or exit_condition3 or exit_condition4 or exit_condition5
        trade.close_position('exit condition(s) met')

    # EXIT SECTION ENDS

print('Finishing the program.')
print('Program finished.')
