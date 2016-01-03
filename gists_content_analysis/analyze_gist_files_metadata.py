import json
import csv
import operator
import math
import os
# go to root foler
os.chdir("..")

type = {}
size = {}
language = {}
files_sum = 0

for i in range(64):
	with open('gists_content/gists_content_' + str(i) + '.json','r') as f:
		data = json.load(f)
		for gist in data:
			files_sum += len(gist['files'])
			for file in gist['files']:
				if file['type'] not in type.keys():
					type[file['type']] = 0
				type[file['type']] += 1
				
				if file['size'] not in size.keys():
					size[file['size']] = 0
				size[file['size']] += 1
				
				if file['language'] not in language.keys():
					language[file['language']] = 0
				language[file['language']] += 1

def export_result(result, label, sort_key, reverse_sort=False, logScale=False):
	for k,v in result.items():
		result[k] = float(v)/files_sum
	
	result_sorted = sorted(result.iteritems(), key=operator.itemgetter(sort_key), reverse = reverse_sort)
	
	headers = []
	last_value = 0
	result_cumu = {}
	for each in result_sorted:
		headers.append(each[0])
		temp = last_value + each[1]
		result_cumu[each[0]] = temp
		last_value = temp
	with open('gists_content_analysis/stat_gists_content_' + label + '.csv', 'wb') as f:
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
		with open('gists_content_analysis/stat_gists_content_' + label + '_log.csv', 'wb') as f:
			w = csv.DictWriter(f, result_log.keys())
			w.writeheader()
			w.writerow(result_log)

export_result(language, "language", sort_key=1, reverse_sort = True)
export_result(size, "size", sort_key=0, reverse_sort = False, logScale=True)
export_result(type, "type", sort_key=1, reverse_sort = True)