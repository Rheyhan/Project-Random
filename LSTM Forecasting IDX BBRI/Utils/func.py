import matplotlib.pyplot as plt
import numpy as np
from tensorflow import keras


def plottraintest(train, test):
    fig =plt.figure(figsize=(12,8))
    ax=fig.add_subplot(2,2,1)
    ax.plot(train, c="blue")
    ax.set_title("train")
    ax=fig.add_subplot(2,2,2)
    ax.plot(test, c="orange")
    ax.set_title("test")
    ax=fig.add_subplot(2,1,2)
    temp=np.array(list(map(list, zip(train.flatten(), range(1,len(train)+1)))))
    ax.plot(temp[:,1], temp[:,0], c="blue", label="train")
    temp=np.array(list(map(list, zip(test.flatten(), range(len(train)+1,len(train)+len(test)+1)))))
    temp=np.concatenate(([[train.flatten()[-1],len(train)]], temp),axis=0)
    ax.plot(temp[:,1], temp[:,0], c="orange", label="test")
    ax.legend(loc="lower right")
    ax.set_title("Train & test")
    
    
def lag(dataset, t=1):
    '''Default t=1'''
    dataX, dataY = [], []
    for i in range(len(dataset)-t-1):
        a = dataset[i:(i+t), 0]
        dataX.append(a)
        dataY.append(dataset[i + t, 0])
    return np.array(dataX), np.array(dataY)

def plot_predicted(df, trainPredict, testPredict, t):
    # shift train predictions for plotting
    trainPredictPlot = np.empty_like(df)
    trainPredictPlot[:, :] = np.nan
    trainPredictPlot[t:len(trainPredict)+t, :] = trainPredict

    # shift test predictions for plotting
    testPredictPlot = np.empty_like(df)
    testPredictPlot[:, :] = np.nan
    testPredictPlot[len(trainPredict)+(t*2)+1:len(df)-1, :] = testPredict

    # plot baseline and predictions
    fig=plt.figure(figsize=(12,8))
    ax=fig.add_subplot(1,1,1)
    ax.grid("on", alpha=0.4)
    ax.plot(df, alpha=0.8, label="actual")
    ax.plot(trainPredictPlot, label="predicted train")
    ax.plot(testPredictPlot, label ="predicted test")
    ax.legend(loc="lower right")
    ax.set_ylabel("Open (IDR)")
    ax.set_xlabel("period")
    
    
def trainvaltestplot(train, val, test):
    fig =plt.figure(figsize=(15,8))
    ax=fig.add_subplot(2,3,1)
    ax.plot(train, c="blue")
    ax.set_title("train")
    ax=fig.add_subplot(2,3,2)
    
    ax.plot(validation, c="red")
    ax.set_title("validation")
    ax=fig.add_subplot(2,3,3)
    ax.plot(test, c="orange")
    ax.set_title("test")

    ax=fig.add_subplot(2,1,2)
    temp=np.array(list(map(list, zip(train.flatten(), range(1,len(train)+1)))))
    ax.plot(temp[:,1], temp[:,0], c="blue", label="train")

    temp=np.array(list(map(list, zip(validation.flatten(), range(len(train)+1,len(train)+len(validation)+1)))))
    temp=np.concatenate(([[train.flatten()[-1],len(train)]], temp),axis=0)
    ax.plot(temp[:,1], temp[:,0], c="red", label="validation")

    temp1=np.array(list(map(list, zip(test.flatten(), range(int(temp[-1][-1])+1, len(df)+1)))))
    temp=np.concatenate(([temp[-1]], temp1),axis=0)
    ax.plot(temp[:,1], temp[:,0], c="orange", label="test")


    ax.legend(loc="lower right")
    ax.set_title("Train, validation, & test")
    


def forecast(predictedday, model, scaler, testdata, t):
    forecasted=[]
    theinput=testdata[-t:]

    firstinput = theinput.reshape((1, t,1))
    temppredicted = model.predict(firstinput, verbose=0)
    theinput=np.concatenate((theinput, temppredicted), axis=0)
    forecasted.append(scaler.inverse_transform(temppredicted.reshape(1,-1))[0])
    
    for i in range(1,predictedday):
        theinput=theinput[1:].flatten().reshape(1,t,1)
        temppredicted=model.predict(theinput, verbose=0)
        theinput=np.concatenate((theinput.reshape(-1,1), temppredicted), axis=0)
        forecasted.append(scaler.inverse_transform(temppredicted.reshape(1,-1))[0])
        
    return np.array(forecasted)