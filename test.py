from dataset import vals as data
import pandas as pd
import matplotlib.pyplot as plt
df=pd.DataFrame(data, columns=['Name','School','X-Coordinate','Y-Coordinate','Season Best','SB Date'])
X=[[],[]]
for val in df['X-Coordinate']:
    X[0].append(val)
for val in df['Y-Coordinate']:
    X[1].append(val)

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

wcss=[]
for i in range(1,11):
    kmeans=KMeans(n_clusters=i,init='k-means++',max_iter=300,n_init=10,random_state=0,copy_x=True)
    kmeans.fit(X)
    wcss.append(kmeans.inertia_)
plt.plot(range(1,11), wcss)
plt.title('Elbow Method')
plt.xlabel('Number of clusters')
plt.ylabel('WCSS')
plt.show()
