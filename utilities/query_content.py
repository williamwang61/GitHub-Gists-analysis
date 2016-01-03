#query gists content by http request

import json
import urllib2
from urllib2 import  Request #using python HTTP request
import time
import re


url_suffix = 'https://api.github.com/gists/'

my_token = "5fb5b1720992d5d7fe520fa248dadaa6807aa776"

def getGists(url):
	request = Request(url)
	request.add_header('Authorization', 'token %s' % my_token)
	try:
		return json.load(urllib2.urlopen(request))
	except:
		return False


with open("gistsToQuery.json", "r") as fp:
	users_gists = json.load(fp)

with open("log.json", "r") as fp6:
	log = json.load(fp6)

with open("gists_content_" + str(log['file_cnt']) + ".json", "r") as fp2:
	result = json.load(fp2)

false_cnt = 0

try:

	while(len(users_gists) > 0):		
		isSuccess = True		
		while(len(users_gists[0]['gists'])>0):
			idd = users_gists[0]['gists'][0]
			document = {}
			document['user'] = users_gists[0]['user']
			document['id'] = idd
			url = url_suffix + idd
			content = getGists(url)
			if(content != False):
				false_cnt = 0
				isSuccess = True
				files = []
				for eachFile in content['files']:
					each = {}
					each['filename'] = content['files'][eachFile]['filename']
					each['type'] = content['files'][eachFile]['type']
					each['language'] = content['files'][eachFile]['language']
					each['size'] = content['files'][eachFile]['size']
					if(re.match('^image/',each['type']) == None):
						each['content'] = content['files'][eachFile]['content']
					else:
						each['content'] = ""
					files.append(each)
				document['files'] = files
				result.append(document)
				users_gists[0]['gists'].pop(0)
				if(len(result) >= 10000):
					with open('gists_content_' + str(log['file_cnt']) + '.json', 'wb') as fp3:
						json.dump(result, fp3)
					result = []
					log['file_cnt'] += 1


			else:
				isSuccess = False
				false_cnt += 1
				users_gists[0]['gists'].insert(len(users_gists[0]['gists'])-1, users_gists[0]['gists'].pop(0))
				print users_gists[0]['user'], idd, "failed"			
				time.sleep(60)
				if(false_cnt>=10):
					false_cnt = 0
					users_gists.insert(len(users_gists)-1, users_gists.pop(0))
					break
					
		if(isSuccess == True):
			log['count'] += 1			
			print users_gists[0]['user'], "succeeded"
			users_gists.pop(0)

	with open('log.json', 'wb') as fp3:
		json.dump(log, fp3)
	with open('gists_content_' + str(log['file_cnt']) + '.json', 'wb') as fp3:
		json.dump(result, fp3)
	with open('gistsToQuery.json', 'wb') as fp3:
		json.dump(users_gists, fp3)

except KeyboardInterrupt:
	with open('log.json', 'wb') as fp3:
		json.dump(log, fp3)
	with open('gists_content_' + str(log['file_cnt']) + '.json', 'wb') as fp3:
		json.dump(result, fp3)
	with open('gistsToQuery.json', 'wb') as fp3:
		json.dump(users_gists, fp3)
