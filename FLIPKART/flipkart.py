import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

#url and response 
url=[]
url.append("https://www.flipkart.com/search?q=apple+mobiles&sid=tyy%2C4io&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_1_10_na_na_ps&otracker1=AS_QueryStore_OrganicAutoSuggest_1_10_na_na_ps&as-pos=1&as-type=RECENT&suggestionId=apple+mobiles%7CMobiles&requestId=27da51f3-59e3-4e91-a4bc-9cd4127ac164&as-backfill=on")
url.append("https://www.flipkart.com/search?q=samsung+mobiles&sid=tyy%2C4io&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_2_4_na_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_2_4_na_na_na&as-pos=2&as-type=RECENT&suggestionId=samsung+mobiles%7CMobiles&requestId=eedcb30d-9e44-4b87-9d8c-8931870ed8fa&as-backfill=on&page=1")
url.append("https://www.flipkart.com/search?q=mi+mobile&sid=tyy%2C4io&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_2_10_na_na_ps&otracker1=AS_QueryStore_OrganicAutoSuggest_2_10_na_na_ps&as-pos=2&as-type=RECENT&suggestionId=mi+mobile%7CMobiles&requestId=fdf7b47a-0120-4cb8-ae62-75a4b9bf91cc&as-backfill=on")

#find links
links=[]
for i in url:
    #conversion of raw text into html parse document
    r=requests.get(i)
    soup=BeautifulSoup(r.text,"lxml")
    a=soup.find_all("a",class_="ge-49M")
    for j in a:
        links.append("https://www.flipkart.com"+j.attrs["href"])

#iterate through links
names,prices,stars,ratings,reviews,descriptions=[],[],[],[],[],[]
header=["Name","Price","Star-Rating","Total-Ratings","Reviews","Description"]

for i in links:
    request=requests.get(i)
    bs=BeautifulSoup(request.text,"lxml")
    rows=bs.find_all("div",class_="_13oc-S")
    for j in rows:
        #Name of the product
        names.append((j.find("div",class_="_4rR01T")).text) 

        #Price of the product      
        try:
            price_element = j.find("div", class_="_30jeq3 _1_WHN1")
            if price_element is not None:
                prices.append(price_element.text.strip())
            else:
                prices.append("Not defined")
        except AttributeError:
            prices.append("Not defined")

        #Star-Ratings of the product
        try:
            star_element = j.find("div", class_="_3LWZlK")
            if star_element is not None:
                stars.append(star_element.text.strip())
            else:
                stars.append("Not defined")
        except AttributeError:
            stars.append("Not defined")
        
        #Ratings and Reviews of the product
        review_div=((j.find("span",class_="_2_R_DZ")).find_all("span")[1:4])
        review_arr=[k.text for k in review_div]
        ratings.append(review_arr[0])
        reviews.append(review_arr[2])

        #Description of the product
        description_div=(j.find("ul",class_="_1xgFaf"))
        description=""
        for i in description_div.find_all("li"):
            description+=(i.text)
        descriptions.append(description)

products=[]
for i in range(len(names)):
    data=[]
    data.append(names[i])
    data.append(prices[i])
    data.append(stars[i])
    data.append(ratings[i])
    data.append(reviews[i])
    data.append(descriptions[i])
    products.append(data)


# Check if the file exists
file_name = "flipkart.xlsx"
file_path = os.path.join(os.getcwd(), file_name)

if os.path.exists(file_path):
    existing_sheets = pd.ExcelFile(file_path).sheet_names
    last_sheet_number = int(existing_sheets[-1].replace("Sheet", ""))
    new_sheet_name = f"Sheet{last_sheet_number + 1}"
    df = pd.DataFrame(products, columns=header)
    with pd.ExcelWriter(file_path, engine='openpyxl', mode='a') as writer:
        df.to_excel(writer, sheet_name=new_sheet_name, index=False)
else:
    df = pd.DataFrame(products, columns=header)
    df.to_excel(file_path, index=False)