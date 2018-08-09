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


#finding clusters with elbow method
from sklearn.cluster import KMeans
wcss = []
for i in range(1,11):
    kmeans = KMeans(n_clusters = i, init = 'k-means++', max_iter = 300, n_init=10, random_state = 0)
    kmeans.fit(dataset)
    wcss.append(kmeans.inertia_)
    
plt.plot(range(1,11), wcss)
plt.title('The Elbow Method')
plt.xlabel("Number of Clusters") 
plt.ylabel('WCSS')
plt.show


#applying elbow method result to out model

kmeans = KMeans(n_clusters = 4, init = 'k-means++', max_iter = 300, n_init = 10, random_state = 5)
y_kmeans= kmeans.fit_predict(dataset)


#visualizing results
plt.close('all')
plt.scatter(dataset[y_kmeans == 0, 0], dataset[y_kmeans == 0, 1], s = 100, c = 'red', label = 'Medium Success')
plt.scatter(dataset[y_kmeans == 1, 0], dataset[y_kmeans == 1, 1], s = 100, c = 'blue', label = 'Outliars')
plt.scatter(dataset[y_kmeans == 2, 0], dataset[y_kmeans == 2, 1], s = 100, c = 'green', label = 'Tragic')
plt.scatter(dataset[y_kmeans == 3, 0], dataset[y_kmeans == 3, 1], s = 100, c = 'cyan', label = 'Decent success')
plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], s = 200, c = 'yellow', label = 'Centroids')
plt.title('Clusters of Evacuation efforts')
plt.xlabel('Successfully Evacuation %')
plt.ylabel('Year')
plt.legend()
plt.show






