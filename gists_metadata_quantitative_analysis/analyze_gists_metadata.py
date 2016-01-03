#### Parameters ######
filename = "gists_meta/gists_meta_618,393_of_177.297_users.json"
######################

import json
import os
import csv
import operator
import math
from datetime import datetime
# go to root foler
os.chdir("..")

def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%Y-%m-%dT%H:%M:%SZ")
    d2 = datetime.strptime(d2, "%Y-%m-%dT%H:%M:%SZ")
    return abs((d2 - d1).days)

with open(filename, 'r') as fp:
	data = json.load(fp)

forks = {}
commits = {}
comments = {}
files = {}
update_create_diff = {}
gists_count = 0
for item in data:
	gists_count += len(item['gists'])
	for gist in item['gists']:
		
		gist_commits = gist['commits']
		if gist_commits in commits.keys():
			commits[gist_commits] += 1
		else:
			commits[gist_commits] = 1

		gist_comments = gist['comments']
		if gist_comments in comments.keys():
			comments[gist_comments] += 1
		else:
			comments[gist_comments] = 1

		gist_forks = gist['forks']
		if gist_forks in forks.keys():
			forks[gist_forks] += 1
		else:
			forks[gist_forks] = 1

		gist_files = gist['files_count']
		if gist_files in files.keys():
			files[gist_files] += 1
		else:
			files[gist_files] = 1

		gist_update_create_diff = days_between(gist['created_at'], gist['updated_at'])
		if gist_update_create_diff in update_create_diff.keys():
			update_create_diff[gist_update_create_diff] += 1
		else:
			update_create_diff[gist_update_create_diff] = 1


def export_result(result, label, logScale=False):
	for k,v in result.items():
		result[k] = float(v)/gists_count
	
	result_sorted = sorted(result.iteritems(), key=operator.itemgetter(0))
	
	headers = []
	last_value = 0
	result_cumu = {}
	for each in result_sorted:
		headers.append(each[0])
		temp = last_value + each[1]
		result_cumu[each[0]] = temp
		last_value = temp
	with open('gists_meta_analysis/stat_gists_meta_' + label + '.csv', 'wb') as f:
		w = csv.DictWriter(f, headers)
		w.writeheader()
		w.writerow(result)
		w.writerow(result_cumu)
	if logScale:
		result_log = {}
		result_log_index = 0
		for each in headers:
			if each >= math.pow(2,result_log_index):
				result_log[result_log_index] = result_cumu[each]
				result_log_index += 1
		with open('gists_meta_analysis/stat_gists_meta_' + label + '_log.csv', 'wb') as f:
			w = csv.DictWriter(f, result_log.keys())
			w.writeheader()
			w.writerow(result_log)


export_result(commits, "commits", True)
export_result(comments, "comments", True)
export_result(files, "files", True)
export_result(forks, "forks", True)
export_result(update_create_diff, "update_create_diff", True)
