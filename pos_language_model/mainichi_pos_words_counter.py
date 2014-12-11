#!/usr/bin/python
#-*-coding:utf-8-*-
#author : Yuki TOMO

import sys,MeCab,pickle,glob
from collections import defaultdict

def mecab_input(txt,posid_bigram_counts,posid_word_counts): #一行（複数分）の品詞連接、単語生成回数を数える
	mecab = MeCab.Tagger("mecabrc")
	node = mecab.parseToNode(txt)
	previous_posid = "B" #前の品詞の初期化
	while node:
		#print "単語:", node.surface
		#print "品詞ID",node.posid
		#print "形態素：",node.feature
		current_posid = node.posid
		current_surface = node.surface
		posid_bigram_counts[previous_posid][current_posid] = posid_bigram_counts[previous_posid].get(current_posid,0) + 1 
		posid_word_counts[current_posid][current_surface] = posid_word_counts[current_posid].get(current_surface,0) + 1
		previous_posid = node.posid
		node = node.next
	return [posid_bigram_counts, posid_word_counts]

def mainichi_txt_inputter(data,posid_bigram_counts,posid_word_counts):
	for line in data:
		type_txt = line.strip().split("＼") #["", "T2"]
		if type_txt[1] == "Ｔ２" or type_txt[1] == "Ｓ２":
			#print "txt:",type_txt[2] #text
			[posid_bigram_counts, posid_word_counts] = mecab_input(type_txt[2], posid_bigram_counts, posid_word_counts)
	return [posid_bigram_counts, posid_word_counts]


def main():
	"""
	input : MAI*_~.TXT.utf8 毎日新聞のデータ
	output : posid_bigram_counts(品詞bigram), posid_word_counts(品詞から単語の生成) 
	"""
	#txt = open(sys.argv[1]) #MAINICHI_SHINBUN
	dir_address = sys.argv[1]
	txts = glob.glob(dir_address + "/*.utf8") #/work/nldata/mainichi
	print txts

	posid_bigram_counts = defaultdict(dict)
	posid_word_counts = defaultdict(dict)

	for txt in txts:
		[posid_bigram_counts, posid_word_counts] = mainichi_txt_inputter(open(txt,"r"), posid_bigram_counts, posid_word_counts)

	pickle.dump(posid_bigram_counts,open("posid_bigram_counts.pkl","w"))
	pickle.dump(posid_word_counts,open("posid_word_counts.pkl","w"))

if __name__ == '__main__':
	main()