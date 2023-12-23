import numpy as np









def givelagvariable(dataset, t):
        '''Default t=1'''
        dataX, dataY = [], []
        for i in range(len(dataset)-t-1):
            a = dataset[i:(i+t), 0]
            dataX.append(a)
            dataY.append(dataset[i + t, 0])
        return np.array(dataX), np.array(dataY)