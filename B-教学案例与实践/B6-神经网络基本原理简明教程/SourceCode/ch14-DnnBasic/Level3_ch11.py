# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for full license information.

import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import math

from MiniFramework.NeuralNet40 import *
from MiniFramework.ActivatorLayer import *
from MiniFramework.ClassificationLayer import *
from MiniFramework.DataReader20 import *

train_file = "../../Data/ch11.train.npz"
test_file = "../../Data/ch11.test.npz"

def LoadData():
    dr = DataReader20(train_file, test_file)
    dr.ReadData()
    dr.NormalizeX()
    dr.NormalizeY(NetType.MultipleClassifier, base=1)
    dr.Shuffle()
    dr.GenerateValidationSet()
    return dr

def ShowData(dataReader):
    for i in range(dataReader.XTrain.shape[0]):
        if dataReader.YTrain[i,0] == 1:
            plt.plot(dataReader.XTrain[i,0], dataReader.XTrain[i,1], '^', c='g')
        elif dataReader.YTrain[i,1] == 1:
            plt.plot(dataReader.XTrain[i,0], dataReader.XTrain[i,1], 'x', c='r')
        elif dataReader.YTrain[i,2] == 1:
            plt.plot(dataReader.XTrain[i,0], dataReader.XTrain[i,1], '.', c='b')
        # end if
    # end for
    plt.xlabel("x1")
    plt.ylabel("x2")
    plt.show()

def ShowResult(net, title):
    fig = plt.figure(figsize=(5,5))
    count = 50
    x = np.linspace(0,1,count)
    y = np.linspace(0,1,count)
    X,Y = np.meshgrid(x,y)
    z = net.inference(np.c_[X.ravel(),Y.ravel()])
    Z = np.max(z,axis=1).reshape(X.shape)
    plt.contourf(X,Y,Z)

def model_relu(num_input, num_hidden, num_output, hp):
    net = NeuralNet40(hp, "chinabank_relu")

    fc1 = FcLayer(num_input, num_hidden, hp)
    net.add_layer(fc1, "fc1")
    r1 = ActivatorLayer(Relu())
    net.add_layer(r1, "Relu1")

    fc2 = FcLayer(num_hidden, num_output, hp)
    net.add_layer(fc2, "fc2")
    softmax1 = ClassificationLayer(Softmax())
    net.add_layer(softmax1, "softmax1")

    net.train(dataReader, checkpoint=50, need_test=True)
    net.ShowLossHistory("epoch")
    
    ShowResult(net, hp.toString())
    ShowData(dataReader)

def model_sigmoid(num_input, num_hidden, num_output, hp):
    net = NeuralNet40(hp, "chinabank_sigmoid")

    fc1 = FcLayer(num_input, num_hidden, hp)
    net.add_layer(fc1, "fc1")
    s1 = ActivatorLayer(Sigmoid())
    net.add_layer(s1, "Sigmoid1")

    fc2 = FcLayer(num_hidden, num_output, hp)
    net.add_layer(fc2, "fc2")
    softmax1 = ClassificationLayer(Softmax())
    net.add_layer(softmax1, "softmax1")

    net.train(dataReader, checkpoint=50, need_test=True)
    net.ShowLossHistory("epoch")
    
    ShowResult(net, hp.toString())
    ShowData(dataReader)


if __name__ == '__main__':
    dataReader = LoadData()
    num_input = dataReader.num_feature
    num_hidden = 8
    num_output = 3

    max_epoch = 5000
    batch_size = 10
    learning_rate = 0.1
    eps = 1e-3

    hp = HyperParameters40(
        learning_rate, max_epoch, batch_size, eps,
        net_type=NetType.MultipleClassifier,
        init_method=InitialMethod.Xavier)
  
    model_relu(num_input, num_hidden, num_output, hp)
    model_sigmoid(num_input, num_hidden, num_output, hp)
