from bs4 import BeautifulSoup
import requests
import time as t
import pandas as pd
import sys

# get the html data
html_text = requests.get('https://www.expatistan.com/cost-of-living/country/kuwait').text
#t.sleep(3)
#print(html_text)

# create a soup class
soup = BeautifulSoup(html_text,'lxml')

# cat_head = soup.find('tr', class_ = 'categoryHeader')
# print(cat_head)

# cat_name = cat_head.find('th', colspan_ = '2')
# print (cat_name)

html_table = soup.find( "table", {"class":"comparison single-city"} )

cats=list()
for cat in html_table.findAll("tr"):
   #print(row)
   cats.append(cat)

with open('cats.txt', 'w') as f:
    print(cats, file=f)

with open('tbl.txt', 'w') as f:
    print(html_table, file=f)
   


