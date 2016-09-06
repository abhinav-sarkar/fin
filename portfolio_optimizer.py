import pandas as pd
import datetime
import pandas_datareader.data as web
import matplotlib.pyplot as plt
import numpy as np
from cvxopt import matrix, solvers, blas

start = datetime.datetime(2010, 1, 1)
end = datetime.datetime(2016, 8, 1)
interest_rate = 0.03/12.0
rmin = 0.02
shift = 1

def plotter(dataframe):
    dataframe.plot()
    plt.show()


symbols = [
    #'IJH', #iShares Core S&P 500 Mid-Cap
    #'IVW', #iShares S&P 500 Growth
    #'IJR', #iShares Core S&P 500 Small-Cap
    #'AAPL',
    #'GLD',
    #'SPY'
    'VTI',
    'VTV',
    'VOE',
    'VBR',
    'VEA',
    'VWO',
    'VTIP',
    'SHV',
    'MUB',
    'LQD',
    'BNDX',
    'VWOB'
 ]

data = {}
for symbol in symbols:
    data[symbol] = web.DataReader(symbol, 'yahoo', start, end)

price = pd.DataFrame({sym: dataframe['Adj Close'] for sym,dataframe in data.items()})

shift_returns = (price/price.shift(shift)) - 1
filter_len = shift
shift_returns_mean = pd.ewma(shift_returns,span=filter_len)
shift_returns_var = pd.ewmvar(shift_returns,span=filter_len)

ew = pd.ewmcov(shift_returns, span=filter_len)
S = matrix(ew.ix[-1].values)
pbar = matrix(shift_returns_var.ix[-1].values)

# Create constraint matrices
G = -matrix(np.eye(n))
h = matrix(0.0, (n ,1))
A = matrix(1.0, (1, n))
b = matrix(1.0)

# Calculate efficient frontier weights using quadratic programming
portfolios = [solvers.qp(mu*S, -pbar, G, h, A, b)['x'] 
              for mu in mus]

## CALCULATE RISKS AND RETURNS FOR FRONTIER
returns = [blas.dot(pbar, x) for x in portfolios]
risks = [np.sqrt(blas.dot(x, S*x)) for x in portfolios]

## CALCULATE THE 2ND DEGREE POLYNOMIAL OF THE FRONTIER CURVE
m1 = np.polyfit(returns, risks, 2)
x1 = np.sqrt(m1[2] / m1[0])

# CALCULATE THE OPTIMAL PORTFOLIO
wt = solvers.qp(matrix(x1 * S), -pbar, G, h, A, b)['x']
print (np.asarray(wt))

plt.ylabel('mean')
plt.xlabel('std')
plt.plot(risks, returns, 'y-o')
plt.show()