#query metadata
import json
import urllib2
from urllib2 import  Request #using python HTTP request
import time

url_suffix = 'https://api.github.com/users/'
url_appendix = '/gists'

my_token = "5fb5b1720992d5d7fe520fa248dadaa6807aa776"
def getGists(url):
	request = Request(url)
	request.add_header('Authorization', 'token %s' % my_token)
	try:
		return json.load(urllib2.urlopen(request))
	except:
		return False


with open("users_all.json", "r") as fp:
	users_all = json.load(fp)

with open("unreal_users.json", "r") as fp:
	unreal_users = json.load(fp)

with open("log.json", "r") as fp:
	log = json.load(fp)

with open("gists.json", "r") as fp:
	users_gists = json.load(fp)

with open("users_obtained.json", "r") as fp:
	users_obtained = json.load(fp)

with open("users_errors.json", "r") as fp:
	false_buffer = json.load(fp)


false_cnt = 0

try:

	while(len(users_all) > 0):
		if (users_all[0] in unreal_users):
			log['unreal'] += 1
			print users_all[0],'is unreal user'
			users_all.pop(0)
			continue
		if ((users_all[0] in users_obtained) or (users_all[0] in users_gists.keys())): 
			#print users_all[0],'already got it'
			users_all.pop(0)
			continue
		else:
			log['count'] += 1
			gists = []	
			gists_data = getGists(url_suffix + users_all[0] + url_appendix)
			
			if(gists_data != False):
				false_cnt = 0
				for j in range(len(gists_data)):
					gist = {}
					each = getGists(gists_data[j]['url'])
					if (each):
						false_cnt = 0
						if('fork_of' not in each.keys()): # those forks from other gists don't count
							gist['id'] = each['id']
							size_sum = 0
							language = []
							files = []
							for each_file in each['files']:
								onefile = {}
								onefile['size'] = each['files'][each_file]['size']
								size_sum += each['files'][each_file]['size']
								if (each['files'][each_file]['language'] != None):
									language.append(each['files'][each_file]['language'])
									onefile['language'] = each['files'][each_file]['language']
								files.append(onefile)
							gist['files'] = files
							gist['language'] = language
							gist['size'] = size_sum
							gist['files_count'] = len(each['files'])
							gist['comments'] = each['comments']
							gist['forks'] = len(each['forks'])
							gist['commits'] = len(each['history'])
							gist['created_at'] = each['created_at']
							gist['updated_at'] = each['updated_at']
							gist['description'] = each['description']
							commits = []
							if (gist['commits'] != 0):	
								for k in range(len(each['history'])):
									if(len(each['history'][k]['change_status']) != 0):
										commits.append(each['history'][k]['change_status'])
							gist['commits_history'] = commits
							gists.append(gist)
				if(gists==[]):
					log['empty'] += 1
				users_gists[users_all[0]] = gists
				log['success'] += 1
				print users_all[0], "OK"
				users_all.pop(0)

			else:
				false_cnt += 1
				log['error'] += 1
				print users_all[0],'failed'
				false_buffer.insert(0,users_all.pop(0))				
				if(false_cnt >= 50):					
					with open('users_errors.json', 'wb') as fp3:
						json.dump(false_buffer, fp3)
					time.sleep(600)
					false_cnt = 0
				

	with open('gists.json', 'wb') as fp:
		json.dump(users_gists, fp)
	with open('log.json', 'wb') as fp:
		json.dump(log, fp)
	with open('users_errors.json', 'wb') as fp:
		json.dump(false_buffer, fp)
	with open('users_all.json', 'wb') as fp:
		json.dump(users_all, fp)

except KeyboardInterrupt:
	with open('gists.json', 'wb') as fp:
		json.dump(users_gists, fp)
	with open('log.json', 'wb') as fp:
		json.dump(log, fp)
	with open('users_errors.json', 'wb') as fp:
		json.dump(false_buffer, fp)
	with open('users_all.json', 'wb') as fp:
		json.dump(users_all, fp)
