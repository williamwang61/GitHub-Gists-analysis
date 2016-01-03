######## Parameters ###########
export_text_only = False
###############################

import json
import os
import string
# go to root foler
os.chdir("..")

def format_filename(s):
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    filename = ''.join(c for c in s if c in valid_chars)
    filename = filename.replace(' ','_') # I don't like spaces in filenames.
    return filename

export_count = 0
file_count = 0

data_chunk_count = 0
while(data_chunk_count<64):
	with open("gists_content/gists_content_" + str(data_chunk_count)+".json", 'r') as fp:
		gists = json.load(fp)
		for gist in gists:
			file_count += len(gist['files'])
			for eachfile in gist['files']:
				if export_text_only == False or (eachfile['type'].startswith('application') or eachfile['type'].startswith('text')):
					formatted_filename = format_filename(eachfile['filename'])
					if len(formatted_filename)>100:
						formatted_filename = formatted_filename[len(formatted_filename)-20 : len(formatted_filename)-1]
					with open('gists_content_analysis/gists_files_text_only/' + gist['id'] + '_' + formatted_filename, 'w') as f:
						f.write(eachfile['content'].encode('utf8'))
						export_count += 1
	data_chunk_count += 1

print 'Number of files in total :', file_count
print 'Number of files successfully exported :', export_count
