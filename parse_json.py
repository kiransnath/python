from urllib2 import urlopen
import json

print ('Starting the JSON operations. First is to hit the URL')

url = 'http://jsonplaceholder.typicode.com/posts'

response = urlopen(url)
json_object = json.load(response);
id_sum = 0

for i in json_object:
	id_sum = id_sum + i['id']

print 'Sum of ids is {}'.format(id_sum)
