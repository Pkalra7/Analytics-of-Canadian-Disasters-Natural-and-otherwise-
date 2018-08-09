# -*- coding: utf-8 -*-
"""
Created on Sun Apr  1 16:37:40 2018

@author: Pritish
"""
#%clear
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import csv
import seaborn as sns

'''
K-MEANS CLUSTERING
'''

#importing dataset and cleaning data to build accurate model
allData=pd.read_csv('cleaned_final.csv', sep = ',', encoding = 'latin-1')
List1 = ['ON' , 'BC' , 'AB' , 'QC' , 'NB', 'SK', 'MB', 'NL', 'NT', 'NS', 'PE', 'YT', 'NU']
allData['PLACE'] = allData['PLACE'].str.extract("(" + "|".join(List1) +")", expand=False)
allData=allData.dropna(subset = ['PLACE'])
allData=allData.fillna(0)
allData['year'] = pd.DatetimeIndex(allData['EVENT START DATE']).year
allData['Evacuation%']=(allData.EVACUATED - (allData['INJURED / INFECTED'] + allData.FATALITIES))/100
X=allData.iloc[:, [22,23]]
X=X.loc[(X['Evacuation%']!=0)]
X=X[X['Evacuation%'] < 150] 

dataset=X.iloc[:,[0,1]].values

import scipy.cluster.hierarchy as sch
dendogram = sch.dendrogram(sch.linkage(dataset, method = 'ward'))
plt.title('Dendogram')
plt.xlabel('Customers')
plt.ylabel('Eucleadian Distances')
plt.show()

#Fitting Hierarchichal clustering to the mall dataset
from sklearn.cluster import AgglomerativeClustering
hc = AgglomerativeClustering(n_clusters = 2, affinity = 'euclidean', linkage = 'ward')
y_hc = hc.fit_predict(dataset)

#Visualizing the clusters
plt.scatter(dataset[y_hc == 0, 0], dataset[y_hc == 0,1], s = 100, c = 'red', label = 'Carefull')
plt.scatter(dataset[y_hc == 1, 0], dataset[y_hc == 1,1], s = 100, c = 'blue', label = 'Standard')
plt.title('Clusters of Clients')
plt.xlabel('year')
plt.ylabel('evac')
plt.legend()
plt.show







