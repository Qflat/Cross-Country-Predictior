import requests
import urllib.request
from bs4 import BeautifulSoup as bs
from tkinter import *

class Runner:
    def __init__(self,season_best,date_ran):
        self.season_best=season_best
        self.date_ran=date_ran
        self.time=self.simplify(self.season_best)

    def simplify(self,season_best):
        a=season_best.split(':')
        for i in range(0,len(a)):
            a[i]=int(a[i])
        while a[0]>0:
            a[0]-=1
            a[1]+=60
        return a[1]

class Webpage:
    def __init__(self,master):
        self.master=master
        master.title('Web Results')
        master.label=Label(text='Please insert the seasons best list you\'d like to evaluate: ')
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

# Gather information from global variable url
response=requests.get(url)
content=bs(response.text,"html.parser")
a=content.findAll('a')
line_count=0
for line in a:
    line=str(line)
    if line_count>=15:  # Results for Athletic.net Start at Line 15
        if 'Athlete' in line:
            # Athlete Info
            splitted=line.split('>')
            val=splitted[1]
            name_val=val.split('<')
            name=name_val[0]
            print(name)
        elif 'meet' in line:
            # Meet Name
            pass
        elif 'result' in line:
            # Result Info
            print(line)
        elif 'School' in line:
            # School Info
            pass
        elif 'pr-text' in line:
            pass    # Empty Hyperlink on Athletic.net
        else:
            break   # End of Athlete list on Athletic.net
    line_count+=1
