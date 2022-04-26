import pandas as pd

from pandas_datareader import data as pdr

import yfinance as yf

import numpy as np

import datetime as dt
import matplotlib.pyplot as plt
tickers = []
list = []
dollars = 0
assets = []



num = int(input("Enter how many different stocks you have (whole number): "))
print("")
print("Enter the ticker and count of each stock one by one when prompted below")
print("Make sure to enter the ticker correctly")
print("To verify a ticker search on Yahoo Finance for the ticker")
print("")
print("Exepct a delay after entering each stock")
print("")

for x in range(1,num + 1):    

    tick = input("Ticker: ")
    tickers.append(tick)
    w = float(input("Enter count: "))
   
    print("")
    n = yf.Ticker(tick).info['regularMarketPrice']
    
    dollars = dollars + w * n
    assets.append(w * n)
   

  #getting portfolio weighting
for i in range(len(assets)):
  assets[i] = assets[i]/dollars
# Create our portfolio of equities


weights = np.array(assets)



 

# Set an initial investment level

initial_investment = dollars
# Download closing prices

data = pdr.get_data_yahoo(tickers, start=dt.date.today() - pd.DateOffset(years=2), end=dt.date.today())['Close']

 

#From the closing prices, calculate periodic returns

returns = data.pct_change()


returns.tail()


cov_matrix = returns.cov()

cov_matrix




# Calculate mean returns for each stock

avg_rets = returns.mean()

 

# Calculate mean returns for portfolio overall, 

# using dot product to 

# normalize individual means against investment weights

 # https://en.wikipedia.org/wiki/Dot_product#:~:targetText=In%20mathematics%2C%20the%20dot%20product,and%20returns%20a%20single%20number.

port_mean = avg_rets.dot(weights)

 

# Calculate portfolio standard deviation

port_stdev = np.sqrt(weights.T.dot(cov_matrix).dot(weights))

 

# Calculate mean of investment

mean_investment = (1+port_mean) * initial_investment

             

# Calculate standard deviation of investmnet

stdev_investment = initial_investment * port_stdev






# Select our confidence interval (I'll choose 95% here)

conf_level1 = 0.05


# Using SciPy ppf method to generate values for the

# inverse cumulative distribution function to a normal distribution

# Plugging in the mean, standard deviation of our portfolio

# as calculated above

# https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.norm.html

#converting to normal dist

from scipy.stats import norm

cutoff1 = norm.ppf(conf_level1, mean_investment, stdev_investment)




#Finally, we can calculate the VaR at our confidence interval

var_1d1 = initial_investment - cutoff1

var_1d1

#output






# Calculate n Day VaR

var_array = []

num_days = int(30)
print("Total Portfolio Balance: " + "{:.2f}".format(dollars))
for x in range(1, num_days+1):    

    var_array.append(np.round(var_1d1 * np.sqrt(x),2))

    print(str(x) + " day VaR @ 95% confidence: " + str(np.round(var_1d1 * np.sqrt(x),2)))

print("")
print("Share this tool and mention @Braun_Capital on Twitter")
print("Also, check out our website brauncapital.net")

# Build plot

plt.xlabel("Day #")

plt.ylabel("Max portfolio loss (USD)")

plt.title("Max portfolio loss (VaR) over 30-day period")

plt.plot(var_array, "r")
plt.show()