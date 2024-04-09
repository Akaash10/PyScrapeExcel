from bs4 import BeautifulSoup
import pandas as pd

#Response<504> -> service unavailable, handled through file handling
with open("amazon.html","r",encoding="utf8")as f:
    html_content=f.read()

#parsing to html document
soup=BeautifulSoup(html_content,"lxml")
li=soup.find_all("li","octopus-pc-item octopus-pc-item-v3")

#converting to details
products=[]
for i in li:
    container=[]
    name=(i.find("span","a-size-base a-color-base").text).strip()
    price=(i.find("span","a-price-whole").text)[:-1]
    purchased=i.find("span","a-size-mini a-color-tertiary").text.strip()
    star=((i.find("span","a-icon-alt").text).split(" "))[0]
    container.append(name)
    container.append(price)
    container.append(purchased)
    container.append(str(star)+"/5")
    products.append(container)

#converting to xlsx
headers=["Product Name","Product Price","Total Purchased","Star Rating"]
df=pd.DataFrame(products,columns=headers)
df.to_excel("amazondetails.xlsx")
