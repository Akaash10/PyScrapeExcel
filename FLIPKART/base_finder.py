import requests
from bs4 import BeautifulSoup

def findLink(url,page):
    r=requests.get(url)
    soup=BeautifulSoup(r.text,"lxml")
    link=""
    if page==0:
        a=soup.find("a",class_="_1LKTO3")
        link="https://www.flipkart.com"+a.attrs["href"]
    else:
        arr=soup.find_all("a",class_="_1LKTO3")
        if len(arr)<2:
            return None
        a=arr[1]
        link="https://www.flipkart.com"+a.attrs["href"]
    return link

url="https://www.flipkart.com/search?q=noise+n1+tws&sid=0pm%2Cfcn%2C821%2Ca7x%2C2si&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_1_8_na_na_ps&otracker1=AS_QueryStore_OrganicAutoSuggest_1_8_na_na_ps&as-pos=1&as-type=RECENT&suggestionId=noise+n1+tws%7CTrue+Wireless&requestId=25df8cda-6fbc-4c3f-b653-a66a6f507e48&as-backfill=on&page=1"

page=0
lists=[]
lists.append(url)
condition=True

while condition:
    next_link = findLink(lists[page], page)
    if next_link is not None:
        lists.append(next_link)
        page += 1
    else:
        condition=False

for i in lists:
    print(i)