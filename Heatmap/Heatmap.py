# -*- coding: utf-8 -*-
"""
Created on Thu Apr  5 07:13:11 2018

@author: Pritish
"""

'''
HEAT MAP
'''

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import csv
import seaborn as sns

#importing dataset and cleaning
hmData=pd.read_csv('cleaned_final.csv', sep = ',', encoding = 'latin-1')   
List1 = ['ON' , 'BC' , 'AB' , 'QC' , 'NB', 'SK', 'MB', 'NL', 'NT', 'NS', 'PE', 'YT', 'NU']
hmData['PLACE'] = hmData['PLACE'].str.extract("(" + "|".join(List1) +")", expand=False)
hmData=hmData.dropna(subset = ['PLACE'])

#Giving each occurence of disaster a count of 1 ( 1 row = 1 count)
hmData=hmData[['EVENT GROUP','PLACE']].copy()
hmData['Occurence']=1
grp = hmData.groupby(['PLACE', 'EVENT GROUP'])
df = grp.apply(lambda x : x.Occurence.sum())
df=pd.DataFrame(df, columns = ['Occurence']).reset_index()

#Creates the dataframe to be fed into seaborns library to create heatmap
df=df.pivot(index = 'PLACE', columns = 'EVENT GROUP', values = 'Occurence')
dfinal = df.fillna(0)

#Visualizing heatmap
plt.close('all')
sns.set(font_scale=0.7)
plt.figure(figsize=(15,7))
plt.figure(1)
plt.title("Amount of fatalities caused by event subgroup for each province")
sns.heatmap(dfinal, cmap='RdYlGn_r', xticklabels=1, yticklabels=1, vmax=120, vmin=0)
plt.subplots_adjust(left=0.2, bottom=0.25, top=0.90) 
plt.xticks(rotation=90)
plt.yticks(rotation=0)

#Visualizing clustered map
plt.close('all')
sns.set(font_scale=0.90)
cg=sns.clustermap(dfinal, cmap='RdYlGn_r', xticklabels=1, yticklabels=1, method="ward",vmax=120)
plt.subplots_adjust(bottom=0.21, top=0.98, right=0.80) 