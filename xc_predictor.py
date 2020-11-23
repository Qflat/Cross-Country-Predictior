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

def check_date(val):
    months=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    for month in months:
        if month in val:
            return True
    return False

def new_user(name,school,sb,sb_date):
    var_name=name.lower()
    disqualified_characters=[" ","'",".","(",")","-"]
    for char in disqualified_characters:
        var_name=var_name.replace(char,"_")
    f=open('dataset.py','a')
    f.write(f'{var_name}=Runner("{name}","{school}",{str(sb)},"{sb_date}")\n')
    f.close()

def month(val):
    months=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    for i in range(0,len(months)):
        if months[i]==val:
            return i+1

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
f.write("vals=[]\n\
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
        if split[0]=='Sep':\n\
            days+=31\n\
        elif split[0]=='Oct':\n\
            days+=61\n\
        days+=int(split[1])\n\
        return days\n\
\n\
    def time(self,t):\n\
        minutes=0\n\
        while t>60.0:\n\
            t-=60.0\n\
            minutes+=1\n\
        if t<10:\n\
            seconds='0'+str(round(t,1))\n\
        else:\n\
            seconds=str(round(t,1))\n\
        return str(minutes)+':'+seconds\n\n")
f.close()

print("Please wait as we gather the athlete's inforamation on the site provided...")
for line in a:
    line=str(line)
    if line_count>=58:
        if 'javascript' in line:
            break
        if 'School' in line:
            school=texts(line)
        elif 'Athlete' in line:
            name=texts(line)
            athlete_page=lines(f"https://www.athletic.net/CrossCountry/{line[12:37]}",'td')
            dates=[]
            times=[]
            num=0
            for a_line in athlete_page:
                a_line=str(a_line)
                if num>0:
                    if num<=3:
                        num+=1
                    else:
                        if 'results' in a_line:
                            pass
                        elif 'result' in a_line:
                            if timed(a_line)>=815:
                                times.append(timed(a_line))
                        elif 'width' in a_line:
                            date=texts(a_line)
                            if check_date(date)==True:
                                dates.append(date)
                        elif str(int(year)-1) in a_line:
                            break
                elif year in a_line:
                    num+=1
            for i in range(0,len(dates)):
                split=dates[i].split(' ')
                if i!=0:
                    date1=datetime.date(int(year),month(split[0]),int(split[1]))
                    if date1<date2:
                        last_date_ran=dates[i-1]
                        break
                    else:
                        date2=date1
                else: 
                    date2=datetime.date(int(year),month(split[0]),int(split[1]))
            for i in range(0,len(dates)):
                if dates[i]==last_date_ran:
                    season_times=times[:i+1]
                    if name=='Lucas Swanson' or name=='Nevin Slater':
                        print(times)
                        print(dates)
                    season_best=min(season_times)
                    for j in range(0,len(season_times)):
                        if season_times[j]==season_best:
                            sb_date=dates[j]
                            break
                    break
            new_user(name,school,season_best,sb_date)
    line_count+=1

section_time("Done")
from dataset import vals as data
