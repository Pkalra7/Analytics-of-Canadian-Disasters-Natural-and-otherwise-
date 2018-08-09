# -*- coding: utf-8 -*-
"""
Created on Thu Apr  5 03:43:02 2018

@author: Pritish
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Importing Dataset
allData=pd.read_csv('cleaned_final.csv', sep = ',', encoding = 'latin-1')
allData['year'] = pd.DatetimeIndex(allData['EVENT START DATE']).year
allData['month'] = pd.DatetimeIndex(allData['EVENT START DATE']).month

X = allData.iloc[:,[1 ,22]]
X['10+Occurences']=1
grp = X.groupby(['year', 'EVENT GROUP'])
X = grp.apply(lambda x : x['10+Occurences'].sum())
X=pd.DataFrame(X, columns = ['10+Occurences']).reset_index()
X.loc[X['10+Occurences'] < 10, ['10+Occurences']]=0
X.loc[X['10+Occurences'] >= 10, ['10+Occurences']]=1
X.loc[X['EVENT GROUP'] == 'Conflict', ['EVENT GROUP']] = 1
X.loc[X['EVENT GROUP'] == 'Technology', ['EVENT GROUP']] = 2
X.loc[X['EVENT GROUP'] == 'Natural', ['EVENT GROUP']] = 3

xx = X.iloc[:, [0,1]]
yy = X.iloc[:, 2]


# Splitting the dataset into training set and test set
from sklearn.cross_validation import train_test_split
X_train, X_test, y_train, y_test = train_test_split(xx, yy, test_size = 0.2, random_state = 0)


#Applying feature scaling
from sklearn.preprocessing import StandardScaler
sc_X = StandardScaler()
X_train = sc_X.fit_transform(X_train)
X_test = sc_X.transform(X_test)


#Fitting Logistic Regression to the training set
from sklearn.linear_model import LogisticRegression
classifier = LogisticRegression(random_state=0)
classifier.fit(X_train, y_train)
y_pred = classifier.predict(X_test)


# Making the confusion matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)


#Visualizing the training set results
plt.close('all')
from matplotlib.colors import ListedColormap
X_set, y_set = X_train, y_train
X1, X2 = np.meshgrid(np.arange(start = X_set[:, 0].min() - 1, stop = X_set[:, 0].max() + 1, step = 0.01),
                     np.arange(start = X_set[:, 1].min() - 1, stop = X_set[:, 1].max() + 1, step = 0.01))
plt.contourf(X1, X2, classifier.predict(np.array([X1.ravel(), X2.ravel()]).T).reshape(X1.shape),
             alpha = 0.75, cmap = ListedColormap(('red', 'green')))
plt.xlim(X1.min(), X1.max())
plt.ylim(X2.min(), X2.max())
for i, j in enumerate(np.unique(y_set)):
    plt.scatter(X_set[y_set == j, 0], X_set[y_set == j, 1],
                c = ListedColormap(('red', 'green'))(i), label = j)
plt.title('Logistic Regression (Training set)')
plt.xlabel('Year')
plt.ylabel('EVENT GROUP')
plt.legend()
plt.show()


#Visualizing the test set results
plt.close('all')
from matplotlib.colors import ListedColormap
X_set, y_set = X_test, y_test
X1, X2 = np.meshgrid(np.arange(start = X_set[:, 0].min() - 1, stop = X_set[:, 0].max() + 1, step = 0.01),
                     np.arange(start = X_set[:, 1].min() - 1, stop = X_set[:, 1].max() + 1, step = 0.01))
plt.contourf(X1, X2, classifier.predict(np.array([X1.ravel(), X2.ravel()]).T).reshape(X1.shape),
             alpha = 0.75, cmap = ListedColormap(('red', 'green')))
plt.xlim(X1.min(), X1.max())
plt.ylim(X2.min(), X2.max())
for i, j in enumerate(np.unique(y_set)):
    plt.scatter(X_set[y_set == j, 0], X_set[y_set == j, 1],
                c = ListedColormap(('red', 'green'))(i), label = j)
plt.title('Logistic Regression (Test set)')
plt.xlabel('Year')
plt.ylabel('EVENT GROUP')
plt.legend()
plt.show() 