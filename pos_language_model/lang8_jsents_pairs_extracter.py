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
					#print string.encode('utf-8')
					source_sents.append(string)

			#訂正文
			#[]を除去
			#print "CORRECTION SENTS"
			correct_sents = []
			for sent_list in load_obj[5]:
				for sent in sent_list:
					if hira.search(sent):
						#sent = headder.sub('',sent)
						#print sent.encode('utf-8')
						correct_sents.append(sent)


			#source_sents, correct_sents 中のペアを抽出
			pair_list = []
			for source_sent in source_sents:
				index = 0
				most_similar_sent_index = 0
				max_score = 0

				for correct_sent in correct_sents:
					score = difflib.SequenceMatcher(None, source_sent, correct_sent).ratio()
					if score > max_score:
						max_score = score
						most_similar_sent_index = index
					index += 1

				most_similar_sent = correct_sents[most_similar_sent_index]

				if source_sent != most_similar_sent:
					pair_list.append((source_sent.encode('utf-8'), most_similar_sent.encode('utf-8')))

			for pair in pair_list:
				print "source : " + pair[0]
				print "correct : " + pair[1]
		print ""
	except:
		pass

lang8_file.close()

