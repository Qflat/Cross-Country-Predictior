import time
start_time=time.time()
import requests
import urllib.request
from bs4 import BeautifulSoup as bs
from tkinter import *
import datetime
from datetime import datetime as dt
import pandas as pd
import numpy as np
from itertools import permutations
import warnings
warnings.filterwarnings("ignore")

section_times=[]

def section_time(phrase):
    import time
    global start_time
    global section_times
    section_final_time=time.time()
    t=float(np.round(section_final_time-start_time,2))
    section_final_time=time.time()
    print(f'Section took {t} seconds to run')
    start_time=section_final_time
    section_times.append(t)
    print(phrase)

class Webpage:
    def __init__(self,master):
        self.master=master
        master.title('Web Results')
        master.label=Label(text='Please insert the hypothetical meet list you\'d like to evaluate: ')
        master.label.grid(row=0)
        master.url_box=Entry(master)
        master.url_box.grid(row=1)
        master.button=Button(master,text='Evaluate',command=self.get_url)
        master.button.grid(row=2)

    def get_url(self):
        global url
        url=self.master.url_box.get()
        self.master.destroy()

# Get URL of Seasons Best From Athletic.net
start=Tk()
evaluate=Webpage(start)
start.mainloop()

# Gather information from variable url
def lines(url,search):
    response=requests.get(url)
    content=bs(response.text,"html.parser")
    val=content.findAll(search)
    return val

def texts(line):
    splitted=line.split('>')
    val=splitted[1]
    new_val=val.split('<')
    final_val=new_val[0]
    return final_val

def timed(result):
    splitted=result.split('>')
    val=splitted[4]
    s=val.split('<')
    time=s[0]
    nums=time.split(':')
    try:
        minutes=float(str((nums[0])))
        seconds=float(str((nums[1])))
        while minutes>0.0:
            minutes-=1.0
            seconds+=60.0
        return seconds
    except ValueError:
        # No Final Result
        return 9999

def new_user(name,school,sb,sb_date):
    var_name=name.lower()
    disqualified_characters=[" ","'",".","(",")","-"]
    for char in disqualified_characters:
        var_name=var_name.replace(char,"_")
    f=open('dataset.py','a')
    f.write(var_name+'=Runner("'+name+'","'+school+'",'+str(sb)+',"'+sb_date+'")\n')
    f.close()

# Defining a few more variables that'll be important later
today=dt.today()
year=str(today.year)
try:
    a=lines(url,'a')
except NameError:
    print('No URL given. Closing Program.')
    exit(0)
line_count=0
f=open('dataset.py','w')
f.write('vals=[]\n\
class Runner:\n\
    def __init__(self,name,school,season_best,sb_date):\n\
        self.name=name\n\
        self.school=school\n\
        self.season_best=season_best\n\
        self.sb_date=sb_date\n\
        self.days=self.day(self.sb_date)\n\
        self.best_time=self.time(self.season_best)\n\
        self.x=season_best\n\
        self.y=self.days\n\
        self.values=(self.name,self.school,self.x,self.y,self.best_time,self.sb_date)\n\
        global vals\n\
        vals.append(self.values)\n\
\n\
    def day(self,date):\n\
        split=date.split(' ')\n\
        days=0\n\
        if split[0]=="Sep":\n\
            days+=31\n\
        elif split[0]=="Oct":\n\
            days+=61\n\
        days+=int(split[1])\n\
        return days\n\
\n\
    def time(self,t):\n\
        minutes=0\n\
        while t>60.0:\n\
            t-=60.0\n\
            minutes+=1\n\
        return str(minutes)+":"+str(round(t,1))\n\n')
f.close()

def month(val):
    if val=='Aug':
        return 8
    elif val=='Sep':
        return 9
    elif val=='Oct':
        return 10
    elif val=='Nov':
        return 11
    elif val=='Dec':
        return 12

# Run through each athlete to gather Data set, code sampled from 'https://github.com/julia-git/webscraping_ny_mta'
print("Please wait as we gather the athlete's information on the site...")
for line in a:
    line=str(line)
    if line_count>=58:
        # Team Information Begins on Line 58 in Hypothetical Meet Page
        if 'javascript' in line:
            # Results Completed
            break
        if 'School' in line:
            # School Name
            school=texts(line)
        elif 'Athlete' in line:
            # Athlete Name
            name=texts(line)
            athlete_page=lines("https://www.athletic.net/CrossCountry/"+line[12:37],'td')
            num=0
            dates=[]
            times=[]
            for a_line in athlete_page:
                a_line=str(a_line)
                if num>0:
                    if num<=3:
                        num+=1
                    else:
                        if 'results' in a_line:
                            pass
                        elif 'result' in a_line:
                            time=timed(a_line)
                            times.append(time)
                        elif 'width' in a_line:
                            date=texts(a_line)
                            if date!='':
                                dates.append(date)    
                elif year in a_line:
                    num+=1
            for i in range(0,len(dates)):
                split=dates[i].split(' ')
                if i!=0:
                    # Big fix here for future versions
                    date1=datetime.date(2020,month(split[0]),int(split[1]))
                    if date1<date2:
                        last_date_ran=dates[i-1]
                        break
                    else:
                        date2=date1
                else: # Big point of emphasis to work on in future versions
                    try:
                        date2=datetime.date(2020,month(split[0]),int(split[1]))
                    except IndexError:
                        pass
            for i in range(0,len(dates)):
                if dates[i]==last_date_ran:
                    season_times=times[:i+1]
                    season_best=min(season_times)
                    for j in range(0,len(season_times)):
                        if season_times[j]==season_best:
                            sb_date=dates[j]
                            break
                    break
            new_user(name,school,season_best,sb_date)
    line_count+=1

section_time("Information of athletes added. Please wait as we begin clustering the data...")

# Using DataFrame to Cluster Data
from dataset import vals as data
df=pd.DataFrame(data, columns=['Name','School','X-Coordinate','Y-Coordinate','Season Best','SB Date'])
x=[val for val in df['X-Coordinate']]
y=[val for val in df['Y-Coordinate']]
X={'x':x,'y':y}
df_vals=pd.DataFrame(X,columns=['x','y'])

from sklearn.cluster import KMeans
from kneed import KneeLocator

# Function to Determine Number of Clusters for Datasets and Subsets
# https://www.geeksforgeeks.org/elbow-method-for-optimal-value-of-k-in-kmeans/
def elbow_method(frame):
    wcss=[]
    for i in range(1,11):
        kmeans=KMeans(n_clusters=i,init='k-means++',max_iter=300,n_init=10,random_state=0,copy_x=True)
        try:
            kmeans.fit(frame)
        except ValueError:
            print('Unable to Cluster. Please refresh the program and try again.') # Point to tweak in future versions
            exit(1)
        wcss.append(kmeans.inertia_)
    k1=KneeLocator(range(1,11),wcss,curve="convex",direction="decreasing")
    return int(k1.elbow)

# https://datatofish.com/k-means-clustering-python/
num_clusters=elbow_method(df_vals)
kmeans=KMeans(n_clusters=num_clusters)
df['Cluster']=kmeans.fit_predict(df_vals)

section_time("Round One of Clustering Complete. Round Two of Clustering Underway...")

dic={}
order=[]
for i in range(0,num_clusters):
    df_num=df[df.Cluster==i]
    times=[]
    for time in df_num['Season Best']:
        times.append(time)  
    dic[times[0]]=i

for val in sorted(dic):
    order.append(dic[val])

val=0
pre_sort=[0 for i in range(0,num_clusters)]
names=[]

# Function to Remove repeating elements from arrays
# https://www.geeksforgeeks.org/python-remove-duplicates-list/
def Remove(arr):
    final_list=[]
    for val in arr:
        if val not in final_list:
            final_list.append(val)
    return final_list

sub_tables=[]
sub_orders=[]
for cluster_assignment in order:
    df_sub=df[df.Cluster==cluster_assignment]
    x=[val for val in df_sub['X-Coordinate']]
    y=[val for val in df_sub['Y-Coordinate']]
    X={'x':x,'y':y}
    df_sub_vals=pd.DataFrame(X,columns=['x','y'])
    num_sub_clusters=elbow_method(df_sub_vals)
    kmeans=KMeans(n_clusters=num_sub_clusters)
    df_sub['Sub_Cluster']=kmeans.fit_predict(df_sub_vals) # Warning Flag
    sub_tables.append(df_sub)

    sub_dic={}
    sub_order=[]
    for i in range(0,num_sub_clusters):
        df_sub_num=df_sub[df_sub.Sub_Cluster==i]
        sub_times=[]
        for time in df_sub_num['Season Best']:
            sub_times.append(time)
        sub_dic[sub_times[0]]=i

    for val in sorted(sub_dic):
        sub_order.append(sub_dic[val])
    
    sub_orders.append(sub_order)
    subset=[]
    for i in range(0,num_sub_clusters):
        df_subset=df_sub[df_sub.Sub_Cluster==i]
        subset.append(list(df_subset['Name']))
        names.append(subset)
    pre_sort[cluster_assignment]=sub_order

names=Remove(names)
section_time('Selective Sub-Clustering In Progress...')

# Some Sub-Clusters Will need to be further divided so that itertools won't break
for i in range(0,len(names)):
    for j in range(0,len(names[i])):
        if len(names[i][j])>8:
            df_prim=sub_tables[i]
            df_subs=df_prim[df_prim.Sub_Cluster==j]
            x=[val for val in df_subs['X-Coordinate']]
            y=[val for val in df_subs['Y-Coordinate']]
            X={'x':x,'y':y}
            df_subbed_vals=pd.DataFrame(X,columns=['x','y'])
            num_subbed_clusters=elbow_method(df_subbed_vals)
            kmeans=KMeans(n_clusters=num_subbed_clusters)
            df_subs['Subbed_Cluster']=kmeans.fit_predict(df_subbed_vals) # Warning Flag
            sub_named=[]
            for k in range(0,num_subbed_clusters):
                sub_names=[]
                sub_pre=df_subs[df_subs.Subbed_Cluster==k]
                for val in sub_pre['Name']:
                    sub_names.append(val)
                sub_named.append(sub_names)
            names[i][j]=sub_named

section_time('Permutating the data...')

# Running itertools to permutate each subset of data prior to scoring
full_list=[]
final_list=[]
for i in range(0,len(order)):
    for j in range(0,len(sub_orders[i])):
        val=sub_orders[i][j]
        full_list.append(names[i][val])

final_list=[]
for i in range(0,len(full_list)):
	if isinstance(full_list[i],list):
		for j in range(0,len(full_list[i])):
			if isinstance(full_list[i][j],list):
				for k in range(0,len(full_list[i][j])):
					if isinstance(full_list[i][j][k],list):
						pass
					else:
						final_list.append(full_list[i][j])
			else:
				final_list.append(full_list[i])
	else:
		final_list.append(full_list)

final_list=Remove(final_list)

perms=[]
for arr in final_list:
    try:
        perms.append(list(permutations(arr)))
    except MemoryError:
        try:
            perms.append(list(permutations(arr[:int(len(arr)/2)])))
            perms.append(list(permutations(arr[int(len(arr)/2):])))
        except MemoryError:
            perms.append(list(permutations(arr[:int(len(arr)/4)])))
            perms.append(list(permutations(arr[int(len(arr)/4):])))

section_time('Tabulating Predicted Results...')

# Preparing to Score the Permutated Data
schools=[]
scores={}
final_scores={}
official_predictions={}
school_averages={}
for val in data:
    school=val[1]
    if school not in schools:
        schools.append(school)
        scores[school]=[]
        final_scores[school]=[]
        official_predictions[school]=0
        school_averages[school]=[]

score=1
marker=0
marks=[]
for i in range(0,len(perms)):
    marks.append(len(perms[i][0]))

# Scoring the Permuatated Data
def points(order,s):
    global data
    global scores
    for name in order:
        for i in range(0,len(data)):
            if name==data[i][0]:
                scores[data[i][1]].append(s)
        s+=1

for perm in perms:
    for order in perm:
        points(order,score)
    print(f'Sub-Section #{marker+1} complete...')
    score+=marks[marker]
    marker+=1
    for school in schools:
        try:
            final_scores[school].append(sum(scores[school])/len(scores[school]))
        except ZeroDivisionError:
            final_scores[school].append(0)

for school in schools:
    for val in final_scores[school]:
        if val==0:
            final_scores[school].remove(val)
    final_scores[school]=Remove(final_scores[school])
    official_predictions[school]=sum(final_scores[school])/len(final_scores[school])

section_time('Clustering Scores...')
sort=[]
for school in schools:
    sort.append(official_predictions[school])
sort=sorted(sort)
X={'x':[],'y':[]}
for i in range(0,len(sort)):
    X['x'].append(sort[i])
    X['y'].append(i)
school_sort=pd.DataFrame(X,columns=['x','y'])
n_school_clusters=elbow_method(school_sort)
kmeans=KMeans(n_clusters=n_school_clusters)
school_sort['Cluster']=kmeans.fit_predict(school_sort)
sorted_order=[0 for i in range(0,len(schools))]
X={'x':[school for school in schools],'y':[]}
for school in schools:
    X['y'].append(official_predictions[school])
Z=[x for _,x in sorted(zip(X['y'],X['x']))]
for i in range(0,len(Z)):
    school_averages[Z[i]].append(i)
for i in range(0,len(schools)):
    school_averages[schools[i]].append(i)
for school in schools:
    avg=sum(school_averages[school])/len(school_averages[school])
    school_averages[school]=avg
Z=[x for _,x in sorted(zip(X['y'],X['x']))]

school_averages={}
for school in schools:
    school_averages[school]=[]
    for i in range(0,len(Z)):
        if Z[i]==school:
            school_averages[school].append(i)
    for i in range(0,len(schools)):
        if schools[i]==school:
            school_averages[school].append(i)
    avg=sum(school_averages[school])/len(school_averages[school])
    school_averages[school]=avg
X={'x':[school for school in schools],'y':[]}
for school in schools:
    X['y'].append(school_averages[school])
Z=[x for _,x in sorted(zip(X['y'],X['x']))]

section_time('Displaying Results...')

class Display:
    def __init__(self,master,results,times):
        self.master=master
        self.results=results
        self.times=times
        master.title('Predicted Results')
        key_label=Label(master,text='Place')
        key_label.grid(row=0,column=0)
        team_label=Label(master,text='Team')
        team_label.grid(row=0,column=1)
        
        for i in range(0,len(results)):
            place_label=Label(text=f'{i+1}. ')
            place_label.grid(row=i+1,column=0)
            team_assignment=Label(text=f'{results[i]}')
            team_assignment.grid(row=i+1,column=1)

        time_label=Label(master,text=f'Program took {self.convert(self.times)} to run')
        time_label.grid(row=len(results)+2,column=0)
            
        close_program=Button(master,text='Exit Window',command=self.close)
        close_program.grid()

    def convert(self,times):
        minutes=0.0
        seconds=0.0
        for time in times:
            seconds+=time
        while seconds>=60.0:
            minutes+=1.0
            seconds-=60.0
        string=f'{str(int(minutes))} and {str(int(round(seconds,2)))} seconds'
        return string

    def close(self):
        self.master.destroy()

final=Tk()
final_display=Display(final,Z,section_times)
final.mainloop()
