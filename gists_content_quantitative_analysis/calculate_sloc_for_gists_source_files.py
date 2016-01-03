from os import listdir
import csv

lines_code_dist = {}
lines_total_dist = {}
for f in listdir("cloc_result"):
	with open("cloc_result/"+f, 'rb') as csvfile:
		lines = csv.reader(csvfile)
		header = lines.next()
		num_files = 0
		num_blank = 0
		num_comment = 0
		num_code = 0
		num_total_lines = 0
		for line in lines:
			num_files += int(line[0])
			num_blank += int(line[2])
			num_comment += int(line[3])
			num_code += int(line[4])
			num_total_lines += num_blank + num_code + num_comment
		
		if num_code not in lines_code_dist.keys():
			lines_code_dist[num_code] = 1
		else:
			lines_code_dist[num_code] += 1

		if num_total_lines not in lines_total_dist.keys():
			lines_total_dist[num_total_lines] = 1
		else:
			lines_total_dist[num_total_lines] += 1


lines_code_dist_sorted = sorted(lines_code_dist.items(), key = lambda x:x[0])
headers = []
for k,v in lines_code_dist_sorted.items():
	headers.append(k)

with open('stat_cloc_code_lines.csv', 'wb') as f:
	w = csv.DictWriter(f, headers)
	w.writeheader()
	w.writerow(lines_code_dist)


lines_total_dist_sorted = sorted(lines_total_dist.items(), key = lambda x:x[0])
headers = []
for k,v in lines_total_dist_sorted.items():
	headers.append(k)

with open('stat_cloc_total_lines.csv', 'wb') as f:
    w = csv.DictWriter(f, headers)
    w.writeheader()
    w.writerow(lines_total_dist)