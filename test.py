from dataset import vals as data
from pandas import DataFrame as DataFrame
import matplotlib.pyplot as plt
import numpy as np
df=DataFrame(data, columns=['Name','School','X-Coordinate','Y-Coordinate','Season Best','SB Date'])
x=[]
y=[]
for val in df['X-Coordinate']:
    x.append(val)
for val in df['Y-Coordinate']:
    y.append(val)

X={'x':x,'y':y}
df_vals=DataFrame(X,columns=['x','y'])

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

wcss=[]
for i in range(1,11):
    kmeans=KMeans(n_clusters=i,init='k-means++',max_iter=300,n_init=10,random_state=0,copy_x=True)
    kmeans.fit(df_vals)
    wcss.append(kmeans.inertia_)
plt.plot(range(1,11), wcss)
plt.title('Elbow Method')
plt.xlabel('Number of clusters')
plt.ylabel('WCSS')
plt.show()
