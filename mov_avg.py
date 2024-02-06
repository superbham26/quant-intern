import numpy as np

class AllCodes:
     
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
        Data = AllCodes.adder(Data, 1)
        for i in range(len(Data)):
            try:
                Data[i, where] = (Data[i - lookback + 1:i + 1, close].mean())
            except IndexError:
                pass
        return Data
    
    
    def ema(Data, alpha, lookback, what, where):
        alpha = alpha / (lookback + 1.0)
        beta  = 1 - alpha
        Data = AllCodes.ma(Data, lookback, what, where)
        Data[lookback + 1, where] = (Data[lookback + 1, what] * alpha) + (Data[lookback, where] * beta)
        for i in range(lookback + 2, len(Data)):
            try:
                Data[i, where] = (Data[i, what] * alpha) + (Data[i - 1, where] * beta)
            except IndexError:
                pass
        return Data 
    
    
    def lwma(Data, lookback, what):
        weighted = []
        for i in range(len(Data)):
            try:
                total = np.arange(1, lookback + 1, 1)                
                matrix = Data[i - lookback + 1: i + 1, what:what + 1]
                matrix = np.ndarray.flatten(matrix)
                matrix = total * matrix
                wma = (matrix.sum()) / (total.sum())
                weighted = np.append(weighted, wma)
            except ValueError:
                pass
        Data = Data[lookback - 1:, ]
        weighted = np.reshape(weighted, (-1, 1)) 
        Data = np.concatenate((Data, weighted), axis=1)   
        return Data
    
    
    def kama(Data, what, where, lookback):
        Data = AllCodes.adder(Data, 2)
        for i in range(len(Data)):
            Data[i, where] = abs(Data[i, what] - Data[i - 1, what])
        Data[0, where] = 0
        for i in range(len(Data)):
            Data[i, where + 1] = (Data[i - lookback + 1:i + 1, where].sum())   
        for i in range(len(Data)):
            Data[i, where + 2] = abs(Data[i, what] - Data[i - lookback, what])
        Data = Data[lookback + 1:, ]
        Data[:, where + 3] = Data[:, where + 2] / Data[:, where + 1]
        for i in range(len(Data)):
            Data[i, where + 4] = np.square(Data[i, where + 3] * 0.6666666666666666667)
        for i in range(len(Data)):
            Data[i, where + 5] = Data[i - 1, where + 5] + (Data[i, where + 4] * (Data[i, what] - Data[i - 1, where + 5]))
            Data[11, where + 5] = 0
        Data = AllCodes.deleter(Data, where, 5)
        Data = AllCodes.jump(Data, lookback * 2)
        return Data
    
    
    def hull_moving_average(Data, what, lookback, where):
        Data = AllCodes.lwma(Data, lookback, what)
        second_lookback = round((lookback / 2), 1)
        second_lookback = int(second_lookback) 
        Data = AllCodes.lwma(Data, second_lookback, what)
        Data = AllCodes.adder(Data, 1)
        Data[:, where + 2] = ((2 * Data[:, where + 1]) - Data[:, where])
        third_lookback = round(np.sqrt(lookback), 1)
        third_lookback = int(third_lookback) 
        Data = AllCodes.lwma(Data, third_lookback, where + 2)
        Data = AllCodes.deleter(Data, where, 3)
        return Data
    
    def signal(Data, close, ma_column, buy_col, sell_col):
        Data = AllCodes.adder(Data, 2)
        for i in range(len(Data)):
            if Data[i, close] > Data[i, ma_column] and Data[i - 1, close] < Data[i - 1, ma_column]:
                Data[i, buy_col] = 1
            elif Data[i, close] < Data[i, ma_column] and Data[i - 1, close] > Data[i - 1, ma_column]:
                Data[i, sell_col] = -1
        return Data
    