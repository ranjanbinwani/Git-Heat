import requests
import bs4

from decimal import Decimal
from base64 import b64encode, b64decode
from json import dump, dumps, load, loads, JSONEncoder,JSONDecodeError
import pickle
import sys
stdout = sys.stdout

class PythonObjectEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (list, dict, str, int, float, bool, type(None))):
            return super().default(obj)
        return {'_python_object': b64encode(pickle.dumps(obj)).decode('utf-8')}

def as_python_object(dct):
    if '_python_object' in dct:
        return pickle.loads(b64decode(dct['_python_object'].encode('utf-8')))
    return dct

train_no = input('Enter the Train Number: ')

filename = train_no + '.json'

try:

	url = "https://enquiry.indianrail.gov.in/xyzabc/ShowTrainSchedule?trainNo=" + train_no;
	response = requests.get(url)
	html = response.text
	soup = bs4.BeautifulSoup(html, "html.parser")
	# print(soup)
	train_table = soup.find("table", {"id": "trnSchDataTbl"})
	# print(train_table)
	table_content = train_table.find_all('tr')
	# print(table_content)

	stoppage = []
	day = []
	arrival = []
	departure = []
	distance = []

	# print(len(table_content))
	cnt = 1
	for row in table_content:

		table_data = row.find_all('td')
		# print(table_data)
		# break
		# for data in table_data:
			# print(data)
		stop = str(table_data[1])
		stop = bs4.BeautifulSoup(stop,'lxml')
		# print(stop.find('td').contents[0])
		stoppage.append(stop.find('td').contents[0])

		
		stop = str(table_data[2])
		stop = bs4.BeautifulSoup(stop,'lxml')
		# print(stop.find('td').contents[0])
		day.append(stop.find('td').contents[0])

		stop = str(table_data[3])
		stop = bs4.BeautifulSoup(stop,'lxml')
		# print(stop)
		# print(stop.find(class_='arrDepTime').contents[0])
		if(stop.find_all(class_='arrDepTime')[0]):
			if(cnt==1):
				departure.append(stop.find_all(class_='arrDepTime')[0].contents[0])
				arrival.append('')
			elif(cnt==len(table_content)):
				arrival.append(stop.find_all(class_='arrDepTime')[0].contents[0])
				departure.append('')
			else:
				arrival.append(stop.find_all(class_='arrDepTime')[0].contents[0])

		else:
			arrival.append('')
		
		if(cnt!=len(table_content) and cnt!=1):
			stop = str(table_data[3])
			stop = bs4.BeautifulSoup(stop,'lxml')
			# print(stop.find(class_='arrDepTime').contents[0])
			if(stop.find_all(class_='arrDepTime')[1]):
				departure.append(stop.find_all(class_='arrDepTime')[1].contents[0])
			else:
				departure.append('')

		stop = str(table_data[4])
		stop = bs4.BeautifulSoup(stop,'lxml')
		# print(stop.find('td').contents[0])
		distance.append(stop.find('td').contents[0])

		cnt+=1

	output = dict()

	for idx in range(0,len(table_content)):
		output.update({str(idx+1):{stoppage[idx],day[idx],arrival[idx],departure[idx],distance[idx]}})

	


	sys.stdout = open(filename, 'w')
	j = dumps(output, cls=PythonObjectEncoder)
	print(loads(j, object_hook=as_python_object))
	sys.stdout = stdout

	print('Output saved to ' + filename)

except IndexError as e:
        print("No such Train found.")

except requests.ConnectionError as e:
    print("Connection Error occurred. Looking for data in local storage..")

    try:
        f = open(filename,'r')
        # print(load(f))
        f.close()
        print('File ' + filename + ' already present')

    except FileNotFoundError as e:
        print("Internet Connection is required to fetch Train Info.")

    except JSONDecodeError as e:
        print("Internet Connection is required to fetch Train Info.")


# print(stoppage)
# print(day)
# print(arrival)
# print(departure)
# print(distance)
# print(output)