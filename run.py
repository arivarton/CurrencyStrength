import datetime as dt
from pandas_datareader.oanda import get_oanda_currency_historical_rates
import numpy as np

window_size = 200
time = 2000

start = dt.datetime.today() - dt.timedelta(days=time)
end = dt.datetime.today()

base_currency = ['EUR', 'GBP', 'JPY', 'AUD', 'NZD', 'CHF', 'CAD', 'USD']


# Heavily inspired by this https://startpythonml.wordpress.com/2016/03/13/smoothed-moving-average-and-variations/
# and this https://www.dailyfx.com/forex/education/trading_tips/post_of_the_day/2011/06/15/How_to_Create_a_Trading_Edge_Know_the_Strong_and_the_Weak_Currencies.html
x = np.array([np.arange(0, time)])

weights = np.repeat(1.0, window_size) / window_size

for quote_currency in base_currency:
    rating = 0
    if base_currency != quote_currency:
        df_rates = get_oanda_currency_historical_rates(
            start, end,
            quote_currency=quote_currency,
            base_currency=base_currency
        )
    else:
        pass
    for base in base_currency:
        y = np.array([df_rates[base + '/' + quote_currency].values])
        yMA = np.convolve(y[0, :], weights, 'valid')
        average_rate = yMA[len(yMA) - 1]
        closing_rate = df_rates[base + '/' + quote_currency][time - 1]
        if yMA[len(yMA) - 1] < df_rates[base + '/' + quote_currency][time - 1]:
            rating -= 1
        elif yMA[len(yMA) - 1] > df_rates[base + '/' + quote_currency][time - 1]:
            rating += 1
        elif yMA[len(yMA) - 1] == df_rates[base + '/' + quote_currency][time - 1]:
            pass
        else:
            print('Something went wrong')
    print('Final rating of ' + quote_currency + ': ' + str(rating))
