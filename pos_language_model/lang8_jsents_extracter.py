#!/usr/bin/python
#-*-coding:utf-8-*-
#2015-02-16 Yuki Tomo

import json
import re

lang8_file = open('/Users/yukitomo/Research/jp_robust_morphame_analysis/data/lang-8-20111007-2.0/lang-8-20111007-L1-v2-Japanese.dat', 'r')

hira = re.compile(r"[あ-ん]")

for line in lang8_file:
	#print line
	try:
		load_obj = json.loads(line)

		for str_list in load_obj[5]:
			#print str_list
			for string in str_list:
				#print string
				if hira.search(string):
					print string
					#print " "
				else:pass

	except:
		pass

#print json.dumps(jsonData, sort_keys = True, indent = 4)

lang8_file.close()