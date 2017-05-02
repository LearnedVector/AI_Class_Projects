import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle, resample
from miniflow import *

df = pd.read_csv('./airlines.csv')

Features = df.drop(['Code', 'Name', 'Month', 'Year', 'Month Name', 'Label'], axis=1)
Labels = df[['Code']]

Labels = pd.get_dummies(Labels)

X_train, X_valid, y_train, y_valid = train_test_split(Features, Labels, test_size=0.05)

X_train, X_test, y_train, y_test = train_test_split(X_train, y_train, test_size=0.05)

X_train = np.array(X_train)
y_train = np.array(y_train)

X_valid = np.array(X_valid)
y_valid = np.array(y_valid)

X_test = np.array(X_test)
y_test = np.array(y_test)

# encode y code into numerical values 0 - 28
new_y_train = []
new_y_valid = []
new_y_test = []

for col, row in enumerate(y_train):
    for i, j in enumerate(row):
        if j == 1:
            new_y_train.append(i)

for col, row in enumerate(y_valid):
    for i, j in enumerate(row):
        if j == 1:
            new_y_valid.append(i)

for col, row in enumerate(y_test):
    for i, j in enumerate(row):
        if j == 1:
            new_y_test.append(i)

y_train = np.array(new_y_train)
y_valid = np.array(new_y_valid)
y_test = np.array(new_y_test)

# normalize the data
X_train = (X_train - np.mean(X_train, axis=0)) / np.std(X_train, axis=0)
X_valid = (X_valid - np.mean(X_valid, axis=0)) / np.std(X_valid, axis=0)
X_test = (X_test - np.mean(X_test, axis=0)) / np.std(X_test, axis=0)

# shuffle data
X_train, y_train = shuffle(X_train, y_train)

# set up Weight and Biases
n_features = X_train.shape[1]
n_hidden = 10
W1_ = np.random.randn(n_features, n_hidden)
b1_ = np.zeros(n_hidden)
W2_ = np.random.randn(n_hidden, 1)
b2_ = np.zeros(1)

# Neural Network
X, y = Input('X'), Input('y')
W1, b1 = Input('W1'), Input('b1')
W2, b2 = Input('W2'), Input('b2')

l1 = Linear(X, W1, b1, 'l1')
s1 = Sigmoid(l1)
l2 = Linear(s1, W2, b2, 'l2')
MSE(y, l2)

feed_dict = {
    X: X_train,
    y: y_train,
    W1: W1_,
    b1: b1_,
    W2: W2_,
    b2: b2_
}

epochs = 300

# total number of examples
m = X_train.shape[0]
batch_size = 50
steps_per_epoch = m // batch_size

graph = topological_sort(feed_dict)
trainables = [W1, b1, W2, b2]

print("Total number of examples = {}".format(m))


# evaluate the test set
def evaluate(trainables, X_, y_):
    # Neural Network
    X, y = Input('X_valid'), Input('y_valid')
    W1, b1 = Input('W1_valid'), Input('b1_valid')
    W2, b2 = Input('W2_valid'), Input('b2_valid')

    l1 = Linear(X, W1, b1, 'l1_valid')
    s1 = Sigmoid(l1, 'sigmoid_valid')
    l2 = Linear(s1, W2, b2, 'l2_valid')
    MSE(y, l2, 'MSE_valid')

    test_feed_dict = {
        X: X_,
        y: y_,
        W1: trainables[0].value,
        b1: trainables[1].value,
        W2: trainables[2].value,
        b2: trainables[3].value
    }

    graph = topological_sort(test_feed_dict)

    for n in graph:
        n.forward()

    y = graph[-1].inbound_nodes[0].value.reshape(-1, 1)
    a = graph[-1].inbound_nodes[1].value.reshape(-1, 1)

    correct = []

    for i, j in enumerate(a):
        if 0 <= abs(y[i] - j) <= 1:
            correct.append(1)

    return sum(correct)/len(y)


# Step 4
for i in range(epochs):
    loss = 0
    for j in range(steps_per_epoch):
        # Step 1
        # Randomly sample a batch of examples
        X_batch, y_batch = resample(X_train, y_train, n_samples=batch_size)
        # Reset value of X and y Inputs
        X.value = X_batch
        y.value = y_batch

        # Step 2
        forward_and_backward(graph)

        # Step 3
        sgd_update(trainables , learning_rate=1e-2)

        loss += graph[-1].value

    # Evaluate model from test data
    print("Epoch: {}, Loss: {:.3f}, Validation Accuracy: {:.3f}".format(i+1, loss/steps_per_epoch, evaluate(trainables, X_valid, y_valid)))

print("Test Accuracy: ", evaluate(trainables, X_test, y_test))
