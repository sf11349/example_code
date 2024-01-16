# Importing the required modules 
#import os
#import sys
import pandas as pd
from bs4 import BeautifulSoup
import requests

html_text = requests.get('https://www.expatistan.com/cost-of-living/country/saudi-arabia').text
#t.sleep(3)
#print(html_text)

# create a soup class
soup = BeautifulSoup(html_text,'html.parser')



#path = 'html.html'

# empty list
data = []

# for getting the header from
# the HTML file
list_header = []
#soup = BeautifulSoup(open(path),'html.parser')
header = soup.find_all("table")[0].find("tr")

for items in header:
	try:
		list_header.append(items.get_text())
	except:
		continue

# for getting the data 
HTML_data = soup.find_all("table")[0].find_all("tr")[1:]
print(HTML_data)

for element in HTML_data:
	sub_data = []
	for sub_element in element:
		try:
			txt = str(sub_element.get_text()).replace('\n','')
			if len(txt) > 0:
				sub_data.append(txt.replace("  ",""))
		except:
			continue
	data.append(sub_data)

# Storing the data into Pandas
# DataFrame 
#dataFrame = pd.DataFrame(data = data, columns = list_header)
dataFrame = pd.DataFrame(data = data)

# Converting Pandas DataFrame
# into CSV file
dataFrame.to_csv('new_data.csv')
