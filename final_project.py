import requests
import urllib.request
from bs4 import BeautifulSoup as bs
from tkinter import *
from datetime import datetime

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

# Gather information from variable url
def lines(url,search):
    response=requests.get(url)
    content=bs(response.text,"html.parser")
    val=content.findAll(search)
    return val

def text(line):
    splitted=line.split('>')
    val=splitted[1]
    new_val=val.split('<')
    final_val=new_val[0]
    return final_val

today=datetime.today()
year=str(today.year)
a=lines(url,'a')
line_count=0
for line in a:
    line=str(line)
    if line_count>=58:  # Team Information Begins on Line 58 in Hypothetical Meet Page
        if 'javascript' in line:
            break   # Results Completed
        if 'School' in line:    # School Name
            school=text(line)
        elif 'Athlete' in line: # Athlete Name
            name=text(line)
            athlete_page=lines("https://www.athletic.net/CrossCountry/"+line[12:37],'td')
            num=0
            dates=[]
            for a_line in athlete_page:
                if num>0:
                    if num<=3:
                        num+=1
                    else:
                        if 'meet' in a_line:
                            pass
                        elif 'result' in a_line:
                            time=text(a_line)
                        elif 'width' in a_line:
                            print("running")
                            date=text(a_line)
                            dates.append(date)
                        elif 'appC' in a_line:
                            break
                elif year in a_line:
                    num+=1
        elif 'result' in line:  # Time Information
            pass
        #print(line)
        #for a_line in athlete_page:
    line_count+=1
