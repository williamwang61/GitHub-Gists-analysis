from os import listdir
import csv
import math

code_lines = {}
files_count = 0
for f in listdir("gists_files_cloc_analysis_result"):
	with open("gists_files_cloc_analysis_result/"+f, 'rb') as csvfile:
		lines = csv.reader(csvfile)
		header = lines.next()
		num_code = 0
		for line in lines:
			files_count += 1
			num_code += int(line[4])
		
		if num_code not in code_lines.keys():
			code_lines[num_code] = 1
		else:
			code_lines[num_code] += 1


lines_code_dist_sorted = sorted(code_lines.items(), key = lambda x:x[0])
headers = []
for k,v in lines_code_dist_sorted:
	headers.append(k)

code_lines_dist = {}
code_lines_dist_cumu = {}
last_value = 0
for each in lines_code_dist_sorted:
	percentage = each[1]/float(files_count)
	code_lines_dist[each[0]] = percentage
	cumu = percentage + last_value
	code_lines_dist_cumu[each[0]] = cumu
	last_value = cumu

with open('stat_cloc_code_lines.csv', 'wb') as f:
	w = csv.DictWriter(f, headers)
	w.writeheader()
	w.writerow(code_lines)
	w.writerow(code_lines_dist)
	w.writerow(code_lines_dist_cumu)

log_index = 0
log_result = {}
for each in headers:
	if each >= math.pow(2,log_index):
		log_result[log_index] = code_lines_dist_cumu[each]
		log_index += 1
with open('stat_cloc_code_lines_log.csv', 'wb') as f:
    w = csv.DictWriter(f, log_result.keys())
    w.writeheader()
    w.writerow(log_result)

