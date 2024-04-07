import requests
from bs4 import BeautifulSoup
import pandas as pd

url="https://www.iplt20.com/auction"
r=requests.get(url)
soup=BeautifulSoup(r.text,"lxml")

section=soup.find_all("section",class_="ih-points-table-sec position-relative")

#header-column values
header=(section[0].find("thead")).find_all("th")
column=[i.text for i in header]

#team-values
team_names=[i.h2.text for i in section]

#player-values
#added team names with every player-value {key-[[list]]}
index=0
ipl={}
for i in section:
    row=i.find_all("tr")
    team_players=[]
    for j in row[1:]:
        player=[]
        for k in j:
            text=k.text
            if text !='\n':
                player.append(text)
        team_players.append(player)
    ipl[team_names[index]]=team_players
    index=index+1

data=[]

#append team-name inside the list and move to data[]
for i in ipl:
    for j in ipl[i]:
        j.insert(0,i)
        data.append(j)

#convert to excel
df_columns = ['Team Name'] + column
df=pd.DataFrame(data,columns=df_columns)
df.to_excel('ipldetails.xlsx',index=False)

