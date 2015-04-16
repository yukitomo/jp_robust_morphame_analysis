#!/usr/bin/python
#-*-coding:utf-8-*-
#2015-02-16 Yuki Tomo

import json
import re
import difflib

lang8_file = open('/Users/yukitomo/Research/jp_robust_morphame_analysis/data/lang-8-20111007-2.0/lang-8-20111007-L1-v2_short.dat', 'r')

hira = re.compile(ur"[あ-ん]")
headder = re.compile(ur"\[/?[a-z]*-?[a-z]*\]")

for line in lang8_file:
	#print line
	try:
		load_obj = json.loads(line)

		if load_obj[2] == "Japanese":
			#元の文
			#print "SOURCE SENTS"
			source_sents = []
			for string in load_obj[4]:
				#print string.encode('utf-8')
				if hira.search(string):
					print string.encode('utf-8')
					#source_sents.append(string)
		#print ""
	except:
		pass

lang8_file.close()

