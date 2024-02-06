import numpy as np

def adder(data, times):
    for i in range(1, times + 1):
        z = np.zeros((len(data), 1), dtype=float)
        data = np.append(data, z, axis=1)
    return data

def deleter(Data, index, times):
    for i in range(1, times + 1):
        Data = np.delete(Data, index, axis=1)
    return Data

def jump(Data, jump):
    return Data[jump:, ]    
    
    
def ma(Data, lookback, close, where): 
    Data = adder(Data, 1)
    for i in range(len(Data)):
        try:
            Data[i, where] = (Data[i - lookback + 1:i + 1, close].mean())
        except IndexError:
            pass
    return Data
    
def ema(Data, alpha, lookback, what, where):
    alpha = alpha / (lookback + 1.0)
    beta  = 1 - alpha
    Data = ma(Data, lookback, what, where)
    Data[lookback + 1, where] = (Data[lookback + 1, what] * alpha) + (Data[lookback, where] * beta)
    for i in range(lookback + 2, len(Data)):
        try:
            Data[i, where] = (Data[i, what] * alpha) + (Data[i - 1, where] * beta)
        except IndexError:
            pass
    return Data 
def rsi(Data, lookback, close, where, width = 1, genre = 'Smoothed'):

    # Adding a few columns
    Data = adder(Data, 5)

    # Calculating Differences
    for i in range(len(Data)):

        Data[i, where] = Data[i, close] - Data[i - width, close]

    # Calculating the Up and Down absolute values
    for i in range(len(Data)):

        if Data[i, where] > 0:

            Data[i, where + 1] = Data[i, where]

        elif Data[i, where] < 0:

            Data[i, where + 2] = abs(Data[i, where])

    # Calculating the Smoothed Moving Average on Up and Down absolute values    
    if genre == 'Smoothed':
        lookback = (lookback * 2) - 1 # From exponential to smoothed
        Data = ema(Data, 2, lookback, where + 1, where + 3)
        Data = ema(Data, 2, lookback, where + 2, where + 4)

    if genre == 'Simple':
        Data = ma(Data, lookback, where + 1, where + 3)
        Data = ma(Data, lookback, where + 2, where + 4)

    # Calculating the Relative Strength
    Data[:, where + 5] = Data[:, where + 3] / Data[:, where + 4]

    # Calculate the Relative Strength Index
    Data[:, where + 6] = (100 - (100 / (1 + Data[:, where + 5])))

    # Cleaning
    Data = deleter(Data, where, 6)
    Data = jump(Data, lookback)

    return Data