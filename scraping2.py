import requests
from bs4 import BeautifulSoup
import pandas

req = requests.get('http://www.pythonhow.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/')
con = req.content

soup = BeautifulSoup(con, 'html.parser')

'''

all = points to the row/division that you are looking into for the information below.

'''
all = soup.find_all('div', {'class': 'propertyRow'})
#all[0].find('h4', {'class':'propPrice'}).text.replace('\n', '').replace(' ','')

#list of that will be append to later in the program
re_list = []

'''
In this loop your are narrowing you search
  to collect the specific data youare looking for.
'''
for items in all:

	# here is the dictionary the capture your data
	d = {}
	d['Price']= items.find('h4',{	'class':'propPrice'	}).text.replace('\n','').replace(' ','')
	d['address'] = items.find_all('span', {'class':'propAddressCollapse'})[0].text
	d['locality'] = items.find_all('span', {'class':'propAddressCollapse'})[1].text
	try:
		d['Bed'] = items.find('span', {'class': 'infoBed'}).find('b').text
	except: 
		d['Bed'] = None

	try:
		d['Area'] = items.find('span', {'class': 'infoSqft'}).find('b').text
	except:
		d['Area'] = None

	try:
		d['Full Bath'] = items.find('span', {'class': 'infoValueFullBath'}).find('b').text
	except:
		d['Full Bath'] = None

	for column_group in items.find_all('div', {'class': 'columnGroup'}):
		#print(column_group)
		for feature_group, feature_name in zip(column_group.find_all('span', {'class':'featureGroup'}), column_group.find_all('span',{'class': 'featureName'})):
			#print(feature_group.text, feature_name.text)
			if 'Lot Size' in feature_group.text:
				d['Lot Size'] = feature_name.text + '\n'
	
	re_list.append(d)

# creation of a dataframe used to organize our information
df = pandas.DataFrame(re_list)

# exporting data to a csv file
df.to_csv('Output.csv')
print('Success')