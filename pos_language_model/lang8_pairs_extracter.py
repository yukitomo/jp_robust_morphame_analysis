#!/usr/bin/python
#-*-coding:utf-8-*-
#2015-02-16 Yuki Tomo

import json
import re
import difflib

lang8_file = open('/Users/yukitomo/Research/jp_robust_morphame_analysis/data/lang-8-20111007-2.0/lang-8-20111007-L1-v2_short.dat', 'r')

hira = re.compile(ur"[あ-ん]")
headder = re.compile(ur"\[/?[a-z]*-?[a-z]*\]")
sline = re.compile(ur"\[sline\].*\[/sline\]")

for line in lang8_file:
	#print line
	try:
		load_obj = json.loads(line)

		if load_obj[2] == "Japanese":
			index = 0
			sent_pairs = []
			for string in load_obj[4]:
				#print string.encode('utf-8')
				if hira.search(string):
					#print string.encode('utf-8')
					correct_sents = load_obj[5][index]
					if not correct_sents == []:
						#print correct_sents[0].encode('utf-8')
						correct_sent = correct_sents[0]
						correct_sent = sline.sub('',correct_sent)
						correct_sent = headder.sub('',correct_sent)
						#print correct_sent.encode('utf-8')
						sent_pairs.append((string.encode('utf-8'), correct_sent.encode('utf-8')))
				index += 1 

			for pair in sent_pairs:
				print "source  : " + pair[0]
				print "correct : " + pair[1]
				print ""
	except:
		pass

lang8_file.close()
