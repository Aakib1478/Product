from include.trade import Trade
from include.tick import Tick
from include.rates import Rates
from include.utilities import Utilities
import pandas as pd
import pandas_ta as ta
import MetaTrader5 as Mt5

time_frame = 1
trade = Trade('test1',  # Expert name
              0.1,  # Expert Version
              'EURUSD',  # symbol
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
    rates = Rates(trade.symbol, time_frame, 0, 201)
    pd_rates_close = pd.Series(rates.close)

    reversed_rates_open = rates.open[::-1]
    reversed_rates_high = rates.high[::-1]
    reversed_rates_low = rates.low[::-1]
    reversed_rates_close = rates.close[::-1]

    sma100 = ta.sma(pd_rates_close, length=200)
    sma100_0 = sma100.iloc[-1]

    rsi = ta.rsi(pd_rates_close, length=2)
    rsi2_0 = rsi.iloc[-1]
    rsi2_1 = rsi.iloc[-2]


    if not len(Mt5.positions_get(symbol=trade.symbol)) == 1:
        # ENTRY SECTION STARTS
        '''
        WHEN: open[1] > sma100[0] and open[0] > sma100[0] and rsi2[0] < 10 and rsi2[1] < 10
        THEN: enter
        '''
        entry_condition1 = False
        entry_condition2 = False
        entry_condition3 = False
        entry_condition4 = False


        if reversed_rates_open[1] > sma100_0:
            entry_condition1 = True
        if reversed_rates_open[0] > sma100_0:
            entry_condition2 = True
        if rsi2_0 > 15:
            entry_condition3 = True
        if  rsi2_1 < 15:
            entry_condition4 = True

        condition_counter = 4
        if entry_condition1:
            condition_counter -= 1
        if entry_condition2:
            condition_counter -= 1
        if entry_condition3:
            condition_counter -= 1
        if entry_condition4:
            condition_counter -= 1

        buy = (entry_condition1 and entry_condition2 and entry_condition3 and entry_condition4)
        if buy:
            print('condition 1 reversed_rates_open[1] > sma100_0', reversed_rates_open[1], sma100_0)
            print('entry_condition2 = reversed_rates_open[0] > sma100_0', reversed_rates_open[1], sma100_0)
            print('entry_condition3 = rsi2_0 > 15 --', entry_condition3)
            print('entry_condition4 = rsi2_1 < 15 --', entry_condition4)

            print('**** entry condition(s) met - SENDING ENTRY REQUEST ****')
        # else:
        #     print(condition_counter, ' entry condition(s) not met')
        sell = False
        trade.open_position(buy, sell, 'take long entry')
    # ENTRY SECTION ENDS

    # EXIT SECTION STARTS
    '''
    WHEN: 5 mins since trade or rsi2[0] > 90 or open[0] < sma100[0]

    THEN: exit
    '''
    if len(Mt5.positions_get(symbol=trade.symbol)) == 1:
        util = Utilities()
        exit_condition1 = util.exit_trade_after_these_minutes(trade.symbol, time_frame, 5, tick.time)
        exit_condition2 = rsi2_0 > 85
        exit_condition3 = reversed_rates_open[0] < sma100_0

        exit = exit_condition1 or exit_condition2 or exit_condition3
        if exit:
            print('**** Exiting Trade ****')
            trade.close_position('exit condition(s) met')
        # else:
        #     print('exit condition(s) not met')

    # EXIT SECTION ENDS

print('Finishing the program.')
print('Program finished.')
