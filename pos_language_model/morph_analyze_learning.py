#!/usr/bin/python
#-*-coding:utf-8-*-

import pickle, math, jctconv
from collections import defaultdict
from make_dict_obj import Morph
from morph_analyzer import *

def parameter_update(best_sequence, wdic_def, cccos_def, wdic, wvcos, cccos):
	"""
	入力:現在のパラメータによる結果の系列、その他パラメータ
	出力:更新されたパラメータ
	"""


def main():
	#辞書の読み込み
	dict_dir = "/Users/yukitomo/Research/jp_robust_morphame_analysis/data/mecab-ipadic-2.7.0-20070801-utf8/"
	pkl_dir = "/Users/yukitomo/Research/jp_robust_morphame_analysis/pkl_data/"
	print "loading dictionary"
	wdic_def = pickle.load(open(pkl_dir + "ipadic_word_dict.pkl", "r"))
	rpdic = pickle.load(open(pkl_dir + "ipadic_read_pron_dict.pkl", "r"))
	iddef_def = load_2colums(open(dict_dir + "left-id.def","r")," ") #mecabはr,l同じID
	wvcos_def = load_3colums_string(open(dict_dir + "wv_cost.def","r"),"\t")
	cccos_def = load_3colums_number(open(dict_dir + "matrix.def","r")," ")

	
	#web上の大量の文を形態素解析し、パラメータの更新を行う
	input_data = open("", "r")

	#初期値の設定　
	[wdic, wvcos, cccos] = [wdic_def, wvcos_def, cccos_def]

	for sent in input_data:
		lm = Lattice_Maker(wdic, rpdic, wvcos, cccos, iddef)
		lattice = lm.create_lattice(input_sent)
		best_sequence = lm.viterbi(lattice)
		[wdic, wvcos, cccos] = parameter_update(best_sequence, wdic_def, cccos_def, wdic, wvcos, cccos)



