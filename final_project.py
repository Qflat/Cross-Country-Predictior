import requests
import urllib.request
from bs4 import BeautifulSoup as bs
from tkinter import *
import datetime
from datetime import datetime as dt

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
    var_name=var_name.replace(' ','_')
    var_name=var_name.replace("'","_")
    f=open('dataset.py','a')
    f.write(var_name+'=Runner("'+name+'","'+school+'",'+str(sb)+',"'+sb_date+'")\n')
    f.close()

# Defining a few more variables that'll be important later
today=dt.today()
year=str(today.year)
a=lines(url,'a')
line_count=0
times=[]
f=open('dataset.py','w')
f.write('class Runner:\n\
    def __init__(self,name,school,season_best,sb_date):\n\
        self.name=name\n\
        self.school=school\n\
        self.season_best=season_best\n\
        self.sb_date=sb_date\n\
        self.days=self.day(self.sb_date)\n\
        self.best_time=self.time(self.season_best)\n\
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

# Run through each athlete to gather Data set, code sampled from 'https://github.com/julia-git/webscraping_ny_mta'
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
                    date1=datetime.date(2020,month(split[0]),int(split[1]))
                    if date1<date2:
                        last_date_ran=dates[i-1]
                        break
                    else:
                        date2=date1
                else:
                    date2=datetime.date(2020,month(split[0]),int(split[1]))
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
        elif 'result' in line:
            pass
    line_count+=1
