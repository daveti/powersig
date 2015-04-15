#!/usr/bin/python

# PowerSig Anormaly Detector
# CPU/CPU or CPU/MEM anormaly detection
# Usuage: ./detector.py psig.csv psig_new.csv
# Reference:
# http://scikit-learn.org/stable/auto_examples/svm/plot_oneclass.html#example-svm-plot-oneclass-py
# Apr 15, 2015
# root@davejingtian.org
# http://davejingtian.org

import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager
from sklearn import svm

# Make sure there are 3 arguments
if len(sys.argv) != 3:
	print("Error: invalid number of arguments")
	sys.exit()

# Read the training data
with open(sys.argv[1]) as f:
	data = f.read()

data = data.split('\n')
data = filter(None, data)

# Convert to numpy array
X_train = []
for d in data:
	tmp = []
	tmp.append(float(d.split(',')[0]))
	tmp.append(float(d.split(',')[1]))
	X_train.append(tmp[:])
X_train = np.asarray(X_train)

# Read the testing data
with open(sys.argv[2]) as f:
	data_new = f.read()

data_new = data_new.split('\n')
data_new = filter(None, data_new)

# Convert to numpy array
X_test = []
for d in data_new:
	tmp = []
	tmp.append(float(d.split(',')[0]))
	tmp.append(float(d.split(',')[1]))
	X_test.append(tmp[:])
X_test = np.asarray(X_test)

# SVM with one class
# fit the model
clf = svm.OneClassSVM(nu=0.1, kernel="rbf", gamma=0.1)
clf.fit(X_train)
y_pred_train = clf.predict(X_train)
y_pred_test = clf.predict(X_test)
n_error_train = y_pred_train[y_pred_train == -1].size
n_error_test = y_pred_test[y_pred_test == -1].size

# plot the line, the points, and the nearest vectors to the plane
xx, yy = np.meshgrid(np.linspace(0, 10, 100), np.linspace(0, 10, 100))
Z = clf.decision_function(np.c_[xx.ravel(), yy.ravel()])
Z = Z.reshape(xx.shape)

plt.title("Anormaly Detection")
plt.contourf(xx, yy, Z, levels=np.linspace(Z.min(), 0, 7), cmap=plt.cm.Blues_r)
a = plt.contour(xx, yy, Z, levels=[0], linewidths=2, colors='red')
plt.contourf(xx, yy, Z, levels=[0, Z.max()], colors='orange')

b1 = plt.scatter(X_train[:, 0], X_train[:, 1], c='green')
b2 = plt.scatter(X_test[:, 0], X_test[:, 1], c='yellow')

plt.axis('tight')
plt.xlim((0, 10))
plt.ylim((0, 10))

plt.legend([a.collections[0], b1, b2],
		["learned frontier", "training observations",
		 "new abnormal observations"],
		loc="upper left",
		prop=matplotlib.font_manager.FontProperties(size=11))
plt.xlabel(
	"anormaly[train]: %d/1000 ; anormaly[new]: %d/4"
	% (n_error_train, n_error_test))
plt.show()
