from os import listdir
import csv
import math

files_count = 0
lines_count = 0
num_lines = {}
for f in listdir("gists_files_text_only"):
	files_count += 1
	print files_count
	lines = sum(1 for line in open('gists_files_text_only/' + f))
	lines_count += lines
	if lines not in num_lines.keys():
		num_lines[lines] = 1
	else:
		num_lines[lines] += 1

num_lines_sorted = sorted(num_lines.items(), key = lambda x:x[0])
headers = []
for each in num_lines_sorted:
	headers.append(each[0])

num_lines_dist = {}
num_lines_dist_cumu = {}
last_value = 0
for each in num_lines_sorted:
	percentage = each[1]/float(files_count)
	num_lines_dist[each[0]] = percentage
	cumu = percentage + last_value
	num_lines_dist_cumu[each[0]] = cumu
	last_value = cumu

with open('stat_files_lines_text_only.csv', 'wb') as f:
    w = csv.DictWriter(f, headers)
    w.writeheader()
    w.writerow(num_lines)
    w.writerow(num_lines_dist)
    w.writerow(num_lines_dist_cumu)

log_index = 0
log_result = {}
for each in headers:
	if each >= math.pow(2,log_index):
		log_result[log_index] = num_lines_dist_cumu[each]
		log_index += 1
with open('stat_files_lines_text_only_log.csv', 'wb') as f:
    w = csv.DictWriter(f, log_result.keys())
    w.writeheader()
    w.writerow(log_result)
	